# REG-018 — Read-only citation/reference audit (incremental implementation)

This report reconciles existing canonical project identifiers and a **current**
SOURCE_VERIFICATION.json report. It reuses the established source-checking
pipeline; it does not introduce scientific gates, Excel tabs, new canonical
evidence registers, or new IDs. The source report is assessed with the
existing input-manifest and internal-consistency checks before any status
is trusted.

## Run

    python scripts/verify_sources.py /authorized/project --offline
    python scripts/reference_audit.py /authorized/project --strict

An offline verification cannot confirm metadata over the internet; use the
existing real checks when access is authorized. A local report file is
**optional** and is written only on explicit request:

    python scripts/reference_audit.py /authorized/project \
      --output 06_Submissao/Arquivos_Finais/reference_audit.json

The report does not synchronize Google Drive or pretend a local copy is the
canonical cloud state. Use actual authorized Drive integration and its receipt
before making a sync claim.

## Findings, not editorial verdicts

- BLOCK: missing/ambiguous canonical identifiers and claim links, malformed
  DOI syntax, source metadata contradiction, a DOI absent from both queried
  providers in an existing recorded report, literal passage/page conflict,
  or a stale/structurally contradictory report.
- REVIEW: no DOI (legitimate for many books and legal/organizational works),
  partial citation, duplicate DOI across multiple Evidence_ID records,
  incomplete provider coverage, unverified metadata/access, corrective and
  retraction notices (which require contextual appraisal, not automatic
  exclusion).
- All recorded results are **about bibliography, canonical linking and
  literal source locations**. An actual citation in a DOCX/PDF/Markdown
  manuscript is not yet parsed by this incremental implementation; only
  the canonical Evidence Matrix and Claim Ledger are reconciled.
- If SOURCE_VERIFICATION.json is missing or stale, previous claims of
  verified identity are NOT carried forward. This does not independently
  authenticate remote API responses, a human reviewer, or scholarly truth.
- --strict returns exit code 2 when any BLOCK or REVIEW finding exists;
  exit code 1 is a tool/structural input failure.

## Privacy

The printed/written report includes identifiers, coded findings and a report
checksum. It omits publication titles, article text, full-text paths, original
DOIs, source excerpts and personal reviewer rationales. It remains internal:
identifiers and status patterns may still be sensitive in some contexts.

## Next REG-018 acceptance step

Before marking REG-018 fully complete, add a separate, explicitly configured
citation parser for the approved canonical manuscript format and reconcile
the in-text citations against the reference list. Do NOT guess how APA,
ABNT and author-year text can be parsed from arbitrary PDF/DOCX without a
method-appropriate extraction and human review.

The next ranked radar item is REG-011, substantive claim-to-passage
verification, and remains independent of this metadata audit.
