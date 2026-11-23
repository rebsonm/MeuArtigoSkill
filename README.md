# Meu Artigo — AI-Assisted Scientific Research Workflow and Governance Tool

**Current version:** `1.0.0-rc.4` — **unpublished release candidate**; **plugin-only distribution planned**. This source is **not published** as RC.4, is **not a stable release**, and has not passed RC.4 live-host acceptance. Do not cite an RC.4 DOI or assume it can already be installed.

**Last published experimental prerelease version:** [v1.0.0-rc.3 on GitHub](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.3); [Zenodo version-specific DOI 10.5281/zenodo.24452285](https://doi.org/10.5281/zenodo.24452285). Its historical Skill ZIP remains accessible and unchanged. Earlier deposits and releases are preserved, including the historical [v0.9.0-beta.6](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.6). Every 0.9.0-beta release is experimental; no stable v1.0.0 has been published.

## Getting started

For **RC.4 and subsequent approved versions**, Meu Artigo will be distributed as **one ChatGPT plugin**, not as a separate downloadable Skill installer. Its scientific skill instructions, methodological documentation and eligible support files live **inside the plugin**. A nested `skills/meu-artigo/SKILL.md` is an internal plugin component, **not a second product**.

- **ChatGPT normal conversation:** open/activate the installed plugin, if available in your account, and request scientific guidance.
- **ChatGPT Work:** use the same plugin inside a Work task when plugin access and Work tools are actually available.
- **Other hosts:** RC.4 standalone Skill, Claude and Gemini installers are **not** promised or distributed. The public repository remains inspectable source code.

The private **Meu Artigo Lab v0.1.0** was a feasibility experiment with an RC.2-based instructional copy and RC.3-style decision flow; it is **not** the official RC.4 build or proof that all capabilities work in each host.

**Installation:** [plugin instructions](docs/INSTALLATION.md). **Technical migration:** [RC.4 plugin-only design](docs/RC4-PLUGIN-DISTRIBUTION.md). **Platforms:** [compatibility and verification](docs/COMPATIBILIDADE-PLATAFORMAS.md).

## Scientific assistance

Meu Artigo helps researchers frame questions, compare methodological strategies, inspect authentic literature, document evidence and decisions, assess source evidence and prepare manuscripts using verified sources. It does **not** replace researcher judgment or confer scientific validation.

- Distinguish **[L]** literature actually consulted, **[I]** bounded interpretation and **[P]** the researcher's differentiated original proposition.
- Make consequential choices through **A/B/C/D**: three options with pros, cons and a contextual recommendation; D accepts an original answer. Functional controls are host-dependent, and submitting a choice does not approve a scientific gate.
- Preserve **all seven human-reviewed gates**. A generated log, tool response or completed C.A.D.A. task is not approval.
- Support qualitative, quantitative, mixed methods, reviews, design science and relevant research-method choices, without forcing every study through one bibliographic-review route.
- Use Google Drive only with genuine authorization and confirmed operations. Plugin installation does not provide credentials, write permissions or tools by itself.
- The public GitHub repository's methodology library contains **475 bibliographic prospecting cards [P] and 174 editorial cards [I]/[P]**, plus **51 separately licensed research PDFs**. The plugin must consult eligible source material on demand where verified access exists; it does not embed third-party PDF binaries or claim they were read by merely indexing them.

Documentation is written primarily in English; researcher-facing responses follow the researcher's language. Manuscript language is a separate scholarly/editorial choice.

## RC.4 preparation status

**Plugin-only packaging is in development.** The user-selected logo has not yet been available as a verified image file for packaging; the release logo asset is therefore **PENDING**, not replaced by a guessed drawing. A release must pass asset verification, integrity checks, supported-host use, rights checks and GitHub–Zenodo identity reconciliation.

The RC.4 build must emit `MeuArtigoPlugin-v1.0.0-rc.4.zip` only. Historic `MeuArtigoSkill-*.zip` files remain published for older releases, but **no new RC.4 standalone Skill ZIP** may be produced or advertised.

## Citation and rights

**Published RC.3 citation:** Mendes, Rebson de Morais. (2026). *Meu Artigo — AI-Assisted Scientific Research Workflow and Governance Tool* (v1.0.0-rc.3) [Software]. Zenodo. https://doi.org/10.5281/zenodo.24452285

**RC.4:** citation metadata are a candidate only. Do not invent publication dates or a version DOI before an actual release and Zenodo deposit. See [CITATION.cff](CITATION.cff) and [GitHub–Zenodo controls](docs/GITHUB-ZENODO-VERSION-PARITY.md).

Software is licensed under the Apache License 2.0 (Apache-2.0), subject to [LICENSE](LICENSE), [NOTICE](NOTICE) and [SECURITY.md](SECURITY.md). Academic PDFs and other third-party source texts retain their original licenses. For rights-holder corrections contact rebsonm@gmail.com.

**Additional guides:** [Start here](docs/COMECE-AQUI.md) · [ChatGPT](docs/CHATGPT.md) · [Research routes](docs/ROTAS-METODOLOGICAS.md) · [Release guide](docs/GUIA-DE-RELEASES.md) · [Open validation issues](docs/VALIDACOES-PENDENTES.md).
