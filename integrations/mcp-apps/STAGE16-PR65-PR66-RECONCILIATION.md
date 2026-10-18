# Stage 16 — scientific controls and legacy preview reconciliation

Status: review candidate only. This memo does **not** authorize merges,
releases, external deployment, tenant changes, or real project data access.

## Immutable sources reviewed

- Integration parent: Draft PR #85, SHA
  `6abc5052539e531a421015d385b6d58d16ad929d`.
- Scientific sidecar ancestor: Draft PR #65, SHA
  `0d3995ce096a32b222c57ba7fc53f31b2962e09f` (diverged).
- Experimental preview: Draft PR #66, SHA
  `62b79707c2aa1435fd7ed751084f8d920721776e` (diverged).
- PR #85 is 234 commits ahead of main (0 behind), modifying 145 files
  at the review time. The diff is not independently reviewed in full.

## PR #65: disposition by invariant, not by filename

PR #65 adds or modifies scientific sidecar scenarios and documentation.
On the original #85 tree, 15 files from its HEAD were absent; after #86 and this branch, the remaining absent paths are **12/40** (eight historical documents, one older CI workflow, the old 12-case runner and test, and the original unified-panel test). other
shared implementation files were not byte-identical. This does **not**
mean that all fifteen scientific controls are missing, and likewise
overlapping current tests do not certify semantic equivalence.

| Scientific control or old artifact | Existing integration state | Resolution in this Draft |
| --- | --- | --- |
| `tests/test_report_output_guard.py` | Report writers remain behind `write_report` with stricter content checks; previous broad cross-writer symlink/canonical overwrite matrix absent | **Port original eight tests verbatim** and execute in current release-audit Python suite |
| `tests/test_semantic_holdout.py` | Frozen 24-case dataset and its evaluator are already present, but old three-test integrity harness absent | **Port original three tests verbatim** and execute against unchanged frozen evaluator and current ledger/export |
| `tests/test_advisory_strict_policy.py` | Existing tests cover advisory-only heuristics, rejected fabricated passages, nonauthenticated reviewers, failed human gates, and source freshness; old eight-case integrated CLI policy matrix absent | **RESTORED WITH PRIVACY ADAPTATION** in the final-candidate branch: eight original strict policy scenarios plus one stdout privacy test; detailed claims are inspected only in-process while the CLI remains sanitized. CI must pass at frozen HEAD |
| `scripts/run_critical_cases.py`, `tests/test_executed_critical_cases.py`, `docs/EXECUTED-CRITICAL-CASES.md` | Existing synthetic tests exercise individual security and scientific boundaries, but do not execute the exact PR #65 12-case catalog | **DEFERRED / NOT INCORPORATED** pending explicit audit of adapter compatibility. Not claimed as a validated scientific benchmark |
| Other PR #65 REG sidecar documents | Current repo retains REG-011/013/018 source and tests, but old experiment-specific narrative/evidence is not in the candidate | Archive historical evidence on PR #65; list any required user-facing guarantees separately before closure |
| `tests/test_unified_researcher_panel.py` | The native research panel now exposes `scientific_diagnostic` through a separate bounded `MEU_ARTIGO_SCIENTIFIC_ADVISORY_PANEL_V1` projection. Old `evidence.diagnostic` nested interface is no longer the current API | **INTENTIONAL CONTRACT CHANGE, NOT BYTE-EQUIVALENT.** Keep new projection and existing `test_stage13_diagnostic_replay` / `test_scientific_diagnostic` tests; independent UI parity still needed |

### Safety rules for restored test coverage

1. Old test imports target current `scripts/` implementations, not
   the PR #65 source. Do not revert currently stricter private-payload
   screening or change production code to make obsolete tests pass.
2. All fixtures are local and fictional; protected canonical files must
   retain exact original bytes. Report files can only be created under
   `98_Technical_Reports`, never overwritten or redirected via symlinks.
3. A frozen synthetic holdout cannot be described as independent human
   ground truth, real scholarly validation, or live provider results.
4. If restored tests fail under current contracts, preserve the failing
   evidence and decide separately whether the observed difference is
   a regression or a deliberate hardening. No test weakening by default.
