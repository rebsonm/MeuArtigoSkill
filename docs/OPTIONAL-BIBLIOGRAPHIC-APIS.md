# Optional bibliographic API integrations — software pilot and continuation plan

Date: 2026-10-10. This document records actual engineering status, not
scientific empirical validation or live user entitlement to any provider.

## Non-negotiable product decision

**No bibliographic API is required to use Meu Artigo.** Existing manual
searching, manual CSV/RIS/BibTeX imports, the Drive-first storage policy,
methods, AI provenance, human scientific gates, original research question
and C.A.D.A. four-column native view remain as before.

The Skill may **once, briefly and non-blockingly** suggest optional account
connection during the literature-search stage. Users may ignore, decline,
disconnect or mix manual records with licensed and openly accessed sources.
Connection credentials belong to secure, authorized execution infrastructure,
not to the conversation or scientific project files.

## Software implemented and documented in PR #24 (merged into main)

M0 — DEFAULT OFF: A missing connectors configuration yields disabled. No
existing initializer, routes or research gates were modified. Regression tests
use synthetic temporary workspaces and assert there is no HTTP call by default.

M1 — GUIDANCE: User-language guidance exists and explains optionality,
individual access, privacy, vendor links and how to stay in manual mode.
Automatic one-time per-project suggestion is documented as a Skill interaction
contract, not implemented as a stateful UI application. A built-in per-project
"already offered" durable switch is NOT verified yet.

M2 — OPEN PROVIDERS: OpenAlex / Crossref metadata-only adaptors support bounded
queries and pagination with sanitised failure codes. The opt-in CLI can attempt
real HTTP if run in a network-enabled authorized environment. This chat
environment could not reach GitHub via container network; no live provider
search or coverage claims are made. Tests use deterministic mock transport.
API-key scope, plans and usage are determined by vendors, not the Skill.

M3 — HYBRID: The CLI uses the EXISTING conservative dedupe_records.py on
multiple manual and API exports. Exact DOI duplicates are audited, conflicting
DOIs preserved and near matches flagged. All dedupe CSV outputs neutralize
spreadsheet formula cells while preserving original input files for audit.
Real retrieval may stage CSV + SHA256 receipts. Canonical local registry append
is permitted ONLY on an explicitly authorized WORK_FALLBACK project. The
three related CSV registers use a recoverable single-writer journal: on an
interrupted update, the project validator blocks progress until an explicit
rollback/reconciliation is performed. This is not a multi-user database
transaction and does not provide live remote synchronization. Google Drive
canonical writes must be independently verified by the actual connector.
No automated RIS/BibTeX parser is added beyond existing capabilities.

M4 — SCIENTIFIC ENRICHMENT: Optional Semantic Scholar metadata-only search,
OpenCitations DOI citation counts and Unpaywall DOI OA-status/landing-URL
lookups implemented with MOCK-only tests and explicit network opt-in.
Not citation validation, open-text retrieval or confirmation of OA licence.
Retraction Watch/Crossref, OpenAIRE, CORE, DOAJ, SciELO, BDTD and
Europe PMC remain candidates. Unpaywall SEARCH was retired 2026-09-18;
this module uses DOI lookup only.

M5 — SCOPUS / WOS: Optional per-provider onboarding guidance; no impersonation
of CAFe, no API-key collection in chat. These licensed adapters are intentionally
DISABLED until rights, credential custody, terms governing AI use and a secure
executor are verified. No authenticated test performed.

M6 — ZOTERO / FULL TEXT: An opt-in Zotero own-library metadata reader uses
locally protected ZOTERO_USER_ID and ZOTERO_API_KEY, MOCK-tested only.
No automatic private library connection inside ChatGPT, Zotero note,
attachment or abstractNote export, PDF ingestion, rights confirmation
or scientific fulltext processing. Metadata never proves article reading.

M7 — RELEASE READINESS: PR #24 was merged into `main` following passing
offline regression and release-audit checks. The v0.9.0-beta.2 source
pilot is packaged as experimental `v0.9.0-beta.2` software. Scientific
end-to-end and installed-platform tests remain pending. PR #22 was
not merged or changed by this work.

## Provider technical reference

| Vendor | API | Authentication | Allowed in this pilot |
| --- | --- | --- | --- |
| OpenAlex | https://api.openalex.org/works | Optional secure OPENALEX_API_KEY; vendor-specific current limits | Metadata only |
| Crossref | https://api.crossref.org/works | Public/polite via contact email | Metadata only |
| Scopus | https://dev.elsevier.com/ | Individual API key plus real institutional entitlement | No live integration |
| WoS Starter | https://developer.clarivate.com/apis/wos-starter | X-ApiKey and plan authorization | No live integration |
| WoS Expanded | https://developer.clarivate.com/apis/wos | Licensed API | No live integration |
| Zotero | https://www.zotero.org/support/dev/web_api/v3/start | Private user library key in protected local runtime | Metadata-only mocked adapter; no live test |
| Semantic Scholar | https://api.semanticscholar.org/api-docs/ | Public and scoped key models | Metadata-only mocked adapter |

Do not fix current quotas in code without a source-of-truth refresh.
OpenAlex and Crossref search are NOT semantic substitutes for Scopus/WoS:
preserve per-base literal queries, date, filters, result limitations and
the researcher's methodological decision about scope.

## How to run the local Python pilot

Run only within an authorized environment that already has the complete
existing Meu Artigo project:

