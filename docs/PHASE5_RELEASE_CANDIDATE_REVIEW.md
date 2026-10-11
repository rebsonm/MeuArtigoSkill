# Phase 5/5 — Corrective software candidate and review handoff

**Decision status: main source integration explicitly authorized by the owner on 2026-10-11. No release, hosted MCP deployment or installed-plugin scientific-code update authorized.**

This report consolidates the post-homologation maintenance of Meu Artigo. It is based on the existing branch's engineering commits, GitHub Actions observations, earlier authorized sanitized Gate 4 audit, and the owner's 12 explicitly illustrative design references. It does not recreate or certify any scientific evidence or private Drive project. The real research Gate 4 remains pending human work.

## Three independent version identities

| Distribution | Version | Status |
|---|---|---|
| Public GitHub Skill release | 0.9.0-beta.2 | Historical published tag and archives untouched |
| Private ChatGPT plugin | 0.9.0-beta.3 | Prior icon-only metadata update, separately managed; no scientific-code update in this maintenance |
| Maintained source candidate | 0.9.0-beta.4 | Source prepared in the corrective branch for owner-authorized main integration; **no public release**, review-only Skill and plugin ZIPs |

VERSION, README, CITATION.cff and CHANGELOG identify the source candidate without asserting a new release date. The source-candidate notes explicitly state NOT PUBLISHED, making the production release metadata check fail closed. Only a later owner-authorized release process should set the actual date and published download URL.

## Post-homologation engineering corrections

| Incident family | Engineering outcome | Remaining limitation |
|---|---|---|
| INC-001 — optional XLSX generator | CLI preflight, lazy import, no fake XLSX on missing artifact_tool | XLSX generation needs a compatible runtime |
| INC-002 — bibliographic import | Reject bad schemas, malformed or unidentified rows; report quarantine; preserve IDs; no automatic fuzzy exclusion | Actual bibliography and decisions need real independent checking |
| INC-006 — distribution identity | Provenance receipt, source commit when verifiable, historical icon and consistent package version | GitHub archive does not identify the currently installed plugin release |
| INC-007 / Gate4-005 — trace/log parsing | Multiple IDs, PARTIAL and NOT_EXECUTED state handling, source verification integrity | Historical records are not rewritten or upgraded to verified |
| PR #22 correction set | Source integrity/report checks, editorial alerts, objective block conditions, selective merge with modern beta.2 code | Providers and independently reviewed articles not verified by synthetic tests |
| Visual migration | Read-only MCP stdio/HTTP prototype with nine modules, first-use and next-action flows, mobile dark mode, original SVG | Hosted HTTPS MCP, actual Drive adapter and on-host visual acceptance pending |

Provider quota/entitlement incidents (Consensus, Scite, Semantic Scholar rate limits and Firecrawl credits) are **external operational conditions**, not repaired by repository tests. Unavailable full texts, inconsistent external metadata, 69 possible fuzzy pairs and unresolved human triage of the remaining corpus must not be auto-resolved. No new scientific approval, protocol change, synthetic article finding or external API execution is implied by this maintenance.

## Owner's UX reference: implementation versus acceptance

The twelve approved conceptual screens are now mapped to implementation states. Functional source paths include overview, next action, seven-stage scientific map, C.A.D.A. kanban, searches, L/I/P, gates, timeline, editorial readiness, synchronization, first use and dark mobile.

**Engineering compilation/contract PASS does not mean screenshot visual PARITY PASS.** Full screenshot comparison against the twelve owner examples, keyboard/screen-reader user tests and actual ChatGPT-host rendering remain pending. See [Phase 4 audit](PHASE4_UX_REGRESSION_AND_ACCEPTANCE.md) and [original reference](UX_APPROVED_REFERENCE_12_SCREENS.md).

## Scientific, privacy and storage invariants retained

