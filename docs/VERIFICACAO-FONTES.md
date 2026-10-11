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