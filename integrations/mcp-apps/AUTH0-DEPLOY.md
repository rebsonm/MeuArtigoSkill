# Meu Artigo MCP — Auth0 + Google, pilot deployment guide (2026-10-16)

Status: staged source candidate, not installed on the Contabo VPS and not
connected to ChatGPT. Do not enable the public proxy until all checks pass.

## Exact registered values

- Auth0 issuer: `https://YOUR_AUTH0_TENANT.us.auth0.com/`
- API v2 identifier / MCP canonical resource: `https://mcp.allflux.com.br/mcp`
- Read-only API scope: `mcp:read`
- Protected resource metadata: `https://mcp.allflux.com.br/.well-known/oauth-protected-resource`
- JWT verification: RS256 from Auth0 JWKS; exact issuer/audience, expiry and scope
- Pilot isolation: exactly one privately configured Google/Auth0 subject
- No Drive sync, analytics, email collection, third-party telemetry or corpus capture
- No multi-user hosting or cross-tenant project access in this candidate

## Auth0 administrator tasks

1. In Applications → APIs → Meu Artigo MCP API v2 → Permissions, define
   `mcp:read` with description `Read authorized Meu Artigo dashboard`.
2. Keep the API's user-delegated access policy as `Per-app authorization`.
3. In Tenant Settings → Advanced, keep the Resource Parameter Compatibility
   Profile enabled.
4. Google Social `google-oauth2` works for the existing `meu-artigo` Web
   Application, but that app is not ChatGPT's client. A ChatGPT client must
   separately be registered/approved by CIMD, DCR or a predefined OAuth
   client. Auth0 supports third-party clients with mandatory PKCE and explicit
   API client grants. Do not enable open DCR or `All apps allowed` casually.
5. The Google social connection may need promotion to domain level for
   third-party OAuth clients (consult Auth0 third-party connections guidance).
6. Use ChatGPT MCP management's actual callback URI; do not guess it. Auth0
   authorization response issuer identification determines callback mode.
7. Ensure a third-party client has an explicit user-delegated grant allowing
   only `mcp:read` on the v2 API. Complete client registration and test user
   consent before attempting ChatGPT connection. Never give ChatGPT the
   `meu-artigo` Regular Web Application's client secret.

## Test source locally on a private developer machine

```sh
cd integrations/mcp-apps
npm install --no-audit --no-fund
npm run build
npm run test:oauth
npm run test:oauth-http
npm run test:http
npm run test:synthetic
npm run test:i18n
npm run test:smoke
```

These tests use synthetic JWTs, a local fake JWKS server, and local-only MCP
requests. They do not call Google, authenticate real users or prove ChatGPT
connectivity.

## Contabo source-only staging — do not activate HTTP OAuth yet

On VPS `YOUR_VPS_IPV4`, after reviewing the PR and CI results, the operator
may fetch the candidate branch using the existing non-root `meuartigo`
account. Avoid updating the VPS by `git pull` from the old feature branch
without naming the new branch.

```sh
runuser -u meuartigo -- git -C /opt/meu-artigo/repo fetch origin feat/mcp-auth0-oauth-2026-10-16
runuser -u meuartigo -- git -C /opt/meu-artigo/repo switch --detach origin/feat/mcp-auth0-oauth-2026-10-16
cd /opt/meu-artigo/repo/integrations/mcp-apps
runuser -u meuartigo -- npm install --no-audit --no-fund
runuser -u meuartigo -- npm run build
runuser -u meuartigo -- npm run test:oauth
runuser -u meuartigo -- npm run test:oauth-http
runuser -u meuartigo -- npm run test:http
```

The current `meu-artigo-mcp.service` may continue running the old Node
process until explicitly restarted. No GitHub CI test proves the VPS works.

## Manual pilot authentication settings — private on VPS only

Only after Auth0 configuration and tests pass, the operator should add to
root-owned `/etc/meu-artigo/mcp.env` (mode 0600), replacing the example
subject with the exact authenticated Auth0 user `sub`. Never put an actual
subject, token or client secret into public GitHub issues, CI output or chat.

```dotenv
MEU_ARTIGO_AUTH_MODE=auth0
MEU_ARTIGO_AUTH_ISSUER=https://YOUR_AUTH0_TENANT.us.auth0.com/
MEU_ARTIGO_AUTH_RESOURCE=https://mcp.allflux.com.br/mcp
MEU_ARTIGO_PILOT_SUB=google-oauth2|REPLACE_WITH_PRIVATE_AUTH0_SUB
```

The older local bearer secret can remain for rollback but is ignored in
`auth0` mode. With pilot subject unset or malformed, the HTTP process fails
closed at startup. With the wrong subject or a token for another audience,
it rejects access. The tool cannot select project roots; when none is
authorized, it returns safe text fallback. Do not set a real project root
until the pilot has verified both authorization and ownership.

On activation, restart only `meu-artigo-mcp.service`, confirm the local
metadata endpoint responds with the exact Auth0 issuer and MCP resource,
and verify `POST http://127.0.0.1:8085/mcp` without credentials returns
`401` plus `WWW-Authenticate` (without revealing any token). The default
Nginx site is intentionally still `404` to outsiders.

## Nginx publication (last step, not yet authorized)

A separate reviewed example exists in
`integrations/mcp-apps/deploy/nginx-auth0.conf.example`.
Use it only after the OAuth service is running and the Auth0 ChatGPT client
has explicit user-delegated scope permission. Test
`nginx -t` before reloading. This changes only the
`mcp.allflux.com.br` virtual host and leaves AllFlux/EMGERN untouched.

Before opening `/mcp`, verify:
- Correct certificate/SNI, HTTPS 404 outside metadata and /mcp.
- Metadata from HTTPS returns `resource` and `authorization_servers`.
- Missing/invalid/wrong-account/wrong-audience tokens receive 401/403.
- Valid pilot account (Google/Auth0) receives tool and UI resource.
- Access after logout, expiry and consent denial behaves correctly.
- No tokens, emails, prompts, research text or identifiers in access logs.
- Existing `sigae_web`, `sigae_queue`, `allflux_db`, `allflux_redis`
  and other Nginx sites remain healthy.
- Certificate renewal hook reloads Nginx when cert rotates.
- Multi-user and telemetry stay off pending design/ethics review.

## Rollback

If the new OAuth service is unhealthy, restore the previous Nginx
`mcp.allflux.com.br` configuration that returns public `404` first,
test `nginx -t`, and reload Nginx. Switch Git back to the prior tested
commit `37c5b928765012b5dbb274a2aecac65aa8c3752c`, restore the prior
`mcp.env` backup, then restart only the Meu Artigo service and verify
internal `401`. Do not reboot the VPS or touch SIGAE/AllFlux.

Sources:
- https://developers.openai.com/plugins/build/auth
- https://auth0.com/docs/get-started/applications/dynamic-client-registration
- https://auth0.com/docs/get-started/apis/add-api-permissions
- https://auth0.com/docs/get-started/applications/third-party-applications/security-controls
