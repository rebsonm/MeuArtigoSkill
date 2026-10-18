#!/usr/bin/env bash
# Candidate-only VPS bootstrap. NO Nginx, Auth0, DNS, systemd, Drive,
# production tree, E05 tunnel, user secrets, merge, release or publication.
# --check: safe read-only inventory. --apply SHA: explicit operator opt-in.
set -Eeuo pipefail
umask 077

STAGE="/opt/meu-artigo-v1-acceptance"
USER_NAME="meuartigo-v1stage"
OLD="/opt/meu-artigo/repo"
EXPECTED_OLD="cdd3affb902028753b9c66b83c2ef5e37f9e1700"
BRANCH="release/prepare-public-mcp-20261018"
REPO_URL="https://github.com/rebsonm/MeuArtigoSkill.git"
PORT=18087

fail(){ printf 'V1_STAGE_STOP_%s\n' "$1" >&2; exit 2; }
[[ "${1:-}" == "--check" || "${1:-}" == "--apply" ]] || fail "USAGE"
MODE="$1"
SHA="${2:-}"
[[ "$MODE" == "--check" || "$SHA" =~ ^[0-9a-f]{40}$ ]] || fail "SHA_REQUIRED"
[[ "$(id -u)" -eq 0 ]] || fail "ROOT_REQUIRED"
for tool in git node npm runuser useradd ss curl openssl systemctl; do
  command -v "$tool" >/dev/null 2>&1 || fail "MISSING_DEPENDENCY"
done
[[ "$(node --version)" == v22.* ]] || fail "NODE_22_REQUIRED"
[[ -d "$OLD/.git" ]] || fail "OLD_GIT_MISSING"
current="$(git -c safe.directory="$OLD" -C "$OLD" rev-parse HEAD 2>/dev/null)" ||
  fail "OLD_SHA_UNREADABLE"
[[ "$current" == "$EXPECTED_OLD" ]] || fail "OLD_SHA_DRIFT"
[[ ! -L "$STAGE" && ! -e "$STAGE" ]] || fail "STAGE_ALREADY_EXISTS"
[[ ! -e "/etc/systemd/system/meu-artigo-v1.service" ]] || fail "V1_SERVICE_ALREADY_EXISTS"
[[ -z "$(ss -H -ltn "( sport = :$PORT )")" ]] || fail "STAGING_PORT_BUSY"
[[ "$(systemctl is-active meu-artigo-mcp.service 2>/dev/null || true)" == "active" ]] ||
  fail "OLD_SERVICE_NOT_ACTIVE"
[[ "$(systemctl is-active meu-artigo-e05-tunnel.service 2>/dev/null || true)" == "active" ]] ||
  fail "E05_NOT_ACTIVE"
