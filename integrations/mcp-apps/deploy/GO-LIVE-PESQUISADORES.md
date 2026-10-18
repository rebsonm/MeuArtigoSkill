# Meu Artigo — production go-live for independently connected researchers

Status: **SOURCE-ONLY / NOT DEPLOYED / NO PUBLICATION AUTHORIZATION**.
This is a single operator runbook, not evidence that any command was executed.
The goal is a stable version that can receive subsequent updates, without
mistaking synthetic E05 fixtures for a multi-researcher production service.

## Mandatory prerequisites

1. Freeze the reviewed integration SHA and reconcile the Skill/Plugin/MCP
   version. Merge to `main` requires explicit SHA-specific maintainer
   approval; PR #91 is an incremental PR stacked on PR #89.
2. Verify DNS ownership, a real production TLS certificate and private key,
   the intended public endpoint and independent least-privilege service
   identity. Keep authenticated request details and credentials out of logs.
3. Verify the exact HTTPS Auth0 issuer, OAuth/OIDC discovery and
   `code_challenge_methods_supported` including `S256`.
   Select an actual supported client-registration approach: CIMD, DCR or
   provided client. Allowlist the exact ChatGPT callback displayed by the
   portal. Require Authorization Code + PKCE, `mcp:read`, and an audience
   exactly equal to `https://<approved-host>/mcp`.
   Never put a client secret, bearer, JWT or OAuth code into Git or chat.
4. Resolve **effective host iframe CSP = NOT_OBSERVED** with real host
   evidence. A declared CSP and an absent warning badge are not proof.
5. Obtain express consent from two independent ChatGPT account owners
   before real A/B tests. Only use researcher-owned fictional Drive records.
   The shared MCP is a transient display service, not a Drive client.

## Running VPS baseline — 2026-10-18 (read-only operator evidence)

Operator observed on the existing VPS, with no production changes:

- Nginx `active`, `meu-artigo-mcp.service` `active`, and E05
  `meu-artigo-e05-tunnel.service` `active` as a separate service.
- Existing MCP Node listener on `127.0.0.1:8085`; `/mcp` returned
  `401` without credentials, while `/readyz` and `/healthz` returned
  `404`. Do **not** treat the `401` as proof of real OAuth acceptance.
- Existing working tree: `/opt/meu-artigo/repo`; the active service uses
  `/opt/meu-artigo/repo/integrations/mcp-apps`. The confirmed Git SHA
  with explicit safe-directory handling is
  `cdd3affb902028753b9c66b83c2ef5e37f9e1700`.
- Candidate source is PR #89 SHA
  `27659d6092a6e2aa68919df6758c20cb8f50022d` plus stacked
  PR #91 SHA `32625a9c74495256bca76515827c9f56fa9a5d74`.
  GitHub comparison from existing VPS SHA to PR #91 returned
  `status=diverged`, `ahead_by=292`, `behind_by=180`, and merge
  base `441b452bacfc602ef09aeac1575aa6d8e390c561`.
  These are repository ancestry metrics and **NOT** an acceptable
  in-place migration or a completed source reconciliation.
- On this VPS `getent ahostsv4 mcp.allflux.com.br` failed, and
  external MCP curl failed name resolution. Confirm authoritative DNS
  ownership and records separately; do not assume the hostname works.

**Non-destructive migration strategy:** Do not pull, force checkout,
hard reset, overlay, delete or restart the active
`/opt/meu-artigo/repo`, and never touch the E05 tunnel. Review
the clean/dirty state and ownership of the active checkout, then stage
a separate immutable reviewed source snapshot under a distinct
least-privilege service account and separate working directory.
Install dependencies in that *staging* tree with lockfile integrity,
run source security tests, and choose a fresh loopback port only after
port inspection. Validate TLS, Auth0, endpoints, and rollback without
pointing the existing public route at staging. Switch ingress only
after maintainer-approved deployment, real two-user consent and
documented gates; retain the old service for immediate fallback.
No credential, API secret or researcher document should move from
the previous service.

These observations are about the **existing installation**, not proof
that PR #91 was deployed or that the publication requirements passed.

## Offline source-only preflight

Run from the reviewed repository checkout:

```bash
python integrations/mcp-apps/scripts/public_ingress_preflight.py \
  --config integrations/mcp-apps/deploy/nginx-auth0-production.conf.template
python -m unittest discover -s integrations/mcp-apps/tests \
  -p test_public_ingress_preflight.py -v
```

`SOURCE_TEMPLATE_PASS` does not verify certificates, OAuth or production.
The older `nginx-auth0.conf.example` deliberately returns 404, and must
not be represented as an activated proxy.

## Authorized operations window (VPS operator only)

**Baseline first.** Inspect the real hostname, DNS, certificates, active
services, current Git SHA, filesystems and listened ports. Preserve the
existing E05/stage17 services, directories and secrets; do not restart or
overwrite them. Prepare a rollback snapshot before doing anything.

