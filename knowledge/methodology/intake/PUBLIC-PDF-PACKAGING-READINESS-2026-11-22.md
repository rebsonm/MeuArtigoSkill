# Public PDF packaging readiness — pre-release rights and integrity preflight

**Date:** 2026-11-22. **Target:** stand-alone Meu Artigo Skill for researchers. This is a SOURCE-ONLY AUDIT RECORD, not release clearance.

## Observed inventory (from immutable branch catalogue and GitHub content listing)

- Catalogue: **51** publicly indexed third-party PDF binaries, **49 declared CC BY 4.0** and **2 declared CC BY (version unspecified in catalogue)**.
- Repository PDF directory: **51 actual PDF file entries**, matching the catalogue path list and recorded byte sizes according to GitHub directory metadata; **41,272,465 raw bytes (~39.36 MiB)**.
- Each public catalogue record contains a source URL, a claimed rights-evidence URL, license reference, DOI, title/authors/year, recorded SHA-256 and file size. **Per-byte SHA-256 checking is a separate CI step**; this report does not invent a checksum verification or independent publisher-license adjudication.
- Source-inventory ledger: **475** private catalogue records, **17** with document-specific positive rights evidence, **458** otherwise NOT_CHECKED. **16** of the 17 were indexed as licensed source copies and **one** (World Bank manual) was kept publisher-link-only. Do not add 17 to the public 51: these are different overlapping accountings.
- Installed RC.1 ZIP currently contains **no PDFs** by explicit allowlist. The maintainer has asked for PDFs in general distribution, with a takedown mechanism; such a mechanism is supplemental and NOT permission to distribute unlicensed material.
- The software's Apache-2.0 license applies to the software **only**, not to third-party articles.

## Publisher-check follow-up (two unversioned licence declarations)

1. `silva-barbosa-lima-2020-analise-tematica-administracao.pdf`, DOI `10.12712/rpca.v14i1.38405` — article publisher <https://periodicos.uff.br/pca/article/view/38405> declares Creative Commons Attribution and permission to distribute and adapt, including commercial use, provided authorship is credited. The exact numbered license revision and edition-specific PDF need final checking; **do not silently re-label as CC BY 4.0**.
2. `figueiredo-filho-et-al-2019-seven-reasons-transparency.pdf`, DOI `10.1590/1981-3821201900020001` — journal article on SciELO <https://www.scielo.br/j/bpsr/a/sytyL4L63976XCHfK3d7Qjh/?format=html&lang=en> states Creative Commons Attribution with unrestricted sharing and proper citation. The catalogue says `CC BY` (unversioned) and provides the CC BY 4.0 license URL; reconcile the precise edition/license version before promoting to an exact-version label.

Both are **license-version review cases**, not allegations of infringement or findings that the articles are ineligible.

## Publication blockers and next actions

