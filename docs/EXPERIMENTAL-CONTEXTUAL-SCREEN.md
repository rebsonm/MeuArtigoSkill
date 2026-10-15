# Parallel contextual screening — experimental REG-011 increment

## Objective and design

This adds an **experimental structured-context sidecar** to the existing
REG-011 human-assisted claim/evidence review. It only runs after an exact
local quoted passage is located with its current source checksum, and after
the existing source report, identifiers and annotation are verified. It
does not call a language model, interpret full research documents, search
external literature, fetch URLs or make scientific judgments.

The existing lexical screen remains **unchanged** and continues to emit
`semantic_risk_codes`. The separate contextual sidecar emits
`contextual_signal_codes` and bounded, generic review questions
for causal attribution, sample scope, sampling denominators, statistics,
observed outcomes, operational status, record dates, methodology,
comparators and numeric direction.

The signals are *possible discrepancies*, not claims that a source is wrong.
Neither empty nor populated signals establish whether a proposition is
supported. Both groups are ADVISORY, and neither changes strict mode,
seven human scientific gates or persistent canonical project files.
REG-013 summarizes the two groups separately as REVIEW-only categories.
Only coded generic observations are exported; neither source passages nor
private research prose are included.

## Comparative evidence

Use the development-visible 24-case fixture with its original provisional
author labels, without changing the detectors:

    python scripts/compare_contextual_probes.py \
      --benchmark benchmarks/claim_support_heldout_v1.json \
      --output-dir /new/synthetic-context-comparison \
      --skill-commit EXACT_40_HEX_CHECKED_OUT_REVISION

Outputs are `comparison.json` (coded results and descriptive counts),
per-case `evidence/*.json`, a two-run REG-001 integrity ledger
and an independently score-replayed REG-019 ZIP. The comparison is between
two developer-authored software probes, *not* an independent prospective
scientific validation. The 24 cases and their failure modes were visible
when this contextual design was proposed: they are **not a new blinded
holdout**. Even favorable counts must not be generalized.

## Mandatory boundaries / acceptance

- A missing, altered or unverified source **prevents both sidecars from
  running** and leaves the existing strict evidence protection intact.
- Suspected overreach alone may trigger a review suggestion but NEVER a
  source-blocking gate or an automatic approval.
- No scientific reviewer is authenticated and no scientific claim is
  certified by these heuristics.
- For an empirical effectiveness claim, acquire lawful independent source
  material and previously unseen labels evaluated by **external human
  assessors**, with predefined adjudication and uncertainty analysis.
- Reviewer independence and a future publication/merge decision are
  different human actions. Neither is performed by this increment.
