# Governança científica — decisões, validação humana e snapshots

## Por que existe esta camada?

O C.A.D.A. responde muito bem:

> O que precisamos fazer agora?

A rastreabilidade responde:

> O que aconteceu durante a construção do artigo?

Faltavam três perguntas:

> Por que tomamos esta decisão?

> Em que momento o pesquisador humano assumiu explicitamente a responsabilidade por uma transição crítica?

> Qual era exatamente o estado oficial do projeto naquele momento?

O Meu Artigo responde a essas perguntas com três identificadores.

---

## DEC_ID — decisão científica

Um `DEC_ID` registra uma decisão que realmente muda o estudo.

Exemplo:

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

Não se cria DEC_ID para formatação, nome de arquivo ou pequenas escolhas administrativas.

---

## GATE_ID — validação humana crítica

A IA continua autônoma na rotina.

Ela **não pede aprovação a cada passo**.

Existem apenas sete gates padrão:

| Gate | Momento |
|---|---|
| `GATE-0001` | pergunta e contribuição |
| `GATE-0002` | método e protocolo |
| `GATE-0003` | estratégia de busca |
| `GATE-0004` | congelamento do corpus |
| `GATE-0005` | síntese / produto teórico |
| `GATE-0006` | claims / auditoria científica |
| `GATE-0007` | liberação para submissão |

Quando um gate fica `READY`, a Skill apresenta somente o que precisa de julgamento humano.

Exemplo:

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

Depois da aprovação, o sistema cria automaticamente um snapshot.

---

## SNAP_ID — estado científico congelado

Um `SNAP_ID` preserva a versão oficial do projeto em um marco.

Exemplos:

```text
SNAP-0001 — pergunta/contribuição aprovada
SNAP-0002 — protocolo congelado
SNAP-0003 — estratégia de busca congelada
SNAP-0004 — corpus congelado
SNAP-0005 — síntese aprovada
SNAP-0006 — claims aprovados
SNAP-0007 — versão liberada para submissão
```

Cada snapshot possui:

- arquivos canônicos;
- manifest SHA-256;
- gate que o originou;
- decisões relacionadas;
- CADA_IDs;
- resumo da mudança;
- vínculo com o snapshot anterior.

Assim é possível perguntar:

> O que mudou entre SNAP-0003 e SNAP-0004?

O script `compare_snapshots.py` responde quais arquivos foram adicionados, removidos ou alterados.

---

## Cadeia de custódia científica

Quando aplicável:

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

Não é obrigatório que todo objeto passe por todos os IDs.

A cadeia existe para reconstruir transições científicas materiais.

---

## Relatório para Revisor/Editor

O Meu Artigo pode gerar:

```text
RELATORIO_TRANSPARENCIA_<timestamp>.md
RELATORIO_TRANSPARENCIA_<timestamp>.json
```

O relatório contém apenas o que está registrado nos artefatos canônicos:

1. identidade do projeto;
2. desenho e protocolo;
3. buscas e corpus;
4. decisões científicas;
5. gates humanos;
6. snapshots;
7. evidências e claims;
8. uso substantivo de IA e validação humana;
9. exports W3C PROV / RO-Crate;
10. lacunas de rastreabilidade ainda abertas.

Ele não é um dump do workspace privado.

---

## Scripts

Registrar uma proposta (estado padrão PROPOSED, sem aprovação humana presumida):

```bash
python scripts/governance_events.py decision /projeto \
  --type METHOD \
  --question "Qual desenho metodológico?" \
  --decision "Revisão integrativa" \
  --rationale "..."
```

Para aprovar uma decisão, informar também `--status APPROVED`, `--decided-by` e `--evidence`, com referência à manifestação humana real.

Aprovar um gate:

```bash
python scripts/governance_events.py gate /projeto \
  --gate-id GATE-0002 \
  --decision APPROVED \
  --validated-by "Pesquisador" \
  --method "Revisão do protocolo e das strings" \
  --evidence "Referência à resposta real do pesquisador"
```

Ao aprovar um gate, o snapshot pós-gate é criado automaticamente.

### Justificativa formativa dos gates científicos

Para novos projetos, a aprovação dos gates GATE-0001 a GATE-0006 exige a explicação do próprio pesquisador sobre **por que escolheu aquele caminho** e **qual é uma limitação ou risco**. A Skill deve explicar a proposta antes, sem redigir a resposta que será atribuída ao pesquisador. Os campos são inseridos no mesmo comando com `--researcher-rationale` e `--researcher-limitation` e vinculados à manifestação humana original indicada em `--evidence`. O comando ilustrativo acima continua válido para projetos anteriores, sem o modo formativo habilitado; para projetos novos, complemente-o com essas duas opções. A documentação detalhada está em [Validação formativa](VALIDACAO-FORMATIVA.md).

O controle automático impede aprovações sem explicação minimamente substantiva; não constitui teste de compreensão ou prova da autoria humana.

Comparar snapshots:

```bash
python scripts/compare_snapshots.py SNAP_A SNAP_B
```

Gerar relatório:

```bash
python scripts/generate_transparency_report.py /projeto
```

---

## Regra anti-Frankenstein

Essa camada existe porque responde perguntas essenciais:

- O que foi decidido?
- Por que?
- Com base em quê?
- Quem validou?
- O que mudou?
- Qual era o estado oficial?

Se uma funcionalidade não melhora uma dessas respostas, ela não entra no núcleo.


## GATE-0006 — robustez dos claims

Antes da aprovação do GATE-0006, os claims materiais devem ser confrontados com:

- evidência favorável;
- evidência contrária;
- explicações alternativas;
- condições de contorno;
- dependência de uma única fonte;
- força da formulação;
- classificação [L]/[I]/[P].

Um claim pode ser ROBUST, QUALIFIED, REVISE, REJECT ou NOT_APPLICABLE.

QUALIFIED significa que a condição/limite precisa aparecer no manuscrito.

A aderência à revista pode ser verificada no mesmo gate quando houver revista-alvo, mas nunca pode justificar omitir evidência contrária.
