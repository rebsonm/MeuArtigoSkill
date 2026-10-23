# Meu Artigo: original 18-delivery master plan

**Source-side engineering record — 2026-10-17. Active delivery: 16 of 18.**
This plan is distinct from the **12 planned UI experiences**, the **10
current HTML screens**, and the **21 canonical C.A.D.A. spreadsheet tabs**.
These are separate inventories; never confuse their totals or claim
that passing CI proves live ChatGPT interoperability.

## Corrected product architecture

- Each researcher connects their own Google Drive **in their own ChatGPT account**.
- The Skill maintains the existing source-of-truth research spreadsheets,
  journal, decisions, gates, and files in the user's authorized Drive.
- The current ChatGPT session reads only its user's authorized records,
  checks canonical identity, and prepares a bounded UI-only projection.
- The MCP receives/transforms that specific display payload **per call** and
  returns it to the interactive HTML panel. No Google API credentials,
  source-file reads, persistent research storage, or cross-user cached state
  exist in the MCP implementation.
- Temporary processing is **not zero knowledge**. Only explicitly approved
  minimum display fields may be sent; the MCP does not independently verify
  host identity, scientific validity, or original Drive provenance.
- Gates and consequential scientific decisions remain human-controlled.
  Displaying a recorded approval is not verifying its authenticity.

## Original master delivery matrix

| # | Original delivery | Evidence level / status | Implemented evidence | Remaining verification |
|---|---|---|---|---|
| 01 | Freeze the baseline and record commit SHAs | HISTORICAL | Baselines and candidate SHAs inventoried | Reconcile the final integration SHA |
| 02 | Map features, overlaps, and duplicates | HISTORICAL | Functional absorption matrix for Skill, Drive, and MCP | Review duplicate responsibility in PR #79 |
| 03 | Define unified architecture and contracts | ADAPTED | ChatGPT owns each researcher's Drive; MCP displays transient projections | Approve minimization and security assumptions |
| 04 | Strengthen CI, dependencies, and security | TECHNICAL | Release audit, security contracts, CodeQL, MCP CI | Require checks on the final commit |
| 05 | Reconcile PR #74 into a safe candidate | TECHNICAL | PR #78 combines Drive F1-F9, UI, MCP with safe PR ancestry | Review final cumulative diff |
| 06 | Secure canonical Drive root and folder reuse | SYNTHETIC | Hierarchy, pagination, duplicate and parent guards | Real read-only per-account validation |
| 07 | Harden Drive F1-F4 | SYNTHETIC | Preconditions, folder identity, and root/parent guards | Real provider proof and permissions |
| 08 | Harden Drive F5-F9 | SYNTHETIC | Journaling, CAS, recovery and synthetic failure cases | Provider-backed remote concurrency and receipts |
| 09 | Develop the blue dashboard | SYNTHETIC | Ten HTML screens with four language paths | ChatGPT-hosted interactive rendering |
| 10 | Unify the MCP Apps service | SYNTHETIC | One MCP UI tool; host supplies bounded display snapshot | Connect real HTTPS endpoint and render inside ChatGPT |
| 11 | Implement Auth0 OAuth resource server | OFFLINE | RS256/JWKS, audience, time bounds and scopes | Live Auth0 + ChatGPT PKCE acceptance belongs to step 17 |
| 12 | Integrate PR #65 scientific integrity reviews | SYNTHETIC | REG-018/REG-011 advisories and provenance controls | Independent methodological and semantic assessment |
| 13 | Implement reproducible scientific diagnostics | SYNTHETIC | REG-013/001/019 sidecar controls | External claim-accuracy review |
| 14 | Integrate PR #66 fictional method projection | SYNTHETIC | Method options without automatic scientific choices | Cross-method expert validation |
| 15 | Run horizontal integrated acceptance | SYNTHETIC | Skill, native panel, HTML and MCP regression coverage | Real host/Drive/Plugin end-to-end session |
| 16 | Consolidate and incorporate pull requests | IN_PROGRESS | PR #79 stacked over PR #78; host projection, Skill routing, visual tests and roadmap restored | Independent cumulative diff review, version choice and explicit merge approval |
| 17 | Accept OAuth on Contabo and ChatGPT | PENDING | Hosted domain designated, OAuth only tested offline | Isolated VPS + real OAuth + separate ChatGPT/Drive accounts A/B |
| 18 | Publish a controlled version | PENDING | Release guardrails and beta distribution constraints documented | Gate 16+17, rollback, privacy and human authorization before release |

**Historical naming correction:** A subsequent high-priority CodeQL/GHAS
security corrective effort was informally called "Stage 17". It did
**not complete or replace** the original delivery 17 (real OAuth on the
external host and ChatGPT). Seven GHAS PR #78 alerts (#5–#11) were
reconciled from maintainer-supplied screenshots; that security evidence
remains transversal across all steps, not a production authorization.

## Original 12 UI experiences

