# PPGA bibliography reconciliation — inspection checkpoint (22 Nov 2026)

**Status: PARTIAL_MATCHING — NO AUTOMATIC DEDUPLICATION OR PROMOTION.** This note is an audit of bibliographic-record metadata and selected filename-level comparisons, not a complete file-by-file identity certificate.

## What is verified

- The Google Drive PPGA supplementary archive has **475 file entries** across 70 topic folders and five nested folders, as enumerated in the intake. These are file objects, not certified unique scholarly works.
- The public GitHub source registry currently has **475 SRC entries**: **132** labeled `SOURCE_PDF_WORK_VERIFIED`, **343** labeled `CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED`; neither category implies scientific peer review.
- Operational dispositions: **474 `VALIDADO_COM_RESTRICOES`**, one `EXCLUIDO_COM_JUSTIFICATIVA` (**SRC-0385**). This is an operational status, not primary scientific [L] evidence.
- Normalizing case, accents, punctuation and whitespace in the existing GitHub source titles reveals **13 repeated-title groups involving 27 SRC records** — 14 surplus catalogue entries relative to one record per distinct normalized title. This finding does **not** establish identical file bytes, edition, licence or scholarly identity.
- The source registry explicitly marks only one `work_duplicate_of` link (`SRC-0337 → SRC-0206`); both records have the same directly checked DOI **10.1590/S0034-759020140211** and year **2014**, which corroborates bibliographic work identity (not identical PDF bytes). Do not invent the other links.

## Duplicate-title groups in the existing SRC registry

| SRC records to reconcile | Repeated source title | Current category (sample) | Evidence caveat |
|---|---|---|---|
| SRC-0006, SRC-0435 | Comparative political research designs | Política Comparada | Check individual edition and source |
| SRC-0111, SRC-0454 | Participant observation principles | Observação Participante | Check individual edition and source |
| SRC-0129, SRC-0132 | Thematic analysis applications in administration | Análise Temática | Check individual edition and source |
| SRC-0206, SRC-0337 | Images as social-science research data | Imagem como dado | May have inspected source metadata |
| SRC-0230, SRC-0344 | Bibliometric analysis of jurimetrics in Brazil | Jurimetria | Check individual edition and source |
| SRC-0235, SRC-0267 | Quantitative and qualitative techniques for policy impact evaluation | Avaliação de Impacto | Check individual edition and source |
| SRC-0244, SRC-0371 | Nonparametric automated content analysis | Texto como Dado (text mining) | Check individual edition and source |
| SRC-0245, SRC-0370 | Text as data and automated political-text analysis | Texto como Dado (text mining) | Check individual edition and source |
| SRC-0349, SRC-0391 | Matching for time-series cross-sectional causal inference | Regressão de Painel | Check individual edition and source |
| SRC-0354, SRC-0438 | Methodological weaknesses of Brazilian political science | Epistemologia | Check individual edition and source |
| SRC-0372, SRC-0373 | Constructing content-analysis categories | Análise de Conteúdo | Check individual edition and source |
| SRC-0402, SRC-0430, SRC-0434 | Introduction to research methods in political science | Regressão linear | Check individual edition and source |
| SRC-0406, SRC-0408 | Survival analysis and Cox regression | Análise de Sobrevivência | Check individual edition and source |

## DOI-level spot check of the 13 repeated-title groups

Only **one pair**, `SRC-0206` / `SRC-0337`, currently exposes the same nonempty original-work DOI in *both* SRC records. In several other pairs only one record has a verified DOI or none has one, so title-normalization alone cannot authenticate a work identity. Mark the other groups `REQUIRES_SOURCE_EDITION_CHECK`; do not infer that each is a distinct work or an identical version.

## Selected cross-folder / same-name warnings from the Drive listing

