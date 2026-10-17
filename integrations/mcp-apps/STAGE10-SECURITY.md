# MCP Apps security: host-only research data boundary

This candidate deliberately exposes a single generic tool
`meu_artigo_painel` and a neutral HTML resource
`ui://meu-artigo/site-v1.html`.

## Security guarantees intended by this implementation

- **No research data**: No project file reader, child process to inspect
  research files, Google APIs, Google refresh tokens, Drive metadata,
  subject-to-project registry or automatic scientific approvals.
- **Host-side Drive only**: Individual researchers use their personal
  ChatGPT Google Drive connector. The MCP cannot and should not obtain
  their Google account grants, documents, IDs, summaries or private
  project progress.
- **Strict arguments**: tool accepts optional locale and MINIMAL/FULL.
  Unknown project paths do not influence the response. It returns neutral
  guidance and no research `structuredContent`.
- **Neutral HTML**: `HOST_NOT_CONNECTED`, no fictional research progress.
  The MCP Apps bridge discards unexpected host tool results to prevent
  researchers' private data from entering the app UI via this server.
- **Startup refusal**: any configured project root, tenant registry,
  Google OAuth secret or token-storage variable blocks startup.
- **Local-only transport**: HTTP binds to 127.0.0.1/::1. Public Nginx
  exposure remains prohibited until independent OAuth acceptance.
- **Standard HTTP guards**: strict Bearer or Auth0 OAuth validation,
  Origin check, JSON/media/body size limit, single stateless MCP request.
- **Authentication is not data authorization**: Auth0 verifies access to
  the generic service; it does not grant access to any Google Drive.
- **No privilege equivalence claims**: the host's Google Drive connector
  handles per-user access according to each user's own consent and
  permissions; the MCP cannot verify or override that boundary.

## Synthetic evidence

`npm run test:host-boundary` uses fictional files, Auth0-signed fake
subjects and a mock JWKS server to verify no project information leaves
the MCP and forbidden storage configurations fail closed. It does not
connect to any real research Drive or user account. Legacy Python/HTML
projection tests run independently of MCP and must not be interpreted
as MCP project read permissions.

A green CI result establishes test coverage at its commit SHA, not live
OAuth/ChatGPT/Drive integration, Nginx safety, installed Plugin freshness
or independent scientific research validity.
