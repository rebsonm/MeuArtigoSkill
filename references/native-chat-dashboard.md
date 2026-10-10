# Native chat dashboard — optional presentation for the Skill

## Purpose and scope

When a researcher asks "show the dashboard", "where is my paper?",
"next step" or equivalent in their own language, present a concise, grounded
dashboard directly **in the conversation**. This is part of the Skill's
presentation rules, not a request to migrate the Skill to a plugin. Native
chat widgets, if available in the active host, are a rendering capability
supplied by the host; this repository does **not** install a new UI engine.

This feature is entirely independent of the optional MCP Apps companion
proposed in PR #22. The Skill remains usable without an MCP server,
deployment, URL, custom plugin or subscription to another service.
Never claim native widgets are supported on every host.

## Source-of-truth gate: do this before rendering

1. When resuming, identify the actual authorized project and read its
   `CONTINUIDADE.md` first. Then consult the relevant canonical registers
   and, for human approval and source integrity, their actual receipts.
2. For Google Drive projects, use the **connected and authorized Drive**
   to read their canonical records. Never make a local mirror silently
   authoritative. Confirm that the connection and synchronization
   were actually observed; otherwise display them as unverified.
3. For an authorized local/Work project with Python available, optionally
   run `scripts/native_chat_dashboard.py PROJECT --format json`.
   Its output is a presentation-neutral read-only projection of the
   existing registers. It is **not** source verification.
4. If a project is not selected, offer a small "choose existing project"
   interaction rather than inventing project counts or creating a new one.
5. If data are missing, stale or conflicting, display **unknown**, **not
   available** or **requires checking**, never zero, approved or complete.

## Layout contract — five views, same underlying state

A native host may show cards, compact grids, progress lists or selectable
tabs. These are *display elements*, not project state transitions.
For small screens choose vertical stacks. Default to the concise overview;
disclose detail progressively. Use the user's conversational language per
`references/language-policy.md`; never translate canonical identifiers.
Do not use an unfamiliar UI widget if the host does not support it.

1. **Overview:** article/project name, recorded scientific stage, next
   operational action, next real human scientific decision, principal
   blocker, known synchronization state and last verified state timestamp.
   Operational fractions may be shown only with a precise denominator.
   Never show a scientific quality or completion percentage.
2. **C.A.D.A. tasks:** use one **simple four-column table**, in this
   exact order in Portuguese conversations:
   `ID Tarefa | Tarefa | Responsável execução | Prazo`.
   Map those columns to the existing canonical C.A.D.A. fields
   `CADA_ID`, `Title`, `Assigned_to`, and `Deadline`, respectively.
   Older workbook imports may use `Task` and `Owner` as fallback aliases.
   Do **not** mistake `Next_action` for the actual task, invent a responsible
   person or assign a due date when the source field is blank.
   Display missing values as "Não informado" (or an equivalent in the
   researcher's language). Do not add status, priority, progress,
   completion proofs or scientific validation as table columns.
   Existing status and evidence controls remain available to the
   underlying governance workflow but are not shown in this simple view.
3. **Human validation:** actual GATE_ID, approval status, validator
   evidence present/missing, next required decision. "Approval recorded"
   is distinct from authenticated approval and independent scientific
   validation. A historically approved gate with contradictory current
   controls requires an explicit alert.
4. **Evidence:** recorded evidence and claim counts, verified/pending/
   blocked *only if a fresh source audit actually supports them*,
   correction/retraction alerts and report freshness. If no actual
   audit was performed, show "not assessed" instead of 0 or "clear".
   Editorial notice or human exception never upgrades source status.
5. **History/synchronization:** trace log events as recorded, snapshots
   actually observed, any PM sync conflicts and Drive authorization/
   synchronization verified *in this session*. Never infer remote
   delivery from a local receipt.

The existing MINIMAL/FULL setting changes **amount of information only**.
A user tapping FULL or changing tabs must not modify PROJECT_CONFIG.json,
registers, gates or methodological choices. Treat any in-chat toggle as an
ephemeral UI preference. Persistent mode changes require the existing
attributable human action via `presentation_mode.set_mode`, not a visual
toggle.

## Renderer choice and graceful fallback

- If host-provided native visual elements are available, use their
  supported cards, tables, charts, navigation controls or progress
  indicators. Only render values grounded in a real authorized snapshot.
  Keep controls for **viewing, filtering and refreshing the presentation**,
  not approving/screening/completing/writing.
- If native elements are not supported, show one brief Markdown status
  table and a clear next action. The research process must work equally
  well in plain text. Do not rely on HTML, custom JavaScript, or host-
  specific component syntax in `SKILL.md`.
- Do not require `visual-app/` or MCP to display the Skill's native
  presentation. Those remain an optional and separately reviewable
  extension.

## Privacy and scientific boundaries

Default presentation exposes IDs, counts, generic states and timeframes,
not local paths, protected full-text passages, DOI lists, internal account
IDs, reviewer identities, unpublished critiques or confidential project
notes. Source titles and task details should only be shown after verifying
the project is authorized and the user has asked for such detail.
Even then, respect rights, anonymity and the manuscript's blind-review
requirements. Never send privileged documents to a public display.

Any interaction that would *change* a scientific state is **not a UI
action**. It must go through the existing governed research workflow and
real researcher decision, with attribution and evidence. Never fabricate
source checks, execution receipts, search results or journal submissions.
Evidence sources [L], inference [I] and original proposals [P] remain
distinct.

## Test and evaluation honesty

`tests/test_native_chat_dashboard.py` checks the local read-only JSON
projection, its visibility boundaries and missing data behavior using
synthetic fixtures. It cannot test a ChatGPT renderer, connected Drive,
quality of scientific claims or actual user experience.

A native chat visualization shown in a conversation is a **pilot example**,
not evidence that a new Skill package has already been imported into an
account. Actual activation of the updated instructions requires loading
the updated Skill artifact when that environment supports it.