- Grimmer & Stewart (2013) appears under text-as-data and content-analysis folders; compare existing `SRC-0245` / `SRC-0370` against actual PDFs and DOIs.
- Hopkins & King (2010) appears under those two topic folders; compare `SRC-0244` / `SRC-0371`.
- Imai, Kim & Wang (2023) appears under panel-regression and matching folders; compare `SRC-0349` / `SRC-0391`.
- Original file names such as `01_Introduction.pdf`, `02_two_by_two.pdf`, `celina.pdf`, `000633536.pdf` and several author/year-only names are not enough to authorize unique work identity.
- Similar author/year labels can refer to **different** studies; do not merge on name resemblance. Distinct language editions/translations should be retained as editions when relevant.

## Overlap triage: 50 new staged PPGA candidate cards versus 174 pre-existing editorial cards

These six cases merit human comparison first. They are **possible complementary or redundant topic-level guidance**, not automatically identical records:

1. `ppga-feminist-epistemology` versus `source-review-0036.md` and `lazar-2007-feminist-critical-discourse.md`.
2. `ppga-online-focus-groups` versus `focus-group-design.md`.
3. `ppga-qualitative-validation-transparency` versus `qualitative-design-quality.md` and `nowell-2017-trustworthy-analysis.md`.
4. `ppga-dresch-lacerda-antunes-design-science` versus `design-science.md`, Hevner and Peffers cards.
5. `ppga-cluster-analysis` versus `source-review-0401.md`.
6. `ppga-correspondence-analysis` versus `source-review-0239.md` / `source-review-0240.md`.

## Next concrete operations (not performed here)

1. Create an **internal, non-public** work/edition/DOI/actual-file-hash correspondence ledger for all 475 items; keep private Drive locators outside public Git.
2. Resolve 13 repeated-title groups and the especially ambiguous file names using PDF front matter, DOI and actual source bytes; do not delete any SRC pending evidence.
3. Compare all 50 candidate cards against the 174 existing editorial cards, consolidate redundant method-selection guidance and verify the original source before upgrading [P] to [I] or [L].
4. Review English prose in active methodology cards (currently outside the source-language scanner), editorial/rights clearance and catalog/hash controls before activating cards.

**Safeguards:** No third-party protected PDF, private Drive locator or manuscript material was published; no SRC or existing card was deleted; scientific researcher gates remain `PENDING`. This checkpoint neither merges the Draft PR nor changes the released Skill.

## Reproducible deterministic check (repository metadata only)

Group `knowledge/methodology/source_registry_catalog.json:documents` by `title` after Unicode NFD deaccenting, lowercasing and replacement of punctuation with spaces. Keep groups of size > 1, excluding titles shorter than 18 normalized characters. This yielded 13 groups / 27 entries on the observed registry snapshot. Edition and PDF identity must be checked separately.

## Editorial overlap triage — six PPGA candidates (2026-11-22)

These are non-scientific, metadata-and-prose-level scope judgments; no candidate is activated.

| PPGA candidate | Triage | Existing active relationship |
|---|---|---|
| `ppga-online-focus-groups` | `RETAIN_AS_DISTINCT_MODALITY` | The existing focus-group-design |
| `ppga-feminist-epistemology` | `RETAIN_AS_DISTINCT_METHOD_CHOICE` | Existing source-review-0036 |
| `ppga-dresch-lacerda-antunes-design-science` | `HOLD_FOR_SOURCE_EDITION_AND_SCOPE` | Existing design-science |
| `ppga-cluster-analysis` | `RETAIN_AS_DISTINCT_METHOD_CHOICE` | Existing source-review-0401 |
| `ppga-correspondence-analysis` | `RETAIN_AS_DISTINCT_METHOD_CHOICE` | Existing source-review-0239 |
| `ppga-qualitative-validation-transparency` | `RETAIN_AS_DISTINCT_CROSS_TRADITION_CHECK` | Existing qualitative-design-quality |

All six now carry their provisional disposition inside the draft card itself; no active card, source PDF, scientific gate or published catalog was changed.
