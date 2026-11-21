# Methodology intake inventory — metadata only

This repository stores an **inventory of a user-designated academic methods collection** in six JSON files: `inventory_part_01.json` through `inventory_part_06.json`. It does **not** reproduce the underlying private/publicly shared Drive files. No Drive file IDs, cloud account, connector URLs or access tokens are included.

**Snapshot 2026-11-21**: 70 first-level categories, five nested folders, **475 PDFs** with a reported cumulative size of **688,482,286 bytes (~688.48 MB)**. Each document records the source filename, category, MIME type, byte count and `rights: "UNVERIFIED"` as an initial intake classification. Some filenames may contain encoding artifacts, duplicates or ambiguous editions. Such metadata is **not** an authoritative bibliographic record or proof that a work was read, scanned, OCR'd, or evaluated.

## Public binary corpus versus metadata inventory

Only individual papers with independently reviewed public redistribution terms and documented attribution may be committed as binary PDFs to `../pdfs/` and declared in `../pdf_catalog.json`. An archive link, a Google Drive permission or a paper's general open-access status is **not** itself a verified redistribution license. The publicly distributed Skill ZIP does not contain this archive or any PDFs.

Other sources remain excluded from public Git, including publisher-protected books. The metadata inventory can support discovery and a rights-audit queue but must not be treated as a source of original passages or be included in citations as if the underlying PDF were accessed.

This is a development snapshot on an isolated draft PR; it does not attest a semantically evaluated RAG, a running host, or approved scientific gates.
