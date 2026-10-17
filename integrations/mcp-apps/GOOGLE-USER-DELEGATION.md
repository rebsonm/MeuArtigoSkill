# Per-researcher Google Drive delegation: identity and isolation

## Mandatory invariant

**The maintainer's Google Drive credentials must never be used as a default
for other researchers.** Every researcher (owner, A, B or C) must authorize
their **own** Google account independently. The ChatGPT/Auth0 access token
authenticates the researcher to the MCP service but does **not** authorize
Google Drive access. Do not reuse the operator's ChatGPT Google connector
as the server's Drive credentials.

Identity flow: ChatGPT -> signed individual Auth0 JWT -> Auth0 subject
`google-oauth2|<google-sub>` -> separate researcher-initiated Google OAuth
consent -> Google UserInfo subject must match the original Auth0 Google
subject -> independently encrypted grant under that user's subject ->
Google Drive request with the **same user's** delegated OAuth token.

An unlinked subject, wrong Google account, rejected consent, expired/replayed
state, revoked grant, provider mismatch or invalid folder structure
must **never** fall back to the maintainer's Drive, another user's grant
or a local registry project.

### Explicitly separate the two implementations

- **Legacy engineering pilot:** `MEU_ARTIGO_MULTIUSER_REGISTRY` and
  `MEU_ARTIGO_TENANT_DATA_ROOT` authorize independent *local*
  projects. This does **not** establish independent Google Drive access.
- **Per-user Google Drive engineering candidate:** set
  `MEU_ARTIGO_GOOGLE_DRIVE_MODE=per_user`. Requires a valid Auth0 identity
  and separate Google OAuth consent. Explicitly excludes global
  `MEU_ARTIGO_PROJECT_ROOT`, `MEU_ARTIGO_PILOT_SUB` and the old local
  tenant registry. Those settings must not be mixed.

The current Google mode implements **read-only folder metadata** for
`My Drive/Meu Artigo/<individual research project folder>`. It does
not read paper contents, download documents, create folders, manage
sharing, synchronize journals or write to Drive. The rich scientific
panel is deliberately unavailable in this mode until a canonical
Drive-specific read adapter is verified. No silent local fallback.

### Tools bound to a verified individual Auth0 subject

- `meu_artigo_google_conectar`: issue a one-time Google consent URL with
  PKCE S256, unguessable OAuth state and a 10-minute expiration.
- `meu_artigo_google_status`: report only that researcher's connection.
- `meu_artigo_google_projetos`: refresh only that researcher's encrypted
  Google grant, recheck the Google UserInfo subject, resolve the exact
  `Meu Artigo` folder as a direct child of the current Google user's
  My Drive root and list only its direct child project folders.
  Validate parent IDs, page bounds and duplicate roots. Do not claim
  article content has been synchronized or screened.
- `meu_artigo_google_desconectar`: discard only this researcher's locally
  stored Google grant. Does not delete or update Google files. Users
  can also revoke the app directly from their Google Account settings.

## Credential protection

- Never use a global Google API key, shared OAuth refresh token, general
  service account, administrator Drive connector, or domain-wide delegation.
- Each user obtains their own refresh grant. Store **only** this encrypted
  refresh token at rest with AES-256-GCM, a per-subject AAD binding, and a
  filename derived from SHA-256(Auth0 subject). Do not echo access or
  refresh tokens to the model, UI, repository, logs or MCP output.
- The private credential directory must already exist, be canonical,
  be owned by the dedicated service user and have POSIX mode 0700.
  Credential files use mode 0600, no-follow reads and atomic writes.
  Keep the 32-byte encryption key outside repository files.
- Refresh access tokens only for the authenticated subject and validate
  Google UserInfo subject for **each** Drive read.
- Reject accounts whose stable Auth0 Google subject differs from the
  Google OAuth subject, even if an email address looks identical.
