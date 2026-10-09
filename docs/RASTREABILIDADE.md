<a id="rastreabilidade-no-meu-artigo"></a>
# Traceability in My Article

<a id="ideia-central"></a>
## Central idea

My Article does not just seek to help you produce a manuscript.

It seeks to allow the researcher to **reconstruct how the manuscript was produced**.

In the age of AI, this means preserving the provenance of the process:

- which searches were performed;
- which files were used;
- what methodological decisions were made;
- what was changed and why;
- where AI participated;
- which tool/model was used when known;
- how the researcher verified the result;
- from which evidence the main statements derive.

<a id="gestão-não-é-rastreabilidade"></a>
## Management is not traceability

The project separates two functions:

<a id="cada-gestão"></a>
### C.A.D.A. — management

Answer:

> Where are we, what is missing, who is responsible, what is the deadline and what proves completion?

<a id="rastreabilidade-proveniência-científica"></a>
### Traceability — scientific provenance

Answer:

> How did we get here, what decisions constructed the article, with what sources/tools and how were they verified?

This avoids trying to use a simple to-do list as a methodological record.

<a id="três-níveis-de-controle"></a>
## Three levels of control

<a id="1-planilha-cada-modo-universal"></a>
### 1. C.A.D.A Spreadsheet. — universal mode

Does not require Trello, Jira or ClickUp.

The master matrix itself functions as the project manager.

The `11_CADA_Control` tab allows you to monitor:

- step;
- responsible;
- next action;
- term;
- status;
- priority;
- dependencies;
- locks;
- evidence of advancement;
- evidence of completion.

This is the **standard and universal** way of management.

<a id="2-gerenciador-externo-modo-opcional"></a>
### 2. External manager — optional mode

ClickUp, Jira/Atlassian and Trello can mirror C.A.D.A. for those who already use these tools.

The link is registered to `12_PM_Sync`.

The external manager never replaces the scientific matrix.

<a id="3-trilha-de-rastreabilidade-proveniência"></a>
### 3. Traceability trail — provenance

The `13_Traceability_Log` tab records material events of the scientific process.

The `14_AI_Use_Log` tab specifically records AI uses relevant for transparency and eventual editorial disclosure.

The `RASTREABILIDADE.md` file maintains a readable summary of the project construction.

<a id="o-que-fica-rastreável"></a>
## What is trackable

An example:

```text
Claim C-17
   ↓
Evidence E-31, E-48
   ↓
Records R-081, R-144
   ↓
Search S2-R1 / snowball SB-03
   ↓
TRACE-0118, TRACE-0121
   ↓
CADA-0054
   ↓
PROTOCOLO v3
```

Thus, an important claim can be linked to the evidence and process that led to its incorporation into the manuscript.

<a id="e-a-ia"></a>
## What about AI?

For material uses of AI, Skill seeks to record:

- platform/tool;
- model/version when available;
- purpose;
- scientific stage;
- input type;
- type of output;
- whether the use was assistive or noun;
- how the human review occurred;
- whether the result was accepted, changed or rejected;
- related artifacts;
- need for editorial declaration.

The goal is not to save every conversation or every prompt.

The rule is to record **events materially relevant to scientific construction**.

<a id="transparência-editorial"></a>
## Editorial transparency

This architecture is in line with a growing editorial trend to demand transparency about the use of AI in research.

The Revista de Ciências da Administração, for example, determines that substantive AI applications be described in the methods, with tool, version, purpose and human validation procedures, to ensure traceability.

Public editorial reference:

- Guidelines for using AI — Journal of Administration Sciences: https://periodicos.ufsc.br/index.php/adm/Diretrizes_para_uso_de_IA

<a id="limites-de-atribuição"></a>
## Assignment limits

Academic and editorial foundations must be linked to identifiable and verifiable sources. Statements attributed to undocumented lectures or presentations should not be recorded as quotations or confirmed evidence.

<a id="resultado-esperado"></a>
## Expected result

At the end of a project, it should be possible to answer:

> How was this article constructed?

without relying solely on the author's memory or chat history.This is the role of the My Article traceability layer.


<a id="interoperabilidade"></a>
## Interoperability

Traceability can also be exported in standardized formats:

- **W3C PROV-O** to represent entities, activities, agents and provenance relationships;
- **RO-Crate 1.3** to package the research object and its metadata;
- **SHA-256** to check the fixity of the package files.

This is an export layer. The researcher does not need to know these standards to use My Article.

See `../meu-artigo/references/provenance-export.md`.


<a id="decisão-responsabilidade-e-estado-congelado"></a>
## Decision, responsibility and frozen state

Traceability distinguishes:

- `DEC_ID`: why a scientific choice was made;
- `GATE_ID`: where the human researcher validated a critical transition;
- `SNAP_ID`: what was the official status of the project at that time.

This allows you to reconstruct not only what happened, but also decisions, human responsibility, and changes between versions.