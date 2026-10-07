---
name: meu-artigo
description: Build and manage a rigorous, traceable scientific article workflow from a user-supplied research problem or question. Use for novelty audits, bibliographic search, integrative/conceptual/systematic-review support, screening, full text, evidence matrices, synthesis, evidence-grounded drafting, final audit, and submission readiness. Govern the step-by-step work with C.A.D.A. (capture, assign, define timing, follow up), optionally mirroring tasks to ClickUp, Jira/Atlassian, Trello, or equivalent. For empirical articles, support literature and provenance but never invent empirical design, data, analysis, or findings.
---

# Meu Artigo

## Core principle

Start from the user's own research problem, question, phenomenon, theory gap, empirical puzzle, or article idea. Never import the topic, constructs, search strings, inclusion criteria, sources, categories, findings, journal, or conclusions of a previous project into a new one.

Treat any prior project only as evidence about **how to work**: stage ordering, audit controls, state persistence, tool orchestration, screening discipline, evidence extraction, synthesis, and writing provenance.

The goal is not to generate a plausible manuscript quickly. The goal is to create a manuscript whose important claims can be traced back through a persistent evidence trail.

## First-run preflight

Before substantive searching, inspect the capabilities available on the current AI platform. Read `references/plugin-onboarding.md`.

Resolve capabilities by **role**, not by product name:

- persistent project storage;
- peer-reviewed literature discovery;
- citation-context / citation-graph verification when available;
- academic web, publisher, repository, and official-source retrieval;
- ingestion of structured bibliographic exports;
- code/script execution when the platform supports it;
- optional work-management integration for step-by-step execution and follow-up.

If a useful integration is missing and the platform exposes an install/connect flow, surface it to the user. Installation, OAuth, account linking, or other third-party authorization always requires the user's explicit platform action; never claim a silent install.

Named services such as Google Drive, Consensus, Scite, Firecrawl, Scopus, or Web of Science are preferred implementations when available, not hard requirements of the methodology. Equivalent tools may fulfill the same role.

For operational project management, ClickUp, Jira/Atlassian, Trello, or an equivalent task manager may be used. Use only one primary work-management provider per article unless the user explicitly requests multiple.

Do not stop at setup. Once the user's problem is sufficiently specific, create/resume the workspace and immediately begin a small novelty/terminology scan with the academic tools actually available on that platform.

## Default operating mode

Operate autonomously with available tools. Ask the user only for information that cannot safely be inferred and is essential to scientific validity. Do not request repeated confirmations for routine steps.

At minimum, require a user-supplied research problem, research question, phenomenon, or sufficiently specific topic. If the user gives only a broad topic, refine it into candidate questions and clearly mark them as proposals rather than user decisions.

Explain technical steps in plain language when the user appears unfamiliar with bibliographic databases or AI-assisted research.

Never fabricate database access, search counts, retrieved papers, full-text reading, screening decisions, inter-rater reliability, saturation, replication, or validation.

## Govern the workflow with C.A.D.A.

Use C.A.D.A. as the operational governance layer across the scientific workflow. Read `references/cada-governance.md`.

C.A.D.A. means:

- **Capturar** — register meaningful work items, decisions, dependencies, deadlines, or blockers;
- **Atribuir** — assign owner, scientific stage, related artifact/ID, priority, and execution mode;
- **Definir prazo** — record a hard deadline, user-set deadline, internal target, dependency-based due point, or explicit TO_DEFINE state;
- **Acompanhar** — maintain status and evidence of progress/completion until the item is resolved.

C.A.D.A. never replaces the scientific method. It manages the work required to execute that method.

Every meaningful operational unit receives a stable `CADA_ID`. Maintain `11_CADA_Control` and the concise C.A.D.A. dashboard inside `CONTINUIDADE.md`.

The **spreadsheet/matrix is the universal default management mode**. Read `references/cada-matrix.md`. A user never needs ClickUp, Jira, Trello, or project-management expertise to use C.A.D.A.

Use one of two modes:

- `MATRIX_ONLY` — canonical spreadsheet/matrix only;
- `MATRIX_PLUS_EXTERNAL` — the same canonical matrix plus one external manager mirror.

If ClickUp, Jira/Atlassian, Trello, or an equivalent task manager is available, it may mirror C.A.D.A. items according to `references/work-management.md`. The persistent scientific workspace remains the source of truth.

## Choose the methodological track

Classify the intended article before building the protocol:

