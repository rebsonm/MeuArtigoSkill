#!/usr/bin/env bash
# Resume only a failed v1 controlled cutover, reusing existing isolated files.
# No package reinstall, no repo reset, no E05/legacy alteration, no real users.
# Operator uses this ONLY after verifying that the original cutover rolled back.
set -Eeuo pipefail
umask 077
fail(){ printf 'V1_RESUME_STOP_%s\n' "$1" >&2; exit 2; }
[[ "$(id -u)" == 0 && "$#" -eq 1 && "$1" == "--apply" ]] ||
 fail "EXPLICIT_ROOT_APPLY_REQUIRED"
ROOT="/opt/meu-artigo-v1-runtime"
SOURCE_SHA="02e03674e8e897d7f5e3f6769f7902062695b8dc"
OLD="/opt/meu-artigo/repo"
OLD_SHA="cdd3affb902028753b9c66b83c2ef5e37f9e1700"
RUN_USER="meuartigo-v1run"
UNIT="/etc/systemd/system/meu-artigo-v1.service"
NAME="meu-artigo-v1.service"
SITE_LINK="/etc/nginx/sites-enabled/meu-artigo-mcp.conf"
HOST="mcp.allflux.com.br"
IP="84.247.134.242"
ISSUER="https://dev-w6estudk22tzwdil.us.auth0.com/"
RESOURCE="https://mcp.allflux.com.br/mcp"
for tool in git node ss curl nginx systemctl grep sed cp mv realpath; do
 command -v "$tool" >/dev/null 2>&1 || fail "TOOL_MISSING"
done
[[ "$(node -p 'process.versions.node.split(".")[0]')" == 22 ]] ||
 fail "NODE_22_REQUIRED"
[[ -d "$ROOT/src/.git" && ! -L "$ROOT" && ! -L "$ROOT/src" ]] ||
 fail "PRIOR_RUNTIME_MISSING"
[[ "$(git -c safe.directory="$ROOT/src" -C "$ROOT/src" rev-parse HEAD)" == "$SOURCE_SHA" ]] ||
 fail "PRIOR_SHA_DRIFT"
git -c safe.directory="$ROOT/src" -C "$ROOT/src" diff --quiet HEAD -- \
 integrations/mcp-apps/server.mjs integrations/mcp-apps/auth0.mjs ||
 fail "AUTH_SOURCE_DRIFT"
[[ -s "$ROOT/src/integrations/mcp-apps/dist/bridge.js" ]] ||
 fail "BRIDGE_NOT_BUILT"
id "$RUN_USER" >/dev/null 2>&1 || fail "PRIOR_USER_MISSING"
[[ "$(stat -c '%U' "$ROOT/src")" == "$RUN_USER" ]] ||
 fail "RUNTIME_OWNER_DRIFT"
[[ "$(git -c safe.directory="$OLD" -C "$OLD" rev-parse HEAD)" == "$OLD_SHA" ]] ||
 fail "LEGACY_SHA_DRIFT"
[[ "$(systemctl is-active meu-artigo-mcp.service)" == active ]] ||
 fail "LEGACY_NOT_ACTIVE"
[[ "$(systemctl is-active meu-artigo-e05-tunnel.service)" == active ]] ||
 fail "E05_NOT_ACTIVE"
