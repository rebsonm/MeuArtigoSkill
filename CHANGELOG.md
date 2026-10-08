# Changelog

## Unreleased

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
