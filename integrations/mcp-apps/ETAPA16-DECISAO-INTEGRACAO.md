# Delivery 16 / 18 — Integration decision dossier (NO MERGE)

**Status:** engineering integration review in progress, derived from
PR #78 -> PR #79. This dossier is a **source/CI-supported review record**,
not final line-by-line approval, not a merge authorization.

## Immutable review bases

- Main: `5c7bf4ff599d73a660bb709616a689140b2edbe7`.
- PR #78: `cd1f1d3f92132676544f4183eef6988dec5f74e5`,
  Draft/open, 122 changed files, based on main.
- PR #79: stacked on #78, Draft/open, **22 changed files**, with
  **15 overlapping paths** and seven additional paths not in #78.
  **129 distinct touched paths across the two PRs**.
  The PR #79 branch is the candidate containing both change sets.
- PR #76: security repair already merged into main.
- PR #77: separate Draft. Its security/lockfile contracts were absorbed
  in #78; merging #77 independently alongside the candidate can duplicate
  changes.
- PR #74: Drive F1-F9 / UI basis, selectively incorporated in #78.
- PR #75: Auth0 OAuth prototype, selectively incorporated in #78; Google
  Drive delegated OAuth is **not** part of the current MCP architecture.
- PR #65: scientific evidence/diagnostic sidecars integrated through
  #78 with safety constraints.
- PR #66: methodological candidate exploration integrated through #78,
  preserving human decisions.

## Architecture after the review

**Per-user source of truth:** All article research records, journals,
C.A.D.A. registers, human gates and actual evidence remain in each
researcher's own Google Drive connected privately to their ChatGPT
account, never an operator-owned shared Drive.

**Skill orchestration:** The Skill reads authorized existing canonical
records through the host connector, reconciles their provenance and
returns *minimum display fields* to the MCP only when the user asks
for a dashboard and the tool is genuinely available.

**MCP transport/UI:** The server receives a schema-checked, per-call
display projection. It **processes temporary research-derived fields**;
it does not read the Drive API, receive Google tokens, use a global
project root, store project files, or persist dashboard snapshots.
A/B test passes do **not** independently validate Google account
isolation in the real host.

**Research integrity:** Seven human gates, DEC/TRACE, C.A.D.A.,
REG scientific caveats and Drive F1-F9 retain original safeguards.
The UI may display recorded values but cannot prove scientific
truth, user identity, or Google sync by itself.

## Specific changes made by this Stage 16 hardening

1. Reject common embedded Google Drive URLs, email addresses, token
   formats, secrets and absolute user file paths even inside otherwise
   allowed display fields. The text scanner is only a partial defense:
   **it cannot establish that arbitrary submitted prose is not private**.
2. Refuse duplicate tasks and duplicate/wrong-range scientific gate IDs
   to prevent inflated recorded-approval totals.
3. Unknown gate totals produce a **partial/unknown** display, not a
   false claim that all unobserved gates are unapproved.
4. Clear the visualized snapshot on host context changes as well as
   explicit failed/no-data tool calls. This is a client-side guard;
   it cannot guarantee isolation of arbitrary external chat sessions.
5. Add adversarial synthetic tests for the above controls, re-run
   release audit, supply-chain, MCP and CodeQL on the exact final HEAD.

## Decision matrix

| Area | Supported now | Current decision | Follow-up |
|---|---|---|---|
| Software CI | Synthetic/on-commit tests | Can be conditionally GO after all checks succeed | Record exact HEAD + results |
| 18-delivery project plan | Versioned source record | GO for continued tracking | Keep 16 active; 17/18 pending |
| 10-screen UI | Synthetic browser rendering | GO for isolated testing, NO-GO for live claim | Actual ChatGPT MCP Apps render |
| Canonical Drive model | Existing files + F1-F9 tests | NO-GO for live remote write claims | Per-user host connector and CAS receipts |
| Multiuser data isolation | No MCP storage; A/B synthetic fixtures | NO-GO for live proof | Two independent users and Drive accounts |
| Auth0/PKCE | Signed tokens with offline JWKS | NO-GO for production deployment | Authorize and complete real OAuth flow |
| Security privacy of dashboard | Allowlist, no server cache, text filter | GO for bounded synthetic usage only | Privacy review, logging/redaction, penetration tests |
| Scientific outcomes | Human gates and sidecars preserved | NO-GO for claims of real validity | Expert/human validation |
| PR merge | 129 distinct touched paths across stack | **NO-GO pending human diff review and explicit permission** | Choose one integration strategy |
| Controlled release | Not deployed or installed | **NO-GO** | Finish deliveries 16 and 17 |

## Recommended integration order — ONE candidate, not parallel merges

A. Review **both** the cumulative PR #78 diff against main and
the delta PR #79 diff against PR #78. Do not review only PR #79's
22-file view and assume the full stack is covered.
B. Reconcile security-sensitive changes: Google Drive identity,
F1-F9 journal/CAS, safe report output, Auth0 validation, per-call
MCP projection, HTML escaping, UI lifecycle and package boundary.
C. Confirm unchanged main and exact candidate HEAD, all required
checks green, zero unexpected high alerts and documented synthetic
fixture exceptions. Obtain actual independent human review.
D. Choose a **single** reviewed integration path after authorization:
   consolidate #78 + #79 into one merge candidate targeting main
   (by retargeting only with express approval, or via an approved
   equivalent controlled integration). Avoid individually merging
   #74/#75/#65/#66/#77/#78/#79 as a chain when the review candidate
   already includes their selected effects.
E. After a separate explicit merge approval, test the resulting main
commit and retain the ability to revert the integrated change cleanly.
   Treat rollback of actual Google data or OAuth grants as separate
   security workflows, not automatic results of a git revert.

## Remaining original deliveries

- 01 Baseline and SHA freeze: technically tested or historically inventoried (with external limits)
- 02 Feature and overlap inventory: technically tested or historically inventoried (with external limits)
- 03 Unified architecture and contracts: technically tested or historically inventoried (with external limits)
- 04 CI / dependency / security: technically tested or historically inventoried (with external limits)
- 05 Safe PR #74 reconciliation: technically tested or historically inventoried (with external limits)
- 06 Canonical Drive root: technically tested or historically inventoried (with external limits)
- 07 Drive F1-F4: technically tested or historically inventoried (with external limits)
- 08 Drive F5-F9: technically tested or historically inventoried (with external limits)
- 09 Blue dashboard and ten screens: technically tested or historically inventoried (with external limits)
- 10 Single MCP Apps: technically tested or historically inventoried (with external limits)
- 11 OAuth resource server offline: technically tested or historically inventoried (with external limits)
- 12 Evidence integrity from #65: technically tested or historically inventoried (with external limits)
- 13 Reproducible diagnostics: technically tested or historically inventoried (with external limits)
- 14 Method exploration from #66: technically tested or historically inventoried (with external limits)
- 15 Horizontal acceptance: technically tested or historically inventoried (with external limits)
- 16 PR consolidation and integration: IN PROGRESS / human review outstanding
- 17 Live Contabo + ChatGPT OAuth acceptance: NOT EXECUTED
- 18 Controlled release: NOT EXECUTED

## Prohibited without separate permission

No merge, PR closure, release, VPS deployment, Nginx proxy, Auth0 or
Google Cloud changes, Plugin installation/update, real Google Drive
writes, or access to third-party research accounts.

Evidence belongs in the current PR checks and descriptions. If this
document changes the HEAD, check statuses must be revalidated for
the resulting final commit.