[[ -z "$(ss -H -ltn '( sport = :18087 )')" ]] || fail "PORT_OCCUPIED"
[[ ! -e "$UNIT" && ! -L "$UNIT" ]] || fail "V1_UNIT_NOT_ROLLED_BACK"
SITE="$(realpath -e "$SITE_LINK")" || fail "NGINX_SITE_MISSING"
[[ "$SITE" == /etc/nginx/* && -f "$SITE" ]] || fail "NGINX_SCOPE_INVALID"
grep -Fq "server_name $HOST;" "$SITE" || fail "HOST_CHANGED"
grep -Fq 'location ^~ /.well-known/acme-challenge/' "$SITE" ||
 fail "ACME_NOT_PRESERVED"
grep -Fq 'location ~ ^/(mcp|\.well-known/oauth-protected-resource(/mcp)?)$' "$SITE" ||
 fail "MCP_ROUTE_CHANGED"
grep -Fq 'location / { return 404; }' "$SITE" || fail "DEFAULT_DENY_CHANGED"
[[ "$(grep -Fc 'proxy_pass http://127.0.0.1:18086;' "$SITE")" == 1 ]] ||
 fail "OLD_UPSTREAM_NOT_RESTORED"
[[ "$(grep -Ec '^[[:space:]]*server_name ' "$SITE")" == 2 ]] ||
 fail "VHOST_STRUCTURE_CHANGED"
[[ "$(grep -Ec '^[[:space:]]*ssl_certificate ' "$SITE")" == 1 ]] ||
 fail "SSL_STRUCTURE_CHANGED"
nginx -t >/dev/null 2>&1 || fail "CURRENT_NGINX_INVALID"

install -d -m 0700 /var/backups/meu-artigo-v1-cutover
BACKUP="/var/backups/meu-artigo-v1-cutover/$(date -u +%Y%m%dT%H%M%SZ)-resume.conf"
cp -a "$SITE" "$BACKUP" || fail "BACKUP_FAILED"
[[ -s "$BACKUP" ]] || fail "BACKUP_EMPTY"

SITE_CHANGED=NO
UNIT_CREATED=NO
SERVICE_STARTED=NO
FINISHED=NO
rollback(){
 status="$?"
 trap - EXIT INT TERM
 if [[ "$FINISHED" != YES ]]; then
   echo "V1_RESUME_ROLLBACK_BEGIN" >&2
   if [[ "$SITE_CHANGED" == YES ]]; then
     cp -a "$BACKUP" "$SITE" || true
     nginx -t >/dev/null 2>&1 && systemctl reload nginx || true
   fi
   if [[ "$SERVICE_STARTED" == YES ]]; then
     systemctl stop "$NAME" || true
   fi
   if [[ "$UNIT_CREATED" == YES ]]; then
     systemctl disable "$NAME" >/dev/null 2>&1 || true
     rm -f -- "$UNIT"
     systemctl daemon-reload || true
   fi
   echo "V1_RESUME_ROLLBACK_END" >&2
 fi
 exit "$status"
}
trap rollback EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

# Re-use immutable existing runtime; NEVER call npm/git clone again.
cat > "$UNIT" <<EOF
[Unit]
Description=Meu Artigo v1 private Auth0 pilot (deny all users)
After=network-online.target
Wants=network-online.target
[Service]
Type=simple
User=$RUN_USER
Group=$RUN_USER
WorkingDirectory=$ROOT/src/integrations/mcp-apps
ExecStart=/usr/bin/node $ROOT/src/integrations/mcp-apps/server.mjs --http
Environment=MEU_ARTIGO_BIND_HOST=127.0.0.1
Environment=MEU_ARTIGO_MCP_PORT=18087
Environment=MEU_ARTIGO_AUTH_MODE=auth0
Environment=MEU_ARTIGO_AUTH_ISSUER=$ISSUER
Environment=MEU_ARTIGO_AUTH_RESOURCE=$RESOURCE
Environment=MEU_ARTIGO_MCP_MULTIUSER=YES
Environment=MEU_ARTIGO_MCP_PRIVATE_PILOT=YES
Environment=MEU_ARTIGO_MCP_PILOT_SUBS=DENY_ALL
NoNewPrivileges=true
PrivateTmp=true
ProtectHome=true
ProtectSystem=strict
ProtectKernelTunables=true
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
CapabilityBoundingSet=
UMask=0077
Restart=on-failure
RestartSec=3
MemoryMax=512M
TasksMax=64
[Install]
WantedBy=multi-user.target
EOF
chmod 0644 "$UNIT"
UNIT_CREATED=YES
systemctl daemon-reload || fail "DAEMON_RELOAD_FAILED"
systemctl start "$NAME" || fail "SERVICE_START_FAILED"
SERVICE_STARTED=YES
READY=NO
for i in $(seq 1 60); do
  [[ "$(systemctl is-active "$NAME" 2>/dev/null || true)" == active ]] ||
   fail "SERVICE_CRASHED"
  code="$(curl --noproxy '*' -sS --max-time 2 -o /dev/null \
    -w '%{http_code}' http://127.0.0.1:18087/readyz 2>/dev/null || true)"
  if [[ "$code" == 200 ]]; then READY=YES; break; fi
  sleep 0.25
done
[[ "$READY" == YES ]] || fail "LOCAL_READINESS_FAILED"
for route in /.well-known/oauth-protected-resource \
 /.well-known/oauth-protected-resource/mcp; do
  json="$(curl --noproxy '*' -fsS --max-time 4 \
   "http://127.0.0.1:18087$route")" || fail "LOCAL_OAUTH_DISCOVERY_FAILED"
  JSON="$json" ISSUER="$ISSUER" RESOURCE="$RESOURCE" node -e '
   const x=JSON.parse(process.env.JSON);
   if(x.resource!==process.env.RESOURCE || x.authorization_servers?.length!==1 ||
    x.authorization_servers[0]!==process.env.ISSUER ||
    !x.scopes_supported?.includes("mcp:read"))process.exit(2);
  ' || fail "LOCAL_OAUTH_METADATA_INVALID"
done
code="$(curl --noproxy '*' -sS --max-time 3 \
 -X POST -H 'content-type: application/json' -d '{}' \
 -o /dev/null -w '%{http_code}' http://127.0.0.1:18087/mcp)" ||
 fail "LOCAL_UNAUTH_HTTP_FAILED"
[[ "$code" == 401 ]] || fail "LOCAL_UNAUTH_MCP_NOT_401"
grep -Fq 'Environment=MEU_ARTIGO_MCP_PILOT_SUBS=DENY_ALL' "$UNIT" ||
 fail "DENY_ALL_NOT_CONFIRMED"

tmp="$(mktemp "$SITE.v1-XXXXXXXX")" || fail "TEMPFILE_FAILED"
cp -p "$SITE" "$tmp" || fail "TEMP_COPY_FAILED"
sed -i 's@proxy_pass http://127\.0\.0\.1:18086;@proxy_pass http://127.0.0.1:18087;@' "$tmp"
[[ "$(grep -Fc 'proxy_pass http://127.0.0.1:18087;' "$tmp")" == 1 ]] ||
 fail "PROXY_REWRITE_INVALID"
mv -f -- "$tmp" "$SITE" || fail "PROXY_ATOMIC_REPLACE_FAILED"
SITE_CHANGED=YES
nginx -t >/dev/null 2>&1 || fail "UPDATED_NGINX_INVALID"
systemctl reload nginx || fail "NGINX_RELOAD_FAILED"

# Nginx reload is asynchronous. Wait for observed public truth rather than
# declaring failure on the very first request. Report only HTTP codes.
probe(){
  curl --noproxy '*' -sS --connect-timeout 4 --max-time 8 \
    --resolve "$HOST:443:$IP" -o /dev/null -w '%{http_code}' \
    "$@" 2>/dev/null || true
}
META=000
ANON=000
READY_PUBLIC=000
SUCCESS=NO
for i in $(seq 1 20); do
  META="$(probe "https://$HOST/.well-known/oauth-protected-resource")"
  ANON="$(probe -X POST -H 'content-type: application/json' -d '{}' "https://$HOST/mcp")"
  READY_PUBLIC="$(probe "https://$HOST/readyz")"
  if [[ "$META" == 200 && "$ANON" == 401 && "$READY_PUBLIC" == 404 ]]; then
    SUCCESS=YES
    break
  fi
  sleep 1
done
printf 'V1_RESUME_OBSERVED_PUBLIC_METADATA_HTTP=%s\n' "$META"
printf 'V1_RESUME_OBSERVED_PUBLIC_ANONYMOUS_HTTP=%s\n' "$ANON"
printf 'V1_RESUME_OBSERVED_PUBLIC_READYZ_HTTP=%s\n' "$READY_PUBLIC"
[[ "$SUCCESS" == YES ]] || fail "PUBLIC_ACCEPTANCE_MISMATCH"
[[ "$(systemctl is-active "$NAME")" == active ]] || fail "NEW_SERVICE_DOWN"
[[ "$(systemctl is-active meu-artigo-mcp.service)" == active ]] || fail "LEGACY_DOWN_POST"
[[ "$(systemctl is-active meu-artigo-e05-tunnel.service)" == active ]] ||
 fail "E05_DOWN_POST"
systemctl enable "$NAME" >/dev/null || fail "ENABLE_FAILED"
FINISHED=YES
printf 'V1_RESUME_PRIVATE_CUTOVER=PASS\n'
printf 'V1_RUNTIME_SHA=%s\n' "$SOURCE_SHA"
printf 'V1_AUTH0_PILOT=DENY_ALL\n'
printf 'V1_REAL_ACCOUNT_LOGIN=NOT_TESTED\n'
printf 'V1_MAIN_AND_PLUGINS=UNCHANGED\n'
printf 'V1_ROLLBACK_FILE=%s\n' "$BACKUP"
