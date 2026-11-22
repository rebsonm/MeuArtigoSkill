# First PDF-bearing Skill trial — source rights and package scope

Date: 2026-11-22. **NOT A RELEASE OR INDEPENDENT LEGAL CERTIFICATION.**

## Approved plan and implemented partition

The maintainer selected staged release preparation (alternative A): review and
package documented openly redistributable originals first, defer unidentified
or rights-restricted copies. This stage changes neither installed Skills nor
historical Git state.

Original public PDF catalogue: **51** binaries, 41,272,465 bytes, all exact
SHA-256 and size checks PASS on CI. Individual source catalogue ledgers:
475 inventory records, **17** rights-positive original entries (overlap with
public sources) and **458** without affirmative distribution approval.
The user's private archive was NOT copied.

**Trial batch selected:** 29 existing PDF originals, 27,287,058 bytes:
25 articles with the PLOS journals' blanket CC BY 4.0 publication policy,
plus four article-specific primary-rights pages. The restricted list is
`PUBLIC-PDF-TEST-APPROVALS-2026-11-22.json`; source PDF files remain
unchanged, individually SHA-pinned.

- PLOS journals' general article rights policy, including commercial reuse
  with attribution: https://journals.plos.org/plosone/s/licenses-and-copyright
  and https://journals.plos.org/ploscompbiol/s/licenses-and-copyright.
  Current publication pages checked as representative individual evidence:
  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0232076,
  https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003149,
  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0330217,
  https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014882,
  https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004961,
  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0283092.
  PLOS policy applies unless the particular article states an exception.
- Koerich et al. 2009 (UFG), article-page explicit CC BY 4.0:
  https://revistas.ufg.br/fen/article/view/47234
- Bicudo 2014 (UFSC), article-page explicit CC BY 4.0:
  https://periodicos.ufsc.br/index.php/revemat/article/view/1981-1322.2014v9nespp7
- Lopez Bernal et al. 2017 (PMC publisher version), explicit CC BY 4.0:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5407170/
- Jaakkola 2020 (Springer), article-specific CC BY 4.0 with reminder about
  excluded third-party materials:
  https://link.springer.com/article/10.1007/s13162-020-00161-0

**Not included in trial:** 20 other catalogue entries marked CC BY 4.0 whose
article/version attribution must be reconciled and two labelled simply CC BY
without numbered version (10.12712/rpca.v14i1.38405 and
10.1590/1981-3821201900020001). The UFF publisher page confirms a broad
attribution licence but does not state a version in the record. This is a
licence-version identification issue, NOT an assertion of copyright violation.

## Implementation and fail-closed checks

- `scripts/build_reviewed_pdf_candidate.py` accepts only the exact
  selected source paths, sizes and hashes from the original catalogue, an
  explicit rights-review list and CC BY 4.0 source page evidence.
- The trial archive embeds **only** the selected PDFs and a filtered local
  catalogue. Its PDF reader prefers these exact local files; missing assets
  cannot silently fall back to the wider remote catalogue.
- Each binary is unchanged, and per-work third-party notices preserve
  authors/year/title/DOI, publisher, licence URL, rights evidence and SHA-256.
  The PDF copyright is separate from the Apache-2.0 software licence.
- The publisher-page documentary assessment was performed by an AI assistant,
  without any claim that every figure, page, edition or third-party material
  was independently audited by a human.
- Normal Skill installer remains unchanged and contains **no PDFs**. The
  separate PDF-bearing CI artifact is unambiguously marked TEST-ONLY.

## Completion requirements before general distribution

- Verify each of the 29 selected articles against the **exact edition** and
  embedded copyright/credit notices, with special attention to exceptions
  involving third-party images and figures. Extend the review to remaining
  20 CC BY 4.0 candidates and two version-unresolved CC BY works as evidence
  becomes available; do not bulk-grant rights by directory name.
- Complete historical rights risk decision in Issue #102 and private-file
  metadata/privacy assessment in Issue #103.
- Clean-install the PDF-bearing archive in the actual host; confirm size
  compatibility, offline PDF lookup, presentation-layer integrity, source
  attribution and expected scientific limits.
- Provide a contact/takedown procedure as a supplementary channel, not as
  a replacement for pre-publication licences or rights review.
- Only after release gates are satisfied obtain separate written maintainer
  authorization to merge, tag and distribute.

**Decision:** technical packaging and rights review underway; no public stable
release, human rights attestation, private PDF inclusion or scientific approval.
