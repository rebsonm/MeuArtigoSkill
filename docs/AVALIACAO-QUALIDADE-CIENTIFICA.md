<a id="benchmark-de-qualidade-científica-calibração-pública-e-comparação-reproduzível"></a>
# Scientific quality benchmark: public calibration and reproducible comparison

The benchmark distinguishes three levels of evidence: **(1) verifiable published facts**, **(2) results actually produced by Skill** and **(3) independent scientific judgments**. They are not interchangeable.

<a id="conjunto-de-referência-congelado"></a>
## Frozen reference set

File: \`benchmarks/public_review_reference_v1.json\`.

It exclusively contains bibliographic facts and selection totals identified in real articles, with links to the respective publishers and, when available, an institutional repository:

1. Madan, R.; Ashok, M. *AI adoption and diffusion in public administration: A systematic literature review and future research agenda*. Government Information Quarterly 40(1), article 101774, 2023, DOI [10.1016/j.giq.2022.101774](https://doi.org/10.1016/j.giq.2022.101774). In the screening section: 221 search results, 27 additional, 166 after removing duplicates, 117 fully examined and 73 included. The differences **248**, **82**, **49** and **44** are arithmetic calculations from these published totals, not separately observed records.
2. Aarab, A.; El Marzouki, A.; Boubker, O.; El Moutaqi, B. *Integrating AI in Public Governance: A Systematic Review*. Digital 5(4), 59, 2025, DOI [10.3390/digital5040059](https://doi.org/10.3390/digital5040059). Includes 67 studies. Other step numbers are not populated if missing in the frozen set.
3. Goulart, J. de M.; Picalho, A. C.; Colombo, J. E. M.; Melo, P. A.; Fadel, L. M. *Governance Processes in Artificial Intelligence in Brazilian Public Bodies: integrative review*. IJKEM, 2025, DOI [10.5007/2316-6517.2025.e109331](https://doi.org/10.5007/2316-6517.2025.e109331). The journal summary reports **400 documents retrieved**, **13 included** (6 dissertations, 2 theses and 5 articles), and five thematic axes. Intermediate steps are not invented. It is the most direct reference for a future **integrative review** replication, which will require access to the full list of studies and analysis criteria.
4. Page, M.J., et al. *The PRISMA 2020 statement*. BMJ 372:n71, 2021, DOI [10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71). It is a reporting guideline; **not** a review to reproduce. Participates only in metadata calibration.

This is a small, intentional, public set. It does not constitute a probabilistic sample of periodicals, a definitive template for categories or external validation of the Skill's quality.

<a id="reprodução-prospectiva-de-uma-revisão-integrativa"></a>
## Prospective reproduction of an integrative review

In addition to the current set, there is a [prepared integrative reproduction case](REPRODUCAO-REVISAO-INTEGRATIVA.md), with protocol in `benchmarks/integrative_replication_protocol_v1.json`. The case is the actual paper by Straub et al. (2023), on concepts and a framework for AI in government. **No reproduction results were produced**. The divergence between the total concepts/terms reported in the summary and in the highlights needs to be checked before comparison.

<a id="como-executar-sem-aplicativos-pagos"></a>
## How to run without paid apps

Python 3.10+ and standard library only. The metadata checker uses the public Crossref and OpenAlex endpoints already adopted by Skill. Does not require paid key; a free OpenAlex key is optional for higher query limits.

<a id="1-verificar-os-metadados-reais"></a>
### 1. Check the actual metadata

\`\`\`bash
python scripts/quality_benchmark.py pilot --output benchmark_pilot.json
\`\`\`

The command performs **real** queries, identifies inconclusions, contradictions and known alerts. Never reports verified results when services are inaccessible. To validate the structure without using a network:

\`\`\`bash
python scripts/quality_benchmark.py pilot --offline --output benchmark_offline.json
\`\`\`

The result of \`pilot\` is just calibration of external bibliography, **not evaluation of AI-generated academic text**.

<a id="2-comparar-um-resultado-real-da-skill"></a>
### 2. Compare a real Skill result

Execute the same scientific work script, with frozen criteria, in base mode and updated mode, preserving the **really** obtained results. Prepare each output in the format of observations:

\`\`\`json
{
  "schema_version": 1,
  "cases": [
    {
      "case": "ai_diffusion_review",
      "doi": "10.1016/j.giq.2022.101774",
      "title": "AI adoption and diffusion in public administration: A systematic literature review and future research agenda",
      "stage_counts": {},
      "locators": []
    }
  ],
  "claims": []
}
\`\`\`

The example shows **only the published structure and metadata**, not dummy Skill results. The \`stage_counts\`, \`locators\` and \`claims\` fields must be filled in only after the actual execution; do not copy counts from the reference set to pretend the Skill reproduced them.

Rate:

\`\`\`bash
python scripts/quality_benchmark.py evaluate \
  --candidate /path/resultado_observado.json \
  --workspace /path/of/project \
  --output /path/relatorio_qualidade.json
\`\`\`

For before/after comparison, add \`--baseline /caminho/baseline_observado.json\`. Without observation for a dimension, the metric is **null / not evaluated**, never 100%. Version differences are only interpretable with the same task, source, period, criteria and denominators.

<a id="dimensões-e-limitações-das-métricas"></a>
## Dimensions and limitations of metrics

| Dimension | When is it measurable | Limitation |
| --- | --- | --- |
| Bibliographic identity | When the work reports a DOI or title comparable to a frozen reference | It does not measure whether new unknown quotes were invented; a broader audit requires checking **all** generated references |
| Counts/flows | When the run comes up with its own numbers | Descriptive precision on published numbers does not reproduce the historical search or individual decisions |
| Locators | When the project has the source text legally accessible | MATCHED means textual presence; does not guarantee semantic support or quality of the study |
| Scientific claims | **Only** with reasoned judgments, outside the predictions and delivered separately | A "reviewer" JSON field does not authenticate independence; disagreements must be adjudicated |
| Theoretical categories | When there is a rubric and independent comparison contextualized | New justified categories should not be penalized just because they differ from the base publication |
| Time/rework/usability | In-house evaluation design, with protocol and operational metrics | Does not correspond to the scientific validity of the manuscript |

<a id="julgamento-independente"></a>
## Independent judgment

The optional notes file requires \`schema_version: 1\`, \`reviewer_reference\` with the documentary reference to the actual assessment, and \`claims\` with \`claim_id\` and \`label\` (SUPPORTED, NOT_SUPPORTED, or UNCERTAIN). It is reported by \`--adjudications\`.

**Do not** generate this file with the very answers that will be evaluated and do not have the AI ​​declare a non-existent "blind" review. An evaluator must consult the evidence directly and justify discrepancies. Respect the applicable ethical framework if the assessment involves human participants.

<a id="protocolo-de-decisão"></a>
## Decision protocol

1. Freeze corpus, date, method, criteria and Skill version.
2. Execute base script and save raw output, hashes and possible unavailability.
3. Run modified version under the same conditions, preferably with counterbalanced order and documented model/tool ​​information.
4. Audit all added references and check original sources/locators.
5. Obtain an independent review of the claims and categories, without accepting the model itself as a template.
6. Publish coverage, denominators, errors, disagreements and limits; not convert a small pilot into "validated scientific quality".The tests in \`tests/test_quality_benchmark.py\` use controlled mutations and disposable files to verify the **software**; are not presented as research data. The pilot that uses real APIs has a separate execution and report with the responses actually observed.

This starter set does not replace a full replication of a published integrative review. Such replication requires access to exported records, selection decisions, corpus and primary categorization, which should not be invented or extracted solely from the article abstract.