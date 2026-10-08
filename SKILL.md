---
name: meu-artigo
description: Develop and resume scientific article projects with traceable literature search, evidence synthesis, drafting, and submission checks. Use for research questions, review workflows, novelty audits, and evidence-grounded manuscripts. For empirical articles, support literature and provenance without inventing design, data, or findings.
---

# Meu Artigo

## Scientific contract

Start from the user's research problem, question, or sufficiently specific topic. Preserve the original input. Prior projects may inform the process, never supply the new project's topic, criteria, sources, findings, or conclusions.

Every material manuscript claim must link to evidence or be explicitly identified as an original contribution. Distinguish literature-supported statements [L], analytical inferences [I], and original propositions [P]. Never invent sources, access, search counts, full-text reading, independent screening, empirical results, or human validation.

Operate autonomously between scientifically consequential decisions. Ask only for essential missing information or a human judgment required by the current gate. Prepare the concrete evidence and decision before asking. Silence is not approval. An available integration does not itself authorize external messages or unrelated writes.

## Start or resume

For an existing project, read CONTINUIDADE.md first, then the protocol, canonical tables, and latest frozen state. Preserve decided records and executed queries; do not reconstruct them from chat memory.

For a new project:
1. Read [plugin onboarding](references/plugin-onboarding.md). Map available capabilities by role; never invent access. Connection/installation requires the user's platform action.
2. Preserve the research input and identify the likely methodological track with [review design](references/review-design.md).
3. Ask whether a target journal and official author rules/template exist. Read [journal-aware](references/journal-aware.md). Use JOURNAL_NEUTRAL when none is selected, JOURNAL_AWARE_PENDING_PROFILE while rules are missing, and JOURNAL_AWARE only after reading the profile. Maintain JOURNAL_PROFILE.json.
4. Create/resume persistent storage using [workspace](references/drive-workspace.md) and [project state](references/project-state.md). Run scripts/init_project.py in filesystem mode. Begin a small novelty/terminology scan once the question is specific enough.
5. Use the canonical spreadsheet in MATRIX_ONLY by default. Read [C.A.D.A.](references/cada-governance.md), [matrix](references/cada-matrix.md), [template](references/spreadsheet-template.md), and [storage mapping](references/storage-mapping.md) when setting it up. Prefer a native spreadsheet, then the official generator, then CSV compatibility tables. Show 00_PAINEL.

For inexperienced users, apply [beginner mode](references/beginner-mode.md). A manager mirror is optional; use [work management](references/work-management.md) only when enabled. Keep one primary manager per article unless explicitly requested otherwise.

## Choose the scientific path

- Integrative/conceptual/theoretical: support synthesis of heterogeneous literature and explicit original contributions.
- Systematic: require comprehensive eligibility and appropriate appraisal; structured searches alone do not justify this label.
- Empirical: require actual design, data and analyses before reporting findings.
- Other review families: retrieve the appropriate methodological guidance; do not force an integrative design.

## Execute the current stage

Read only the relevant section of [detailed workflow](references/workflow-stages.md) and its references.

| Stage | Required output and control | Supporting reference |
|---|---|---|
| 1. Novelty | Compare nearest literature; narrow unsupported novelty claims | workflow-stages.md |
| 2–4. Protocol and search | Freeze eligibility and version executable queries; preserve and validate raw exports and counts | [search/screening](references/search-screening.md), [tool roles](references/tool-orchestration.md) |
| 5–7. Dedupe, screen, retrieve | Audit exclusions; preserve ambiguous duplicates; distinguish actual full text from abstracts | [search/screening](references/search-screening.md) |
| 8–9. Evidence and synthesis | Extract locators, limitations and evidence roles; compare sources; label inference | [evidence/synthesis](references/evidence-synthesis.md) |
| 10. Normative evidence | Separate institutional authority from scientific findings; omit when irrelevant | workflow-stages.md |
| 11–12. Journal and drafting | Draft from evidence and actual search logs; journal fit never changes findings | [journal-aware](references/journal-aware.md) |
| 12.5–13. Robustness and audit | Check Counter_Evidence_IDs, alternatives, boundaries, single-source dependence and Robustness_status | [scientific governance](references/scientific-governance.md) |
| 14. Submission | Verify rules, exact outgoing files and authorization; preserve submitted state and receipt | [anonymization](references/anonymization.md) |

Use scripts/dedupe_records.py for compatible exports. Conflicting DOIs must remain separate; title matches without corroborating author/year are review candidates. Lack of full-text access is pending access, not a scientific exclusion reason. Do not imply that purposive full-text sampling assessed every candidate.

Grounded Corpus Mode uses only validated eligible full text; give Record_IDs, Evidence_IDs and locators and disclose unsupported answers. Read [grounded corpus](references/grounded-corpus.md) when answering corpus questions. Corpus Map is optional exploration of real metadata, not a change of review design; read [corpus map](references/corpus-map.md).

## Decisions, continuity, and release

Read [traceability](references/traceability.md) and [scientific governance](references/scientific-governance.md) for material events. Preserve CADA_ID, TRACE_ID, Evidence_ID and Claim_ID links. Use DEC_ID for material decisions, GATE_ID for actual human checkpoints and SNAP_ID for meaningful freezes. Proposals remain PROPOSED until explicit human judgment and evidence are recorded.

Default gates cover question, method, search, corpus, synthesis, claims and submission. Apply only relevant gates. Claims marked REVISE or REJECT block final freeze; QUALIFIED wording must carry its qualification into the manuscript.

At each material stage boundary update CONTINUIDADE.md, canonical tables, RASTREABILIDADE.md and applicable AI-use records with exact counts, changes, blockers, links, and the next valid action. Record real human review; do not infer it from a script's execution.

Before external artifacts, read [anonymization](references/anonymization.md). Keep ANONYMIZATION_PROFILE.json confidential; separate identified title pages from blinded manuscripts. Audit exact outgoing files with scripts/audit_anonymization.py. Empty scope or unverified profiles cannot pass. Record actual manual review where needed. Approval is bound to file and profile hashes; any change requires a new audit. Scientific meaning and necessary self-citations must be preserved.

Run scripts/validate_project.py before release. Use scripts/governance_events.py for recorded decisions, scripts/create_snapshot.py and scripts/compare_snapshots.py for freezes, and scripts/generate_transparency_report.py for a report based solely on canonical data. These tools record/check state; they do not establish scientific validity.

For optional interoperable audit packages, read [provenance export](references/provenance-export.md): W3C PROV, RO-Crate and SHA-256 support provenance and fixity. Do not claim submission occurred without actual completion by the user or an authorized tool.
