# Meu Artigo — compatibility and distribution from RC.4

**Only the ChatGPT plugin is planned for RC.4.** There will be no standalone RC.4 Skill ZIP or dedicated Claude/Gemini installation package. The GitHub repository remains public source code and historical Skill releases remain untouched.

| Surface | RC.4 plan | Evidence status |
| --- | --- | --- |
| ChatGPT normal chat | Select the official Meu Artigo plugin | Lab plugin observed by maintainer; official RC.4 NOT_VERIFIED |
| ChatGPT Work | Use the same official plugin when Work exposes it | Lab plugin observed by maintainer; official RC.4 NOT_VERIFIED |
| Standalone Skill import | **Not offered for RC.4** | Historical RC.3 and earlier only |
| Claude / Gemini | No official RC.4 installer promised | NOT_SUPPORTED_AS_A_RELEASE_TARGET |

The internal `skills/meu-artigo/SKILL.md` is part of the plugin archive. It does not create a separate product or guarantee a host will execute bundled scripts.

Researcher interactions may use Portuguese, English or another requested language. Source documents are maintained mainly in English and manuscripts follow verified editorial requirements independently.

Full platform capability verification remains PENDING. See [platform-capability-preflight.md](../references/platform-capability-preflight.md). External tools, writable Drive, remote GitHub consultation, native choice UI and local Python execution depend on the host and permissions; a successful static package test is not a real-host functional test. Scientific judgments remain subject to human review and the seven gates.

**Last published version:** [GitHub RC.3](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.3) with [Zenodo DOI](https://doi.org/10.5281/zenodo.24452285). **RC.4: unpublished candidate; no DOI.**

[Installation](INSTALLATION.md) · [ChatGPT](CHATGPT.md) · [RC.4 technical contract](RC4-PLUGIN-DISTRIBUTION.md).
