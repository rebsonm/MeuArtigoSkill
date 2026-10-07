# Canonical persistent research workspace

## Purpose

Treat the persistent project workspace as the project memory. Google Drive is the reference implementation, but an equivalent cloud/file system is acceptable. The chat is never the source of truth. Every material research action must leave a durable artifact that another agent can inspect and continue.

When persistent storage is connected, create or resume this canonical logical structure before large searches. Do not create a parallel structure if a compatible project folder already exists.

## Folder tree

Use a project root named `ARTIGO_<short-title>_<YYYY>` unless the user supplies another title.

```text
ARTIGO_<short-title>_<YYYY>/
├── 00_Gestao_e_Continuidade/
│   ├── CONTINUIDADE.md
│   ├── PROTOCOLO.md
│   ├── PROJECT_CONFIG.json
│   ├── RASTREABILIDADE.md
│   └── MATRIZ_MESTRA_<short-title>
├── 01_Auditoria_de_Novidade/
│   ├── Notas_de_Auditoria/
│   └── Artigos_Semente/
├── 02_Buscas_e_Exports/
│   ├── Scopus/
│   ├── Web_of_Science/
│   ├── Outras_Bases/
│   └── Snapshots/
├── 03_Screening_e_FullText/
│   ├── FullText_Corpus/
│   ├── Pendentes_de_Acesso/
│   └── Excluidos_com_Justificativa/
├── 04_Evidencias_e_Sintese/
│   ├── Notas_de_Sintese/
│   ├── Figuras_e_Modelos/
│   └── Claims_Ledger/
├── 05_Manuscrito/
│   ├── Rascunhos/
│   └── Versao_Canonica/
├── 06_Submissao/
│   ├── Regras_da_Revista/
│   ├── Arquivos_Finais/
│   └── Comprovantes/
└── 99_Arquivo_Historico/
```

Create only the optional subfolders needed by the project. Never delete an older valid artifact merely because a newer version exists; move superseded material to `99_Arquivo_Historico/` when cleanup is necessary.

## `CONTINUIDADE.md`

This is the first file every resumed session must read. Prefer a raw Markdown file. If the runtime cannot upload/update raw Markdown directly, maintain an equivalent Google Doc and a local Markdown mirror, then synchronize the raw `.md` when file upload becomes available.

Required sections:

```text
# CONTINUIDADE — <project>
Updated: <ISO date/time>

## 1. User research input
- Original problem/topic/question supplied by the user.

## 2. Current research object
- Current question
- Objective
- Intended contribution
- Article/review design
- Scope and exclusions

## 3. Tool and plugin status
- Google Drive
- Consensus
- Scite
- Firecrawl/web
- Scopus access
- Web of Science access
- Other relevant sources

## 4. Canonical workspace links
- Project root
- Master matrix
- Protocol
- Manuscript

## 5. Frozen decisions

## 6. Search status
- Search families and canonical versions
- Executed runs
- Counts
- Invalid/superseded runs

## 7. Deduplication and screening status

## 8. Full-text status

## 9. Evidence-matrix status

## 10. Synthesis status

## 11. Manuscript status

## 12. Journal/submission status

## 13. Open issues and blockers

## 14. Next valid action

## 15. Change log
- timestamp — material change — rationale

## 16. C.A.D.A. dashboard
- Current stage
- Stage outcome required
- READY items
- IN_PROGRESS items
- WAITING/BLOCKED items
- Hard/external deadlines
- Internal targets
- Next valid action with CADA_ID, owner, and due
- Recently completed items with evidence
- Work-management provider/container/sync health
```

Update this file after every material stage, after any invalid search/export, after a major methodological change, and before ending a long work session.

## `RASTREABILIDADE.md`

This is the human-readable process-provenance artifact. Unlike `CONTINUIDADE.md`, which describes the current state and next action, `RASTREABILIDADE.md` explains how material parts of the project were constructed.

