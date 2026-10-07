# Work-management integration: ClickUp, Jira/Atlassian, Trello

## Purpose

Meu Artigo may mirror C.A.D.A. work items into a work-management system so the researcher can see the article as an executable project.

Supported conceptual targets include:

- ClickUp;
- Jira through Atlassian;
- Trello;
- another task/issue manager with equivalent read/write capabilities.

The scientific workspace remains canonical. External project-management systems are operational mirrors.

## Provider selection

Use exactly one primary work-management provider per article unless the user explicitly asks for multiple.

Resolve provider in this order:

1. provider explicitly selected in project configuration;
2. provider containing an existing linked project/board/list for this article;
3. if exactly one supported provider is connected, use it;
4. if several are connected, choose by existing work context:
   - prefer Jira when the research already lives in an Atlassian/team project context;
   - prefer ClickUp for a general-purpose research project needing hierarchy, assignments, deadlines, custom fields, or richer project tracking;
   - prefer Trello for a lightweight visual board, especially for a simple/solo workflow;
5. if several are connected and no contextual signal exists, default to ClickUp as the general-purpose provider, record the choice as `AUTO_SELECTED`, and allow the user to change it later;
6. if none is connected, continue without external PM and surface a connection option when useful.

Persist:

- provider;
- workspace/site;
- project/board/list/container ID;
- container URL;
- sync mode;
- last successful sync.

Do not silently create the same project in multiple providers.

## Canonical sync table

Maintain `12_PM_Sync`:

```text
CADA_ID
Provider
Workspace_or_site
Container_ID
External_item_ID
External_URL
External_status
External_assignee
External_due
Canonical_status
Canonical_assignee
Canonical_deadline
Last_pushed_at
Last_pulled_at
Sync_status
Conflict
Notes
```

One row per CADA_ID × provider.

## Source-of-truth rules

Canonical scientific truth:

- `CONTINUIDADE.md`;
- protocol;
- Search Log;
- screening table;
- full-text tracker;
- evidence matrix;
- synthesis log;
- claims ledger;
- C.A.D.A. control table.

External manager may control day-to-day presentation of:

- assignee;
- due date;
- operational status;
- priority;
- comments;
- checklists;
- reminders.

If external and canonical values conflict:

1. do not silently overwrite the canonical record;
2. log the conflict in `12_PM_Sync`;
3. reconcile based on the most recent intentional change;
4. never let an external task status change scientific evidence or eligibility decisions by itself.

## What to create externally

Default project title:

`ARTIGO — <short title>`

Represent scientific stages as the provider's best available grouping:

- ClickUp: Space/Folder/List or List + task hierarchy;
- Jira: existing Project + Epic, or another permitted hierarchy;
- Trello: Board + Lists;
- equivalent platform: project/container + stages.

Do not assume the user has admin permission to create a new Jira project. If project creation is unavailable, create/use an Epic or issue grouping in an authorized project.

## External item format

Task/issue/card title:

`[CADA-####] <action-oriented title>`

Description should contain:

```text
CADA_ID:
Scientific stage:
Purpose:
Next action:
Owner:
Deadline:
Deadline type:
Dependencies:
Canonical artifact:
Completion evidence required:
```

Add links to the canonical workspace when available.

## Status mapping

Do not require custom statuses. Map provider-native states to canonical C.A.D.A. states.

Suggested logical mapping:

| C.A.D.A. | Generic PM |
|---|---|
| CAPTURED | Backlog / Inbox |
| ASSIGNED | To do |
| READY | Ready / To do |
| IN_PROGRESS | In progress |
| WAITING | Waiting / On hold |
| BLOCKED | Blocked |
| DONE | Done / Complete |
| CANCELLED | Cancelled / Archived |
| SUPERSEDED | Superseded / Archived |

When the provider cannot represent WAITING/BLOCKED separately, use labels/custom fields/comments.

## ClickUp adapter

When ClickUp is connected:

- create or reuse one article container;
- prefer parent tasks for scientific stages and child tasks for operational units;
- use due dates and assignees when known;
- use custom fields only when they materially improve C.A.D.A. visibility;
- keep CADA_ID in the task name even if a custom field also exists;
- use task comments for progress evidence links, not as the only scientific record.

## Jira / Atlassian adapter

When Atlassian/Jira is connected:

- search for an existing authorized project appropriate to the article before attempting project creation;
- prefer an Epic named `ARTIGO — <short title>` when project creation is unnecessary or not permitted;
- create Tasks/Stories beneath or associated with the Epic using `[CADA-####]`;
- map status to the project's existing workflow rather than assuming custom statuses;
- use labels such as `meu-artigo` and `cada` when permitted;
- store canonical workspace links in the issue description;
- comments may record progress, but scientific decisions must also be persisted canonically.

## Trello adapter

When Trello is connected:

Prefer one board per article when permitted.

Suggested lists:

- Capturado
- Próxima ação
- Em andamento
- Aguardando / Bloqueado
- Concluído

Cards use `[CADA-####]` in the title. Use labels for scientific stage and deadline type where useful.

Do not put one card per literature record; group work at an actionable research-management level.

## Synchronization moments

Synchronize when:

- a C.A.D.A. item is created;
- owner changes;
- deadline changes;
- item enters/leaves BLOCKED;
- item is completed;
- a major scientific stage closes;
- the user asks for a project-status view;
- before ending a long work session.

Avoid unnecessary writes for trivial notes.

## Project-status briefing

When the user asks "onde estamos?", "o que falta?", or equivalent, answer from canonical C.A.D.A. state and, if available, reconcile with the external manager.

A useful briefing contains:

- current scientific stage;
- completed milestone;
- active C.A.D.A. items;
- deadlines;
- blockers;
- next valid action;
- progress evidence;
- sync health.

## Privacy and access

Do not copy full copyrighted papers or sensitive research data into external task descriptions unless the user explicitly intends that and access controls are appropriate.

Prefer links/IDs to canonical artifacts.

Third-party connection and authorization remain user-controlled.
