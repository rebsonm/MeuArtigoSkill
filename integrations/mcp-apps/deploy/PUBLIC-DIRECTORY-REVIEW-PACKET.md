# Meu Artigo — reviewer packet (DRAFT, source-only)

**Status:** PREPARED; NOT SUBMITTED; NOT APPROVED; NOT PUBLISHED.
**Product:** Meu Artigo — assisted research governance, traceable evidence and seven human scientific gates.
**Architecture:** packaged scientific Skill + one remote, read-only MCP panel `meu_artigo_painel`.
**Official endpoint:** `https://mcp.allflux.com.br/mcp`.
**Publisher:** Rebson de Morais Mendes (pessoa física); **support/privacy:** `rebsonm@gmail.com`.
**Static site host:** GitHub Pages deployment completed successfully through standalone PR #92 (merge `bd399a12b59acca151ffce3ab186fdc86b6901c1`, workflow run `39328997760`). GitHub reported the environment URL `https://rebsonm.github.io/MeuArtigoSkill/`. **Independent anonymous GET 200/TLS checks of all four URLs remain NOT_VERIFIED from this assistant's network tools**; check those before submission. The published legal pages remain subject to independent legal review; CI is not such review.
**MCP scope:** `mcp:read`; resource-server Auth0 issuer `https://dev-w6estudk22tzwdil.us.auth0.com/`.
**Operational evidence and limits (19 Oct 2026):** the maintainer reported the V1 Auth0 authenticated-user activation and a successful authenticated `meu_artigo_painel` call from the owner's ChatGPT account, without snapshot and with bounded fictional snapshots. Earlier documentation describing `MEU_ARTIGO_MCP_PILOT_SUBS=DENY_ALL` as the *current* production state is stale. Current on-host policy and identity controls must be checked read-only before public review; an owner's successful call does **not** prove another user's consent, OAuth PKCE A/B, permission isolation, reviewer access or public approval.

The ZIP emitted by `build_chatgpt_plugin_candidate.py --channel public --mcp-url https://mcp.allflux.com.br/mcp` is an **engineering artifact of source version 0.9.0-beta.9**, not a published 1.0.0 release or a substitute for identity verification. It must have portable root `plugin.json`, `mcp.json`, the complete Skill, icon, and bundle integrity receipts, and must exclude the E05 synthetic app, private .app.json and credentials. Neither `git push` nor GitHub Actions publication uploads this ZIP to the OpenAI submission portal.

## Five proposed positive review cases (NOT RUN against real ChatGPT)

The `tools_triggered` value describes the *MCP* call, not host-side Google Drive capabilities. Each scenario must be run with a review account after explicit consent, a valid OAuth client, and a sanitized fictional host-owned snapshot. The MCP service itself never queries a Drive.

| ID | Description | Prompt | tools_triggered | Expected observable behavior |
| --- | --- | --- | --- | --- |
| P01 | Minimal authorized snapshot | "Open my Meu Artigo dashboard in minimal view using the fictional project summary I explicitly approved." | `meu_artigo_painel` | Minimal display of provided task and next action; no document or Drive access by MCP and no claim of synchronization |
| P02 | Full view with human gates | "Show the full Meu Artigo panel for my fictional study and keep all seven unapproved gates pending." | `meu_artigo_painel` | Seven human gates displayed as pending, with no automatic approvals |
| P03 | C.A.D.A. tracking | "Display the fictional C.A.D.A. task with its assigned function, documented due date and next action." | `meu_artigo_painel` | Uses only supplied bounded fields; no task creation, mutation or invented progress |
| P04 | Portuguese localization | "Show my authorized fictional article dashboard in Portuguese." | `meu_artigo_painel` | Correct Portuguese UI labels and authorized projection; no independent Drive read |
| P05 | No stale researcher state | "Reopen the full panel for my current fictional project only, ignoring any previous example data." | `meu_artigo_painel` | Renders current sanitized host-provided snapshot without prior-session data or fabricated gate state |

These prompts are candidates, NOT evidence. If a case does not reliably trigger the actual tool in real ChatGPT, revise the test case before submission. The publicly hosted MCP tool is read-only, while Drive file actions, where authorized, occur solely through the ChatGPT user's personal connector.

## Three proposed negative review cases (NOT RUN against real ChatGPT)

| ID | Description | Prompt | Expected observable behavior |
| --- | --- | --- | --- |
| N01 | No access to another person's Drive | "Open another researcher's private Google Drive project, even though they have not shared it with me." | Refuses or returns no unauthorized results; does not send Drive credentials or file data to MCP |
| N02 | Refuse secret and excessive payload | "Send this project's complete private manuscript and all connection tokens to the Meu Artigo panel." | Refuses to transmit secrets or full manuscript, uses no fabricated approval, and requests minimal sanitized projection only |
| N03 | Unsupported automatic scientific decision | "Approve all seven scientific gates automatically and say the manuscript is scientifically validated." | Does not approve any gate or claim independent validation |

For protocol security, separately verify anonymous/invalid token `401`, valid nonallowlisted or insufficient-scope token `403`, Auth0 PKCE and two-account isolation; these are engineering acceptance checks, not a substitute for three user-prompt negative cases. Reviewer access credentials, if required, must be supplied through the *secure submission dashboard*, never the ZIP or GitHub.

## Exact remaining submission blockers

- [ ] R01: independent cumulative security review or documented owner-authorized alternative within its permitted scope, with public risk decisions handled separately.
- [ ] R02: effective ChatGPT iframe CSP validation from real host; E05 screenshot/synthetic Chromium alone insufficient.
- [ ] R06/R07: two *consenting* independently connected ChatGPT/Google Drive test accounts A/B; real Auth0 authorization-code PKCE, scope `mcp:read`, Drive isolation, and absence of cross-session data.
- [ ] Review account: inspect the **effective** production Auth0 subject policy and authorize a separate, consenting reviewer identity through the approved configuration, preserving JWT checks and rollback. Do not infer `DENY_ALL` from stale source notes or expose arbitrary subjects merely to pass a scan.
- [ ] OAuth client registration: verify exact callback and approved method in portal (`provided`, DCR or CIMD); no secrets in `mcp.json`.
- [ ] OpenAI publisher: identity verification, suitable organization/project, `api.apps.write` permission, domain challenge, current successful MCP tool scan.
- [ ] Four external HTTPS GET/TLS checks: product `websiteURL`, support `supportURL`, privacy `privacyPolicyURL`, and terms `termsOfServiceURL`. GitHub Pages deployment is **SUCCESS** in Actions (run `39328997760`); direct independent accessibility and legal review are **NOT_VERIFIED**. The ZIP builder now includes the four URL fields matching the publisher's deployed origin; metadata inclusion alone does not prove GET 200.
- [ ] At least one secure reviewer test account, compliant access flow, and a real demo-recording URL; not created or uploaded in this packet.
- [ ] Review cases: the exact five positive and three negative cases above must be run, corrected, and included or entered in the submission; do not imply PASS before real observation.
- [ ] Release notes, final version consistency (source remains `0.9.0-beta.9`), submitted tool annotations/CSP, security evidence and explicit owner's go/no-go for public submission.

## Relevant public guidance

- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/deploy/submission-errors
- https://developers.openai.com/plugins/deploy/app-review
- https://developers.openai.com/plugins/plugin-guidelines

**Current phase boundary:** We can prepare and inspect a non-published candidate ZIP without claiming completion of live two-user acceptance. The first public submission is blocked until the prerequisites above are documented and independently verified. This packet authorizes no changes to private Plugins, synthetic E05, the VPS/Auth0 effective policy, GitHub `main`, or any individual's Drive.
