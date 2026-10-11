# Meu Artigo — v0.9.0-beta.2

**Experimental public beta (software release).** This is an engineering
update, **not** an independently validated research method, peer-reviewed
product or guarantee of scientific article quality. The canonical installable
ZIP and SHA-256 checksum are distributed through the
[matching tagged GitHub release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.2).
Use the official asset, not GitHub's automatic source-code ZIP.

## Improvements since v0.9.0-beta.1

- **Optional bibliographic metadata adapters:** explicit opt-in Python tools
  for bounded OpenAlex, Crossref and Semantic Scholar searches, limited
  OpenCitations citation counts, Unpaywall DOI availability metadata, and
  user-owned Zotero metadata, subject to authorization and network access.
- **Manual research mode preserved:** no API keys, subscriptions, extra
  connectors or network access are required for ordinary Skill use.
- **Safer CSV exports:** bibliographic deduplication and audit output
  neutralizes spreadsheet formula cells from externally retrieved metadata.
- **Recoverable local imports:** the three related CSV registers use a
  single-writer recovery journal. Project validation blocks operations
  after an interrupted write until explicit recovery.
- **Clearer trace evidence:** imported records use the existing
  `UNVERIFIED` state until actual independent execution evidence exists;
  a legitimate zero-result search is not misreported as network failure.
- **Consolidated documentation:** installation, public-versus-source version,
  scientific boundaries, privacy, citation metadata and release checks
  have been reviewed and synchronized.
- **Release controls:** automated code, link, privacy, packaging and
  software regression checks, including protection against publication
  metadata that still describes a source candidate.

## Scientific safeguards retained

The [L] literature / [I] inference / [P] proposal distinction,
human scientific decisions, C.A.D.A. operational tracking, source and claim
provenance, journal-aware editing, anonymization, AI-use transparency,
full-text copyright rules, and Google Drive-first policy remain in place.
A confirmed local software event is not an independent scientific review.

## Explicit limitations

- Bibliographic adapters passed **offline simulated-response tests**;
  vendor production usage, rate limits, licensed subscriptions, secure
  private Zotero access and real end-to-end API operation remain unverified.
- The Skill ZIP provides research instructions and optional scripts rather than an independent hosted interface.
  in this release. The API tools are opt-in local Python modules, not
  automatic ChatGPT tool connections.
- Licensed Scopus / Web of Science authenticated integrations and publisher
  full-text retrieval **are not included**.
- Multi-user transactional storage is not implemented; the local journal
  is single-writer and does not synchronize Google Drive by itself.
- Actual installation, Google Drive write/readback, session resumption,
  multilingual usability and full scientific article execution with this
  exact beta still require observed authorized tests.
- Independent scientific validation, empirical productivity improvement,
  publication outcomes and third-party endorsements **have not been established**.

## Installation and feedback

1. Download `MeuArtigoSkill-v0.9.0-beta.2.zip` and `SHA256SUMS.txt`
   from this exact GitHub release after it is available.
2. Verify the checksum, then follow the
   [installation guide](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/COMECE-AQUI.md) for your supported platform.
3. Work only with lawfully accessible sources and confirm writing
   permissions before declaring files saved remotely.
4. Report non-sensitive defects through GitHub Issues; use a private channel
   for secrets, unpublished manuscripts or protected institutional data.

Existing published releases and their rights are preserved.
