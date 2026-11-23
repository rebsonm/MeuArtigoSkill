# Install Meu Artigo

**RC.3 authorized release (2026-11-23 UTC):** [GitHub v1.0.0-rc.3](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.3) | [installable Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.3/MeuArtigoSkill-v1.0.0-rc.3.zip). Historical RC.1 references below remain valid for their original archived assets; the Zenodo RC.3 version-specific DOI is pending independent verification.


You do not need to be a programmer or use GitHub commands to install Meu Artigo. You do need an assistant that supports Skills.

## Which version should I use?

The **current published experimental prerelease is [v1.0.0-rc.1](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.1)** (22 November 2026). Download the [prepared Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.1/MeuArtigoSkill-v1.0.0-rc.1.zip) and [SHA256SUMS](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.1/SHA256SUMS.txt) directly from GitHub. It is experimental, not stable v1.0.0 or comprehensive host certification.

**Zenodo experimental RC.2 record:** [DOI 10.5281/zenodo.24450459](https://doi.org/10.5281/zenodo.24450459), archived separately. The previous GitHub RC.1 installer linked above is not the RC.2 package; do not confuse the two publication channels. The current lightweight Skill is designed to consult the 51 public PDF files remotely on GitHub rather than including them in the installable ZIP.

The release also contains a [separate archive of 51 attributed academic PDFs](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.1/MeuArtigo-PDFs-51-attributed.zip). **Do not import this PDF archive as a Skill**. The older [beta.6](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.6) remains accessible for historical comparison.

## Install in a supported assistant

1. On the published release page, download the file named `MeuArtigoSkill-v1.0.0-rc.1.zip` and, if you wish to verify it, `SHA256SUMS.txt`.
2. In your assistant, find its supported **Skills** import feature. The name and availability depend on the service and account.
3. Import the downloaded Skill ZIP. If your environment instead uses Skill folders, unpack it so that `SKILL.md` is at the top level.
4. Start a conversation in your usual language:
   > I want to start a scientific article with Meu Artigo. Please check which tools and authorized storage are available, then help me formulate a research question.
5. Review the suggested approaches and decide how you want to proceed.

**Important:** GitHub's **Code → Download ZIP** and automatic **Source code** archives are copies of the development repository, not the prepared Skill installer.

## What happens at first use?

Meu Artigo checks which services it can actually reach. Google Drive is its preferred project storage when you have authorized and verified write access. Simply seeing a connected account is not confirmation that your files were saved there. If Drive cannot be used, the assistant must ask before switching to another workspace.

You can start without a journal in mind. If you already have one, share its official author guidelines. You do not need to build search strings, matrices or a complete methodology before your first conversation.

## Using current online methodological cards and PDFs

The updated `SKILL.md` in the repository source directs the assistant to
consult the public GitHub method library automatically **when** methodological
guidance is needed, after the authorized project-storage preflight. This does
not mean the installation action itself fetches PDFs. The assistant uses the
available runtime tools: preferably the small bundled
`scripts/consult_live_methodology.py` client (Python and HTTPS required), or
an actually accessible read-only GitHub/web source. The lookup is scoped to
relevant source entries and one immutable Git commit.

If no network or PDF parser exists, the Skill must say what was not read; no
scientific gate is autoapproved. The **already published RC.1 ZIP does not
contain this new live router**, so researchers must install a future
updated, verified bundle/source to receive the new behavior. Do not use a
source-code archive as though it were the prepared RC.1 installer.

## Updating an installed Skill

A new GitHub version does **not** update the copy installed in your assistant. Install a new package deliberately and preserve your existing research files. Ask Meu Artigo to read the actual saved project before continuing; it should not reconstruct decisions from memory alone.

## If something does not work

- **No Skills import:** check whether your assistant/account offers the feature; see [platform guidance](COMPATIBILIDADE-PLATAFORMAS.md).
- **ZIP rejected:** use the prepared file from the release page, not the source-code ZIP.
- **Drive unavailable:** ask the assistant to explain what access is missing. No upload should be reported as completed without evidence.
- **No literature database connection:** Meu Artigo can help design a search and work with an authentic export you provide; it must not invent retrieved studies.
- **Cannot continue an earlier article:** identify the correct saved project and authorized storage. If those records are inaccessible, progress remains unverified.

See [Getting started](COMECE-AQUI.md) and [Support / feedback](TESTE-BETA-PESQUISADORES.md).
