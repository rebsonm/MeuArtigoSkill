# Changelog

All notable changes to Meu Artigo are recorded here.

The project follows semantic versioning while in beta. Breaking changes may still occur before 1.0.0, but they must be documented.

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
- Usability-testing protocol.

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
