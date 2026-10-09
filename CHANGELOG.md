# Changelog

## Unreleased

- Separate C.A.D.A. operational task completion from scientific decisions, evidence and execution receipts in deterministic reports.
- Prevent management-only DONE/identifier attestations from serving as scientific validation for new project gates.
- Add a cost-free auditable boundary check, compatibility-preserving project flag and regression tests.
- Freeze an unexecuted with/without C.A.D.A. comparative protocol using identical scientific safeguards and independently measured administrative outcomes; no invented efficacy findings.

- Enforce distinct provenance expectations for [L] source-supported statements, [I] analytical inferences, and [P] proposed contributions.
- Require nearby prior works, contribution differences, a bounded novelty scope and existing search references before freezing original propositions.
- Detect categorical universal-priority language and hold such claims for rewriting rather than accepting an unverifiable 'first-ever' assertion.
- Add standard-library claim-integrity audit, reuse canonical ledger columns and GATE-0006, and preserve the scientific-validity limitations of automated checks.

- Update public README and installation documentation to match the repository's intended public beta distribution.
- Introduce type-specific, no-cost critical appraisal for empirical quantitative, qualitative, mixed methods, reviews, conceptual, normative and other sources.
- Retain criterion-level judgments, documented limitations and real human response references inside the existing evidence matrix.
- Require appraisals of materially cited evidence before claim freeze in new projects and reject reliance on sources judged insufficient or unsuitable.
- Preserve older workspaces and add offline adversarial regression tests without equating checklist completion with scientific validity.

- Separate AI-only screening suggestions from researcher-attributed final Pass1/Pass2 selection decisions in existing screening records.
- Require evidence and rationale for exclusions, resolve AI-human disagreements explicitly, and block corpus freeze when human screening remains incomplete.
- Provide a standard-library screening CLI with adversarial regression tests for omitted, conflicting, and retrospectively altered decisions.
- Extend 07_SCREENING with provenance columns while retaining original decision positions, dashboard formulas, and canonical IDs.

- Add a reproducible quality-calibration framework with a frozen set of factual citations and published review-selection totals.
- Score observed manuscript outputs against published DOI/title/count facts and local textual locators, reporting explicit coverage and non-evaluated dimensions rather than invented success rates.
- Separate independent claim adjudications and conceptual-category review from metadata matching and software tests.
- Introduce an optional-cost-free public metadata pilot via Crossref/OpenAlex and an observable GitHub Actions report.
- Include adversarial offline regression tests; real scientific quality and complete review replication remain unclaimed until independent empirical evaluation.


- Require a researcher's recorded rationale and acknowledged limitation before approving scientific gates in new projects, while preserving autonomy between gates.
- Store structured formative explanations in the existing validation table and check their presence and consistency during project validation.
- Keep the submission gate operational and preserve backward compatibility for projects created before the formative control was enabled.
- Add offline regression tests for unsupported approvals, contradictory rationale/limitation, direct human response references and legacy behavior.

- Separate machine-captured local executions from unverified event declarations in the canonical TRACE log, preserving existing IDs and matrix sheets.
- Add a standard-library execution recorder with hashed receipts, allowlisted scripts, output binding and an independent receipt audit.
- Reject fabricated or altered execution receipts and old COMPLETE statuses in newly initialized projects, with regression tests for failure, partial output and unauthorized promotion.
- Report confirmed versus unverified trace events without treating local script success as proof of external queries or scientific validity.

- Add independent metadata and textual-locator checks with public free APIs and optional local PDF parsing.
- Preserve unknown status for inaccessible identifiers, sources, services, and evidence; expose correction/retraction warnings without inferring scientific validity.
- Link technical verification to the canonical evidence matrix and final literature-claim audit, with offline regression tests.

