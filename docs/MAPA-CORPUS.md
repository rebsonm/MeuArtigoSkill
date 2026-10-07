# Mapa do Corpus e Grounded Corpus Mode

## O que o Mapa do Corpus responde?

> Como o corpus validado está organizado?

Ele complementa a rastreabilidade e a matriz de evidências.

Não substitui o método da pesquisa e não transforma automaticamente o estudo em bibliometria.

A aba oficial é:

`20_MAPA_CORPUS`

Ela pode mostrar, quando os metadados reais permitirem:

- quantidade de registros retidos;
- CORE e SUPPORT;
- evolução por ano;
- autores recorrentes;
- periódicos/fontes;
- keywords e conceitos;
- cobertura de DOI/OpenAlex;
- estrutura de rede;
- clusters;
- artigos-ponte;
- warnings de cobertura.

Campos sem dados permanecem vazios. A Skill não inventa metadados para “completar” o mapa.

## Quando clusters podem aparecer?

Somente quando existe uma relação de rede real, por exemplo:

- citação;
- coautoria;
- acoplamento bibliográfico;
- cocitação;
- coocorrência de keywords.

Um agrupamento semântico sugerido por IA não deve ser apresentado como cluster bibliométrico sem essa base.

## Grounded Corpus Mode

O Grounded Corpus Mode responde outra pergunta:

> O que o corpus validado realmente sustenta?

Quando ativado, a IA trabalha somente sobre fontes elegíveis do corpus com full text efetivamente disponível.

Por padrão:

- `FULL TEXT — CORE`;
- `FULL TEXT — SUPPORT`.

A resposta deve apontar, quando disponível:

```text
afirmação
  ↳ Record_ID
  ↳ Evidence_ID
  ↳ locator
  ↳ [L] ou [I]
```

Se o corpus não sustentar a resposta, a Skill deve dizer isso.

Ela não pode completar silenciosamente com memória do modelo.

## Relação entre os dois

```text
CORPUS VALIDADO
      │
      ├── MAPA DO CORPUS
      │      "como ele se organiza?"
      │
      └── GROUNDED CORPUS
             "o que ele sustenta?"
```

## Proveniência

A geração do mapa e análises materiais no Grounded Corpus Mode entram na rastreabilidade.

Quando aplicável, registrar:

- TRACE_ID;
- SNAP_ID/corpus de entrada;
- Record_IDs;
- Evidence_IDs;
- fonte de enriquecimento;
- regras/algoritmos;
- AI_Use_ID;
- validação humana.

## Implementação

Gerar mapa em projeto local:

```bash
python scripts/build_corpus_map.py /caminho/do/projeto
```

Saídas:

```text
04_Evidencias_e_Sintese/
├── MAPA_CORPUS.json
└── MAPA_CORPUS.md
```

A aba `20_MAPA_CORPUS` é a visualização humana correspondente na matriz oficial.

## Regra anti-Frankenstein

O Meu Artigo não exige banco vetorial específico, OpenAlex, Zotero ou qualquer fornecedor de RAG.

Essas ferramentas podem ser usadas quando disponíveis.

O núcleo exige apenas:

- corpus elegível;
- proveniência;
- ligação com evidências;
- transparência sobre limites;
- validação humana para conclusões científicas materiais.
