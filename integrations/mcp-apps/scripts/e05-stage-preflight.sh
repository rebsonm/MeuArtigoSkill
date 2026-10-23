#!/usr/bin/env bash
# E05 candidate only. Run as dedicated meuartigo-e05 (NOT root).
# No changes to /opt/meu-artigo-stage17, Nginx, Auth0, firewall or systemd.
set -Eeuo pipefail
umask 077
expected="${1:-}"
root="/opt/meu-artigo-e05/src"
app="$root/integrations/mcp-apps"
if [[ "$(id -un)" != "meuartigo-e05" ]]; then
  echo "E05_REFUSED_EXPECTED_DEDICATED_USER" >&2; exit 2
fi
if [[ ! "$expected" =~ ^[0-9a-f]{40}$ ]]; then
  echo "E05_REFUSED_NO_PINNED_SHA" >&2; exit 2
fi
if [[ "$(realpath -e "$root")" != "$root" ||
      "$(realpath -e "$app")" != "$app" ]]; then
  echo "E05_REFUSED_STAGE_PATH_MISMATCH" >&2; exit 2
fi
if [[ -e "$root/.env" || -e "$app/.env" ]]; then
  echo "E05_REFUSED_ENV_FILE_PRESENT" >&2; exit 2
fi
if [[ "$(git -C "$root" rev-parse HEAD)" != "$expected" ]]; then
  echo "E05_REFUSED_SHA_MISMATCH" >&2; exit 2
fi
if [[ -n "$(git -C "$root" status --porcelain --untracked-files=normal)" ]]; then
  echo "E05_REFUSED_DIRTY_REPO" >&2; exit 2
fi
if ! command -v npm >/dev/null || ! command -v node >/dev/null; then
  echo "E05_REFUSED_MISSING_NODE" >&2; exit 2
fi
node -e 'if(Number(process.versions.node.split(".")[0])<22)process.exit(2)'
cd "$app"
echo "E05_CANDIDATE_SHA=$expected"
echo "E05_NODE_VERSION=$(node --version)"
npm ci --ignore-scripts --no-audit --no-fund
npm run build
node --check server.mjs
node --check dist/bridge.js
node --check scripts/e05-synthetic-stdio.mjs
npm run test:ui-resource-contract
npm run test:e05-csp
npm run test:e05-synthetic
npm run test:smoke
npm run test:synthetic
npm run test:host-boundary
npm run test:stage10
npm run test:stage15
sha256sum dist/bridge.js
printf 'E05_STAGING_PREFLIGHT_PASS (no service started)\n'