[[ "$(readlink -f "$(command -v node)")" != /root/* ]] || fail "NODE_PRIVATE_TO_ROOT"

if [[ "$MODE" == "--check" ]]; then
  printf 'V1_STAGE_READONLY_PASS\n'
  printf 'V1_OLD_SHA=%s\n' "$current"
  printf 'V1_PORT=%s_FREE\n' "$PORT"
  printf 'V1_NO_CHANGES=YES\n'
  exit 0
fi

# GitHub must permit anonymous HTTPS read. Abort if private, without PATs.
[[ ! -e "$STAGE" ]] || fail "STAGE_RACE"
if id "$USER_NAME" >/dev/null 2>&1; then fail "USER_ALREADY_EXISTS"; fi
useradd --system --home-dir "$STAGE" --no-create-home \
  --shell /usr/sbin/nologin "$USER_NAME" || fail "USER_CREATION_FAILED"
install -d -m 0700 -o "$USER_NAME" -g "$USER_NAME" "$STAGE" ||
  fail "STAGE_DIRECTORY_FAILED"

# Never execute fetched unreviewed scripts as root.
runuser -u "$USER_NAME" -- env \
  PATH="/usr/local/bin:/usr/bin:/bin" \
  HOME="$STAGE" \
  GIT_TERMINAL_PROMPT=0 \
  STAGE="$STAGE" SHA="$SHA" BRANCH="$BRANCH" REPO_URL="$REPO_URL" PORT="$PORT" \
  bash -Eeuo pipefail -c '
    umask 077
    fail(){ printf "V1_STAGE_STOP_%s\n" "$1" >&2; exit 2; }
    [[ ! -e "$STAGE/src" ]] || fail "SOURCE_EXISTS"
    git clone --quiet --no-checkout --single-branch --branch "$BRANCH" \
      "$REPO_URL" "$STAGE/src" || fail "GIT_ANONYMOUS_FETCH_FAILED"
    actual="$(git -C "$STAGE/src" rev-parse "refs/remotes/origin/$BRANCH")" ||
      fail "BRANCH_SHA_NOT_FOUND"
    [[ "$actual" == "$SHA" ]] || fail "BRANCH_MOVED_STOP"
    git -C "$STAGE/src" checkout --quiet --detach "$SHA" ||
      fail "CHECKOUT_FAILED"
    [[ "$(git -C "$STAGE/src" rev-parse HEAD)" == "$SHA" ]] ||
      fail "CHECKOUT_DRIFT"
    cd "$STAGE/src/integrations/mcp-apps"
    npm ci --ignore-scripts --no-audit --no-fund ||
      fail "NPM_INSTALL_FAILED"
    npm audit --omit=dev --audit-level=high ||
      fail "NPM_SECURITY_AUDIT_FAILED"
    npm run build || fail "BUILD_FAILED"
    node --check server.mjs || fail "SOURCE_SYNTAX_FAILED"
    npm run test:oauth || fail "OAUTH_SYNTHETIC_FAILED"
    npm run test:oauth-http || fail "OAUTH_HTTP_SYNTHETIC_FAILED"
    npm run test:auth-origin || fail "ORIGIN_SYNTHETIC_FAILED"
    npm run test:operational || fail "READINESS_SYNTHETIC_FAILED"
    npm run test:host-boundary || fail "DRIVE_BOUNDARY_SYNTHETIC_FAILED"
    npm run test:host-projection || fail "PROJECTION_SYNTHETIC_FAILED"
    [[ -z "$(ss -H -ltn "( sport = :$PORT )")" ]] ||
      fail "PORT_CHANGED_DURING_BUILD"
    # Short-lived localhost-only bearer server. NO Auth0/Drive real access.
    token="$(openssl rand -hex 32)" || fail "RANDOMNESS_UNAVAILABLE"
    env -i HOME="$STAGE" PATH="/usr/local/bin:/usr/bin:/bin" \
      MEU_ARTIGO_AUTH_MODE=bearer \
      MEU_ARTIGO_MCP_BEARER="$token" \
      MEU_ARTIGO_MCP_PORT="$PORT" MEU_ARTIGO_BIND_HOST=127.0.0.1 \
      node server.mjs --http >"$STAGE/probe.log" 2>&1 &
    probe_pid="$!"
    cleanup(){
      if kill -0 "$probe_pid" 2>/dev/null; then
        kill "$probe_pid" 2>/dev/null || true
        wait "$probe_pid" 2>/dev/null || true
      fi
    }
    trap cleanup EXIT
    ready=0
    for i in $(seq 1 50); do
      kill -0 "$probe_pid" 2>/dev/null || fail "PROBE_PROCESS_EXITED"
      code="$(curl -sS --noproxy "*" --max-time 1 -o /dev/null \
        -w "%{http_code}" "http://127.0.0.1:$PORT/readyz" 2>/dev/null || true)"
      if [[ "$code" == "200" ]]; then ready=1; break; fi
      sleep 0.2
    done
    [[ "$ready" -eq 1 ]] || fail "READINESS_FAILED"
    unauth="$(curl -sS --noproxy "*" --max-time 3 -o /dev/null \
      -w "%{http_code}" "http://127.0.0.1:$PORT/mcp")" ||
      fail "MCP_PROBE_UNAVAILABLE"
    [[ "$unauth" == "401" ]] || fail "MCP_UNAUTHORIZED_NOT_DENIED"
    metadata="$(curl -sS --noproxy "*" --max-time 3 -o /dev/null \
      -w "%{http_code}" "http://127.0.0.1:$PORT/.well-known/oauth-protected-resource")" ||
      fail "METADATA_PROBE_UNAVAILABLE"
    [[ "$metadata" == "404" ]] || fail "BEARER_PROBE_EXPOSED_OAUTH"
    cleanup
    trap - EXIT
    printf "V1_STAGE_SHA=%s\n" "$SHA"
    printf "V1_STAGE_OFFLINE_TESTS=PASS\n"
    printf "V1_TEMPORARY_LOCAL_READINESS=200\n"
    printf "V1_TEMPORARY_LOCAL_MCP_NO_TOKEN=401\n"
    printf "V1_AUTH0_REAL_LOGIN=NOT_TESTED\n"
    printf "V1_EXTERNAL_MCP=NOT_ACTIVATED\n"
    printf "V1_STAGE_APPLIED_SOURCE_ONLY=YES\n"
  ' || fail "ISOLATED_RUN_FAILED"

[[ "$(git -c safe.directory="$OLD" -C "$OLD" rev-parse HEAD)" == "$EXPECTED_OLD" ]] ||
  fail "POST_OLD_SHA_DRIFT"
[[ "$(systemctl is-active meu-artigo-mcp.service)" == "active" ]] ||
  fail "POST_OLD_SERVICE_CHANGED"
[[ "$(systemctl is-active meu-artigo-e05-tunnel.service)" == "active" ]] ||
  fail "POST_E05_CHANGED"
[[ -z "$(ss -H -ltn "( sport = :$PORT )")" ]] || fail "PROBE_PORT_NOT_RELEASED"
printf 'V1_STAGE_ISOLATED_COMPLETE=YES\n'
