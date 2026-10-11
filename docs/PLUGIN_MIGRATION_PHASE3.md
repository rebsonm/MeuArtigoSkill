# Phase 3/5 — ChatGPT plugin migration and PR #22 integration

Status: **Unreleased source implementation on a corrective maintenance branch**.
Historical public `v0.9.0-beta.2` is immutable. Do not confuse installed
plugin metadata with a published GitHub release, a hosted MCP Apps service,
or independent scientific evaluation.

## Distribution identities

- GitHub source: `VERSION = 0.9.0-beta.2` until Phase 5 candidate versioning.
- Privately installed plugin: separate icon-only hotfix version
  `0.9.0-beta.3`. The update changed only the portable and Codex manifest
  icon references and retained the original SVG already shipped as
  `assets/icon.svg`. Read-back confirmed both `logo` and `composerIcon`.
  Runtime rendering in a user's browser is not verified by the package read-back.
- Source-code feature: PR #22's read-only MCP Apps five-view dashboard
  selectively ported to the post-beta.2 branch, *not merged into main*.
- `scripts/build_plugin_bundle.py`: reproducible
  `MeuArtigoPlugin-v<VERSION>-candidate.zip` with compatible manifest,
  icon and complete namespaced `skills/meu-artigo/` core, plus an external
  `PLUGIN_BUILD_RECEIPT.json`. This is a **skills-only candidate**, not a
  host deployment or update to the installed personal plugin.

## Reused visual identity

The historical logo is the GitHub source file `assets/icon.svg`.
The plugin candidate must include an identical copy as
`skills/meu-artigo/assets/icon.svg`. Manifests at
`plugin/plugin.json` and `plugin/.codex-plugin/plugin.json` must both
reference `./assets/icon.svg` via `logo` and `composerIcon`.
No recreated or stock imagery is allowed to replace this asset.
The manifest path, not merely the asset's existence, is the listing contract.

## Functional PR #22 reconciliation

- `scripts/source_report_integrity.py` verifies source report inputs,
  hashes, decision bindings and source/reviewer boundaries.
- `scripts/visual_dashboard.py` derives read-only statuses from a
  configured local mirror; no new canonical database or implied Drive sync.
- `visual-app/` supplies five views (overview, C.A.D.A., human gates,
  evidence controls, and history/synchronization), MCP Apps resource and
  `meu_artigo_dashboard` tool. The UI itself never approves a gate.
- **UX parity is not yet complete:** the product owner provided 12 approved
  conceptual screen experiences. The original five-section MCP implementation
  is a technical MVP rather than visual acceptance. See
  [approved UX and gap-by-gap acceptance](UX_APPROVED_REFERENCE_12_SCREENS.md)
  before claiming a design match; no screenshots' illustrative metrics are
  real research data.
- Existing code in `verify_sources.py`, `quality_benchmark.py`,
  `scientific_evidence_tiers.py`, `governance_events.py` and
  `validate_project.py` was updated by applying PR #22 patches
  **to the corrective branch's existing files**, preserving newer
  beta.2 data-integrity and trace parsing fixes.
- Original reviewable draft PR #22 stays open and unmerged.
- The ported PR's offline tests and Node client/server smoke cover synthetic
  inputs, not real ChatGPT account integration or licensed database access.

## Truth and authorization model

Source of truth: existing authorized Google Drive project and canonical
CSV/JSON plus CONTINUIDADE.md, human decisions and snapshots.
Local `GOOGLE_DRIVE_STAGING` means a read-only derived mirror; the
current MVP has **no live Drive API adapter**. `WORK_FALLBACK` requires
explicit authorization. No project/corpus/Drive data was edited for this
source migration.

The MCP app must not receive arbitrary filesystem paths, edit decisions,
invent human validation or claim synchronization. `MINIMAL`/`FULL`
change only presentation. MCP results may expose bounded project title,
task description, owner and short trace summaries; use host permissions,
user consent, tenant isolation and content redaction before a real hosted
multi-user connection. No protected PDFs, source text or keys may enter
the public code or packaged source.

## Deployment boundary

The currently installed private ChatGPT plugin remains **skills-only** after
its icon hotfix. Registering or deploying MCP Apps requires an actual
authenticated HTTPS endpoint and supported connection/binding, along with
an authorized project adapter. A localhost port or GitHub source URL
is **not** a remote production endpoint. The runtime from PR #22 is a
local prototype; do not expose it publicly without identity controls.

Updating GitHub does not automatically update ChatGPT's privately installed
plugin, and a package that carries an MCP Apps UI source is not proof that
the UI is active in the host. Never update the installed plugin's scientific
core or change its distribution mode silently.

## Engineering acceptance checkpoints

1. Repository Python regressions and public release safety audit pass.
2. PR #22 Python verification tests pass.
3. Node TypeScript build + MCP stdio tool/resource smoke pass with synthetic
   files; no live Google Drive or independent evidence invented.
4. Icon file bytes and both manifest paths match exact historical SVG.
5. Candidate plugin ZIP excludes secrets, PDFs, private corpus,
   temporary output and unconfigured MCP endpoints.
6. Any failed check remains visible in GitHub Actions history and is
   resolved by a new passing run rather than rewriting historical evidence.
7. Deployment, installation and Phase 5 publication need independent
   authorization and actual host verification.

## Next steps

Phase 4: full regression, documentation coherence, portability checks,
controlled recovery cases and a fresh-session continuity exercise with an
authorized test fixture. Phase 5: bump a separate candidate version,
generate complete source/plugin artifacts and hashes, and create a PR
for review without merging or publishing the scientific release.

## Executed regression — 2026-10-11

Successful source code runs on the corrective branch after the PR #22 port:

- [Post-beta2 corrective regressions, run 38111626207](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/38111626207):
  **372 Python unittest tests, 0 failed**, static release audit,
  checked internal documentation links, public-data leak audit, English-source
  audit, provenance smoke, and reproducible Skill ZIP SHA-256 check.
- [Meu Artigo Visual checks, run 38111626202](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/38111626202):
  8 dashboard tests, 14 integrity tests, 13 verification tests,
  `npm run build` and `npm run test:smoke` (real local MCP stdio
  handshake, read-only tool and UI resource in a synthetic sandbox, no mutation).
- Private plugin icon: current private release `0.9.0-beta.3` read back
  from the plugin account. Both root/compat manifests have
  `logo=composerIcon=./assets/icon.svg`. The asset's **entire SVG content**
  was compared with GitHub `assets/icon.svg` and found identical. This
  checks package identity, not client UI rendering.

The release audit initially failed after the README mentioned a private
internal script path; that documentation issue was fixed and the new CI run
passed. A prior SKILL entrypoint length failure was likewise corrected
without discarding substantive gate protections. All failed intermediate
runs remain visible.

Unexecuted: live ChatGPT MCP Apps connection, dedicated hosted server with
per-user Drive data access, real cross-session Drive synchronization, public
deployment and scientific evaluation. No human Gate 4 decision was generated.
