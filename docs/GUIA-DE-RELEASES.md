# Meu Artigo release procedure — plugin-only since RC.4

**Current published experimental release: [v1.0.0-rc.5.1](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.5.1) (2026-11-24 UTC).** [Plugin ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.5.1/MeuArtigoPlugin-v1.0.0-rc.5.1.zip) and checksum are attached. RC.3 and earlier Skill packages are historical; RC.4 began plugin-only distribution. Zenodo version DOI pending independent confirmation.

RC.5.1 publication used the audited source commit `8a08726e366b4c0ad6345150b5d17923f877b66d` and the one-time [publication run](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/45494841982). No new tag or release is required for documentation maintenance. See [GitHub–Zenodo identity](GITHUB-ZENODO-VERSION-PARITY.md).

## Canonical distribution from RC.4

One **ChatGPT plugin** for normal chat and Work; no standalone Skill ZIP as an RC.4 release asset. The source `SKILL.md` is included internally at `skills/meu-artigo/SKILL.md` by the plugin builder; this is a plugin component, not a second installer. RC.3 and earlier Skill releases remain accessible historical records.

## Historical RC.4 candidate checks — completed for the published source

1. Develop on a branch and keep the seven scientific gates and [L]/[I]/[P] controls unchanged.
2. Verify original user-selected logo at `assets/rc4-logo.png`; no placeholder substitution. The selected logo has been verified and source includes a derived 128 × 128 PNG from the same artwork. The private plugin uses the full original 256 × 256 PNG. Confirm the CI bundle references the reviewed source icon. Run `python scripts/build_plugin_bundle.py --preflight`; a missing logo must block actual packaging.
3. Run source tests and rights checks (read-only CI; no fabricated authorization): `python scripts/release_audit.py`, `python -m unittest discover -s tests -v`, `python scripts/audit_repository_secrets.py`, `python scripts/audit_public_docs.py` and `python scripts/check_documentation_links.py`.
4. Only after the approved logo is packaged: `python scripts/build_plugin_bundle.py` followed by `python scripts/build_plugin_bundle.py --verify dist/MeuArtigoPlugin-v1.0.0-rc.4.zip` and actual SHA-256 comparison.
5. Install the exact private RC.4 plugin candidate and test separately in normal chat and Work with fictitious records. Verify only witnessed operations, including the full scientific entrypoint, A/B/C/D interaction, source rights, tools and gate integrity; maintain NOT_RUN where inaccessible. The Lab v0.1.0 is **not** equivalent RC.4 evidence.
6. Open/review a PR. Neither CI success nor merge constitutes a publication. Create a new manual RC.4-specific publisher **only after** the plugin package, rights, logo, host acceptance and release metadata are approved. An authorized RC.4 publisher was created and executed successfully on the merge commit; do not rerun it.
7. After publication (completed 2026-11-23 UTC): reconcile source citation and version DOI, verify the immutable GitHub tag and **plugin archive only**, and verify the Zenodo version-specific DOI. Do not invent DOI/date or repeat historic RC.3 deposits.

## Safety and history

- `.github/workflows/release-audit.yml` stays read-only. RC.4 builds only the plugin; legacy Skill build steps are conditioned out for RC.4. Historical manual beta/RC.1/RC.3 workflows remain as archival code and **must not be dispatched to publish RC.4**.
- `OFFICIAL_SKILL_RELEASE` is retained at `1.0.0-rc.3` as a historical pointer, not an active RC.4 distribution format.
- The public 51 third-party PDFs retain their separate licenses and must not enter the plugin package. The 649 cards remain on-demand references, not guaranteed as full text.
- Software publication does not imply independent scientific or performance validation.

See [RC.4 technical contract](RC4-PLUGIN-DISTRIBUTION.md), [installation](INSTALLATION.md), [citation/Zenodo parity](GITHUB-ZENODO-VERSION-PARITY.md).