- Add conceptual-lineage fields to `09_MATRIZ_EVID` for foundational/canonical literature, classic critiques, methodological foundations, contemporary updates, empirical support, contrary evidence and contextual sources.
- Require an explicit classification basis so publication age or citation count alone cannot define a work as “classic”.
- Track whether origin/definition attributions were checked against the primary source (`PRIMARY_VERIFIED`, `SECONDARY_ONLY`, `NOT_VERIFIED`, `NOT_APPLICABLE`).
- Preserve dual anchoring between foundational/canonical literature and contemporary developments without imposing mechanical citation quotas.

- Add a blocking Google Drive-first storage gate before substantive research.
- Require the Skill to request/verify Google Drive connection before creating canonical project state.
- Require explicit affirmative user authorization before using Work/platform/local artifacts as `WORK_FALLBACK`.
- Record storage policy, storage state, Drive workspace URL, fallback authorization actor and timestamp in project state.
- Treat local/Work files as staging, not canonical state, whenever Google Drive is the project backend.
- Add validator checks and initialization safeguards so `WORK_FALLBACK` cannot be activated without explicit authorization.

- Strengthen anonymized outputs with `ZERO_NONESSENTIAL_METADATA`: remove creator/producer/generator/application fields, generation/edit timestamps, OOXML properties, PDF Info/XMP/document IDs, image EXIF/XMP/IPTC and equivalent nonessential provenance.
- Add `scripts/sanitize_metadata.py` so anonymized outgoing files are cleaned before the deterministic anonymization audit.
- Treat residual generator labels such as Python, pypdf, ReportLab, Matplotlib or LibreOffice as release-blocking metadata.
- Add regression tests proving OOXML generator metadata fails audit and is removed by the sanitizer.

- Preserve conflicting DOI records, corroborate exact-title merges with author/year and retain Unicode titles.
- Bind anonymization audits to exact outgoing file/profile hashes; reject empty scope and unverified profiles.
- Default decisions to proposals and require explicit human attribution/evidence for completed decisions.
- Add behavioral regression tests and provenance smoke test to CI.
- Shorten skill entrypoint, retain detailed stage procedures, document storage mapping and add an explicitly illustrative walkthrough.

All notable changes to Meu Artigo are recorded here.

The project follows semantic versioning while in beta. Breaking changes may still occur before 1.0.0, but they must be documented.

## 0.7.0-beta.1 — 2026-10-08

### Added

- High-rigor anonymization as a core release-control policy for generated and shareable artifacts.
- Confidential `ANONYMIZATION_PROFILE.json` with explicit identity/sensitive-term categories.
- Default `EXTERNAL_ANONYMIZED` mode when identity is unnecessary or destination rules are not yet known.
- Deterministic `scripts/audit_anonymization.py` for filenames, visible text, OOXML package content/metadata, configured identity terms, common personal identifiers, local paths and PDF checks.
- `ANONYMIZATION_AUDIT` reports with PASS, PASS_WITH_HUMAN_REVIEW, REVIEW_REQUIRED and FAIL states.
- Submission-checklist items for visible identity, hidden metadata, comments/revisions, filenames/paths/links, participant/case identifiers and final outgoing-file audit.
- GATE-0007 enforcement requiring VERIFIED anonymization state or explicit NOT_REQUIRED rationale, plus a passing audit when anonymization applies.
- User-facing anonymization documentation in `docs/ANONIMIZACAO.md` and full specification in `references/anonymization.md`.

### Privacy and scientific guardrails

- Internal identified sources and external anonymized derivatives are kept separate.
- The confidential anonymization profile is excluded from snapshots and provenance exports.
- A visually anonymous document is not considered anonymous if hidden metadata still reveals identity.
- PDF/image outputs require explicit human visual review when automation cannot guarantee inspection.
- Self-citations are not automatically deleted; journal-specific blind-review rules must be followed without distorting the scientific record.
- Anonymization may not silently alter findings, evidence, methodological facts, limitations or claim meaning.
- Participant/case de-identification does not replace ethics review, consent, data-protection duties or the research protocol when those apply.

## 0.6.0-beta.1 — 2026-10-07

### Packaging correction

