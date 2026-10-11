# Post-beta.2 homologation baseline — diagnostic before code changes

**Date:** 2026-10-11  
**Status:** Phase 1/5, pre-fix evidence inventory. Not a scientific validation or software acceptance.  
**Source baseline:** `main` at `d180ea28dd9f856c4e96b86b2e6a0011a6797aa4`.  
**Source version:** `VERSION = 0.9.0-beta.2`; `SKILL.md` inspected on this commit.  
**Historical published beta.2 assets:** immutable and outside the modification scope.

## Scope and evidence hierarchy

This document summarizes engineering findings grounded in:
- Current GitHub source and current repository metadata (primary code evidence).
- Homologation dossier, incident register, final validation log, screening matrix, and sanitized audit package from the authorized Google Drive workspace (historical operation evidence; **not independent audit**).
- Local controlled reproductions performed on the preserved installed `dedupe_records.py` copy. Git blob SHA-1 `a34b7fe970ed465df74b4e7df352f4dd19a4c5e3` matches `main/scripts/dedupe_records.py` on the baseline commit.
- Private installed ChatGPT plugin metadata and manifests (installation evidence; not proof of live execution).

Do **not** copy Drive IDs, private local source paths, authenticated URLs, protected full texts or credentials into this public repository. This public report contains sanitized identifiers only. Original controlled evidence stays in its authorized store.

## Confirmed baseline

