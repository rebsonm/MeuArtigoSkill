# Detailed scientific workflow

Read the section for the current stage; retain its controls when executing that stage.

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

## Optional scientific quality benchmark

For Skill-level assessment or release comparisons, follow [quality evaluation](../docs/AVALIACAO-QUALIDADE-CIENTIFICA.md). Use the frozen factual casepack in `benchmarks/public_review_reference_v1.json`; keep real Skill outputs and any independent claim assessments separate from the published reference. Report denominator and coverage per dimension. A live Crossref/OpenAlex metadata pilot alone does not measure interpretation, category construction, or general scientific validity.

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

Read `references/evidence-synthesis.md` and `references/source-verification.md`. Where scripts are available, run `scripts/verify_sources.py` and sync its report to the canonical workspace. Verify text locally and never infer claim support from the mere existence of a citation or passage.

## Explore the validated corpus without changing the methodology

Read `references/corpus-map.md` and `references/grounded-corpus.md`.

### Corpus Map

After a meaningful retained corpus exists, the Skill may build an exploratory Corpus Map.

Use only metadata actually present in the canonical project or legitimately retrieved from a scholarly metadata source. Report metadata/enrichment coverage explicitly.

The map may show, where supported:

- publications by year;
- recurrent authors;
- journals/source titles;
- source-derived keywords/concepts;
- evidence-matrix constructs;
- real citation/coauthorship/co-occurrence network structure;
- clusters and bridge records only when an actual edge model supports them.

Do not fabricate missing metadata. Do not infer citation links from semantic similarity. Do not label the study bibliometric merely because the Skill provides an exploratory map.

Use `scripts/build_corpus_map.py` in filesystem mode. Record map generation as a TRACE event and AI use when cluster interpretation is substantively AI-assisted.

### Grounded Corpus Mode

When the user asks analytical questions about the retained literature, prefer Grounded Corpus Mode when full text is available.

Ground answers only in eligible validated corpus sources. Default eligible states are FULL TEXT — CORE and FULL TEXT — SUPPORT with actual full-text access.

For material answers:

- identify supporting Record_IDs;
- use Evidence_IDs where available;
- provide locators when available;
- label literature-supported statements [L] and analytical inferences [I];
- say when the corpus does not support the answer.

Do not silently supplement a grounded answer with model memory or unrestricted web knowledge. If external literature is needed, explicitly leave Grounded Corpus Mode and tell the user that the answer is being expanded beyond the frozen corpus.

Grounded retrieval does not replace human validation before a synthesis, theoretical category, material inference, or key manuscript claim is frozen.

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

When a target journal is known, work from `JOURNAL_PROFILE.json`, the supplied/official rules and template, and the relevant recent archive.

Use the formal editorial contract during manuscript construction, not only for final formatting. This includes required section architecture, length constraints, abstract/keyword rules, anonymization, reference style, declarations, AI/data policies, and required submission files.

Use aims & scope, editorials, and relevant recent journal articles to understand the scientific conversation and contribution profile. Keep this scientific/editorial profile separate from mandatory formal rules.

Do not claim that rules are current unless the supplied or official source was actually checked. Do not use journal fit to suppress contradictory evidence or alter scientific findings.

Identify substantively relevant papers already published there.

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

## Stage 12.5 — Audit claim robustness before freezing

Read `references/evidence-synthesis.md` and `references/scientific-governance.md`.

Before GATE-0006 can be approved, audit every material claim for contestability.

For each material Claim_ID, examine:

- supporting Evidence_IDs;
- contradictory or disconfirming Evidence_IDs in the retained corpus;
- plausible alternative explanations;
- boundary conditions;
- dependence on a single source or fragile evidence chain;
- whether wording exceeds the evidentiary strength;
- [L] / [I] / [P] status;
- human validation outcome.

Use the robustness statuses:

- `NOT_AUDITED`
- `ROBUST`
- `QUALIFIED`
- `REVISE`
- `REJECT`
- `NOT_APPLICABLE`

A `QUALIFIED` claim must carry the qualification/condition into the manuscript.

When useful, perform a dependency check: if the central supporting evidence were removed, would the claim remain defensible? Treat this as an argument-dependency check, not as a universal statistical test.

Do not hide contradictory evidence merely to improve journal fit.

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
- material claims have completed robustness/contestability review;
- counter-evidence, alternative explanations, boundary conditions, and single-source dependencies were not silently ignored;
- `[I]` and `[P]` were not disguised as literature consensus;
- no citations were invented or cited from search snippets without source verification;
- limitations include real scope and access constraints;
- target-journal rules are satisfied against the current verified JOURNAL_PROFILE when a journal is defined;
- every external/shareable artifact has the correct identified/anonymized mode;
- the anonymization profile is verified or explicitly NOT_REQUIRED with rationale;
- the exact outgoing files have a PASS or PASS_WITH_HUMAN_REVIEW anonymization audit when anonymization applies;
- hidden metadata, comments/revisions, filenames, paths and visual outputs have been checked for identity leakage;
- `EXTERNAL_ANONYMIZED` files contain no nonessential descriptive/provenance metadata, including Creator/Producer/Generator/Application, generation/edit timestamps, XMP/EXIF/IPTC or tool labels such as Python/pypdf/ReportLab/Matplotlib/LibreOffice;
- continuity state is updated.

Run `scripts/validate_project.py` when using the standard workspace. When local spreadsheet generation is available, also use `scripts/build_matrix_template.py` or let `scripts/init_project.py` invoke it automatically. Use `scripts/governance_events.py`, `scripts/create_snapshot.py`, `scripts/compare_snapshots.py`, and `scripts/generate_transparency_report.py` for deterministic governance operations. Use `scripts/build_corpus_map.py` for corpus mapping when a retained corpus exists, and `scripts/release_audit.py` before a release.

## Stage 14 — Prepare submission and preserve the outcome

When the user is ready to submit:

1. verify the target journal/conference requirements from an authoritative current source;
2. complete `10_Submission_Checklist`;
3. freeze the canonical manuscript and supplementary files;
4. create separate identified and anonymized derivatives when required, sanitize the exact anonymized files with `scripts/sanitize_metadata.py`, then audit those exact files with `scripts/audit_anonymization.py`;
5. preserve the exact submitted versions;
6. record the submission date, identifier/receipt, and any next external deadline;
7. create/update the corresponding C.A.D.A. items;
8. synchronize the primary external work manager when connected;
9. preserve reviewer/editor follow-up as new C.A.D.A. work items rather than overwriting the submitted state.

Do not claim a submission occurred unless the user or an authorized tool actually completed it.

## Recovery and continuation rule

When resuming an existing project, read `CONTINUIDADE.md` first, then inspect the persistent workspace root, master matrix, protocol, and latest canonical trackers. Do not re-screen decided records or reconstruct executed search strings from memory unless an explicit audit is requested.

If records conflict, prefer the most recent explicitly marked canonical entry and preserve superseded history rather than deleting it.


