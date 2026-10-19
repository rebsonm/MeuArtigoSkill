#!/usr/bin/env bash
# Emergency E05-only shutdown and source rollback to last observed previous SHA.
set -Eeuo pipefail
[[ "$(id -u)" -eq 0 && "${1:-}" == "--apply" && $# -eq 1 ]] || { echo E05_ROLLBACK_STOP=AUTHORIZATION_REQUIRED >&2; exit 2; }
E05=/opt/meu-artigo-e05/src
PILOT=/opt/meu-artigo-stage17/src
OLD=f7bdf1b92d62163b1530549361416fc0789cf98b
TARGET=3ed581f941767e2b15b0b4a2f782b24151985540
PILOT_SHA=fab60a8a2a254461d1fcd1fc66e67d7e109ed760
UNIT=meu-artigo-e05-tunnel.service
[[ -d "$E05" && -d "$PILOT" ]] || exit 2
[[ "$(git -c safe.directory="$PILOT" -C "$PILOT" rev-parse HEAD)" == "$PILOT_SHA" ]] || { echo E05_ROLLBACK_STOP=PILOT_DRIFT >&2; exit 2; }
[[ "$(stat -c %U "$E05")" == meuartigo-e05 ]] || exit 2
systemctl disable --now "$UNIT" || { echo E05_ROLLBACK_STOP=SERVICE_STOP_FAILED >&2; exit 2; }
if pgrep -u meuartigo-e05 -x tunnel-client >/dev/null 2>&1; then echo E05_ROLLBACK_STOP=TUNNEL_STILL_RUNNING >&2; exit 2; fi
runuser -u meuartigo-e05 -- /bin/bash -s -- "$E05" "$OLD" "$TARGET" <<'STAGE_ONLY'
set -Eeuo pipefail
cd "$1"
head="$(git rev-parse HEAD)"
[[ "$head" == "$2" || "$head" == "$3" ]] || { echo E05_ROLLBACK_STOP=UNKNOWN_HEAD >&2; exit 3; }
[[ -z "$(git status --porcelain --untracked-files=normal)" ]] || { echo E05_ROLLBACK_STOP=DIRTY_STAGE >&2; exit 3; }
git merge-base --is-ancestor "$2" "$head" || { echo E05_ROLLBACK_STOP=NOT_ANCESTOR >&2; exit 3; }
git switch --detach "$2"
[[ "$(git rev-parse HEAD)" == "$2" ]] || exit 3
STAGE_ONLY
printf 'E05_ROLLBACK=PASS\nE05_AUTOSTART=DISABLED\nE05_CREDENTIAL=RETAINS_ROOT_PROTECTED_FILE_REQUIRES_REVOKE_IF_COMPROMISED\nE05_PILOT=UNCHANGED\n'
