# Public PDF packaging — Round 2, batch 01/04 (five of 20 CC BY 4.0 candidates)

**Date:** 2026-11-22 (America/Fortaleza). **Provenance:** `rebsonm/MeuArtigoSkill` PR #112, pre-audit HEAD `9ded032c467f6ca20fd97a9891175f5fac74ff74`. **Status:** DOCUMENTARY_CHECK_COMPLETE_WITH_CONDITIONS / NO_PUBLIC_RELEASE_APPROVAL.

## Scope and selection rule

First five documents **in `knowledge/methodology/pdf_catalog.json` order**, excluding the 29 `documents` paths already listed in `knowledge/methodology/intake/PUBLIC-PDF-TEST-APPROVALS-2026-11-22.json`. The two `CC BY` without version are outside this 20-document round. This report does not alter those lists.

Methods: GitHub API `fetch_file(encoding=base64, ref=9ded...)` of five actual public PDFs; Base64 decoded in memory; independently recomputed SHA-256 using a checked SHA-256 implementation (known vector "abc") and compared exact sizes/hash from the public catalog. Primary publisher pages and accessible PDF text inspected for authors/title/year/DOI/issue/licence and selected captions/source notices. **SHA-256 validates GitHub against its GitHub catalog; it DOES NOT prove bitwise identity with the publisher PDF.** No private Drive PDFs were accessed, reuploaded or disclosed.

## Per-document ledger (all statuses CONDITIONAL / NOT YET CLEARED)

### 01 — Lycarião, Roque & Costa (2023): systematic reviews and reliability

