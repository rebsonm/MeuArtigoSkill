#!/usr/bin/env bash
# Meu Artigo E05 - VPS autonomous staging ONLY. No main / real Drive / production changes.
# A one-time operator must run interactively as root on the authorized VPS.
set -Eeuo pipefail
umask 077

STAGE=/opt/meu-artigo-e05/src
PILOT=/opt/meu-artigo-stage17/src
OWNER=meuartigo-e05
PROFILE=meu-artigo-e05
SERVICE=meu-artigo-e05-tunnel.service
OLD=f7bdf1b92d62163b1530549361416fc0789cf98b
TARGET=3ed581f941767e2b15b0b4a2f782b24151985540
PILOT_SHA=fab60a8a2a254461d1fcd1fc66e67d7e109ed760
BRANCH=security/stage17-auth0-origin-hardening-20261018
REPO=https://github.com/rebsonm/MeuArtigoSkill.git
UNIT=/etc/systemd/system/$SERVICE
KEY=/etc/meu-artigo-e05/runtime-key
WRAPPER=/usr/local/libexec/meu-artigo-e05/start-tunnel.sh

fail(){ printf 'E05_BOOTSTRAP_STOP=%s\n' "$1" >&2; exit 1; }
step(){ printf 'E05_PROGRESS=%s\n' "$1"; }
[[ "$(id -u)" -eq 0 ]] || fail NOT_ROOT
[[ "${1:-}" == "--apply" && $# -eq 1 ]] || fail EXPECTED_APPLY_FLAG
for cmd in git runuser stat realpath systemctl systemd-analyze install pgrep npm node; do
  command -v "$cmd" >/dev/null 2>&1 || fail "MISSING_TOOL_${cmd}"
done
[[ -d "$STAGE" && -d "$PILOT" ]] || fail EXPECTED_CHECKOUT_MISSING
[[ "$(realpath -e "$STAGE")" == "$STAGE" ]] || fail STAGE_PATH_NOT_CANONICAL
[[ "$(realpath -e "$PILOT")" == "$PILOT" ]] || fail PILOT_PATH_NOT_CANONICAL
[[ "$(stat -c %U "$STAGE")" == "$OWNER" ]] || fail STAGE_OWNER_INVALID
[[ "$(git -c safe.directory="$PILOT" -C "$PILOT" rev-parse HEAD)" == "$PILOT_SHA" ]] || fail PILOT_DRIFT
[[ ! -e "$STAGE/.env" && ! -e "$STAGE/integrations/mcp-apps/.env" ]] || fail STAGE_ENV_NOT_ALLOWED
if systemctl is-active --quiet "$SERVICE"; then fail SERVICE_ALREADY_ACTIVE; fi
if pgrep -u "$OWNER" -x tunnel-client >/dev/null 2>&1; then fail OTHER_TUNNEL_PROCESS_ACTIVE; fi
if [[ -e "$UNIT" ]]; then fail EXISTING_SERVICE_UNIT_REQUIRES_MANUAL_REVIEW; fi

# Important: earlier root-run `git status` may have refreshed .git/index as root.
# Never run git status as root and never chmod/chown recursively.
GITDIR="$STAGE/.git"
[[ -d "$GITDIR" && ! -L "$GITDIR" ]] || fail GIT_DIR_NOT_OWNED_DIRECTORY
[[ "$(realpath -e "$GITDIR")" == "$GITDIR" ]] || fail GIT_DIR_NOT_CANONICAL
[[ "$(stat -c %U "$GITDIR")" == "$OWNER" ]] || fail GIT_DIR_OWNER_INVALID
INDEX="$GITDIR/index"
if [[ -e "$INDEX" ]]; then
  [[ -f "$INDEX" && ! -L "$INDEX" ]] || fail INDEX_NOT_REGULAR
  [[ "$(stat -c %h "$INDEX")" == 1 ]] || fail INDEX_HARDLINKED
  case "$(stat -c %U "$INDEX")" in
    "$OWNER") : ;;
    root)
      chown -- "$OWNER:$OWNER" "$INDEX" || fail INDEX_REPAIR_FAILED
      step 'REPAIRED_ROOT_OWNED_INDEX_ONLY'
      ;;
    *) fail UNEXPECTED_INDEX_OWNER ;;
  esac
fi
[[ ! -e "$GITDIR/index.lock" ]] || fail GIT_INDEX_LOCK_PRESENT
runuser -u "$OWNER" -- test -w "$GITDIR" || fail GIT_DIR_UNWRITABLE
[[ ! -e "$INDEX" ]] || runuser -u "$OWNER" -- test -w "$INDEX" || fail GIT_INDEX_UNWRITABLE

