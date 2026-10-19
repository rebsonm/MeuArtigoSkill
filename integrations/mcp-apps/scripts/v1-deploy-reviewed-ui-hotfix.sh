#!/usr/bin/env bash
# Reviewed minimal hotfix: isolated copy of existing live runtime, replace exactly
# three pinned files, validate offline, then systemd override for v1 ONLY.
# --rollback removes just this override and restarts the original v1 runtime.
# Public app publication, legacy MCP, E05, Auth0 and Drive are NOT modified.
set -Eeuo pipefail
umask 077
fail(){ printf 'V1_UI_HOTFIX_STOP_%s\n' "$1" >&2;exit 2; }
[[ "$(id -u)" -eq 0 && "$#" -eq 1 ]] || fail "ROOT_AND_MODE_REQUIRED"
MODE="$1"
[[ "$MODE" == --apply || "$MODE" == --rollback ]] || fail "INVALID_MODE"
for c in systemctl git curl cp mv rm chmod mktemp grep stat npm node runuser install;do
 command -v "$c" >/dev/null 2>&1 || fail "MISSING_COMMAND"
done
SOURCE_SHA="4365456fd63cb6090dac7e79dd1cadaf0732da2c"
ORIGINAL_SHA="02e03674e8e897d7f5e3f6769f7902062695b8dc"
ROOT="/opt/meu-artigo-v1-runtime/src"
STAGE="/opt/meu-artigo-v1-ui-hotfix-20261019"
SERVICE="meu-artigo-v1.service"
UNIT="/etc/systemd/system/$SERVICE"
DROP_DIR="/etc/systemd/system/$SERVICE.d"
DROP="$DROP_DIR/80-ui-source-hotfix.conf"
ALLOW="$DROP_DIR/70-authenticated-multiuser.conf"
USER_NAME="meuartigo-v1run"
URL="https://raw.githubusercontent.com/rebsonm/MeuArtigoSkill/$SOURCE_SHA"
fail_if_present(){
 [[ ! -e "$DROP" && ! -e "$STAGE" ]] || fail "HOTFIX_ALREADY_PRESENT"
}
[[ -f "$UNIT" && ! -L "$UNIT" && ! -L "$DROP_DIR" && ! -L "$DROP" ]] || fail "UNIT_INVALID"
[[ "$(git -c safe.directory="$ROOT" -C "$ROOT" rev-parse HEAD 2>/dev/null)" == "$ORIGINAL_SHA" ]] || fail "BASE_SHA_DRIFT"
[[ "$(systemctl is-active "$SERVICE")" == active ]] || fail "V1_INACTIVE"
[[ "$(systemctl is-active meu-artigo-mcp.service)" == active ]] || fail "LEGACY_INACTIVE"
[[ "$(systemctl is-active meu-artigo-e05-tunnel.service)" == active ]] || fail "E05_INACTIVE"
for line in \
 'Environment=MEU_ARTIGO_AUTH_MODE=auth0' \
 'Environment=MEU_ARTIGO_MCP_MULTIUSER=YES' \
 'Environment=MEU_ARTIGO_MCP_PRIVATE_PILOT=YES' \
 'Environment=MEU_ARTIGO_MCP_PILOT_SUBS=DENY_ALL' \
 'Environment=MEU_ARTIGO_MCP_PORT=18087';do
 grep -Fxq "$line" "$UNIT" || fail "AUTH_BASE_DRIFT"