~~~sh
python scripts/bibliographic_workflow.py guide --lang pt
python scripts/bibliographic_workflow.py status --project /authorized/project

# No network by default; returns NOT_EXECUTED.
python scripts/bibliographic_workflow.py search --provider openalex \
  --query "governance accountability" --limit 50 --out-dir /private/staging

# Explicit opt-in, subject to runtime network and provider limits.
python scripts/bibliographic_workflow.py search --provider crossref \
  --query "knowledge governance" --limit 50 --out-dir /private/staging \
  --allow-network

# Hybrid: reuse the EXISTING deduplication logic and review its audit.
python scripts/bibliographic_workflow.py dedupe \
  /private/scopus_manually_exported.csv /private/staging/openalex_metadata.csv \
  --out-dir /private/review
~~~

For real, explicitly authorized local fallback projects, the explicit
--commit-local switch additionally appends to the original three canonical
project CSVs using the recoverable journal. Do not modify the registers
manually or run concurrent writers during an import. If an interrupted
journal is detected, stop research and run:
`python scripts/bibliographic_workflow.py recover-local --project /authorized/project`.
Inspect the recovery result and rerun validation. Never use this on a
Drive-canonical project: upload/sync and its actual receipt must be handled
by the real connected Google Drive integration.

The staging receipt records what the LOCAL adapter reported; it is not a
signed vendor response. Exporting a CSV is not scientific screening, DOI
verification, rights confirmation, fulltext reading, evidence evaluation,
human validation, manuscript submission or journal compliance.

## Header integrity of imported bibliographic exports (development only)

The hybrid importer checks CSV, TSV and optional XLSX column headings **before**
converting records into dictionaries. Repeated names (including spacing/case
variants), empty headings, and competing names for the same recognized field
(e.g. `Title` plus `Article Title`, or `Record_ID` plus `Record ID`)
are **not automatically resolved**: all rows from the ambiguous file are
quarantined with a specific diagnostic. Other unambiguous files in the same
invocation may continue processing.

**Verified compatibility exception:** Scopus and Web of Science legitimately
export both short/initialed authors (`Authors` or `AU`) and full author names
(`Author full names` or `AF`) as complementary columns. One short-form plus
one full-form column is accepted, **even when their text differs**, and both
columns are preserved in the canonical export. The existing canonical-author
selection favors the short form when populated; the full form remains available
for human interpretation. A second alias *within the same representation*
still triggers quarantine; other critical fields such as title and DOI have
no exception. An `AF` field alone may supply author names for WoS tabular exports.

**Second compatibility exception:** WoS tabular exports may contain both
`Publication Date` (a date-level value) and `Publication Year` (a year-level
value). This pairing is accepted and retained in separate columns; the
year-level field takes precedence for the normalized year. Two competing
year-level aliases (`Year` plus `Publication Year`) or two date-level
aliases remain ambiguous and are quarantined.

**Supported-format boundary:** the importer handles tabular CSV, TSV and
optional XLSX, including WoS tab-delimited files, but it is **not a parser
for WoS tagged plain-text `FN/VR/AU/AF/TI/ER` records**. Use a licensed,
authorized tabular export or make and verify a conversion; never treat a
tagged .txt as a validated tabular import. These exceptions concern field
formats and do not verify the scientific content.

Tests use **synthetic examples matching documented Scopus/WoS headers**, not
licensed live exports. True end-to-end homologation awaits authorized real
export files and rights confirmation; neither is inferred from passing CI.

The original input files remain unchanged. The import source manifest keeps
the input fingerprint and the quarantine count; positional cell previews
(up to 3,000 characters per row) are available for manual inspection.
The tool does not guess which duplicate column is authoritative or make a
scientific inclusion/exclusion decision. Repair headings in a copy of the
source export and run again in a **new output directory**; preserve the
original evidence and the rejected import report.

## Acceptance criteria before any production release

1. No API connected -> no API onboarding gate, no HTTP call, normal legacy mode.
2. One provider fails -> existing manual research workflow continues.
3. Search results actually received -> accurate provider-specific metadata
   CSV, reported/received counts, timestamp, SHA256 and partial status.
4. Credentials not in logs, exports, stack traces, public bundle or Git.
5. Existing Search_ID, Record_ID, TRACE_ID; no fabricated GATE_ID approval.
6. Hybrid results -> original inputs preserved, original dedup audit reused.
7. Google Drive writes -> independently confirmed; otherwise pending.
8. Scopus/WoS and fulltexts -> require effective rights and secure execution.
9. Native C.A.D.A. remains four fields in order, no extra displayed columns.
10. Complete test suite and release auditors pass on final branch.

## Deferred technical work requiring separate authorization

- Build a secure, user-scoped credential connector with proper consent,
  refresh/revoke, encryption and an auditable isolated executor; never
  prototype one using chat or local project files as a secrets vault.
- Independently confirm Elsevier/Clarivate licences and AI-processing terms.
- Add live service integration/e2e tests only with disposable keys and a
  provider-authorized environment, separate from public CI.
- Add retriever modules for OpenCitations, citation corrections, OA versions,
  institution-owned Zotero libraries, and fulltext with rights evidence.
- Upgrade single-writer recoverable local CSV journals to a concurrency-safe
  transactional persistence design before any multi-user or remote operation.
  Add resumable pagination/checkpoints for large, long-running searches.
- Verify that optional onboarding is offered only once per project with a
  real authorized persistent state write (without creating a science gate).
