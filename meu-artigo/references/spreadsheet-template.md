# Canonical spreadsheet template — Meu Artigo

## Role

The canonical spreadsheet is not a fallback. It is the default management and traceability interface of Meu Artigo.

Default mode:

`MATRIX_ONLY`

Optional extension:

`MATRIX_PLUS_EXTERNAL`

The same workbook supports both.

## User experience

A researcher should be able to open the workbook and answer in seconds:

- Onde estamos?
- O que faço agora?
- O que está bloqueado?
- Qual é o prazo?
- Como chegamos aqui?
- Qual evidência sustenta a afirmação?
- Onde a IA participou?
- Como essa participação foi validada?

## Canonical visible sheets

Use these exact sheet names and order:

1. `00_PAINEL`
2. `01_CADA`
3. `02_LINHA_TEMPO`
4. `03_PROJETO`
5. `04_EVIDENCIAS`
6. `05_PROTOCOLO`
7. `06_BUSCAS`
8. `07_SCREENING`
9. `08_FULL_TEXT`
10. `09_MATRIZ_EVID`
11. `10_SINTESE`
12. `11_CLAIMS`
13. `12_USO_IA`
14. `13_SUBMISSAO`
15. `14_PM_SYNC`
16. `15_CONFIG`
17. `16_INTEROPERABILIDADE`

Do not rename these sheets without a migration step because formulas and agents rely on them.

## 00_PAINEL

Purpose: executive research-governance cockpit.

Top block:

- project title;
- current scientific stage;
- management mode;
- external manager;
- last update.

KPI cards:

- C.A.D.A. completion rate;
- active items;
- blocked items;
- overdue items.

Next-action block:

- CADA_ID;
- next action;
- owner;
- due.

Traceability/AI block:

- DONE items with completion evidence;
- number of TRACE events;
- substantive AI uses reviewed;
- verified claims.

Alerts:

- external deadlines in next 30 days;
- blocked items;
- substantive AI use pending human review;
- claims not verified.

Questions block:

- Onde estamos? → stage + C.A.D.A.
- O que faço agora? → next action.
- Como chegamos aqui? → `02_LINHA_TEMPO`.
- Qual é a evidência? → `09_MATRIZ_EVID` / `11_CLAIMS`.
- Onde a IA participou? → `12_USO_IA`.

Include a C.A.D.A. status chart and a 00–14 stage roadmap.

## 01_CADA

Columns:

```text
CADA_ID
Etapa
Tarefa
Responsável
Próxima ação
Prazo
Tipo de prazo
Status
Prioridade
Dependências
Bloqueio
Evidência de avanço
Evidência de conclusão
Artefato relacionado
Última atualização
Trace_IDs
PM Provider
External Item ID
Observações
```

Controlled values:

Status:
- CAPTURED
- ASSIGNED
- READY
- IN_PROGRESS
- WAITING
- BLOCKED
- DONE
- CANCELLED
- SUPERSEDED

Priority:
- BAIXA
- MÉDIA
- ALTA
- CRÍTICA

Deadline type:
- EXTERNAL
- USER_SET
- INTERNAL_TARGET
- DEPENDENCY
- TO_DEFINE

Provider:
- NONE
- CLICKUP
- JIRA
- TRELLO
- OTHER

Formatting:

- DONE: green;
- BLOCKED: red;
- IN_PROGRESS: blue;
- READY: amber;
- CRÍTICA: red;
- overdue nonterminal deadline: red.

Freeze header + first three columns.

## 02_LINHA_TEMPO

This is the readable traceability log.

Columns:

```text
Trace_ID
Timestamp
Etapa
CADA_ID
Ator
Ferramenta / IA
Modelo / versão
Tipo de ação
Resumo da ação
Entrada / Fonte
Decisão / Saída
Justificativa
Artefato antes
Artefato depois
Método de verificação
Validação humana
IDs relacionados
Materialidade
Status
Observações
```

Actor:
- HUMAN
- AI
- HUMAN+AI
- DATABASE
- SCRIPT
- EXTERNAL_REVIEWER
- EDITOR
- OTHER

Materiality:
- ASSISTIVE
- SUBSTANTIVE
- ADMINISTRATIVE
- NOT_APPLICABLE

## 03_PROJETO

Columns:

`Campo | Valor | Status | Última atualização`

Required rows:

- Título curto do projeto
- Problema original
- Pergunta atual
- Objetivo
- Contribuição pretendida
- Desenho metodológico
- Escopo e exclusões
- Revista-alvo
- Idiomas
- Período de busca
- Etapa atual
- Modo de gestão
- Gerenciador externo
- Rastreabilidade habilitada

The original problem is preserved verbatim.

## 04_EVIDENCIAS

High-level evidence map.

Columns:

```text
Evidence_ID
Fonte / Citação
Conceito / Categoria
Achado / contribuição
Papel
Força / relevância
Claim_IDs
Locator / trecho
Status
Observações
```

This is a user-facing summary, not a replacement for `09_MATRIZ_EVID`.

## 05_PROTOCOLO

Columns:

`Item | Decisão | Justificativa | Status | Versão | Atualizado em | Trace_ID`

Never silently overwrite an executed/frozen methodological decision. Version it.

## 06_BUSCAS

Columns:

```text
Search_ID
Data
Base / Fonte
Blocos conceituais
String literal
Filtros
Encontrados
Exportados
Arquivo / URL
Status
Iteração
Trace_ID
Validação
Observações
```

Literal executed strings are immutable.

## 07_SCREENING

Columns:

