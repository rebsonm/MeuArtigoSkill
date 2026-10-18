#!/usr/bin/env bash
# Canonical E05 runtime: exact same profile and credential for doctor and run.
set -Eeuo pipefail
umask 077
export LC_ALL=C

CLIENT=/opt/meu-artigo-e05/bin/tunnel-client
PROFILE=/opt/meu-artigo-e05/tunnel-profiles/meu-artigo-e05.yaml
CREDENTIALS="${CREDENTIALS_DIRECTORY:-}"

stop() { printf 'E05_RUNTIME_STOP=%s\n' "$1" >&2; exit 78; }

case "${1:-}" in ""|--doctor-only) : ;; *) stop UNSUPPORTED_ARGUMENT ;; esac
[[ $# -le 1 ]] || stop TOO_MANY_ARGUMENTS
[[ "$(id -un)" == meuartigo-e05 ]] || stop WRONG_UNIX_PRINCIPAL
[[ -n "$CREDENTIALS" && "$CREDENTIALS" == /* ]] || stop CREDENTIAL_DIRECTORY_MISSING
[[ -f "$CREDENTIALS/control_plane_api_key" && -r "$CREDENTIALS/control_plane_api_key" ]] || stop CREDENTIAL_NOT_AVAILABLE
[[ -f "$PROFILE" && ! -L "$PROFILE" && -r "$PROFILE" ]] || stop ORIGINAL_PROFILE_UNAVAILABLE
[[ -f "$CLIENT" && ! -L "$CLIENT" && -x "$CLIENT" ]] || stop ORIGINAL_CLIENT_UNAVAILABLE

# Local doctor proves configuration only, not OpenAI remote authorization.
# Capture machine report in memory; never print the CLI's raw diagnostic text.
if ! python3 - "$CLIENT" "$PROFILE" "$CREDENTIALS/control_plane_api_key" <<'PY_DOCTOR'
import json, pathlib, subprocess, sys
client, profile, credential = sys.argv[1:]
try:
    raw = pathlib.Path(credential).read_bytes()
    if not (20 <= len(raw) <= 2048 and raw.startswith(b"sk-") and
            b"\x00" not in raw and b"\n" not in raw and b"\r" not in raw):
        print("E05_RUNTIME_STOP=CREDENTIAL_FORMAT_OR_READ_FAILED", file=sys.stderr)
        sys.exit(78)
    cmd = [client, "doctor", "--profile-file", profile,
           "--control-plane.api-key=file:" + credential, "--json"]
    # Some original E05 profiles have control_plane.api_key: env:CONTROL_PLANE_API_KEY.
    # The upstream profile loader resolves that YAML reference before applying
    # the explicit --control-plane.api-key=file override. Populate only this
    # child process's environment from the already protected systemd credential.
    process_env = dict(__import__("os").environ)
    process_env["CONTROL_PLANE_API_KEY"] = raw.decode("ascii")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            env=process_env, check=False, timeout=40)
    document = json.loads(result.stdout.decode("utf-8"))
    checks = {x.get("id"): x.get("status") for x in document.get("checks", [])
              if isinstance(x, dict)}
    required = ("config_source", "profile_load", "control_plane_api_key")
    if (result.returncode != 0 or document.get("result") != "ok" or
        document.get("failed_checks") or
        any(checks.get(k) != "PASS" for k in required)):
        for check_id in required:
            state = checks.get(check_id)
            safe_state = state if state in ("PASS", "FAIL", "SKIP") else "UNKNOWN"
            print("E05_RUNTIME_DOCTOR_" + check_id.upper() + "=" + safe_state,
                  file=sys.stderr)
        print("E05_RUNTIME_STOP=DOCTOR_LOCAL_CONTRACT_FAILED", file=sys.stderr)
        sys.exit(78)
except (OSError, ValueError, UnicodeError, subprocess.TimeoutExpired, TypeError, AttributeError, KeyError):
    print("E05_RUNTIME_STOP=DOCTOR_UNAVAILABLE", file=sys.stderr)
    sys.exit(78)
print("E05_RUNTIME_LOCAL_CONTRACT=PASS")
PY_DOCTOR
then
  exit 78
fi

if [[ "${1:-}" == "--doctor-only" ]]; then
  echo E05_RUNTIME_DOCTOR_ONLY=PASS
  exit 0
fi

# Keep the old env:-based profile contract, while the explicit file: flag
# continues to read from LoadCredential. No environment key is added to the
# systemd unit file or command-line arguments; it stays in this E05 process.
export CONTROL_PLANE_API_KEY="$(cat "$CREDENTIALS/control_plane_api_key")"
exec "$CLIENT" run --profile-file "$PROFILE" \
  --control-plane.api-key="file:$CREDENTIALS/control_plane_api_key"
