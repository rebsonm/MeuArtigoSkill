<a id="cada-no-meu-artigo"></a>
# C.A.D.A. in Meu Artigo

<a id="para-que-serve"></a>
## What is it for

In Meu Artigo, the **C.A.D.A. It is the management layer of scientific work**.

It does not replace research method, integrative review, systematic review, protocol, analysis or evidence.

It organizes step by step so that the researcher knows, at any time:

- where the article is;
- what has already been done;
- what needs to happen next;
- who is responsible;
- what is the deadline;
- what is blocked;
- which evidence proves that a stage has advanced.

<a id="o-ciclo"></a>
## The cycle

<a id="c-capturar"></a>
### C — Capture

Record a unit of work when a verifiable action, decision, dependency, deadline, or block arises.

Examples:

- perform novelty audit;
- validate export from Web of Science;
- review BORDERLINE articles;
- get full text;
- review a section of the manuscript;
- meet a magazine requirement.

Each item is assigned a stable identifier:

`CADA-0001`, `CADA-0002`, ...

<a id="a-atribuir"></a>
### A — Assign

Set:

- responsible;
- scientific stage;
- priority;
- dependencies;
- related artifact;
- whether AI can perform alone or needs human decision.

<a id="d-definir-prazo"></a>
### D — Set deadline

Every active item must have a time expectation.

Meu Artigo distinguishes:

- **EXTERNAL** — actual term of magazine, congress, institution, etc.;
- **USER_SET** — deadline defined by the researcher;
- **INTERNAL_TARGET** — internal operational target;
- **DEPENDENCY** — depends on the completion of another item;
- **TO_DEFINE** — still needs to be defined.

This avoids turning an internal goal into an “official deadline”.

<a id="a-acompanhar"></a>
### A — Follow

The item remains tracked until:

- DONE;
- CANCELED;
- SUPERSEDED.

When possible, the conclusion needs evidence.

Examples:

- validated export file;
- updated protocol;
- created matrix line;
- full text stored;
- Evidence_ID created;
- proof of submission saved.

<a id="cada-não-significa-criar-um-cartão-para-cada-artigo-encontrado"></a>
## C.A.D.A. does not mean creating a card for each item found

Management works at a useful project level.

For example:

```text
CADA-0030 — Stage 07: Screening
  CADA-0031 — Triar registros novos da Scopus
  CADA-0032 — Rever BORDERLINE
  CADA-0033 — Rechecar amostra de exclusões
  CADA-0034 — Congelar contagens do screening
```

Individual bibliographic records remain in the screening/evidence tables.

<a id="dois-modos-de-gestão"></a>
## Two management modes

Meu Artigo works even for those who have never used a formal task management tool.

<a id="modo-1-planilha-cada-matrix_only"></a>
### Mode 1 — C.A.D.A Spreadsheet. (`MATRIX_ONLY`)

It is the universal and default mode. The official visual implementation is documented in [MATRIZ-CADA.md](./MATRIZ-CADA.md).

The master matrix itself functions as the project manager. The researcher tracks the stage, person responsible, next action, deadline, status, blocks and evidence directly in the spreadsheet.

The `15_CADA_Dashboard` tab offers a summary view for those who prefer not to work with detailed filters and tables.

<a id="modo-2-planilha-gerenciador-externo-matrix_plus_external"></a>
### Mode 2 — Spreadsheet + external manager (`MATRIX_PLUS_EXTERNAL`)

The same matrix remains canonical, but items can be mirrored in ClickUp, Jira or Trello.

This is a management convenience, not a requirement.

<a id="onde-fica-o-controle"></a>
## Where is the control

The master matrix contains:

<a id="11_cada_control"></a>
### `11_CADA_Control`

It is the main operational source.

Fields include:

- EACH_ID;
- title;
- scientific stage;
- responsible;
- next action;
- term;
- type of deadline;
- status;
- dependencies;
- blocking;
- evidence of advancement;
- evidence of conclusion;
- related artifact;
- external manager.

