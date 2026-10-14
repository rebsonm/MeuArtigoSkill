# Meu Artigo — v0.9.0-beta.5

**Experimental public pre-release for external beta testing.** This is not a stable release and does not establish independent scientific validation or improved research quality. It is a corrective software update to the research-support Skill; scientific decisions remain under researcher control.

## What changed in beta.5

- **More reliable project start:** essential scientific project documents and tracking records are created and checked before optional visual spreadsheet generation.
- **Fewer incomplete projects:** a stalled visual spreadsheet now has a bounded execution time. The research protocol and continuity records remain available when the optional spreadsheet cannot be generated.
- **Safer recovery:** project initialization can be resumed without silently overwriting an existing researcher's documents. An existing invalid spreadsheet is retained for inspection rather than replaced.
- **More truthful progress:** the Skill distinguishes a locally verified research workspace from a pending or failed visual spreadsheet, and no longer marks the first operational task complete before essential local files are checked.
- **Scientific governance unchanged:** seven researcher decision gates and the separation of literature consulted [L], defensible inference [I] and original propositions [P] are retained.
- **Existing research supported:** the correction does not intentionally migrate or reset prior studies, editorial decisions, or canonical Google Drive records.

## What was checked

The corrective Pull Request #62 passed a GitHub Actions run with **610 automated software tests** before integration. The tests included synthetic cases for a stalled spreadsheet generator, partial output, unavailable dependencies, interruption recovery, preservation of existing files, and invalid core tables. Further release-specific audits run as part of the publication process. These are engineering checks, not field usability studies or evidence of scientific efficacy.

## Known limitations

- **No independent scientific validation** or demonstrated improvement in the accuracy, quality, productivity, traceability or autonomy of real researchers.
- **Real-world installations remain under evaluation.** Assistant features, script execution, filesystem access and connectors depend on actual platform/account permissions.
- **Cloud storage must be verified.** A locally checked project is not proof of a completed Google Drive upload or successful canonical synchronization.
- **The visual XLSX remains optional in local fallback.** Without supported spreadsheet-generation dependencies, researchers can continue with the authorized project core and documented CSV representations.
- **Feedback is welcome:** report the actual installed version, platform, steps to reproduce, expected and observed behavior through [GitHub Issues](https://github.com/rebsonm/MeuArtigoSkill/issues); do not disclose unpublished material, sensitive personal data, licensed articles or account credentials.

## Installing and recovering

Use the prepared, versioned Skill ZIP and SHA-256 checksum from the [v0.9.0-beta.5 GitHub release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.5) **once the tagged assets are published**; GitHub's generic source-code ZIP is not the installation package. An already installed Skill is **not automatically updated** by a repository merge. Preserve project and Drive data and follow the [installation guide](INSTALLATION.md). For technical diagnosis, see the [initialization hotfix guide](INITIALIZATION-HOTFIX-2026-10-14.md).

Earlier experimental betas, including beta.4, remain archived and are not modified by this release. The package is software assistance, not a substitute for researcher judgment, source verification, research ethics or journal rules.
