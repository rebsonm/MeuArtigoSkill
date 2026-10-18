# MCP OAuth transport: ChatGPT-host Drive architecture

This candidate is **not deployed** or connected to a real ChatGPT account.
The MCP service is stateless for research: it never accesses Google Drive,
projects, manuscripts, tokens or research metadata. Each researcher connects
their own Google Drive directly in their own ChatGPT session. The Skill's
methodological guidance and document operations happen host-side.

## Purpose of Auth0

Auth0, when used, controls access to this **generic MCP UI and method
information only**. It is not Google OAuth, provides no Drive permissions,
and does not authorize access to any user's research files.

`MEU_ARTIGO_AUTH_MODE=auth0` enables JWT verification. Configure:

- `MEU_ARTIGO_AUTH_ISSUER`: exact HTTPS Auth0 issuer, trailing slash.
- `MEU_ARTIGO_AUTH_RESOURCE=https://mcp.allflux.com.br/mcp`: exact audience.
- `MEU_ARTIGO_MCP_MULTIUSER=YES` for separately authenticated people
  using the **same content-free MCP**. No `MEU_ARTIGO_PILOT_SUB` in this mode.
- For a legacy one-user test only, omit multiuser and set an exact
  allowlisted `MEU_ARTIGO_PILOT_SUB`.
- Scope `mcp:read`, RS256 via trusted JWKS, bounded expiration and
  required issued-at checks. Anonymous or invalid tokens are denied.

The service makes no user-specific data request. It deliberately does not
interpret a ChatGPT Drive connector identity, email or token.

## Transport boundaries

- Only `127.0.0.1` / `::1` listener is allowed.
- RFC 9728 protected-resource metadata endpoints:
  `/.well-known/oauth-protected-resource` and
  `/.well-known/oauth-protected-resource/mcp`.
- Unauthenticated `/mcp` returns a Bearer challenge.
- Wrong issuer/audience/signature/expiry gives HTTP 401.
- Missing scope or blocked user subject gives HTTP 403.
- Origin, JSON body-size, content-type and token-header guards apply.
- OAuth Authorization Code + PKCE and real callback registration are handled
  by the identity provider and approved ChatGPT OAuth client, not by this
  MCP resource server.

The server has **no `/google/oauth/callback`**, never asks Google for a
Drive token and never persists refresh grants. Any mention of this legacy
path in older review notes describes a withdrawn design, not the candidate.

## Public deployment restrictions

The example Nginx configuration intentionally returns 404 and includes no
active `proxy_pass`. Do not open the MCP or deploy a proxy to production
without reviewing actual Auth0 application registration, PKCE, redirect,
client permissions, TLS, request limits, safe logs and ChatGPT host access.

There is no need for a Google Cloud OAuth client or Drive API credential in
the MCP. Each researcher's Google Drive connection is established privately
by them **inside ChatGPT** according to connector availability.

Passing offline tests does not prove live ChatGPT OAuth, installed Plugin
version, MCP Apps UI rendering, individual Drive permissions, or scientific
validity. All remain independent acceptance gates.

## Local health and static-UI readiness

The review candidate exposes `GET /healthz` and `GET /readyz` only on the
loopback listener, after verifying that the reviewed UI can be assembled at
startup. The responses reveal only `{"status":"ok"}`, not identity, tokens,
configuration, user files, payloads or telemetry. All other non-MCP operational
URLs return 404; methods other than GET are rejected for probes.

An external reverse proxy must NOT forward these paths by default. Use
loopback service supervision instead. In particular, HTTP readiness is not a
proof of real issuer availability, ChatGPT OAuth/PKCE, Drive authorization,
complete end-to-end operation or effective iframe CSP. No deployment performed.
