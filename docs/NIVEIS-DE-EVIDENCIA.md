<a id="níveis-distintos-de-comprovação-científica"></a>
# Different levels of scientific proof

**My Article** does not automatically transform a system record into
scientific confirmation. There are four different questions and no level can
be inferred from the previous one. This unfolding is a **rule of integrity of the
software**, not a methodological scale validated by third parties.

| Level | What is verifiable | What has not yet been demonstrated |
|---|---|---|
| 1. Bibliographic identity | DOI metadata, title, year and author correspond to academic records consulted | Reading of the original text, methodological quality or adequacy to the statement |
| 2. Queryable literal passage | A textual sequence appears in a truly accessible and identified file; report can record hash and location | That the interpretation made of the excerpt is correct or representative of the study |
| 3. Documented human judgment | The matrix declares human validation/appreciation and points to an original manifestation | Authenticity independent of the reviewer's identity and scientific validity of the conclusion |
| 4. Sustained empirical result | There are data/materials, procedures actually carried out and traceable analysis/evaluation | Validity of inference, absence of bias, generalization or independent reproduction |

<a id="procedimento-com-os-mesmos-arquivos"></a>
## Procedure with the same files

- `05_Evidence_Matrix.csv`: record what was actually examined,
  `Evidence_ID`, the source locator and role.
- `SOURCE_VERIFICATION.json`: metadata check result and
  passages according to `scripts/verify_sources.py`, linked by SHA-256 to
  matrix. Only `metadata_status=VERIFIED` indicates document verification of
  bibliographic identity; only `locator_status=MATCHED` indicates that a
  literal excerpt could be found in the consulted copy. Both can be
  absent and never prove semantic support.
- `09_Claims_Ledger.csv`: register `Claim_type`, source, `Trace_IDs`,
  limits, `Researcher_review_evidence`, and scientific review status.
  The categories **[L], [I] and [P] remain independent**: source text,
  Bounded inference and original proposition are not interchangeable.
- `17_Decision_Log.csv`, `18_Human_Validation_Gates.csv` and
  `METHOD_PROFILE.json`: preserve the researcher's original statements,
  chosen method and link to materials, analysis and integration when
  there are claims about empirical results.
- `EMPIRICAL_RESULT`: when freezing assertions in new projects with routes
  explicit, require empirical route/design science, documentary reference
  of materials and analysis actually carried out, valid decisions of
  `GATE-0004` and `GATE-0005`, `Trace_IDs` and human traceable review.
  The presence of these fields **does not yet certify** the find or identity
  of those who reviewed: one must examine the original sources and the conditions of the
  inference. A barely planned study remains without results.

Run the conservative inspection locally, in the already authorized workspace:

```bash
python scripts/scientific_evidence_tiers.py /caminho/do/projeto
python scripts/scientific_evidence_tiers.py /caminho/do/projeto --freeze
```

The output distinguishes counts from **documentary evidence** and includes the limits
`bibliographic_identity_proves_text_read=false`,
`literal_locator_proves_claim_semantics=false`,
`human_review_record_authenticates_reviewer=false` and
`empirical_scientific_result_independently_validated=false`.
Does not produce scientific quality scores and does not require a new tab or
family of identifiers.

The `GATE-0006` closing audit uses this check when the
project has active methodological governance. In older projects,
the choice of a new route and the migration of scientific records require
documented decision: never retroactively complete a validation.

<a id="limites-e-auditabilidade"></a>
## Limits and auditability- A simple file reference or URL in `METHOD_PROFILE.json`
  **does not prove** that the file exists, is up to date, or has been examined.
  Always check original evidence and project permissions, including
  when Google Drive is the canonical repository.
- The script audit only checks presence and formal coherence of
  records. No field results, statistical analysis or evaluation
  artifact was performed by the act of completing this protocol.
- Recognition of a literal sequence does not prove fidelity
  semantics of interpretation; This requires contextualized reading.
- No causal inference should be made exclusively from
  correlation, simple before/after contrast or protocol approval.
- Engineering test reports and *gates* do not equate to
  independent scientific evaluation of Skill, which remains pending.