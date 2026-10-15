# Install Meu Artigo

You do not need to be a programmer or use GitHub commands to install Meu Artigo. You do need an assistant that supports Skills.

## Which version should I use?

The [beta.5 release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.5) is the latest **confirmed published installer**. The beta.6 improvements are already present in the repository's source, but its installable release has not been confirmed. Always check [Releases](https://github.com/rebsonm/MeuArtigoSkill/releases) for the newest complete package before downloading.

All current releases are experimental; none is independently scientifically validated.

## Install in a supported assistant

1. On the published release page, download the file named `MeuArtigoSkill-v0.9.0-beta.5.zip` and, if you wish to verify it, `SHA256SUMS.txt`.
2. In your assistant, find its supported **Skills** import feature. The name and availability depend on the service and account.
3. Import the downloaded Skill ZIP. If your environment instead uses Skill folders, unpack it so that `SKILL.md` is at the top level.
4. Start a conversation in your usual language:
   > I want to start a scientific article with Meu Artigo. Please check which tools and authorized storage are available, then help me formulate a research question.
5. Review the suggested approaches and decide how you want to proceed.

**Important:** GitHub's **Code → Download ZIP** and automatic **Source code** archives are copies of the development repository, not the prepared Skill installer.

## What happens at first use?

Meu Artigo checks which services it can actually reach. Google Drive is its preferred project storage when you have authorized and verified write access. Simply seeing a connected account is not confirmation that your files were saved there. If Drive cannot be used, the assistant must ask before switching to another workspace.

You can start without a journal in mind. If you already have one, share its official author guidelines. You do not need to build search strings, matrices or a complete methodology before your first conversation.

## Updating an installed Skill

A new GitHub version does **not** update the copy installed in your assistant. Install a new package deliberately and preserve your existing research files. Ask Meu Artigo to read the actual saved project before continuing; it should not reconstruct decisions from memory alone.

## If something does not work

- **No Skills import:** check whether your assistant/account offers the feature; see [platform guidance](COMPATIBILIDADE-PLATAFORMAS.md).
- **ZIP rejected:** use the prepared file from the release page, not the source-code ZIP.
- **Drive unavailable:** ask the assistant to explain what access is missing. No upload should be reported as completed without evidence.
- **No literature database connection:** Meu Artigo can help design a search and work with an authentic export you provide; it must not invent retrieved studies.
- **Cannot continue an earlier article:** identify the correct saved project and authorized storage. If those records are inaccessible, progress remains unverified.

See [Getting started](COMECE-AQUI.md) and [Support / feedback](TESTE-BETA-PESQUISADORES.md).
