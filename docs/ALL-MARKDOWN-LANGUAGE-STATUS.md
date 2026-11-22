# English migration status — all Markdown, not just docs

Date: 22 November 2026. This is a **partial implementation record**, not a
claim that the complete source tree has been translated or validated.

The Git tree inventory at the start of the work counted **853 Markdown files**
across root documentation, `docs/`, `references/`, `wiki/`, and the research
library. This includes 475 bibliographic prospecting cards and 174 editorial
methodology cards. The previous strict source-language scanner deliberately
exempted the methodology cards and intake records.

## Changes in this migration increment

- The three editorial cards on Snyder (2019), Grant and Booth (2009),
  and Jaakkola (2020) now contain English editorial prose.
- The SRC-0001 and SRC-0002 bibliographic prospecting cards have English
  editorial prose, without changing their source records or research status.
- Updated catalogue SHA-256 values track the exact changed card bytes.
- A comprehensive inventory script scans Markdown across **all** directories,
  including previously exempted cards, source cards and intake records.
- The policy and README no longer equate a narrow language gate with
  full Markdown language coverage.

Marzi et al. (2025) retains its previously reviewed Portuguese card because
the original correction and review receipt binds to its historic exact hash.
An English replacement would require fresh independent fidelity checks
before replacing the hash-bound card.

## Outstanding work and nonclaims

Remaining Markdown documents may still contain Portuguese editorial prose,
especially in historical research-intake notes and hundreds of method cards.
Use `python scripts/audit_all_markdown_language.py` and inspect its JSON
output to obtain the current candidate list; the present repository state
is **NOT** certified as English-only.

Bibliographic titles and direct source quotations stay in their original
language when necessary for provenance. Scientific decisions, seven human
gates and [L]/[I]/[P] classifications are unchanged. Immutable older Git
history and existing published release assets are not rewritten.

A review of translation fidelity is still needed before claiming full
English migration. This audit is not scientific review or a copyright check.

## Source-compared English editorial cards (22 November 2026)

Six additional, narrowly scoped methodological cards have been translated by
comparing the English wording directly against the existing Portuguese Markdown:
`source-review-0259.md`, `source-review-0298.md`,
`yin-2018-case-study-design.md`, `suddaby-2006-grounded-theory-not.md`,
`zupic-cater-2015-bibliometric-methods.md`, and
`donthu-2021-bibliometric-how-to.md`. Bibliographic identities, evidence
classification [I]/[P]/[L], limited source-reading scope and exact rights
boundaries were maintained. Historical scientific-review-pending identifiers
remain as technical provenance labels where used by the original cards.

These edits do not claim independent scholarly peer review. The original
649-card catalogue cardinality and all seven human scientific gates are
unchanged. A separate translation effort is tracked in PR #121 (bibliographic
prospecting cards) and PR #122 (remaining editorial cards). Those larger
machine-generated batches contain material translation errors and are **not
ready for merge** without substantive corrections.


## Bibliographic source-card translation batch (22 November 2026)

The 475-record source registry remains unchanged in cardinality. The source-card
machine translation branch reconciled **472 existing translated source cards**
against the operational ledger (649 total cards) and repaired 102 corrupted
machine-rendered status labels using original published records. Each of the
translated source records is explicitly marked **MACHINE_TRANSLATED_REVIEW_PENDING**
and links to its pre-translation public Git revision for comparison. Machine
translation has **not** been independently reviewed for methodological or legal
fidelity, and no [L] or scientific gate is approved. This notice does not
certify that all repository Markdown is English-only.

Source-card English editorial prose is a provisional aid and must not be
presented as an authoritative translation of any article, book, license, or
scientific finding. Where errors or ambiguous semantics persist, consult the
original and the public source registry.

## Editorial card machine-translation batch (22 November 2026)

This branch contains **110** provisional English machine-translated editorial
cards. A controlled integrity repair restored **40** corrupted scientific
status markers from the original Markdown record, and preserved **six**
previously source-compared English cards byte-for-byte. All 110 machine
translations remain **MACHINE_TRANSLATED_REVIEW_PENDING**; they are not
certified translations or independent scientific evaluations. The seven human
scientific gates and the 649-record library coverage do not change.

The source-of-truth notice in each translated card links to the corresponding
original public Portuguese record. Neither editorial translation nor exact
SHA-256 reconciliation grants rights to reproduce third-party PDFs.
