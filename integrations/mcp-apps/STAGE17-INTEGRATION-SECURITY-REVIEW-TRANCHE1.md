# Stage 17 — consolidated PR #87 security review, tranche 1

Status: **targeted source/security review and one defensive correction**.
This document does not represent a second independent security reviewer,
a penetration test, a full 151-file line-by-line audit, or authorization for
merge, VPS deployment, installed Plugin replacement or researcher onboarding.

## Scope and frozen sources

- Baseline: `main` at
  `5c7bf4ff599d73a660bb709616a689140b2edbe7`.
- Reviewed aggregate PR #87 HEAD:
  `0eab6e00da30db858bdb497f86262b05175a527d`.
- This new security branch adds only the defensive F5 leaf-name guard,
  associated negative tests, and this report. New HEAD must be verified
  by its own GitHub workflows before treating it as accepted.
- Aggregate changed-file inventory including this branch at its second
  commit: 151 files, 244 commits ahead of main, 0 behind, comprising
  44 MCP-related paths, 43 Drive/security paths, 32 scientific-related
  paths, and 32 other paths under a first-match classification. Counts
  are for **triage**, not attestation.

## Confirmed findings

### S17-SEC-01: low-risk defense-in-depth gap at the F5 Drive POST boundary

`scripts/drive_f5_operator.py::api_create_folder_once` validates the
parent Drive ID but previously checked the leaf name only for being a
nonempty string with no forward slash. It did not independently enforce
the canonical planner's `delivery.safe_relative` rules before issuing
a Google Drive POST. This helper is not directly exposed on the MCP,
and its approved caller already validates the plan/root, so the
review does not assert a remote exploit.

**Correction in isolated branch:** reuse the canonical single-leaf
validation and reject ASCII control and DEL characters before calling
`sender(..., method="POST")`. The code keeps the same sanitized
`INVALID_FOLDER_NAME` error on bad leaves, and existing authorized
leaf names remain valid.

**New tests:** `tests/test_drive_f5_leaf_name_guard.py` checks (1)
malicious/dot/backslash/control names cause zero simulated external
requests, (2) nonstring names cause zero requests, (3) a valid single
leaf yields exactly one correctly scoped synthetic POST, and (4) an
invalid parent denies before POST. No real tokens or Drive writes.

**Acceptance:** require release-audit Python discovery and the
existing F5–F9 suite to pass at the final SHA. The new tests should
also appear by name in the CI logs.

## Source boundary analysis (targeted, not an end-to-end certification)

| Boundary | Direct source evidence | Review decision |
| --- | --- | --- |
| Auth0 issuer/audience/JWKS | `integrations/mcp-apps/auth0.mjs` validates HTTPS Auth0 issuer, exact configured audience and RS256 JWT, `exp`/`iat`, scope `mcp:read`. Pilot allowlist and generic multiuser configuration cannot coexist | Mechanism present; **real configured tenant and ChatGPT login not tested** |
| HTTP front door | `integrations/mcp-apps/server.mjs` binds loopback, requires bearer or Auth0 token, checks request origin when supplied, enforces body length/JSON content type, and registers a stateless MCP transport | Source checks present; **TLS ingress/reverse proxy and public threat-model review still pending** |
| Research-data boundary | MCP `noResearchAccess` rejects Drive/local project credential environment settings; `normalizeHostSnapshot` allows only a bounded display projection, refuses obvious credentials/URLs and returns no canonical-write/sync/auto-science claims | Structural minimization present; **cannot prove arbitrary text free of personal/confidential information** |
| F5 non-idempotent create | Root identity check, provider-backed complete parent scan, durable journal push/readback, signed F7 receipt and external F8 CAS before a create, fresh post-create reconciliation; helper now validates leaf before POST | Source-control chain present; **real provider/OAuth/IAM/CAS state not independently exercised** |
| F7–F9 head | F7 HMAC archive verifies receipt chain, F8 checks independent trusted head, F9 DynamoDB adapter uses a conditional `UpdateItem` with consistent readback | Offline logic reviewed partially; **production cloud provisioning, authority and concurrency remain unverified** |
| E05 CSP | Offline resource test verifies empty domain lists and restrictive HTML CSP; user screenshot showed `CSP desativada` | **Host enforcement unknown; public publication NO-GO** |
| Seven scientific gates | Source assertions disallow automatic scientific approval in MCP and pass the old strict policy + report-output tests | **Human scientific review still separate** |

## Explicit exclusions and residual risks

1. No real Google Drive content, OAuth credentials or Auth0 secrets have been
   consulted. The previous E05 acceptance used only ALPHA/BRAVO fiction.
2. This review is NOT a proof that every changed file has been audited;
   the 151-file aggregate diff still requires an independent human reviewer,
   including changes stacked after #74/#75 and older scientific #65/#66
   differences. No duplicate merges or silent PR closures.
3. Real ChatGPT-to-Auth0 login, two independent users' individual Drive
   permissions, endpoint response headers, CSP sandbox enforcement, CSRF
   behavior and private-to-public Plugin packaging remain release blockers.
4. `VERSION` in candidate source is beta.6 while the installed personal
   Plugin manifest was previously observed beta.8; do not downgrade.
5. The F5 hardened helper does not enable real creation. Its top-level CLI
   remains constrained to explicitly authorized synthetic Drive roots
   and independent F8 trusted-head configuration.

## Decision

- `SEC_TRANCHE1_SOURCE_REVIEW = COMPLETE_WITH_LIMITATIONS`.
- `F5_DIRECT_POST_LEAF_GUARD = CORRECTED_PENDING_CI` until checks complete.
- `GO_SOURCE_TESTS` depends on successful CI at the new final SHA.
- `GO_MERGE = NO-GO`, `GO_REAL_DRIVE = NO-GO`,
  `GO_PLUGIN_PRIVATE_UPDATE = NO-GO`, `GO_PUBLIC = NO-GO` until
  remaining gates and explicit human approvals are satisfied.

Do not treat GitHub Actions success alone as independent code review or
scientific approval.
