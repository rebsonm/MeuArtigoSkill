# Meu Artigo — read-only multiuser MCP pilot

This is an isolated engineering candidate derived from PR #78. **Not
approved for public traffic**, live researchers, Google Drive access, or
production. Never enable an Nginx `proxy_pass` from these instructions.

## Request security boundary

1. HTTPS reverse proxy terminates TLS (not provided by this change).
2. The MCP service accepts connections **only on 127.0.0.1 / ::1**.
3. Auth0 JWT verified by trusted remote JWKS: exact issuer and audience,
   RS256 signature, iat/exp <= 3600s, mandatory `mcp:read`.
4. On each HTTP request, a verified `sub` is looked up in a private
   read-only registry **before** tools can execute. Unknown subject -> 403.
5. The request gets a **new MCP server bound only to that subject's project map**.
6. `project_id` is a stable slug, not a filesystem path; wrong-owner,
   traversal and unknown slugs resolve to no project. If the user has
   multiple projects, an explicit allowed `project_id` is required.
7. `meu_artigo_projetos` lists only authorized IDs; `meu_artigo_painel`
   returns a read-only, bounded project projection and never grants gates.
8. Live Drive access, multiuser Drive tokens, manuscript sharing,
   mutable project state, and other MCP tools are **not implemented**.

## Private registry

Store the registry **outside git and outside the project directories**:

```json
{
  "schema": "MEU_ARTIGO_TENANT_REGISTRY_V1",
  "tenants": [
    {"subject": "google-oauth2|FAKE_IDENTITY_A12345",
     "tenant_id": "tenant-alpha", "projects": ["paper-one", "paper-two"]},
    {"subject": "google-oauth2|FAKE_IDENTITY_B12345",
     "tenant_id": "tenant-bravo", "projects": ["paper-one"]}
  ]
}
```

The identities above are **synthetic examples**, not actual users.

With an operator-chosen `MEU_ARTIGO_TENANT_DATA_ROOT=/srv/meu-artigo/tenants`,
the trusted registry maps these projects only to:

- `/srv/meu-artigo/tenants/tenant-alpha/paper-one`
- `/srv/meu-artigo/tenants/tenant-alpha/paper-two`
- `/srv/meu-artigo/tenants/tenant-bravo/paper-one`

Directory names are derived exclusively from validated registry IDs.
The registry file must be regular, non-symlinked, <=64KiB and `0600`
on POSIX. The data root, tenant directories and project directories must
already exist, be absolute and canonical (no symlink path).
Duplicate subjects, duplicate tenants, duplicate projects and missing roots
**block startup**. The registry is a read-once snapshot: changes need
a deliberate service restart and reapproval.

Example **only after local acceptance**, under a dedicated unprivileged
service account and protected configuration (do not store secrets in
environment files within git):

```sh
export MEU_ARTIGO_AUTH_MODE=auth0
export MEU_ARTIGO_AUTH_ISSUER=https://YOUR_AUTH0_TENANT.us.auth0.com/
export MEU_ARTIGO_AUTH_RESOURCE=https://mcp.allflux.com.br/mcp
export MEU_ARTIGO_MULTIUSER_REGISTRY=/etc/meu-artigo/tenants.json
export MEU_ARTIGO_TENANT_DATA_ROOT=/srv/meu-artigo/tenants
unset MEU_ARTIGO_PILOT_SUB
unset MEU_ARTIGO_PROJECT_ROOT
# No public bind. Keep 127.0.0.1 until real OAuth/callback,
# proxy and consent are independently approved.
node server.mjs --http
```

The old single-user pilot remains possible when both
`MEU_ARTIGO_MULTIUSER_REGISTRY` and
`MEU_ARTIGO_TENANT_DATA_ROOT` are absent, using an exact
`MEU_ARTIGO_PILOT_SUB`. Mixed single-user/multiuser settings fail closed.
There is **no safe multiuser mode over stdio**, as stdio lacks the
authenticated HTTP request identity.

## Tests

From `integrations/mcp-apps`:

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm run build
npm run test:multiuser
npm run test:stage10
npm run test:oauth
npm run test:oauth-http
```

`test:multiuser` uses disposable directories and a locally generated
RS256 signing key/JWKS server, **not** a real Auth0 tenant. It checks
valid and invalid JWT identities, scope/audience denials, two users,
three projects, permission leakage, independent parallel calls,
private-registry permissions, duplicate identities and symlink
attacks. Passing these tests does not prove real ChatGPT OAuth,
tenant-specific storage permissions, UI rendering, revocation latency,
concurrency/load limits or live HTTPS hosting.

## Mandatory external acceptance before deployment

- Independently verify Auth0 application/client registration, PKCE,
  callback redirect URIs, issuer/audience, scopes and organization
  permissions in ChatGPT's actual MCP client.
- Test unauthorized users and cross-user reads in a private E2E
  environment with disposable accounts, immutable test projects,
  incident logs without private content, and a kill switch.
- Validate a hardened execution boundary (dedicated service account,
  filesystem permissions, read-only volumes, no other tenants' system
  credentials, request limits, timeouts, proxy/TLS).
- Decide how each researcher's Google Drive will be authorized,
  encrypted, scoped and revoked. **No Drive support is implied here.**
- Obtain explicit approval to connect Nginx publicly, change Auth0,
  install/update the Plugin, run production E2E, or merge PRs.

Do not conflate local synthetic validation with a live multiuser deployment.
