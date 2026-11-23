# RC.4 — canonical plugin-only distribution contract

## Decision and scope

Starting with `1.0.0-rc.4`, **Meu Artigo is distributed only as a ChatGPT plugin**. One installable product must be usable from ordinary ChatGPT conversation and Work, when the host/account exposes that plugin. This replaces the prior two-format proposal: **there will be no separate RC.4 standalone Skill ZIP**.

The existing root `SKILL.md` stays in the Git source as the canonical scientific instruction text; the plugin builder **copies** it to `skills/meu-artigo/SKILL.md`, together with its references, eligible scripts and documentation. It is an internal plugin skill, not a separate distribution artifact. Historical Skill installers/DOIs/tags remain unchanged.

## Required package

- Portable Agent Plugins manifest `plugin.json`: name `meu-artigo`, version `1.0.0-rc.4`, author Rebson de Morais Mendes, official title/presentation and accurate capabilities.
- Archive `MeuArtigoPlugin-v1.0.0-rc.4.zip` with one enclosing `meu-artigo/` folder.
- Internal `skills/meu-artigo/SKILL.md` with exact source content (no experimental Lab override), scientific documents and eligible support scripts; dependency closure and per-file checksums.
- **New user-supplied logo:** reserve `assets/rc4-logo.png` at package root, referenced by the final plugin manifest. The selected logo is now included as a reviewed PNG optimized to 128 × 128 directly from the user's uploaded 256 × 256 artwork, preserving the composition. The private plugin candidate contains the original 256 × 256 image. The builder must still verify its signature and dimensions, never substitute unrelated artwork.
- No scholarly third-party PDF binaries, credentials, private research data, generated output or host installation receipts in the package.
- Exactly one RC.4 version marker across `VERSION`, root `CITATION.cff`, plugin manifest, build receipt and subsequent release metadata. DOI/date are **unset until real publication**; RC.3 DOI is historical.

## Capability boundaries

The internal scientific contract remains unchanged: C.A.D.A., [L]/[I]/[P], A/B/C/D (native only when available), RAG/on-demand method-card consultation when permitted tools genuinely retrieve materials, optional scripts when the host can run them, source rights, method-specific analysis, seven researcher gates with no automatic approvals, project continuity only from the authorized canonical state.

Plugin creation alone cannot prove:
1. execution of Python scripts or a remote MCP service,
2. Drive storage persistence or write permission,
3. access to all 649 cards or third-party PDF full text,
4. genuine keyboard-operable native radio UI in each host,
5. identical behavior in normal ChatGPT and Work.

Test these independently in both intended surfaces. Retain NOT_RUN/NOT_VERIFIED for unavailable capabilities. Do not infer complete RC.3 feature parity from the private RC.2-based Lab prototype.

## Publication process

1. Prepare RC.4 source on a review branch; maintain source/version/documentation without touching RC.3 tags, assets or Zenodo records.
2. Obtain the original user-selected logo image file, check rights, file signature, legibility, dimensions (48–4096px), <=5 MiB, appropriate square composition; keep the visual artwork unchanged unless separately approved.
3. Run `python scripts/build_plugin_bundle.py --preflight`. A missing logo may be reported as a **blocking pending prerequisite**, not treated as acceptance.
4. Once complete, build `python scripts/build_plugin_bundle.py` and verify the resulting archive and SHA-256. Verify source/packaged SKILL exact SHA-256 equivalence, dependencies, no third-party PDFs, release identity.
5. Install the exact RC.4 candidate in a private test plugin and perform fictitious normal-chat and Work tests; preserve seven PENDING gates and externally observed receipts.
6. Only after actual functional and rights acceptance, prepare an explicitly authorized, manual one-time GitHub release, then verify Zenodo automatic archival and version-specific DOI. Do not republish or edit historical RC.3 through this RC.4 pipeline.

**Status:** PREPARATION ONLY. No RC.4 GitHub release, tag, Zenodo DOI, official plugin installation or scientific validation is asserted.
