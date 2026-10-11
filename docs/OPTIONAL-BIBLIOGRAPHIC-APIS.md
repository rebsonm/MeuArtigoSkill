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

**Supported-format boundary:** the importer handles tabular CSV, TSV,
optional XLSX (`openpyxl`) and, in the development branch, **legacy binary
Excel .xls** (`xlrd>=2.0.2`). WoS `savedrecs.xls` workbooks are read-only;
original bytes are not rewritten or converted in place. Install the optional
reader in the authorized runtime or use a separately verified CSV/XLSX copy.
If an opt-in XLS/XLSX reader is absent, that file receives a
MISSING_OPTIONAL_EXCEL_PARSER diagnostic and a fingerprint (when readable);
other input files in the batch continue to import. Absence of a parser must
not erase valid CSV/TSV evidence or be described as scientific rejection.
Legacy XLS date/numeric values are normalized for import without fabricating
scientific identifiers. The first worksheet is read as a table; it must have
unique or compatible headings, and ambiguous sheets are quarantined by input.
This reader is an **opt-in runtime dependency**, not a bundled or authenticated
WoS connector. The original XLS and its recorded SHA-256 remain the provenance
source. Do not interpret successful parsing as an institutional rights check.

**WoS tagged plain-text `FN/VR/AU/AF/TI/ER` records are still NOT
tabular CSV/TSV/XLS and remain unsupported**. Convert and verify separately
before import, while preserving original content and provenance. Passing
synthetic XLS tests does not constitute a live-provider or real-file
homologation. Manual testing with licensed real exports was **waived for
this development iteration by the maintainer**, not declared passed.

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

## PR #45 — Verifiable staging provenance and partial failures

The manual mode remains available without connecting any API. Automated
metadata retrieval is attempted only with explicit opt-in; synthetic tests
cannot establish live access, provider coverage, or rights under licensed
API agreements.

OpenAlex, Crossref and Semantic Scholar metadata clients mark malformed
pages, including invalid items, as `INVALID_RESPONSE` rather than silently
dropping records and reporting `COMPLETE`. Earlier valid pages remain
separate and are marked `PARTIAL`, with the failure cause in `error_code`.
A Crossref query requiring further pages but lacking a valid cursor reports
`PARTIAL`/`PAGINATION_INCOMPLETE`. Bounded results do not establish
complete coverage of any external provider.

The `retrieval_receipt.json` stage receipt records the provider, literal
query, timestamp, records received, provider-reported total, pages, status,
interruption reason and CSV SHA-256. Existing staged CSV or receipt files
cannot be silently overwritten. Receipt writing uses a temporary file and
atomic replacement.

The `--commit-local` switch records results **only** in an explicitly
authorized `WORK_FALLBACK` project, with intact CSV and receipt already
inside that project's permitted staging area. Before any scientific
register changes, it checks file hashes, receipt data and exact
correspondence between exported rows and in-memory results. A failed
check, forged receipt, changed file or unauthorized path blocks the commit.
Partial-search receipts preserve error codes and the content hash in
`02_Search_Log.csv` and `13_Traceability_Log.csv`; the scientific
operation remains `UNVERIFIED`. Human screening is not inferred.

These guarantees are local. A receipt does not independently authenticate
the remote server; SHA-256 cannot prove that a real API query took place.
Google Drive requires separate verified writes and read-back. Fixtures
are synthetic; no authenticated Scopus/Web of Science operation and no
release approval is implied.

## PR #46 — Transport security and private export

Optional OpenAlex/Crossref/Semantic Scholar search and
Unpaywall/OpenCitations/Zotero enrichment use only HTTPS destinations
on a strict provider allowlist. The shared HTTP layer refuses automatic
301, 302, 303, 307 and 308 redirects, preventing personal keys and
Zotero credentials from being forwarded to unexpected hosts.
`REDIRECT_BLOCKED` reports a safe error code without printing tokens,
headers or redirect destinations. Response size and format are bounded
before accepting metadata; HTTP/transport failures are reported safely.
Tests use offline simulated responses, not real user accounts.

The optional user-owned Zotero library export remains limited to
permitted bibliographic fields: no private notes, tags, attachments,
abstracts or API keys. IDs must be ASCII decimal; credentials with CR/LF
are rejected. Structurally invalid Zotero items fail the request rather
than being counted as a complete success. Staged private files receive
local `0600` permissions and are written first to temporary files,
then published with exclusive creation, without overwriting previous
results. An error must not expose a partial CSV.

Limitations: synthetic tests cannot verify actual licensed operation,
response authenticity, universal vendor compliance, complete OS
security, real Google Drive synchronization or scientific validity.
API use remains strictly optional; declining access never blocks
manual research. These tests do not authorize a release by themselves.

## PR #47 — Integrated manual-source and API checks

Manual Scopus and Web of Science files (CSV, TSV, XLSX or XLS with an
authorized optional reader) may be combined with OpenAlex/Crossref/
Semantic Scholar metadata, without requesting licensed database
credentials or simulating CAFe access. The existing
`scripts/dedupe_records.py` remains the sole conservative deduplicator:
exact identity by DOI or by title/author/year when appropriate; near
matches remain `REVIEW_REQUIRED`, never silently removed.

DOI comparison requires a complete normalized DOI match; spurious
suffixes containing spaces or additional text must not create an exact
identity. Every preserved input is assigned a stable `INPUT-xxxx`
identifier and SHA-256. The deduplicator fingerprints files before
and after parsing and checks each input again before publishing output.
Any source change during processing aborts the batch without declaring
an intact merged output. This is not a multi-process writer lock or
proof of a digital signature.

When a manual input cannot be read or has rejected records, valid rows
from other inputs remain inspectable, while
`import_diagnostics.json` records `status=PARTIAL_INPUTS` and
`requires_researcher_review=true`; the terminal also displays
`import_status=PARTIAL_INPUTS`. For compatibility the CLI may still
return exit code 0 if valid data from other sources exist: **exit code
alone does not establish import completeness**. Review diagnostics
and provenance before subsequent scientific gates. An entirely invalid
bibliographic batch remains a failure.

Deduplication creates a reviewable stage; it does not approve screening,
freeze the corpus, change human decisions or synchronize Google Drive.
An optional separate, authorized `WORK_FALLBACK` operation can register
API metadata while retaining pending screening decisions and scientific
statuses. Passing code tests or local hashes cannot authenticate a
remote query, imply scientific rights or authorize software publication.
