#!/usr/bin/env bash
# Private controlled cutover, no publication, no legacy/E05 modification.
# Fails closed with an automatic Nginx rollback on any unsuccessful check.
set -Eeuo pipefail
umask 077
SHA="02e03674e8e897d7f5e3f6769f7902062695b8dc"
REPO="https://github.com/rebsonm/MeuArtigoSkill.git"
BRANCH="release/prepare-public-mcp-20261018"
ROOT="/opt/meu-artigo-v1-runtime"
USER_NAME="meuartigo-v1run"
SERVICE="meu-artigo-v1.service"
UNIT="/etc/systemd/system/$SERVICE"
SITE_LINK="/etc/nginx/sites-enabled/meu-artigo-mcp.conf"
ISSUER="https://dev-w6estudk22tzwdil.us.auth0.com/"
RESOURCE="https://mcp.allflux.com.br/mcp"
HOST="mcp.allflux.com.br"
IP="84.247.134.242"
fail(){ echo "V1_STOP_$1" >&2; exit 2; }
[[ "$(id -u)" == 0 && "$#" -eq 1 && "$1" == "--apply" ]] || fail "EXPLICIT_ROOT_APPLY_REQUIRED"
for x in git npm node runuser useradd ss curl nginx systemctl sed cp mv grep realpath; do
 command -v "$x" >/dev/null 2>&1 || fail "TOOL_MISSING"
