# Native visual dashboard in ChatGPT (Skill-only pilot)

The researcher can use **Meu Artigo as a Skill** and ask the assistant to
display a visual research dashboard inside the chat. This does **not**
require adopting a custom MCP plugin or hosting any server.

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

For a strictly read-only local/Work projection, without deploying MCP:

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

The optional **MCP Apps** implementation in
[PR #22](https://github.com/rebsonm/MeuArtigoSkill/pull/22)
remains untouched and unmerged. It is a more deeply customized interface
that requires a connected compatible MCP service. This Skill-native
pilot is independent: users do not need that PR to see ordinary charts,
tables, cards and research status messages in an environment that can
render those natively. Neither option replaces the Skill.

## Status and validation limits

This branch is a software **pilot**. The local projection has synthetic
regression tests. No claims are made of installing the changed Skill in a
user account, running a live ChatGPT host compatibility test, or verifying
Drive sync or empirical usability. Separate setup and research review
are still required for these claims.
