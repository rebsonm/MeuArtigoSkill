# PPGA PDF binary reconciliation — actual bytes and SHA-256 (22 November 2026)

**Status: SOURCE_FILE_BYTE_CHECKED — NOT SCIENTIFIC_ACCEPTANCE.** This report captures a bounded binary inspection of the original private PDF files, not a full methodological review, licence assessment or the identity of every one of 475 entries.

## Measured results

- **12** repeated-title groups remain after the SRC-0372 catalogue-title correction proposed in draft PR #117.
- **10 groups** contain byte-for-byte identical original PDFs, confirmed by raw file comparison and locally calculated SHA-256. These account for **11 redundant file-copy appearances** within the inspected groups; the triple-record group contributes two extra copies.
- **1 group** contains the same published thematic-analysis article and DOI but **two nonidentical PDF files** (aggregator version with cover vs journal-formatted version). Store as two provenance copies of one bibliographic work; do **not** claim binary identity.
- **1 group** shares a title and author but holds **different research outputs**: Cox-regression teaching slides and a journal article. Keep both type-specific bibliographic records, not one deduplicated paper.
- **SRC-0372 and SRC-0373** are distinct publications. They appeared as a false repeated-title pair because a stale title was stored in the registry; see draft PR #117. Do not count them here.

## Original-file hash results

| Source identifiers | Brief source label | Result | Source PDF size (bytes) | SHA-256 of original PDF |
|---|---|---|---:|---|
| SRC-0006, SRC-0435 | Comparative research design book | **Identical bytes** | 2535759 each | `fe1ba0c860a4c8b4fb23ecec3cbd6701d5a63a0a7702d82ab01805542eec7c04` |
| SRC-0111, SRC-0454 | Participant observation review | **Identical bytes** | 63385 each | `9b12a0c0f29cc77cbe06c20fd2b0fb2bba3ff1d20db14f677bfa87a937471036` |
| SRC-0129 | Thematic analysis in administration article — Open-access aggregator wrapper and article | **Distinct PDF** | 672728 | `ed2e37192bca40bce5b3ab5d456def4ff8acbf29b1570c4f8e442ecf039c01b7` |
| SRC-0132 | Thematic analysis in administration article — Journal-formatted article | **Distinct PDF** | 631240 | `ba56e9b7fff572af066706ddbe0d886f36eff0ecf8916227c1ff0ec7798a5870` |
| SRC-0206, SRC-0337 | Image research bibliographic review | **Identical bytes** | 230328 each | `9ec4986eacda3dfccc8ceef0b7f0f96198144fd9b61c3a81cf15954b51a1ab99` |
| SRC-0230, SRC-0344 | Bibliometric study of jurimetrics | **Identical bytes** | 574651 each | `b9160abe4e69654761076dc02a2edd6cfc114511d169c10b2c7d0194593edc84` |
| SRC-0235, SRC-0267 | Policy impact evaluation methods article | **Identical bytes** | 263280 each | `9a2d07e4f62edfa668bcf311e13920f99263c704a8187fae77065d0c1369674e` |
| SRC-0244, SRC-0371 | Automated nonparametric content analysis paper | **Identical bytes** | 528155 each | `cf7139ab385e44efb75e26e8c6334f1c959cceb5bb29010e4670f59070446d5d` |
| SRC-0245, SRC-0370 | Text-as-data promise and pitfalls paper | **Identical bytes** | 972383 each | `329b88773b6d4c1c82bba37f7f83b995add6f2e188f380eb332081da53ddd390` |
| SRC-0349, SRC-0391 | Time-series cross-sectional causal matching paper | **Identical bytes** | 889686 each | `a4f11f5d1a13bb4c150a3f4090f74aa522cf2f3e8276704847a9841d47153986` |
| SRC-0354, SRC-0438 | Brazilian political science methodological critique | **Identical bytes** | 120525 each | `c8d8e7792adc0bc8b8893f5a7ecd9b9cec3bf913429bf5ee80c9ac07019231b0` |
| SRC-0402, SRC-0430, SRC-0434 | Introduction to research methodology in political science | **Identical bytes** | 2633104 each | `daed917cbcca5ad77cfa3ac53150012600748cf235de376835e7d00990b8731b` |
| SRC-0406 | Cox regression teaching slides versus journal article — Slides, not a scholarly journal article | **Distinct PDF** | 602343 | `c02f5ce76ec9d4e0cfb1a1db35656f363faf936576c5aa2d5b6c4b08f1211782` |
| SRC-0408 | Cox regression teaching slides versus journal article — Journal article, 39 pages | **Distinct PDF** | 7569582 | `f7e29c1d52a6c860fac6a2321a78f1866a7f2477453a0516517385e2a476bbac` |

## Method and limitations

1. Original file identity was selected by the topic-folder file listing plus the existing `src-XXXX.md` documentary-provenance records (and source DOI where available). No source content was uploaded to the public GitHub repository.
2. PDFs were fetched directly from the user's connected private Drive. For purported duplicate copies, a byte-for-byte comparison of complete raw Base64 payloads verified equality. The raw bytes of locally mounted files were independently hashed with SHA-256. For the repeated three-copy source, both non-reference copies were compared against the same reference.
3. File hashes above are **PDF binary hashes**, not the `sha256` fields of the existing `source_registry_catalog.json` (which refer to source-card contents). Do not substitute one for the other.
4. The thematic pair was checked in both text fronts for the same title, authors and **DOI 10.12712/rpca.v14i1.38405**, and their SHA-256 values differ. The two Cox PDFs differ in bytes and in output type according to their title pages / documentary source cards.
5. This audit does not claim **a global 464-unique-file count** or any universal deduplication of all 475 sources; it only establishes findings for these 12 preselected title groups. Other matches across the entire archive may exist, and same-size alone never proves identical content.
6. All 475 SRC entries remain in place as provenance records; there is no automatic deletion, metadata reassignment beyond separate PR #117, change to active catalogue or scientific gate approval.

## Operational next step

Preserve all original SRC IDs as traceable inventory provenance. Design a **work-level alias layer** after source-card title correction and edition/right checks, optionally associating the 10 confirmed byte-equal groups without deleting independent directory locators. Compare the two thematic PDF versions as editions/packaging if page-specific citations matter. Do not consolidate the slides/journal pair at scholarly-work level. Separately review 50 PPGA methodological draft cards for content overlap and source-specific verification before any active promotion.
