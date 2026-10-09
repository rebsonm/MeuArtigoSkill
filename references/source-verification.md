# Independent source verification

Before freezing material literature-grounded claims, read docs/VERIFICACAO-FONTES.md and run scripts/verify_sources.py whenever execution is possible.

- Use the existing Evidence_ID, Record_ID and Claim_ID relationships. Do not add IDs or spreadsheet tabs.
- Read canonical 05_Evidence_Matrix.csv and join real screening/full-text tracker rows. Save SOURCE_VERIFICATION.json with an evidence-matrix hash and synchronize it to Google Drive if Drive is canonical.
- Crossref and OpenAlex offer public free DOI metadata lookup. OPENALEX_API_KEY is optional and free. Respect quotas; no paid plan is required. Never expose API credentials in logs.
- Check quotations in lawful local PDFs/TXT; do not upload source PDFs to metadata providers. Optional pypdf or pdftotext extracts PDF text locally.
- A valid DOI verifies an identity/metadata claim, not semantic evidentiary support. A matched passage verifies text presence, not that the scientific claim follows.
- Unknown DOI, absent full text, missing title, inaccessible API or unextractable PDF means UNVERIFIED/REVIEW_REQUIRED, not VERIFIED. Legitimate sources without DOI require alternative/manual bibliographic checking.
- Handle editorial correction and retraction alerts cautiously, documenting context and limitations.
- Before GATE-0006, examine source-check results and substantiate human review of any unresolved or semantically material claims. Never invent a completed verification.

A source-verification report is technical evidence, not peer review or a replacement for critical appraisal.