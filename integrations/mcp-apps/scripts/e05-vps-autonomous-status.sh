#!/usr/bin/env bash
# Read-only remote status: never emit secrets, profile YAML, or research payloads.
set -Eeuo pipefail
E05=/opt/meu-artigo-e05/src
PILOT=/opt/meu-artigo-stage17/src
UNIT=meu-artigo-e05-tunnel.service
printf 'E05_STATUS_SCHEMA=E05_SYSTEMD_V1\n'
for cmd in git systemctl stat; do command -v "$cmd" >/dev/null || exit 2; done
if [[ -d "$E05" ]]; then
  git -c safe.directory="$E05" -C "$E05" rev-parse HEAD 2>/dev/null | sed 's/^/E05_SHA=/' || echo E05_SHA=UNKNOWN
  echo "E05_OWNER=$(stat -c %U "$E05")"
else echo E05_STAGE=MISSING; fi
if [[ -d "$PILOT" ]]; then
  git -c safe.directory="$PILOT" -C "$PILOT" rev-parse HEAD 2>/dev/null | sed 's/^/E05_PILOT_SHA=/' || echo E05_PILOT_SHA=UNKNOWN
fi
printf 'E05_SYSTEMD_ENABLED=%s\n' "$(systemctl is-enabled "$UNIT" 2>/dev/null || true)"
printf 'E05_SYSTEMD_ACTIVE=%s\n' "$(systemctl is-active "$UNIT" 2>/dev/null || true)"
printf 'E05_RUNTIME_TUNNEL_READY=NOT_PROVEN_BY_SYSTEMD\nE05_CHATGPT_CSP_AND_DRIVE=NOT_TESTED\n'
