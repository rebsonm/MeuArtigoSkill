# C.A.D.A. governance layer

## Purpose

C.A.D.A. is the operational governance layer of Meu Artigo. It gives the researcher a visible step-by-step view of the work while preserving scientific rigor.

The canonical implementation is the spreadsheet/matrix itself. External task managers are optional mirrors.

C.A.D.A. does **not** replace the scientific method, article design, review protocol, screening rules, evidence appraisal, analysis, or reporting standard.

The scientific workflow answers:

> What research procedure is valid?

C.A.D.A. answers:

> What work item exists, who owns it, what is the next verifiable action, when is it due, and what evidence shows progress or completion?

Use C.A.D.A. across every scientific stage.

## The four operations

### C — Capturar

Create a durable work item whenever something creates a meaningful action, decision, dependency, deadline, or blocker.

Examples:

- research problem received;
- novelty threat identified;
- method decision required;
- search family to execute;
- export to validate;
- borderline records to revisit;
- full text to obtain;
- evidence category to reconcile;
- manuscript section to revise;
- reviewer request to answer;
- submission deadline detected.

Do not create C.A.D.A. items for every conversational thought. Capture items only when there is a meaningful next action or follow-up need.

Every captured item receives a stable ID:

`CADA-0001`, `CADA-0002`, ...

Never recycle a `CADA_ID`.

### A — Atribuir

Every captured item must have an owner and an analytical location.

Record:

- responsible actor: researcher, coauthor, agent, reviewer, external party, or joint;
- scientific stage;
- related canonical artifact;
- related Record_ID, Evidence_ID, Search_ID, Claim_ID, or other identifier when applicable;
- priority;
- dependency/parent item;
- whether AI may execute it autonomously or human action is required.

Assignment is broader than a person's name. It answers **who/what is responsible and where the item belongs in the research system**.

### D — Definir prazo

Every active item needs a temporal expectation.

Use one of:

- `EXTERNAL` — journal, conference, ethics, funder, institutional or other real deadline;
- `USER_SET` — deadline explicitly chosen by the researcher/team;
- `INTERNAL_TARGET` — operational target proposed/managed by the workflow;
- `DEPENDENCY` — due after another verifiable item is completed;
- `TO_DEFINE` — temporarily allowed only when a real target cannot yet be set.

Never convert an internal target into an external deadline in reporting.

If a user requests a schedule, create realistic internal targets and distinguish them from hard deadlines.

### A — Acompanhar

Track each item until it is completed, cancelled, superseded, or explicitly deferred.

A task is not complete merely because somebody said "done". Whenever possible, completion needs evidence such as:

- export file validated;
- Search Log row created;
- screening decisions recorded;
- full-text file/link added;
- Evidence_ID created;
- protocol decision versioned;
- manuscript section updated;
- submission receipt stored.

Use explicit states:

- `CAPTURED`
- `ASSIGNED`
- `READY`
- `IN_PROGRESS`
- `WAITING`
- `BLOCKED`
- `DONE`
- `CANCELLED`
- `SUPERSEDED`

## C.A.D.A. control table

Maintain a canonical table/tab named `11_CADA_Control`:

```text
CADA_ID
Item_type
Title
Description
Scientific_stage
Captured_at
Source_or_trigger
Assigned_to
Execution_mode
Priority
Dependency_IDs
Next_action
Deadline
Deadline_type
Status
Evidence_of_progress
Completion_evidence
Related_artifact
Related_research_IDs
Blocker
Last_updated
External_manager
External_item_ID
Notes
```

Rules:

- one stable CADA_ID per operational work item;
- no duplicate CADA_ID;
- every nonterminal item has a `Next_action`;
- every nonterminal item has a deadline type;
- DONE should normally include `Completion_evidence`;
- changes of owner, deadline, blocker, or status update `Last_updated`;
- scientific decisions remain in protocol/evidence artifacts even when also represented as C.A.D.A. tasks.

## Stage roadmap

Use these default scientific stages. Adapt only when the article design requires it.

| Stage | Scientific purpose | Typical C.A.D.A. deliverable |
|---|---|---|
| 00 | Intake & workspace | problem captured, workspace created, integrations checked |
| 01 | Novelty audit | nearest literature assessed; contribution decision |
| 02 | Method/design | article/review track frozen |
| 03 | Protocol | scope, criteria, source roles, search families frozen |
| 04 | Search execution | database/source runs executed and logged |
| 05 | Export validation | exports verified and invalid runs isolated |
| 06 | Deduplication | canonical corpus + duplicate audit |
| 07 | Screening | pass decisions + reasons |
| 08 | Full text | access/eligibility/evidence readiness |
| 09 | Evidence extraction | evidence matrix populated |
| 10 | Synthesis | cross-source categories, tensions, boundaries |
| 11 | Journal dialogue | outlet fit + relevant journal conversation |
| 12 | Manuscript | evidence-grounded drafting |
| 13 | Final audit | counts, claims, citations, method, limits reconciled |
| 14 | Submission | files, checklist, receipt, follow-up |

Do not force irrelevant stages. Mark them NOT APPLICABLE with rationale.

## Parent/child structure

Use a hierarchy when it improves visibility:

- parent item = scientific stage/milestone;
- child item = verifiable unit of work.

Example:

```text
CADA-0030  Stage 07 — Screening
  CADA-0031  Screen Scopus incremental records
  CADA-0032  Revisit BORDERLINE set
  CADA-0033  Recheck exclusion sample
  CADA-0034  Freeze screening counts
```

Do not create thousands of external cards for individual bibliographic records. Record-level decisions belong in the screening/evidence tables. Create C.A.D.A. tasks at a useful management granularity.

## C.A.D.A. dashboard in CONTINUIDADE.md

Maintain a concise dashboard:

```text
## C.A.D.A. dashboard

### Current stage
- Stage:
- Stage outcome required:

### Active work
- READY:
- IN_PROGRESS:
- WAITING/BLOCKED:

### Deadlines
- hard/external:
- internal targets:

### Next valid action
- CADA_ID:
- action:
- owner:
- due:

### Recently completed
- CADA_ID — evidence

### Management sync
- provider:
- container:
- last sync:
- conflicts:
```

This dashboard is for orientation. The canonical detailed list remains `11_CADA_Control`.

## Spreadsheet management

Read `cada-matrix.md`.

The default mode is `MATRIX_ONLY`. The researcher can manage the entire article through `11_CADA_Control` and `15_CADA_Dashboard` without knowing any task-management software.

## Relationship to traceability

C.A.D.A. manages the work; traceability preserves how the scientific work actually occurred.

Read `traceability.md`.

Do not overload C.A.D.A. rows with every provenance event. Link CADA_ID to one or more Trace_ID values instead.

## Management-tool integration

Read `work-management.md`.

C.A.D.A. is canonical. Trello, Jira, ClickUp, or another task manager is an **operational mirror**, not the source of scientific truth.

A task-manager item should include the CADA_ID visibly. Prefer:

`[CADA-0042] Validate Web of Science export`

Scientific evidence, search strings, exclusion decisions, and evidence matrices remain in the canonical research workspace.

## Completion rule

Before marking a major scientific stage DONE:

1. verify its required scientific artifact exists;
2. verify active child C.A.D.A. items are resolved, deferred, or explicitly transferred;
3. record completion evidence;
4. update `CONTINUIDADE.md`;
5. update the master matrix;
6. synchronize the external manager when connected;
7. create the next stage's actionable items.

The user should always be able to answer:

- Where are we?
- What has been completed?
- What is blocked?
- What happens next?
- Who/what owns it?
- What is the deadline?
- What proves the work advanced?
