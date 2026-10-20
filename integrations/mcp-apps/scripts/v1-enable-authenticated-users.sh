#!/usr/bin/env bash
# Owner-authorized, reversible GENERAL authenticated access to the display-only MCP.
# No ChatGPT directory publication, no OAuth bypass and no Google Drive read.
set -Eeuo pipefail
umask 077
SERVICE=meu-artigo-v1.service
UNIT="/etc/systemd/system/$SERVICE"
DROPIN_DIR="/etc/systemd/system/$SERVICE.d"
DROPIN="$DROPIN_DIR/70-authenticated-multiuser.conf"
ROOT="/opt/meu-artigo-v1-runtime/src"
EXPECTED_SHA="02e03674e8e897d7f5e3f6769f7902062695b8dc"
ISSUER="https://dev-w6estudk22tzwdil.us.auth0.com/"
RESOURCE="https://mcp.allflux.com.br/mcp"
fail(){ printf 'V1_MULTIUSER_STOP_%s\n' "$1" >&2; exit 2; }
[[ "$(id -u)" -eq 0 && "$#" -eq 1 ]] || fail "ROOT_AND_MODE_REQUIRED"
[[ "$1" == --apply || "$1" == --rollback ]] || fail "INVALID_MODE"
for cmd in systemctl git grep mktemp mv rm chmod curl stat seq sleep mkdir; do
 command -v "$cmd" >/dev/null 2>&1 || fail "DEPENDENCY_UNAVAILABLE"
done
[[ -f "$UNIT" && ! -L "$UNIT" && -d "$ROOT/.git" ]] || fail "BASE_RUNTIME_MISSING"
[[ "$(git -c safe.directory="$ROOT" -C "$ROOT" rev-parse HEAD 2>/dev/null)" == "$EXPECTED_SHA" ]] || fail "DEPLOYED_SHA_DRIFT"
git -c safe.directory="$ROOT" -C "$ROOT" diff --quiet HEAD -- \
 integrations/mcp-apps/server.mjs integrations/mcp-apps/auth0.mjs || fail "AUTH_SOURCE_DRIFT"
for line in \
  "Environment=MEU_ARTIGO_MCP_MULTIUSER=YES" \
  "Environment=MEU_ARTIGO_MCP_PRIVATE_PILOT=YES" \
  "Environment=MEU_ARTIGO_MCP_PILOT_SUBS=DENY_ALL" \
  "Environment=MEU_ARTIGO_AUTH_MODE=auth0" \
  "Environment=MEU_ARTIGO_AUTH_ISSUER=$ISSUER" \
  "Environment=MEU_ARTIGO_AUTH_RESOURCE=$RESOURCE" \
  "Environment=MEU_ARTIGO_BIND_HOST=127.0.0.1" \
  "Environment=MEU_ARTIGO_MCP_PORT=18087"; do
 grep -Fxq "$line" "$UNIT" || fail "BASE_AUTH_CONTRACT_CHANGED"
