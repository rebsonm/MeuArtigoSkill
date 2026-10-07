# C.A.D.A. no Meu Artigo

## Para que serve

No Meu Artigo, o **C.A.D.A. é a camada de gestão do trabalho científico**.

Ele não substitui método de pesquisa, revisão integrativa, revisão sistemática, protocolo, análise ou evidência.

Ele organiza o passo a passo para que o pesquisador saiba, a qualquer momento:

- onde o artigo está;
- o que já foi feito;
- o que precisa acontecer depois;
- quem é responsável;
- qual é o prazo;
- o que está bloqueado;
- qual evidência comprova que uma etapa avançou.

## O ciclo

### C — Capturar

Registrar uma unidade de trabalho quando surge uma ação, decisão, dependência, prazo ou bloqueio verificável.

Exemplos:

- executar auditoria de novidade;
- validar export da Web of Science;
- rever artigos BORDERLINE;
- obter full text;
- revisar uma seção do manuscrito;
- atender uma exigência da revista.

Cada item recebe um identificador estável:

`CADA-0001`, `CADA-0002`, ...

### A — Atribuir

Definir:

- responsável;
- etapa científica;
- prioridade;
- dependências;
- artefato relacionado;
- se a IA pode executar sozinha ou precisa de decisão humana.

### D — Definir prazo

Todo item ativo deve ter uma expectativa temporal.

O Meu Artigo distingue:

- **EXTERNAL** — prazo real de revista, congresso, instituição etc.;
- **USER_SET** — prazo definido pelo pesquisador;
- **INTERNAL_TARGET** — meta operacional interna;
- **DEPENDENCY** — depende da conclusão de outro item;
- **TO_DEFINE** — ainda precisa ser definido.

Isso evita transformar uma meta interna em “prazo oficial”.

### A — Acompanhar

O item permanece acompanhado até:

- DONE;
- CANCELLED;
- SUPERSEDED.

Quando possível, a conclusão precisa de evidência.

Exemplos:

- arquivo de export validado;
- protocolo atualizado;
- linha da matriz criada;
- full text armazenado;
- Evidence_ID criado;
- comprovante de submissão salvo.

## C.A.D.A. não significa criar um cartão para cada artigo encontrado

A gestão trabalha em nível útil de projeto.

Por exemplo:

```text
CADA-0030 — Etapa 07: Screening
  CADA-0031 — Triar registros novos da Scopus
  CADA-0032 — Rever BORDERLINE
  CADA-0033 — Rechecar amostra de exclusões
  CADA-0034 — Congelar contagens do screening
```

Os registros bibliográficos individuais continuam nas tabelas de screening/evidência.

## Onde fica o controle

A matriz-mestra contém:

### `11_CADA_Control`

É a fonte operacional principal.

Campos incluem:

- CADA_ID;
- título;
- etapa científica;
- responsável;
- próxima ação;
- prazo;
- tipo de prazo;
- status;
- dependências;
- bloqueio;
- evidência de avanço;
- evidência de conclusão;
- artefato relacionado;
- gerenciador externo.

### `12_PM_Sync`

Registra a correspondência entre o item C.A.D.A. e um card/ticket/tarefa externa.

Exemplo:

```text
CADA-0042
Provider: Jira
External item: ART-31
Canonical status: IN_PROGRESS
External status: In Progress
Sync status: OK
```

## Painel em CONTINUIDADE.md

O arquivo de continuidade contém um resumo:

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

Assim, uma conversa nova pode entender rapidamente onde o trabalho parou.

## Integração com ClickUp, Jira ou Trello

A Skill pode usar um gerenciador externo como **espelho operacional**.

Ela usa apenas um principal por artigo, salvo se o usuário pedir explicitamente outro arranjo.

### ClickUp

Pode usar tarefas-pai para etapas científicas e subtarefas para unidades C.A.D.A.

### Jira / Atlassian

Pode usar um Epic para o artigo e Tasks/Stories com o identificador C.A.D.A.

### Trello

Pode usar um board com listas como:

- Capturado;
- Próxima ação;
- Em andamento;
- Aguardando/Bloqueado;
- Concluído.

## Regra de ouro

O card/ticket **não é a evidência científica**.

Se um ticket estiver marcado como Done, mas o export não foi salvo ou a decisão não está registrada no protocolo, a etapa científica não está necessariamente concluída.

A fonte de verdade continua sendo o workspace científico:

- `CONTINUIDADE.md`;
- protocolo;
- Search Log;
- screening;
- full-text tracker;
- Evidence Matrix;
- Synthesis Log;
- Claims Ledger;
- `11_CADA_Control`.

O gerenciador externo serve para tornar o trabalho visível e acompanhável.

## Resultado esperado

A Skill deve conseguir responder a qualquer momento:

> Onde estamos?

com algo semelhante a:

```text
Etapa atual: 06 — Deduplicação

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

Evidência de avanço:
- arquivo GLOBAL_DEDUP_v02.csv

Gerenciador:
- ClickUp — sincronizado
```

Essa visão é a principal função do C.A.D.A. no Meu Artigo.
