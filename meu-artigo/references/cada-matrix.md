# C.A.D.A. spreadsheet / matrix management

## Principle

The spreadsheet is the universal C.A.D.A. management interface.

A researcher does **not** need ClickUp, Jira, Trello, or prior project-management knowledge to use Meu Artigo.

Every project should work fully in one of two modes:

- `MATRIX_ONLY` — canonical spreadsheet + CONTINUIDADE.md + research artifacts;
- `MATRIX_PLUS_EXTERNAL` — the same canonical spreadsheet plus an external task manager mirror.

The matrix is always created. External tools are optional.

## Canonical tabs

Management and provenance tabs:

- `11_CADA_Control` — canonical operational work items;
- `12_PM_Sync` — external task-manager mapping; can remain empty;
- `13_Traceability_Log` — material process-provenance events;
- `14_AI_Use_Log` — AI-specific transparency/disclosure log;
- `15_CADA_Dashboard` — human-readable management dashboard derived from canonical tables.

## 11_CADA_Control as a task manager

Treat `11_CADA_Control` as a complete project-management table.

Recommended user-facing columns to keep visible/frozen first:

```text
CADA_ID
Scientific_stage
Title
Assigned_to
Next_action
Deadline
Deadline_type
Status
Priority
Blocker
Evidence_of_progress
Completion_evidence
Last_updated
```

Additional provenance/linking columns may remain to the right.

## Suggested spreadsheet usability

When the spreadsheet platform supports it:

- freeze the header row;
- freeze identifier/stage/title columns;
- enable filters;
- add dropdown/data validation for controlled vocabularies;
- use date formatting for deadlines;
- add filter views for ACTIVE, BLOCKED, OVERDUE, DUE SOON, DONE;
- protect identifier/formula columns when appropriate;
- do not use decorative formatting that obscures auditability.

Conditional formatting may be used for usability, but never encode scientifically meaningful information by color alone.

## Useful views

### Active work

Filter status to:

- READY
- IN_PROGRESS
- WAITING
- BLOCKED

### Next actions

Show:

- CADA_ID
- Title
- Assigned_to
- Next_action
- Deadline
- Status

Sort by deadline, priority, stage.

### Blocked work

Show BLOCKED/WAITING plus:

- Blocker
- Dependency_IDs
- responsible actor
- next resolution action.

### Completed with evidence

Show DONE plus:

- Completion_evidence
- Related_artifact
- Last_updated.

### Deadline view

Separate:

- EXTERNAL
- USER_SET
- INTERNAL_TARGET
- DEPENDENCY
- TO_DEFINE.

Never merge internal targets with external deadlines.

## 15_CADA_Dashboard

This tab is a derived summary, not a source of truth.

Suggested metrics:

```text
Current_scientific_stage
Current_stage_outcome
Total_active_items
Ready_items
In_progress_items
Waiting_items
Blocked_items
Overdue_items
Due_next_7_days
Done_items
Completion_rate
Next_CADA_ID
Next_action
Next_owner
Next_due
Hard_external_deadline
Last_completed_CADA_ID
Last_trace_event
Traceability_gaps
Substantive_AI_uses_unreviewed
External_PM_provider
External_PM_sync_health
Last_updated
```

When formulas are supported, derive metrics from `11_CADA_Control`, `13_Traceability_Log`, and `14_AI_Use_Log`.

When formulas are not supported, update dashboard values after material stages.

## Spreadsheet-only workflow

In `MATRIX_ONLY` mode:

1. create all canonical matrix tabs;
2. initialize C.A.D.A. tasks;
3. set `work_management_provider = null`;
4. set `work_management_mode = MATRIX_ONLY`;
5. keep `12_PM_Sync` empty but present;
6. use `15_CADA_Dashboard` as the primary visual management interface;
7. update C.A.D.A. and dashboard after material actions;
8. continue full traceability logging.

The absence of an external PM tool is never a blocker.

## External-manager workflow

In `MATRIX_PLUS_EXTERNAL` mode:

1. the matrix remains canonical;
2. select one primary provider;
3. mirror operational items;
4. map each external item through `12_PM_Sync`;
5. reconcile conflicts explicitly;
6. update the dashboard with sync health.

## Relationship to traceability

The spreadsheet is not only a task list.

It should allow the researcher to navigate:

```text
CADA_ID (work)
   ↓
Trace_ID (what actually happened)
   ↓
Search/Record/Evidence/Claim IDs (scientific artifacts)
   ↓
AI_Use_ID when AI materially contributed
```

This is what makes the matrix useful for both project management and scientific transparency.
