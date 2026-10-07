# Project state and persistent artifacts

## Core rule

Treat chat as an interface, not as project memory. Persist decisions, strings, counts, files, exclusions, evidence, synthesis decisions, and next actions outside the conversation.

When a persistent cloud/file workspace is available, use the canonical schema in `drive-workspace.md`. Google Drive is the reference implementation. When persistent storage is unavailable, create a local mirror with `scripts/init_project.py` and synchronize it later.

## Source of truth

The canonical continuity artifact is `CONTINUIDADE.md`. A resumed agent must read it before taking substantive action.

The canonical tracking artifact is the master matrix, preferably a native structured spreadsheet/table in the connected workspace, with tabs/sections for project metadata, protocol, search log, screening, full text, evidence, synthesis, claims, submission, C.A.D.A. control, optional project-manager synchronization, traceability, AI use, and the C.A.D.A. dashboard.

The spreadsheet/matrix is a complete management interface in its own right. External work-management tools are optional.

## C.A.D.A. operational state

The scientific state and the operational state must coexist.

Scientific tables preserve evidence and methodological decisions.

Operational work is governed through stable `CADA_ID` values in `11_CADA_Control`. Material scientific choices are governed through `DEC_ID`, critical human transitions through `GATE_ID`, and frozen states through `SNAP_ID`. The default mode is `MATRIX_ONLY`, using `15_CADA_Dashboard` for a readable project view. If a project manager is connected, `12_PM_Sync` maps each mirrored external item back to its canonical CADA_ID and the mode becomes `MATRIX_PLUS_EXTERNAL`.

Research-process provenance is governed through stable `TRACE-####` events in `13_Traceability_Log` and summarized in `RASTREABILIDADE.md`. Material AI use is recorded in `14_AI_Use_Log`.

Never treat an external card/ticket status as sufficient evidence that a scientific action occurred.

## Status vocabulary

Use explicit states:

- PLANNED
- IN PROGRESS
- COMPLETE
- VALID
- INVALID
- SUPERSEDED
- PENDING ACCESS
- FROZEN
- NOT APPLICABLE

## Versioning rules

- Preserve raw exports unchanged.
- Never replace an executed search string in history; create a new version.
- Preserve invalid runs with a reason rather than deleting them.
- Preserve original database occurrences even after deduplication.
- Use stable record IDs across files.
- Keep canonical/latest trackers distinguishable from historical snapshots.
- Prefer immutable identifiers such as DOI, WoS UT, Scopus EID, PubMed ID, or another persistent identifier over row numbers.
- Reconcile manuscript counts only from canonical files.

## Recovery rules

When resuming:

1. read `CONTINUIDADE.md`;
2. inspect the project root and master matrix;
3. read the protocol;
4. identify the latest canonical search, screening, full-text, evidence, synthesis, Corpus Map (when generated), C.A.D.A., decisions, gates, snapshots, traceability, and AI-use state;
5. verify the last completed stage;
6. do not reclassify decided records without an explicit audit reason;
7. continue from the documented `Next valid action`;
8. inspect active C.A.D.A. items and the next valid action;
9. reconcile the connected work-management mirror if present;
10. recover material DEC_ID decisions, the next pending/READY GATE_ID, and the latest SNAP_ID;
11. record material process-provenance events;
12. update the AI-use log for substantive/assistive AI actions when applicable;
13. update continuity and RASTREABILIDADE.md before ending.

## Required workspace details

Read `drive-workspace.md` before creating or repairing a project workspace. It defines the reference folder tree, master-matrix tabs/sections, schemas, naming rules, snapshot policy, and continuity-file structure.


## Corpus-state recovery

When resuming a project:

- if `MAPA_CORPUS.json` exists, treat it as a derived view of the retained corpus, not as a replacement for screening/evidence tables;
- verify its generation timestamp and warnings before relying on it;
- use Grounded Corpus Mode only with full text that is actually available and canonically eligible;
- never reconstruct missing corpus facts from model memory.
