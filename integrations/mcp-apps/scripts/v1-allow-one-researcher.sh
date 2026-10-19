#!/usr/bin/env bash
# Private, single consenting Auth0 user pilot for the already-running v1 server.
# The user ID is entered locally, never in a URL, command argument or output.
# This script never edits Nginx, source code, Google Drive or other services.
set -Eeuo pipefail
umask 077

SERVICE="meu-artigo-v1.service"
UNIT="/etc/systemd/system/$SERVICE"
ROOT="/opt/meu-artigo-v1-runtime/src"
PINNED_SHA="02e03674e8e897d7f5e3f6769f7902062695b8dc"
CONF_DIR="/etc/systemd/system/$SERVICE.d"
OVERRIDE="$CONF_DIR/60-private-one-user.conf"
SECRET_DIR="/etc/meu-artigo-v1-private"
ALLOW_ENV="$SECRET_DIR/pilot-allowlist.env"
MARKER="# MEU_ARTIGO_V1_SINGLE_RESEARCHER_PILOT"

fail(){ printf 'V1_SINGLE_PILOT_STOP_%s\n' "$1" >&2; exit 2; }
[[ "$(id -u)" -eq 0 && "$#" -eq 1 ]] || fail "ROOT_EXPLICIT_MODE_REQUIRED"
[[ "$1" == "--apply" || "$1" == "--rollback" ]] || fail "UNKNOWN_MODE"
for program in systemctl grep git curl stat mktemp install mv rm; do
 command -v "$program" >/dev/null 2>&1 || fail "COMMAND_UNAVAILABLE"
done
[[ -f "$UNIT" && ! -L "$UNIT" ]] || fail "UNIT_NOT_VERIFIED"
grep -Fxq 'Environment=MEU_ARTIGO_MCP_PRIVATE_PILOT=YES' "$UNIT" || fail "PRIVATE_PILOT_NOT_ENABLED"
grep -Fxq 'Environment=MEU_ARTIGO_MCP_MULTIUSER=YES' "$UNIT" || fail "MULTIUSER_NOT_ENABLED"
grep -Fxq 'Environment=MEU_ARTIGO_MCP_PILOT_SUBS=DENY_ALL' "$UNIT" || fail "BASE_DENY_ALL_MISSING"
grep -Fxq 'Environment=MEU_ARTIGO_AUTH_MODE=auth0' "$UNIT" || fail "AUTH0_NOT_ACTIVE"
grep -Fxq 'Environment=MEU_ARTIGO_MCP_PORT=18087' "$UNIT" || fail "NOT_V1_PORT"
[[ "$(git -c safe.directory="$ROOT" -C "$ROOT" rev-parse HEAD 2>/dev/null)" == "$PINNED_SHA" ]] || fail "RUNTIME_SHA_CHANGED"
git -c safe.directory="$ROOT" -C "$ROOT" diff --quiet HEAD -- \
 integrations/mcp-apps/server.mjs integrations/mcp-apps/auth0.mjs || fail "AUTH_SOURCE_CHANGED"
[[ "$(systemctl is-active "$SERVICE")" == active ]] || fail "V1_SERVICE_NOT_ACTIVE"
[[ "$(systemctl is-active meu-artigo-mcp.service)" == active ]] || fail "LEGACY_NOT_ACTIVE"
[[ "$(systemctl is-active meu-artigo-e05-tunnel.service)" == active ]] || fail "E05_NOT_ACTIVE"
[[ ! -L "$CONF_DIR" && ! -L "$SECRET_DIR" && ! -L "$OVERRIDE" && ! -L "$ALLOW_ENV" ]] ||
 fail "SYMLINK_NOT_ALLOWED"

probe(){
 curl --noproxy '*' -sS --connect-timeout 2 --max-time 5 -o /dev/null \
  -w '%{http_code}' "$@" 2>/dev/null || true
}
assert_running(){
 [[ "$(systemctl is-active "$SERVICE")" == active ]] || fail "SERVICE_DID_NOT_START"
 local ready="000"
 for i in $(seq 1 40); do
  ready="$(probe http://127.0.0.1:18087/readyz)"
  [[ "$ready" == 200 ]] && break
  sleep 0.25
 done
 [[ "$ready" == 200 ]] || fail "LOCAL_READY_NOT_200"
 [[ "$(probe -X POST -H 'content-type: application/json' -d '{}' \
  http://127.0.0.1:18087/mcp)" == 401 ]] || fail "ANONYMOUS_ACCESS_NOT_DENIED"
 [[ "$(systemctl is-active meu-artigo-mcp.service)" == active ]] || fail "LEGACY_CHANGED"
 [[ "$(systemctl is-active meu-artigo-e05-tunnel.service)" == active ]] || fail "E05_CHANGED"
}

if [[ "$1" == "--rollback" ]]; then
 [[ -f "$OVERRIDE" && -f "$ALLOW_ENV" ]] || fail "NO_MANAGED_PILOT_TO_REVERT"
 grep -Fxq "$MARKER" "$OVERRIDE" || fail "NOT_OUR_OVERRIDE"
 grep -Fxq "[Service]" "$OVERRIDE" || fail "OVERRIDE_NOT_RECOGNIZED"
 grep -Fxq "EnvironmentFile=$ALLOW_ENV" "$OVERRIDE" || fail "OVERRIDE_NOT_RECOGNIZED"
 rm -f -- "$OVERRIDE" "$ALLOW_ENV"
 systemctl daemon-reload || fail "DAEMON_RELOAD_FAILED"
 systemctl restart "$SERVICE" || fail "RESTART_FAILED"
 assert_running
 printf 'V1_SINGLE_PILOT_ROLLBACK=DENY_ALL_RESTORED\n'
 printf 'V1_LEGACY_AND_E05=UNCHANGED\n'
 exit 0
