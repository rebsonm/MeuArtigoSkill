# Project state and persistent artifacts

## Core rule

Treat chat as an interface, not as project memory. Persist decisions, strings, counts, files, exclusions, evidence, synthesis decisions, and next actions outside the conversation.

Google Drive is the default canonical project memory. Before substantive research, verify that Drive is connected and writable. If it is not, request the platform connection flow and re-check. If Drive still cannot be used, do not silently create a local mirror. Ask the user explicitly whether they want to continue without Drive using Work/platform/local artifacts. Only after an affirmative answer may `scripts/init_project.py` or equivalent local storage become the temporary canonical fallback. Record that authorization and the storage limitation in PROJECT_CONFIG.json and CONTINUIDADE.md.

If fallback was authorized and Drive later becomes available, migrate/synchronize the project to Drive before treating new Drive artifacts as canonical. Preserve the fallback history and do not silently discard either state.

## Researcher understanding at critical gates

New project configurations enable `formative_gates_required=true`. For GATE-0001 through GATE-0006, keep the researcher's own reason for a scientific choice and one limitation in the canonical `18_Human_Validation_Gates.csv` Notes field, with an external reference to the direct response. The validator checks structure and consistency, not genuine comprehension or identity. Do not infer gate approval from silence or model-written text. See `docs/VALIDACAO-FORMATIVA.md`.

## Recorded execution evidence

Confirmed local operations should be recorded with `scripts/trace_execution.py` and their receipts stored at `00_Gestao_e_Continuidade/TRACE_RECEIPTS/`. Do not equate an automatically generated TRACE row with proof that a database search, external service action or human approval actually occurred. New projects enforce `trace_receipts_required=true`; older `COMPLETE` statuses are legacy and require explicit reconciliation before any claim of confirmed execution. Audit receipts when resuming and before an external transparency report. Keep receipts synchronized to Drive when it is canonical.

## Source of truth

The canonical continuity artifact is **`00_Gestao_e_Continuidade/CONTINUIDADE.md`**, inside the project workspace (both when the authorized workspace is on Drive and when WORK_FALLBACK is expressly approved). A resumed agent must read that exact file before substantive action and verify that the recorded storage backend is still accessible. Do not mistake a root-level `CONTINUIDADE.md` for the canonical document or silently migrate/overwrite it; if such a copy exists, pause and reconcile the conflict with the researcher. A missing Drive connection is not permission to switch to Work/local storage.

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

## Snapshot collision and interruption safety

Snapshots are immutable research evidence. If a snapshot directory already
exists for a would-be `SNAP_ID` (including a different milestone name or an
incomplete directory whose registry row is missing), snapshot creation fails
closed. Never delete the folder to force success. Reconcile the original
manifest, files, snapshot register and gate reference before retrying; do not
claim an interrupted snapshot was validated. These local protections do not
prove a Google Drive copy was completed.

## Recoverable method-route changes

The local `choose_method_route.py` command journals the scientific method
route transition across PROJECT_CONFIG, METHOD_PROFILE, human gate table,
DEC decision log and TRACE register. An ordinary failure rolls back these
five local artifacts; a hard interruption leaves
`00_Gestao_e_Continuidade/.pending_method_route_change` and project
validation blocks further work. Inspect the canonical files and use
`python scripts/choose_method_route.py /authorized/project --recover-pending`
in a safe, authorized local environment to reconcile a PREPARED transaction.
A COMMITTED journal is cleared only if its resulting file hashes still match.
Do not remove the journal by hand or treat a route decision as a completed
scientific gate. Recovery does not prove external Drive synchronization.
The journal protects these five files only; changes made by unrelated writers
or other processes outside this protocol are not transactionally protected.

## Human gate and snapshot recovery