done
[[ "$(node -p 'process.versions.node.split(".")[0]')" == 22 ]] || fail "NODE_22_REQUIRED"
[[ ! -e "$ROOT" && ! -L "$ROOT" && ! -e "$UNIT" && ! -L "$UNIT" ]] || fail "V1_ALREADY_EXISTS"
id "$USER_NAME" >/dev/null 2>&1 && fail "V1_USER_ALREADY_EXISTS"
[[ -z "$(ss -H -ltn '( sport = :18087 )')" ]] || fail "PORT_18087_BUSY"
[[ "$(systemctl is-active meu-artigo-mcp.service)" == active ]] || fail "LEGACY_DOWN"
[[ "$(systemctl is-active meu-artigo-e05-tunnel.service)" == active ]] || fail "E05_DOWN"
[[ "$(git -c safe.directory=/opt/meu-artigo/repo -C /opt/meu-artigo/repo rev-parse HEAD)" == "cdd3affb902028753b9c66b83c2ef5e37f9e1700" ]] || fail "LEGACY_SHA_CHANGED"
SITE="$(realpath -e "$SITE_LINK")" || fail "NGINX_SITE_MISSING"
[[ "$SITE" == /etc/nginx/* ]] || fail "NGINX_SITE_OUT_OF_SCOPE"
grep -Fq "server_name $HOST;" "$SITE" || fail "HOST_MISMATCH"
grep -Fq 'location ^~ /.well-known/acme-challenge/' "$SITE" || fail "ACME_NOT_PRESENT"
grep -Fq 'location ~ ^/(mcp|\.well-known/oauth-protected-resource(/mcp)?)$' "$SITE" || fail "MCP_LOCATION_CHANGED"
grep -Fq 'location / { return 404; }' "$SITE" || fail "DEFAULT_DENY_MISSING"
[[ "$(grep -Fc 'proxy_pass http://127.0.0.1:18086;' "$SITE")" == 1 ]] || fail "UPSTREAM_NOT_EXACT"
[[ "$(grep -Ec '^[[:space:]]*server_name ' "$SITE")" == 2 ]] || fail "VHOST_COUNT_CHANGED"
[[ "$(grep -Ec '^[[:space:]]*ssl_certificate ' "$SITE")" == 1 ]] || fail "TLS_CHANGED"
nginx -t >/dev/null 2>&1 || fail "NGINX_ALREADY_INVALID"
install -d -m 0700 /var/backups/meu-artigo-v1-cutover
BACKUP="/var/backups/meu-artigo-v1-cutover/$(date -u +%Y%m%dT%H%M%SZ)-site.conf"
cp -a "$SITE" "$BACKUP" || fail "BACKUP_FAILED"
[[ -s "$BACKUP" ]] || fail "BACKUP_EMPTY"
SITE_CHANGED=NO
UNIT_CREATED=NO
SERVICE_STARTED=NO
DONE=NO
rollback(){
 rc=$?
 trap - EXIT
 if [[ "$DONE" != YES ]]; then
  echo "V1_AUTOMATIC_ROLLBACK_BEGIN" >&2
  if [[ "$SITE_CHANGED" == YES ]]; then
   cp -a "$BACKUP" "$SITE" || true
   nginx -t >/dev/null 2>&1 && systemctl reload nginx || true
  fi
  [[ "$SERVICE_STARTED" != YES ]] || systemctl stop "$SERVICE" || true
  if [[ "$UNIT_CREATED" == YES ]]; then
   systemctl disable "$SERVICE" >/dev/null 2>&1 || true
   rm -f -- "$UNIT"
   systemctl daemon-reload || true
  fi
  echo "V1_AUTOMATIC_ROLLBACK_END" >&2
 fi
 exit "$rc"
}
trap rollback EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
useradd --system --user-group --home-dir "$ROOT" --no-create-home --shell /usr/sbin/nologin "$USER_NAME" || fail "USER_CREATION"
install -d -m 0700 -o "$USER_NAME" -g "$USER_NAME" "$ROOT" || fail "DIR_CREATION"
runuser -u "$USER_NAME" -- env -i HOME="$ROOT" PATH="/usr/local/bin:/usr/bin:/bin" GIT_TERMINAL_PROMPT=0  ROOT="$ROOT" REPO="$REPO" BRANCH="$BRANCH" SHA="$SHA" bash -Eeuo pipefail -c '
 git clone --quiet --no-checkout --single-branch --branch "$BRANCH" "$REPO" "$ROOT/src"
 git -C "$ROOT/src" cat-file -e "$SHA^{commit}"
 git -C "$ROOT/src" checkout --quiet --detach "$SHA"
 [[ "$(git -C "$ROOT/src" rev-parse HEAD)" == "$SHA" ]]
 cd "$ROOT/src/integrations/mcp-apps"
 npm ci --ignore-scripts --no-audit --no-fund
 npm audit --omit=dev --audit-level=high
 npm run build
 npm run test:private-pilot
 node --check server.mjs
' || fail "SOURCE_OR_TEST_FAILED"
[[ "$(readlink -f "$(command -v node)")" == "/usr/bin/node" ]] || fail "NODE_NOT_SYSTEM_BINARY"
cat > "$UNIT" <<EOF
[Unit]
Description=Meu Artigo v1 private Auth0 pilot - denied by default
After=network-online.target
Wants=network-online.target
[Service]
Type=simple
User=$USER_NAME
Group=$USER_NAME
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
systemctl start "$SERVICE" || fail "SERVICE_START_FAILED"
SERVICE_STARTED=YES
READY=NO
for i in $(seq 1 80); do
 [[ "$(systemctl is-active "$SERVICE" 2>/dev/null || true)" == active ]] || fail "SERVICE_CRASHED"
 CODE="$(curl --noproxy '*' -sS --max-time 2 -o /dev/null -w '%{http_code}' http://127.0.0.1:18087/readyz 2>/dev/null || true)"
 if [[ "$CODE" == 200 ]]; then READY=YES; break; fi
 sleep 0.25
done
[[ "$READY" == YES ]] || fail "LOCAL_READINESS_FAILED"
for PATHNAME in /.well-known/oauth-protected-resource /.well-known/oauth-protected-resource/mcp; do
 JSON="$(curl --noproxy '*' -fsS --max-time 5 "http://127.0.0.1:18087$PATHNAME")" || fail "LOCAL_METADATA_FAIL"
 JSON="$JSON" RESOURCE="$RESOURCE" ISSUER="$ISSUER" node -e '
 const j=JSON.parse(process.env.JSON);
 if(j.resource!==process.env.RESOURCE || j.authorization_servers?.length!==1 ||
  j.authorization_servers[0]!==process.env.ISSUER ||
  !j.scopes_supported?.includes("mcp:read"))process.exit(2);
 ' || fail "METADATA_CONTENT_FAIL"
done
CODE="$(curl --noproxy '*' -sS --max-time 5 -X POST -H 'content-type: application/json' -d '{}' -o /dev/null -w '%{http_code}' http://127.0.0.1:18087/mcp)" || fail "LOCAL_MCP_FAIL"
[[ "$CODE" == 401 ]] || fail "LOCAL_ANONYMOUS_ALLOWED"
grep -Fq 'Environment=MEU_ARTIGO_MCP_PILOT_SUBS=DENY_ALL' "$UNIT" || fail "PILOT_NOT_DENY_ALL"
TEMP="$(mktemp "$SITE.v1-XXXXXXXX")" || fail "TEMPFILE_FAIL"
cp -p "$SITE" "$TEMP" || fail "TEMP_COPY_FAIL"
sed -i 's@proxy_pass http://127\.0\.0\.1:18086;@proxy_pass http://127.0.0.1:18087;@' "$TEMP"
[[ "$(grep -Fc 'proxy_pass http://127.0.0.1:18087;' "$TEMP")" == 1 ]] || fail "REWRITE_FAIL"
mv -f -- "$TEMP" "$SITE" || fail "REPLACEMENT_FAILED"
SITE_CHANGED=YES
nginx -t >/dev/null 2>&1 || fail "NGINX_INVALID"
systemctl reload nginx || fail "NGINX_RELOAD_FAILED"
test_http(){
 curl -sS --connect-timeout 5 --max-time 12 --resolve "$HOST:443:$IP"   -o /dev/null -w '%{http_code}' "$@" 2>/dev/null || true
}
META="$(test_http "https://$HOST/.well-known/oauth-protected-resource")"
UNAUTH="$(test_http -X POST -H 'content-type: application/json' -d '{}' "https://$HOST/mcp")"
HEALTH="$(test_http "https://$HOST/readyz")"
[[ "$META" == 200 && "$UNAUTH" == 401 && "$HEALTH" == 404 ]] || fail "PUBLIC_ACCEPTANCE_FAILED"
[[ "$(systemctl is-active meu-artigo-mcp.service)" == active ]] || fail "LEGACY_CHANGED"
[[ "$(systemctl is-active meu-artigo-e05-tunnel.service)" == active ]] || fail "E05_CHANGED"
systemctl enable "$SERVICE" >/dev/null || fail "SERVICE_ENABLE_FAILED"
DONE=YES
echo "V1_PRIVATE_CUTOVER=PASS"
echo "V1_SHA=$SHA"
echo "V1_PUBLIC_METADATA=200"
echo "V1_PUBLIC_UNAUTH_MCP=401"
echo "V1_PUBLIC_READYZ=404"
echo "V1_AUTH0_PILOT=DENY_ALL"
echo "V1_REAL_LOGIN=NOT_TESTED"
echo "V1_LEGACY_AND_E05=PRESERVED"
echo "V1_NGINX_ROLLBACK=$BACKUP"
echo "V1_PLUGIN_AND_MAIN=UNCHANGED"
