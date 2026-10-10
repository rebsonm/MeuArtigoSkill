# Bibliographic API connectors — optional, never a research entry gate

**Default:** Meu Artigo works normally WITHOUT a bibliographic API. No API
key, network, licence or token may be required for project initialization,
resumption, manual CSV/RIS/BibTeX imports, screening, drafting or submission.
The pre-existing GOOGLE_DRIVE_FIRST *project storage* policy is independent
of optional *bibliographic source* authentication.

## Nonblocking offer at the literature-search stage

At most once per project, when search/export becomes relevant, offer a brief,
non-blocking suggestion in the researcher's language. Portuguese example:

> Você pode continuar normalmente sem conectar APIs. Se desejar automatizar
> buscas e exportações, posso orientar a conexão das suas próprias fontes
> bibliográficas. A opção pode ser ativada depois.

If ignored or declined, continue the current flow without further questions.
No form, scientific approval gate or connection requirement. Older projects
without a connectors setting keep the default OFF.

## Modes

- **MANUAL (default):** current assisted searching and file imports; unchanged.
- **AUTOMATED (opt-in):** query a connected provider using a real authorized
  network executor and the researcher's effective permissions.
- **HYBRID (opt-in):** combine manual Scopus/WoS exports with OpenAlex/Crossref
  API CSVs; retain all input artifacts and per-provider IDs. Use existing
  conservative dedupe_records.py, not a separate identification methodology.

A Python CLI in the repository is not by itself a ChatGPT tool or connected
account. If the session has no authorized execution route, report NOT_EXECUTED
and preserve the manual workflow; never present mocks as a live retrieval.

## Implemented local pilot

- python scripts/bibliographic_workflow.py guide --lang pt
- python scripts/bibliographic_workflow.py status --project PROJECT
- python scripts/bibliographic_workflow.py configure --project PROJECT --provider openalex --enable
- python scripts/bibliographic_workflow.py configure --project PROJECT --provider openalex --disable
- python scripts/bibliographic_workflow.py search --provider openalex --query "..." --limit 50 --out-dir STAGING --allow-network
- python scripts/bibliographic_workflow.py search --provider crossref --query "..." --limit 50 --out-dir STAGING --allow-network
- python scripts/bibliographic_workflow.py search --provider semantic_scholar --query "..." --limit 30 --out-dir STAGING --allow-network
- python scripts/bibliographic_workflow.py dedupe INPUT1.csv INPUT2.csv --out-dir DEDUPED
- python scripts/bibliographic_enrichment.py doi --provider opencitations --doi 10.1234/example --allow-network
- python scripts/bibliographic_enrichment.py doi --provider unpaywall --doi 10.1234/example --allow-network
- python scripts/bibliographic_enrichment.py zotero --limit 25 --out-dir PRIVATE_STAGING --allow-network

The CLI's --allow-network flag is explicit opt-in. Without it the search
does not touch the network. Provider keys are NEVER accepted as CLI arguments.
OPENALEX_API_KEY, SEMANTIC_SCHOLAR_API_KEY, MEU_ARTIGO_CONTACT_EMAIL,
OPENCITATIONS_ACCESS_TOKEN, ZOTERO_USER_ID and ZOTERO_API_KEY may be supplied
by the local user's protected execution environment, never pasted into ChatGPT
or saved with the article. DOI enrichment and Zotero have separate opt-in commands.

The configure command records an optional preference only on an explicitly
authorized local WORK_FALLBACK project; it is NOT credential authorization.
Removing an optional preference is not equivalent to revoking a token at the
provider; the researcher must revoke keys at the actual vendor when required.

The output CSV and sanitized receipt are staging files. --commit-local may
append search, screening and trace rows only to WORK_FALLBACK projects with
recorded explicit authorization; the script NEVER claims Google Drive sync.
For Drive-canonical projects, the host needs to execute an authorized real
Drive write and verify it separately. Project scientific gates are unchanged.

## Scientific and security guardrails

- Preserve research question, conceptual query, literal base-specific query,
  actual filters, timestamp, received count, provider-reported count and
  partial/error state. Search semantics differ between providers.
- A bound of 50 records is not an exhaustive literature search. PARTIAL means
  limited/unfinished retrieval. NOT_EXECUTED, AUTH_FAILED, LICENSE_BLOCKED,
  NETWORK_ERROR and RATE_LIMITED must not be mistaken for zero matches.
- Metadata/DOI does NOT establish fulltext access, reading, synthesis quality
  or human scientific validation. Keep [L]/[I]/[P] and approvals separate.
- The existing deduplication engine preserves originals, exact-DOI audit and
  review-required near duplicates, instead of silently deleting evidence.
- BYOC is private and isolated; secrets never enter prompts, Drive, CSV, ZIP
  or logs. A provider API entitlement is not necessarily authorization to
  process licensed content using a third-party AI service.
- No CAFe password, SAML cookies, paywall/captcha or quota bypass.

## Candidate support status — never overclaim real tests

| Provider | Implementation here | Review point |
| --- | --- | --- |
| OpenAlex | Opt-in metadata CLI, mocked offline tests | Vendor limits, actual current key policy |
| Crossref | Opt-in metadata CLI, mocked offline tests | Polite pool and pagination |
| Scopus | Guidance ONLY | Institutional entitlements, Elsevier AI/retention terms |
| WoS Starter / Expanded | Guidance ONLY | Plan and effective API licence |
| OpenCitations | DOI citation-count lookup, mocked offline tests | Coverage, citation context requires scientific review |
| Semantic Scholar | Opt-in metadata-only search, mocked offline tests | Academic graph, field and rate limits |
| Crossref / Retraction Watch | Candidate | Retractions and correction notifications |
| OpenAIRE / CORE / DOAJ / SciELO / BDTD / Europe PMC | Candidates | OA/domain-specific coverage, provider terms |
| Unpaywall | Opt-in DOI OA-status/URL lookup, mocked offline tests | Search retired September 18, 2026; no PDFs downloaded |
| Zotero | Optional own-library METADATA reader via secure runtime key, mocked offline tests | No notes, attachments or article fulltext |

## Official references — recheck when implementing later adapters

- [OpenAlex](https://help.openalex.org/api/)
- [Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/)
- [Elsevier authentication](https://dev.elsevier.com/tecdoc_api_authentication.html)
- [Elsevier terms](https://dev.elsevier.com/api_service_agreement.html)
- [WoS Starter](https://developer.clarivate.com/apis/wos-starter)
- [WoS Expanded](https://developer.clarivate.com/apis/wos)
- [Semantic Scholar](https://api.semanticscholar.org/api-docs/)
- [OpenCitations](https://api.opencitations.net/index/v2)
- [Retraction Watch](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/)
- [Unpaywall](https://unpaywall.org/api)
- [Zotero](https://www.zotero.org/support/dev/web_api/v3/start)