1. **Integrative / conceptual / theoretical synthesis** — use this skill end-to-end. The default review label is "integrative literature review" when the purpose is to combine heterogeneous conceptual and/or empirical literature to construct or refine concepts, mechanisms, propositions, models, typologies, or frameworks.
2. **Systematic review** — use a stricter exhaustive eligibility and full-text pathway. Do not call a project systematic merely because searches are structured or reproducible. Read `references/review-design.md` before using this label.
3. **Empirical article** — use this skill for novelty audit, theory/literature grounding, search logging, evidence matrix, journal dialogue, and manuscript provenance. Require a domain-appropriate empirical design for sampling, measurement, data collection, ethics, analysis, and results; never invent these components.
4. **Other review family** — if scoping, meta-analysis, bibliometric, realist, umbrella, or another design is requested, identify the correct methodological requirements before proceeding. Do not force the integrative workflow onto an incompatible design.

## Build a persistent research workspace

Create or reuse a project workspace before large searches. Prefer a connected persistent storage system when available. Google Drive is the canonical reference implementation, but an equivalent cloud/file workspace is acceptable if it can preserve folders, structured tables, documents, raw exports, and stable links. Otherwise create local files that can later be synchronized.

Maintain these canonical artifacts:

- `CONTINUIDADE.md` as the canonical resumable state;
- protocol;
- search log;
- screening table;
- evidence matrix;
- journal dialogue table when a target outlet is known;
- optional institutional/normative corpus when the topic requires it;
- full-text tracker;
- synthesis notes;
- manuscript;
- submission checklist;
- C.A.D.A. control table;
- optional project-manager synchronization table;
- scientific-process traceability log;
- AI-use transparency log;
- C.A.D.A. spreadsheet dashboard;
- human-readable `RASTREABILIDADE.md` provenance summary.

Read `references/drive-workspace.md` and `references/project-state.md` for the canonical workspace tree, master tracking matrix, tab schemas, versioning rules, and recovery flow. Treat the Drive layout as the reference schema even when another storage system is used. Run `scripts/init_project.py` when a filesystem workspace is available or persistent cloud storage is temporarily unavailable.

Before ending any material stage, update `CONTINUIDADE.md` with what is frozen, what changed, tool/plugin status, exact counts, unresolved issues, canonical links, the C.A.D.A. dashboard, and the next valid action. Update the master matrix, traceability artifacts, AI-use log when applicable, and any connected work-management mirror in the same stage. Another agent should be able to continue without reading the original chat.

## Preserve scientific-process traceability

Treat traceability as a first-class output of the project. Read `references/traceability.md`.

Maintain:

- `RASTREABILIDADE.md` — human-readable provenance summary;
- `13_Traceability_Log` — structured record of material scientific-process events;
- `14_AI_Use_Log` — AI-specific use, purpose, materiality, human validation, and disclosure readiness;
- links between CADA_ID, Trace_ID, Search_ID, Record_ID, Evidence_ID, Claim_ID, and canonical artifacts.

Do not attempt to archive every conversational token. Log material actions that affect method, corpus, evidence, synthesis, claims, manuscript state, or disclosure.

For substantive AI-assisted work, record tool/platform, model/version when known, purpose, input/output category, human review method, final human decision, and related artifacts. Never claim human validation without an actual verification action.

The final goal is that a researcher, coauthor, reviewer, editor, or future agent can reconstruct how important parts of the article were built.

## Stage 1 — Audit the idea before exhaustive searching

Convert the user input into a provisional research object:

- problem or puzzle;
- provisional question;
- intended contribution;
- unit of analysis or phenomenon;
- boundaries and explicit exclusions;
- article type;
- target journal or field if known.

Then run a **novelty audit**, not yet an exhaustive review. Use seed sources from the user's files/persistent workspace, available peer-reviewed discovery tools, citation-context tools, academic web search, publisher pages, and relevant journal archives.

For the closest neighboring papers, record:

- what they already do;
- where they overlap with the new idea;
- what they do not do;
- whether the proposed novelty survives;
- how the research question or contribution should be narrowed.

Revise the contribution before scaling the search. Prefer a narrower defensible contribution over a broad unsupported novelty claim.

Use epistemic labels internally:

- `[L]` = directly supported by literature, data, or an authoritative source;
- `[I]` = analytical inference from comparison/synthesis;
- `[P]` = original proposition, model element, hypothesis, or author contribution.

Do not present `[I]` or `[P]` as established literature findings.

## Stage 2 — Freeze a review/search protocol

Translate the question into conceptual blocks and search families. Separate:

- conceptual query logic;
- literal executable string for each database;
- filters;
- date executed;
- database/platform;
- export file;
- records found/exported;
- status and notes.

Never overwrite a previously executed search string. If syntax, synonyms, wildcards, field tags, filters, or date ranges change, create a new version identifier and explain why.

Define before large-scale screening:

- databases and their roles;
- years;
- languages;
- document types;
- inclusion criteria;
- exclusion criteria;
- treatment of seminal older sources;
- treatment of preprints and conference/article pairs;
- screening rules;
- full-text retrieval rules;
- snowballing rule;
- stopping/saturation rule appropriate to the review design.

