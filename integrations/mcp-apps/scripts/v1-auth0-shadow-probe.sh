#!/usr/bin/env bash
# Stage-only Auth0 resource server probe, using the already-accepted source.
# No external exposure, Auth0 account edits, Google Drive, Nginx, systemd,
# production tree, E05, secrets, merges or release/publish mutations.
# Run as root only after verifying the SHA of this script.
set -Eeuo pipefail
umask 077

STAGE="/opt/meu-artigo-v1-acceptance"
STAGE_USER="meuartigo-v1stage"
STAGE_SHA="07a92e6decc9c79d6a297522079c7389f6762ac2"
OLD="/opt/meu-artigo/repo"
OLD_SHA="cdd3affb902028753b9c66b83c2ef5e37f9e1700"
ISSUER="https://dev-w6estudk22tzwdil.us.auth0.com/"
RESOURCE="https://mcp.allflux.com.br/mcp"
PORT=18087

fail(){ printf 'V1_AUTH0_SHADOW_STOP_%s\n' "$1" >&2; exit 2; }
[[ "${1:-}" == "--check" || "${1:-}" == "--probe" ]] || fail "USAGE"
MODE="$1"
[[ "$(id -u)" == 0 ]] || fail "OPERATOR_REQUIRED"
for tool in node curl ss runuser git systemctl; do
  command -v "$tool" >/dev/null 2>&1 || fail "MISSING_DEPENDENCY"
done
[[ "$(node -p 'process.versions.node.split(".")[0]')" == 22 ]] ||
  fail "NODE_22_REQUIRED"
[[ -d "$STAGE/src/.git" && ! -L "$STAGE" && ! -L "$STAGE/src" ]] ||
  fail "STAGING_ABSENT_OR_LINKED"
[[ "$(git -c safe.directory="$STAGE/src" -C "$STAGE/src" rev-parse HEAD)" == "$STAGE_SHA" ]] ||
  fail "STAGING_SHA_DRIFT"
[[ -s "$STAGE/src/integrations/mcp-apps/dist/bridge.js" ]] ||
  fail "STAGING_UI_UNBUILT"
git -c safe.directory="$STAGE/src" -C "$STAGE/src" diff --quiet HEAD \
  -- integrations/mcp-apps/server.mjs integrations/mcp-apps/auth0.mjs ||
  fail "STAGING_AUTH_CODE_MODIFIED"
[[ "$(git -c safe.directory="$OLD" -C "$OLD" rev-parse HEAD)" == "$OLD_SHA" ]] ||
  fail "OLD_SHA_DRIFT"
[[ "$(systemctl is-active meu-artigo-mcp.service 2>/dev/null || true)" == "active" ]] ||
  fail "OLD_MCP_DOWN"
[[ "$(systemctl is-active meu-artigo-e05-tunnel.service 2>/dev/null || true)" == "active" ]] ||
  fail "E05_DOWN"
id "$STAGE_USER" >/dev/null 2>&1 || fail "STAGE_USER_MISSING"
[[ -z "$(ss -H -ltn "( sport = :$PORT )")" ]] || fail "PORT_BUSY"

if [[ "$MODE" == "--check" ]]; then
  printf 'V1_AUTH0_SHADOW_PREFLIGHT=PASS\n'
  printf 'V1_STAGING_SHA=%s\n' "$STAGE_SHA"
  printf 'V1_SHADOW_LOOPBACK=%s_FREE\n' "$PORT"
  printf 'V1_NO_CHANGES=YES\n'
  exit 0
fi