1. Confirm **exact source-specific redistribution rights** and mandatory notices for candidate binaries. Catalogue claims and website links are evidence leads, not a new independent legal opinion. Recheck the exact version, publisher page, original PDF notices, translations, figures and third-party elements.
2. Perform full SHA-256 and size comparison of every public PDF to the recorded catalogue values. CI runs `python scripts/audit_public_pdf_release.py --verify-only`; this only certifies the bytes, not the copyright.
3. Generate an explicit per-work attribution manifest, including authors, year, title, DOI/source URL, correct license and URL, retained copyright notices, changes (none if exact original), and takedown contact/process. The source-only script offers `--out-credits` to prepare a **DRAFT**, never a legal approval.
4. Determine a safe, supported public installer capacity for the ~41 MiB uncompressed PDF set; do not assume all hosts accept the resulting ZIP.
5. Handle outstanding historical rights exposure in [Issue #102](https://github.com/rebsonm/MeuArtigoSkill/issues/102), private-file metadata in [Issue #103](https://github.com/rebsonm/MeuArtigoSkill/issues/103), and final author/maintainer release sign-off. No historical rewrite, public release or user ACL changes are authorized by this preflight.
6. For the 458 inventory entries with no verified redistribution rights, publish citation metadata/link **only** until source-specific clearance; do not copy private-source PDFs into the public Skill.

## Public PDF register — SHA-256 prefixes for quick lookup

Each row is a **candidate record**, not permission granted by this audit. Full hashes are retained in `knowledge/methodology/pdf_catalog.json`.

| # | Public PDF basename | DOI | Declared license | Review disposition | Publisher evidence | SHA-256 prefix |
|---:|---|---|---|---|---|---|
| 1 | `lycariao-roque-costa-2023.pdf` | `10.1590/2318-0889202335e220027` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://periodicos.puc-campinas.edu.br/transinfo/article/view/10064) | `37c3906ba2ac3982…` |
| 2 | `paranhos-et-al-2016.pdf` | `10.1590/15174522-018004221` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://www.scielo.br/j/soc/a/WtDMmCV3jQB8mT6tmpnzkKc/?format=html&lang=pt) | `36cfd9c1ce8313c7…` |
| 3 | `maia-bezerra-2020.pdf` | `10.20396/rdbci.v18i0.8658889` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://periodicos.sbu.unicamp.br/ojs/index.php/rdbci/copyright) | `b9160abe4e696547…` |
| 4 | `bicudo-2014.pdf` | `10.5007/1981-1322.2014v9nespp7` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://periodicos.ufsc.br/index.php/revemat/article/view/1981-1322.2014v9nespp7) | `0a1bc9ab6316d1d1…` |
| 5 | `prigol-behrens-2019.pdf` | `10.1590/2175-623684611` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://www.scielo.br/j/edreal/a/rDDFsHvBCQyWKpthzPjMGzk/?format=html&lang=pt) | `01bce687bc27e3d3…` |
| 6 | `lopez-bernal-cummins-gasparrini-2017.pdf` | `10.1093/ije/dyw098` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://pmc.ncbi.nlm.nih.gov/articles/PMC5407170/) | `9232ae91f9cdb1de…` |
| 7 | `harrison-birks-franklin-mills-2017.pdf` | `10.17169/fqs-18.1.2655` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://researchonline.jcu.edu.au/47422/) | `3918abd6dc74255c…` |
| 8 | `guest-namey-chen-2020-saturation.pdf` | `10.1371/journal.pone.0232076` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/plosone/s/licenses-and-copyright) | `becf8d627dba454e…` |
| 9 | `pautasso-2013-literature-review.pdf` | `10.1371/journal.pcbi.1003149` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/s/licenses-and-copyright) | `c8b15037bfc77e25…` |
| 10 | `mensh-kording-2017-paper-structure.pdf` | `10.1371/journal.pcbi.1005619` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/s/licenses-and-copyright) | `f02a2c14c630369f…` |
| 11 | `sandve-et-al-2013-reproducible-research.pdf` | `10.1371/journal.pcbi.1003285` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/s/licenses-and-copyright) | `35648a3880bdd8bf…` |
| 12 | `forero-et-al-2019-meta-analysis.pdf` | `10.1371/journal.pcbi.1006922` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/s/licenses-and-copyright) | `412601e19c72d269…` |
| 13 | `byrne-2022-reflexive-thematic-analysis.pdf` | `10.1007/s11135-021-01182-y` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://link.springer.com/article/10.1007/s11135-021-01182-y) | `fbe98aa82d7caea7…` |
| 14 | `vikan-et-al-2025-llm-rta.pdf` | `10.1177/10497323251365211` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.sagepub.com/doi/10.1177/10497323251365211) | `8432987a7e7a95ad…` |
| 15 | `plos-pone-0181689.pdf` | `10.1371/journal.pone.0181689` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0181689) | `cfcab6a0959325bc…` |
| 16 | `plos-pone-0210776.pdf` | `10.1371/journal.pone.0210776` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0210776) | `6a9bea29d0eca26a…` |
| 17 | `plos-pone-0270673.pdf` | `10.1371/journal.pone.0270673` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0270673) | `c1f0a77321a270f4…` |
| 18 | `plos-pone-0331666.pdf` | `10.1371/journal.pone.0331666` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0331666) | `90fb1b49689dc792…` |
| 19 | `plos-pone-0289695.pdf` | `10.1371/journal.pone.0289695` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0289695) | `bd11421a17ceacc2…` |
| 20 | `plos-pone-0283092.pdf` | `10.1371/journal.pone.0283092` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0283092) | `92847729cc91ccf7…` |
| 21 | `plos-pcbi-1004961.pdf` | `10.1371/journal.pcbi.1004961` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004961) | `527fc8f7054f80b2…` |
| 22 | `plos-pcbi-1012179.pdf` | `10.1371/journal.pcbi.1012179` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012179) | `e887af39e1982b7e…` |
| 23 | `plos-pcbi-1014882.pdf` | `10.1371/journal.pcbi.1014882` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014882) | `6992aafd1be44a31…` |
| 24 | `plos-pcbi-1008938.pdf` | `10.1371/journal.pcbi.1008938` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008938) | `05ae04660633fe3a…` |
| 25 | `plos-pcbi-1006508.pdf` | `10.1371/journal.pcbi.1006508` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006508) | `ae64e526caa2ad52…` |
| 26 | `plos-pcbi-1004385.pdf` | `10.1371/journal.pcbi.1004385` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004385) | `24ebd796f1315d61…` |
| 27 | `plos-pcbi-1006379.pdf` | `10.1371/journal.pcbi.1006379` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006379) | `3bfbea8bee896869…` |
| 28 | `plos-pcbi-1010139.pdf` | `10.1371/journal.pcbi.1010139` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010139) | `4588713574299621…` |
| 29 | `plos-pcbi-1005412.pdf` | `10.1371/journal.pcbi.1005412` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005412) | `002081be65fbd42c…` |
| 30 | `plos-pcbi-1007846.pdf` | `10.1371/journal.pcbi.1007846` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007846) | `67cdeb70bbb0697d…` |
| 31 | `plos-pcbi-1006036.pdf` | `10.1371/journal.pcbi.1006036` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006036) | `093a8ad0fd8501b8…` |
| 32 | `plos-pcbi-1010749.pdf` | `10.1371/journal.pcbi.1010749` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010749) | `91f24205d1559622…` |
| 33 | `plos-pcbi-1014419.pdf` | `10.1371/journal.pcbi.1014419` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014419) | `ad679a03d64fbbed…` |
| 34 | `dias-mishima-2023-thematic-analysis.pdf` | `10.12957/sustinere.2023.71828` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://doi.org/10.12957/sustinere.2023.71828) | `9d623d1f2e22d8d9…` |
| 35 | `campos-saidel-2022-qualitative-sampling.pdf` | `10.33361/RPQ.2022.v.10.n.25.545` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://editora.sepq.org.br/rpq/article/view/545) | `b3e78db1e163a787…` |
| 36 | `koerich-et-al-2009-action-research.pdf` | `10.5216/ree.v11.47234` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://revistas.ufg.br/fen/article/view/47234) | `178ca5ae19c4e3fb…` |
| 37 | `marzi-balzano-caputo-pellegrini-2025-bslr.pdf` | `10.1111/ijmr.12381` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://onlinelibrary.wiley.com/doi/10.1111/ijmr.12381) | `0a40cb1cdf36acff…` |
| 38 | `jaakkola-2020-designing-conceptual-articles.pdf` | `10.1007/s13162-020-00161-0` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://link.springer.com/article/10.1007/s13162-020-00161-0) | `3ec15c06890a7130…` |
| 39 | `schroeder-lequere-randazzo-mimno-schoenebeck-2025-llm-qualitative.pdf` | `10.1145/3706598.3713120` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://doi.org/10.1145/3706598.3713120) | `1e0580e558bd2a12…` |
| 40 | `mayring-2025-chatgpt-content-analysis.pdf` | `10.17169/fqs-26.1.4252` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://www.qualitative-research.net/index.php/fqs/article/download/4252/5160/19733) | `224084ab56a7c51c…` |
| 41 | `costa-bryda-christou-kasperiuniene-2025-ai-coresearcher.pdf` | `10.1177/16094069251383739` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://doi.org/10.1177/16094069251383739) | `46cc9ba2e44ea25c…` |
| 42 | `nguyen-trung-2025-guided-ai-thematic-analysis.pdf` | `10.1007/s11135-025-02165-z` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://doi.org/10.1007/s11135-025-02165-z) | `cc1a9a2eeae764d1…` |
| 43 | `dahal-et-al-2025-metacrisis-generativity.pdf` | `10.3389/frma.2025.1685968` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://doi.org/10.3389/frma.2025.1685968) | `4dbdd0b4a8928a75…` |
| 44 | `jowsey-et-al-2025-frankenstein-thematic-appraisal.pdf` | `10.1371/journal.pone.0330217` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://doi.org/10.1371/journal.pone.0330217) | `c9534d54e5d16ae5…` |
| 45 | `castellanos-et-al-2025-llm-thematic-summarization.pdf` | `10.2196/64447` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://ai.jmir.org/2025/1/e64447) | `afe781822e0637a1…` |
| 46 | `messner-smith-richards-2025-epistemological-incongruences.pdf` | `10.1177/16094069251371481` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://doi.org/10.1177/16094069251371481) | `af28adfce56d6ce3…` |
| 47 | `eschrich-sterman-2024-llm-qualitative-framework-arxiv-v1.pdf` | `10.48550/arXiv.2407.11198` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://arxiv.org/abs/2407.11198) | `2c4e1e1e012a5fda…` |
| 48 | `silva-barbosa-lima-2020-analise-tematica-administracao.pdf` | `10.12712/rpca.v14i1.38405` | CC BY | REVIEW_VERSION | [Publisher](https://periodicos.uff.br/pca/article/view/38405) | `ba56e9b7fff572af…` |
| 49 | `figueiredo-filho-et-al-2019-seven-reasons-transparency.pdf` | `10.1590/1981-3821201900020001` | CC BY | REVIEW_VERSION | [Publisher](https://www.scielo.br/j/bpsr/a/sytyL4L63976XCHfK3d7Qjh/) | `c2dc25fc39a0782b…` |
| 50 | `atkinson-2023-mca-versus-catpca.pdf` | `10.1007/s11135-023-01669-w` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://doi.org/10.1007/s11135-023-01669-w) | `a31b1304cf1fa0e0…` |
| 51 | `guedes-neto-2026-experimentos-survey-administracao.pdf` | `10.1590/0034-761220250695` | CC BY 4.0 | CANDIDATE_NOT_CLEARANCE | [Publisher](https://periodicos.fgv.br/rap/article/view/99745) | `e0a3ae577c946ad4…` |

## Status

**PUBLIC_RELEASE_RIGHTS_CLEARANCE = PENDING**.

A technical-archive build incorporating PDFs, if later prepared, must be clearly marked **test-only** until full per-file rights evidence, precise attribution, host-size acceptance, history/privacy remediation, and final release authorization are recorded. No scientific gates were approved.