Read `references/review-design.md` and `references/search-screening.md`.

## Stage 3 — Orchestrate sources by role

Use capabilities for distinct purposes rather than treating all search systems as interchangeable.

- **Persistent storage / user files**: recover prior reading, project artifacts, PDFs, notes, exports, templates, and continuity state.
- **Peer-reviewed discovery tool**: rapid literature discovery, terminology calibration, nearby-paper discovery, and cross-checking. Do not treat a discovery tool as an exhaustive bibliographic database.
- **Citation-context / citation-graph tool**: targeted literature verification, citation traversal, citation intent/context, and full-text support where legitimately available.
- **Indexed bibliographic databases**: primary structured searches when the protocol calls for them. Scopus and Web of Science are common implementations. If direct connectors are unavailable, use exports or authorized browser workflows and validate the files before screening.
- **Academic/public web, publishers, repositories, and official sites**: locate official metadata, lawful full text, current institutional documents, journal archives, and authoritative source pages.
- **Sensitivity/snowball search tools**: identify additional candidates and citation chains; do not treat them as automatically exhaustive or reproducible.

Read `references/tool-orchestration.md` before multi-source searching. Map available platform tools to these roles; do not invent missing capabilities.

## Stage 4 — Execute and audit bibliographic searches

For every search family:

1. execute the literal version appropriate to the database;
2. log date, filters, counts, and exact string;
3. export enough metadata for screening and deduplication;
4. verify the actual exported row count;
5. verify required fields such as title, abstract, DOI/identifier, year, document type, authors, and keywords when available;
6. mark partial, malformed, wrongly filtered, or field-deficient exports as invalid and re-export instead of silently using them;
7. preserve raw exports unchanged.

When reproducing a strategy in a second database, call it a **replication in a complementary bibliographic database**, followed by cross-database deduplication and incremental screening. Do not call Scopus × WoS a meta-analysis or data triangulation.

## Stage 5 — Deduplicate conservatively

Use multiple keys:

- normalized DOI when bibliographically valid;
- normalized title;
- database identifiers;
- author overlap;
- year proximity;
- abstract comparison for suspicious pairs.

Then check near-duplicates, preprint versus final publication, translated/bilingual titles, and conference paper versus expanded article.

Never remove a record solely because an automatic similarity score is high. Flag candidate pairs and confirm before exclusion.

Use `scripts/dedupe_records.py` when compatible exports are available. Preserve original records and log which occurrence was retained.

## Stage 6 — Screen in explicit passes

For integrative/conceptual synthesis, use two passes by default:

**Pass 1 — title + abstract**
- INCLUDE
- BORDERLINE
- EXCLUDE

**Pass 2 — retained records**
- FULL TEXT — CORE
- FULL TEXT — SUPPORT
- EXCLUDE

Record a short reason for exclusions. Screen only records that are new after deduplication when a complementary database is added.

For single-author work, do not simulate independent double screening. Instead use a second pass for borderline cases plus a documented sample recheck of included/excluded records. If genuine multiple reviewers exist, record their real procedure.

For systematic reviews, follow the stricter design described in `references/review-design.md` rather than substituting priority sampling for full eligibility assessment.

## Stage 7 — Retrieve full text without access bias

Track for each candidate:

- full text found: yes/no;
- version: final, accepted manuscript, preprint, other;
- acquisition source;
- access date;
- full-text decision;
- exclusion reason if excluded;
- notes relevant to synthesis.

Lack of access is not a scientific exclusion criterion. Keep the item pending and try legitimate alternatives such as institutional access, open repositories, accepted manuscripts, author pages, or author contact.

Do not claim to have read full text when only an abstract or snippets were available.

## Stage 8 — Extract evidence, not summaries alone

For each included source, populate a structured evidence matrix. Adapt fields to the field and article, but preserve the logic:

- citation / persistent identifier;
- construct or concept;
- definition or central claim;
- problem, tension, mechanism, relationship, or finding;
- study design / evidence type;
- context and sample/data if empirical;
- relevant process or stage;
- actors/roles when applicable;
- observable evidence or artifact;
- boundary conditions / limitations;
- transferability to the user's question;
- evidence strength/role;
- exact locator or supporting passage when useful;
- `[L]`, `[I]`, `[P]` status for downstream synthesis.

Write from this matrix later. Do not write the literature argument from model memory.

Read `references/evidence-synthesis.md`.

## Stage 9 — Synthesize across sources

Move from paper-by-paper summaries to cross-source comparison. Look for:

- recurring constructs;
- mechanisms or relationships;
- contradictions;
- boundary conditions;
- missing links;
- distinct explanatory roles;
- methodological disagreements;
- contexts where transfer is weak or strong.

