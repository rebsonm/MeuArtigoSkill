# Stage 16 — single integration candidate / release decision register

This is a **consolidated review entry**, NOT merge approval, scientific
independent review, a release, or production deployment.

## Frozen ancestry and review surface

- Base: `main` SHA `5c7bf4ff599d73a660bb709616a689140b2edbe7`
  (recheck before integration).
- Stacked source sequence: PR #78 → #79 → #80 → #81 → #82 → #84 →
  #85 → #86 → this review branch. Each upstream PR remains Draft.
- The eight stacked PRs are not independent features that must all be
  merged separately. Git ancestry already carries them into this branch.
  If a single-PR integration is authorized, review the **full
  accumulated diff against main** in the consolidated Draft rather
  than merging every ancestor and then merging a duplicate.
- Last fully tested parent: PR #86 SHA
  `6c790e0a5a3d9a3bc190c3c8fbf07f0b3d781f09`, all six GitHub
  Actions checks passed. This consolidated branch has additional
  advisory-policy tests and docs and requires **fresh CI** at its own
  definitive SHA.

## Evidence inventory

| Subsystem | Present source/verification | Remaining gap |
| --- | --- | --- |
| Standalone Skill | Release audit and pinned packaging tests | Choose a version consistent with installed Plugin metadata, evaluate final bundle |
| Drive F1–F9 | Automated isolation/permissions/journal regression; cumulative changes carried by #78/#79 | Two independent authorized **real** accounts, remote readback and actual permissions, no live authorization here |
| Auth0/OAuth | Local/JWT/HTTP/PKCE simulated tests and security checks | Live configured audience/scopes, denied users, token boundaries and real ChatGPT sign-in |
| MCP Apps/UI | E04 reference Chromium, resource contract, E05 live ALPHA and BRAVO synthetic tool calls | Real host CSP enforcement, live private production service, independent full browser traces |
| Hover/layout | PR #82 fixes; human E05 visual confirmation of no tremor | Cross-device host regression; screenshot is not browser instrumentation |
| CSP | PR #85 offline fail-closed resource/allowlist test | Host screenshot shows `CSP desativada`; effective policy and unique public widget origin unverified |
| Scientific gates | Seven gate display/approval invariants preserved in candidate tests | Each real decision still explicitly human, no independent scientific validation |
| Scientific output files | 8 original PR #65 canonical-write/symlink adversarial tests carried by #86 | Real writable authorized project workflow cannot be inferred from synthetic filesystem |
| Scientific holdout | 3 restored tests, 24 fictional held-out examples | Not human-labelled ground truth, no semantic accuracy claim |
| Strict advisory policy | 8 original scientific assertions adapted to current privacy-safe diagnostic console + one privacy regression | Confirm new test suite via GitHub release audit; no automatic scientific approval |
| Old 12-case catalogue | Existing smaller feature-level regressions | Exact original PR #65 runner/test not brought forward; optional separately reviewed experiment |
| Old MCP preview | Current 10-screen authenticated architecture supersedes the historical unauthenticated transport | No proven pixel/function parity of original 5-dimensional interactive methodology selector |
| Plugin distribution | Private/public deterministic ZIP builder and manifest enforcement | Production MCP registered app ID, reconciled metadata version, reviewer approval, real install |
| Public listing | Source prep only | Verified HTTPS endpoint, CSP/origin, privacy policy, identity, OpenAI review and publication |

## Older PR reconciliation

- #68, #69, #77: ancestors of the integration tree. Never merge again.
- #74: divergent PR; its 58 changed-file paths exist in the new tree,
  38 unchanged blobs and 20 with later revisions. Compare those
  sensitive Drive and MCP changes before formally resolving #74.
- #75: divergent PR; all 12 paths exist, one byte-identical and 11
  later revised. Review Auth0, HTTP metadata and supply-chain boundaries
  rather than cherry-picking an obsolete OAuth implementation.
- #65: out of 40 files touched at that PR head, the final branch has
  12 paths still absent (eight historical docs, one workflow, two
  twelve-case runner/test files, one old unified research panel test).
  The 8-case policy suite is ported with sanitization preserved;
  historical experimentation not silently considered reproduced.
- #66: eight legacy preview-only paths remain intentionally absent;
  no second anonymous MCP service is introduced.
- All original PRs remain open until the maintainer explicitly
  approves reconciliation/closure; no review status is invented.

## Explicit decision ladder

1. **SOURCE_INTEGRITY**: CI for the final consolidated SHA must show
   release audit, MCP Apps, security contracts, Chromium, CodeQL Python,
   CodeQL JS/TS all completed successfully. Document exact SHA.
2. **SCIENTIFIC_BOUNDARY**: A second reviewer inspects protected gates,
   mutable project files, report-writer confinement, advisory-only
   classification and missing alternate scientific experiments.
3. **INTEGRATION_SECURITY**: A second reviewer inspects cumulative Drive
   F1–F9, Auth0/OAuth, origin, hostname, credential handling, logs,
   idempotency, 403/404 behavior, CSP and multitenancy.
4. **VERSION_DECISION**: Main source VERSION currently
   `0.9.0-beta.6`; maintainer's Plugin metadata observed previously
   at `0.9.0-beta.8` with inner source beta.6. This mismatch cannot
   be fixed by downgrading or relabeling the installed Plugin blindly.
5. **MERGE_APPROVAL**: Obtain explicit authorization naming the
   consolidated PR and its reviewed final SHA. Do not mark ancestor
   PRs merged by GitHub unless they were actually merged.
6. **PRIVATE_GO_LIVE**: Deploy reviewed non-synthetic production MCP
   in controlled infrastructure after separate approval, validate
   real OAuth, two isolated ChatGPT/Drive users and rollback.
7. **PUBLIC_SUBMISSION**: Verify CSP/widget origin, policy and identity,
   submit using the official With MCP route, pass OpenAI review,
   then verify actual installation by an external researcher.

## No-go summary

| Operation | Decision before independent review |
| --- | --- |
| Build ZIP locally in CI | Allowed synthetic audit |
| Merge to main | NO-GO |
| Close earlier overlapping PRs | NO-GO |
| Deploy current draft to live VPS | NO-GO |
| Modify registered Plugin | NO-GO |
| Access or migrate real user Drive data | NO-GO |
| Publish to directory | NO-GO |

The programmatic diff inventory and six green CI checks are not a
standalone vulnerability assessment nor a substitute for human approval.
