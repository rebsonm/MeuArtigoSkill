# Stage 11 — Auth0 OAuth source-only integration

This release candidate is NOT deployed, connected to ChatGPT, or exposed
outside loopback. Exactly one MCP Apps server remains: `server.mjs`.
The server has one read-only tool and one HTML resource.

## Protected resource configuration (no actual credentials in this repository)

- `MEU_ARTIGO_AUTH_MODE=auth0` explicitly enables OAuth validation on loopback.
- `MEU_ARTIGO_AUTH_ISSUER=https://YOUR_TENANT.us.auth0.com/` is exact,
  HTTPS-only, tenant-bound, and ends with a slash.
- `MEU_ARTIGO_AUTH_RESOURCE=https://YOUR_MCP_HOST.example/mcp` is the
  exact audience and public resource identifier; no query or fragment.
- `MEU_ARTIGO_PILOT_SUB` must be the EXACT privately configured
  `google-oauth2|...` subject of the one authorized pilot account.
- `mcp:read` must be granted to the approved user-delegated client for
  this API. A subject allowlist does not prove that the connected OAuth
  client is approved or that a Google account owns an arbitrary project.

The repository's source-control `.gitignore` excludes local secret
files, private-key material, cache directories and compiled browser
artifacts. Ignore rules are only a preventive convenience: they do not
delete any secrets already committed to history. Retain scanner checks,
review repository history privately, and rotate any exposed credentials.

The service validates JWT RS256 signatures using the issuer's trusted JWKS,
checks exact issuer and audience, required iat/exp with maximum one-hour
lifetime, user subject and scope. No real account, access token, client
secret or authorized folder ID is committed here.

## RFC 9728 and MCP

The resource document is available on loopback (when auth0 mode is explicitly
enabled) at:
- `/.well-known/oauth-protected-resource`
- `/.well-known/oauth-protected-resource/mcp`

Uncredentialed `/mcp` returns a 401 Bearer resource_metadata challenge.
Wrong subject or missing scope returns 403. Invalid signature, expiry,
issuer, audience or missing JWT returns 401. Disclosure is limited to
generic Unauthorized/Forbidden errors; the metadata itself does not
enumerate projects or users.

Authorization Code + PKCE S256 is performed by an external OAuth
authorization server and approved MCP client, NOT by this resource server.
The unit test computes and contrasts PKCE S256 challenge values; this
does not test Auth0's authorization endpoint, client registration,
redirect_uri, user consent, token exchange or real ChatGPT integration.

## Protection against premature exposure

- `--http` is restricted to 127.0.0.1 or ::1 even when auth0 mode is on.
- The Nginx example is intentionally disabled by default.
- The registered OAuth client, actual callback, S256 requirement, API grant,
  audience, user identity, real JWKS, proxy TLS, and single-project ownership
  all require independent acceptance before any public enablement.
- Do not copy the #75 draft's unprotected public-binding branch, general
  `npm install` deployment recipe, or rollback SHA into production.
- Preserve `npm ci --ignore-scripts`, the verified lock, the #76 bridge
  security fixes, Stage 10 request limits and read-only gates.

Do not enable public listeners, create accounts, change Auth0 settings,
register callbacks, change Nginx, publish releases, install plugins, or
write to Google Drive as part of this stage.

## External references

- RFC 9728: https://www.rfc-editor.org/rfc/rfc9728.html
- MCP authorization: https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization
- Auth0 client/application registration and JWT validation require
  tenant-specific operator review before any real integration.
