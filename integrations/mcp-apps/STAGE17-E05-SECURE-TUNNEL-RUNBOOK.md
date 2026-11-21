# E05 — Private ChatGPT homologation via Secure MCP Tunnel (operator runbook)

## Current state and guarantees

- Approval covers **isolated E05 configuration only**, with no merge/release and no change to the currently installed Meu Artigo pilot.
- This runbook **does not assert** that the user's OpenAI Platform organization has tunnel entitlement, Tunnels roles, an associated ChatGPT workspace, or a runtime key.
- Reference: https://developers.openai.com/api/docs/guides/secure-mcp-tunnels
- Reference: https://developers.openai.com/plugins/deploy/connect-chatgpt
- Existing VPS production path: `/opt/meu-artigo-stage17/src` (read only).
- E05 staging path: `/opt/meu-artigo-e05/src`, **a separate clone and UNIX identity**.
- Tunnel-mode transport: private **stdio** process `scripts/e05-synthetic-stdio.mjs`, launched by the OpenAI `tunnel-client` under `meuartigo-e05`. No public listener, no new Nginx route, no firewall change.
- E05 fixture-only guard accepts exactly the ALPHA or BRAVO fake request; other private research data, extra fields, and human gate approvals fail closed.
- Nothing accesses Drive. No private documents, paths or secrets must be copied into ChatGPT, logs or GitHub.

## Gate T0 — Account and tunnel availability (must be checked first)

1. Sign in to https://platform.openai.com/settings/organization/tunnels .
2. Check **Tunnels Read + Manage** for tunnel setup, **Tunnels Read + Use** for the runtime key and ChatGPT operator, and association with the intended ChatGPT workspace (if your account exposes that surface).
3. Provision an **E05-only tunnel**, not the existing pilot connection, or reuse a verified idle tunnel with equivalent isolation.
4. Create a restricted runtime API key for `tunnel-client`. **Never send its value to ChatGPT, this repo, a git commit, a screenshot or a shell command argument.** Keep it only in a secure local prompt/environment of the VPS session.
5. If tunnel creation, permission or workspace association is unavailable, **STOP**. Do not work around it by making the current Nginx/Auth0 endpoint unauthenticated.

## Gate T1 — VPS staging preparation, ROOT shell, no touch of production

Before using any command, compare current head with this PR and confirm the staging destination is not already occupied. Record a redacted output. The script never resets/removes the original stage17 tree.

```bash
set -Eeuo pipefail
BASE=/opt/meu-artigo-stage17/src
DEST=/opt/meu-artigo-e05
BRANCH=test/stage17-e05-chatgpt-isolated-20261017
echo "ORIGINAL_SHA=$(git -c safe.directory="$BASE" -C "$BASE" rev-parse HEAD)"
test "$(git -c safe.directory="$BASE" -C "$BASE" rev-parse HEAD)" = "fab60a8a2a254461d1fcd1fc66e67d7e109ed760" || { echo "ORIGINAL_DRIFT_STOP"; exit 1; }
test ! -e "$DEST/src" || { echo "E05_PATH_ALREADY_PRESENT_STOP"; exit 1; }
if ! id -u meuartigo-e05 >/dev/null 2>&1; then
  useradd --system --no-create-home --home-dir "$DEST" --shell /usr/sbin/nologin meuartigo-e05
fi
install -d -m 0750 -o meuartigo-e05 -g meuartigo-e05 "$DEST"
runuser -u meuartigo-e05 -- env GIT_TERMINAL_PROMPT=0 git clone --depth 1 --single-branch --branch "$BRANCH" \
  https://github.com/rebsonm/MeuArtigoSkill.git "$DEST/src"
```

**Note:** If the repository is private and `git clone` cannot authenticate noninteractively for this dedicated UNIX user, STOP. Use an operator-controlled authenticated transfer of the approved snapshot instead; **never paste a GitHub PAT into a command or URL**. Do not make the GitHub repository public merely for this test.

## Gate T2 — Strict SHA and build validation

Use the **exact reviewed HEAD SHA** reported in PR #81 after its six CI checks pass, not the prior approved E04 commit. If the PR head has moved, revalidate the latest commit and update the displayed placeholder yourself.

