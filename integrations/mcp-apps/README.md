# Meu Artigo — host-owned Google Drive, generic MCP Apps companion

## Ownership boundary (mandatory)

**Each researcher connects their own Google Drive through their own ChatGPT
account and ChatGPT's Google Drive connector.** ChatGPT executes permitted
document reads under that account. The Meu Artigo Skill applies methodology
and seven human scientific gates **in ChatGPT**.

This MCP service is limited to a **generic methodological interface**, a
text-only tool `meu_artigo_painel` and a neutral resource
`ui://meu-artigo/site-v1.html`. It MUST NOT read files, articles,
references, project metadata, Google Drive folders, tokens or private
research records, or store any of them on the VPS. A model must NOT
send a research document or Drive ID in tool arguments.

The MCP does **not** manage Google Cloud OAuth, Drive refresh tokens,
Google API calls, identity-to-project registries, journal CAS, shared
folders, or scientific approvals.

A/B/C/operator data separation is enforced at the **host connector**
boundary, not by a shared Google token on this server. The assistant must
only access the Google Drive connector that the current researcher has
authorized in their own ChatGPT session.

## Current interface

- `meu_artigo_painel(locale?,mode?)` accepts only a UI language and
  MINIMAL/FULL display preference. Its response is generic guidance,
  **never** researcher-specific status, task counts or evidence.
- The MCP Apps HTML resource initializes as `HOST_NOT_CONNECTED`.
  The bridge explicitly discards ALL tool results instead of accepting
  `structuredContent.site` from private sources.
- ChatGPT, not this MCP, is responsible for presenting actual research
  information in the conversation and enforcing human scientific gates.
- A complete research dashboard populated from private Drive files cannot
  be offered by this MCP without violating its current privacy boundary.
  If desired, it must be implemented using ChatGPT-native surfaces that
  do not transmit the underlying research content to this server.

## Reproducible local acceptance

Node 20+, Python 3.10+; in `integrations/mcp-apps`:

```bash
npm ci --ignore-scripts --no-audit --no-fund
npm run build
npm run test:smoke
npm run test:synthetic
npm run test:host-boundary
npm run test:http
npm run test:stage10
npm run test:oauth
npm run test:oauth-http
npm run test:stage15
```

Research and Google environment variables are **forbidden** in this
server. Supplying any of the following refuses startup instead of
allowing a data-reading fallback:

`MEU_ARTIGO_PROJECT_ROOT`,
`MEU_ARTIGO_MULTIUSER_REGISTRY`,
`MEU_ARTIGO_TENANT_DATA_ROOT`,
`MEU_ARTIGO_GOOGLE_DRIVE_MODE`,
`MEU_ARTIGO_GOOGLE_TOKEN_DIR`,
`MEU_ARTIGO_GOOGLE_TOKEN_KEY`,
`MEU_ARTIGO_GOOGLE_CLIENT_ID`,
`MEU_ARTIGO_GOOGLE_CLIENT_SECRET`,
`MEU_ARTIGO_GOOGLE_REDIRECT_URI`.

The repository also retains isolated synthetic tests of scientific
projections in Python and browser HTML. Those test artifacts do NOT
represent MCP retrieval of a user's real project.

## Auth0 is MCP access control, never Drive authorization

For a single-identity pilot, `MEU_ARTIGO_AUTH_MODE=auth0` with
`MEU_ARTIGO_PILOT_SUB` enforces one validated pilot subject.

For a generic multi-researcher service, the separate option
`MEU_ARTIGO_MCP_MULTIUSER=YES` permits validated individual human
Auth0 subjects and rejects a simultaneous global pilot allowlist.
Tokens must have a valid RS256 signature, trusted issuer, exact
`https://mcp.allflux.com.br/mcp` audience, bounded lifetime, and
`mcp:read`. **Neither Auth0 setup grants Google Drive access.**

The HTTP service is still bound to `127.0.0.1:8085` by default.
A public HTTPS reverse proxy is NOT provided or enabled here. The
included Nginx template is deliberately disabled (404). Do not deploy
it before actual ChatGPT OAuth, TLS, least-privilege and operational review.

## Scope of evidence

Successful tests prove that the server cannot read project data through
its registered tools, can refuse forbidden storage configuration, and
can serve a neutral UI to MCP clients. They do not prove that a
researcher has connected Google Drive inside their own ChatGPT account,
that the host provides MCP Apps rendering, that real identities have
passed OAuth E2E, or that the research methodology has been independently
validated.

Do not merge, publish, update the Plugin, configure Auth0/Google Cloud,
deploy to VPS, proxy public traffic or access anyone's Drive without
a separate explicit authorization.
