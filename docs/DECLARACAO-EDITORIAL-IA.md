<a id="declaração-editorial-de-uso-de-ia"></a>
# AI Usage Editorial Statement

My Article exclusively uses the events recorded in `14_AI_Use_Log.csv` to prepare the editorial statement. Skill cannot reconstruct an imagined history, invent tools, assign human review without real feedback, or present the text as approved by the magazine.

<a id="política-específica-do-periódico"></a>
## Periodical specific policy

In `06_Submissao/Regras_da_Revista/JOURNAL_PROFILE.json`, the `ai_disclosure_policy` object records: `status=VERIFIED`, `source` official, `verified_at`, `statement_location`, `category_rules` by category, and, when applicable, `require_model_version`. The allowed decisions are `ALLOWED`, `PROHIBITED`, and `EDITORIAL_REVIEW`. Any missing or prohibitive rule blocks the final declaration. The old field `ai_policy` is not equivalent to a checked policy.

The `ai_disclosure_attestation` object requires a real statement from the researcher about the completeness of the log, date, authorship, response reference and exact SHA-256 of the CSV. An empty log does not in itself prove that no AI was used.

<a id="uso-da-tabela-existente"></a>
## Use of existing table

The `12_USO_IA` tab and the `14_AI_Use_Log.csv` file add three columns without creating new tabs or IDs: `Disclosure_category`, `Human_review_evidence` and `Confidentiality_review`. The categories: ADMIN_SUPPORT, LITERATURE_SEARCH, SCREENING, EVIDENCE_EXTRACTION, DATA_ANALYSIS, DRAFTING_EDITING, FIGURES and OTHER.

For substantive events, report human review and your actual reference. A `Disclosure_required=NO` does not overcome journal policy. Do not include full prompts, restricted text or personal data in the public statement.

<a id="comandos"></a>
## Commands

```bash
python scripts/editorial_ai_disclosure.py audit /projeto
python scripts/editorial_ai_disclosure.py draft /projeto
python scripts/editorial_ai_disclosure.py final /projeto
python scripts/editorial_ai_disclosure.py verify-final /projeto
```

The draft may have pending issues; the final is only issued after reconciliation and policy verified. It is located at `06_Submissao/Regras_da_Revista/AI_DISCLOSURE_FINAL.md`, associated with the report with hashes `00_Gestao_e_Continuidade/AI_DISCLOSURE_AUDIT.json`. `GATE-0007` revalidates both.

The final text is a proposal for placement in the manuscript and letter, not evidence of submission. Skill cannot authenticate people, automatically confirm that all AI use has been recorded, or guarantee editorial acceptance.

<a id="versão-breve-para-o-periódico"></a>
## Short version for the journal

The concise statement only aggregates tools and purposes that are in the actual records; the full audit remains accessible for review. The text limit corresponds to **an approximate editorial page** and does not guarantee an A4 sheet in any format. If the material exceeds the limit, the generator does not silently omit events: it advises reviewing the writing while keeping the full record.

```bash
python scripts/editorial_ai_disclosure.py compact /projeto
python scripts/editorial_ai_disclosure.py compact-final /projeto
```

`compact` produces drafts even with pending issues (clearly flagged); `compact-final` requires a complete validated declaration, verified journal rules, and history-linked human attestation. The final brief statement is integrity hashed in the audit report and its subsequent change invalidates the check. Do not confuse the prepared text with submission accepted by the magazine.

<a id="referências-gerais"></a>
## General references

- ICMJE, `https://www.icmje.org/recommendations/browse/artificial-intelligence/`
- COPE, `https://doi.org/10.24318/cCVRZBms`

These guidelines do not replace the official rules of each magazine. You should not attribute authorship to an AI, nor assume that human review was effective because there is a filled column. Anonymization controls and the legal use of PDFs remain mandatory. No paid service required.