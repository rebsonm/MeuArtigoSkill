# Public Markdown English: editorial correction and limits

## Current status — 22 November 2026

The public methodology library contains 649 catalogued records: **475
bibliographic prospecting cards** and **174 original editorial methodology
cards**. In this two-round correction, **582 previously machine-translated
Markdown cards** have been rewritten as conservative English editorial aids:

| Area | Cards corrected | Result |
| --- | ---: | --- |
| Bibliographic source cards | 472 | English bibliography and method-specific research questions |
| Methodological editorial cards | 110 | 24 pre-existing substantive English cards restored; 68 rewritten cards refined with topic-specific guidance; 18 retain conservative general guidance |
| **Total** | **582** | No prior machine-translation draft is treated as a certified translation |

All updated card contents have their SHA-256 values reconciled with the
corresponding catalogue and the shared 649-record operational-validation
ledger. The old machine-translation status no longer applies to those 582
cards. This correction does not change any scientific gate, source reading
status, bibliographic identity, copyright permission, or published PDF.

## Nature and limitations of the work

The corrected cards are **new English editorial guidance grounded in publicly
catalogued metadata**. They are **not literal or certified translations**
of the older Portuguese notes, and they do not claim that the underlying
publications were read or independently scientifically reviewed. The original
Portuguese editorial records remain accessible through immutable Git links
from the rewritten cards; the 24 pre-existing English substantive cards
were restored where appropriate.

The seven scientific gates remain pending. No third-party publication has
been redistributed, and no new version of the installed Skill or release has
been created as part of this language correction.

Original published titles, author names, DOIs, stable identifiers, archival
evidence and immutable historical receipts are retained in their original
forms. In particular, historical methodology-intake records are **not
silently overwritten or retrospectively translated**. The Marzi (2025)
card remains bound to its prior review/correction record and requires an
independent check before any content-changing translation.

## Validation and remaining language scope

For a repository-wide language inventory run:

    python scripts/audit_all_markdown_language.py
    python scripts/audit_all_markdown_language.py --strict

The first command records candidate untranslated material; the second fails
on unresolved indicators. This heuristic does **not** certify semantic
equivalence. Archival Markdown documents and bibliographic titles may still
contain Portuguese, so do **not** claim the entire Git repository is
English-only merely because the 582 corrections have been published.

Recheck the precise changes and CI in the public PR associated with this
correction. Preceding snapshots remain available in Git history and the
source-of-truth links in individual cards.

The regression suite now checks all 582 corrected-card digests, English
editorial prose, source-attribution boundaries and the exact 649-entry ledger.
The checks do not amount to independent scholarly or translation certification.
