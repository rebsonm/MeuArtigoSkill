# REG-013 — One-page scientific diagnostic

REG-013 is a **technical research-support diagnostic**, not editorial peer
review, independent study evaluation or certified scientific quality.

## Implemented behavior

- Read-only consolidation of the REG-018 bibliography and canonical citation
  audit, the REG-011 documented claim-to-passage review, and a limited
  structural inventory of decisions in the research protocol.
- Separate **objective blockers** from **items requiring human judgment**:
  outdated source verification, inconsistent references, unsupported links,
  uncertain source access, undeclared human reviews, and incomplete protocol
  records. A populated protocol cannot establish methodological adequacy.
- Deterministic sorting of up to six finding categories and four practical
  next actions, with complete category counts and an explicit omitted count.
  Repeated findings are grouped by category instead of creating long lists.
- Stable technical IDs and source-input SHA-256 hashes. The published report
  omits bibliographic titles, copyrighted passages, reviewer names,
  free-text rationales and internal source-file paths.
- Three outputs: compact Markdown (no more than 28 lines/3,300 characters),
  detailed structured JSON and print-friendly A4 HTML. Actual physical
  pagination depends on available fonts, browser and print settings.
- No changes to existing seven gates, canonical scientific files, recorded
  human decisions, or remote account data.

## Use after authorized access to a research project

    python scripts/scientific_diagnostic.py /authorized/project
    python scripts/scientific_diagnostic.py /authorized/project --format json
    python scripts/scientific_diagnostic.py /authorized/project \
      --format html --output 98_Technical_Reports/diagnostic.html

The optional separately declared human assessment input follows
docs/CLAIM-SEMANTIC-REVIEW-REG011.md:

    python scripts/scientific_diagnostic.py /authorized/project \
      --assessments 04_Evidencias_e_Sintese/assessment.json --strict

A missing or structurally invalid source, protocol, evidence register or
review is never silently replaced with fabricated results. Strict mode
returns exit code 2 when blocking findings or **required non-advisory**
technical/review conditions remain; an invalid input or execution error
returns 1. A lexical overreach hint alone (and an otherwise formally
recorded full-support declaration) does not make `--strict` fail.
Counts distinguish `blocking_occurrences`, `review_occurrences`,
`heuristic_advisory_occurrences` and `strict_required_occurrences`.
Exit code 0 is **not** a scientific correctness certificate, authenticated
human approval, or permission to submit.

Technical report exports are restricted to **new files directly inside**
`98_Technical_Reports/` in the authorized local project. They cannot
replace any canonical register, gate record, continuity document or other
existing file. Symlink and traversal attempts are denied. These files are
local and do not confirm Google Drive synchronization.

The compact report includes a coded REVIEW finding when a confirmed source
passage and its linked claim trigger an exploratory possible-overreach signal.
The signal requires review; it cannot independently decide semantic correctness,
evidence strength, causality or submission readiness.

## Limitations and acceptance still pending

- In-text citations in the canonical manuscript are not yet parsed. REG-018
  requires format-specific, authorized manuscript reconciliation.
- The protocol inventory records presence and unresolved states only. It does
  not evaluate the scientific fit, completeness or rigor of the method.
- REG-011 has no automatic semantic-entailment judgment. It records declared
  reviewer decisions without independent authentication.
- A local report is not proof of synchronized Google Drive storage.
- All automated tests use synthetic material. Passing them does not prove
  the quality of actual scientific manuscripts.

Before considering this improvement complete, conduct real authorized
researcher usability checks, confirm one-page print layout in supported
environments and document both diagnostic false positives and omissions.
Source comments and repository documents are English-first; the assistant
can communicate these findings in the researcher's language as specified
by references/language-policy.md.
