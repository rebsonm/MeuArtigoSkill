# Journal-aware construction

## Principle

When a target journal is known, Meu Artigo should construct the manuscript **for that scientific destination from the beginning**, rather than write a generic article and format it only at the end.

This affects presentation, manuscript architecture, dialogue with the journal, required declarations, and submission artifacts.

It must **not** distort scientific evidence, change results to fit editorial expectations, or retroactively modify methodological rules because of observed findings.

## Intake question

At project intake, ask one concise question:

> Do you already have a target journal? If yes, send the official author-guidelines link/file and the journal template/layout, if one exists.

Accepted inputs include:

- official author-guidelines URL;
- official PDF/DOCX with submission rules;
- official manuscript template;
- official checklist;
- journal aims & scope;
- relevant editorial policy pages.

Prefer official journal/publisher sources over third-party summaries.

If the user has no target journal, do not block the project. Record:

```text
construction_mode = JOURNAL_NEUTRAL
target_journal = TO_DEFINE
```

Continue the scientific workflow normally.

## Canonical artifact

When a target journal is defined, maintain:

`06_Submissao/Regras_da_Revista/JOURNAL_PROFILE.json`

Optionally also maintain a human-readable:

`06_Submissao/Regras_da_Revista/JOURNAL_PROFILE.md`

### Canonical JSON structure

```json
{
  "schema_version": "1.0",
  "status": "TO_DEFINE | PENDING_RULES | LOADED | VERIFIED | SUPERSEDED",
  "construction_mode": "JOURNAL_NEUTRAL | JOURNAL_AWARE_PENDING_PROFILE | JOURNAL_AWARE",
  "journal_name": "",
  "journal_url": "",
  "guidelines_source": "",
  "template_source": "",
  "rules_verified_at": "",
  "official_rules_verified": false,
  "article_type": "",
  "formal_contract": {
    "word_or_page_limit": "",
    "section_requirements": [],
    "abstract_rules": "",
    "keyword_rules": "",
    "reference_style": "",
    "tables_figures_rules": "",
    "anonymization_rules": "",
    "title_page_rules": "",
    "cover_letter": "",
    "highlights": "",
    "graphical_abstract": "",
    "supplementary_material": "",
    "ai_policy": "",
    "data_policy": "",
    "orcid": "",
    "credit_taxonomy": "",
    "conflicts_of_interest": "",
    "funding_statement": "",
    "ethics_statement": "",
    "fees": "",
    "file_formats": "",
    "other_requirements": []
  },
  "scientific_profile": {
    "aims_scope": "",
    "contribution_profile": "",
    "common_article_genres": "",
    "journal_dialogue_notes": "",
    "recent_relevant_articles": []
  },
  "planning": {
    "provisional_section_budget": {},
    "required_submission_artifacts": []
  },
  "source_files_or_urls": [],
  "notes": ""
}
```

Never fill an unknown field by guessing.

## Two layers

### 1. Formal editorial contract

Derived from official submission rules and templates:

- length;
- required sections;
- abstract/keywords;
- references;
- tables/figures;
- anonymization;
- title page;
- declarations;
- AI/data policies;
- required files;
- fees and file formats when relevant.

Populate the submission checklist from this layer.

### 2. Scientific/editorial profile

Derived from aims & scope, editorials, and recent relevant articles when the user wants journal-fit analysis:

- scope;
- expected contribution style;
- recurring debates;
- article genres;
- journal-specific scientific dialogue.

Keep this separate from mandatory formal rules.

## Construction behavior

When `construction_mode = JOURNAL_AWARE`:

- adapt manuscript structure to the allowed/required section architecture;
- maintain a word/page budget when a real journal constraint exists;
- reserve space for required declarations and supplementary artifacts;
- shape the journal-dialogue analysis around the outlet's actual scope and published conversation;
- use the journal's reference and anonymization rules during drafting, not only at final formatting;
- keep `13_SUBMISSAO` synchronized with the formal contract.

Do not use universal word percentages as if they were journal rules. Any section budget that is not explicitly imposed by the journal must be marked as a planning estimate.

## Scientific non-interference boundary

Journal awareness may change:

- presentation;
- manuscript architecture;
- terminology appropriate to the field;
- length allocation;
- dialogue with the outlet;
- submission artifacts.

Journal awareness must not change merely to improve acceptance odds:

- empirical or review findings;
- inclusion/exclusion decisions after seeing outcomes;
- evidence strength;
- contradictory evidence;
- methodological facts;
- uncertainty;
- limitations.

If the target journal changes, record a material `DEC_ID` of type JOURNAL when the change affects scientific presentation. Rebuild the journal profile and submission checklist, but do not rewrite the scientific record.

## Timing

If the journal is known at intake, load the profile before substantive manuscript construction.

If no journal is known, proceed in `JOURNAL_NEUTRAL` mode. Before full manuscript consolidation, prompt the user to define a target journal when appropriate.

A journal can be selected later without invalidating prior scientific work.

## Versioning and traceability

Record a TRACE event when:

- a profile is first created;
- official rules are re-verified;
- the journal changes;
- a materially changed template/guideline is loaded.

Preserve superseded profiles in project history when rules materially change.

Record the source and verification date. Do not state that rules are current without actually checking the supplied or official source.

## Relationship to existing artifacts

Do not create a new workbook tab.

Use:

- `03_PROJETO` — target journal, construction mode, profile status;
- `06_Journal_Dialogue.csv` — scientific dialogue with the target outlet;
- `10_Submission_Checklist.csv` / `13_SUBMISSAO` — formal requirements and compliance;
- `17_DECISOES` — material journal-selection/change decisions;
- `CONTINUIDADE.md` — current target/profile status.

The journal profile is a canonical source document, not another management system.
