# Documentation consistency audit — 2026-10-10

**Status:** post-merge documentation corrections prepared in draft PR #25.
This is an engineering/documentation audit, **not** a third-party scientific
validation, real ChatGPT installation or authorization to publish another beta.

## Repository and source identity

- Repository: https://github.com/rebsonm/MeuArtigoSkill
- Feature integration: PR #24 merged into main on 2026-10-10.
- Source version in main: **0.9.0-beta.2**, still an **unpublished candidate**.
- Latest verified publicly tagged downloadable beta: **v0.9.0-beta.1**,
  published 2026-10-09.
- PR #22 is a separate MCP Apps/UI experiment and is not part of this audit.
- The release must never be inferred merely from a VERSION update, a successful
  CI ZIP checksum or a merge into main.

## Audit method and coverage

The baseline main tree contained **166 files**, including **84 Markdown**
documents (49 in docs/, 30 in references/, and 5 at repository root).
The documentation link checker / public document auditing jobs cover the
configured maintained-document surface. Manual source review focused on
entrypoints, installation, platform compatibility, security, scientific
claims, release history, API adapters, C.A.D.A. guides, scientific validation
limits and referenced published workflows.

Checks performed or required on the final head:
- GitHub repository/release/merge metadata, to separate the code candidate
  from the actual downloadable version.
- Current version versus README, CHANGELOG, CITATION.cff and release notes.
- Maintained platform instructions versus the **current vendor guidance**,
  including https://help.openai.com/pt-br/articles/20001066-skills-in-chatgpt,
  https://platform.claude.com/docs/pt-BR/agents-and-tools/agent-skills/overview,
  and https://support.google.com/gemini/answer/17094296?hl=en.
  This is a spot check, **not exhaustive external URL monitoring**.
- Internal Markdown relative links, public artifact privacy checks,
  English-source heuristics, software regressions, deterministic package ZIP
  and SHA-256 check using the repository CI. Passing these checks cannot
  certify semantic correctness of all third-party references.
- Scientific/editorial language: distinguish source location, source
  verification, human decisions, ChatGPT runtime capability, user research
  evaluation and actual public distribution.

## Findings and corrective actions

| ID | Impact | Finding | Correction |
| --- | --- | --- | --- |
| DOC-01 | HIGH | Main README described beta.2 as an unmerged development branch and repeated published-beta links | Distinguish merged source candidate from published beta.1; consolidate installation action |
| DOC-02 | HIGH | Beta.2 candidate release notes and stabilization checklist claimed PR #24 had not merged | Identify the completed merge while retaining all pending real-world acceptance gates |
| DOC-03 | HIGH | CFF candidate declared a publication date for a version with no public tag | Omit date-released for the unpublished source candidate; permit safe later insertion by the release synchronization utility |
| DOC-04 | HIGH | Manual release process could ship candidate notes and metadata without an explicit documentary check | Add a fail-closed manual-publication metadata preflight with deterministic negative tests |
| DOC-05 | MEDIUM | English-language migration history still called beta.8 the latest published version | Preserve as a historical migration record; identify beta.1 as the published migration and beta.2 as source-only |
| DOC-06 | MEDIUM | Installation guide asserted beta.1 predated the English-source migration it actually shipped | Correct migration chronology and distinguish source ZIP from installable release ZIP |
| DOC-07 | MEDIUM | API documentation still said it lived in an unmerged PR | Describe merged implementation, mocked vendor tests, optionality and still-missing live validation accurately |
| DOC-08 | MEDIUM | Source preflight text had malformed heading/list and confusing fallback instructions | Repair formatting and retain required WORK_FALLBACK identifier |
| DOC-09 | MEDIUM | Public validation register asserted active branch protection without verified repository settings | Replace the unverified claim with a maintainer-verification requirement |
| DOC-10 | LOW | Security coverage identified only historical 0.8 releases | Clarify coverage across historical and current experimental versions |
| DOC-11 | LOW | Proof-of-events and C.A.D.A. docs contained malformed Markdown list headings | Repair without modifying their methodological contracts |
| DOC-12 | MEDIUM | Changelog could duplicate a candidate's version heading if publishing on a later date | Reconcile an existing candidate heading to the actual authorized publication date; regression tests added |

Only the release metadata synchronization and manual-publication preflight
code are altered beyond Markdown/YAML metadata. **No scientific research
methods, evidence validation thresholds, project register schemas,
bibliographic adapters or user-facing workflows are changed by this PR.**

## Explicit remaining limitations

1. **Real ChatGPT behavior untested:** installation, resume after a new chat,
   manual import, current UI capabilities and verified Drive write/readback
   require an authorized observed run on the exact intended ZIP.
2. **Academic validity untested:** no fresh end-to-end article on this version
   with a researcher-confirmed corpus, full-text locators and human gate
   decisions; software CI is not a substitute.
3. **Academic API integrations not certified live:** offline mocks do not
   establish Scopus/WoS entitlement, current provider quotas, private Zotero
   permissions or secure multi-user MCP operations.
4. **External URLs not checked exhaustively:** official vendor references
   were spot checked; product menus and plan eligibility may change.
5. **Branch protection not independently verified:** review GitHub
   repository settings/ruleset enforcement before promising compliance.
6. **Published v0.9.0-beta.1 is immutable:** corrections in this PR and beta.2
   source must not be attributed to that released artifact.
7. **Publication intentionally blocked:** do not run the manual publication
   workflow until the real release date, actual release notes and README link
   are finalized and the researcher approves it.

## Completion criteria for this documentation PR

- Pass regression tests and the regular release audit on the final PR head.
- Report truthful latest GitHub release and version in main.
- No stale unmerged PR #24 statements in maintained guidance.
- No speculative data, empirical validation or platform claims.
- Clear distinction between external vendor capabilities and this Skill's
  **observed** behavior.
- Do not merge or tag as a side effect of conducting the audit.

This register records the scope of a **documentation consistency review**.
No third-party scientific review, usability study, participant feedback,
security penetration test, official journal approval, live API search or
deployment was performed as part of this documentation task.