done
[[ -f "$ALLOW" && ! -L "$ALLOW" ]] || fail "AUTHENTICATED_USER_OVERRIDE_MISSING"
grep -Fxq 'Environment=MEU_ARTIGO_MCP_PRIVATE_PILOT=' "$ALLOW" || fail "MULTIUSER_FLAG_MISSING"
grep -Fxq 'Environment=MEU_ARTIGO_MCP_PILOT_SUBS=' "$ALLOW" || fail "DENY_ALL_ACTIVE"
for file in "$DROP_DIR"/*.conf;do
 [[ ! -e "$file" || "$file" == "$ALLOW" || "$file" == "$DROP" ]] || fail "OTHER_OVERRIDE_PRESENT"
done
probe(){
 curl --noproxy '*' -sS --connect-timeout 2 --max-time 5 \
  -o /dev/null -w '%{http_code}' "$@" 2>/dev/null || true
}
verify_runtime(){
 local ready=000
 for _ in $(seq 1 40);do
   ready="$(probe http://127.0.0.1:18087/readyz)"
   [[ "$ready" == 200 ]] && break
   sleep 0.25
 done
 [[ "$ready" == 200 ]] || fail "READINESS_NOT_200"
 [[ "$(probe -X POST -H 'content-type: application/json' -d '{}' \
  http://127.0.0.1:18087/mcp)" == 401 ]] || fail "ANONYMOUS_NOT_401"
 [[ "$(probe http://127.0.0.1:18087/.well-known/oauth-protected-resource)" == 200 ]] || fail "OAUTH_DISCOVERY_NOT_200"
 [[ "$(systemctl is-active meu-artigo-mcp.service)" == active ]] || fail "LEGACY_CHANGED"
 [[ "$(systemctl is-active meu-artigo-e05-tunnel.service)" == active ]] || fail "E05_CHANGED"
}
if [[ "$MODE" == --rollback ]];then
 [[ -f "$DROP" && ! -L "$DROP" ]] || fail "HOTFIX_OVERRIDE_NOT_FOUND"
 grep -Fxq '# MEU_ARTIGO_REVIEWED_UI_HOTFIX' "$DROP" || fail "HOTFIX_OVERRIDE_NOT_OURS"
 rm -f -- "$DROP"
 systemctl daemon-reload || fail "RELOAD_FAILED"
 systemctl restart "$SERVICE" || fail "RESTART_FAILED"
 verify_runtime
 echo 'V1_UI_HOTFIX=ROLLED_BACK_TO_ORIGINAL_RUNTIME'
 echo 'V1_AUTH0_MULTIUSER=UNCHANGED'
 echo 'V1_E05_LEGACY=UNCHANGED'
 exit 0
fi
fail_if_present
TEMP=""
STAGED=NO
SWITCHED=NO
COMPLETED=NO
cleanup(){
 local code=$?
 trap - EXIT INT TERM
 [[ -z "$TEMP" || ! -e "$TEMP" ]] || rm -f -- "$TEMP"
 if [[ "$SWITCHED" == YES && "$COMPLETED" != YES ]];then
  rm -f -- "$DROP"
  systemctl daemon-reload >/dev/null 2>&1 || true
  systemctl restart "$SERVICE" >/dev/null 2>&1 || true
  echo 'V1_UI_HOTFIX_AUTO_ROLLBACK=ORIGINAL_RUNTIME' >&2
 fi
 if [[ "$STAGED" == YES && "$COMPLETED" != YES ]];then
  rm -rf -- "$STAGE"
 fi
 exit "$code"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

STAGED=YES
cp -a -- "$ROOT" "$STAGE" || fail "RUNTIME_COPY_FAILED"
# Only three source files differ: no changes to auth, HTTP, dependencies,
# systemd security sandbox, E05 fixture policy or reverse proxy.
for file in \
  assets/research_site.html \
  integrations/mcp-apps/server.mjs \
  integrations/mcp-apps/ui_output_schema.mjs;do
 case "$file" in
  assets/research_site.html) expected=8866aabc8935fe7e6055b24b6dbcdaf8732bba61;;
  integrations/mcp-apps/server.mjs) expected=f821c78deec655e5b2d43b1c0314ee3a53d317f3;;
  integrations/mcp-apps/ui_output_schema.mjs) expected=dec3246d9ba0a7e402a17b544e3c4982bd3180fd;;
  *) fail "UNAPPROVED_SOURCE_PATH";;
 esac
 dest="$STAGE/$file"
 [[ -f "$dest" && ! -L "$dest" ]] || fail "SOURCE_DESTINATION_INVALID"
 curl -fsSL --connect-timeout 5 --max-time 30 \
   "$URL/$file" -o "$dest.new" || fail "SOURCE_DOWNLOAD_FAILED"
 [[ "$(git hash-object "$dest.new")" == "$expected" ]] || fail "SOURCE_BLOB_NOT_PINNED"
 chmod 0644 "$dest.new"
 mv -f -- "$dest.new" "$dest" || fail "SOURCE_REPLACE_FAILED"
done

# Validate the assembled UI, protocol, privacy and synthetic E05 behavior
# before making ANY systemd change.
runuser -u "$USER_NAME" -- bash -euc '
 cd "$1/integrations/mcp-apps"
 npm run test:smoke
 npm run test:host-projection
 npm run test:host-projection-ui
 npm run test:e05-synthetic
 npm run test:ui-resource-contract
 npm run test:e05-csp
' bash "$STAGE" || fail "STAGED_PROTOCOL_OR_UI_TEST_FAILED"
TEMP="$(mktemp "$DROP_DIR/.ui-hotfix-XXXXXXXX")" || fail "OVERRIDE_TEMP_FAILED"
cat > "$TEMP" <<EOF
# MEU_ARTIGO_REVIEWED_UI_HOTFIX
[Service]
WorkingDirectory=$STAGE/integrations/mcp-apps
ExecStart=
ExecStart=/usr/bin/node $STAGE/integrations/mcp-apps/server.mjs --http
EOF
chmod 0644 "$TEMP"
mv -f -- "$TEMP" "$DROP" || fail "OVERRIDE_INSTALL_FAILED"
SWITCHED=YES
systemctl daemon-reload || fail "DAEMON_RELOAD_FAILED"
systemctl restart "$SERVICE" || fail "SERVICE_RESTART_FAILED"
verify_runtime
PID="$(systemctl show -P MainPID "$SERVICE")"
[[ "$PID" =~ ^[0-9]+$ && "$PID" -gt 1 ]] || fail "PID_INVALID"
grep -zFq "$STAGE/integrations/mcp-apps/server.mjs" "/proc/$PID/cmdline" ||
 fail "WRONG_RUNTIME_STARTED"
grep -zFxq 'MEU_ARTIGO_AUTH_MODE=auth0' "/proc/$PID/environ" || fail "AUTH0_LOST"
grep -zFxq 'MEU_ARTIGO_MCP_MULTIUSER=YES' "/proc/$PID/environ" || fail "MULTIUSER_LOST"
grep -zFxq 'MEU_ARTIGO_MCP_PRIVATE_PILOT=' "/proc/$PID/environ" || fail "ALLOWLIST_CHANGED"
COMPLETED=YES
echo 'V1_UI_HOTFIX=PASS'
echo "V1_UI_SOURCE_SHA=$SOURCE_SHA"
echo 'V1_AUTH0_MULTIUSER=UNCHANGED'
echo 'V1_E05_LEGACY=UNCHANGED'
echo 'V1_GOOGLE_DRIVE_ACCESS=NONE_BY_MCP'
echo 'V1_PUBLIC_DIRECTORY=NOT_PUBLISHED'
echo 'V1_HOST_CSP=NOT_INDEPENDENTLY_VERIFIED'
echo "V1_ROLLBACK=bash $0 --rollback"