- The separate OAuth callback endpoint
  `https://mcp.allflux.com.br/google/oauth/callback` is a GET
  redirect from Google's browser flow, without an Auth0 bearer header.
  It is authorized by single-use state + PKCE + exact Google subject
  matching before any grant is persisted.
- Protect the callback behind TLS when authorized for deployment.
  Disable or redact query strings in Nginx access logs at this path,
  because the callback contains a short-lived authorization code.
- The Node service remains loopback-only (127.0.0.1:8085). No public
  Nginx proxy is enabled by this change.

### Google scope and platform requirements

The initial delegated scope is `openid` plus
`https://www.googleapis.com/auth/drive.metadata.readonly`.
According to Google's documentation, the Drive metadata scope
is **restricted**, cannot download document contents, and may require
OAuth app verification and an independent security assessment before
public distribution. New functionality should request an additional
least-privilege scope only after explicit user consent and review.

**Google Cloud configuration to be authorized separately:** create a
test Web OAuth client, enable Google Drive API, configure the consent
screen and test users, approve the exact redirect URI, and store
client credentials in an approved secrets manager.

**Auth0 configuration to be authorized separately:** validate each
Google-backed Auth0 subject, audience `https://mcp.allflux.com.br/mcp`,
RS256 trusted JWKS signature, permitted client, callback, PKCE and
`mcp:read`. Equality of emails is **not** sufficient.

Example environment **only for a controlled, separately authorized pilot**:

```sh
MEU_ARTIGO_AUTH_MODE=auth0
MEU_ARTIGO_AUTH_ISSUER=https://YOUR_TENANT.us.auth0.com/
MEU_ARTIGO_AUTH_RESOURCE=https://mcp.allflux.com.br/mcp
MEU_ARTIGO_GOOGLE_DRIVE_MODE=per_user
MEU_ARTIGO_GOOGLE_CLIENT_ID=<Google Cloud web OAuth client ID>
MEU_ARTIGO_GOOGLE_CLIENT_SECRET=<from secrets manager>
MEU_ARTIGO_GOOGLE_REDIRECT_URI=https://mcp.allflux.com.br/google/oauth/callback
MEU_ARTIGO_GOOGLE_TOKEN_DIR=/var/lib/meu-artigo/private-google-grants
MEU_ARTIGO_GOOGLE_TOKEN_KEY=<32-byte AES key, base64url>
MEU_ARTIGO_BIND_HOST=127.0.0.1
MEU_ARTIGO_MCP_PORT=8085
```

Do **not** define `MEU_ARTIGO_PILOT_SUB`,
`MEU_ARTIGO_PROJECT_ROOT`, `MEU_ARTIGO_MULTIUSER_REGISTRY` or
`MEU_ARTIGO_TENANT_DATA_ROOT` in this mode.

### Operator privilege and privacy limits

The MCP application's users are isolated by per-principal authorization.
However, a privileged VPS operator with access to the encryption key,
secret store, process memory or operating-system administration may still
technically compromise grants. This is **not end-to-end zero-knowledge
encryption against the server administrator**. Preventing even a hosting
administrator from accessing grants requires an additional key-custody
architecture and independent audits. Do not claim absolute isolation
against every privileged operator.

## Evidence and acceptance

The synthetic `npm run test:google-delegation` uses a fake Google OAuth
provider and fake Drive API, not real accounts. It verifies independent
A/B consent, PKCE, one-time state, subject mismatch rejection, separate
encrypted refresh grants, individual refresh and Google UserInfo
verification, canonical folder parent scoping, independent A/B results,
scoped disconnect, and refusal of unsafe token directories and global
project fallback. Existing MCP CI tests, supply-chain checks and the
release audit run alongside the new suite.

Passing these checks does not prove a live Auth0 tenant, Google OAuth
verification, ChatGPT connection, user-owned Drive content operations,
revocation timing, load isolation, VPS hardening, user-facing usability,
or an installed Plugin update. **No merge, release, public deployment,
Auth0/Google Cloud modification, plugin update or real Drive write
is authorized by this document.**
