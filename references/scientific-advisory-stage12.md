# Stage 12 — Source-linked scientific advisories (REG-018 / REG-011)

Scope: selective import from historical PR #65 into the PR #78 candidate.
The baseline `scripts/claim_integrity.py` is not replaced or wrapped to
override its existing checks. The DEC/TRACE human decision ledger, C.A.D.A.
workflow, seven scientific gates, and Drive F1–F9 remain unchanged.

## Modules and contracts

- `reference_audit.audit(root)` (REG-018): checks canonical bibliographic
  references, claims' Evidence_ID links, DOI syntax, provenance of the
  source-verification report, and literal locator state. An objective
  missing/ambiguous identifier or stale verification can have structural
  severity BLOCK. That is NOT a judgment of scientific validity.
- `semantic_claim_review.review(root, assessments=None)` (REG-011):
  checks recorded source and passage fingerprints and explicitly declared
  human review annotations. Review declarations are NOT authenticated. Its
  output has `semantic_support_proven=false`,
  `gate_approval_performed=false`, and `researcher_authenticated=false`.
- `claim_overreach_signals.signals(claim, passage)`:
  language-limited, pattern-based lexical hints. All outcomes (including
  NOT_EVALUATED) have `severity=ADVISORY`, never approve or block a
  scientific gate, and do not demonstrate semantic entailment.
- `contextual_support_probe.examine(claim, excerpt)`:
  bounded experimental contextual mismatch hints. Every reported signal
  is ADVISORY; no positive-result certification is possible.
- `report_output_guard.write_report`: local report helper, create-only,
  confined to `98_Technical_Reports`. It is imported only to support
  existing explicit CLI output, not called by a dashboard or external interface transport.

## Required decision boundary

The source quotation must be independently verified against current source
hashes before either sidecar is invoked by REG-011. A clean DOI or a zero
signal count never proves that a claim is supported. Reviewer fields are
user-declared metadata, not cryptographically authenticated identities.
No published or independent external peer assessment is included.
All project-local reports are optional, explicit, nonoverwriting writes,
never Google Drive synchronization.

The imported reference module's BLOCK findings concern objective trace and
bibliographic consistency; they never authorize automated manuscript
acceptance or scientific gate transitions. Advisory heuristic alerts must
not increase the workflow's hard-blocker count. Any future connection to
the blue dashboard must use an explicit read-only projection adapter and
separate review, not a substitute for native_chat_dashboard.py.

## Verification boundary

The suites `tests/test_reference_audit.py`,
`tests/test_semantic_claim_review.py`,
`tests/test_claim_overreach_signals.py` and
`tests/test_stage12_scientific_advisory.py` run synthetic data only.
They are not a controlled blinded empirical evaluation of precision,
recall, scientific reliability, model bias, or real researchers.

No merge, release, authenticated source modifications, installed app
updates, VPS work, or Google Drive changes are authorized by this stage.