done
[[ ! -L "$DROPIN_DIR" && ! -L "$DROPIN" ]] || fail "UNSAFE_DROPIN_LINK"
[[ "$(systemctl is-active "$SERVICE")" == active ]] || fail "V1_NOT_RUNNING"
[[ "$(systemctl is-active meu-artigo-mcp.service)" == active ]] || fail "LEGACY_NOT_RUNNING"
[[ "$(systemctl is-active meu-artigo-e05-tunnel.service)" == active ]] || fail "E05_NOT_RUNNING"
# Never bypass a prior restrictive override or a separate systemd configuration.
if [[ -d "$DROPIN_DIR" ]]; then
 for file in "$DROPIN_DIR"/*.conf; do
  [[ ! -e "$file" || "$file" == "$DROPIN" ]] || fail "OTHER_DROPIN_UNREVIEWED"
 done
fi
probe(){
 curl --noproxy '*' --silent --show-error --connect-timeout 3 --max-time 8 \
  -o /dev/null -w '%{http_code}' "$@" 2>/dev/null || true
}
check_server(){
 local code="000"
 for _ in $(seq 1 30); do
  code="$(probe http://127.0.0.1:18087/readyz)"
  [[ "$code" == 200 ]] && break
  sleep 0.5
 done
 [[ "$code" == 200 ]] || fail "V1_NOT_READY"
 [[ "$(probe -X POST -H 'content-type: application/json' -d '{}' \
   http://127.0.0.1:18087/mcp)" == 401 ]] || fail "ANONYMOUS_NOT_401"
 [[ "$(systemctl is-active meu-artigo-mcp.service)" == active ]] || fail "LEGACY_CHANGED"
 [[ "$(systemctl is-active meu-artigo-e05-tunnel.service)" == active ]] || fail "E05_CHANGED"
}
if [[ "$1" == --rollback ]]; then
 [[ -f "$DROPIN" && ! -L "$DROPIN" ]] || fail "NO_MANAGED_OVERRIDE"
 grep -Fxq '# MEU_ARTIGO_OWNED_MULTIUSER_OVERRIDE_V1' "$DROPIN" ||
  fail "OVERRIDE_NOT_OURS"
 rm -f -- "$DROPIN"
 systemctl daemon-reload || fail "DAEMON_RELOAD_FAILED"
 systemctl restart "$SERVICE" || fail "V1_RESTART_FAILED"
 check_server
 printf 'V1_MULTIUSER=DENY_ALL_RESTORED\nV1_OTHER_SERVICES=UNCHANGED\n'
 exit 0
fi
[[ ! -e "$DROPIN" ]] || fail "ALREADY_CONFIGURED"
mkdir -p -- "$DROPIN_DIR"
TEMP="$(mktemp "$DROPIN_DIR/.allow-all-XXXXXXXX")" || fail "TEMPFILE_FAILED"
APPLIED=NO
COMPLETED=NO
cleanup(){
  local code=$?
  trap - EXIT INT TERM
  [[ ! -e "$TEMP" ]] || rm -f -- "$TEMP"
  if [[ "$APPLIED" == YES && "$COMPLETED" != YES ]]; then
    rm -f -- "$DROPIN"
    systemctl daemon-reload >/dev/null 2>&1 || true
    systemctl restart "$SERVICE" >/dev/null 2>&1 || true
    printf 'V1_MULTIUSER_AUTO_REVERT=DENY_ALL\n' >&2
  fi
  exit "$code"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
cat > "$TEMP" <<'END_CONFIG'
# MEU_ARTIGO_OWNED_MULTIUSER_OVERRIDE_V1
[Service]
# Both empty: OAuth remains mandatory and authenticates each user.
Environment=MEU_ARTIGO_MCP_PRIVATE_PILOT=
Environment=MEU_ARTIGO_MCP_PILOT_SUBS=
END_CONFIG
chmod 0644 "$TEMP"
mv -f -- "$TEMP" "$DROPIN" || fail "OVERRIDE_CREATION_FAILED"
APPLIED=YES
systemctl daemon-reload || fail "DAEMON_RELOAD_FAILED"
systemctl restart "$SERVICE" || fail "V1_RESTART_FAILED"
check_server
PID="$(systemctl show -P MainPID "$SERVICE")"
[[ "$PID" =~ ^[0-9]+$ && "$PID" -gt 1 ]] || fail "MAIN_PID_INVALID"
grep -zFxq 'MEU_ARTIGO_MCP_PRIVATE_PILOT=' "/proc/$PID/environ" ||
 fail "PRIVATE_PILOT_FLAG_NOT_CLEARED"
grep -zFxq 'MEU_ARTIGO_MCP_PILOT_SUBS=' "/proc/$PID/environ" ||
 fail "PILOT_ALLOWLIST_NOT_CLEARED"
grep -zFxq 'MEU_ARTIGO_AUTH_MODE=auth0' "/proc/$PID/environ" ||
 fail "AUTH0_LOST"
grep -zFxq 'MEU_ARTIGO_MCP_MULTIUSER=YES' "/proc/$PID/environ" ||
 fail "MULTIUSER_LOST"
COMPLETED=YES
printf 'V1_MULTIUSER=ALL_AUTHENTICATED_AUTH0_SUBJECTS\n'
printf 'V1_OAUTH_SCOPE=mcp:read\n'
printf 'V1_PUBLIC_DIRECTORY=NOT_PUBLISHED\n'
printf 'V1_LIVE_USER_LOGIN=NOT_YET_VERIFIED\n'
printf 'V1_GOOGLE_DRIVE_ACCESS=NONE_BY_MCP\n'
printf 'V1_OTHER_SERVICES=UNCHANGED\n'
printf 'V1_ROLLBACK=bash %s --rollback\n' "$0"
