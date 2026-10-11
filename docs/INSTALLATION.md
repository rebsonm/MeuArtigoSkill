# Install Meu Artigo — choose the correct download

**No programming required.** This guide is for someone seeing Meu Artigo for the first time. You do not need to understand GitHub branches, commits, or programming files.

## Start here: which installation do you want?

| I want to… | Where to install | Correct file | Available to whom? |
| --- | --- | --- | --- |
| **Use the public Meu Artigo Skill** | ChatGPT **Skills / Habilidades** (if available on your account), or another supported Skills platform | [Download the published Skill beta.2 ZIP directly](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.2/MeuArtigoSkill-v0.9.0-beta.2.zip) | Public experimental beta |
| **Use the Meu Artigo ChatGPT plugin** | ChatGPT **Plugins** | A separately prepared plugin ZIP with `plugin.json` and `skills/meu-artigo/SKILL.md` | **Beta.4 currently exists as an owner's private plugin.** A general public plugin installer/listing is **not yet available** |
| **Update a plugin I already own** | Open **my existing plugin**, then **Upload new version / Enviar nova versão** | A compatible, newer **plugin** ZIP; never a Skill or GitHub source ZIP | Eligible plugin owners/editors with the actual package |
| **Read the source code** | GitHub | **Code → Download ZIP** | Everyone; **not an installation ZIP** |

**Important:** The beta.4 source has been merged to `main`, but the last public installable **Skill release** is still **beta.2**. The owner's private **plugin** has a beta.5 PNG-icon presentation update, while its scientific core remains beta.4. These are different distribution channels, not an automatic upgrade.

## A. Install the public Skill (recommended public entry path)

1. Click **[Download the actual Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.2/MeuArtigoSkill-v0.9.0-beta.2.zip)**. Your downloaded filename should be `MeuArtigoSkill-v0.9.0-beta.2.zip`.
2. In ChatGPT, open **Plugins → Habilidades / Skills**. Where your account provides a Skill upload control, choose **Create / Add / Upload from computer** (labels may vary).
3. Select that **Skill ZIP**. Do **not** select **Plugins → Add plugin / Adicionar plugin** for a Skill ZIP.
4. Wait until the platform confirms installation. Start a conversation in your language: *“Quero começar um artigo científico usando Meu Artigo. Primeiro verifique minhas conexões e o local de armazenamento.”*
5. Ask the assistant to verify actual Google Drive read/write access before it claims anything was saved. Installing a Skill does not grant paid research API access, executable Python or the visual MCP App.

If your account does not offer Skills upload, do not assume you have access or try to force a plugin ZIP. Consult the [platform guide](CHATGPT.md) and [official ChatGPT help](https://help.openai.com/pt-br/articles/20001066-skills-in-chatgpt).

## B. Install the ChatGPT plugin (for eligible recipients)

**Not a public beta.4 distribution yet:** only the creator's private plugin is confirmed installed; other users cannot automatically install that private instance from this repository.

When a properly distributed Meu Artigo plugin ZIP is made available to you:

1. Verify you received a **plugin** ZIP, not the GitHub source archive or the public Skill ZIP. A genuine plugin package has `plugin.json` at its package root and the included `skills/meu-artigo/SKILL.md`, along with the icon files.
2. Open **Plugins** and choose **Adicionar / Add → Add plugin / Novo plugin** (the name may vary by platform).
3. Choose the plugin ZIP and follow the onscreen installer. Use an available permissions review if shown.
4. Look for **Meu Artigo** in your created/installed plugins. Open it to confirm its name and installed version.
5. Check services separately: the current private beta.4 plugin is **skills-only**. A visual MCP host and Google Drive connector are not silently provisioned by the ZIP.

**If you already have Meu Artigo:** open the **existing plugin** and use **Enviar nova versão / Upload new version**. Don't create a duplicate. Only the owner of a plugin can use its update control; you cannot update someone else's plugin without permission.

## C. Never upload these ZIPs as a ChatGPT plugin

| File or button | Why it is the wrong choice |
| --- | --- |
| **Code → Download ZIP** on the repository page | Downloads the **source tree**, not a packaged plugin |
| GitHub's automatic **Source code (zip)** / **Source code (tar.gz)** | Same source tree; missing the manifest in the required package position |
| `MeuArtigoSkill-v…zip` | This is for **Skills**, not **Add plugin** |
| Any ZIP renamed to include “Plugin” | Renaming does **not** convert its contents |
| A partial ZIP containing only `SKILL.md` | Does not contain the complete plugin structure and support files |

When a public plugin distribution exists in the future, it must have its **own clearly named release asset and verified hash**, distinct from the Skill ZIP and GitHub-generated source downloads. Until then, the repository should not pretend that an installable public plugin beta.4 asset exists.

## D. Common error messages and what to do

**“Não foi possível adicionar o plugin” / “Unable to add plugin.”**

Check the filename. If it looks like `MeuArtigoSkill-main.zip` or `MeuArtigoSkill-fix-….zip`, it is probably a GitHub source archive. Return to the decision table above and choose the correct installation route.

**“Plugin archive must contain … plugin.json … skills/*/SKILL.md …”**

This is a **package structure error**, not a problem with your article or the research method. Download or request a separately built **plugin** ZIP. Do not manually move individual files into random directories without validating the result.

**“Upload new version” refuses the ZIP.**

First confirm you are editing the **same owned plugin**, that the ZIP contains a valid plugin manifest with its matching name, and that its version is newer than the installed one. A Skills ZIP or source archive is not a plugin update.

**The icon is missing, despite successful upload.**

A plugin must bundle the actual image and point `logo` / `composerIcon` to the correct contained path. For Meu Artigo beta.4 the original SVG is `assets/icon.svg`. The creator should check the installed manifest; uploading random images or replacing branding is not necessary.

**The plugin installs but the twelve custom visual screens do not appear.**

Installation of the **skills-only** beta.4 plugin does **not** deploy the separate MCP Apps prototype. The visual host, security and live Drive adapter still require independent integration and authorization.

**There is no Skills or plugin upload menu.**

Features and permissions depend on the account and workspace. Refer to current ChatGPT settings and supported methods. We cannot guarantee a hidden installer or a universal one-click link.

## E. Optional ZIP preflight (for support personnel)

Ordinary users do **not** need Python. Maintainers can run this offline checker without uploading data:

```bash
python scripts/check_install_package.py "download.zip" --expect plugin
python scripts/check_install_package.py "download.zip" --expect skill
```

It reports **PLUGIN**, **SKILL** or **GITHUB_SOURCE** and gives a next step. It does not contact ChatGPT, install anything, read private research data or prove product entitlement. A passed ZIP check means **packaging structure**, not guaranteed live account installation.

## Need help?

Include the **filename**, whether you chose **Habilidades / Skills** or **Plugins**, and the **error text** in a [GitHub issue](https://github.com/rebsonm/MeuArtigoSkill/issues). You do **not** need to send passwords, authenticated links, private research data or proprietary full texts.

If possible, share an image of the error after removing personal account details. This helps improve the guide without exposing your research.