Create higher-order categories only when supported by more than one independent source stream or when the methodological design supplies another explicit justification. Keep provisional categories marked as inference until sufficiently grounded.

For integrative/conceptual work, theoretical or purposive full-text sampling may be used when explicitly justified by the research purpose. Never represent a prioritized subset as if every pre-full-text candidate had been fully assessed.

Treat saturation cautiously. Record it as provisional unless there is an operational stopping rule and recent additions demonstrably cease to create new categories or materially alter the synthesis.

## Stage 10 — Add institutional or normative evidence only when relevant

If the question concerns regulation, governance, standards, policy, professional practice, public administration, compliance, or another institutionally governed domain, build a separate institutional/normative corpus.

Keep scientific literature and institutional authority analytically distinct. Record jurisdiction, binding status, version/date, scope, mechanisms, and relevance. Do not treat regulations or standards as empirical research articles.

If the topic does not need this corpus, omit it.

## Stage 11 — Enter the target journal's conversation

When a target journal is known, inspect its instructions and relevant recent archive. Identify substantively relevant papers already published there.

For each useful journal anchor, record:

- what the journal paper already established;
- where the new article agrees, extends, narrows, contradicts, or relocates the discussion;
- why citing it is substantively justified.

Avoid citation gaming. Do not add journal citations solely to appear tailored.

## Stage 12 — Draft from evidence and provenance

Draft only after the question, contribution, protocol, and evidence structure are stable enough.

For each substantive paragraph, be able to identify whether it is:

- literature-supported;
- an analytical integration;
- an original proposition;
- an empirical result supplied by the user's actual data/analysis.

Keep claims no stronger than the evidence. Do not call a conceptual framework "validated" without empirical validation. Do not claim causal necessity from conceptual synthesis alone.

Use the Search Log and state file to write the methods section. Reconcile every count before publication.

## Stage 13 — Run the final audit

Before declaring the manuscript ready, verify:

- review type is labeled correctly;
- research question and contribution still match the evidence;
- all reported search strings correspond to actual executed versions;
- counts reconcile from raw search through deduplication and screening;
- invalid/partial exports are excluded from official counts;
- duplicates were handled transparently;
- full-text claims match actual access level;
- important claims trace to evidence entries;
- `[I]` and `[P]` were not disguised as literature consensus;
- no citations were invented or cited from search snippets without source verification;
- limitations include real scope and access constraints;
- target-journal rules are satisfied;
- continuity state is updated.

Run `scripts/validate_project.py` when using the standard workspace.

## Stage 14 — Prepare submission and preserve the outcome

When the user is ready to submit:

1. verify the target journal/conference requirements from an authoritative current source;
2. complete `10_Submission_Checklist`;
3. freeze the canonical manuscript and supplementary files;
4. preserve the exact submitted versions;
5. record the submission date, identifier/receipt, and any next external deadline;
6. create/update the corresponding C.A.D.A. items;
7. synchronize the primary external work manager when connected;
8. preserve reviewer/editor follow-up as new C.A.D.A. work items rather than overwriting the submitted state.

Do not claim a submission occurred unless the user or an authorized tool actually completed it.

## Recovery and continuation rule

When resuming an existing project, read `CONTINUIDADE.md` first, then inspect the persistent workspace root, master matrix, protocol, and latest canonical trackers. Do not re-screen decided records or reconstruct executed search strings from memory unless an explicit audit is requested.

If records conflict, prefer the most recent explicitly marked canonical entry and preserve superseded history rather than deleting it.

## Required references

Read only what the current task needs:

- `references/review-design.md` — choose and correctly label the review/article design.
- `references/drive-workspace.md` — canonical persistent-workspace schema, with Google Drive as the reference implementation, plus master matrix tabs, MD continuity file, naming and snapshots.
- `references/project-state.md` — persistence, versioning, and recovery rules.
- `references/plugin-onboarding.md` — platform-neutral integration preflight, capability mapping, connection flow, minimum research stack, and Scopus/WoS handoff.
- `references/tool-orchestration.md` — source roles and automation/fallback behavior.
- `references/search-screening.md` — strings, exports, deduplication, screening, full text.
- `references/evidence-synthesis.md` — evidence matrix, cross-source synthesis, L/I/P discipline.
- `references/beginner-mode.md` — user-facing flow for researchers with little AI/tooling experience.
- `references/cada-governance.md` — C.A.D.A. governance, stage roadmap, work-item schema, deadlines, statuses, and completion evidence.
- `references/work-management.md` — optional ClickUp/Jira/Trello synchronization and source-of-truth rules.
- `references/cada-matrix.md` — spreadsheet-first C.A.D.A. management mode and dashboard.
- `references/traceability.md` — research-process provenance, Trace IDs, AI-use logging, and final transparency audit.
