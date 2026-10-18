# Meu Artigo — Stage 17 / E05: live ChatGPT visual acceptance

**Status: PARTIAL LIVE E05 (ALPHA renders in ChatGPT side panel); inline presentation and full matrix PENDING.** 2026-10-17.
**Base:** stacked Draft PR #80, E04-accepted SHA `17bfb7399ba850165c37e44624bfb755f0cf79dc`.
**This E05 candidate:** `test/stage17-e05-chatgpt-isolated-20261017`.
Do NOT mark E05 completed based on local/CI/browser basic-host success.

## E05 real ChatGPT evidence and inline correction — 2026-10-17

- The user independently created the restricted E05 tunnel, validated the release checksum and Sigstore attestation, installed the isolated client, and confirmed `/healthz = live` and `/readyz = ready`.
- The separate E05 test Plugin was connected in ChatGPT; `meu_artigo_painel` accepted the fixed ALPHA fixture with 1 synthetic task and seven unapproved gates, and the screenshot confirms the widget visibly rendered with the overview and navigation. This closes the **previous render-crash symptom** for ALPHA in the real ChatGPT host; it does not prove all ten screens or BRAVO.
- User feedback: the ChatGPT host chose a **conversation side panel**; inline rendering in the message body is the desired experience. A side-panel render is not an HTML or MCP failure.
- Corrective UI metadata: `_meta["openai/ui"] = {preferredDisplayMode: "inline", availableDisplayModes: ["inline", "fullscreen"]}` in the resource. Preference is a hint; the host MAY override it. No automatic `requestDisplayMode` invocation is appropriate (it requires user action). See https://github.com/openai/mcp-extensions/blob/main/docs/spec.md .
- Use new UI cache key **`ui://meu-artigo/site-v3.html`** consistently in tool metadata, resource response and tests. Scientific **data schema remains `MEU_ARTIGO_SITE_V1`**.
- Source/browser acceptance: run both fixed ALPHA and BRAVO in a NEW ChatGPT conversation after the isolated VPS runtime has been safely updated and restarted, the test connection metadata has been refreshed if supported, and the new URI is confirmed. Confirm actual inline vs side-panel rendering separately, ten-screen expansion/navigation, host context changes and privacy rejection. Do **not** claim inline is guaranteed or E05 fully accepted without a screenshot.
- Update ONLY the isolated E05 stage. Current pilot services, main, Auth0, Nginx and Drive remain untouched. No merge, release, installed Plugin modification, or autonomous production deployment.

## Purpose and dependencies
The candidate addresses two proven bugs corrected in PR #80: (a) literal JavaScript substitution expanding the HTML into 28 scripts; (b) host-context changes clearing an already received snapshot. The E05 inline-preference follow-up publishes the **new** cache key `ui://meu-artigo/site-v3.html` (tool `_meta.ui.resourceUri`, `openai/outputTemplate`, `resources/read` all consistent). Scientific schema stays `MEU_ARTIGO_SITE_V1`: **resource version is not a data contract change**.

The latest docs say to refresh metadata for custom MCP connections after tool/UI changes and start a new ChatGPT conversation. See https://developers.openai.com/plugins/deploy/connect-chatgpt and https://developers.openai.com/plugins/build/chatgpt-ui .

## Authorization hold before ANY external modification
No change to existing VPS services, public Nginx, Auth0 tenant/app, scope, user allowlist, Google Drive, live Plugin or installed connection. No PR merge or release.
A **separate explicit user approval** must name the chosen test connection method:
1. Prefer a private temporary MCP Tunnel or other genuinely isolated endpoint supported by the user's environment, **if** its authentication and privacy requirements can be demonstrated and consented to. Never disable authorization for a public endpoint.
2. Otherwise: a separate HTTPS test hostname/path, separate loopback port, separate systemd unit, independent OAuth configuration and explicitly restricted test identity, with a documented rollback. Resolve potential audience mismatch before use. Nothing is public without authorization and reviewed controls.
3. If neither can be isolated safely, STOP; do not repurpose the current installed pilot.

**Never** send bearer tokens, signed JWTs, cookies, OAuth secrets, identifiable Drive files or manuscripts to logs/commits/ChatGPT messages.

## Preflight — must pass before authorizing live stage
- [ ] E05 SHA is frozen; inspect full changed-files diff vs PR #80; no changes outside URI version and acceptance documents/tests.
- [ ] `npm ci --ignore-scripts --no-audit --no-fund && npm run build` on the exact SHA.
- [ ] `npm run test:ui-resource-contract` asserts `site-v2.html`, MIME `text/html;profile=mcp-app`, 3 actual script elements, ten screens, zero untrusted external domains, same seven gates.
- [ ] `npm run test:smoke` and full MCP Apps, host isolation, privacy, CodeQL and release-audit gates pass.
- [ ] E04 Chromium basic-host passes at the E05 SHA (same synthetic fixture).
- [ ] The final HTML and bridge hashes recorded in release manifest only (no private content).
- [ ] Rollback plan ready, and installed old service verified unchanged (no guessed status).

## E05 acceptance protocol (real ChatGPT; authorized test-only connection)
1. Create/connect a **new isolated private testing plugin connection** referencing only the approved test endpoint/tunnel; leave currently installed `Meu Artigo — MCP Piloto` untouched.
2. Verify the newly connected plugin's `tools/list` advertises `meu_artigo_painel`, `outputSchema.site`, the exact `ui://meu-artigo/site-v3.html` URI and `openai/outputTemplate`.
3. Explicitly refresh new test connection metadata if necessary, start a NEW chat, select only test plugin, never rely on an old conversation's cached UI.
4. First call with a **single synthetic snapshot** (`SYNTH-E05-A`) and seven gates all unapproved, no Drive/files.
5. Record separately: MCP tool-call result; whether UI resource was read (only if observable); iframe loaded; JavaScript exception/CSP; bridge `CONNECTED`, `TOOL_RESULT_RECEIVED`, `SNAPSHOT_SHOWN`; visible synthetic task; ten-screen navigation.
6. Test size/theme/locale changes **without clearing** the current view.
7. Repeat with synthetic `SYNTH-E05-B`; ensure A disappears; try invalid input and ensure no stale project remains. Reopen/close to verify teardown without accidental persistence.
8. Test explicitly denied/unauthenticated connection where feasible; ensure no research projection returned and no bypass of OAuth.
9. Capture redacted screenshots + `HTTP status`/console error *codes only*; no HAR with tokens and no JWT/Authorization headers.

### Acceptance gates
- `E05-UI-01` panel reliably loads in ChatGPT web, no "Não foi possível exibir" (ALPHA witnessed 2026-10-17, recheck v3).
- `E05-UI-02` all ten screens usable, proper responsive behavior.
- `E05-UI-03` synthetic result arrives and remains visible on resize/context events.
- `E05-UI-04` B replaces A; invalid/new input clears old data; teardown clears.
- `E05-SEC-05` valid/invalid auth isolated, no new resource domains, no arbitrary URLs.
- `E05-SCI-06` seven human gates never auto-approved and Drive synchronization never claimed.
- `E05-OPS-07` original live Plugin and VPS unchanged; deletion of temporary staging credentials is planned.
- `E05-LOG-08` all evidence source-labeled; any unobservable behavior explicitly marked unverified.

If any gate fails, STOP test-only exposure, preserve minimal redacted evidence, and return to a Draft PR. Do not merge, release, widen CSP, or enable multitenancy to force a pass.

## Scope boundary
E05 **does not** validate Google Drive personal connector A/B real-user access or grant scientific approval. The private-account isolation acceptance follows later under separate informed consent and without inspecting personal research documents.
