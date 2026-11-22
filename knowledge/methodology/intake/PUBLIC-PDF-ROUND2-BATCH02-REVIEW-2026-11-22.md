# Public PDF inclusion — round 2, batch 02/04 (five additional CC BY 4.0 catalogue entries)

**Date:** 2026-11-22 (America/Fortaleza). **Project:** `rebsonm/MeuArtigoSkill`, PR #112 (Draft). **Frozen audit inputs:** PR head `e1a1da185185fc4ea7b67124eb6ce4b3eabd44a9`; `knowledge/methodology/pdf_catalog.json` and `PUBLIC-PDF-TEST-APPROVALS-2026-11-22.json` from that commit. **Disposition:** `DOCUMENTARY_BATCH_REVIEWED; NO_PUBLIC_DISTRIBUTION_CLEARANCE`. This report is not a legal opinion or permission from rightsholders.

## Deterministic inclusion/exclusion

Selected the **next five, in original catalogue order**, among the 20 catalogue entries marked `CC BY 4.0` but *not* included in the original 29-entry TEST-ONLY allowlist, after subtracting the five covered by `PUBLIC-PDF-ROUND2-BATCH01-REVIEW-2026-11-22.md`. Catalogue indices: **13, 14, 34, 35, 37**. This is batch 2/4, not a review or alteration of the 29 already-packaged PDFs, the two catalogue entries with unversioned CC BY, or the 475 private inventory PDFs.

## Verification method and limits

