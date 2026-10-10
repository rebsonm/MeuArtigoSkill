# Meu Artigo — 0.9.0-beta.2

**RELEASE CANDIDATE ONLY — NOT PUBLISHED.** Version frozen in the PR #24
development branch for engineering and researcher-evaluation preparation.
The latest tagged public release remains v0.9.0-beta.1 until a maintainer
explicitly authorizes a new signed-off release. Do not represent the CI
artifact as an independently validated, published, or tested-on-ChatGPT Skill.

## Change summary

- Protect every bibliographic deduplication CSV output from formula injection
  caused by third-party spreadsheet metadata.
- Add consistent three-register bibliographic imports with a recoverable local
  write-ahead journal. Failed or interrupted imports require documented rollback
  before a project can be validated or another import can proceed.
- Restore compatibility with the canonical traceability validator by treating
  locally recorded bibliographic retrieval as UNVERIFIED until independently
  attested by permitted execution receipts.
- Treat a genuinely successful provider query returning zero records as zero
  matches, **not** a failed network request.
- Include optional, explicit network metadata adapters for OpenAlex,
  Crossref and Semantic Scholar; DOI lookups from Unpaywall/OpenCitations
  and a user-scoped Zotero metadata export, with protected external secrets.
- Keep manually imported CSV/RIS/BibTeX research workflows as the default;
  optional API connections are NEVER onboarding prerequisites or research
  quality certification. Licensed Scopus/WoS APIs are not connected here.

## Boundaries

- Provider adapters have offline mocked software tests. A real vendor search,
  the effective provider licence, private Zotero authentication, and a live
  ChatGPT plugin were not verified in this release-candidate work.
- Single-project offline journal protects against interrupted local multi-file
  writes but is not a remotely shared database or transactional Google Drive
  implementation. Only explicitly authorized WORK_FALLBACK files can be modified.
- The manual research method, scientific gates, [L]/[I]/[P], claims ledger,
  evidence checks, and native four-column C.A.D.A. view remain unchanged.
- A successful CI run establishes software-test success only. Independent
  research-method evaluation and human article review are still pending.
- Existing read-only source checks and copyright/fulltext rights rules remain.

## Release conditions

1. Pass release-audit CI, package manifest/hash and all regression tests.
2. Read the actual release-candidate evaluation report and complete the human
   acceptance criteria; do not infer these from an automated passing badge.
3. Execute a researcher-authorized real academic end-to-end article in the
   installed Skill, recording actual scientific decisions and licensed sources.
4. Test install/resume and Google Drive writes with a real authorized ChatGPT
   account. Report platform limitations and pending items.
5. Explicit maintainer decision, then one-time manual GitHub release after
   moving approved changes onto main. The PR itself never publishes a release.

No release, merge, journal submission, real participant feedback, or journal
acceptance is implied by preparing this candidate.