fi

[[ ! -e "$OVERRIDE" && ! -e "$ALLOW_ENV" ]] || fail "PILOT_ALREADY_CONFIGURED"
# Never override someone else's drop-in configuration for this service.
if [[ -d "$CONF_DIR" ]]; then
 [[ -z "$(find "$CONF_DIR" -mindepth 1 -maxdepth 1 -name '*.conf' -print -quit)" ]] ||
  fail "UNREVIEWED_EXISTING_DROPIN"
fi
printf 'Paste only YOUR exact Auth0 User ID from Auth0 Dashboard > User Management > Users.\n'
printf 'Input is hidden, is not written to terminal history and is not sent to GitHub.\n'
IFS= read -r -s -p 'Auth0 User ID (hidden): ' SUB || fail "SUBJECT_INPUT_FAILED"
printf '\n'
[[ "$SUB" =~ ^[A-Za-z0-9_-]{2,48}\|[A-Za-z0-9_.-]{5,128}$ ]] || fail "SUBJECT_FORMAT_INVALID"
read -r -p 'Type ALLOW_ONE_PRIVATE_RESEARCHER to confirm: ' CONSENT || fail "CONSENT_NOT_RECEIVED"
[[ "$CONSENT" == "ALLOW_ONE_PRIVATE_RESEARCHER" ]] || fail "CONSENT_NOT_GRANTED"

CREATED="NO"
DONE="NO"
TEMP_ENV=""
TEMP_CONF=""
revert_on_failure(){
 local code="$?"
 trap - EXIT INT TERM
 [[ -z "$TEMP_ENV" ]] || rm -f -- "$TEMP_ENV"
 [[ -z "$TEMP_CONF" ]] || rm -f -- "$TEMP_CONF"
 if [[ "$DONE" != YES && "$CREATED" == YES ]]; then
  rm -f -- "$OVERRIDE" "$ALLOW_ENV"
  systemctl daemon-reload >/dev/null 2>&1 || true
  systemctl restart "$SERVICE" >/dev/null 2>&1 || true
  printf 'V1_SINGLE_PILOT_AUTO_REVERT=DENY_ALL\n' >&2
 fi
 unset SUB
 exit "$code"
}
trap revert_on_failure EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

install -d -m 0700 "$SECRET_DIR" || fail "SECRET_DIR_FAILED"
install -d -m 0755 "$CONF_DIR" || fail "OVERRIDE_DIR_FAILED"
TEMP_ENV="$(mktemp "$SECRET_DIR/.pilot-env-XXXXXXXX")" || fail "TEMP_ENV_FAILED"
TEMP_CONF="$(mktemp "$CONF_DIR/.pilot-conf-XXXXXXXX")" || fail "TEMP_CONF_FAILED"
CREATED="YES"
# A pipe character in the Auth0 User ID is permitted by systemd EnvironmentFile.
printf 'MEU_ARTIGO_MCP_PILOT_SUBS=%s\n' "$SUB" > "$TEMP_ENV"
printf '%s\n[Service]\nEnvironmentFile=%s\n' "$MARKER" "$ALLOW_ENV" > "$TEMP_CONF"
chmod 0600 "$TEMP_ENV" "$TEMP_CONF"
mv -f -- "$TEMP_ENV" "$ALLOW_ENV" || fail "ALLOW_ENV_REPLACE_FAILED"
mv -f -- "$TEMP_CONF" "$OVERRIDE" || fail "OVERRIDE_REPLACE_FAILED"
systemctl daemon-reload || fail "DAEMON_RELOAD_FAILED"
systemctl restart "$SERVICE" || fail "SERVICE_RESTART_FAILED"
assert_running

# Verify actual process environment without printing private Auth0 User ID.
PID="$(systemctl show -P MainPID "$SERVICE")"
[[ "$PID" =~ ^[0-9]+$ && "$PID" -gt 1 ]] || fail "PID_NOT_VERIFIED"
grep -zFxq "MEU_ARTIGO_MCP_PILOT_SUBS=$SUB" "/proc/$PID/environ" ||
 fail "ALLOWLIST_NOT_APPLIED_TO_PROCESS"
[[ "$(stat -c '%a' "$ALLOW_ENV")" == 600 ]] || fail "ALLOW_ENV_PERMISSIONS"
[[ "$(stat -c '%a' "$OVERRIDE")" == 600 ]] || fail "OVERRIDE_PERMISSIONS"
DONE="YES"
unset SUB
printf 'V1_SINGLE_PILOT=ONE_APPROVED_IDENTITY_ACTIVE\n'
printf 'V1_SINGLE_PILOT_REAL_LOGIN=NOT_YET_TESTED\n'
printf 'V1_SINGLE_PILOT_PUBLIC_RELEASE=NO\n'
printf 'V1_LEGACY_AND_E05=UNCHANGED\n'
printf 'V1_SINGLE_PILOT_ROLLBACK_COMMAND=bash %s --rollback\n' "$0"