Maintain references to major method changes, canonical search versions, corpus milestones, evidence/synthesis decisions, AI-assisted steps, human verification, manuscript versions, and submission artifacts.

Use `13_Traceability_Log` as the structured source and keep this Markdown file as the readable synthesis.

## Master tracking matrix

Create one structured master matrix named `MATRIZ_MESTRA_<short-title>`. Prefer a native spreadsheet when the platform supports it. Use the following tabs. Keep tabs even if some remain unused; mark them `NOT APPLICABLE` rather than deleting them when doing so improves continuity.

### `00_Projeto`

Key/value project metadata:

```text
Field | Value | Status | Updated | Notes
```

Include: research problem, current question, objective, contribution, article type, review type if applicable, target journal, languages, years, current scientific stage, C.A.D.A. governance status, primary work-management provider, external project/container URL, and canonical project folder URL.

### `01_Protocolo`

```text
Item | Decision | Rationale | Status | Version | Updated
```

Use for scope, criteria, databases, date limits, document types, screening rules, full-text rules, snowballing rule, stopping rule, and method-label decisions.

### `02_Search_Log`

```text
Search_ID | Date | Database_or_source | Conceptual_blocks | Literal_query | Filters | Records_found | Records_exported | Export_file_or_URL | Status | Iteration | Notes
```

Never rewrite an executed query in place. Create a new search version.

### `03_Screening`

```text
Record_ID | Source_database | Search_ID | Title | Authors | Year | DOI | Other_identifier | Abstract | Document_type | Language | Pass1_decision | Pass1_reason | Pass2_decision | Pass2_reason | Duplicate_status | Canonical_record_id | Notes
```

### `04_FullText_Tracker`

```text
Record_ID | Priority | Full_text_status | Version_accessed | Access_source | Access_date | Full_text_decision | Exclusion_reason | Evidence_matrix_id | File_or_URL | Notes
```

### `05_Evidence_Matrix`

```text
Evidence_ID | Citation | DOI_or_persistent_ID | Construct_or_concept | Definition_or_claim | Problem_tension_or_risk | Mechanism_relationship_or_finding | Study_design_or_source_type | Sample_data_or_material | Context | Process_or_stage | Actors_or_roles | Decision_right_or_action | Observable_evidence_or_artifact | Boundary_conditions | Limitations | Transferability_to_question | Evidence_role_or_strength | Supporting_locator | Epistemic_label | Notes
```

### `06_Journal_Dialogue`

```text
Journal_article | Why_relevant | What_it_already_says | What_new_article_adds | Use_in_manuscript | Citation_status | Notes
```

Use only when a target journal is known.

### `07_Normative_Corpus`

```text
ID | Institution | Document | Year | Jurisdiction | Authority_type | Scope | Relevant_constructs | Mechanisms | Lifecycle_stage | Binding_status | URL | Include_status | Version_or_access_date | Notes
```

Use only when the research problem requires institutional, legal, standard, policy, or professional authority.

### `08_Synthesis_Log`

```text
Synthesis_ID | Category_or_theme | Evidence_IDs | Cross_source_pattern | Contradictions | Boundary_conditions | Inference | Epistemic_status | Decision | Notes
```

Use to make the transition from article-by-article notes to cross-source synthesis explicit.

### `09_Claims_Ledger`

```text
Claim_ID | Manuscript_section | Claim_text | Claim_type | Evidence_IDs | Locator_status | Strength | Draft_status | Notes
```

Every important manuscript claim should eventually be traceable to evidence IDs, actual empirical results, or a clearly marked original proposition.

### `10_Submission_Checklist`

```text
Item | Requirement | Source_of_requirement | Status | Evidence_or_file | Notes
```

### `11_CADA_Control`

```text
CADA_ID | Item_type | Title | Description | Scientific_stage | Captured_at | Source_or_trigger | Assigned_to | Execution_mode | Priority | Dependency_IDs | Next_action | Deadline | Deadline_type | Status | Evidence_of_progress | Completion_evidence | Related_artifact | Related_research_IDs | Blocker | Last_updated | External_manager | External_item_ID | Notes
```

