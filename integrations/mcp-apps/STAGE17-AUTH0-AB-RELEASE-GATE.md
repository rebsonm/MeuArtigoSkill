# Stage 17 — OAuth/Auth0 and two-user ChatGPT acceptance gate

**Status: document-and-source security candidate only; no live acceptance.**
This checklist does not authorize access to a user's Drive or changing the
private or public Plugin registration, Auth0 tenant, VPS, DNS or main branch.

## Source boundary: what the MCP can and cannot do

- Auth0 is the **OAuth resource server** access boundary for a generic
  display-only `meu_artigo_painel` tool. `MEU_ARTIGO_AUTH_RESOURCE`
  must exactly name the HTTPS `/mcp` audience; issuer is one exact
  Auth0 tenant, signatures are RS256 through that tenant's JWKS, and
  the short-lived JWT must include the `mcp:read` scope.
- For a private pilot, use the allowlisted exact Google Auth0 subject.
  For an approved multiuser generic MCP, `MEU_ARTIGO_MCP_MULTIUSER=YES`
  requires no pilot subject allowlist. This **does not** grant users
  Google Drive permissions or authorize reading another user's files.
- Each researcher connects Google Drive **independently through ChatGPT**.
  The MCP must never be supplied tokens, original research documents,
  URLs, file identifiers, full claims, or free-form manuscripts.
  A minimal redacted on-screen projection is the maximum permissible
  data passed into this MCP.
- The current candidate binds only loopback and has no approved public
  reverse proxy. Changing that is a **separate operational decision**.
- A browser `Origin` is an exact HTTPS origin tuple: no `http:`,
  opaque `null`, credentials, wildcard, path/query/fragment or
  noncanonical `https://host/` form. The optional
  `MEU_ARTIGO_ALLOWED_ORIGIN` may be left absent for machine-to-machine
  transports; when set it must match the request exactly. Authorization
  bearer/JWT remains mandatory even for a matching origin.

## Negative and positive source tests in this candidate

`npm run test:auth-origin` is synthetic and may use only local loopback.
It verifies exact Origin parser behavior; fail-before-bind for invalid
configuration in both bearer and Auth0 modes; cross-origin request 403
with synthetic bearer; permitted origin or server-to-server absence
of an Origin not confused with authentication. This last allowance
is **not** a CORS bypass, a CSRF guarantee or an OAuth login test.

Existing synthetic contracts:
- `npm run test:oauth`: RS256 signature, issuer, audience, expiry,
  `iat`, scope, subject allowlist, invalid signer and PKCE *simulator*.
- `npm run test:oauth-http`: RFC 9728 metadata and invalid-token
  HTTP denials against a local server, no valid human Auth0 session.
- `npm run test:host-connector-boundary`: in-memory JWT checks for
  two fictional Auth0 subjects, generic MCP resource access and no
  local Drive lookup.
- `npm run test:host-projection`: independent synthetic A/B payloads,
  no cached prior researcher data, no writes, no auto-science flags.

**Passing these is evidence only of synthetic code behavior**.
The real ChatGPT OAuth authorization-code + PKCE exchange, Auth0
consent/redirect, Google Drive connector permissions and end-to-end
A/B isolation remain untested.

## Minimum authorized real A/B checklist (separate execution)

Preconditions: independent explicit authorization by **both**
researchers, separate private test workspaces containing entirely
fictional documents, externally approved HTTPS endpoint/identity
setup, verified CSP host mode, and a reviewed/approved Plugin build.

1. Login to distinct Auth0 accounts A and B using two separate
   ChatGPT profiles or isolated browser sessions. Only researcher-owned
   Google Drive connections may be attached to each profile.
2. Check the official ChatGPT OAuth redirect/consent path and required
   `mcp:read` permission. Validate a successful MCP tool call for
   each user without recording raw bearer tokens, headers, cookies,
   authorization codes or their contents.
3. In account A, query only its synthetic `TEST_A_ONLY` record.
   In account B, query only its synthetic `TEST_B_ONLY` record.
   Reinvoke B after A without any projected A content; re-open A
   with an empty payload and verify no cached B state.
4. Attempt account A to retrieve B's fictional test record via the
   **individual Google Drive connection**, not via a shared/unrestricted
   connector. Expected result: no unauthorized file results.
   Repeat symmetrically for B to A. If a Drive document is legitimately
   shared, record that permission separately; such a read is not evidence
   of isolation failure, nor proof of default isolation.
5. Verify unauthorized/expired token gets 401 with no data; a valid
   but nonpermitted pilot subject or insufficient scope gets 403,
   without disclosing the expected subject, token or hidden files.
6. Test ten UI screens, switch A/B, stale state, keyboard focus and
   locale; capture sanitized results. Record that all scientific gates
   remain human-controlled; no silent approvals or Drive sync claims.
7. Check effective iframe CSP and browser console **violation counts/
   categories** only. If `CSP desativada` is still displayed, investigate
   which host policy the badge describes before public release.

### Minimum evidence manifest

Only record operator-verified facts in an approved internal repository
note; never put JWTs, credentials, private URLs, screenshots with names
or source text in public GitHub:
```json
{
  "test_environment": "independent authorized non-production",
  "sha_reviewed": "FILL_WITH_ACTUAL_DEPLOYED_SHA",
  "auth0_a_valid_scope": "PASS_OR_FAIL_NOT_TESTED",
  "auth0_b_valid_scope": "PASS_OR_FAIL_NOT_TESTED",
  "a_cannot_read_b": "PASS_OR_FAIL_NOT_TESTED",
  "b_cannot_read_a": "PASS_OR_FAIL_NOT_TESTED",
  "expired_token_401": "PASS_OR_FAIL_NOT_TESTED",
  "insufficient_scope_403": "PASS_OR_FAIL_NOT_TESTED",
  "no_cross_session_cache": "PASS_OR_FAIL_NOT_TESTED",
  "effective_host_csp": "PASS_OR_FAIL_NOT_TESTED",
  "observer_role": "AUTHORIZED_TEST_OPERATOR",
  "approval_for_public_release": false
}
```

## Gate decisions at source PR submission

| Gate | Decision |
| --- | --- |
| JWT signature, issuer, scope and local A/B tests | Previously passed in synthetic CI |
| HTTP Origin configuration hardening | Pending new HEAD CI |
| Real ChatGPT Auth0 OAuth login A/B | NOT_TESTED |
| Independent Google Drive access denial A/B | NOT_TESTED |
| Effective iframe CSP and verified widget domain | NOT_VERIFIED |
| Public / installed Plugin update / production deploy | NO-GO |
| Merge to main | NO-GO until independent cumulative review and explicit authorization |

Do not transform a local mock, green CodeQL run, human visual feedback
on an E05 synthetic tunnel, or a security checklist into evidence of
real end-user OAuth acceptance.
