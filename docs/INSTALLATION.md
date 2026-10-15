# Install Meu Artigo — Skill


> **Last planned experimental beta: `v0.9.0-beta.6` (release preparation, 2026-10-15).** The cumulative continuity, conversational resume and safe blocker guidance update is documented in [beta.6 release notes](NOTAS-DA-VERSAO-0.9.0-beta.6.md). **Beta.5 remains the latest published installer until GitHub actually publishes beta.6 and its checksum.** This last-beta designation is a plan, not stable certification; the project-owned external-tool service and external-tool Apps UI are not live-validated. Existing installations do not auto-update.

> **Published release (2026-10-14):** [v0.9.0-beta.5](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.5) is the **recommended experimental beta**. Its versioned [Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.5/MeuArtigoSkill-v0.9.0-beta.5.zip) and [SHA-256 checksum](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.5/SHA256SUMS.txt) are available. Previous releases remain archived; installed Skills do not automatically update.


**Choose the prepared Skill archive rather than GitHub's source download.** No coding is necessary for a researcher.

**Recommended experimental version:** [beta.5 release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.5). [Historical beta.4 release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.4) remains available for reproducibility; neither is stable.

## Install the published Skill

1. **[Download the published MeuArtigoSkill-v0.9.0-beta.5.zip](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.5/MeuArtigoSkill-v0.9.0-beta.5.zip)** with the matching [SHA256SUMS.txt](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.5/SHA256SUMS.txt) from the tagged **Pre-release**.
2. Open your assistant's supported **Skills / Habilidades** import, if available for your account.
3. Select this exact Skill ZIP and confirm installation.
4. Ask: *"Quero começar um artigo com Meu Artigo; verifique primeiro minhas conexões e o armazenamento."*
5. Confirm Google Drive read/write access (or explicit fallback authorization) before creating canonical research files.

The **beta.5 tagged ZIP and checksum have been published**; use the versioned installer rather than the source checkout. All releases remain **experimental betas**; the `main` source tree is not the published installer. Earlier beta assets remain available for reproducibility.

## Avoid incorrect downloads

GitHub's **Code → Download ZIP** and automatic **Source code** archives are development checkouts with a wrapper folder. They are not the prepared Skill archive. An installable Skill has `SKILL.md` at its package root, together with the necessary references and optional scripts.

## Common problems

- **ZIP rejected:** use the direct release link above; inspect that the root contains `SKILL.md`.
- **No Skills import option:** availability depends on your plan and workspace; do not assume undocumented controls exist.
- **No Google Drive permission:** the Skill must verify access and writing, not assume installation granted authorization.
- **Visual matrix unavailable or timed out:** in beta.5 the essential protocol and continuity files should remain available. Review the reported matrix status and retry only in an authorized workspace; do not delete prior researcher files.
- **No academic database connection:** queries can be planned but never labeled executed without actual results.
- **Unclear progress:** select the real existing project before requesting a read-only summary; no fictitious project status is valid.

Maintainers can inspect ZIP structure offline using `python scripts/check_install_package.py file.zip` without uploading private data. Contact maintainers through [GitHub Issues](https://github.com/rebsonm/MeuArtigoSkill/issues), but do not share credentials or unpublished confidential materials.
