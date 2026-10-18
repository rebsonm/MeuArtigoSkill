# Meu Artigo — remaining go-live milestone matrix (2026-10-18)

This file separates **engineering work** from **human or external
authorizations**. The original master plan has 18 deliveries. Deliveries
16, 17 and 18 remain open. The ten items below are final acceptance
milestones, not ten new software modules.

## Verified baseline and limitations

- The sole integration decision is Draft PR #89 against `main`.
  Historical PR #87 and #88 must not be merged separately.
- Source Skill beta.9 is an unpublished candidate. The installed private
  ChatGPT package remains beta.8, embedding Skill beta.6. The last
  confirmed published Skill release is beta.6.
- Seven CI workflows passed at the earlier source SHA
  `ad340fc3a07b82c728e7152f8527ea8d95a6a0f4`.
  Any new commit must obtain its own checks and an independently reviewed
  final SHA. Do not reuse the earlier CI status.
- The current candidate added pre-bind reviewed-UI validation, loopback-only
  /healthz and /readyz, and explicit rejection of known E05 and private
  pilot app identifiers in production candidate packages. These features
  do not demonstrate real TLS/OAuth or Drive isolation.

## Ten remaining acceptance milestones

| ID | Original delivery | Required work | Evidence required to close | Blocker |
|---|---|---|---|---|
| R01 | 16 | Independent cumulative review of security, scientific boundaries, Auth0, F1–F9 and all relevant source changes | Independent reviewer sign-off for exact final SHA, HIGH findings resolved | Human independent reviewer |
| R02 | 17, pre-merge | Real ChatGPT E05 acceptance: ALPHA/BRAVO, ten screens, layout, focus, locale, teardown and effective CSP | Host-side reproducible report at pinned SHA and investigation of the CSP-disabled label | E05 approval and real host |
| R03 | 16 | Explicit SHA-specific authorization to merge only PR #89 into main | Maintainer decision and merge commit | Owner authorization |
| R04 | 16 to 17 | Post-merge CI, packaging and SHA-256 reproduction from main | Passed checks and archived checksum at resulting main SHA | R03 |
| R05 | 17 | Reviewed HTTPS production endpoint, Auth0 configuration, local health/ready, safe logs, secrets and rollback | Approved operational ingress and verified operation; /readyz 200 alone is insufficient | Production VPS authorization |
| R06 | 17 | Real OAuth/PKCE A/B with two independent accounts, 401/403 and revocation | Sanitized ChatGPT login and denial evidence | R05 and consent |
| R07 | 17 | Individual Drive A/B, F1–F9, journal/CAS, readback and cross-account denials | Separately authorized canonical workspace verification and isolation evidence | R06 and consent |
| R08 | 17 | Full create/resume article workflow, C.A.D.A. tasks, seven human scientific gates, recovery and privacy/rollback | Maintainer acceptance using consented synthetic projects; no automatic scientific approval | R07 |
| R09 | 18 | Verified production app packaging, private installation and controlled researcher pilot | Prior/current release IDs, first-run checks and approved beta feedback | R08 and separate Plugin authorization |
| R10 | 18 | With MCP directory submission, review, public approval and external installation | Public review approval, listing and independent researcher installation | R09 and separate publication authorization |

**Remaining: ten acceptance milestones**. Automated source checks, negative
tests, static review, release preparation and documentation can proceed without
production access. Synthetic CI cannot close the real-host conditions in
R02/R05/R06/R07.

## Documentary evidence checker

Run from a checked-out source repository:

```sh
python integrations/mcp-apps/scripts/release_gate.py --source-sha "$(git rev-parse HEAD)"
```

The report defaults to all gates not verified. Optional `--records`
accepts a sanitized local JSON document. Even if ten records say PASS,
the tool must never authorize a merge, deployment, installation or
publication. Each record requires an exact source commit, an externally
held evidence reference and the expected observer role. This only checks
the shape, not the truth or source of evidence.

Example of one **fictional**, unapproved record:

```json
{
  "R01": {
    "status": "PASS",
    "source_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "evidence_ref": "EVID-REVIEW-0001",
    "observer_role": "INDEPENDENT_REVIEWER"
  }
}
```

Stale SHAs, missing evidence, extra fields, unexpected roles, credentials,
private URLs, source documents or personal identifiers must not enter the
public release record. The checker exposes only gate codes and statuses.

## Current decision boundary

- `GO_SOURCE_TESTS`: per-SHA CI results only.
- `GO_INDEPENDENT_REVIEW`: not verified.
- `GO_REAL_E05_CSP`: not verified.
- `GO_MERGE`: NO-GO without SHA-specific approval.
- `GO_REAL_OAUTH_AB`, `GO_DRIVE_AB`: not verified.
- `GO_PRIVATE_PLUGIN`, `GO_PUBLIC`: NO-GO.

No merge, production deployment, Auth0/Drive change, Plugin installation
or public publication is authorized by this matrix.