1. Seven scientific gates and researcher-owned interpretation, choices, judgments and human review remain outside automatic UI updates.
2. Administrative C.A.D.A. activity completion cannot count as a scientific approval or validation.
3. [L], [I], [P] source/proposal distinctions, evidence provenance, honest external source checking and claims/counterevidence traceability are retained.
4. No fabricated database access, actual full-text availability, real Drive sync, journal compliance or external publication success.
5. A canonical project remains Drive-first; local read-only mirrors are not canonical remote evidence unless authorized and reconciled.
6. No protected full texts, unreleased research corpus, secrets, OAuth credentials, .env files or personal Drive exports in the public code or review packages.
7. No user submission, disclosure waiver, Gate 4/7 approval, public release, plugin update or change to existing project records is established by these tests. Main integration was subsequently authorized expressly by the owner; it does not validate research.

## Review candidate artifacts and verification

The maintenance CI builds:
- MeuArtigoSkill-v0.9.0-beta.4.zip: deterministic Skill ZIP, license/NOTICE, external SHA256SUMS.txt and BUNDLE_BUILD_RECEIPT.json.
- MeuArtigoPlugin-v0.9.0-beta.4-candidate.zip: a separate **skills-only** private plugin archive with root and Codex manifests, original SVG and the full namespaced Skill; it does **not** contain live MCP bindings or an automatically connected dashboard.
- CANDIDATE_VERIFICATION.json, CANDIDATE_SHA256SUMS.txt, PLUGIN_BUILD_RECEIPT.json, NOT_PUBLISHED_CHECK.txt.

All archives are generated by GitHub Actions, published only as **temporary Actions artifacts for review**, never as GitHub release assets. Artifact expiry can apply. GitHub Actions run-level artifact links, the exact SHA-256 digests and the matching source commit should be copied into the eventual draft PR body rather than embedded as self-referential source files in this package.

Automated candidate audit verifies: ZIP CRC, member safety, per-file hash manifest, preserved author license/NOTICE, original SVG across root/nested plugin, root/compat manifest fields, consistent versions and default prompts, full Skill core, exact embedded source for all unmodified files, external SHA-256 receipts, and explicit no-MCP/no-Drive/no-scientific-certification flags. An intentionally unpublished metadata check must report BLOCKED.

Engineering CI includes Python unit tests, static public audit, documentation link/privacy checks, source-language review, provenance smoke, reproducible package build, Node compilation and real **local, synthetic** MCP handshake/tool/UI-resource/no-mutation smoke.

## Manual review and blockers before changing distribution

- Compare the actual rendered 12 screens to the owner's images with desktop/mobile dark screenshots; document explicit approval. No automated claim of pixel parity.
- Implement and independently test a real authorized, authenticated per-user project adapter if remote live Drive sync is desired. A filesystem mirror or local stdio smoke does not substitute for production OAuth/HTTPS isolation.
- Decide how the private icon-only plugin beta.3 should receive the **full** beta.4 skill update. A standalone ZIP does not update it; any actual update requires explicit owner authorization, guarded current-release check and post-install verification.
- Host and authorize an actual MCP server before connecting tools/UI to the plugin. Do **not** invent an endpoint or imply the skills-only ZIP delivers the hosted UI.
- Reconcile original draft [PR #22](https://github.com/rebsonm/MeuArtigoSkill/pull/22) as a historical source of the visual prototype, without merging it separately on top of this consolidated branch.
- The owner expressly authorized merging consolidated PR #27 into main on 2026-10-11, conditioned on reviewing and correcting the README first. Check the current CI head and merge manually using the approved PR; this does not authorize any release or private plugin update.
- Public GitHub beta.2 release and its checksums must be kept available without amendment.
- If the owner later explicitly authorizes a public release, first revise candidate publication metadata and run the protected manual release process from an authorized main commit. Release metadata checks must block the current candidate.

**Acceptance recommendation: engineering candidate ready for reviewer evaluation only; distribution deployment, visual parity and scientific validation remain blocked/pending.**