5. A CI pass certifies only the tested software behavior; scientific
   gates still need an authorized human decision.

## PR #66: explicit retirement of prototype transport

Old PR #66 shipped `mcp-preview/server.mjs` and
`mcp-preview/widget.html`, a **fictional-only, unauthenticated**
local prototype, plus `scripts/mcp_preview_projection.py` and its tests.
It exposed `meu_artigo_preview` with
`ui://meu-artigo/research-map.html` and an interactive map of five
methodological dimensions. It did not offer production OAuth, authorizing
a researcher, connected Drive files, or a server ready for public use.
Its widget used direct `postMessage` protocol handling with wildcard
target rather than the current bundled official `App` bridge.

The newer `integrations/mcp-apps/` service has a **different** contract:
`meu_artigo_painel`, `ui://meu-artigo/site-v3.html`, bounded
`MEU_ARTIGO_SITE_V1` projections, per-call no-storage semantics,
explicit CSP domain lists, single-user Auth0 pilot / restricted E05
synthetic staging, and ten-screen visual acceptance in ChatGPT.

**Decision proposed (reviewer approval required):**
- **Do not cherry-pick or merge** the old `mcp-preview/` server,
  widget, or old `mcp_preview_projection.py`; that would create an
  unreviewed second tool/transport and bypass the contemporary E05 gate.
- Reuse the already shared methodological support scripts
  (`method_routes`, `adaptive_method_guide`, method decision/fill
  preflight), not the abandoned prototype's transport.
- Treat the old standalone five-dimension interactive selector as a
  distinct, non-mandatory feature: there is *no verified pixel/interaction
  parity* against the current ten-screen panel. Track its user utility
  separately and do not claim full replacement equivalence.
- Only the current method-selection contracts and the seven original
  human science gates may authorize scientific state. The UI never
  silently records or approves a user's method.

## Release decision

| Gate | Result from this review |
| --- | --- |
| Original broad report-writer adversarial suite | RESTORED — verify CI at final SHA |
| Frozen 24-case synthetic holdout integrity suite | RESTORED — verify CI at final SHA |
| Old strict-policy eight-case CLI integration | RESTORED WITH PRIVACY ADAPTATION; independent CI PASS required |
| Old 12-case synthetic catalog | NOT INCORPORATED; separate optional analysis |
| Legacy unauthenticated preview transport | RETIREMENT PROPOSED; no merge |
| Exact legacy interactive methodological selector parity | UNVERIFIED |
| Seven independent human scientific decisions | Still mandatory |
| Real researcher A/B Drive and OAuth | Not validated by this reconciliation |
| Effective public ChatGPT CSP | Not validated by offline test |
| GO_MERGE / GO_RELEASE / GO_PUBLIC | NO-GO pending authorizations and remaining gates |

This is a **targeted reconciliation** of PR #65 and #66, not a
line-by-line attestation for the entire cumulative integration diff.
Never close those original PRs solely from this memo without explicit
maintainer review and an independently frozen CI result.

## Final-candidate follow-up (2026-10-18)

- Restored `tests/test_advisory_strict_policy.py` preserving the original eight
  scientific decision scenarios, with one additional safe-output regression.
  The current diagnostic CLI deliberately redacts detailed results from
  terminal output; strict verdicts are checked using `compose(...)` in process.
  The expected error for a rejected cross-reference remains generic in the
  diagnostic CLI rather than printing the canonical ledger details.
- PR #65 files absent from the current branch (12/40 changed-file paths):
  `.github/workflows/critical-cases-registry.yml`, seven historical documents
  covering REG and experiments, `scripts/run_critical_cases.py`,
  `tests/test_executed_critical_cases.py`, and
  `tests/test_unified_researcher_panel.py`.
  Historical documents remain available in the original Draft PR. The old
  executed critical-case runner remains a distinct, unmerged optional suite;
  the current native panel contract differs from the old nested diagnostic.
- PR #66 still has eight absent preview-only paths; this retirement is
  intentional but requires a review decision before the old PR can be closed.
- For PRs #74 and #75, **all** changed-file paths survive in the final
  candidate, but 20 and 11 files respectively were modified afterward.
  Presence is not byte-level or security equivalence; independently review
  those follow-up changes against the older branch.
