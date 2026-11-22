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
