# Install Meu Artigo — Skill

> **Release status (2026-10-14):** `0.9.0-beta.5` is the current source candidate and still requires manual tagged publication. Until its ZIP and checksum are confirmed, install the [published beta.4 Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.4/MeuArtigoSkill-v0.9.0-beta.4.zip). The beta.5 documentation describes the upcoming corrective release, not an installed upgrade.


**Choose the prepared Skill archive rather than GitHub's source download.** No coding is necessary for a researcher.

**Published installer:** [beta.4 release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.4). **Next source version:** beta.5, pending manual release. [Historical beta.1 ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.1/MeuArtigoSkill-v0.9.0-beta.1.zip) remains available; neither version is stable.

## Install the published Skill

1. **[Download the published MeuArtigoSkill-v0.9.0-beta.4.zip](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.4/MeuArtigoSkill-v0.9.0-beta.4.zip)** with the matching [SHA256SUMS.txt](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.4/SHA256SUMS.txt) from the tagged **Pre-release**.
2. Open your assistant's supported **Skills / Habilidades** import, if available for your account.
3. Select this exact Skill ZIP and confirm installation.
4. Ask: *"Quero começar um artigo com Meu Artigo; verifique primeiro minhas conexões e o armazenamento."*
5. Confirm Google Drive read/write access (or explicit fallback authorization) before creating canonical research files.

The **beta.5 source candidate is not yet a public installer**; check its separate tagged ZIP and checksum when released. All releases remain **experimental betas**; the `main` source tree is not the published installer. Earlier beta assets remain available for reproducibility.

## Avoid incorrect downloads

GitHub's **Code → Download ZIP** and automatic **Source code** archives are development checkouts with a wrapper folder. They are not the prepared Skill archive. An installable Skill has `SKILL.md` at its package root, together with the necessary references and optional scripts.

## Common problems

- **ZIP rejected:** use the direct release link above; inspect that the root contains `SKILL.md`.
- **No Skills import option:** availability depends on your plan and workspace; do not assume undocumented controls exist.
- **No Google Drive permission:** the Skill must verify access and writing, not assume installation granted authorization.
- **Visual matrix unavailable or timed out:** in beta.5 the essential protocol and continuity files should remain available. Review the reported matrix status and retry only in an authorized workspace; do not delete prior researcher files.\n- **No academic database connection:** queries can be planned but never labeled executed without actual results.
- **Unclear progress:** select the real existing project before requesting a read-only summary; no fictitious project status is valid.

Maintainers can inspect ZIP structure offline using `python scripts/check_install_package.py file.zip` without uploading private data. Contact maintainers through [GitHub Issues](https://github.com/rebsonm/MeuArtigoSkill/issues), but do not share credentials or unpublished confidential materials.