# Auth0 resource-server configuration needs only public issuer and audience;
# no client ID, client secret, Google token or personally identifiable data.
# Clear operator environment and launch as dedicated non-root stage user.
runuser -u "$STAGE_USER" -- env -i \
  PATH="/usr/local/bin:/usr/bin:/bin" HOME="$STAGE" \
  STAGE="$STAGE" PORT="$PORT" ISSUER="$ISSUER" RESOURCE="$RESOURCE" \
  MEU_ARTIGO_AUTH_MODE=auth0 \
  MEU_ARTIGO_AUTH_ISSUER="$ISSUER" \
  MEU_ARTIGO_AUTH_RESOURCE="$RESOURCE" \
  MEU_ARTIGO_MCP_MULTIUSER=YES \
  MEU_ARTIGO_BIND_HOST=127.0.0.1 \
  MEU_ARTIGO_MCP_PORT="$PORT" \
  bash -Eeuo pipefail -c '
    umask 077
    fail(){ printf "V1_AUTH0_SHADOW_STOP_%s\n" "$1" >&2; exit 2; }
    cd "$STAGE/src/integrations/mcp-apps"
    node server.mjs --http >"$STAGE/auth0-shadow.log" 2>&1 &
    child="$!"
    cleanup(){
      if kill -0 "$child" 2>/dev/null; then
        kill "$child" 2>/dev/null || true
        wait "$child" 2>/dev/null || true
      fi
    }
    trap cleanup EXIT

    ready=0
    for i in $(seq 1 60); do
      kill -0 "$child" 2>/dev/null || fail "SERVER_EXITED"
      code="$(curl -sS --noproxy "*" --max-time 1 -o /dev/null \
        -w "%{http_code}" "http://127.0.0.1:$PORT/readyz" 2>/dev/null || true)"
      if [[ "$code" == 200 ]]; then ready=1; break; fi
      sleep 0.2
    done
    [[ "$ready" == 1 ]] || fail "READY_TIMEOUT"

    for route in \
      /.well-known/oauth-protected-resource \
      /.well-known/oauth-protected-resource/mcp; do
      json="$(curl -fsS --noproxy "*" --max-time 3 \
        "http://127.0.0.1:$PORT$route")" || fail "OAUTH_DISCOVERY_MISSING"
      # Verify metadata contents locally without printing URLs or JSON to logs.
      printf "%s" "$json" | node -e '\''
        let raw="";
        process.stdin.on("data",chunk=>raw+=chunk);
        process.stdin.on("end",()=>{
          try{
            const m=JSON.parse(raw);
            if(m.resource!==process.env.RESOURCE ||
              !Array.isArray(m.authorization_servers) ||
              m.authorization_servers.length!==1 ||
              m.authorization_servers[0]!==process.env.ISSUER ||
              !m.scopes_supported?.includes("mcp:read"))process.exitCode=2;
          }catch{process.exitCode=2;}
        });
      '\'' || fail "OAUTH_DISCOVERY_CONTENT_INVALID"
    done
    denied="$(curl -sS --noproxy "*" --max-time 3 \
      -X POST -H "content-type: application/json" -d "{}" \
      -o /dev/null -w "%{http_code}" \
      "http://127.0.0.1:$PORT/mcp")" || fail "UNAUTHENTICATED_HTTP_UNAVAILABLE"
    [[ "$denied" == 401 ]] || fail "UNAUTHENTICATED_NOT_DENIED"
    wrong="$(curl -sS --noproxy "*" --max-time 3 \
      -X POST -H "content-type: application/json" \
      -H "Authorization: Bearer synthetic_invalid_no_secrets_1234567890" \
      -d "{}" -o /dev/null -w "%{http_code}" \
      "http://127.0.0.1:$PORT/mcp")" || fail "INVALID_TOKEN_TEST_UNAVAILABLE"
    [[ "$wrong" == 401 ]] || fail "INVALID_TOKEN_NOT_DENIED"
    external="$(curl -sS --noproxy "*" --max-time 3 \
      -o /dev/null -w "%{http_code}" \
      "http://127.0.0.1:$PORT/unexpected-route")" ||
      fail "UNEXPECTED_ROUTE_TEST_FAILED"
    [[ "$external" == 404 ]] || fail "UNEXPECTED_ROUTE_OPEN"
    cleanup
    trap - EXIT
    printf "V1_AUTH0_SHADOW_LOCAL_READY=200\n"
    printf "V1_AUTH0_SHADOW_RFC9728=PASS\n"
    printf "V1_AUTH0_SHADOW_NO_TOKEN=401\n"
    printf "V1_AUTH0_SHADOW_INVALID_TOKEN=401\n"
    printf "V1_AUTH0_SHADOW_UNEXPECTED_ROUTE=404\n"
    printf "V1_AUTH0_REAL_PKCE_LOGIN=NOT_TESTED\n"
    printf "V1_AUTH0_SHADOW_PUBLIC_ROUTE=NOT_CHANGED\n"
  ' || fail "PROBE_FAILED"

[[ -z "$(ss -H -ltn "( sport = :$PORT )")" ]] ||
  fail "TEMPORARY_PORT_NOT_RELEASED"
[[ "$(systemctl is-active meu-artigo-mcp.service)" == "active" ]] ||
  fail "POST_OLD_MCP_CHANGED"
[[ "$(systemctl is-active meu-artigo-e05-tunnel.service)" == "active" ]] ||
  fail "POST_E05_CHANGED"
printf 'V1_AUTH0_SHADOW_COMPLETE=PASS\n'
