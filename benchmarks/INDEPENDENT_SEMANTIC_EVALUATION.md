# Independent scientific evaluation — not a simulated approval

This protocol addresses MEL-03. It is **not** evidence that independent
evaluation has already occurred.

## Freeze before classification
- Define the target task and claim-status labels, inclusion boundaries, methods,
  source access modes (metadata-only / abstract / full text), and expected
  stratification by discipline and design.
- Use a corpus chosen independently of the tool's own outputs where possible.
- Freeze and hash the source corpus and an initial question set.
- Keep gold-standard labels and adjudication notes hidden from the model during
  prediction. A model judging its own answers is not an independent reviewer.
- Annotate citations and exact locators, deontic versus observational claims,
  negation, quantifiers, populations, contradictions, and ambiguous scope.

## Humans and disagreement
- Obtain original judgments from at least two genuinely independent qualified
  assessors, or report the actual smaller review design honestly.
- Record disagreement and adjudication with exact evidence; do not invent people.
- Keep researcher-authored human gate decisions separate from assessor opinions.

## Report
- Compare without-controls / with-controls under the same source corpus,
  task wording, version, output constraints and retrieval rights.
- Publish denominators, missing evaluations, abstentions, confusion matrix,
  coverage, per-class precision/recall when valid, and qualitative error cases.
- Treat unavailable full text and unreachable APIs as unverified rather than
  negative evidence.
- Preserve blind labels until after first-pass predictions are frozen.
- Store first pass and corrections separately; label any same-agent critique
  INTERNAL and never report it as independent accuracy.

## Criteria for pending status
Until real independent reviewers and frozen original evidence are supplied,
set independent_semantic_accuracy = NOT_EVALUATED. Synthetic fixtures test
software behavior only, not truth, adoption or academic quality.
