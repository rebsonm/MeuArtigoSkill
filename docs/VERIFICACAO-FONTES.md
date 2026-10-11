<a id="verificação-de-fontes-e-passagens"></a>
# Checking sources and passages

Bibliographic checking is separate from AI writing. The script checks DOI metadata against open databases and searches for passages only in legitimately accessible local copies. It does not certify the methodological quality or the semantic interpretation of claims.

<a id="custos-e-pré-requisitos"></a>
## Costs and prerequisites
- Python 3.10+; external queries only use standard libraries.
- Crossref: Free public API, no account and no key. Subject to rate limits.
- OpenAlex: free basic consultations without a key. Optional free key in OPENALEX_API_KEY, useful on larger volumes.
- PDFs: optional installation of the free pypdf library (pip install pypdf) or pdftotext now available. TXT and Markdown work without extra libraries.
- No complete PDF is transmitted to Crossref/OpenAlex. Without executable code available, Skill cannot claim to have performed deterministic checks.

<a id="utilização"></a>
## Usage
With the workspace authorized and the Evidence Matrix completed:

    python scripts/verify_sources.py "/caminho/do/projeto" --strict

To check only local locators, without access to APIs:

    python scripts/verify_sources.py "/caminho/do/projeto" --offline

Optionally, --mailto EMAIL enables identification in Crossref. The result is written to 00_Gestao_e_Continuidade/SOURCE_VERIFICATION.json. When Google Drive is canonical, sync the report there; Isolated local result does not replace the workspace.

The script links 05_Evidence_Matrix.csv, 04_FullText_Tracker.csv, and 03_Screening.csv, using Evidence_ID and Record_ID. Text in local files can be declared in FullText_path, Full_text_path, PDF_path, Source_path or File_path, or in the tracker's File_or_URL. Remote files are never automatically downloaded.

To test a locator, provide a literal passage of at least five words (25 characters), optionally with p. N. Only the indication "p. 12" does not prove the textual occurrence.

<a id="interpretação"></a>
## Interpretation
- VERIFIED metadata: at least one provider identifies the DOI and corroborates title, year/author when informed, with no contradictions detected. It does not mean that the claim is true.
- MISMATCH, INVALID_DOI and NOT_FOUND require correction or investigation. NOT_FOUND requires express absence in both services.
- NO_DOI: legitimate books and documents without DOI are not automatically deleted; require another type of verification.
- UNVERIFIED: provider unavailable, insufficient data or offline mode. It's not approval.
- MATCHED: passage found in the text extracted from the local copy. PASSAGE_NOT_FOUND and PAGE_MISMATCH require review of the original and extract.
- TEXT_UNAVAILABLE, REMOTE_NOT_DOWNLOADED and LOCATOR_NOT_CHECKABLE: pending issues, not demonstrating fraud.
- Crossref `updated-by` describes a notice changing this article; `update-to` means this record is the notice about a *different* article. The two directions are not interchangeable. Save the notice DOI, type, provider and direction without copying protected content.
- `retraction_alert` and `correction_alert` are distinct; they require separate researcher attention and do not alone prescribe exclusion. `provider_warnings` retains OpenAlex outages instead of hiding them when Crossref can answer.
- `PASSAGE_NOT_FOUND` and `PAGE_MISMATCH` are objective blockers of GATE-0006, not waivable limitations.
- claim_support_status remains NOT_SEMANTICALLY_VERIFIED, even when DOI and locator match. It is up to human review to evaluate the actual support for the argument.

The report preserves the results and hashes, without reproducing protected long texts. Don't share files with internal paths or sensitive titles.

## Exact input integrity and exceptional human reviews

Version 2 of SOURCE_VERIFICATION.json records a deterministic manifest of all
three inputs: the Evidence Matrix, Screening register and FullText Tracker,
plus their currently referenced local PDF/TXT/MD files and complete
Evidence_ID/Record_ID bindings. Missing, added, removed, modified or
duplicated records/files invalidate the report. Legacy version 1 reports must
be regenerated; they cannot justify new GATE-0006 approvals. The manifest
contains local relative paths for internal audit; it must not be published or
shown unfiltered to chat users. Source passages and complete PDFs are not
embedded in the report.

