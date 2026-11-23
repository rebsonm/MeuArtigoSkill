# Meu Artigo release procedure — RC.4 plugin-only

**Current source:** `1.0.0-rc.4`, **unpublished**. **Last published release:** [v1.0.0-rc.3](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.3), [Zenodo DOI 10.5281/zenodo.24452285](https://doi.org/10.5281/zenodo.24452285). The full title and author remain Meu Artigo — AI-Assisted Scientific Research Workflow and Governance Tool; Mendes, Rebson de Morais.

## Canonical distribution from RC.4

One **ChatGPT plugin** for normal chat and Work; no standalone Skill ZIP as an RC.4 release asset. The source `SKILL.md` is included internally at `skills/meu-artigo/SKILL.md` by the plugin builder; this is a plugin component, not a second installer. RC.3 and earlier Skill releases remain accessible historical records.

## Candidate checks — no release side effects

1. Develop on a branch and keep the seven scientific gates and [L]/[I]/[P] controls unchanged.
2. Verify original user-selected logo at `assets/rc4-logo.png`; no placeholder substitution. This is **PENDING** until the original verified image is available. Run `python scripts/build_plugin_bundle.py --preflight`; a missing logo must block actual packaging.
3. Run source tests and rights checks (read-only CI; no fabricated authorization): `python scripts/release_audit.py`, `python -m unittest discover -s tests -v`, `python scripts/audit_repository_secrets.py`, `python scripts/audit_public_docs.py` and `python scripts/check_documentation_links.py`.
4. Only after the approved logo is packaged: `python scripts/build_plugin_bundle.py` followed by `python scripts/build_plugin_bundle.py --verify dist/MeuArtigoPlugin-v1.0.0-rc.4.zip` and actual SHA-256 comparison.
5. Install the exact private RC.4 plugin candidate and test separately in normal chat and Work with fictitious records. Verify only witnessed operations, including the full scientific entrypoint, A/B/C/D interaction, source rights, tools and gate integrity; maintain NOT_RUN where inaccessible. The Lab v0.1.0 is **not** equivalent RC.4 evidence.
6. Open/review a PR. Neither CI success nor merge constitutes a publication. Create a new manual RC.4-specific publisher **only after** the plugin package, rights, logo, host acceptance and release metadata are approved. No RC.4 publisher exists now.
7. At approved publication time, reconcile VERSION/CITATION/manifest, record actual UTC publication date, create a new immutable GitHub tag and **plugin archive only**, verify GitHub source commit, then independently verify Zenodo's automatically generated version DOI. Do not invent DOI/date or repeat historic RC.3 deposits.

## Safety and history

- `.github/workflows/release-audit.yml` stays read-only. RC.4 builds only the plugin; legacy Skill build steps are conditioned out for RC.4. Historical manual beta/RC.1/RC.3 workflows remain as archival code and **must not be dispatched to publish RC.4**.
- `OFFICIAL_SKILL_RELEASE` is retained at `1.0.0-rc.3` as a historical pointer, not an active RC.4 distribution format.
- The public 51 third-party PDFs retain their separate licenses and must not enter the plugin package. The 649 cards remain on-demand references, not guaranteed as full text.
- Software publication does not imply independent scientific or performance validation.

See [RC.4 technical contract](RC4-PLUGIN-DISTRIBUTION.md), [installation](INSTALLATION.md), [citation/Zenodo parity](GITHUB-ZENODO-VERSION-PARITY.md).
