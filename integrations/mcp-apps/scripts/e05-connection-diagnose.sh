#!/usr/bin/env bash
# Meu Artigo E05: read-only, sanitized tunnel/process diagnosis.
# Never reads/prints credentials, profile contents, logs, research files or Drive.
# Never starts, stops, modifies, downloads or connects to a network service.
set -Eeuo pipefail
umask 077

stage=/opt/meu-artigo-e05/src
pilot=/opt/meu-artigo-stage17/src
stage_user=meuartigo-e05
expected="${1:-}"

if (( $# > 1 )) || { [[ -n "$expected" ]] && [[ ! "$expected" =~ ^[0-9a-f]{40}$ ]]; }; then
  printf '%s\n' 'E05_DIAG_ARGUMENT=EXPECTED_SHA_OPTIONAL_40_HEX' >&2
  exit 2
fi

printf '%s\n' 'E05_DIAG_SCHEMA=MEU_ARTIGO_E05_READONLY_V1' 'E05_NO_CHANGES=YES'
if id -u "$stage_user" >/dev/null 2>&1; then
  echo 'E05_UNIX_USER=PRESENT'
  user_present=yes
else
  echo 'E05_UNIX_USER=ABSENT'
  user_present=no
fi

if [[ -d "$stage" ]]; then
  echo 'E05_STAGE_DIRECTORY=PRESENT'
  if [[ "$(realpath -e "$stage" 2>/dev/null || true)" == "$stage" ]]; then
    echo 'E05_STAGE_CANONICAL=YES'
  else
    echo 'E05_STAGE_CANONICAL=NO'
  fi
  if [[ "$(stat -c '%U' "$stage" 2>/dev/null || true)" == "$stage_user" ]]; then
    echo 'E05_STAGE_OWNER=EXPECTED'
  else
    echo 'E05_STAGE_OWNER=DIFFERENT_OR_UNKNOWN'
  fi
  if command -v git >/dev/null 2>&1; then
    sha="$(git -c safe.directory="$stage" -C "$stage" rev-parse --verify HEAD 2>/dev/null || true)"
  else
    sha=''
  fi
  if [[ "$sha" =~ ^[0-9a-f]{40}$ ]]; then
    echo "E05_STAGE_SHA=$sha"
    if [[ -n "$expected" ]]; then
      if [[ "$sha" == "$expected" ]]; then
        echo 'E05_STAGE_EXPECTED_SHA=MATCH'
      else
        echo 'E05_STAGE_EXPECTED_SHA=DIFFERENT'
      fi
    else
      echo 'E05_STAGE_EXPECTED_SHA=NOT_REQUESTED'
    fi
    if git -c safe.directory="$stage" -C "$stage" diff --quiet --ignore-submodules -- 2>/dev/null &&
       git -c safe.directory="$stage" -C "$stage" diff --cached --quiet --ignore-submodules -- 2>/dev/null &&
       [[ -z "$(git -c safe.directory="$stage" -C "$stage" ls-files --others --exclude-standard 2>/dev/null)" ]]; then
      echo 'E05_STAGE_WORKTREE=CLEAN'
    else
      echo 'E05_STAGE_WORKTREE=DIRTY_OR_UNKNOWN'
    fi
  else
    echo 'E05_STAGE_SHA=UNAVAILABLE'
    echo 'E05_STAGE_WORKTREE=UNVERIFIED'
  fi
  if [[ -f "$stage/integrations/mcp-apps/scripts/e05-synthetic-stdio.mjs" ]]; then
    echo 'E05_SYNTHETIC_ENTRY=EXISTS'
  else
    echo 'E05_SYNTHETIC_ENTRY=MISSING'
  fi
  stage_present=yes
else
  echo 'E05_STAGE_DIRECTORY=ABSENT'
  echo 'E05_STAGE_SHA=UNAVAILABLE'
  echo 'E05_STAGE_WORKTREE=UNVERIFIED'
  echo 'E05_SYNTHETIC_ENTRY=UNVERIFIED'
  stage_present=no
fi

if [[ -d "$pilot" ]] && command -v git >/dev/null 2>&1; then
  psha="$(git -c safe.directory="$pilot" -C "$pilot" rev-parse --verify HEAD 2>/dev/null || true)"
  if [[ "$psha" =~ ^[0-9a-f]{40}$ ]]; then
    echo "E05_ORIGINAL_PILOT_SHA=$psha"
  else
    echo 'E05_ORIGINAL_PILOT_SHA=UNVERIFIED'
  fi
else
  echo 'E05_ORIGINAL_PILOT_SHA=UNVERIFIED'
fi

# A tunnel-client executable can have other run modes and profiles. Only
# a process owned by the dedicated E05 UNIX user with these exact argument
# tokens is a profile match. This is NOT an API/control-plane readiness test.
tunnel=NO_MATCHING_PROCESS_DETECTED
if [[ "$user_present" == yes ]] && command -v pgrep >/dev/null 2>&1; then
  while IFS= read -r pid; do
    [[ "$pid" =~ ^[0-9]+$ ]] || continue
    [[ -r "/proc/$pid/cmdline" ]] || continue
    argv="$(tr '\0' '\n' < "/proc/$pid/cmdline" 2>/dev/null || true)"
    if printf '%s\n' "$argv" | grep -Fxq 'run' &&
       printf '%s\n' "$argv" | grep -Fxq -- '--profile' &&
       printf '%s\n' "$argv" | grep -Fxq -- 'meu-artigo-e05'; then
      tunnel=MATCHING_PROCESS_PRESENT
      break
    fi
  done < <(pgrep -u "$stage_user" -x tunnel-client 2>/dev/null || true)
elif [[ "$user_present" == yes ]]; then
  tunnel=PROCESS_CHECK_UNAVAILABLE
fi
echo "E05_TUNNEL_PROCESS=$tunnel"

if [[ "$stage_present" != yes ]]; then
  echo 'E05_NEXT_DIAGNOSIS=VERIFY_ISOLATED_STAGE_EXISTENCE'
elif [[ "$user_present" != yes ]]; then
  echo 'E05_NEXT_DIAGNOSIS=VERIFY_E05_UNIX_USER'
elif [[ "$tunnel" == NO_MATCHING_PROCESS_DETECTED ]]; then
  echo 'E05_NEXT_DIAGNOSIS=CHECK_FOREGROUND_TUNNEL_SESSION_WITH_OPERATOR'
elif [[ "$tunnel" == MATCHING_PROCESS_PRESENT ]]; then
  echo 'E05_NEXT_DIAGNOSIS=VERIFY_RUNTIME_HEALTH_AND_CHATGPT_CONNECTOR'
else
  echo 'E05_NEXT_DIAGNOSIS=READ_ONLY_PROCESS_CHECK_UNAVAILABLE'
fi
printf '%s\n' 'E05_REAL_CHATGPT_AUTH=CANNOT_BE_DETERMINED_LOCALLY' 'E05_DRIVE_AND_CSP=NOT_TESTED' 'E05_DIAG_COMPLETE=YES'
