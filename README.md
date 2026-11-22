# Meu Artigo

**Repository language:** Maintained authorial text is intended to be in English throughout
the repository, including every `.md` methodology card, bibliographic card
and historical intake note—not only `docs/`. This is an **ongoing
translation**, not a completed English-only certification. Original scholarly
titles, quoted source evidence and stable identifiers remain unchanged.
See the [English migration guide](docs/ENGLISH-SOURCE-MIGRATION.md) for the
complete Markdown audit commands and the strict unresolved-language check. The
installed assistant still responds in the researcher's requested language.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24397699.svg)](https://doi.org/10.5281/zenodo.24397699)

**A research-support Skill for people preparing scientific articles.** Meu Artigo helps a researcher organize a question, consider appropriate methods, find and assess sources, document decisions, and prepare a manuscript. You remain responsible for the scientific work.

The project is available in a **public GitHub repository**. **Every 0.9.0-beta release is experimental**, not an independently validated research method; no stable v1.0.0 has been released.

## Getting started

**Recommended published experimental prerelease:** [v1.0.0-rc.1](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.1), published 2026-11-22 with the [installable Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.1/MeuArtigoSkill-v1.0.0-rc.1.zip), [51 attributed third-party PDFs](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.1/MeuArtigo-PDFs-51-attributed.zip) in a separate archive, and SHA-256 checksums. The earlier [v0.9.0-beta.6](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.6) remains available as a historical beta.

**Current version:** `1.0.0-rc.1` — **published GitHub experimental prerelease**, not stable v1.0.0 or comprehensive host certification. The versioned installable Skill ZIP is distinct from GitHub's source-code archive; installed copies do not update automatically. The central CSV/Drive workflow passed a fictional-project functional test; optional XLSX generation failed because its dependency was unavailable.

1. Follow the [installation guide](docs/INSTALLATION.md) for a compatible assistant.
2. Start a conversation about a genuine research problem. For example: *"I want to develop an article with Meu Artigo. Help me define the question and possible methodological approaches. First, check which storage and research tools are actually available."*
3. Review the options presented. You choose your method, evidence and scientific conclusions.
4. Return later and say *"Let's continue my article"* to resume from your authorized project records, when those records are accessible.

You can converse in Portuguese or another language you prefer. The article's writing language can be different from the language of your conversation.

## What can it help with?

- **Research question and method:** compare paths suited to qualitative, quantitative, mixed, theoretical, review or design-oriented research rather than impose one template.
- **Sources and evidence:** plan searches, organize results actually retrieved, distinguish what a source supports from an inference, and identify gaps that need checking.
- **Research continuity:** show where the recorded project stands, what still needs a decision and what may be done next.
- **C.A.D.A.:** organize tasks, people responsible and deadlines, without treating completion of a task as scientific approval.
- **Writing and submission preparation:** structure a manuscript using verified source material and journal rules; review rights, anonymity and disclosure before sharing.

The Skill separates **[L]** consulted literature, **[I]** interpretation/inference and **[P]** original propositions. Consequential scientific choices are made by the researcher, not silently by the assistant.

## Public third-party PDF and methodology-card library

This repository includes a **public library of 51 third-party academic PDFs**, individually attributed under their publishers' Creative Commons Attribution terms. The papers retain their authors' licenses; they are **not** part of the software's Apache-2.0 license. See the [51-PDF attribution register](knowledge/methodology/PDF-ATTRIBUTIONS.md) and the [PDF catalogue](knowledge/methodology/pdf_catalog.json). One publisher labels its work CC BY without a version; no specific version is invented.

The library also includes **475 bibliographic prospecting cards [P] and 174 editorial methodological cards [I]/[P]**. These cards are aids to research, not 649 independently validated primary-source analyses or new PDFs. See the [card policy](knowledge/methodology/CARD-POLICY.md). The prepared installer ZIP stays small and retrieves public references on demand; it does not embed the third-party PDF binaries.

## What it does not promise

Installing a Skill does not automatically connect Google Drive, academic databases or other services. Access and permission must be verified; a different storage location requires your explicit agreement. A source cited by an AI may still fail to support the claim. No scientific originality, publication acceptance, quality improvement or independent validation is guaranteed.

**Help and documentation:** [Start here](docs/COMECE-AQUI.md) · [Installation](docs/INSTALLATION.md) · [ChatGPT](docs/CHATGPT.md) · [Claude](docs/CLAUDE.md) · [Gemini](docs/GEMINI.md) · [Methodological routes](docs/ROTAS-METODOLOGICAS.md) · [How to report a problem](docs/TESTE-BETA-PESQUISADORES.md).

## Citation

If you use Meu Artigo in your research, please cite the archived software: **Mendes, Rebson de Morais (2026). *Meu Artigo* [Computer software]. Zenodo. [https://doi.org/10.5281/zenodo.24397699](https://doi.org/10.5281/zenodo.24397699).** The repository's [CITATION.cff](CITATION.cff) also provides machine-readable citation metadata. This DOI identifies a software deposit, not an independently validated scientific method or a peer-reviewed article.

The source and original documentation are licensed under the **Apache License 2.0**; third-party research materials retain their own rights. See [LICENSE](LICENSE), [NOTICE](NOTICE), [CITATION.cff](CITATION.cff) and [security guidance](SECURITY.md).

### Integrated RC.1 source (experimental)

The integrated source combines RC preparation and scoped IB/V1 changes.
Its operational card review is recorded in
[the individual disposition ledger](knowledge/methodology/intake/operational-validation.json).
Restricted entries are consultation aids only; blocked entries are excluded
from recommendations. AI/code acceptance does not approve scientific gates,
clear source-PDF rights, demonstrate installed-host operation or authorize a
stable release. See [card policy](knowledge/methodology/CARD-POLICY.md).
