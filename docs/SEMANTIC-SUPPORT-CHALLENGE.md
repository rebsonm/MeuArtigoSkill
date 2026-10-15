# REG-011 preliminary, author-labeled semantic-support stress evaluation

This reproducible **synthetic software-behavior challenge** is a diagnostic
of the scientific *limits* of the claim-to-passage validator, NOT a completed
scientific evaluation, authenticated human review or standalone sample of
scientific literature.

## Design fixed before execution

The 16 frozen cases were committed separately in
`benchmarks/claim_support_challenge_v1.json`. They contain
four author-labeled examples of each class: SUPPORTED, PARTIALLY_SUPPORTED,
NOT_SUPPORTED and INCONCLUSIVE. The dataset deliberately covers shifts in
causality, population, denominator, external validity, direction, statistics,
methods, sampling, missing outcomes and indeterminate evidence. All sources
are made-up passages, not representations of actual published documents.
Their provisional reference labels were written by the development assistant,
NOT by a blinded independent human evaluator.

The script creates temporary canonical tables, synthetic source documents
and internally consistent **mocked** source-verification records. This is a
valid software fixture but **NOT live external source verification**.

Each actual REG-011 review is run three times:

1. **No review:** confirm that each claim remains PENDING_HUMAN_REVIEW.
2. **Adversarial blanket attestation:** mark every claim as SUPPORTED, with
   all declared alignment dimensions ALIGNED and a literal exact quote.
   The supposed reviewer is clearly synthetic, not an actual person.
3. **Reference-label-supplied declaration:** give the checker the
   author-supplied classification and aligned/misaligned dimension values.
   This measures only recording of declarations, NOT automated recovery
   of semantic truth or authentic reviewer participation.

A recorded but unverified declaration is **not** an approved scientific
claim or a verified reviewer. The current tool is not designed to perform
semantic entailment. The stress test intentionally probes that missing
ability rather than assuming it exists.

## Offline reproducibility

    python scripts/evaluate_semantic_challenge.py \
      --benchmark benchmarks/claim_support_challenge_v1.json \
      --out-dir /new/synthetic-semantic-run \
      --skill-commit EXACT_40_CHARACTER_SOURCE_COMMIT

This creates:
- `preliminary_assessment.json` with provisional class counts,
  bounded confusion counts, limits and only case IDs.
- `evidence/SYN-NNN.json` with codified observed statuses
  and SHA-256 hashes, omitting the passages and project file paths.
- `semantic_case_catalog.json`: a derived test case
  catalog that maps the author's positive examples to PASS and negative
  examples to FLAG *only for this expected-versus-observed challenge*.
- `evaluation_runs.jsonl`: REG-001 append-only technical
  evaluation record and its input hash.
- `evaluation-replay.zip`: REG-019 deterministic
  privacy-reduced export with replay verification.

The existing REG-001 registry now accepts expected PASS for *synthetic
negative-control cases* as well as expected BLOCK/FLAG. PASS never certifies
scientific correctness or an authenticated human review.

## Follow-up exploratory lexical screening

The frozen 16-case challenge is also executed against optional conservative
lexical risk indicators when a source quotation matches exactly. The baseline
formal review status remains a non-authenticated *declared* judgment. New
signals are separately reported by code, and are only reasons to request
human examination. Results from this development-visible case collection
must be labeled **in-sample**, with no independent assessor or blinding.

## Interpretation and limits

If adversarial blanket SUPPORTED declarations receive a status saying only
that a human judgment was recorded **but not authenticated**, the formal
schema has NOT detected any semantic overreach. That is not a scientific
gate approval or claimed source corroboration. A false negative in this
report means a developer-labeled semantic discrepancy was *not independently
flagged by the current formal reviewer*, NOT a missed decision by an
automated semantic classifier (there is none).

Confusion counts are given against author-supplied hypothetical labels only.
Do **not** generalize precision, recall or specificity to real researchers,
journal publications, Brazilian public organizations or other tools.
No participants were enrolled, no person gave a research verdict and no
researcher interaction was observed. Real independent adjudication, blinded
labeling, sources with valid access rights, assessor agreement and checks
against broader phenomena remain to be completed before publication.
