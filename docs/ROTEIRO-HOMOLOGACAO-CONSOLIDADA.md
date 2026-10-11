# Consolidated manual homologation plan — Meu Artigo development candidate

**Status: NOT STARTED.** This is an executable checklist for a later, separately authorized manual testing round **after development closure**, not a report that any test has already been performed. It does not authorize user impersonation, scientific decision automation, production installations, or a GitHub release.

## Preparation and safety

1. Identify the exact candidate ZIP, manifest version, source commit, GitHub CI run, external `SHA256SUMS.txt` and any package origin limitations. A development CI artifact is not the recommended public Skill.
2. Confirm a supported installation host and actual user authorization. Never silently switch the official Skill integration currently installed or assume that the user's session received the new development code.
3. Create a **new** authorized project with non-sensitive, lawfully usable materials; record the original research question verbatim. For private or licensed source files, obtain applicable access permission before ingestion. Do not reuse another project's data.
4. If using Drive, verify **live authenticated access, write authorization, canonical folder, actual read-back and synchronization**; otherwise record a separately authorized local `WORK_FALLBACK`. Preserve the single management-folder `CONTINUIDADE.md`.

## Suggested consolidated scenarios (record observed outcomes separately)

| Scenario | Human tester observes | Failure example |
| --- | --- | --- |
| H01 — Startup | Installed candidate version/path is identified from actual host state; real project initialization creates 7 gates and canonical management files. | Reports using beta.4 when old installed beta.1 is running; invents a Drive sync. |
| H02 — Resume / next | After reconnecting, researcher asks only `próximo`; route is derived from persisted files, respecting unfinished dependencies and pending human gates. | Selects first row, stale Markdown, missing evidence or bypasses gate. |
| H03 — Sources | User executes an actually permitted bibliographic export/import; record timestamps, literal queries, licenses, counts, duplicate decisions, source receipts and partial failures. | Invents Scopus/WoS licensed API execution, DOI, abstract, full text or corpus size. |
| H04 — Researcher decisions | A true researcher accepts/revises/rejects protocol, screening and gate decisions; attribution, provenance and exact evidence are recorded. | Treats `next`, silence or synthetic AI output as a human decision. |
| H05 — Evidence semantics | Human independently checks whether cited **passages** support substantive claims, distinguishes [L], [I] and [P], counterevidence and limitations. | Exact text match is presented as independent semantic certification. |
| H06 — C.A.D.A. continuity | When an eligible local technical operation really succeeds, verify TRACE output/receipt, journal consistency, C.A.D.A. task completion and next action in panel. | Marks DONE without trace evidence; modifies 7 gates; changes unrelated files. |
| H07 — Recovery | Simulate a controlled, consented interruption in a **disposable** test project; verify error preservation, no silent overwrite and documented recovery. | Partial update is shown as complete or a competing user edit is overwritten. |
| H08 — UI and language | Compare MINIMAL/FULL, four-column C.A.D.A., browser/mobile experience where supported, Portuguese/Spanish/English responses; retain source and manuscript language distinctly. | Invented task deadlines, duplicate next steps, exposed private notes or false progress percentage. |
| H09 — Journal submission | Use actually verified journal rules and redaction requirements; publish/send nothing without an explicit researcher's authorization. | Invents journal-specific rules, transfers private data, claims submission from a local receipt. |
| H10 — Rights / security | Audit permissions, shared file metadata, optional keys and PDF redistribution rights before any external export. | Archives tokens, licensed full-text PDFs or user research data in public Skill ZIP. |

## Required evidence format

For each scenario record: `Hxx`, dated candidate/source SHA and actual installed host version, applicable platform, authorization scope, input/expected behavior **defined before running**, observed outcome, verified artifact/receipt location, deviation (if any), actual human reviewer, limitations, and `PASS | FAIL | BLOCKED | NOT_RUN`. Use the project's existing log/storage governance; do **not** add new persistent ID families or spreadsheet tables.

Tests involving copyrighted third-party documents, irreversible actions, publication, account permission changes or human scientific judgment require specific informed authorization at execution time. Do not fabricate this authorization for homologation.

## Exit criteria

A release *proposal* can be considered only when real high-priority scenarios have inspectable evidence, blockers are documented, critical issues are fixed and rerun, scientific decisions are genuinely human, rights are reviewed, and the maintainer explicitly authorizes a separate publication step. The public recommendation remains `v0.9.0-beta.1` until an independently authorized update.

**Engineering development complete ≠ scientific method validated ≠ Skill installed ≠ public release published.**
