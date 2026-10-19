#!/usr/bin/env bash
# Read-only, redacted operational inventory. Never reads or prints log events,
# tokens, environment variables, auth headers, account IDs, or file contents.
set -Eeuo pipefail
export LC_ALL=C
umask 077

usage() {
  printf 'Usage: bash v1-privacy-log-inventory.sh --audit\n' >&2
  exit 2
}
[[ "${1:-}" == "--audit" && "$#" -eq 1 ]] || usage
printf 'V1_PRIVACY_INVENTORY=SOURCE_AND_RUNTIME_ONLY\n'
printf 'V1_PRIVACY_INVENTORY_WRITES=NONE\n'

if [[ "$(id -u)" -ne 0 ]]; then
  printf 'V1_PRIVACY_INVENTORY=ROOT_REQUIRED_FOR_COMPLETE_READ\n'
  exit 2
fi
if ! command -v systemctl >/dev/null 2>&1; then
  printf 'V1_SYSTEMD=UNAVAILABLE\n'
else
  for service in meu-artigo-v1.service meu-artigo-mcp.service meu-artigo-e05-tunnel.service; do
    case "$service" in
      meu-artigo-v1.service) prefix=V1 ;;
      meu-artigo-mcp.service) prefix=LEGACY ;;
      meu-artigo-e05-tunnel.service) prefix=E05 ;;
    esac
    state="$(systemctl is-active "$service" 2>/dev/null || true)"
    case "$state" in
      active|inactive|failed|activating|deactivating) ;;
      *) state=UNKNOWN ;;
    esac
    printf 'V1_SERVICE_%s=%s\n' "$prefix" "$state"
    stdout="$(systemctl show "$service" --property=StandardOutput --value 2>/dev/null || true)"
    case "$stdout" in
      journal|journal+console|kmsg|kmsg+console) output=JOURNAL ;;
      null) output=NULL ;;
      file:*|append:*|truncate:*) output=FILE_BACKED ;;
      *) output=OTHER_OR_UNVERIFIED ;;
    esac
    printf 'V1_SERVICE_%s_STDOUT=%s\n' "$prefix" "$output"
  done
fi

site=/etc/nginx/sites-enabled/meu-artigo-mcp.conf
if [[ ! -e "$site" ]]; then
  printf 'V1_NGINX_SITE=NOT_FOUND\n'
else
  resolved="$(readlink -f -- "$site" 2>/dev/null || true)"
  if [[ "$resolved" != /etc/nginx/* || ! -f "$resolved" ]]; then
    printf 'V1_NGINX_SITE=UNSAFE_OR_UNVERIFIED\n'
  else
    printf 'V1_NGINX_SITE=FOUND\n'
    if grep -Eq '^[[:space:]]*access_log[[:space:]]+off[[:space:]]*;' "$resolved"; then
      printf 'V1_NGINX_SITE_ACCESS_LOG=OFF_DIRECTIVE_PRESENT\n'
    elif grep -Eq '^[[:space:]]*access_log[[:space:]]+' "$resolved"; then
      printf 'V1_NGINX_SITE_ACCESS_LOG=ON_DIRECTIVE_PRESENT\n'
    else
      printf 'V1_NGINX_SITE_ACCESS_LOG=INHERITED_OR_UNVERIFIED\n'
    fi
    if grep -Eq '^[[:space:]]*error_log[[:space:]]+' "$resolved"; then
      printf 'V1_NGINX_SITE_ERROR_LOG=EXPLICIT_DIRECTIVE_PRESENT\n'
    else
      printf 'V1_NGINX_SITE_ERROR_LOG=INHERITED_OR_UNVERIFIED\n'
    fi
    printf 'V1_NGINX_EFFECTIVE_LOGGING=REQUIRES_FULL_CONFIG_REVIEW\n'
  fi
fi

if command -v systemd-analyze >/dev/null 2>&1; then
  if journald_config="$(systemd-analyze cat-config systemd/journald.conf 2>/dev/null)"; then
    printf 'V1_JOURNALD_SOURCE=CONFIG_READ\n'
    for key in Storage MaxRetentionSec SystemMaxUse RuntimeMaxUse SystemKeepFree RuntimeKeepFree; do
      # Only expose a short allowlisted duration/storage setting, not raw files.
      value="$(printf '%s\n' "$journald_config" | awk -F= -v k="$key" '$0 ~ "^[[:space:]]*" k "[[:space:]]*=" {v=$2} END {print v}' | tr -d '[:space:]')"
      if [[ -z "$value" ]]; then
        value=INHERITED_OR_DEFAULT
      elif [[ ! "$value" =~ ^[A-Za-z0-9._-]{1,24}$ ]]; then
        value=REDACTED
      fi
      printf 'V1_JOURNALD_%s=%s\n' "$key" "$value"
    done
  else
    printf 'V1_JOURNALD_SOURCE=UNAVAILABLE\n'
  fi
else
  printf 'V1_JOURNALD_SOURCE=UNAVAILABLE\n'
fi

# A local reader cannot inspect provider-side tenant retention/streams.
printf 'V1_AUTH0_LOG_RETENTION=NOT_VERIFIED_CHECK_TENANT_PLAN\n'
printf 'V1_AUTH0_LOG_STREAMS=NOT_VERIFIED_CHECK_AUTH0_DASHBOARD\n'
printf 'V1_REVIEW_SCOPE=CONFIGURATION_ONLY_NO_LOG_EVENTS_READ\n'
printf 'V1_PRIVACY_INVENTORY_END=PASS_READ_ONLY\n'