```text
Record_ID
Fonte
Search_ID
Título
Autores
Ano
DOI / ID
Resumo
Tipo
Idioma
Pass1
Motivo Pass1
Pass2
Motivo Pass2
Duplicata
Canonical_ID
Trace_ID
Observações
```

Pass 1:
- INCLUDE
- BORDERLINE
- EXCLUDE

Pass 2:
- FULL TEXT — CORE
- FULL TEXT — SUPPORT
- EXCLUDE

## 08_FULL_TEXT

Columns:

```text
Record_ID
Prioridade
Status full text
Versão acessada
Fonte de acesso
Data de acesso
Decisão
Motivo exclusão
Evidence_ID
Arquivo / URL
Observações
```

Absence of access is not scientific exclusion.

## 09_MATRIZ_EVID

Detailed evidence matrix:

```text
Evidence_ID
Citação
DOI / ID
Conceito
Definição / claim
Problema / tensão
Mecanismo / achado
Desenho / tipo de fonte
Amostra / dados
Contexto
Processo / etapa
Atores / papéis
Ação / decisão
Evidência observável
Condições de contorno
Limitações
Transferibilidade
Papel / força
Locator
Rótulo epistêmico
Observações
```

Epistemic labels:
- [L]
- [I]
- [P]

## 10_SINTESE

Columns:

```text
Synthesis_ID
Tema / Categoria
Evidence_IDs
Padrão entre fontes
Contradições
Condições de contorno
Inferência
Status epistêmico
Decisão
Claim_IDs
Trace_ID
```

## 11_CLAIMS

Columns:

```text
Claim_ID
Seção do manuscrito
Claim / afirmação
Tipo
Evidence_IDs
Locators
Trace_IDs
Força
Verificação
Status de redação
Observações
```

Claim type:
- LITERATURE
- INFERENCE
- PROPOSITION
- EMPIRICAL_RESULT

The goal is backward traceability from manuscript to evidence and process provenance.

## 12_USO_IA

Columns:

```text
AI_Use_ID
Data
Etapa
CADA_ID
Trace_ID
Plataforma / ferramenta
Modelo / versão
Finalidade
Categoria de entrada
Categoria de saída
Materialidade
Método de revisão humana
Decisão humana
Aceito / modificado / rejeitado
Artefatos relacionados
Disclosure necessário
Texto / nota de disclosure
Observações
```

Substantive use must not be treated as validated until a real human review method is recorded.

## 13_SUBMISSAO

Columns:

`Item | Requisito | Fonte do requisito | Status | Prazo | Evidência / arquivo | Trace_ID | Observações`

Preserve the exact submitted version and receipt/identifier.

## 14_PM_SYNC

Optional. Can remain empty in MATRIX_ONLY.

Columns:

```text
CADA_ID
Provider
Workspace / site
Container ID
External item ID
External URL
Status externo
Responsável externo
Prazo externo
Status canônico
Responsável canônico
Prazo canônico
Último push
Último pull
Sync status
Conflito
Observações
```

The external task manager never becomes scientific source of truth.

## 15_CONFIG

Store:

- controlled vocabularies;
- stage map;
- status definitions;
- deadline types;
- actor vocabulary;
- AI materiality vocabulary;
- management modes;
- provider list.

This sheet may be hidden/protected by the platform when appropriate, but must remain accessible to the agent.

## Visual design

Reference palette:

- navy: `#17324D`
- teal: `#1F6E6A`
- blue: `#2D6CDF`
- light blue: `#EAF2FF`
- light gray: `#F4F6F8`
- green: `#2E7D32`
- light green: `#EAF5EA`
- amber: `#B7791F`
- light amber: `#FFF5D9`
- red: `#B42318`
- light red: `#FDECEC`
- purple: `#6B4FA1`
- light purple: `#F2ECFA`

Use professional, restrained formatting. Do not make scientific state depend on color alone.

## Formula logic

The dashboard should derive, not manually type:

- completion rate = DONE / nonempty CADA_ID;
- active = READY + IN_PROGRESS + WAITING + BLOCKED;
- blocked = BLOCKED;
- overdue = deadline < today and status nonterminal;
- next action = first IN_PROGRESS, else first READY;
- trace-event count;
- substantive AI uses reviewed / total substantive AI uses;
- verified claims / total claims;
- external deadlines in next 30 days;
- substantive AI uses pending review.

If formula support differs across spreadsheet platforms, preserve the calculation logic even if syntax changes.

## Generation priority

When starting a new project:

1. create the canonical spreadsheet before large searches;
2. populate `03_PROJETO`;
3. seed CADA-0001 through CADA-0003;
4. seed TRACE-0001;
5. set management mode to MATRIX_ONLY unless external management is intentionally enabled;
6. show the user `00_PAINEL` first;
7. update the matrix continuously rather than retrospectively.

## Platform implementation

Preferred:

- native Google Sheet when Google Sheets/Drive write access exists;
- native equivalent in another connected spreadsheet system;
- official XLSX generator when local spreadsheet tooling is available;
- CSV mirrors only as a last-resort compatibility mode.

Read `scripts/build_matrix_template.py` for the reference XLSX implementation.


## 16_INTEROPERABILIDADE

Purpose: log machine-readable provenance exports.

Columns:

```text
Export_ID
Timestamp
Padrões
Pacote / URL
SHA-256 do pacote
Validação
TRACE events
PROV entities
PROV activities
PROV agents
RO-Crate files
Warnings
Observações
```

Use stable `EXPORT-####` IDs.

Each W3C PROV / RO-Crate export should create one row. In local-project mode, synchronize this sheet with `00_Gestao_e_Continuidade/16_Interoperabilidade.csv`.

The sheet is an export history, not the provenance graph itself. The graph lives in the generated package.
