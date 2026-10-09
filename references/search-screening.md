# Search, deduplication, screening, and full text

## Contents
- Build search families
- Freeze literal strings
- Validate exports
- Cross-database consolidation
- Deduplication hierarchy
- Two-pass screening
- Full-text retrieval
- Snowballing
- Stopping rules

## Build search families

Decompose the research question into conceptual blocks. Typical block roles include:

- phenomenon/technology/intervention;
- theoretical construct;
- outcome/problem/mechanism;
- context/population/domain.

Do not mechanically require every block in every query. Create complementary search families that trade sensitivity and specificity.

Example abstract form:

```text
S1 = A AND B AND C
S2 = A AND C AND D
S3 = B AND A
S4 = specialized mechanism terms AND A
S5 = A AND specific application context AND governance/outcome terms
```

The blocks and family count are project-specific. Never reuse another project's literal vocabulary by default.

## Freeze literal strings

Maintain both:

1. conceptual family description; and
2. database-specific literal executable string.

For every executed version, record:

- quotation marks;
- wildcards/truncation;
- Boolean operators;
- field tags;
- parentheses;
- date restrictions;
- document filters;
- languages;
- database/platform;
- execution date.

A change to any of these creates a new version. A re-run is a reproduction only when the relevant literal query and filters are the same.

## Validate exports

Before screening, verify:

- number of exported records equals intended coverage or is explicitly partial;
- year filters are correct;
- document types are present/correct;
- title exists;
- abstract exists when title/abstract screening is planned;
- DOI or database ID is retained where available;
- keyword fields are present if required;
- encoding/import has not collapsed columns.

Never use a malformed or partial export as the official result without labeling it.

## Cross-database consolidation

For a complementary database:

1. execute equivalent conceptual families using native syntax;
2. validate export;
3. deduplicate against all earlier canonical records;
4. calculate overlap/new records;
5. screen only the new records;
6. preserve overlap counts for the audit trail.

Call this cross-database deduplication/consolidation and incremental screening.

## Deduplication hierarchy

Use the following evidence hierarchy:

1. valid normalized DOI exact match;
2. exact normalized title;
3. trusted database identifier mapping;
4. high title similarity + author overlap + compatible year;
5. abstract/content comparison for suspicious pairs.

Normalize DOI by lowercasing, stripping URL/prefix wrappers and whitespace, and validating a plausible DOI pattern before using it as a key.

Normalize titles by lowercasing, Unicode normalization, whitespace collapsing, and punctuation handling. Preserve the original title separately.

Do not auto-delete fuzzy matches. Send them to a duplicate-audit table with the reason and evidence used.

## Two-pass screening

### Pass 1: title and abstract

Default decisions:

- INCLUDE — clearly contributes evidence relevant to the question;
- BORDERLINE — plausible relevance but ambiguous from metadata;
- EXCLUDE — fails criteria or lacks relevant contribution.

Store a concise reason code plus optional note.

### Pass 2: retained records

For integrative/conceptual work:

- FULL TEXT — CORE — likely central to the synthesis or contribution;
- FULL TEXT — SUPPORT — relevant but secondary/contextual/transferable;
- EXCLUDE — insufficient after closer abstract/metadata review.

CORE/SUPPORT are prioritization labels, not evidence-quality ratings.

For a systematic review, do not use priority labels to bypass full eligibility assessment.

## Deterministic separation of AI proposals and scientific decisions

Read [screening audit](../docs/SCREENING-AUDITAVEL.md). New projects set `screening_human_decisions_required=true`. AI recommendations are saved in `Pass1_AI_proposal`/`Pass2_AI_proposal` with source and rationale; they can never silently become final decisions. `scripts/screening_review.py` records the researcher's actual Pass1/Pass2 decision, reason, reviewer and source of their response. Disagreement requires documented resolution, not replacement of the original AI proposal. If review is pending, the record remains pending and GATE-0004 cannot approve incomplete screening.

The code verifies evidence-reference fields, not real authorship; keep a verifiable link to the researcher's response. A model's suggestion is not an independent second human reviewer.

## Single-reviewer integrity

If one researcher is screening:

- never claim independent double screening;
- revisit all BORDERLINE records;
- recheck a documented sample of INCLUDE and EXCLUDE decisions;
- preserve reasons;
- optionally use an AI as a consistency checker, not as a fictional second human reviewer.

If multiple real reviewers participate, document their actual independent/joint procedures and agreement handling.

## Rights to read versus rights to redistribute

A legitimate institutional, personal, publisher or repository PDF may be retained for authorized academic reading without being exportable as a public copy. For each local full text use the existing 04_FullText_Tracker.csv rights fields. A DOI, paywall status or generic license description is not evidence that the **specific article** may be redistributed. See [full-text rights](../docs/DIREITOS-FULLTEXT-E-PDFS.md). If access is unavailable, record uncertainty and pursue authorized routes; that alone is not a scientific exclusion reason.


## Full-text retrieval

For each full-text candidate, track:

- access status;
- version;
- source;
- date;
- decision;
- exclusion reason;
- evidence-extraction status.

Do not exclude because a paywall exists. Mark `PENDING ACCESS`, pursue lawful institutional/repository routes, and distinguish unavailable evidence from irrelevant evidence.

Do not equate:

- search snippet with abstract;
- abstract with full text;
- accepted manuscript with final version without noting version;
- conference proceeding with later journal article without comparison.

## Snowballing

Use backward and forward snowballing when:

- the core literature is sufficiently stable;
- seminal foundations are missing;
- a construct emerges that structured strings did not cover;
- a citation network reveals a near-neighbor cluster.

Log snowball sources and reasons. Do not let snowballing silently become an unbounded second search strategy.

## Stopping rules

Match the stopping rule to the review design.

For integrative/conceptual synthesis, a defensible stop may combine:

- declining contribution of new databases/search families;
- high overlap among complementary searches;
- repeated reinforcement of existing categories;
- no materially new construct/mechanism in recent high-relevance full texts;
- adequate representation of conflicting and boundary-condition evidence.

Call this **provisional conceptual saturation** unless the rule was explicitly operationalized and documented.

For systematic reviews, stopping is not theoretical saturation; it follows the completion of the planned comprehensive search and eligibility process.
