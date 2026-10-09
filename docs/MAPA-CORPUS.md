<a id="mapa-do-corpus-e-grounded-corpus-mode"></a>
# Corpus Map and Grounded Corpus Mode

<a id="o-que-o-mapa-do-corpus-responde"></a>
## What does the Corpus Map answer?

> How is the validated corpus organized?

It complements the traceability and evidence matrix.

It does not replace the research method and does not automatically transform the study into bibliometrics.

The official tab is:

`20_MAPA_CORPUS`

It can show, when the actual metadata allows:

- number of records retained;
- CORE and SUPPORT;
- evolution per year;
- recurring authors;
- periodicals/sources;
- keywords and concepts;
- DOI/OpenAlex coverage;
- network structure;
- clusters;
- bridge articles;
- coverage warnings.

Fields without data remain empty. The Skill does not invent metadata to “complete” the map.

<a id="quando-clusters-podem-aparecer"></a>
## When can clusters appear?

Only when there is a real network relationship, for example:

- quote;
- co-authorship;
- bibliographic coupling;
- cocitation;
- co-occurrence of keywords.

A semantic cluster suggested by AI should not be presented as a bibliometric cluster without this basis.

<a id="grounded-corpus-mode"></a>
## Grounded Corpus Mode

Grounded Corpus Mode answers another question:

> What does the validated corpus really support?

When activated, the AI ​​only works on eligible sources in the corpus with full text actually available.

By default:

- `FULL TEXT — CORE`;
- `FULL TEXT — SUPPORT`.

The answer should indicate, when available:

```text
afirmação
  ↳ Record_ID
  ↳ Evidence_ID
  ↳ locator
  ↳ [L] ou [I]
```

If the corpus does not support the answer, the Skill should say so.

It cannot complete silently with model memory.

<a id="relação-entre-os-dois"></a>
## Relationship between the two

```text
CORPUS VALIDADO
      │
      ├── MAPA DO CORPUS
      │      "como ele se organiza?"
      │
      └── GROUNDED CORPUS
             "o que ele sustenta?"
```

<a id="proveniência"></a>
## Provenance

Map generation and material analysis in Grounded Corpus Mode are included in traceability.

When applicable, record:

- TRACE_ID;
- SNAP_ID/input corpus;
- Record_IDs;
- Evidence_IDs;
- source of enrichment;
- rules/algorithms;
- AI_Use_ID;
- human validation.

<a id="implementação"></a>
## Implementation

Generate map in local project:

```bash
python scripts/build_corpus_map.py /caminho/do/projeto
```

Outputs:

```text
04_Evidencias_e_Sintese/
├── MAPA_CORPUS.json
└── MAPA_CORPUS.md
```

The `20_MAPA_CORPUS` tab is the corresponding human view in the official matrix.

<a id="regra-anti-frankenstein"></a>
## Anti-Frankenstein rule

My Article does not require a specific vector database, OpenAlex, Zotero or any RAG provider.

These tools can be used when available.

The core only requires:

- eligible corpus;
- provenance;
- connection with evidence;
- transparency about limits;
- human validation for material scientific conclusions.