# Native chat dashboard — optional presentation for the Skill

## Optional MCP Apps component and immediate fallback

The separately maintained `integrations/mcp-apps/` companion registers
`meu_artigo_painel` with a standard `ui://meu-artigo/site-v1.html`
resource and a useful localized **text** result. The HTML begins without
fabricated project data, accepts only valid authorized read-only snapshots
and offers a manual interface-language selector. It is **not** loaded by
a Skill-only installation automatically.

If the MCP tool, UI resource or host rendering fails: use the existing
source-grounded native dashboard/text workflow in the user's language,
include actual blockers and a single safe next action, and never claim
the missing tool was executed. Treat the conversation as an equal fallback
for hosts without MCP Apps, including other AI services.

For secure setup, translation coverage, authorized host requirements and
tests see [the MCP Apps integration guide](../integrations/mcp-apps/README.md).

## Purpose and scope

When a researcher asks "show the dashboard", "where is my paper?",
"next step" or equivalent in their own language, present a concise, grounded
dashboard directly **in the conversation**. This is part of the Skill's
presentation rules, not a separate installation. Native
chat widgets, if available in the active host, are a rendering capability
supplied by the host; this repository does **not** install a new UI engine.

This presentation belongs to the Skill itself. It does not require an
external hosted interface or a separate subscription.
Never claim native widgets are supported on every host.

## Guided use in an interactive host

Apply the [shared researcher UX contract](researcher-ux.md) before choosing
a native visual layout. Start in the Overview, allow lightweight navigation
among Methods, My Justification, C.A.D.A. and All Details, and preserve a
single safe next-action summary. A view switch or draft selection is never a
canonical write. The portable local HTML view provides keyboard-accessible
focus buttons and prepares a privacy-safe continuation message without
network submission. Host-native controls must offer real actions or be
omitted; never promise unsupported tabs.

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

## Safe continuation panel

The read-only local projector uses **one** authoritative
`continuation` classification from `scripts/next_step_router.py`.
For backwards compatibility, `overview.next_task_id` and
`overview.next_gate_id` are aliases of these same safe values, **not**
competing first-active-row predictions. This prevents a BLOCKED or CAPTURED
row from appearing as an executable task and keeps undocumented human gates
pending. The four-column C.A.D.A. table remains unchanged; MINIMAL
prioritizes the eligible task when one exists. The fallback prints the safe
next step only once with its first blocker. Neither view exposes the raw
`Next_action` prose, continuity text, source excerpts or review evidence.
MINIMAL and FULL preserve the same classification and scientific controls.

Navigation status never authorizes actual actions; agents still need their
existing execution rights and must record actual outcomes in the canonical
store. The `próximo` command is an expression of navigation intent, not
approval of GATE-0001–GATE-0007. A documented approval is not proof of the
researcher's identity. If continuity, dependencies, storage or transactions
are unverified, surface the blocker rather than moving to a later stage.

## Conversational resume — `continue` / `próximo` / `next`

For a selected, **authorized** local/Work project, the Skill may use
`scripts/research_resume_brief.py PROJECT --format json`. It reads the
same `native_chat_dashboard.panel`, which already reconciles C.A.D.A.,
the seven human gates, DEC/TRACE, method profile and known continuation
conflicts. This is an **optional read-only view**, not a new scientific
control, persistent progress ledger, external service or method choice.

Respond in the researcher's conversational language and include only:
the last **recorded** decision ID (if reliably present, never a claim
of human authentication); the recorded methodological route and next
missing required field (not an evaluation of completeness); the existing
next CADA_ID/GATE_ID and responsible actor; the first blocker and what
original records must be reviewed; and an invitation to explore the
next valid step without treating a chat navigation request as approval.
The brief refuses to disclose private researcher rationale, task title,
`Next_action` prose, sources, documents or storage credentials.

The result is always guidance. A `TECHNICAL_PREPARATION_CANDIDATE` is a
router-derived *candidate*, **not execution authorization**. Before
actually running a task, independently re-check the current canonical
state, real operator permission, and the existing C.A.D.A. rules.
A `RECONCILIATION_REQUIRED` state permits an explanation and original
record review, not technical task execution or a gate transition.

A local bridge/snapshot cannot verify canonical Google Drive sync.
The resume brief therefore blocks local technical preparation on
Drive-canonical mirrors and on local projects without an explicitly
recorded `WORK_FALLBACK` authorization. For Drive projects, read and
reconcile the canonical records using the **authorized Drive tools
themselves**; do not promote a local snapshot to the source of truth.
A missing actual project must trigger selection of an authorized project,
not a fictional resume. When local scripts are unavailable, apply these
same rules to the verified records through the host's native interface.
The JSON status codes are locale-neutral; host language adaptation
does not change the decisions or read/write permissions.

## Conversational blocker resolution (safe explanation only)

When the resume summary reports `RECONCILIATION_REQUIRED` or the
researcher asks why the work cannot continue, the Skill can run
`python scripts/research_blocker_guide.py PROJECT --format json`
for an **already selected, authorized local project**. This tool composes
the previous read-only `research_resume_brief` and never edits records.
For Drive-canonical research, it **cannot** establish current Drive
access/synchronization; inspect the canonical files via authorized
Drive tools and apply the same conservative principles in chat.

Speak the researcher's language. Prefer four concise elements:
**what is blocking progress** (an explanation, not just an internal
status code), **why it matters**, **which original records need review**,
and **who is responsible for the decision or verification**. Present
the most consequential issue first. When multiple issues exist,
progressively disclose details, never claim that a code is evidence of
file corruption or of real-world scientific invalidity.

A safe interaction offers only real read-only alternatives: show the
known recorded reference IDs, compare canonical DEC/TRACE, inspect
C.A.D.A./continuity evidence, or discuss method options without
recording a researcher choice. A journal recovery, storage fallback,
methodological choice, gate approval, sync or task-state change requires
the existing governed workflow and **independent rechecking of current
authorization**; no click, `next`, `repair` or merely viewing this
guidance authorizes a write. Do not ask for credentials in chat.
Unknown blocker codes are deliberately summarized as
`UNCLASSIFIED_RECONCILIATION_CAUSE` instead of being echoed as
trusted instructions.

Only fixed public relative canonical filenames and technical status
labels are emitted. The guide never exports the original decision
rationale, research content, source excerpts, private C.A.D.A.
`Next_action` or filesystem paths. It cannot verify researcher identity,
user experience or real cloud synchronization. No extra installation
is required beyond the normal Skill execution environment.

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
- Do not require `an external dashboard to display the Skill's native
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
