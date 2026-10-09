<a id="interoperabilidade-w3c-prov-ro-crate-e-sha-256"></a>
# Interoperability — W3C PROV, RO-Crate and SHA-256

<a id="o-que-isso-muda-para-quem-usa-o-meu-artigo"></a>
## What does this change for those who use My Article?

Almost nothing in the routine.

The researcher continues to work with:

- Panel;
- C.A.D.A.;
- timeline;
- protocol;
- searches;
- evidence;
- claims;
- record of AI usage.

Interoperability appears when the project needs to be **audited, preserved, shared or submitted**.

The Skill can then generate a standardized package.

<a id="o-pacote-auditável"></a>
## The auditable package

Example:

```text
RO_CRATE_meu-projeto_20261007T030000Z/
├── ro-crate-metadata.json
├── manifest-sha256.txt
├── provenance/
│   ├── prov.jsonld
│   ├── provenance-report.json
│   └── PROVENANCE_REPORT.md
└── payload/
    ├── 00_Gestao_e_Continuidade/
    │   ├── CONTINUIDADE.md
    │   ├── PROTOCOLO.md
    │   ├── RASTREABILIDADE.md
    │   ├── MATRIZ_MESTRA_*.xlsx
    │   └── logs e matrizes
    ├── 05_Manuscrito/
    └── 06_Submissao/
```

By default, the full text corpus is not included because it may contain files protected by license or copyright.

<a id="w3c-prov-o"></a>
## W3C PROV-O

W3C PROV is used to express provenance in an interoperable way.

In My Article:

| My Article | PROV |
|---|---|
| EACH_ID | context/plan |
| TRACE_ID | Activity |
| Search_ID | Activity |
| Record_ID | Entity |
| Evidence_ID | Entity |
| claim_ID | Entity |
| researcher | Agent |
| AI/script | Agent |

Examples of relationships:

```text
Claim
   wasDerivedFrom
Evidence

Record
   wasGeneratedBy
Search

Arquivo
   wasGeneratedBy
TRACE activity

TRACE
   wasAssociatedWith
Pesquisador / IA / script
```

Official reference:

https://www.w3.org/TR/prov-o/

<a id="ro-crate-13"></a>
## RO-Crate 1.3

RO-Crate packages the search object and its metadata in JSON-LD.

The main file is:

`ro-crate-metadata.json`

My Article uses version 1.3:

https://w3id.org/ro/crate/1.3

The package root is represented as `Dataset`, and files are referenced by `hasPart`.

The W3C PROV file is inside the RO-Crate itself.

<a id="sha-256"></a>
##SHA-256

The package also includes:

`manifest-sha256.txt`

Each file is given a SHA-256 hash.

If any byte of the file changes, the hash changes.

This allows you to check **fixity**: whether the package remains exactly the same as it was exported.

Fixity does not prove that the research is correct. It only helps demonstrate that the files have not been changed since the manifest was generated.

<a id="relatório-de-proveniência"></a>
## Provenance report

The export produces a report with:

- number of TRACE events;
- number of PROV entities;
- PROV activities;
- PROV agents;
- files in RO-Crate;
- claims without Evidence_ID;
- C.A.D.A. completed without evidence of completion;
- substantive use of AI awaiting human validation;
- search performed without literal string;
- other gaps detected.

<a id="registro-na-planilha"></a>
## Record in spreadsheet

The spreadsheet has the tab:

`16_INTEROPERABILIDADE`

Each export receives an ID:

`EXPORT-0001`

And records:

- date/time;
- patterns;
- path/URL;
- SHA-256 of the package;
- validation status;
- PROV counts;
- number of RO-Crate files;
- warnings.

<a id="scripts"></a>
## Scripts

Generate:

```bash
python scripts/export_provenance.py /caminho/ARTIGO_projeto_2026
```

Validate:

```bash
python scripts/validate_provenance_package.py /caminho/RO_CRATE_projeto.zip
```

By default, the package is saved in:

`06_Submissao/Arquivos_Finais/`

<a id="quando-gerar"></a>
## When to generate?

It is not necessary to generate with each action.

Useful moments:

- frozen protocol;
- frozen corpus;
- synthesis completed;
- frozen version of the manuscript;
- before submission;
- after submission;
- when reviewer/editor requests transparency;
- when the researcher wants an auditable snapshot.

<a id="o-que-isso-permite-afirmar"></a>
## What does this allow us to say?

It allows us to state that the project has a **standardized and interchangeable provenance trail**.

It does not automatically allow us to state that the study is:

- valid;
- reproducible in the strict sense;
- error free;
- methodologically correct.

These remain scientific questions.

<a id="princípio-do-meu-artigo"></a>
## Principle of My Article

The human interface can remain simple:

```text
Painel → C.A.D.A. → Rastreabilidade
```

Underneath:

```text
TRACE / Evidence / Claim
        ↓
     W3C PROV
        ↓
     RO-Crate
        ↓
SHA-256 / pacote auditável
```

The technical complexity lies with the Skill, not the researcher.


<a id="compartilhamento-e-sigilo"></a>
## Sharing and confidentialityThe full export must remain in public `PRIVATE` as it contains records
internal and may reveal confidential information. The audiences `PUBLIC` and
`COLLABORATIVE` remove individual names and events, and the second only accepts files
textual texts authorized one by one and linked by SHA-256. Cryptographic integrity
does not mean anonymization or authorization for publication. Consult
[secure export](EXPORTACAO-SEGURA.md) before sharing files.