<a id="12_pm_sync"></a>
### `12_PM_Sync`

It's optional. May remain empty when the project uses the spreadsheet only.



Registers the correspondence between item C.A.D.A. and an external card/ticket/task.

Example:

```text
CADA-0042
Provider: Jira
External item: ART-31
Canonical status: IN_PROGRESS
External status: In Progress
Sync status: OK
```

<a id="15_cada_dashboard"></a>
### `15_CADA_Dashboard`

It is the management view of the spreadsheet.

It can show:- current scientific stage;
- number of active items;
- blocked items;
- expired items;
- upcoming deadlines;
- completion rate;
- next action;
- responsible;
- traceability gaps;
- substantive uses of AI not yet reviewed;
- health of the external synchronization, when it exists.

<a id="painel-em-continuidademd"></a>
## Panel in CONTINUIDADE.md

The continuity file contains a summary:

```text
## C.A.D.A. dashboard

Current stage:
Stage outcome required:

READY:
IN_PROGRESS:
WAITING/BLOCKED:

Hard deadlines:
Internal targets:

Next valid action:
CADA_ID:
Owner:
Due:

Recently completed:

Management sync:
Provider:
Container:
Last sync:
Conflicts:
```

This way, a new conversation can quickly understand where the work left off.

<a id="relação-com-rastreabilidade"></a>
## Relationship with traceability

C.A.D.A. manages the work. Traceability records how scientific work happened.

Therefore, in addition to `11_CADA_Control`, the project maintains:

- `13_Traceability_Log`;
- `14_AI_Use_Log`;
- `RASTREABILIDADE.md`.

A C.A.D.A. item can generate several traceability events.

Example:

```text
CADA-0042 — validar export WoS
  TRACE-0104 — export recebido
  TRACE-0105 — validação executada
  TRACE-0106 — erro de filtro detectado
  TRACE-0107 — novo export validado
```

See [TRACEABILITY.md](./RASTREABILIDADE.md).

<a id="integração-com-clickup-jira-ou-trello"></a>
## Integration with ClickUp, Jira or Trello

The Skill can use an external manager as an **operational mirror**.

It uses only one principal per article, unless the user explicitly requests another arrangement.

<a id="clickup"></a>
### ClickUp

You can use parent tasks for scientific steps and subtasks for C.A.D.A units.

<a id="jira-atlassian"></a>
### Jira / Atlassian

You can use an Epic for the article and Tasks/Stories with the identifier C.A.D.A.

<a id="trello"></a>
### Trello

You can use a board with lists like:

- Captured;
- Next action;
- In progress;
- Waiting/Blocked;
- Completed.

<a id="regra-de-ouro"></a>
## Rule of thumb

The card/ticket **is not scientific evidence**.

If a ticket is marked as Done, but the export has not been saved or the decision is not recorded in the protocol, the scientific step is not necessarily completed.

The source of truth remains the scientific workspace:

- `CONTINUIDADE.md`;
- protocol;
- Search Log;
- screening;
- full-text tracker;
- Evidence Matrix;
- Synthesis Log;
- Claims Ledger;
- `11_CADA_Control`.

The external manager serves to make the work visible and followable.

<a id="resultado-esperado"></a>
## Expected result

The Skill must be able to respond at any time:

> Where are we?

with something similar to:

```text
Current stage: 06 — Deduplicação

Concluído:
- buscas Scopus e WoS
- exports validados

Em andamento:
- CADA-0027 — consolidar corpus global

Bloqueado:
- nenhum

Próxima ação:
- CADA-0028 — revisar 14 near-duplicates

Prazo:
- meta interna: 09/10

Progress evidence:
- arquivo GLOBAL_DEDUP_v02.csv

Gerenciador:
- ClickUp — sincronizado
```

This vision is the main function of C.A.D.A. in Meu Artigo.