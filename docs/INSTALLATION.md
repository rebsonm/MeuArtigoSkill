# Install Meu Artigo — Skill

**Choose the prepared Skill archive rather than GitHub's source download.** No coding is necessary for a researcher.

**Previously published experimental beta:** [beta.1 Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.1/MeuArtigoSkill-v0.9.0-beta.1.zip). This historical fallback remains downloadable while the beta.4 prerelease assets are not yet available; neither beta is stable.

## Install the published Skill

1. **[Download MeuArtigoSkill-v0.9.0-beta.4.zip](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.4/MeuArtigoSkill-v0.9.0-beta.4.zip)** once its tagged **Pre-release** assets and `SHA256SUMS.txt` are visible. Until then, an earlier published beta remains available.
2. Open your assistant's supported **Skills / Habilidades** import, if available for your account.
3. Select this exact Skill ZIP and confirm installation.
4. Ask: *"Quero começar um artigo com Meu Artigo; verifique primeiro minhas conexões e o armazenamento."*
5. Confirm Google Drive read/write access (or explicit fallback authorization) before creating canonical research files.

All released versions remain **experimental betas**. A prepared beta.4 source is not an installable published release until the tagged ZIP and checksum appear. The `main` source tree is never a substitute. Earlier published beta assets remain available for reproducibility.

## Avoid incorrect downloads

GitHub's **Code → Download ZIP** and automatic **Source code** archives are development checkouts with a wrapper folder. They are not the prepared Skill archive. An installable Skill has `SKILL.md` at its package root, together with the necessary references and optional scripts.

## Common problems

- **ZIP rejected:** use the direct release link above; inspect that the root contains `SKILL.md`.
- **No Skills import option:** availability depends on your plan and workspace; do not assume undocumented controls exist.
- **No Google Drive permission:** the Skill must verify access and writing, not assume installation granted authorization.
- **No academic database connection:** queries can be planned but never labeled executed without actual results.
- **Unclear progress:** select the real existing project before requesting a read-only summary; no fictitious project status is valid.

Maintainers can inspect ZIP structure offline using `python scripts/check_install_package.py file.zip` without uploading private data. Contact maintainers through [GitHub Issues](https://github.com/rebsonm/MeuArtigoSkill/issues), but do not share credentials or unpublished confidential materials.