The local `governance_events.py gate` workflow now journals TRACE,
human-validation gates and the snapshot register as one recoverable unit.
Before any new snapshot appears, an ordinary failure restores original
registers. Abrupt interruptions leave
`00_Gestao_e_Continuidade/.pending_gate_snapshot` as a visible blocker;
`python scripts/governance_events.py recover-gate PROJECT` performs
explicit, verified recovery of a PREPARED local operation. If an interrupted
operation has already created a snapshot folder, the journal stays and
automatic recovery refuses to delete or silently declare that folder valid:
its evidence requires reconciliation. Historical decisions are preserved;
the code cannot authenticate human identity or confirm Google Drive writes.

## Cross-operation consistency and interlocks

Three recoverable local workflows share canonical files: bibliographic
metadata imports, human method-route selection and gate/snapshot recording.
When an operation leaves its journal behind, **other** workflows that touch
these records refuse to write or perform independent rollback. Recovery is
explicit and journal-specific; reconcile existing data before trying another
operation. Gate-initiated snapshots are allowed only in their controlled
workflow; a direct snapshot request cannot proceed while another research
journal is pending. Do not manually remove journal folders.

This interlock is a *fail-closed pending-journal check*, not a multi-process
mutex or a replacement for exclusive filesystem locking. Independent direct
writers, concurrent starts racing before journal creation and external Google
Drive synchronization are not covered. Do not run concurrent local writers;
the final homologation must validate end-to-end Drive state separately.
No synthetic test constitutes human scientific approval.

## Deterministic, read-only "next" navigation

When a researcher says "próximo", "next", "continue" or "resume", the
current chat is not a scientific approval. On local authorized fallback
projects, `scripts/next_step_router.py PROJECT --intent next` reads the
persisted `CONTINUIDADE.md`, checks known transaction journals and the
canonical C.A.D.A. and seven-gate tables, then classifies which documented
action is eligible to be prepared. It does **not** execute that action,
authenticate the person who approved a previous gate, or write to any file.
It returns only task/gate identifiers and generic codes, never private
research notes, quoted text or the full `Next_action`.

The local resolver reads only the management-folder continuity document that `init_project.py` actually creates. A second root-level file is not a fallback and blocks navigation until explicitly reconciled. The local resolver also compares `CADA_ID` markers in the
`Next valid action` sections of `CONTINUIDADE.md` to the eligible C.A.D.A.
task. Conflicting markers or a mismatch disable technical preparation and
require reconciliation; private continuity prose is not returned. Such
markers are structured hints, not executable instructions, and their absence
never proves a task was completed. The next candidate task must be
READY/IN_PROGRESS, contain a recorded Next_action, have genuinely completed
dependencies with operational evidence,
and not skip a still-unapproved earlier human gate. The execution mode must
explicitly allow agent preparation. Decisions assigned to the researcher,
unrecognized execution modes, missing evidence, duplicate identifiers or
an interrupted transaction block automatic advancement. The gate resolver
does not skip a "COMPLETED" row without structurally documented human
review; documentation alone still does not independently authenticate the
reviewer. An incomplete seven-gate schema requires reconciliation.
The C.A.D.A. dashboard is derived, not authoritative.

For Google Drive-canonical projects, a local readout is never proof that
remote state is synchronized or writable. Connect through the actual
authorized Drive and check its current artifacts before action; do not
convert the local router's `CANONICAL_STORAGE_RECHECK_REQUIRED` status
into a fake approval. A user's earlier fallback authorization is not
perpetual permission to use an unsynchronized mirror after Drive becomes
available. If `CONTINUIDADE.md` and current matrices disagree, inspect
the conflict before applying any writes.

## Recovery rules

When resuming:

1. read `CONTINUIDADE.md`;
2. inspect the project root and master matrix;
3. read the protocol;
4. identify the latest canonical search, screening, full-text, evidence, synthesis, claim-robustness status, Corpus Map (when generated), journal profile/mode, C.A.D.A., decisions, gates, snapshots, traceability, and AI-use state;
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


## Journal-state recovery

When resuming a project:

- read `JOURNAL_PROFILE.json` when present;
- distinguish JOURNAL_NEUTRAL from JOURNAL_AWARE_PENDING_PROFILE and JOURNAL_AWARE;
- verify whether the rules were actually checked and when;
- do not assume a target journal from prior model memory;
- if the journal changed, recover the latest non-superseded profile and related DEC_ID.