This is the canonical operational-control table. Use stable CADA_ID values and never recycle them.

### `12_PM_Sync`

```text
CADA_ID | Provider | Workspace_or_site | Container_ID | External_item_ID | External_URL | External_status | External_assignee | External_due | Canonical_status | Canonical_assignee | Canonical_deadline | Last_pushed_at | Last_pulled_at | Sync_status | Conflict | Notes
```

Use only when a work-management provider is connected. Preserve one row per CADA_ID × provider.

### `13_Traceability_Log`

```text
Trace_ID | Timestamp | Scientific_stage | CADA_ID | Actor | AI_platform_or_tool | Model_or_version | Action_type | Action_summary | Input_or_source | Source_or_artifact_IDs | Decision_or_output | Rationale | Artifact_before | Artifact_after | Verification_method | Human_validation | Related_Search_IDs | Related_Record_IDs | Related_Evidence_IDs | Related_Claim_IDs | Prompt_or_instruction_summary | Reproducibility_information | Materiality | Status | Notes
```

Use stable `TRACE-####` identifiers. Record material scientific-process events, not every conversational action.

### `14_AI_Use_Log`

```text
AI_Use_ID | Date | Scientific_stage | CADA_ID | Trace_ID | Platform_or_tool | Model_or_version | Purpose | Input_category | Output_category | Materiality | Human_review_method | Human_decision | Accepted_modified_or_rejected | Related_artifacts | Disclosure_required | Disclosure_text_or_note | Notes
```

Use stable `AIUSE-####` identifiers for material AI use. This tab supports transparency and journal-specific disclosure.

### `15_CADA_Dashboard`

```text
Metric | Value | Last_updated | Notes
```

This is a derived human-readable management view. Suggested metrics include current stage, active/blocked/overdue items, next action, external deadline, completion rate, traceability gaps, substantive AI uses pending human review, and external-manager sync health.

The dashboard is never the source of truth; derive it from canonical tables.

## Snapshot and filename rules

Preserve stage history. Use names that encode stage, source, version, count, and date when useful.

Examples:

```text
SCOPUS_S1_R1_RAW_1029_2026-10-05.csv
WOS_S2_R2_FULLRECORD_322_2026-10-05.xlsx
GLOBAL_PRE_FULLTEXT_434_2026-10-05.xlsx
FULLTEXT_TRACKER_v03_2026-10-06.xlsx
```

These are examples of naming syntax only; never reuse the counts, dates, search families, or substantive content in a new project.

Rules:

- raw exports are immutable;
- invalid exports remain preserved and are marked INVALID;
- corrected runs get a new version identifier;
- canonical files must be distinguishable from historical snapshots;
- stable IDs must survive movement between tables;
- counts reported in the manuscript must come from canonical artifacts, not chat memory.

## Creation order on a new project

When persistent storage is connected:

1. create the project root;
2. create the canonical folders;
3. create `CONTINUIDADE.md` (or temporary Doc mirror + Markdown mirror);
4. create `PROTOCOLO.md` or a native Doc mirror;
5. create the master Sheet and all tabs;
6. populate `00_Projeto` with the user's original problem and current project state;
7. record plugin/tool status;
8. initialize `11_CADA_Control` with the first actionable project items;
9. initialize `13_Traceability_Log`, `14_AI_Use_Log`, `15_CADA_Dashboard`, and `RASTREABILIDADE.md`;
10. set management mode to `MATRIX_ONLY` by default;
11. if a work-management provider is connected and useful, switch to `MATRIX_PLUS_EXTERNAL`, choose one primary provider, and initialize `12_PM_Sync`;
12. run the first novelty audit;
13. persist results before expanding the search.

Do not wait for the manuscript stage to create project state. Persistence begins before the first substantive search.
