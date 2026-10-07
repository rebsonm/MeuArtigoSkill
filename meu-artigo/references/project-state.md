# Project state and persistent artifacts

## Core rule

Treat chat as an interface, not as project memory. Persist decisions, strings, counts, files, exclusions, evidence, synthesis decisions, and next actions outside the conversation.

When Google Drive is available, use the canonical Drive workspace in `drive-workspace.md`. When it is not, create a local mirror with `scripts/init_project.py` and upload/synchronize it later.

## Source of truth

The canonical continuity artifact is `CONTINUIDADE.md`. A resumed agent must read it before taking substantive action.

The canonical tracking artifact is the master matrix, preferably a native Google Sheet, with tabs for project metadata, protocol, search log, screening, full text, evidence, synthesis, claims, and submission.

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
4. identify the latest canonical search, screening, full-text, evidence, and synthesis state;
5. verify the last completed stage;
6. do not reclassify decided records without an explicit audit reason;
7. continue from the documented `Next valid action`;
8. update continuity before ending.

## Required Drive details

Read `drive-workspace.md` before creating or repairing a project workspace. It defines the folder tree, master-sheet tabs, schemas, naming rules, snapshot policy, and continuity-file structure.