- `main` HEAD: `d180ea28dd9f856c4e96b86b2e6a0011a6797aa4`.
- `VERSION`, `CITATION.cff`, `README.md`, and `CHANGELOG.md` label the public code as beta.2.
- ChatGPT installation: private **skills-only** plugin `meu-artigo`, version beta.2; `plugin.json` and `.codex-plugin/plugin.json` present, with `skills/meu-artigo/SKILL.md` adapted for plugin context. It does not itself deploy an MCP server.
- [PR #22](https://github.com/rebsonm/MeuArtigoSkill/pull/22): open draft, unmerged, head `2aec56c61904f88a03564b493be7ee6050b6ff9d`, 25 changed files, based on an earlier main; provides read-only MCP Apps dashboard, five views and smoke/CI tests. No verified live Drive connector, hosted authenticated ChatGPT deployment or plugin release. Merge conflicts/semantic overlap must be reconciled against current main; never fast-forward or merge blindly.
- Historical prior suite: **332 passed** in historical `unittest_results.json`, no failures/skips. **Not rerun** during this diagnosis.
- Historical Gate 4 validator: `validation_errors=0`, `validation_warnings=48`. A strict/freeze rejection with 759 human decisions missing is expected and must remain a blocker.
- Historical Gate 4 simulated screening: 25 candidates, 18 proposed INCLUDE, four BORDERLINE, three EXCLUDE; zero individual final human decisions. Remaining 734 records and 69 near-duplicate pairs remain outside reviewed scope.
- Historical search evidence: 12 bounded searches, 1,200 occurrences, 759 canonical records, 441 exact duplicates; outputs PARTIAL. Scopus and Web of Science not executed.
- Authorized audit ZIP examined locally: 61 files, readable ZIP structure, no PDF/DOC/HTML/.env/.pem/.key entries; SHA-256 `a313bde2ba4056a49543ce8750fd8e8d72deec1a7b5d428fedfeb24f883ce370`. An extension check is **not** a complete privacy/security audit.

## Incident matrix (classification at diagnosis)

| Incident | Finding / classification | Severity | Disposition for next phase |
| --- | --- | --- | --- |
| INC-001 / COR-02 | Generator imports `artifact_tool` at module import time. Confirmed static CLI fragility; historical environment lacked optional dependency. | Medium | Lazy optional import, clear preflight, tested CSV fallback; actual new isolated failure-mode test pending. |
| INC-002 / COR-01 | **Confirmed and locally reproduced source defect:** unsupported CSV schema silently accepted. | High | Reject/quarantine missing bibliography identity before canonicalization; preserve raw metadata, IDs and fuzzy pairs. |
| INC-003 | Consensus quota exhausted: legitimate external service restriction. | Medium | Explicit restricted/blocked state; no invented zero search or paid plan requirement. |
| INC-004 | Scite entitlement required: legitimate external service restriction. | Medium | Honest optional connector fallback. |
| INC-005 | Semantic Scholar RATE_LIMITED: transient external constraint; exact cause beyond response not established. | Medium | Preserve error-vs-empty distinction and bounded retry. |
| INC-006 / COR-05 | Historical installed commit not attested; provenance/package metadata gap. | Medium | Future build manifest, revision and SHA-256 linkage; never infer historical commit. |
| INC-007 | Search Log missing literals/enum mismatch recovered operationally; NOT_EXECUTED diagnostic ambiguity remains. | Low | Clarify validation behavior/messages, add historical regression. |
| INC-008 | TRACE-0011 historical mismatch reconciled operationally; no proven current code fault. | Low | Preservation and idempotent replay test, no historical overwrite. |
| INC-G4-001 | Firecrawl INSUFFICIENT_CREDITS: legitimate provider constraint. | Medium | Explicit failure status and primary-source fallback. |
| INC-G4-002 / COR-06 | Conflicting bibliographic source dates/types/authors: established data quality issue; importer failure not yet proved. | Medium/High for R-000088 | Maintain original vs verified event/version fields; targeted normalization tests before code changes. |
| INC-G4-003 | Coverage and eligibility incomplete: scientific/human pending, **not code defect**. | High scientific gate | Preserve strict/freeze, no automatic advancement. |
| INC-G4-004 | Five inaccessible texts/limited reading: external access and scientific boundary. | Medium | No claims of full reading or inferred exclusion by paywall. |
| INC-G4-005 / COR-03/08 | `TRACE-0009;TRACE-0010` treated as one ID by current `validate_project.py` (static comparison confirmed against log); `Human_decision=PARTIAL` is historical non-final value; unverified trace and rights/editorial warnings legitimate. | Medium | Test multi-ID parser; interpret legacy PARTIAL explicitly without treating as approval; keep genuine warnings. |
| INC-G4-OPER-001 | `TRACE*.stdout.txt` absent; wrong assumption in historical orchestration, recovered; no repository fault established. | Low | Wrapper-contract test only unless source link demonstrated. |
| INC-G4-OPER-002 | Empty stderr upload lacked verified remote confirmation; environmental/orchestration hypothesis, not proven connector defect. | Low | Idempotent upload receipt/recovery tests; no fictitious confirmation. |
| COR-09 | Project config `status=INITIALIZED` at Gate 4; initializer sets this value, update semantics not yet determined. Drive is canonical; native editable Sheet has locale pt_BR and timezone America/Los_Angeles. | Medium | Verify lifecycle semantics and timestamp contract; Sheet is mirror until sync contract proves otherwise. |
| PR-22-MIGRATION | Skills-only installed plugin is not equivalent to the separate MCP Apps visual companion. Branch lags later main changes. | High integration | Design supported plugin packaging/authenticated runtime, reconcile 25 changed paths, preserve read-only scientific separation. |

**Classification precision:** Incident source allegations are not equivalent to new test results. Only INC-002 was executed as a fresh local defect reproduction in this phase. INC-001 and the TRACE list parser have direct static source evidence plus historical logs, but their new controlled executions are still pending. Historical service responses are not live rechecks.

## Controlled Phase 1 reproduction (not project data)

Executed with Python against the installed `dedupe_records.py` copy whose Git blob identity matches the baseline source. Inputs were new temporary synthetic CSV files:
1. Header `unexpected_column`, one non-bibliographic row: **exit 0**, `input_records=1`, `canonical_after_exact_dedup=1` (**INC-002 reproduced**).
2. No DOI; title, author and year supplied: exit 0, one canonical (valid no-DOI behavior baseline).
3. Two entries with identical DOI: exit 0, one canonical and one exact duplicate (control).
4. Same title/author/year but conflicting DOIs: exit 0, two canonical, one near-duplicate review pair (control).

A Python environment warmup printed a separate spreadsheet runtime warning on stderr for these commands, although they completed with exit 0; do not attribute this to the deduper without isolation. No controlled case touched the scientific project or its Drive files.

## Plugin migration design constraints

- Preserve the seven human-gated workflows and all `TRACE_ID`, `DEC_ID`, `GATE_ID`, `SNAP_ID`, `CADA_ID`, `Record_ID` records.
- Keep `GOOGLE_DRIVE_FIRST` and original authorized remote IDs as canonical. Local mirror and native Sheet are projections until explicit synchronization contract/receipts exist.
- Start from beta.2 main and **cherry-pick/reconcile** PR #22 functionality semantically; do not replace late validators/docs with older PR versions.
- Visual UI must not write scientific decisions or expose DOI/private source paths/PDFs via public MCP payloads.
- Current private plugin's installation ID/release tokens are confidential and not checked in. Updating GitHub is not an update to this plugin. Prepare a new versioned plugin package, but do not install, publish or replace without explicit approval.
- Retain platform-neutral/read-only visual fallback in `SKILL.md` while plugin-specific screens are tested. Avoid unsupported automatic app permissions.

## Gate 4 controls that must remain after maintenance

- 18/4/3 labels remain **AI simulation**, with human fields blank.
- 734 records unevaluated, 69 fuzzy pairs to review, five full texts unresolved, uncertain proceedings, R-000086 and R-000088 unresolved.
- Traces declared `UNVERIFIED` remain so. Warnings about 19 rights statuses, AI-use review, missing journal/profile, and missing XLSX remain legitimate unless genuinely resolved.
- Gates 5–7 never run as a consequence of code fixes. No manuscript/corpus freeze or scientific approval is implied.

## Five-part maintenance sequence and release stop points

1. **Diagnosis** (this document) — baseline, independent local reproduction for INC-002, incident classification, plugin migration inventory.
2. **Data and provenance correctness** — COR-01/02/03/05/06 plus regression fixtures; no semantic data migration before contract review.
3. **Orchestration, Drive and plugin UI integration** — COR-04/07/08/09, and PR #22 MCP visual reconciliation with main; enforce privilege and scientific gate boundaries.
4. **Regression and documentation** — complete old/new tests, failures/CI evidence, SKILL/README/guides/logs, release metadata and an explicit human/technical warnings taxonomy.
5. **Candidate and review** — reproducible sanitized package, SHA-256 manifest, release metadata, plugin update procedure, new draft PR and evidence; **no merge, tag/public release, plugin update, or scientific Gate 4 advancement**.

## Tests pending at end of Part 1

- Rerun of entire historical 332-test suite: **not executed** (no complete executable main checkout materialized in this session).
- XLSX with/without optional dependency: not executed.
- New validator, upload, API adapter, Drive and visual integration suite: not executed.
- Live ChatGPT MCP visual test and plugin update: not executed/unauthorized for publication.
- Independent scientific appraisal: not executed and outside software homologation.

**Next action:** Make code fixes on this branch only after keeping this diagnostic commit intact, with reproducible tests in isolated temp fixtures and no edits to the Drive homologation corpus.
