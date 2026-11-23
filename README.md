# Meu Artigo

**Repository language:** Maintained authorial text is intended to be in English throughout
the repository, including every `.md` methodology card, bibliographic card
and historical intake note—not only `docs/`. This is an **ongoing
translation**, not a completed English-only certification. Original scholarly
titles, quoted source evidence and stable identifiers remain unchanged.
See the [English migration guide](docs/ENGLISH-SOURCE-MIGRATION.md) for the
complete Markdown audit commands and the strict unresolved-language check. The
installed assistant still responds in the researcher's requested language.

[![Zenodo v1.0.0-rc.3 DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24452285.svg)](https://doi.org/10.5281/zenodo.24452285)

**Current published Zenodo software:** [Meu Artigo v1.0.0-rc.3 — DOI 10.5281/zenodo.24452285](https://doi.org/10.5281/zenodo.24452285), automatically archived from [GitHub v1.0.0-rc.3](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.3). The Zenodo version-specific DOI identifies the published **repository source snapshot**, not the separately distributed installable Skill ZIP. Earlier historical [Zenodo RC.2 — DOI 10.5281/zenodo.24450459](https://doi.org/10.5281/zenodo.24450459) remains preserved. Existing installed Skills do not automatically update.

**How to cite this version:** Mendes, Rebson de Morais. (2026). *Meu Artigo — AI-Assisted Scientific Research Workflow and Governance Tool* (v1.0.0-rc.3) [Software]. Zenodo. https://doi.org/10.5281/zenodo.24452285

**A research-support Skill for people preparing scientific articles.** Meu Artigo helps a researcher organize a question, consider appropriate methods, find and assess sources, document decisions, and prepare a manuscript. You remain responsible for the scientific work.

The project is available in a **public GitHub repository**. **Every 0.9.0-beta release is experimental**, not an independently validated research method; no stable v1.0.0 has been released.

## Getting started

**Recommended published experimental prerelease:** [v1.0.0-rc.3](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.3), authorized for publication on 2026-11-23 with the [installable Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.3/MeuArtigoSkill-v1.0.0-rc.3.zip) and [SHA-256 checksums](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.3/SHA256SUMS.txt). The separate [historical RC.1 library of 51 attributed PDFs](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.1/MeuArtigo-PDFs-51-attributed.zip) remains accessible and is not being repackaged as a new RC.3 release asset. The earlier [v0.9.0-beta.6](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.6) remains available as a historical beta.

**Current version:** `1.0.0-rc.3` — **published GitHub experimental prerelease** (not a stable release). The **recommended published GitHub experimental prerelease** is `v1.0.0-rc.3`, not stable v1.0.0 or comprehensive host certification. The versioned installable Skill ZIP is distinct from GitHub's source-code archive; installed copies do not update automatically. The central CSV/Drive workflow passed a fictional-project functional test; optional XLSX generation failed because its dependency was unavailable.

1. Follow the [installation guide](docs/INSTALLATION.md) for a compatible assistant.
2. Start a conversation about a genuine research problem. For example: *"I want to develop an article with Meu Artigo. Help me define the question and possible methodological approaches. First, check which storage and research tools are actually available."*
3. Review the options presented. You choose your method, evidence and scientific conclusions.
4. Return later and say *"Let's continue my article"* to resume from your authorized project records, when those records are accessible.

You can converse in Portuguese or another language you prefer. The article's writing language can be different from the language of your conversation.

**Release identity policy:** A future RC must use the same
software version on GitHub and Zenodo and identify the same archived
code. See the [GitHub–Zenodo parity gate](docs/GITHUB-ZENODO-VERSION-PARITY.md).
The GitHub RC.1 and separately deposited Zenodo RC.2 are not claimed
equivalent without an actual archived-source comparison.

## Researcher-guided next steps

At a meaningful decision point, updated Skill instructions propose **three
alternatives (A/B/C)** with a concrete advantage, disadvantage and next step
for each, mark **one context-based recommendation**, and offer **D — Other**
so the researcher can freely type a different answer. **Where native
radio controls exist, all four choices must have a real single-select radio
button in front of their labels** (without preselecting the recommended
option). D has a **real text field that is visible and enabled from
the start**, even before the researcher selects it; **typing selects D
automatically**. A real **Submit answer** button always appears below the
options and becomes enabled only when a valid A/B/C or nonblank D response
exists. The selected response is sent **only when that button is clicked**.
Where the host cannot render functional controls, use explicit plain-chat
A/B/C/D answers via the usual message send action, without fake clickable
circles, text boxes or buttons. Installing the Skill does not
install any additional host UI components. This is decision support,
not an automatic scientific approval or new graphical application. See the
[four-choice next-step policy](references/decision-navigation.md).
Existing installed release ZIPs do not update themselves when these source
instructions change.

## What can it help with?

- **Research question and method:** compare paths suited to qualitative, quantitative, mixed, theoretical, review or design-oriented research rather than impose one template.
- **Sources and evidence:** plan searches, organize results actually retrieved, distinguish what a source supports from an inference, and identify gaps that need checking.
- **Research continuity:** show where the recorded project stands, what still needs a decision and what may be done next.
- **C.A.D.A.:** organize tasks, people responsible and deadlines, without treating completion of a task as scientific approval.
- **Writing and submission preparation:** structure a manuscript using verified source material and journal rules; review rights, anonymity and disclosure before sharing.

The Skill separates **[L]** consulted literature, **[I]** interpretation/inference and **[P]** original propositions. Consequential scientific choices are made by the researcher, not silently by the assistant.

## Online methodological guidance from the public library

In updated source installations, a substantive methodology question triggers a
**read-only, on-demand consultation** of the public GitHub method library,
subject to actual host network and tool access. The Skill selects relevant
editorial cards, bibliographic prospecting cards and licensed public PDF pages
from the current catalogue using one pinned commit per consultation. It does
not download every PDF during installation, nor turn catalogue metadata into
a claim that an original source was read. See the
[online consultation contract](references/GITHUB-METHODOLOGY.md).

The existing published v1.0.0-rc.1 installer remains an immutable earlier
bundle: updating GitHub `main` does **not** silently update that ZIP or any
user's installed copy. This new behavior requires installation of an updated
bundle or source with these files.

## Public third-party PDF and methodology-card library

This repository includes a **public library of 51 third-party academic PDFs**, individually attributed under their publishers' Creative Commons Attribution terms. The papers retain their authors' licenses; they are **not** part of the software's Apache-2.0 license. See the [51-PDF attribution register](knowledge/methodology/PDF-ATTRIBUTIONS.md) and the [PDF catalogue](knowledge/methodology/pdf_catalog.json). One publisher labels its work CC BY without a version; no specific version is invented.

The library also includes **475 bibliographic prospecting cards [P] and 174 editorial methodological cards [I]/[P]**. These cards are aids to research, not 649 independently validated primary-source analyses or new PDFs. See the [card policy](knowledge/methodology/CARD-POLICY.md). The prepared installer ZIP stays small and retrieves public references on demand; it does not embed the third-party PDF binaries.

## What it does not promise

Installing a Skill does not automatically connect Google Drive, academic databases or other services. Access and permission must be verified; a different storage location requires your explicit agreement. A source cited by an AI may still fail to support the claim. No scientific originality, publication acceptance, quality improvement or independent validation is guaranteed.

**Help and documentation:** [Start here](docs/COMECE-AQUI.md) · [Installation](docs/INSTALLATION.md) · [ChatGPT](docs/CHATGPT.md) · [Claude](docs/CLAUDE.md) · [Gemini](docs/GEMINI.md) · [Methodological routes](docs/ROTAS-METODOLOGICAS.md) · [How to report a problem](docs/TESTE-BETA-PESQUISADORES.md).

## Rights holders and non-commercial research purpose

Meu Artigo is an independently maintained, **non-commercial research-support
initiative** intended to help scholars, not to replace original publications.
If you are an author or other rights holder and want a work corrected or
removed, please email **[rebsonm@gmail.com](mailto:rebsonm@gmail.com)**
with the title or DOI and the relevant file link. Good-faith requests are
reviewed for prompt correction or withdrawal as appropriate. The project's
purpose does **not** itself authorize redistribution of copyrighted works,
and it does not change the original software's Apache-2.0 license.
See the [full rights-holder notice](RIGHTSHOLDER-NOTICE.md).

**Source versus archive:** GitHub `main` contains changes newer than the published
GitHub RC.1 installer. The newer experimental RC.2 has a separate
[Zenodo archival DOI](https://doi.org/10.5281/zenodo.24450459), reported by
the maintainer; it is not a new GitHub release. The
[source-review snapshot workflow](docs/ZENODO-DEPOSIT-PREPARATION.md) remains a
separate, unpublished archival-preparation process. It intentionally omits
third-party PDF binaries **from that ZIP only**: all 51 original PDF files
remain in the public GitHub methodology library for online, on-demand use.

## Citation

For the newer archived experimental version, cite **Mendes, Rebson de Morais (2026). *Meu Artigo* (v1.0.0-rc.2) [Computer software]. Zenodo. [https://doi.org/10.5281/zenodo.24450459](https://doi.org/10.5281/zenodo.24450459).** The earlier Zenodo DOI, [10.5281/zenodo.24397699](https://doi.org/10.5281/zenodo.24397699), remains documented as a prior citation. The root [CITATION.cff](CITATION.cff) retains the original GitHub RC.1 release metadata while offering the Zenodo RC.2 record as the preferred citation. A software DOI does not constitute independent methodological validation.

The source and original documentation are licensed under the **Apache License 2.0**; third-party research materials retain their own rights. See [LICENSE](LICENSE), [NOTICE](NOTICE), [CITATION.cff](CITATION.cff) and [security guidance](SECURITY.md).

### Integrated RC.1 source (experimental)

The integrated source combines RC preparation and scoped IB/V1 changes.
Its operational card review is recorded in
[the individual disposition ledger](knowledge/methodology/intake/operational-validation.json).
Restricted entries are consultation aids only; blocked entries are excluded
from recommendations. AI/code acceptance does not approve scientific gates,
clear source-PDF rights, demonstrate installed-host operation or authorize a
stable release. See [card policy](knowledge/methodology/CARD-POLICY.md).