**MCP loopback.** Use an isolated reviewed runtime checkout and a dedicated
restricted service user. Start the reviewed HTTP MCP server only on
`127.0.0.1` with the separately agreed local port (the proxy template
expects 8085). Set protected environment configuration:
`MEU_ARTIGO_AUTH_MODE=auth0`,
`MEU_ARTIGO_AUTH_ISSUER=<exact production HTTPS issuer>`,
`MEU_ARTIGO_AUTH_RESOURCE=https://<approved-host>/mcp`,
`MEU_ARTIGO_MCP_MULTIUSER=YES`; leave `MEU_ARTIGO_PILOT_SUB` unset.
Set `MEU_ARTIGO_ALLOWED_ORIGIN` only to an exact observed legitimate
HTTPS Origin when needed; never use `*`, `null` or insecure HTTP.
Only store runtime configuration in access-controlled local settings.
Do not supply Google tokens, file IDs or research data to the MCP.
Require a local `/readyz` pass before examining public ingress.

**Nginx candidate.** Copy the reviewed
`nginx-auth0-production.conf.template` to a temporary configuration
outside the active enabled-sites directory. Replace the exact intended
hostname and the two certificate/key placeholders with verified paths.
Only `/mcp`, the two OAuth RFC 9728 metadata paths and the optional
OpenAI domain-challenge path may be externally reachable. Domain
verification must use the exact portal-issued challenge token; never
invent one or commit it. Run the following checks before any activation:

```bash
python integrations/mcp-apps/scripts/public_ingress_preflight.py \
  --config /PATH/TO/RENDERED-CONFIG.conf \
  --expected-host mcp.allflux.com.br --require-cert-files
sudo nginx -t
```

`mcp.allflux.com.br` is the intended host from the project sources,
**not an observed live endpoint**. Substitute the verified hostname if
different. The source check rejects missing certificate files and
world/group-readable private keys. It does not cryptographically verify
TLS, run OAuth/PKCE or attest to iframe CSP. Activate and reload the
Nginx site **only after explicit maintainer authorization** and a known
good rollback plan. Do not expose private health endpoints.

## Minimum real acceptance tests

Record only non-sensitive pass/fail evidence tied to the SHA, never
bearers, cookies, private headers or unpublished research material.

| Probe | Expected evidence |
| --- | --- |
| GET `https://<host>/.well-known/oauth-protected-resource` | 200 JSON with exact HTTPS resource, issuer and scopes |
| GET `https://<host>/.well-known/oauth-protected-resource/mcp` | 200 consistent RFC 9728 metadata |
| POST `https://<host>/mcp` without token | 401 with Bearer resource challenge |
| Expired, wrong-issuer or wrong-audience token | 401 and no research data |
| Valid token with insufficient scope | 403 |
| External GET `/readyz` and `/healthz` | 404; 200 only on loopback |
| Unexpected paths | 404 and no upstream forwarding |
| Two independent ChatGPT/IdP users | Real PKCE S256, audience, issuer and scope validated |
| Two independently connected Drive accounts | No A/B crossover, no shared cache; fictional records only |
| Real host iframe and UI | Effective CSP and browser behavior directly observed |

The MCP never independently proves article quality, source support or
scientific gate completion. Scientific judgments remain human-controlled.
Any security or identity failure is a stop condition.

## Rollback and subsequent updates

On failure, disable **only the new production proxy route**, revalidate
the saved previous Nginx configuration using `nginx -t` and reload it.
Do not disturb E05, stage17, Drive projects or unrelated services.
Never use recursive permission changes, `git reset --hard`, wildcard
deletions or an anonymous emergency endpoint. Revoke exposed credentials
through the identity provider's administration UI. The MCP itself stores
no canonical research records. Record the SHA, time, neutral error category
and operator decision.

Researchers on separate ChatGPT accounts need a publicly discoverable
With MCP plugin, or their own eligible individual remote MCP configuration.
Directory publication requires verified publisher identity, HTTPS
website/support/privacy/terms, real demonstration evidence, exactly five
positive and three negative cases, domain challenge, current tool scan,
and external OpenAI approval. The source beta.9 PRs are not a v1.0.0
release. Eligible remote server updates may be rescanned after deployment;
changes to packaged Skill or metadata require an updated plugin ZIP.
Treat the published remote URL as a long-lived identifier.

## Decisions reserved for the maintainer

- Accept or reject documented R01 risks RA-01–RA-06 and verify the real
  R02 CSP evidence before any SHA-specific merge authorization.
- Approve the actual VPS/Nginx/Auth0 changes and two consenting users
  only after technical prerequisites have passed.
- Approve submission and eventual publication separately from testing;
  a successful source test never approves public release.

Official references:
- https://developers.openai.com/plugins/build/auth
- https://developers.openai.com/plugins/build/mcp-server
- https://developers.openai.com/plugins/deploy/submission