Before manuscript consolidation, if the project is still JOURNAL_NEUTRAL, surface the target-journal decision without blocking scientific work.

## Claim-robustness recovery

Before considering GATE-0006 ready, recover the claims ledger and inspect Robustness_status, Counter_Evidence_IDs, Alternative_explanations, Boundary_conditions, Single_source_dependency, and Human_validation for material claims.

Do not treat a claim as validated merely because Evidence_IDs are present.


## Canonical backend and view mapping

Read [storage mapping](storage-mapping.md) before exporting, synchronizing or resolving conflicts between CSV tables and workbook views. The template generator does not synchronize existing research data.

## Evidenced C.A.D.A. completion and continuity transaction

For **explicitly authorized local WORK_FALLBACK projects only**, an actual
local execution recorded by `trace_execution.py run` with a `CADA_ID`,
appropriate stage and a changed, verifiable output artifact may be followed by:

```bash
python scripts/update_cada_continuity.py PROJECT --cada-id CADA-0002 --trace-id TRACE-0001
```

This is **an operational task-state transition**, not an AI claim to have
reviewed a research finding. The updater verifies the unique CONFIRMED
TRACE row, SHA-256 receipt, actual changed local output, matching task
stage and `Related_artifact`, authorized execution mode, dependencies
and current continuity. Only an eligible READY/IN_PROGRESS task may be
marked DONE. It then transactionally changes exactly the existing
`11_CADA_Control.csv`, `CONTINUIDADE.md` and
`15_CADA_Dashboard.csv` files; the existing TRACE and seven human-gate
rows are not forged, deleted or approved. Current next-action markers in
continuity and dashboard are derived from recorded tasks and pending
gates, never reconstructed from the chat. Where a human gate is pending,
the next item indicates researcher review, not approval. Other continuity
paragraphs and management metrics not derived by this command are
preserved. Neither spreadsheet nor files are synchronized with Drive by
this local operation; on Drive-canonical projects, refuse this local write.

The journal `.pending_cada_continuity` integrates with the existing
scientific/bibliographic interlocks, and interrupts ordinary navigation and
writes until recovered. On an interrupted PREPARED local write, inspect
the files and run:

```bash
python scripts/update_cada_continuity.py PROJECT --recover-pending
```

Recovery compares pre- and post-operation SHA-256 with current files; if
an independent edit is detected, it preserves the journal for explicit
reconciliation rather than overwriting someone else's work. A COMMITTED
journal is cleared only when all three outputs match. These protections
do not create a cross-process database transaction, external authentication
or independent scientific validation.

## Phase 5 integrated integrity and conservative project validation

After a local PR-49 C.A.D.A. completion, the read-only
`scripts/cada_continuity_integrity.py` audits the three canonical
operational artifacts **together**: the last completed CADA_ID, TRACE
receipt and current output hash; `11_CADA_Control.csv` status;
`CONTINUIDADE.md` next-action markers and change-log linkage; and
`15_CADA_Dashboard.csv` current counts, task and gate IDs. The
`validate_project.py` command checks this audit, and the native chat
dashboard shows a generic integrity status/error count without leaking
research notes or source material. A broken audit disables proposed
technical preparation in the panel and prevents another evidenced
C.A.D.A. write until records are reconciled.

A pending `.pending_cada_continuity` journal independently blocks
project validation, even when three CSV/Markdown files happen to
exist. Explicit verified recovery is required. Audit is read-only and
does not approve scientific gates, authenticate a reviewer or verify
remote Drive synchronization. Legacy projects without a previous
evidenced C.A.D.A. completion are left NOT_APPLICABLE_LEGACY; when a
task has a TRACE-linked completion but its dashboard pointers have
been deleted, the mismatch is explicitly blocked instead of silently
treating it as legacy. Only local confirmed executions are checked;
the audit does not itself validate interpretation, causality, external
API retrieval, paper quality or claimed human reviews.