- Removed the structured user-evaluation protocol, perception form, participant sample guidance, and standardized feedback collection from the repository.
- External comments are now documented only as voluntary development suggestions or methodological critiques, not as a research data-collection instrument.

- Documented the validated ChatGPT installation path: import the full ZIP downloaded from GitHub.
- Removed the incorrect assumption that Plus accounts cannot use Skills; availability is now documented as account/rollout-dependent, with a successful Plus test recorded on 2026-10-07.
- Added icon packaging/configuration guidance for `assets/icon.svg` and `agents/openai.yaml`.
- Reorganized the repository so the installable Skill bundle lives directly at repository root.
- Moved `SKILL.md`, `agents/`, `references/`, and `scripts/` to the root level expected by direct ZIP/folder installation.
- Updated release audit and platform installation guides to the root-bundle layout.
- Removed the extra `meu-artigo/` nesting that could cause incomplete uploads or hide supporting files.

### Added

- Journal-aware construction as a core intake directive.
- Early request for official author guidelines and journal template/layout when a target journal already exists.
- Canonical `JOURNAL_PROFILE.json` with separate formal editorial contract and scientific/editorial profile.
- `JOURNAL_NEUTRAL`, `JOURNAL_AWARE_PENDING_PROFILE`, and `JOURNAL_AWARE` construction modes.
- Target journal and editorial mode in the project cockpit without adding a new workbook tab.
- Material journal changes tracked through existing DEC_ID/TRACE mechanisms.
- Adversarial/contestability audit for material claims inside GATE-0006.
- Claims-ledger fields for counter-evidence, alternative explanations, boundary conditions, single-source dependency, robustness status, gate link, and human validation.
- Robustness state exported in the transparency report and W3C PROV layer.
- Validation rules that block frozen/final claims with unresolved robustness status.
- Submission-gate validation against verified journal rules when a target journal is defined.

### Scientific guardrails

- Journal rules may shape presentation and manuscript architecture but never scientific findings, evidence strength, contradictory evidence, or methodological facts.
- Journal fit must not be used to suppress disconfirming evidence.
- A supporting citation alone is not sufficient for GATE-0006 approval.
- Claims marked QUALIFIED must carry their qualification into the manuscript.

### Notes

No new management ID or workbook tab was introduced. Journal awareness reuses the existing project, journal dialogue, submission, decision, traceability, and gate structures.

## 0.5.0-beta.1 — 2026-10-07

### Added

- C.A.D.A. as the operational governance layer for scientific work.
- Spreadsheet-first `MATRIX_ONLY` management mode with optional ClickUp/Jira/Trello mirroring.
- Canonical research dashboard and scientific workflow workbook.
- Scientific-process traceability with stable `TRACE_ID`.
- AI-use transparency log and explicit human-review fields.
- Material scientific decision records with stable `DEC_ID`.
- Seven default human validation gates with stable `GATE_ID`.
- Frozen scientific states with stable `SNAP_ID` and SHA-256 manifests.
- Snapshot comparison.
- Reviewer/editor transparency report.
- W3C PROV-O provenance export.
- RO-Crate 1.3 packaging.
- SHA-256 fixity manifest.
- Interoperability export log with stable `EXPORT_ID`.
- Corpus Map specification and generator.
- Grounded Corpus Mode for evidence-bounded AI consultation over validated full text.
- Cross-platform guidance for ChatGPT/Codex, Claude, and Gemini.

### Scientific guardrails

- The Skill does not import topic/content from previous projects.
- Search strings already executed are versioned rather than silently overwritten.
- Full-text absence is not treated as a scientific exclusion criterion.
- AI output is not treated as human-validated unless an actual review action occurred.
- Critical human gates cannot be inferred from silence or unrelated user messages.
- Corpus mapping is exploratory unless the research design explicitly adopts bibliometric methods.
- Grounded Corpus Mode must cite canonical Record/Evidence identifiers and locators when available.

### Notes

No fictitious demonstration project or synthetic research corpus is included in this version.
