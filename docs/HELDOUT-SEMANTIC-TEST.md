# REG-011 post-freeze synthetic holdout exercise (24 fictional cases)

**Scope:** a second collection of twenty-four **new synthetic** claim/passage
pairs, different from the sixteen examples used to develop REG-011 lexical
overreach signals. The cases and provisional classifications were committed
**before** the first execution, on commit
`21ece0992633a88734a8fa01d9b0ebf831df5d77`.

The lexical detector was frozen at source commit
`486a50fe8fb6b9d43525efa9bbf6f15ca1125fdb`. This evaluation
**does not train, tune thresholds or modify its rules**, regardless of outcome.

## Important scientific limits

The reference labels were authored by the same development assistant, with
knowledge of the existence of the detector. Consequently this is not a
blinded, externally sourced or independently adjudicated validation set.
Calling it "held-out" is correct **only relative to the original 16 examples
used for rule development**, NOT relative to the full development process.
It is a useful fixed software stress test, not evidence of accuracy on
published papers or the behavior of real researchers.

The cases comprise 6 author-labeled SUPPORTED, 6 PARTIALLY_SUPPORTED,
6 NOT_SUPPORTED, and 6 INCONCLUSIVE. They include qualified causal claims,
negated statistical significance, subgroup direction, bounded universal
quantifiers, missing-data fidelity, manual versus automated design, protocol
versus results, and uncertain evidence.

The executor uses the *actual* current REG-011 code and exact-quote,
hashed-source fixtures, supplied mock bibliographic verification and a
synthetic **unauthenticated** blanket-support declaration. It records what
the heuristic flags, and computes only provisional confusion counts against
the author's labels. It never classifies a claim as scientifically approved.

## Invocation and evidence

    python scripts/evaluate_semantic_holdout.py \
      --benchmark benchmarks/claim_support_heldout_v1.json \
      --out-dir /new/heldout-run-directory \
      --skill-commit EXACT_40_HEX_REVISION

The output includes `holdout_assessment.json`, per-case coded evidence
without quoted source text, REG-001 hash-chained runs and a REG-019
replay package. The output folder must be new, and the workflow stores a
limited-retention **synthetic-only** CI artifact.

A CI pass means that code executed and evidence/score contracts held.
CI **must not** be configured to require particular confusion-matrix values
or to change detector rules to make the score perfect. Missed cases and
false alarms are legitimate findings and remain visible in the output.