These are not deliveries 19–30. Some correspond to more than one screen
or are cross-cutting experiences.

| # | Planned experience | Evidence and remaining work |
|---|---|---|
| 01 | Research dashboard | Overview screen exists; live host rendering unverified |
| 02 | Next action | Registered next action display exists; source readback unverified |
| 03 | Scientific map | Corpus map exists in canonical matrix but is not a dedicated MCP view |
| 04 | C.A.D.A. board | Task screen exists; live authorized spreadsheet extraction unverified |
| 05 | Sources and searches | Screen exists; MCP cannot certify literature retrieval |
| 06 | Evidence [L]/[I]/[P] | Evidence screen exists; original source content stays in Drive |
| 07 | Human gates | Stages and validation views; no automatic scientific approval |
| 08 | Timeline | Traceability screen exists; original event history remains in records |
| 09 | Submission readiness | Submission screen shows unverified state honestly |
| 10 | Synchronization | Synchronization view never claims Drive persistence proof |
| 11 | First-run onboarding | Skill onboarding exists; real host first-run not observed |
| 12 | Mobile and dark mode | Source/visual design exists; real device and theme tests pending |

**Current ten HTML screens:** Overview, Stages, C.A.D.A. Tasks,
Sources/Searches, Evidence, Validations, Methods, Traceability,
Submission and Synchronization. The corpus map, first-run onboarding
and mobile/dark themes are not necessarily separate screens.

## Delivery 16: actual engineering work and hard limits

On PR #79, stacked on PR #78:

1. Removed direct MCP access to Google Drive, tokens, files and local
   projects; the server cannot read another user's Drive.
2. Added `host_projection.mjs`: strict allowlist for task, gate,
   next-action and advisory display fields; limited counts and bytes;
   rejected private source bodies and claims of automatic approval.
3. The MCP Apps bridge renders the current request and clears an
   earlier user's UI state when the tool fails or omits a snapshot.
4. Added actionable Skill instructions in
   `references/mcp-tool-use.md` for reading the **existing canonical**
   C.A.D.A./continuity registers from the researcher's connected
   Drive and creating only a minimum display projection.
5. Added alternate fictional A/B request tests and a browser renderer
   regression covering ten screens and stale-state clearance.
6. Restored this **18-delivery matrix** and the separate **12-experience
   visualization inventory**, with explicit evidence levels.

Remaining for delivery 16: a real reviewer must reconcile PR #78 and
PR #79 cumulative diff, choose one integration strategy, confirm
packaging/version consistency and explicitly approve any merge.
**No merge is implied by passing software tests.**

## Delivery 17: real hosted pilot, NOT EXECUTED

1. Confirm the actual installed Skill/Plugin version and that custom
   MCP tools and the UI are available in the tester's ChatGPT account.
2. With separate authorization, configure a restricted environment
   at `https://mcp.allflux.com.br/mcp` behind HTTPS/Nginx, without
   publicly exposing the Node loopback port.
3. Independently validate Auth0 registration, callback, PKCE, issuer,
   audience, scopes, token expiration, and logout.
4. Have volunteer A use **only A's own Google Drive** in ChatGPT and
   volunteer B use **only B's own Drive** in a separate account.
   Both hosts may call the same shared MCP but must send only their
   own selected display fields.
5. Exercise project changes, denied access, revoked connection,
   missing files, no-approval flags, no data persistence and
   dashboard stale-state clearing.
6. Observe ten real screens, four languages, responsive experience,
   first-run workflow and report a truthful GO/NO-GO verdict with
   redacted logs and user-approved test evidence.

Real Google Drive/ChatGPT isolation is a host-level property and
cannot be certified by the MCP's mock A/B tests alone.

## Delivery 18: controlled publication, NOT EXECUTED

Only after independent acceptance of deliveries 16 and 17, privacy and
security review, compatible installed versions, rollback procedures,
human scientific review, and explicit authorization to merge, release
and update the distributable Plugin.

## Mandatory progress reporting in every future conversation

Always show **delivery N/18, goal, completed work, remaining work,
current PR/HEAD, checks at the same SHA, requested authorizations,
and next justified action**. Keep visualization status separate
by **code / synthetic test / real host / human evaluation**.
Do not introduce additional numbered micro-stages for ordinary
bug fixes or isolated checks.

## Evidence links

- https://github.com/rebsonm/MeuArtigoSkill/pull/78
- https://github.com/rebsonm/MeuArtigoSkill/pull/79
- https://github.com/rebsonm/MeuArtigoSkill/blob/feature/mcp-multiuser-readonly-isolation/references/mcp-tool-use.md
- https://github.com/rebsonm/MeuArtigoSkill/blob/feature/mcp-multiuser-readonly-isolation/integrations/mcp-apps/README.md
- https://github.com/rebsonm/MeuArtigoSkill/blob/feature/mcp-multiuser-readonly-isolation/docs/MATRIZ-CADA.md
