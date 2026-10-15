# Native visual dashboard in ChatGPT (Skill-only pilot)

The researcher can use **Meu Artigo as a Skill** and ask the assistant to
display a visual research dashboard inside the chat. This does **not**
require adopting a custom external application or hosting any server.

The host is responsible for deciding which native cards, grids, tables,
indicators or interaction elements it can display. The Skill's canonical
science and storage rules apply unchanged. Where a host does not provide
native visual elements, use ordinary Markdown and conversational updates.
A native panel is regenerated from actual authorized project information
during the conversation; it is not an independently installed persistent
web application.

## Five views

| View | Presented | What is *not* implied |
| --- | --- | --- |
| Overview | Article stage, next task, pending researcher decision | Quality or total scientific-completion percentage |
| C.A.D.A. | Four-column table: task ID, task, execution owner, due date | Completed scientific validation |
| Human gates | Registered decisions and review evidence | Authenticated human identity or science certification |
| Evidence | Actual evidence counts, source checks only if audited | Real literature search, text access or semantic validation |
| History / sync | Logs and observed transfer evidence | Live Google Drive synchronization without verification |

Modes **MINIMAL** and **FULL** alter only presentation detail.
Navigating tabs, filtering and toggling presentation in chat do not
write to scientific registers or to PROJECT_CONFIG.json.

## C.A.D.A. — compact table

For a user interacting in Brazilian Portuguese, the C.A.D.A. view is
limited to these four columns, in this order:

| ID Tarefa | Tarefa | Responsável execução | Prazo |
| --- | --- | --- | --- |

Each row is read from `CADA_ID`, `Title`, `Assigned_to` and `Deadline`
in the authorized canonical C.A.D.A. CSV register. Older Excel imports
may use `Task` and `Owner` when the canonical headings are absent.
MINIMAL prioritizes active tasks; FULL shows every recorded task. An absent field is
presented as "Não informado", not fabricated. Do not add status,
priority, claim-evidence information or approval buttons to this
table. MINIMAL can show fewer rows than FULL; neither mode changes
the canonical register.

## Pilot workflow

1. Ask in the researcher's usual language: "Show the Meu Artigo panel for
   my current project."
2. Identify and read the authorized `CONTINUIDADE.md` and the relevant
   canonical records, preferably directly from the connected Drive.
3. Build the five views from the real state, labeling any unavailable
   register explicitly as unavailable. Default to MINIMAL.
4. If supported, use the ChatGPT host's native visual presentation. If not,
   fall back to a compact Markdown table. Do not describe a mockup as a
   verified project snapshot.
5. Validate the clarity of the display with the researcher; do not label
   one conversation a UX study or an empirically validated product.

For a strictly read-only local/Work projection, without deploying an external service:

~~~sh
python scripts/native_chat_dashboard.py /authorized/project --format json
python scripts/native_chat_dashboard.py /authorized/project --mode FULL --format text
~~~

The Python script consumes the existing canonical configuration and
registers and never writes to them. It deliberately reports local Drive
synchronization as **not verified in this session** and reports mere
presence of `SOURCE_VERIFICATION.json`, never unverified health checks.
A host may add real fresh audit results after separately checking them.

## Relationship to PR #22

The optional **external application Apps** implementation in
[PR #22](https://github.com/rebsonm/MeuArtigoSkill/pull/22)
remains untouched and unmerged. It is a more deeply customized interface
that requires a connected compatible external application service. This Skill-native
pilot is independent: users do not need that PR to see ordinary charts,
tables, cards and research status messages in an environment that can
render those natively. Neither option replaces the Skill.

## Status and validation limits

This capability is an experimental **software pilot** in `main`.
The local projection has synthetic regression tests. No claims are made of installing the changed Skill in a
user account, running a live ChatGPT host compatibility test, or verifying
Drive sync or empirical usability. Separate setup and research review
are still required for these claims.

## Phase 5: safe navigation with "next" / "próximo"

The read-only local projection exposes a `continuation` object with
a status code, next `CADA_ID`, next `GATE_ID`, pending human-decision
requirement, eligibility for technical preparation and recorded blockers.
Unlike the previous raw *first active task* projection, it considers the
canonical continuity document, completion evidence for dependencies,
all seven scientific gates and pending transaction journals.

The C.A.D.A. layout still contains **exactly four columns**.
MINIMAL and FULL show the same safety classification and differ only
in the amount of displayed detail.

Example for an expressly authorized local project:

```bash
python scripts/next_step_router.py /authorized/project --intent proximo
python scripts/native_chat_dashboard.py /authorized/project --format json
```

Neither command is an autonomous file-modifying agent.
`technical_preparation_possible=true` only indicates that a recorded
technical task may be considered after verifying real permissions and
observed results. It does not grant authority to approve a research
protocol, choose the scientific method, pass a human gate, record an
invented researcher's judgment or claim Google Drive synchronization.

Dependencies, permissions and task statuses must be checked against the
actually canonical storage. Tests use disposable synthetic projects
and do not constitute interface homologation or scientific validation.

## Phase 6: one next step, not competing dashboards

The `overview.next_task_id`/`next_gate_id` keys remain available to
existing native renderers, but are now read-only aliases of the
`continuation` safe classification. They no longer represent the first
active row or merely a gate with a non-COMPLETED status. Pending gate
approval requires the existing full documented check, including validation
reference; no new acceptance rule was introduced.

MINIMAL displays at most three C.A.D.A. rows and puts the genuinely
eligible task first if present, even when earlier rows are BLOCKED or
CAPTURED. FULL retains the complete recorded order. Both render exactly
`ID Tarefa | Tarefa | Responsável execução | Prazo`; neither renders
private `Next_action` text or mistakes a recorded C.A.D.A. completion
for independent science. The text fallback has one "Next step" line
and a single generic first-blocker status, not a second/raw recommendation.

The existing `next_step_router.py` now supplies the same
`pending_human_gate` and `next_eligible_task` pure rules to the
post-TRACE C.A.D.A. updater. This removes duplicated eligibility logic
instead of adding another orchestration layer, metric, file or ID.
Symlinked or malformed CSV projections are reported as unavailable,
not as zero observations or verified project facts. Human decisions,
permissions, Drive synchronization and scientific validation still
require their existing independent checks. These are software tests,
**not** measured improvements in UX or scientific outcomes.


## REG-017: integrated evidence diagnosis (incremental)

The five-view presentation is unchanged: Evidence now includes the
read-only diagnostic produced by the REG-013 / REG-018 / REG-011 checks.
It is not another scientific state engine, separate dashboard or
additional canonical register. Human gates, safe next-step selection
and the C.A.D.A. four-column task table remain unchanged.

A diagnostic status of ASSESSED_LIMITED_SCOPE reports only bounded
structural observations; NOT_READY means the authorized input is
unavailable or incompatible. Missing counts remain null, never zero
or independently verified. Source passages, reviewer identities,
research text and internal paths are excluded.

MINIMAL displays at most two finding categories and one proposed
next action; FULL displays up to six categories and four actions.
The totals and underlying scientific state are identical in both
views. Plain text reports the same short diagnosis without an
additional interface.

A local read-only projection cannot establish a successful
Google Drive write or a verified remote receipt. No host action,
cloud write or scientific gate approval is simulated by this change.
User-interface and real researcher validation remain pending.