1. Independently consulted primary editor/journal pages, accessible published PDFs, archive pages and DOI cross-references for authors, title, DOI, year/volume, licence and component provenance. Limited visual checks on PDF pages (including first pages of Sustinere, RPQ and Wiley); where a PDF could not be rendered reliably, publisher HTML and text were used. No full page-by-page third-party rights clearance.
2. Retrieved GitHub binary content at a *pinned commit* using `fetch_file(encoding=base64)` for these five paths. **Three** payloads were returned completely; Base64 decoded, SHA-256 recomputed locally with implementation tested on known SHA-256 vector `abc`, sizes and `%PDF-` headers matched the catalog. For **Byrne and Vikan**, the Github file tool exposed blob SHA-1 but not complete base64 bytes (likely endpoint >1MB limitation); these two were **NOT independently rehashed in this review**.
3. Separately confirmed GitHub Actions Release audit run [#44984430160](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/44984430160) of pinned input head: `Verify every catalogued public PDF against its SHA-256` **SUCCESS**, with job log reporting 51 catalogue paths, 51 files, 41,272,465 bytes, `integrity_status=PASS` and `release_clearance=BLOCKED_PENDING_INDEPENDENT_RIGHTS_REVIEW`. This is **CI-level checksum evidence for all five**, not an independent second rehash of the two large ones. Do not substitute source catalog hash for a hash of the publisher's separately downloaded exact PDF; **publisher-vs-GitHub binary equality remains unverified for all five**.
4. Third-party visuals/figures, instruments, excerpts and data inherit the article's CC licence **only to the extent actually covered**; no blanket presumption of coverage or infringement. Source evidence is a locator and provisional judgement, not legal authorization.

## Individual rights/edition/attribution ledger

### 06/20 — Byrne 2022, catalogue index 13

- **File:** `knowledge/methodology/pdfs/byrne-2022-reflexive-thematic-analysis.pdf`
- **Attribution:** David Byrne. *A worked example of Braun and Clarke's approach to reflexive thematic analysis*. *Quality & Quantity*, 56, 1391–1412 (2022). DOI [10.1007/s11135-021-01182-y](https://doi.org/10.1007/s11135-021-01182-y).
- **Primary edition/rights:** [Springer article](https://link.springer.com/article/10.1007/s11135-021-01182-y) specifies online publication **26 June 2021**, print issue **June 2022** and article-level **CC BY 4.0**. Springer expressly says that images/other third-party content are under the article's licence unless a specific credit line states otherwise; if excluded, permission may be needed. The available article text does not establish that *every* possible credit line was checked. The GitHub catalogue itself notes **research-archive copy** and explicitly **no independent binary comparison** against the publisher version.
- **Third-party items/exception review:** example depends on prior research and cited Braun & Clarke work; no independently verified exemption-free inventory of figures, quoted participant data or supplemental materials. Presence of citations alone does not imply a licence conflict.
- **Catalog SHA-256:** `fbe98aa82d7caea73f1bad2785eabe70c88c58a6f4b4037d8cb1d331f3abab3c`; **2,860,307 bytes**. GitHub returned blob SHA-1 `3ac57aadc39c2788b832390a439eeb0b13ae220e`. **Independent rehash: NOT COMPLETED (bytes unavailable from this API). CI 51/51 PASS.**
- **Disposition:** `CONDITIONAL_SOURCE_RIGHTS_AND_COPY_EQUIVALENCE`; do not move into TEST-ONLY until exact archived copy, third-party credits and source notices are checked.

### 07/20 — Vikan et al. 2025 (online), catalogue index 14

- **File:** `knowledge/methodology/pdfs/vikan-et-al-2025-llm-rta.pdf`
- **Attribution:** Magnhild Vikan; Ramtin Aryan; Mari Serine Kannelønning; Michael Alexander Riegler; Stein Ove Danielsen. *Reflecting on LLM Support in Reflexive Thematic Analysis: An Exploratory Study*. *Qualitative Health Research*, online **8 September 2025**, later indexed in **vol. 36(2–3), 191–205 (2026)**. DOI [10.1177/10497323251365211](https://doi.org/10.1177/10497323251365211). Preserve the distinction between electronic-publication year and issue year; never call a mismatched date an error without checking edition.
- **Primary edition/rights:** [SAGE published article](https://journals.sagepub.com/doi/10.1177/10497323251365211) explicitly attributes © authors **2025**, **CC BY 4.0**; [PMC copy](https://pmc.ncbi.nlm.nih.gov/articles/PMC12949038/) corroborates article/DOI/year. Supplemental materials are a separate scope.
- **Third-party items/exception review:** Figure 1 (tests 1–7), Figure 2 (main results), Tables 1–2 and supplemental prompts are present in the editor text, but independently establishing all graphic/data rights and exact-archive-copy provenance remains pending. No inference that these are infringing.
- **Catalog SHA-256:** `8432987a7e7a95ad035bd55ab0d46e6c8f7eb311f9ed624b11bd195b96f5cfa7`; **1,063,915 bytes**. GitHub blob SHA-1 `1644de4406c345852f540cdee4f8ec95478f2d5a`. **Independent rehash NOT COMPLETED (bytes unavailable from this API); CI 51/51 PASS.**
- **Disposition:** `CONDITIONAL_SOURCE_RIGHTS_AND_COPY_EQUIVALENCE`; resolve year-of-issue credit and figures/data before trial inclusion.

### 08/20 — Dias & Mishima 2023, catalogue index 34

- **File:** `knowledge/methodology/pdfs/dias-mishima-2023-thematic-analysis.pdf`
- **Attribution:** Ernandes Gonçalves Dias; Silvana Martins Mishima. *Análise temática de dados qualitativos: uma proposta prática para efetivação*. *Revista Sustinere*, **11(1), 402–411 (2023)**. DOI [10.12957/sustinere.2023.71828](https://doi.org/10.12957/sustinere.2023.71828).
- **Primary edition/rights:** [UERJ/Sustinere article](https://www.e-publicacoes.uerj.br/sustinere/article/view/71828) presents journal attribution **CC BY 4.0**; the [official PDF](https://www.e-publicacoes.uerj.br/sustinere/article/download/71828/47206/272585) opens with the DOI, title, authors and journal pagination.
- **Third-party items/exception review:** PDF **Quadro 1** gives selected statements and a table from 2018 professional master's dissertation research, credited to the authors and that source; provenance, consent/quotation permissions and rights for any materials not owned by authors have not been independently checked. This is a *documentation obligation*, not a finding of violation.
- **Catalog SHA-256:** `9d623d1f2e22d8d93b571ded0eb9f34e5b6062669ee32f47f12fca67aad97d7a`; **433,874 bytes**. **INDEPENDENT SHA-256 MATCH**, size and `%PDF-` header MATCH.
- **Disposition:** `CONDITIONAL_QUADRO1_PROVENANCE_AND_EXACT_COPY`.

### 09/20 — Campos & Saidel 2022, catalogue index 35 — licence contradiction

- **File:** `knowledge/methodology/pdfs/campos-saidel-2022-qualitative-sampling.pdf`
- **Attribution:** Claudinei José Gomes Campos; Maria Giovana Borges Saidel. *Amostragem em investigações qualitativas: conceitos e aplicações ao campo da saúde*. *Revista Pesquisa Qualitativa*, **10(25), 404–424 (2022)**. DOI [10.33361/RPQ.2022.v.10.n.25.545](https://doi.org/10.33361/RPQ.2022.v.10.n.25.545).
- **Primary edition/rights:** The [article page](https://editora.sepq.org.br/rpq/article/view/545) specifically shows **Creative Commons Attribution 4.0 International**, while the *same publication site* says in its general footer **“essa revista é licenciada ... 4.0, não-comercial”**. The [journal PDF](https://editora.sepq.org.br/rpq/article/download/545/337) opening page identifies the article, DOI and 2022 pagination but **does not resolve this site-wide CC BY vs non-commercial contradiction**. An article-specific notice may control over general boilerplate, but no definitive publisher clarification for this exact PDF/copy was obtained. **Do not automatically conclude CC BY-NC applies, nor ignore this discrepancy.**
- **Third-party items:** Limited accessible PDF text showed an essay with citations; did not locate an explicit figure caption in this limited scan, which is *not* a comprehensive absence-of-third-party-elements finding.
- **Catalog SHA-256:** `b3e78db1e163a787ec0ac08c44fca1cbb2c664f53564581128779c65a8ddd1a8`; **223,205 bytes**. **INDEPENDENT SHA-256 MATCH**, size and `%PDF-` header MATCH.
- **Disposition:** `BLOCKED_LICENSE_CONFLICT_PENDING_PUBLISHER_CLARIFICATION` for unrestricted public distribution or admission into a CC BY-only TEST-ONLY package. Request publisher clarification identifying exact work/edition and licence URL; no silent licensing metadata rewrite.

### 10/20 — Marzi et al. 2025, catalogue index 37

- **File:** `knowledge/methodology/pdfs/marzi-balzano-caputo-pellegrini-2025-bslr.pdf`
- **Attribution:** Giacomo Marzi; Marco Balzano; Andrea Caputo; Massimiliano M. Pellegrini. *Guidelines for Bibliometric-Systematic Literature Reviews: 10 steps to combine analysis, synthesis and theory development*. *International Journal of Management Reviews*, **27(1), 81–103 (2025)**. DOI [10.1111/ijmr.12381](https://doi.org/10.1111/ijmr.12381).
- **Primary edition/rights:** [Wiley publication](https://onlinelibrary.wiley.com/doi/10.1111/ijmr.12381) confirms bibliographic citation. [Author/institutional archived published-layout PDF](https://arts.units.it/bitstream/11368/3093458/3/Marzi-Balzano-Caputo-Pellegrini-IJMR-2025.pdf) first page identifies volume and pagination and states Creative Commons Attribution, © authors **2024** with **2025 issue**. A [university metadata record](https://ricerca.unityfvg.it/entities/publication/f77909ae-3cb1-47f4-b418-9e35faba3b2f/details) explicitly lists license URI `http://creativecommons.org/licenses/by/4.0/`; author [B-SLR site](https://www.b-slr.org/resources-for-authors) also asserts CC BY 4.0 (the website's own license may not independently govern every figure). Need exact publisher-vs-archive-vs-GitHub binary equality.
- **Third-party items:** Figure 1 depicts B-SLR workflow and tables/typologies reference other scholarly methods/software; independently confirm whether any logos, adapted graphics or licensed third-party visual assets occur in the *exact* PDF. No blanket third-party clearance derived from article-level CC terms.
- **Catalog SHA-256:** `0a40cb1cdf36acff0446d6d4ce80597ea64afbb4ffaf20b2df386c8f66ccf117`; **528,164 bytes**. **INDEPENDENT SHA-256 MATCH**, size and `%PDF-` header MATCH.
- **Disposition:** `CONDITIONAL_THIRD_PARTY_AND_EXACT_COPY`.

## Results and audit provenance

| Candidate | Bibliographic identity / edition | Licence evidence | Third-party / exception check | Direct GitHub SHA-256 this session | Publisher PDF byte-equivalence | Release status |
|---|---|---|---|---|---|---|
| Byrne 2022 | MATCH with online/issue year distinction | CC BY 4.0, Springer explicit | PARTIAL | NOT AVAILABLE; CI PASS | NOT VERIFIED | CONDITIONAL |
| Vikan et al. 2025 | MATCH online 2025 / issue 2026 | CC BY 4.0, SAGE explicit | PARTIAL | NOT AVAILABLE; CI PASS | NOT VERIFIED | CONDITIONAL |
| Dias & Mishima 2023 | MATCH DOI/volume/pages | CC BY 4.0, UERJ Sustinere | PARTIAL (Quadro 1) | MATCH | NOT VERIFIED | CONDITIONAL |
| Campos & Saidel 2022 | MATCH DOI/volume/pages | **CONFLICT** article CC BY 4.0 / journal footer non-commercial | PARTIAL | MATCH | NOT VERIFIED | **BLOCKED** |
| Marzi et al. 2025 | MATCH online 2024 / journal 2025 | CC BY 4.0, institutional metadata | PARTIAL | MATCH | NOT VERIFIED | CONDITIONAL |

**Technical inventory:** 5/5 have expected GitHub paths and blob IDs; current-head GitHub Actions public-PDF integrity is PASS for all 51 catalogue entries; 3/5 independently rehashed from returned bytes here, 2/5 not independently recalculated due to tool binary response size. **Rights:** 4 conditional, 1 blocked due to conflicting notices; **0 unrestricted clearances**, no review falsely attributed to human or publisher.

**Credits/attribution draft rule for future candidate:** retain full author list, title/year including online-versus-issue distinction when relevant, journal/volume/pages, DOI, copyright and exact article/source URL, appropriate CC BY 4.0 URI *only once scope is confirmed*, publisher and named third-party credit/restriction notices, identity of the actual delivered PDF (SHA-256) and whether any modification was made. Article CC does not cover protected external content marked as excluded.

**Remaining:** 10 CC BY 4.0 entries to review in lots 03/04 and 04/04; the two generic CC BY entries are in a separate reconciliation lane. 29-PDF TEST-ONLY bundle unchanged. Issues #102 (rights/history) and #103 (private locator history) remain separate release blockers. No release rights approvals, 7 scientific gates, corpus publication, ACL changes, force-push, merge, tag or stable release.

**Next action:** lot 03/04: next five eligible CC BY 4.0 entries in original catalogue order, excluding the 29 TEST-ONLY and first 10 already reviewed. Separately request editorial clarification on RPQ 2022 licence, keep index 35 blocked until recorded written evidence and owner decision.