- **Catalog slot/path:** 1, `knowledge/methodology/pdfs/lycariao-roque-costa-2023.pdf`
- **Bibliography:** Diógenes Lycarião; Robson Roque; Débora Costa. *Revisão Sistemática de Literatura e Análise de Conteúdo na Área da Comunicação e Informação: o problema da confiabilidade e como resolvê-lo*. *Transinformação*, v.35, e220027 (2023), DOI [10.1590/2318-0889202335e220027](https://doi.org/10.1590/2318-0889202335e220027). [Publisher page](https://periodicos.puc-campinas.edu.br/transinfo/article/view/10064); [publisher/SciELO PDF locator](https://www.scielo.br/j/tinf/a/hX8CfMV7xgKV4JbghWL4yXJ/?format=pdf&lang=pt).
- **License/version:** Publisher directly states [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (publisher copyright note: 2023 Transinformação); individual edition/title/DOI/year align. License source independently inspected.
- **Third-party/components:** Text of accessible publisher PDF has Tables 1–4 credited “Elaborado pelos autores (2022)” and an original summarized protocol; no specific borrowed-image exclusion positively identified in this limited check. **Absence of an observed exception is not proof of exhaustive clearance.** Figures/tables/appendices/embedded fonts and edition-specific notices not certified item by item.
- **Hash/size:** 147563 bytes, `37c3906ba2ac39827ae1ae3c2066dd225c941f4d451cde65e6a09be2646651d6` — independently recalculated, **MATCH**.
- **Disposition:** `CONDICIONAL`. Need item-level exact-PDF publisher equivalence, third-party notices, and final credits/attribution review before expanding the test-only set.

### 02 — Paranhos et al. (2016): mixed methods

- **Catalog slot/path:** 2, `knowledge/methodology/pdfs/paranhos-et-al-2016.pdf`
- **Bibliography:** Ranulfo Paranhos; Dalson Britto Figueiredo Filho; Enivaldo Carvalho da Rocha; José Alexandre da Silva Júnior; Diego Freitas. *Uma introdução aos métodos mistos*. *Sociologias* 18(42), pp.384–411 (2016), DOI [10.1590/15174522-018004221](https://doi.org/10.1590/15174522-018004221). [SciELO publication page](https://www.scielo.br/j/soc/a/WtDMmCV3jQB8mT6tmpnzkKc/?format=html&lang=pt); [publisher PDF](https://www.scielo.br/pdf/soc/v18n42/1517-4522-soc-18-42-00384.pdf).
- **License/version:** Official SciELO page has a Creative Commons hyperlink **directly to CC BY 4.0**; metadata/title/issue/DOI consistent.
- **Third-party/components:** Figure 1 says “elaboração dos autores a partir de Gorard e Taylor (2004)”; three research-data tables cite Ipespe, *Barômetro de Pernambuco* (2008). Whether those underlying source elements require additional permission is **NOT independently certified**. Avoid assuming a broad article licence grants independent rights to underlying data/figures.
- **Hash/size:** 274339 bytes, `36cfd9c1ce8313c7fe753abcaf74cb1bb007cbe19b9a1cca1b4a397f68c3c7c4` — independently recalculated, **MATCH**.
- **Disposition:** `CONDICIONAL_TERCEIROS`; review adapted graphic, data acknowledgments and actual PDF/caption before packaging.

### 03 — Maia & Bezerra (2020): Brazilian jurimetry bibliometrics

- **Catalog slot/path:** 3, `knowledge/methodology/pdfs/maia-bezerra-2020.pdf`
- **Bibliography:** Marcos Maia; Cicero Aparecido Bezerra. *Análise bibliométrica dos artigos científicos de jurimetria publicados no Brasil*. *RDBCI*, v.18, e020018 (2020), DOI [10.20396/rdbci.v18i0.8658889](https://doi.org/10.20396/rdbci.v18i0.8658889). [Unicamp publisher page](https://periodicos.sbu.unicamp.br/ojs/index.php/rdbci/article/view/8658889); [publisher PDF](https://periodicos.sbu.unicamp.br/ojs/index.php/rdbci/article/download/8658889/22605).
- **License/version:** Article page explicitly displays **CC BY 4.0**, with copyright © 2020 Marcos Maia and Cicero Aparecido Bezerra.
- **Third-party/components:** Article PDF has credited adapted material: a research summary/table “adaptado de Machado (2017)”, a figure “adaptado de Vanti (2002)” and another figure “adaptado de Quoniam et al. (2001)”. Original work/underlying expression and the extent of license coverage were **not independently assessed**.
- **Hash/size:** 574651 bytes, `b9160abe4e69654761076dc02a2edd6cfc114511d169c10b2c7d0194593edc84` — independently recalculated, **MATCH**.
- **Disposition:** `CONDICIONAL_TERCEIROS`; require detailed attribution or exclusion rights review for adapted images/table before package admission.

### 04 — Prigol & Behrens (2019): grounded theory in education

- **Catalog slot/path:** 5, `knowledge/methodology/pdfs/prigol-behrens-2019.pdf`
- **Bibliography:** Edna Liz Prigol; Marilda Aparecida Behrens. *Teoria Fundamentada: metodologia aplicada na pesquisa em educação*. *Educação & Realidade* 44(3), 2019, DOI [10.1590/2175-623684611](https://doi.org/10.1590/2175-623684611). [Official SciELO article](https://www.scielo.br/j/edreal/a/rDDFsHvBCQyWKpthzPjMGzk/?format=html&lang=pt).
- **License/version:** SciELO’s Creative Commons Attribution link points to **CC BY 4.0**; DOI/title/year match the catalog.
- **Third-party/components:** Official article inventories **nine figures**. Figures 1–4 and 6–9 are credited to author-created graphics “com base em Charmaz (2009)”; Figure 5 “a autora”. This is derivative/intellectual-source attribution, not independent evidence that any figure infringes. Determine whether permissions or special notice are necessary for the exact diagrams/edition.
- **Hash/size:** 414982 bytes, `01bce687bc27e3d3c7014a1927fe906082ba50069c19b8744bab4ce2773fddce` — independently recalculated, **MATCH**.
- **Disposition:** `CONDICIONAL_TERCEIROS` pending diagram review and exact-copy/credit check.

### 05 — Harrison, Birks, Franklin & Mills (2017): case study research

- **Catalog slot/path:** 7, `knowledge/methodology/pdfs/harrison-birks-franklin-mills-2017.pdf`
- **Bibliography:** Helena Harrison; Melanie Birks; Richard Franklin; Jane Mills. *Case Study Research: Foundations and Methodological Orientations*. *Forum Qualitative Sozialforschung / Forum: Qualitative Social Research*, 18(1), Art.19 (2017), DOI [10.17169/fqs-18.1.2655](https://doi.org/10.17169/fqs-18.1.2655). [University repository record](https://researchonline.jcu.edu.au/47422/); [published-version PDF](https://researchonline.jcu.edu.au/47422/1/47422_Birks_2017.pdf).
- **License/version:** JCU explicitly describes the **published version** as CC BY 4.0; the PDF first page includes the CC BY 4.0 link. Title/authors/volume/article year consistent.
- **Third-party/components:** PDF Figure 1 on the history of case study research is credited “JOHANSSON (2003, p.7)” and described by authors as adapted for this discussion. **Do not assume the underlying figure is independently CC BY 4.0.**
- **Hash/size:** 202781 bytes, `3918abd6dc74255c4bf68075f1edc00528a46507fb0c97223e6ab4d3aee2ef5d` — independently recalculated, **MATCH**.
- **Disposition:** `CONDICIONAL_TERCEIROS` pending original figure source/permission and PDF-equivalence check.

## Cross-batch technical evidence and candidate credits

| Document | Original GitHub size | SHA256 catalog vs actual GitHub bytes | License primary | Borrowed components flag | Final distribution |
|---|---:|---|---|---|---|
| Lycarião–Roque–Costa 2023 | 147563 | MATCH | CC BY 4.0 publisher | no specific exception positively identified; full inspection pending | NOT CLEARED |
| Paranhos et al. 2016 | 274339 | MATCH | CC BY 4.0 SciELO link | adapted figure; research-data attribution | NOT CLEARED |
| Maia–Bezerra 2020 | 574651 | MATCH | CC BY 4.0 publisher | adapted figure(s)/table | NOT CLEARED |
| Prigol–Behrens 2019 | 414982 | MATCH | CC BY 4.0 SciELO link | author-created figures based on cited work | NOT CLEARED |
| Harrison et al. 2017 | 202781 | MATCH | CC BY 4.0 repository + PDF | Johansson (2003) adapted figure | NOT CLEARED |

**Integrity:** 5/5 SHA256 MATCH; 5/5 byte lengths MATCH; 5/5 PDF header `%PDF-`; no file edited, no catalog write, no ingestion into test package, no CI run in this batch. **Authorship/credit requirements:** display each full bibliographic author/title/year, DOI, publisher/journal, link to origin, correct CC BY 4.0 link, changes status (unmodified GitHub payload, but unverified against publisher), plus distinct credits/restrictions for borrowed figures and datasets, if permitted. Do not claim that `Apache-2.0` of the Skill licenses the research papers.

**Remaining:** 15 of the original 20 CC BY 4.0 candidates not covered by this round; plus the 2 unversioned CC BY records evaluated separately; 29 PDFs stay in a TEST-ONLY candidate. Historical rights Issue #102, private metadata Issue #103 and real-host installation remain independent blockers. No human rights review, GO, stable public release, merge, tag, rewriting Git history, change to scientific [L]/[I]/[P] or seven gates.

**Next operational action:** round 2 batch 02/04 — next five not-yet-selected CC BY 4.0 entries in unchanged original catalog order. Reuse this evidence scheme and only after complete edition/rights checks propose any expansion to the test-only set.
