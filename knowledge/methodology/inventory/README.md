# Methodological research archive inventory — licensing review

**Status (2026-11-21):** inventory completed; blanket public redistribution of the original PDFs is **not authorized**.

- Source: a thematic research archive identified by its owner. Google Drive IDs and account details are intentionally excluded from this public repository.
- Enumerated scope: **70 top-level folders and 5 nested folders, containing 475 PDFs**.
- Size according to Drive metadata: **688,482,286 bytes (approximately 688.5 MB)** before deduplication.
- The 475 files have **466 distinct filenames**; repeated names do not establish identical file contents.
- Largest recorded PDF: approximately 91.5 MB. Every observed file is smaller than 100 MB; that fact does not make it advisable or lawful to put the files into Git.
- Original PDFs actually published in this branch are explicitly listed in `../pdf_catalog.json`. Only sources with separately verified redistribution rights may be committed in `../pdfs/`.

## Metadata inventory files

1. [Part 01 — first 18 folders](./drive-source-candidates-part-01.json): 170 PDFs
2. [Part 02 — next 18 folders](./drive-source-candidates-part-02.json): 100 PDFs
3. [Part 03 — next 18 folders](./drive-source-candidates-part-03.json): 104 PDFs
4. [Part 04 — last 16 folders](./drive-source-candidates-part-04.json): 66 PDFs
5. [Part 05 — five nested folders](./drive-source-candidates-part-05.json): 35 PDFs

These entries are **metadata, not PDF contents**. The value `rights_status: NOT_REVIEWED` identifies an unverified redistribution right, not a presumption of permission. Each published PDF requires its own verified license evidence in the public PDF catalog. A DOI, openly shared Drive link, or personal academic access alone does **not** establish redistribution permission.

**Guardrail:** do not upload a protected PDF into this public repository, its branches, Git LFS, Actions artifacts or Releases unless the public redistribution license is properly documented. Do not expose private account IDs, secret tokens, cloud credentials or restricted full texts in public metadata. Bibliographic links and original editorial syntheses may be included subject to applicable terms.

A separate **private GitHub repository** would still require lawful storage and access, and authenticated host permissions for the installed Skill. Never embed credentials inside a publicly distributable ZIP.

**Functional distinction:** a complete metadata inventory is not a full text corpus and does not demonstrate validated vector retrieval. The installed Skill must remain small, with indexes and source documents excluded from the installer.
