<a id="governança-científica-decisões-validação-humana-e-snapshots"></a>
# Scientific governance — decisions, human validation and snapshots

<a id="por-que-existe-esta-camada"></a>
## Why does this layer exist?

The C.A.D.A. responds very well:

> What do we need to do now?

Traceability responds:

> What happened during the construction of the article?

Three questions were missing:

> Why did we make this decision?

> At what point did the human researcher explicitly assume responsibility for a critical transition?

> What exactly was the official status of the project at that time?

My Article answers these questions with three identifiers.

---

<a id="dec_id-decisão-científica"></a>
## DEC_ID — scientific decision

A `DEC_ID` records a decision that actually changes the study.

Example:

```text
DEC-0014

Pergunta decisória:
Qual desenho de revisão melhor responde ao objetivo?

Decisão:
Revisão integrativa.

Alternativas consideradas:
Revisão sistemática; scoping review.

Justificativa:
O objetivo exige síntese conceitual de literatura heterogênea.

Evidências relacionadas:
E-021; E-034

Impacto:
PROTOCOLO v3; estratégia de busca; screening.

Status:
FROZEN
```

DEC_ID is not created for formatting, file name or small administrative choices.

---

<a id="gate_id-validação-humana-crítica"></a>
## GATE_ID — critical human validation

AI remains autonomous in its routine.

She **doesn't ask for approval at every step**.

There are only seven default gates:

| Gate | Moment |
|---|---|
| `GATE-0001` | question and contribution |
| `GATE-0002` | method and protocol |
| `GATE-0003` | search strategy |
| `GATE-0004` | corpus freezing |
| `GATE-0005` | synthesis / theoretical product |
| `GATE-0006` | claims / scientific audit |
| `GATE-0007` | release for submission |

When a gate is `READY`, the Skill only presents what needs human judgment.

Example:

```text
GATE-0004 — Congelamento do corpus

Condição:
screening e full text encerrados
contagens reconciliadas
duplicatas resolvidas

Validar:
73 estudos elegíveis
12 CORE
61 SUPPORT
14 exclusões em full text

Decisão humana:
APPROVED
```

After approval, the system automatically creates a snapshot.

---

<a id="snap_id-estado-científico-congelado"></a>
## SNAP_ID — frozen scientific status

A `SNAP_ID` preserves the official version of the project in a milestone.

Examples:

```text
SNAP-0001 — pergunta/contribuição aprovada
SNAP-0002 — protocolo congelado
SNAP-0003 — estratégia de busca congelada
SNAP-0004 — corpus congelado
SNAP-0005 — síntese aprovada
SNAP-0006 — claims aprovados
SNAP-0007 — versão liberada para submissão
```

Each snapshot has:

- canonical files;
- manifest SHA-256;
- gate that originated it;
- related decisions;
- EACH_IDs;
- summary of the change;
- link with the previous snapshot.

So you can ask:

> What changed between SNAP-0003 and SNAP-0004?

The `compare_snapshots.py` script answers which files were added, removed, or changed.

---

<a id="cadeia-de-custódia-científica"></a>
## Scientific chain of custody

When applicable:

```text
DEC_ID
   ↓
CADA_ID
   ↓
TRACE_ID
   ↓
Record / Evidence / Synthesis / Claim
   ↓
GATE_ID
   ↓
SNAP_ID
   ↓
Manuscrito
   ↓
EXPORT_ID / RO-Crate
```

It is not mandatory that every object passes through all IDs.

The chain exists to reconstruct material scientific transitions.

---

<a id="relatório-para-revisoreditor"></a>
## Report to Reviewer/Editor

My Article can generate:

```text
RELATORIO_TRANSPARENCIA_<timestamp>.md
RELATORIO_TRANSPARENCIA_<timestamp>.json
```

The report contains only what is recorded in the canonical artifacts:

1. project identity;
2. design and protocol;
3. searches and corpus;
4. scientific decisions;
5. human gates;
6. snapshots;
7. evidence and claims;
8. substantive use of AI and human validation;
9. exports W3C PROV/RO-Crate;
10. traceability gaps still open.

It is not a dump of the private workspace.

---

<a id="scripts"></a>
## Scripts

Register a proposal (default state PROPOSED, no human approval assumed):

```bash
python scripts/governance_events.py decision /projeto \
  --type METHOD \
  --question "Qual desenho metodológico?" \
  --decision "Revisão integrativa" \
  --rationale "..."
```

To approve a decision, also inform `--status APPROVED`, `--decided-by` and `--evidence`, with reference to the real human manifestation.

Approve a gate:

```bash
python scripts/governance_events.py gate /projeto \
  --gate-id GATE-0002 \
  --decision APPROVED \
  --validated-by "Pesquisador" \
  --method "Revisão do protocolo e das strings" \
  --evidence "Referência à resposta real do pesquisador"
```

When approving a gate, the post-gate snapshot is automatically created.

<a id="justificativa-formativa-dos-gates-científicos"></a>
### Formative justification of scientific gates

For new projects, approval of gates GATE-0001 to GATE-0006 requires the researcher himself to explain **why he chose that path** and **what is a limitation or risk**. Skill must explain the proposal first, without writing the answer that will be attributed to the researcher. The fields are entered in the same command with `--researcher-rationale` and `--researcher-limitation` and linked to the original human manifestation indicated in `--evidence`. The illustrative command above remains valid for previous projects, without formative mode enabled; for new projects, complement it with these two options. Detailed documentation is in [Formative validation](VALIDACAO-FORMATIVA.md).Automatic control prevents approvals without a minimally substantive explanation; does not constitute a test of understanding or proof of human authorship.

Compare snapshots:

```bash
python scripts/compare_snapshots.py SNAP_A SNAP_B
```

Generate report:

```bash
python scripts/generate_transparency_report.py /projeto
```

---

<a id="regra-anti-frankenstein"></a>
## Anti-Frankenstein rule

This layer exists because it answers essential questions:

- What was decided?
- Why?
- Based on what?
- Who validated it?
- What changed?
- What was the official status?

If a feature doesn't improve one of these answers, it doesn't go into the core.


<a id="gate-0006-robustez-dos-claims"></a>
## GATE-0006 — robustness of claims

Before approval of GATE-0006, material claims must be compared with:

- favorable evidence;
- contrary evidence;
- alternative explanations;
- boundary conditions;
- dependence on a single source;
- strength of the formulation;
- classification [L]/[I]/[P].

A claim can be ROBUST, QUALIFIED, REVISE, REJECT or NOT_APPLICABLE.

QUALIFIED means that the condition/threshold needs to appear in the manuscript.

Adherence to the magazine can be checked at the same gate when there is a target magazine, but it can never justify omitting contrary evidence.