# Meu Artigo — reviewer packet (DRAFT, source-only)

**Status:** PREPARED; NOT SUBMITTED; NOT APPROVED; NOT PUBLISHED.
**Product:** Meu Artigo — assisted research governance, traceable evidence and seven human scientific gates.
**Architecture:** packaged scientific Skill + one remote, read-only MCP panel `meu_artigo_painel`.
**Official endpoint:** `https://mcp.allflux.com.br/mcp`.
**MCP scope:** `mcp:read`; resource-server Auth0 issuer `https://dev-w6estudk22tzwdil.us.auth0.com/`.
**Private production switch:** `MEU_ARTIGO_MCP_PILOT_SUBS=DENY_ALL` currently prevents *all* real accounts from calling the tool. Do NOT relax it or attempt portal scanning on the premise that public authorization is complete.

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
- [ ] Review account: replace `DENY_ALL` only with exactly approved Auth0 test/reviewer subject(s) in a controlled, rollback-ready change; never open arbitrary subjects just to pass a scan.
- [ ] OAuth client registration: verify exact callback and approved method in portal (`provided`, DCR or CIMD); no secrets in `mcp.json`.
- [ ] OpenAI publisher: identity verification, suitable organization/project, `api.apps.write` permission, domain challenge, current successful MCP tool scan.
- [ ] Four **actually available and accurate** HTTPS pages: product `websiteURL`, support `supportURL`, privacy `privacyPolicyURL`, and terms `termsOfServiceURL`. Do not invent URLs or policy promises.
- [ ] At least one secure reviewer test account, compliant access flow, and a real demo-recording URL; not created or uploaded in this packet.
- [ ] Review cases: the exact five positive and three negative cases above must be run, corrected, and included or entered in the submission; do not imply PASS before real observation.
- [ ] Release notes, final version consistency (source remains `0.9.0-beta.9`), submitted tool annotations/CSP, security evidence and explicit owner's go/no-go for public submission.

## Relevant public guidance

- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/deploy/submission-errors
- https://developers.openai.com/plugins/deploy/app-review
- https://developers.openai.com/plugins/plugin-guidelines

**Current phase boundary:** We can prepare and inspect a non-published candidate ZIP without claiming completion of intervention 3. The first public submission is blocked until the prerequisites above are documented and independently verified. No changes to the private installed beta.8, MCP Piloto, synthetic E05, persistent VPS Auth0 `DENY_ALL`, GitHub `main`, or any individual's Drive are authorized by this packet.
