# Stage 10 — Single MCP Apps Server and Transport Boundaries

The only optional production MCP Apps server in this candidate is
`integrations/mcp-apps/server.mjs`. There is one read-only tool
`meu_artigo_painel`, one HTML resource `ui://meu-artigo/site-v1.html`,
and a text `content` fallback whenever the UI is not rendered.

## Isolation and privacy

- The operator alone configures the absolute project root through
  `MEU_ARTIGO_PROJECT_ROOT`. Model-supplied `project`, `root`, or
  `path` arguments never select an alternate workspace.
- Symlinks in the authorized project path are denied using `realpath`.
  This check is not a sandbox against a compromised host or concurrent
  filesystem replacement after the check; OS isolation is still required.
- The Python child receives a minimal environment, not the MCP bearer,
  AWS credentials, Drive tokens, or unrelated host secrets.
- Structured content is sourced from the read-only local projector.
  Untrusted types, missing non-write flags, unsafe next-action codes,
  excessive projection size and malformed records fail closed.
- Returned text summarizes a bounded code and counts, not private task
  content. Neither the server nor UI authorizes scientific gates or Drive sync.
- MCP Apps HTML includes a neutral HOST_NOT_CONNECTED state and an
  embedded bridge. The UI resource is bounded to 2 MiB.
- HTTP uses a strict Bearer authorization header and rejects foreign
  Origins. Requests with non-JSON media, malformed objects, or over
  256 KiB are denied before reaching the MCP transport handler.
- HTTP is strictly loopback-only in Stage 10, even if legacy proxy
  environment flags are set. Public bindings require Stage 11 OAuth and
  resource-specific authorization; operational flags alone are insufficient.
- The Skill ZIP must exclude MCP Apps server code and executable Node
  dependencies. The retired `mcp-preview` implementation does not become
  another production endpoint.

## Synthetic acceptance

The `stage10-contracts.mjs` suite launches real stdio and loopback
Streamable HTTP transports with fictional credentials and paths. It checks
one tool/resource, metadata, JSON limits, strict header syntax, fallback,
error handling and rejection of symlink-backed project aliases.
Previous smoke, synthetic project, HTTP and browser/i18n tests also run.

It does not validate a real ChatGPT host, authenticated human authorization,
Auth0 OAuth, reverse proxy/WAF, browser CORS enforcement, resource upload,
external Drive storage, multi-user isolation, or remote operations.