# All Git operations against the stage run as its dedicated account.
step STAGING_GIT_CHECKS
runuser -u "$OWNER" -- /bin/bash -s -- "$STAGE" "$OLD" "$TARGET" "$BRANCH" "$REPO" <<'STAGE_SCRIPT'
set -Eeuo pipefail
STAGE="$1"; OLD="$2"; TARGET="$3"; BRANCH="$4"; REPO="$5"
cd "$STAGE"
head="$(git rev-parse HEAD)"
if [[ "$head" != "$OLD" && "$head" != "$TARGET" ]]; then echo 'E05_BOOTSTRAP_STOP=UNEXPECTED_STAGE_HEAD' >&2; exit 3; fi
[[ -z "$(git status --porcelain --untracked-files=normal)" ]] || { echo E05_BOOTSTRAP_STOP=DIRTY_STAGE >&2; exit 3; }
origin="$(git remote get-url origin)"
case "$origin" in https://github.com/rebsonm/MeuArtigoSkill|https://github.com/rebsonm/MeuArtigoSkill.git) :;; *) echo E05_BOOTSTRAP_STOP=UNEXPECTED_GIT_ORIGIN >&2; exit 3;; esac
GIT_TERMINAL_PROMPT=0 git fetch --no-tags origin "refs/heads/$BRANCH"
git cat-file -e "$TARGET^{commit}"
git merge-base --is-ancestor "$TARGET" FETCH_HEAD || { echo E05_BOOTSTRAP_STOP=PINNED_SHA_NOT_ON_BRANCH >&2; exit 3; }
git merge-base --is-ancestor HEAD "$TARGET" || { echo E05_BOOTSTRAP_STOP=NON_FAST_FORWARD >&2; exit 3; }
if [[ "$head" != "$TARGET" ]]; then git switch --detach "$TARGET"; fi
[[ "$(git rev-parse HEAD)" == "$TARGET" ]] || { echo E05_BOOTSTRAP_STOP=POST_SWITCH_SHA_MISMATCH >&2; exit 3; }
[[ -z "$(git status --porcelain --untracked-files=normal)" ]] || { echo E05_BOOTSTRAP_STOP=POST_SWITCH_DIRTY >&2; exit 3; }
# This extensive preflight may modify the E05 build outputs only, not source or pilot.
bash integrations/mcp-apps/scripts/e05-stage-preflight.sh "$TARGET"
echo E05_SOURCE_AND_PREFLIGHT=PASS
STAGE_SCRIPT

[[ "$(git -c safe.directory="$PILOT" -C "$PILOT" rev-parse HEAD)" == "$PILOT_SHA" ]] || fail PILOT_CHANGED

# Never pass key as argv, via a Git commit, or via an environment file that
# could be readable by the runtime user. systemd LoadCredential copies it.
step VERIFY_RUNTIME_KEY
install -d -m 0700 -o root -g root /etc/meu-artigo-e05
if [[ -e "$KEY" ]]; then
  [[ -f "$KEY" && ! -L "$KEY" ]] || fail CREDENTIAL_NOT_REGULAR
  [[ "$(stat -c %U "$KEY")" == root && "$(stat -c %a "$KEY")" == 400 ]] || fail CREDENTIAL_PERMISSIONS_INVALID
  [[ "$(stat -c %h "$KEY")" == 1 ]] || fail CREDENTIAL_HARDLINKED
