# Meu Artigo — executable project progress and acceptance matrix

Updated: 2026-10-18. Scope: [Draft PR #89](https://github.com/rebsonm/MeuArtigoSkill/pull/89) versus unchanged main.
This document is the **single source of truth for progress reporting**, and intentionally distinguishes source development from deployment and real-world acceptance.
It does not grant merge, deployment, OAuth, Drive access or publication approval.

## Current deliverables

| Deliverable | State | Evidence / decision |
| --- | --- | --- |
| D01–D15: baseline implementation and source engineering | IMPLEMENTED IN CANDIDATE (not released) | Changes exist in stacked PR #89; independent aggregate acceptance still required |
| D16: integration into main | OPEN | Draft PR #89 not merged; explicit SHA-specific maintainer decision and R01–R02 gate needed |
| D17: real ChatGPT, Auth0, Drive and research workflow | OPEN | No full real-user end-to-end acceptance |
| D18: private Plugin pilot and public directory | OPEN | Separate distribution and publication authorizations needed |

**Source-only acceptance**: GitHub Actions 7/7 SUCCESS on source SHA `92a742dda8ca78bbdaa1259884d8049e5013e782` (seven workflow artifacts available in PR). This is NOT user-facing proof of working E05/production deployment. Last published Skill beta.6; candidate source beta.9; installed private Plugin metadata beta.8 with embedded beta.6. These are distinct artifacts, do not silently update or conflate them.

## Ten stable go-live milestones — no resetting when a test passes

| Gate | Concrete end result | State | Verified advance | Unresolved closing evidence / owner |
| --- | --- | --- | --- | --- |
| R01 | Independent security and cumulative code/science boundary review | PARTIAL | Author-side tranche 1 and tranche 2 corrections, regression tests, 7/7 CI | **Independent** reviewer approval on exact final SHA; no author review may masquerade as independent |
| R02 | Real ChatGPT E05 ALPHA→BRAVO: ten screens, focus, locale, teardown, CSP | BLOCKED — CONNECTOR SESSION | Historical 2026-10-17 screenshot confirms ALPHA inline; BRAVO tool accepted in prior session; E04 Chromium synthetic CI green | 2026-10-18 **both** E05 test Plugin calls returned `McpServerError: Session terminated`. No live view rendered today. Investigate isolated test connection state, then consented real acceptance and effective CSP. Do not alter the main pilot or production to work around it |
| R03 | Authorized one-PR integration into main | WAITING FOR AUTHORIZATION | #89 has clean single branch, do not merge #87/#88 separately | Human SHA-specific merge approval and merge commit after R01/R02 |
| R04 | Post-merge CI, package hash and reproducibility | DEPENDS ON R03 | Source-only 7/7 at pre-merge SHA | CI on merged main SHA and verification of SHA256 |
| R05 | Reviewed production HTTPS Auth0-enabled endpoint, logs and rollback | DEPENDS ON R04 | Loopback health/ready and HTTP limits source-tested | Authorized infrastructure work, TLS/proxy checks and rollback proof |
| R06 | Real ChatGPT Auth0 OAuth/PKCE with two accounts, denial and revocation | DEPENDS ON R05 | Synthetic JWT, issuer, scopes, bearer and origin tests | Two consented real accounts plus redacted A/B evidence |
| R07 | Independent Drive A/B canonical F1–F9 and CAS/readback | DEPENDS ON R06 | Offline simulated journal/trust-gate controls | Real individual Drive permissions and consented cross-account checks |
| R08 | Researcher create/resume article, tasks, seven human gates and recovery | DEPENDS ON R07 | Scientific source contracts and synthetic UI only | Real end-to-end project acceptance with human sign-offs |
| R09 | Private ChatGPT Plugin delivery, installation and pilot | DEPENDS ON R08 | Candidate packaging/test guards | Explicit permission to update/install production private Plugin and limited pilot evidence |
| R10 | Public With MCP directory review, listing and external researcher verification | DEPENDS ON R09 | No public distribution evidence | Explicit separate authorization, review/approval, public listing and external installation |

**Remaining acceptance gates: 10** (R01–R10), comprising **three still-open original deliveries D16–D18**. Closed *go-live* gates: 0/10. Source progress is real, but it must not inflate the gate closure count.

## Actual E05 investigation on 2026-10-18

- Called connected `Meu Artigo — E05 Teste Sintético` exactly with approved fixed fake ALPHA fixture (one task, no real data, seven unapproved scientific gates): `INVALID_ARGUMENT ... McpServerError: Session terminated`.
- Repeated independently with approved fixed fake BRAVO fixture: same result. No project data, credentials, file IDs or personal information submitted.
- Called separate pre-existing private `Meu Artigo — MCP Piloto` in guidance-only/minimal mode: connector returned an error wrapping the neutral MCP guidance message. This is *not* a health-check or proof of production availability. It is a distinct plugin and must not be swapped into the E05 test.
- **Interpretation:** live E05 acceptance is blocked at connector session/connectivity; this result alone neither proves a software regression nor identifies a root cause. No E05 screenshots, CSP enforcement or ten-screen result were obtained today.
- **Actionable investigation order:** inspect isolated E05 test connection status/refresh in ChatGPT; independently confirm authorized test tunnel and its /readyz endpoint without exposing credentials; inspect sanitized service/process logs; restore only the isolated E05 test connection after explicit authorization; rerun ALPHA/BRAVO, ten-screen, locale, resizing, focus, teardown and CSP. Do not turn off authentication or relax CSP to make tests pass.

## Method of recording progress from now on

1. Keep stable gate IDs; never create a new acceptance milestone to replace one left open.
2. A source commit/test improvement changes **Verified advance**, NOT gate state to DONE.
3. Close a gate only after its stated external evidence is available; link it, state observer and SHA.
4. On each continuation, report delta: files/commits changed, checks on latest head, which gate advanced/closed, new blocker and exact next operation.
5. Stop repetitive hardening when source CI is green, unless a specific reproducible defect is found. Prioritize E05 restoration and owner review toward real-user release.
6. Every status claim must distinguish **observed**, **inferred** and **not verified**.

## Active decision

- GO_SOURCE_CI: PASS on `92a742dda8ca78bbdaa1259884d8049e5013e782` only; if this matrix commit becomes new head, check its own CI before claiming current HEAD passed.
- GO_REAL_E05: BLOCKED (`Session terminated`); GO_INDEPENDENT_REVIEW: NOT COMPLETE.
- GO_MERGE / GO_DEPLOY / GO_PRIVATE_PLUGIN / GO_PUBLIC: NO-GO.
