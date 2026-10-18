#!/usr/bin/env bash
# E05 ONLY: guarded repair of an already installed VPS tunnel service.
# No npm, no git checkout, no credential changes, no changes to the original pilot.
set -Eeuo pipefail
umask 077
readonly SERVICE=meu-artigo-e05-tunnel.service
readonly UNIT=/etc/systemd/system/meu-artigo-e05-tunnel.service
readonly WRAPPER=/usr/local/libexec/meu-artigo-e05/start-tunnel.sh
readonly DROPINDIR=/etc/systemd/system/meu-artigo-e05-tunnel.service.d
readonly DROPIN=/etc/systemd/system/meu-artigo-e05-tunnel.service.d/90-meu-artigo-e05-local-fail.conf
readonly KEY=/etc/meu-artigo-e05/runtime-key
readonly PROFILE=/opt/meu-artigo-e05/tunnel-profiles/meu-artigo-e05.yaml
readonly E05_SRC=/opt/meu-artigo-e05/src
readonly PILOT=/opt/meu-artigo-stage17/src
readonly PILOT_SHA=fab60a8a2a254461d1fcd1fc66e67d7e109ed760
readonly LAUNCHER_BLOB=4fd0918974c03265df920d300ee3e69357ca6ea3
die(){ echo "E05_ACTIVATE_STOP=$1" >&2; exit 2; }
[[ "$(id -u)" == 0 && $# -eq 2 ]] || die EXPLICIT_APPLY_AND_PIN_REQUIRED
[[ "$1" == --apply && "$2" =~ ^[0-9a-f]{40}$ ]] || die EXPLICIT_APPLY_AND_PIN_REQUIRED
readonly SOURCE_REF="$2"
for exe in systemd-run systemctl systemd-analyze stat git curl runuser mktemp install python3 bash grep realpath timeout; do
  command -v "$exe" >/dev/null || die MISSING_REQUIRED_TOOL
done
[[ -f "$UNIT" && ! -L "$UNIT" && -f "$WRAPPER" && ! -L "$WRAPPER" ]] || die EXISTING_UNIT_OR_WRAPPER_NOT_TRUSTED
[[ "$(stat -c %U:%h "$UNIT")" == root:1 && "$(stat -c %U:%h "$WRAPPER")" == root:1 ]] || die EXISTING_UNIT_OR_WRAPPER_OWNER_INVALID
[[ "$(stat -c %U:%a:%h "$KEY")" == root:400:1 && -f "$KEY" && ! -L "$KEY" ]] || die RESTRICTED_RUNTIME_CREDENTIAL_UNSAFE
[[ -f "$PROFILE" && ! -L "$PROFILE" ]] || die EXPECTED_PROFILE_MISSING
runuser -u meuartigo-e05 -- test -r "$PROFILE" || die PROFILE_UNREADABLE_BY_E05
[[ "$(git -c safe.directory="$PILOT" -C "$PILOT" rev-parse HEAD 2>/dev/null)" == "$PILOT_SHA" ]] || die ORIGINAL_PILOT_SHA_MISMATCH
[[ -d "$E05_SRC" ]] || die ISOLATED_SOURCE_MISSING
[[ "$(stat -c %U "$E05_SRC")" == meuartigo-e05 ]] || die ISOLATED_SOURCE_OWNER_CHANGED
[[ "$(systemctl show "$SERVICE" -p User --value)" == meuartigo-e05 ]] || die WRONG_SYSTEMD_PRINCIPAL
[[ "$(systemctl show "$SERVICE" -p FragmentPath --value)" == "$UNIT" ]] || die UNEXPECTED_SYSTEMD_FRAGMENT
grep -Fxq 'LoadCredential=control_plane_api_key:/etc/meu-artigo-e05/runtime-key' "$UNIT" || die UNIT_CREDENTIAL_DECLARATION_MISMATCH
grep -Fxq 'ExecStart=/usr/local/libexec/meu-artigo-e05/start-tunnel.sh' "$UNIT" || die UNIT_EXECSTART_DECLARATION_MISMATCH
systemctl show "$SERVICE" -p ExecStart --value | grep -Fq "$WRAPPER" || die EFFECTIVE_EXECSTART_CHANGED
systemctl is-active --quiet "$SERVICE" && die SERVICE_ALREADY_ACTIVE
if pgrep -u meuartigo-e05 -x tunnel-client >/dev/null 2>&1; then die ANOTHER_E05_TUNNEL_RUNNING; fi
[[ ! -e "$DROPIN" && ! -L "$DROPIN" ]] || die PREEXISTING_E05_REPAIR_DROPIN
echo E05_ACTIVATE_PRECONDITIONS=PASS

work="$(mktemp -d /root/.e05-activate.XXXXXXXX)" || die TEMP_DIRECTORY_FAILED
# Root-only workspace contains rollback backups and captured doctor output.
# Transient systemd runs as meuartigo-e05 and cannot traverse /root.
# Export only the already verified public launcher into a group-readable /run path.
probe=""
changed=NO
accepted=NO
cleanup() {
  status=$?
  if [[ "$changed" == YES && "$accepted" != YES ]]; then
    systemctl stop "$SERVICE" >/dev/null 2>&1 || true
    install -m 0755 -o root -g root "$work/original-wrapper" "$WRAPPER" || true
    rm -f -- "$DROPIN"
    systemctl daemon-reload >/dev/null 2>&1 || true
    echo E05_ACTIVATE_ROLLBACK=ORIGINAL_WRAPPER_RESTORED_SERVICE_STOPPED
  fi
  if [[ -n "$probe" ]]; then
    rm -f -- "$probe/launcher"
    rmdir "$probe" 2>/dev/null || true
  fi
  rm -f -- "$work/launcher" "$work/original-wrapper" "$work/preflight" "$work/preflight.err"
  rmdir "$work" 2>/dev/null || true
  exit "$status"
}
trap cleanup EXIT
readonly URI="https://raw.githubusercontent.com/rebsonm/MeuArtigoSkill/$SOURCE_REF/integrations/mcp-apps/scripts/e05-vps-runtime-launch.sh"
curl --fail --location --silent --show-error --max-time 40 --proto '=https' --tlsv1.2 --output "$work/launcher" "$URI" || die PINNED_LAUNCHER_FETCH_FAILED
[[ "$(git hash-object "$work/launcher")" == "$LAUNCHER_BLOB" ]] || die PINNED_LAUNCHER_INTEGRITY_FAIL
bash -n "$work/launcher" || die PINNED_LAUNCHER_INVALID
chmod 0755 "$work/launcher"
echo E05_ACTIVATE_PINNED_SOURCE=VERIFIED

# The script is public, checksum-pinned and contains no credentials. The service
# identity may read it via this root-owned, dedicated-group /run directory.
# Do not expose private backup files or doctor diagnostics stored under /root.
probe="$(mktemp -d /run/.e05-doctor-XXXXXXXX)" || die PROBE_DIRECTORY_CREATE_FAILED
chown root:meuartigo-e05 "$probe" || die PROBE_DIRECTORY_GROUP_FAILED
chmod 0750 "$probe" || die PROBE_DIRECTORY_MODE_FAILED
install -m 0750 -o root -g meuartigo-e05 -- "$work/launcher" "$probe/launcher" || die PROBE_LAUNCHER_INSTALL_FAILED
[[ "$(stat -c %U:%G:%a "$probe")" == root:meuartigo-e05:750 ]] || die PROBE_DIRECTORY_PERMISSIONS_FAILED
runuser -u meuartigo-e05 -- test -r "$probe/launcher" || die PROBE_LAUNCHER_UNREADABLE_BY_SERVICE_USER
echo E05_ACTIVATE_PROBE_USER_ACCESS=PASS

# Exact same LoadCredential source and dedicated UNIX user as the real service;
# '--doctor-only' never polls/starts an additional tunnel runtime.
if ! timeout 55 systemd-run --quiet --wait --collect --pipe \
  --unit="meu-artigo-e05-doctor-$$" \
  --property=User=meuartigo-e05 \
  --property=Group=meuartigo-e05 \
  --property=WorkingDirectory=/opt/meu-artigo-e05 \
  --property="LoadCredential=control_plane_api_key:$KEY" \
  -- /bin/bash "$probe/launcher" --doctor-only >"$work/preflight" 2>"$work/preflight.err"; then
  # Emit only launcher-owned finite-state codes, not raw journal or error text.
  grep -E '^E05_RUNTIME_(DOCTOR_(CONFIG_SOURCE|PROFILE_LOAD|CONTROL_PLANE_API_KEY)=(PASS|FAIL|SKIP|UNKNOWN)|STOP=[A-Z_]+)$' "$work/preflight.err" || true
  die SAME_IDENTITY_CREDENTIAL_DOCTOR_FAILED
fi
grep -Fxq 'E05_RUNTIME_LOCAL_CONTRACT=PASS' "$work/preflight" || die DOCTOR_CONTRACT_DID_NOT_PASS
grep -Fxq 'E05_RUNTIME_DOCTOR_ONLY=PASS' "$work/preflight" || die DOCTOR_MODE_DID_NOT_PASS
echo E05_ACTIVATE_REAL_SYSTEMD_DOCTOR=PASS

cp -p -- "$WRAPPER" "$work/original-wrapper"
changed=YES
install -m 0755 -o root -g root -- "$work/launcher" "$WRAPPER"
install -d -m 0755 -o root -g root "$DROPINDIR"
printf '[Service]\nRestartPreventExitStatus=78\n' > "$DROPIN"
chmod 0644 "$DROPIN"
chown root:root "$DROPIN"
systemd-analyze verify "$UNIT" >/dev/null || die SYSTEMD_UNIT_VERIFY_FAILED
systemctl daemon-reload
systemctl reset-failed "$SERVICE" >/dev/null 2>&1 || true
systemctl restart "$SERVICE" || die E05_SERVICE_START_FAILED
sleep 4
restarts="$(systemctl show "$SERVICE" -p NRestarts --value)"
sleep 21
[[ "$restarts" == "$(systemctl show "$SERVICE" -p NRestarts --value)" ]] || die E05_TUNNEL_RESTARTED_DURING_ACCEPTANCE
systemctl is-active --quiet "$SERVICE" || die E05_TUNNEL_NOT_ACTIVE
systemctl is-enabled --quiet "$SERVICE" || die E05_AUTOSTART_NOT_ENABLED
[[ "$(git -c safe.directory="$PILOT" -C "$PILOT" rev-parse HEAD 2>/dev/null)" == "$PILOT_SHA" ]] || die PILOT_SHA_CHANGED
accepted=YES
echo E05_ACTIVATE_SYSTEMD=ACTIVE_STABLE_25_SECONDS
echo E05_ACTIVATE_AUTOSTART=ENABLED
echo E05_ACTIVATE_PILOT=UNCHANGED
# /readyz belongs to E05 only when its listener is demonstrably owned by MainPID.
pid="$(systemctl show "$SERVICE" -p MainPID --value)"
if [[ "$pid" =~ ^[1-9][0-9]*$ ]] && command -v ss >/dev/null && \
  ss -ltnp '( sport = :8080 )' 2>/dev/null | grep -Fq "pid=$pid," && \
  curl --fail --silent --max-time 3 --output /dev/null http://127.0.0.1:8080/readyz; then
  echo E05_ACTIVATE_LOOPBACK_READYZ=PASS_E05_PID_MATCHED
else
  echo E05_ACTIVATE_LOOPBACK_READYZ=NOT_VERIFIED_NO_PID_MATCHED_READY_RESPONSE
fi
echo E05_ACTIVATE_CHATGPT_REAL_HOST=NOT_TESTED
echo E05_ACTIVATE_COMPLETE=YES
