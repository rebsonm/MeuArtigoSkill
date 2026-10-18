# Meu Artigo — transient dashboard, researcher-owned Google Drive

## Data ownership and flow

Every researcher connects **their own** Google Drive to ChatGPT. The existing
Meu Artigo Skill creates and maintains its spreadsheets, gates, C.A.D.A.
registers, journal and research files in that authorized Drive. **Those
files stay there**; the MCP has no Google API client, refresh tokens,
folder search, filesystem project reader or Drive write capability.

The assistant uses the current user's ChatGPT Drive connector to read the
**existing canonical registers**, and prepares a small `MEU_ARTIGO_SITE_V1`
summary for the `meu_artigo_painel` MCP tool. The MCP **does receive and
process those explicitly selected display fields** temporarily to render
its UI, but it does not fetch source files or persist the payload.
A new request replaces the previous display; a missing or invalid
payload resets the UI. This is **not** zero knowledge: the MCP operator
could in principle observe request contents in process memory or network
infrastructure, so only approved minimum display fields should be sent.

```text
Researcher A -> ChatGPT(A) -> A's Drive connector -> A's original registers
                         -> bounded, per-call UI projection -> shared MCP
Researcher B -> ChatGPT(B) -> B's Drive connector -> B's original registers
                         -> bounded, per-call UI projection -> shared MCP
```

The MCP **never uses A's Google credential for B**, nor anyone else's,
and keeps no server-side tenant project mapping or remembered snapshot.

## Tool and renderer contract

`meu_artigo_painel(locale?,mode?,snapshot?)` accepts a projection created
in the current ChatGPT conversation. It must use **only** values actually
read from the currently connected Drive; the assistant must not invent
gate approvals, task completion or provenance. Omission leaves the
display neutral `HOST_NOT_CONNECTED`.

`snapshot` has this exact bounded shape (no extra keys):

```json
{
  "schema":"MEU_ARTIGO_SITE_V1",
  "active_route":"qualitative documentary",
  "registered_gate_total":7,
  "gate_view_partial":false,
  "tasks":[{"id":"TASK-01","task":"Review literature","execution_owner":"Researcher","deadline":null}],
  "gates":[{"id":"GATE-0001","approval_documented":false}],
  "next_action":{"code":"REVIEW","explanation":"Review search criteria","responsible":"Researcher"}
}
```

The example is fictional. It does not approve a scientific gate or claim
Drive sync. Tasks are capped at 200; gates at seven. The tool performs
strict field/type/size validation, recomputes documented gate counts,
preserves partial-state warnings and only accepts the restrictive
status/code-only diagnostic sidecar when supplied. It rejects document
bodies, references, quotes, file IDs, URLs, tokens, extra attributes,
bulk collections and invalid scientific approval claims. No cross-user
cache, database or log of project contents is part of the implementation.

The server returns `structuredContent.site` with
`kind=HOST_AUTHORIZED_SNAPSHOT` only for valid input. The MCP Apps
bridge forwards this view **in memory** to the existing ten-screen HTML
dashboard; it does not push raw PDFs, CSV files or entire articles to
the app. Host data origin and scientific validity are not independently
verified by the MCP. Status labels must distinguish display data from
verified source evidence.

## Safety tests

Run from `integrations/mcp-apps`:

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm run build
npm run test:host-boundary
npm run test:host-projection
npm run test:stage15
npm run test:oauth
npm run test:oauth-http
```

`test:host-projection` covers alternating fictional A/B snapshots,
a subsequent empty call, no memory reuse, strict whitelist denials,
seven-gate preservation and fail-closed metadata. This suite uses no
external Google accounts or Drive API calls. It does not prove that
ChatGPT selected the correct user's connected account. The product
still requires real host-side two-account acceptance and human review.

For HTTP deployment, Node remains bound to 127.0.0.1:8085 behind a
separately reviewed HTTPS reverse proxy. Multi-user Auth0 can
authenticate access to this generic display service, but it is **not**
permission to read Google Drive; the ChatGPT connector handles that.

**No deployment, external OAuth changes, Google writes, Plugin update,
merge or release has been authorized by these code changes.**

## Operational liveness and readiness (source-only)

When started in `--http` mode, the process validates the reviewed local
HTML/bridge UI **before** binding the loopback socket. A missing or malformed
UI aborts startup, instead of reporting readiness while serving an unusable
interface. `GET /healthz` and `GET /readyz` both return only
`{"status":"ok"}` with `Cache-Control: no-store` and `nosniff`, once this
preflight passes. There are no user IDs, account details, software version,
tokens, metrics, debug routes, cross-origin permissions or research metadata.

The responses do **not** prove that Auth0, Google Drive, HTTPS, ChatGPT CSP,
the user account or a remote reverse proxy is functioning. They are for
loopback/local process supervision only. Reverse-proxy exposure requires a
separate review; the example external Nginx host still denies all requests.
`npm run test:operational` exercises bearer and synthetic Auth0 modes.

## Network resource limits and local-path projection guard

The HTTP listener is loopback only, with 16 KiB maximum request headers,
10-second header timeout, 15-second request and idle timeouts, 5-second
keepalive timeout, 64 concurrent sockets, a 64-request-per-socket ceiling
and a maximum of 64 header fields. Reverse proxy quotas and TLS controls
remain independently required; these application limits do not demonstrate
DoS resilience, OAuth correctness or real ChatGPT connectivity.

Host-supplied dashboard text rejects absolute Windows drive paths (any
folder after a drive letter), UNC shares, Unix home/root paths, URLs and
obvious credentials before returning structured results. Synthetic
projection tests cover ordinary Windows paths, arbitrary drive folders,
UNC shares and fields outside task descriptions. The filter is heuristic,
not a guarantee that user-supplied display text is free of personal data.
