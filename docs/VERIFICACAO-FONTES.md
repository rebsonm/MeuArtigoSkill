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
- retraction_alert/update_alert: require evaluation of the editorial notice and scientific consequences; do not determine automatic exclusion.
- claim_support_status remains NOT_SEMANTICALLY_VERIFIED, even when DOI and locator match. It is up to human review to evaluate the actual support for the argument.

The report preserves the results and hashes, without reproducing protected long texts. Don't share files with internal paths or sensitive titles.

Before GATE-0006, check the updated report and document the necessary human checks. In projects with source_verification_required=true, the validator prevents approval with a report that is missing, outdated or containing deterministic divergences. Pending issues should not be treated as automatic confirmations.