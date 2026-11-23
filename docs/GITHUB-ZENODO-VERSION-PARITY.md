# GitHub–Zenodo source and release identity — plugin-only RC.4

## Current verifiable history

- [Published RC.3 GitHub release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.3) and [version-specific Zenodo DOI 10.5281/zenodo.24452285](https://doi.org/10.5281/zenodo.24452285) are historical. RC.3 distributed a standalone Skill ZIP; its original archive remains intact.
- Historical RC.2 Zenodo DOI: [10.5281/zenodo.24450459](https://doi.org/10.5281/zenodo.24450459); earlier RC.1 release remains preserved.
- The source candidate `1.0.0-rc.4` is **NOT PUBLISHED**. The RC.4 DOI, date, official plugin URL and Zenodo publication are all unassigned.

## Exact RC.4 identity and distribution

For RC.4, GitHub tag `v1.0.0-rc.4` must match root `VERSION`, root `CITATION.cff` and root `plugin.json` version, plus the archived source commit and Zenodo version if publication occurs. `CITATION.cff` retains the official title **Meu Artigo — AI-Assisted Scientific Research Workflow and Governance Tool** and author **Mendes, Rebson de Morais**, as split family/given names.

**Artifact:** `MeuArtigoPlugin-v1.0.0-rc.4.zip` containing the plugin manifest and internal skill. **Never** publish `MeuArtigoSkill-v1.0.0-rc.4.zip` or a second release to correct metadata. The plugin ZIP SHA-256 is not necessarily comparable with GitHub's source archive SHA; compare identical archive types only.

## Two-stage identity verification

1. **Before publication:** check out the exact approved source commit, run `python scripts/check_github_zenodo_parity.py preflight --tag v1.0.0-rc.4`, confirm the user-selected logo asset, build/verify the plugin ZIP, check source and archive integrity, software rights and RC.4 host functionality. Confirm the tag does **not** already exist. Offline tests cannot prove that.
2. **After a separately authorized GitHub release and Zenodo's automatic GitHub archiving:** independently read GitHub tag/source-commit information and Zenodo's version DOI, version and archived-source provenance. Run `scripts/check_github_zenodo_parity.py reconcile` with real evidence objects. Missing provenance is NOT_VERIFIED, never guessed from a DOI alone. Zenodo "Sync now" does not create a version: publishing the GitHub release triggers automatic archiving when the integration is enabled.

The separate `zenodo/metadata-draft.json` is internal preparation only. A root `.zenodo.json`, if introduced later, overrides the metadata interpretation of root `CITATION.cff`; ensure its title, creator and version agree exactly. Updating GitHub source or a future plugin does not retroactively change an already published Zenodo record. Do not republish RC.3 or mint a duplicate DOI for the same archived version.

## Scientific independence

DOI, repository publication, script execution, metadata parity, a plugin listing and host installation do **not** certify scientific quality, originality, empirical effects, source-rights clearance, gate approval or independent reviewer decisions. Maintain [L]/[I]/[P] and seven human-reviewed gates.

[RC.4 release process](GUIA-DE-RELEASES.md) · [RC.4 packaging](RC4-PLUGIN-DISTRIBUTION.md).