The existing DEC_ID decision log, not a new register, supports narrow
human assessments of genuine uncertainty. For each affected Evidence_ID,
append a new `EVIDENCE` decision with `Status=APPROVED`,
`Gate_ID=GATE-0006`, one exact `Evidence_IDs` token, a
`Decided_by` identity and substantive `Rationale`. Set
`Affected_artifacts` to
`SOURCE_VERIFICATION.json#sha256=<exact SHA-256 of the report bytes>`.
Its `Notes` must include one line each:

    SOURCE_REVIEW_LIMITATIONS=<specific recognized limitations>
    ORIGINAL_RESPONSE_REF=<reference to researcher's authentic response>

Use the existing `governance_events.py decision` command with matching
flags including `--evidence` for the actual human response. Keep the
DEC_ID history; on a new report or changed source, re-evaluate and record a
new decision rather than rewriting history. Such a decision can document
unverifiable DOI information, absent access, provider failure or an
editorial notice; it **never upgrades** the source result to verified.
It **cannot override** a non-existent passage, wrong page, mismatched DOI,
duplicate IDs, missing inputs or stale manifest.

GATE-0006 approvals are blocked when the report is missing, stale,
structurally inconsistent, objectively contradictory or has unreviewed
limitations. A completed gate is re-audited by the validator against current
inputs; a historical approved state is not silently considered valid after
a subsequent source change. Neither a hash nor a self-reported human decision
authenticates the researcher or semantic support. Honest attribution remains
necessary; scientific validation requires an independent substantive review.

See `scripts/source_report_integrity.py` for read-only evaluation and
`tests/test_source_integrity.py` for deliberately synthetic regressions.
## Status integrity, provenance and verification during execution

The verifier records the SHA-256 digest of the JSON returned by each
Crossref/OpenAlex provider, retaining only bibliographic summaries and
hashes in the report, not extensive metadata or copyrighted full text.
A hash allows a locally preserved genuine response to be compared with
what was processed, but **does not authenticate the remote server** or
independently prove a real external API request.

Provider unavailability or missing responses are explicitly recorded as
warnings even when another provider corroborates the metadata. Partial
provider coverage must therefore trigger review rather than a
declaration of fully verified provenance.

Before and after each batch, the verifier recalculates the manifest for
canonical registers and referenced local files. Changes during the run
block the new report with
`SOURCE_INPUTS_CHANGED_DURING_VERIFICATION`. Replacing an existing
official report is atomic; write failures cannot overwrite its last
verified intact version.

The existing `source_report_integrity.py` audit also checks internal
consistency: `METADATA_AND_LOCATOR_CHECKED` is allowed only with
`VERIFIED` identity, a `MATCHED` text passage, the current SHA-256
of its local source, no unresolved warnings or alerts, and at least one
positive provider response. Offline reports cannot simultaneously claim
that a live metadata query verified an article. Retraction or correction
notices associated with the examined work must not be hidden by a
success summary. Contradictions block GATE-0006.

These controls do not demonstrate that any scientific statement is true,
replace methodological analysis or authenticate a human decision.
Retractions, corrections and incomplete checks require a documented
researcher interpretation rather than automatic article exclusion.

## Integrated verification of literature [L] citations at Gate 6

At final audit, the existing `scripts/claim_source_integrity.py`
compares each `Evidence_ID` cited by a literature [L] claim against
the effective `SOURCE_VERIFICATION.json` report. A
`Locator_status=MATCHED` cell in `09_Claims_Ledger.csv` is **not
self-validating**: every cited evidence item must have a literally
matched passage in the current verified report.

If a locator is unavailable, the claim cannot independently declare
itself `MATCHED`; limitations need a recorded human assessment and
`REVIEWED_LIMITATIONS` in the source report. Missing links, stale
reports or contradictory records prevent Gate 6 approval. The project
validator reapplies this same rule even after earlier approvals,
without changing or deleting the history of human decisions.

This is a **structural citation-consistency check**, not semantic
verification or authentication of the evaluator's identity.
All test researchers and source text are synthetic; real Google Drive
homologation remains a subsequent authorized evaluation.
