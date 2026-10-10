# Meu Artigo Visual — optional in-chat scientific cockpit (MVP)

Status: **experimental integration on a feature branch**. This is a read-only
companion to the Skill, not a new scientific method, project database,
or independently evaluated UX. See the source in visual-app/.

## What is actually implemented

- scripts/visual_dashboard.py reads the existing project configuration and
  canonical CSV registers, never overwriting them.
- A portable CLI renders a compact text or JSON progress view.
- A standalone MCP Apps companion server exposes meu_artigo_dashboard as
  a read-only tool and associates it with a ui:// resource.
- The UI has overview, C.A.D.A. tasks, researcher validation gates,
  evidence/register counts, and registered event/sync summaries.
- MINIMAL and FULL control only what is presented; they do not alter the
  scientific checks. Small screens and light/dark host preferences are supported.
- Tests verify missing data, task/approval separation, deadlines, storage
  uncertainty and non-mutation. A separate MCP smoke test exercises actual
  tool discovery, tool execution and UI resource reading over stdio.

This integration does not install or authenticate Drive connectors, deploy a
hosted app, inspect ChatGPT entitlements, prove independent human approval, or
perform database searching, journal submissions or task writes.

## CLI — works without a chat UI

Prerequisite: an existing authorized local/Work **mirror** of a canonical
Meu Artigo project. For Drive-canonical projects, local data must have
actually synchronized before it is treated as current.

~~~sh
python scripts/visual_dashboard.py /absolute/path/ARTIGO_PROJECT --format text
python scripts/visual_dashboard.py /absolute/path/ARTIGO_PROJECT --mode FULL --format json
~~~

If PROJECT_CONFIG.json does not exist, the reader fails. It does not silently
load synthetic demonstration data. Missing tables are shown as unavailable,
not as zero or done. It never modifies project files.

## MCP Apps companion — local setup

Requires Python 3.10+, Node 20+ and an MCP Apps compatible host.

~~~sh
cd visual-app
npm install
npm run build
MEU_ARTIGO_PROJECT_ROOT=/absolute/path/ARTIGO_PROJECT npm start
~~~

The HTTP endpoint listens on 127.0.0.1:3001/mcp by default. For a local
stdio-compatible MCP client, after building use:

~~~sh
MEU_ARTIGO_PROJECT_ROOT=/absolute/path/ARTIGO_PROJECT node dist/main.js --stdio
~~~

Change the Python executable with MEU_ARTIGO_PYTHON if necessary.
Only the operator chooses MEU_ARTIGO_PROJECT_ROOT; the MCP tool does
not accept a path. Its outputs are limited read-only projections rather
than full texts, abstracts, research questions or source PDFs.

**The application does not become available in ChatGPT just because the
repository includes it.** An operator must deploy/connect a compatible
MCP server to an authorized host. A remote connection needs HTTPS,
the host's approved authentication/authorization approach, and a
persistent, authorized research data adapter. This MVP reads ONLY
the configured local mirror. There is no live Google Drive adapter.

### Security boundary

The default HTTP bind is loopback. Binding to any non-loopback host
requires MEU_ARTIGO_BEARER_TOKEN with at least 32 characters, alongside
a trusted HTTPS reverse proxy, traffic/identity controls, and a suitably
restricted runtime. MEU_ARTIGO_ALLOWED_ORIGIN may be used to restrict CORS.
Do not expose the local project filesystem or use the example server as
a public multi-user SaaS application. Each user must have isolated,
authorized storage and credentials in any future hosted deployment.

Tokens should be generated privately and never committed to Git.
Do not upload private, copyrighted, or confidential research artifacts
to a public demonstration server. Never log project payloads.

## Provenance and meaning of dashboard values

Operational metrics count task rows as *recorded*, not as objectively
completed work. Gates are counted as documented approvals only when
their status, decision, validator and validation evidence fields are set.
This tests field presence, not identity or scientific correctness.
Researcher-authored decisions and formative rationales remain governed
by the existing project rules and validators.

Search count means logged search rows; a database access event is not
confirmed just because a spreadsheet cell says COMPLETE. Screening
record count is not a number of consulted full texts. Evidence rows and
claims do not demonstrate semantic support or originality. The panel
never computes a scientific quality percentage.

The reported storage state comes from PROJECT_CONFIG.json; live Drive
synchronization is explicitly UNKNOWN unless verified elsewhere.
External work-manager conflict counts are only records in PM_Sync.

## UX flows

The overview answers four user questions: Where am I? What has been
registered as done? What is still missing? What is the next executable
action/real researcher decision? The tabs provide progressive detail
without adding new canonical tabs or ID families.

User actions are confined to navigation, refresh and MINIMAL/FULL
projection. Task completion, gate approvals, source screening and
methodological choices remain exclusively with existing controlled
workflows. No action in this UI writes to a project.

## Follow-on work before production

1. Validate npm build and MCP host round-trip with real connected host.
2. Add an authorized Google Drive adapter without compromising the
   canonical-state/reconciliation requirements.
3. Add authenticated per-user/tenant isolation and production HTTPS
   before any remote deployment.
4. Test with real consenting researchers; measure usability without
   asserting causal scientific benefits.
5. Extend method-specific stage labels and claims provenance detail
   without conflating [L], [I], [P] or methods.
6. Consider write actions only with authorization, checks, receipts
   and human scientific decision rules intact.

## Standards

MCP Apps specification (2026-01-26):
https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx

Official implementation quickstart:
https://apps.extensions.modelcontextprotocol.io/api/documents/quickstart.html