else
  [[ -r /dev/tty && -w /dev/tty ]] || fail REQUIRES_INTERACTIVE_TTY_FOR_INITIAL_KEY
  printf 'E05_KEY_ACTION=ENTER_RESTRICTED_RUNTIME_KEY_LOCALLY (input invisible)\n' >/dev/tty
  IFS= read -r -s RESTRICTED_KEY < /dev/tty || fail KEY_INPUT_FAILED
  [[ "$RESTRICTED_KEY" == sk-* && ${#RESTRICTED_KEY} -ge 20 ]] || fail INVALID_RUNTIME_KEY_FORMAT
  # Create atomically under root-only directory and without a key in logs/argv.
  tmpkey="$(mktemp /etc/meu-artigo-e05/.credential.XXXXXXXX)" || fail KEY_TMP_CREATE
  chmod 0400 "$tmpkey"
  printf '%s' "$RESTRICTED_KEY" > "$tmpkey"
  unset RESTRICTED_KEY
  mv -n -- "$tmpkey" "$KEY" || fail CREDENTIAL_INSTALL_FAILED
  [[ -f "$KEY" ]] || fail CREDENTIAL_INSTALL_FAILED
fi

# Validate a preexisting, operator-installed binary, never fetch executables.
BIN="${MEU_ARTIGO_E05_TUNNEL_BIN:-$(command -v tunnel-client || true)}"
[[ -n "$BIN" && "$BIN" == /* && "$BIN" =~ ^/[A-Za-z0-9_./-]+$ ]] || fail TUNNEL_BINARY_ABSOLUTE_PATH_REQUIRED
[[ -f "$BIN" && -x "$BIN" ]] || fail TUNNEL_BINARY_NOT_EXECUTABLE
BIN="$(realpath -e "$BIN")"
[[ "$BIN" =~ ^/[A-Za-z0-9_./-]+$ ]] || fail TUNNEL_BINARY_PATH_UNSAFE
[[ "$(stat -c %U "$BIN")" == root ]] || fail TUNNEL_BINARY_MUST_BE_ROOT_OWNED

[[ -f "$STAGE/integrations/mcp-apps/scripts/e05-vps-runtime-launch.sh" ]] || fail CANONICAL_LAUNCHER_NOT_IN_CHECKOUT
[[ -f /opt/meu-artigo-e05/tunnel-profiles/meu-artigo-e05.yaml ]] || fail E05_EXPLICIT_PROFILE_NOT_FOUND
runuser -u "$OWNER" -- test -r /opt/meu-artigo-e05/tunnel-profiles/meu-artigo-e05.yaml || fail E05_PROFILE_NOT_READABLE
step INSTALL_PERSISTENT_UNIT
install -d -m 0755 -o root -g root /usr/local/libexec/meu-artigo-e05
# Install the exact source-reviewed launcher. Never synthesize an untested inline wrapper.
SOURCE_LAUNCHER="$STAGE/integrations/mcp-apps/scripts/e05-vps-runtime-launch.sh"
[[ -f "$SOURCE_LAUNCHER" && ! -L "$SOURCE_LAUNCHER" ]] || fail REVIEWED_LAUNCHER_MISSING
install -m 0755 -o root -g root -- "$SOURCE_LAUNCHER" "$WRAPPER"
bash -n "$WRAPPER" || fail INSTALLED_LAUNCHER_INVALID
cat > "$UNIT" <<'UNIT_FILE'
[Unit]
Description=Meu Artigo E05 private synthetic-only tunnel (VPS autonomous)
Wants=network-online.target
After=network-online.target
StartLimitIntervalSec=300
StartLimitBurst=8

[Service]
Type=simple
User=meuartigo-e05
Group=meuartigo-e05
WorkingDirectory=/opt/meu-artigo-e05
Environment=HOME=/opt/meu-artigo-e05
Environment=PATH=/opt/meu-artigo-e05/bin:/usr/local/bin:/usr/bin:/bin
LoadCredential=control_plane_api_key:/etc/meu-artigo-e05/runtime-key
ExecStart=/usr/local/libexec/meu-artigo-e05/start-tunnel.sh
Restart=always
RestartPreventExitStatus=78
RestartSec=12s
TimeoutStartSec=30s
TimeoutStopSec=20s
NoNewPrivileges=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/opt/meu-artigo-e05
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
RestrictSUIDSGID=yes
UMask=0077
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
UNIT_FILE
chmod 0644 "$UNIT"
chown root:root "$UNIT"
systemd-analyze verify "$UNIT" >/dev/null || fail SYSTEMD_UNIT_VALIDATION_FAILED
systemctl daemon-reload
systemctl enable --now "$SERVICE" || fail SYSTEMD_START_FAILED
sleep 2
if systemctl is-active --quiet "$SERVICE"; then
  echo E05_PERSISTENT_SERVICE=ACTIVE
else
  echo E05_PERSISTENT_SERVICE=FAILED
  echo E05_OPERATOR_NEXT=REVIEW_SANITIZED_JOURNAL_LOCALLY
  exit 4
fi
if systemctl is-enabled --quiet "$SERVICE"; then
  echo E05_AUTOSTART=ENABLED
else
  fail AUTOSTART_NOT_ENABLED
fi
[[ "$(git -c safe.directory="$PILOT" -C "$PILOT" rev-parse HEAD)" == "$PILOT_SHA" ]] || fail PILOT_CHANGED_AT_END
printf 'E05_STAGE_SHA=%s\nE05_PILOT_UNCHANGED=YES\nE05_RUNTIME_KEY=SERVER_MANAGED_NO_OUTPUT\nE05_HOST_CHATGPT_UI=NOT_VERIFIED\nE05_BOOTSTRAP_COMPLETE=YES\n' "$TARGET"