```bash
APPROVED_E05_SHA="REPLACE_WITH_REVIEWED_40_CHAR_SHA"
runuser -u meuartigo-e05 -- bash \
  /opt/meu-artigo-e05/src/integrations/mcp-apps/scripts/e05-stage-preflight.sh "$APPROVED_E05_SHA"
```

Require `E05_STAGING_PREFLIGHT_PASS`. This builds the bridge, tests the full MCP resource, tool contracts and **synthetic-only guard**. No server starts automatically. Do not begin T3 on any test failure.

## Gate T3 — Secure tunnel client installed and run as dedicated user

1. Obtain the signed/published `tunnel-client` binary from your Platform Tunnel settings or https://github.com/openai/tunnel-client/releases/latest . Follow the published checksum/signature procedure where available. Do not execute unreviewed remote `curl | bash` as root.
2. Install that verified binary with an absolute executable path available to the dedicated staging user; do not change the existing stage17 service or Nginx.
3. Start a **new interactive shell under staging user** (this user's home may have a nologin login shell; `runuser` may still execute bash):

```bash
runuser -u meuartigo-e05 -- /bin/bash
cd /opt/meu-artigo-e05
command -v tunnel-client
tunnel-client help quickstart
read -r -s -p 'Restricted runtime API key (invisible): ' CONTROL_PLANE_API_KEY
echo
export CONTROL_PLANE_API_KEY
read -r -p 'E05-only tunnel ID: ' E05_TUNNEL_ID
NODE_BIN="$(command -v node)"
tunnel-client init --profile meu-artigo-e05 --tunnel-id "$E05_TUNNEL_ID" \
  --mcp-command "$NODE_BIN /opt/meu-artigo-e05/src/integrations/mcp-apps/scripts/e05-synthetic-stdio.mjs"
tunnel-client doctor --profile meu-artigo-e05 --explain
tunnel-client run --profile meu-artigo-e05
```

The last command runs in foreground. Keep this session open throughout ChatGPT test. The key is **not** an Auth0 key and is **never** shared in chat. If `init` flags differ in the installed release, use `tunnel-client init --help` and stop rather than improvising insecure arguments. It is normal for the tunnel to be unreachable after terminating this session.

## Gate T4 — Separate ChatGPT TEST connection only

1. In https://chatgpt.com Plugins, choose **Add custom MCP server** → **Tunnel**, select the E05 tunnel or enter its `tunnel_id` as authorized by the workspace. Name the test connection `Meu Artigo — E05 Sintético`. Do **not** edit, delete, replace or refresh the existing pilot.
2. Complete authentication settings required by the UI. The fixture-only server has no user Drive access; workspace-limited tunnel access is still required. If the UI requires external OAuth not supported by the chosen tunnel, STOP.
3. Check `tools/list` shows `meu_artigo_painel` with the **E05 synthetic-only description** and resource `ui://meu-artigo/site-v3.html`, then start a **new chat** selecting ONLY the test plugin.
4. Run two calls separately with **no Drive or project files**:
  - ALPHA: one task `SYN-E05-A-01`, name `SYNTHETIC E05 ALPHA`, owner `Synthetic Researcher`, deadline null, seven gates all false, code REVIEW, explanation SYNTHETIC E05 REVIEW, responsible Synthetic Researcher; schema MEU_ARTIGO_SITE_V1, route documentary, total gates 7, partial false.
  - BRAVO: same fields, but task `SYN-E05-B-01` and `SYNTHETIC E05 BRAVO`.
5. Confirm ten screens, screenshot of displayed task, A disappears after B, no false approvals, no download/Drive claims. Resize and navigate: existing task must stay visible. Invalid projection must fail closed, never revealing the previous task.

### Capture evidence safely

Record the reviewed SHA, ChatGPT browser version, new test plugin name, rendered/non-rendered state, console **error codes** and pass/fail matrix. No API keys, JWTs, cookies, Authorization headers, HAR contents, private Drive names, personal research materials or project identifiers.

## Gate T5 — Stop and rollback

- Stop foreground `tunnel-client run` with **Ctrl+C**; clear restricted secret from the session with `unset CONTROL_PLANE_API_KEY` and exit. If you need to keep runtime configuration for another test, never put secrets in git.
- Confirm existing `meu-artigo-stage17` and `meu-artigo-stage17-auth0` systemd units are still active and original HEAD unchanged (observation only).
- Remove/deactivate E05 custom test connection or revoke the E05 tunnel/runtime key when the acceptance is complete, according to the account's controls. Do NOT uninstall the production Plugin.
- Any cleanup of `/opt/meu-artigo-e05` is a separate operator decision. Never use wildcard `rm -rf /opt/meu-artigo-*`.
- **E05 complete** only after the real ChatGPT E05 plugin renders both fixture projections correctly. Local/Chromium CI alone is not sufficient.

## Inline preference follow-up (E05 UI v3 — 2026-10-17)

- Original synthetic ALPHA rendered in a ChatGPT conversation side panel. New resource `ui://meu-artigo/site-v3.html` requests `preferredDisplayMode: "inline"` with fullscreen allowed for ten-screen navigation. This is a **host hint, not a forced mode**.
- The original E05 VPS checkout remains pinned to the former SHA until an operator performs a deliberate isolated-only update with the tunnel daemon stopped. **Do not update files while the old client is still serving them.** Existing profile, keys, and tunnel ID remain; never rerun T1 initial-clone instructions.
- The user must review the new PR #81 HEAD, pass all checks, stop the E05 foreground daemon with Ctrl+C, check the original stage17 SHA, fast-forward only `/opt/meu-artigo-e05/src` to the exact reviewed new SHA, rerun preflight, then restart E05 tunnel with the existing scoped Runtime key. No production restart. Refresh the *test* ChatGPT connection metadata and start a new chat before testing v3.
- Accept inline only with visual evidence; if the host still chooses side panel, record `HOST_INLINE_HINT_NOT_HONORED` without trying to bypass platform UI. No automatic requestDisplayMode without user action. No full E05 acceptance until BRAVO and all gates are tested.

## E05 Rerun — pinned go-live candidate #84 (2026-10-17)

**Status: operator execution required; NOT executed by the source review.**
The currently connected synthetic E05 tool returned
`McpServerError: Session terminated` during an authorized fixed ALPHA
invocation. This is a **connection failure**, not evidence of a visual defect,
a successful deployment, or a verified installed revision.

The deployment pin below identifies the **code candidate SHA that already passed
6/6 GitHub workflows**, before this documentary runbook amendment. New
commits on PR #84 must run their own CI, and the operator must independently
confirm that the pinned SHA remains the intended source for the E05 test.

- Previously CI-green code SHA (pinned E05 target): `bc06fd3503ed35b93291ee96fe720cf6bec69733`
- E05 staging only: `/opt/meu-artigo-e05/src`
- Original pilot path (read-only): `/opt/meu-artigo-stage17/src`
- Staging UNIX principal: `meuartigo-e05`
- No Nginx, systemd, Auth0, Drive, firewall, release, main, or installed main Plugin changes.

### U1 — Stop existing E05 tunnel foreground session

In the VPS shell that is running `tunnel-client run --profile meu-artigo-e05`,
press **Ctrl+C**. Do not kill a production service or restart any
`meu-artigo-stage17*` systemd unit. Keep runtime keys out of shell history.

### U2 — Execute pinned isolated update in the existing VPS root SSH session

The block below checks a read-only fingerprint of the unchanged pilot,
the isolated stage path and dedicated UNIX owner, a clean Git worktree,
an inactive E05 tunnel, the remote origin, exact branch tip and an ancestry
relationship before switching ONLY the E05 checkout. It refuses unexpected
state. It neither creates a staging clone nor modifies the original pilot.

```bash
set -Eeuo pipefail
TARGET=bc06fd3503ed35b93291ee96fe720cf6bec69733
BRANCH=feat/go-live-plugin-packaging-preflight-20261017
ORIGINAL=/opt/meu-artigo-stage17/src
E05=/opt/meu-artigo-e05/src
EXPECTED_ORIGINAL=fab60a8a2a254461d1fcd1fc66e67d7e109ed760

test "$(id -u)" -eq 0
test "$(git -c safe.directory="$ORIGINAL" -C "$ORIGINAL" rev-parse HEAD)" = "$EXPECTED_ORIGINAL" || {
  echo ORIGINAL_DRIFT_STOP >&2; exit 1;
}
test "$(realpath -e "$E05")" = "$E05"
test "$(stat -c '%U' "$E05")" = meuartigo-e05
test -z "$(git -c safe.directory="$E05" -C "$E05" status --porcelain)" || {
  echo E05_DIRTY_WORKTREE_STOP >&2; exit 1;
}
if pgrep -u meuartigo-e05 -f 'tunnel-client run' >/dev/null; then
  echo E05_TUNNEL_STILL_RUNNING_STOP >&2; exit 1
fi

runuser -u meuartigo-e05 -- env E05_TARGET="$TARGET" E05_BRANCH="$BRANCH" bash -s <<'E05_SCRIPT'
set -Eeuo pipefail
cd /opt/meu-artigo-e05/src
origin="$(git remote get-url origin)"
case "$origin" in
  https://github.com/rebsonm/MeuArtigoSkill|https://github.com/rebsonm/MeuArtigoSkill.git) ;;
  *) echo E05_UNEXPECTED_REMOTE_STOP >&2; exit 1 ;;
esac
git fetch --no-tags --depth=300 origin "refs/heads/$E05_BRANCH"
test "$(git rev-parse FETCH_HEAD)" = "$E05_TARGET" || {
  echo E05_BRANCH_SHA_CHANGED_STOP >&2; exit 1;
}
git merge-base --is-ancestor HEAD "$E05_TARGET" || {
  echo E05_NOT_FAST_FORWARD_STOP >&2; exit 1;
}
git switch --detach "$E05_TARGET"
test "$(git rev-parse HEAD)" = "$E05_TARGET"
bash integrations/mcp-apps/scripts/e05-stage-preflight.sh "$E05_TARGET"
E05_SCRIPT

echo E05_PINNED_SOURCE_AND_PREFLIGHT_COMPLETE
```

**Required evidence:** `E05_CANDIDATE_SHA=bc06fd...`, followed by
`E05_STAGING_PREFLIGHT_PASS` and
`E05_PINNED_SOURCE_AND_PREFLIGHT_COMPLETE`.
A `git fetch` or SHA-check failure is a hard STOP; do not use
`git reset --hard`, force checkout, re-clone, chmod production trees or
remove the staging directory as a workaround.

### U3 — Restart the existing private E05 tunnel

Use the already installed verified `tunnel-client`, existing E05-only
tunnel ID/profile, and a restricted runtime key entered invisibly.
Do **not** rerun `tunnel-client init` or overwrite the production pilot.

```bash
runuser -u meuartigo-e05 -- /bin/bash
cd /opt/meu-artigo-e05
read -r -s -p 'E05-only runtime API key (hidden): ' CONTROL_PLANE_API_KEY
echo
export CONTROL_PLANE_API_KEY
tunnel-client doctor --profile meu-artigo-e05 --explain
tunnel-client run --profile meu-artigo-e05
```

The last command is a foreground session. Do not paste the key,
token, profile contents, auth headers, or project data into ChatGPT.
An operator must observe the tunnel connected; if doctor fails, STOP.

### U4 — Real ChatGPT E05 acceptance

Refresh **only** the separate test plugin's metadata in ChatGPT, start
a **new conversation**, and select `Meu Artigo — E05 (Teste Sintético)`.
Invoke exactly the documented ALPHA then BRAVO fictional fixtures, with
all seven human scientific gates `approval_documented=false`.
Verify 10 menu pages, hover stability on `Fontes e buscas`, keyboard
focus, locale changes, resize, sidebar/inline host display, A-to-B
replacement, invalid input rejection, stale state clearance, CSP
behavior and absence of Drive/approval claims.

Record the source SHA, server-side preflight status, ChatGPT E05
connection result, and screenshots sanitized of user identifiers.
Do not state `E05_ACCEPTED` until the updated source is provably
active and the real ChatGPT checks have actually been observed.
