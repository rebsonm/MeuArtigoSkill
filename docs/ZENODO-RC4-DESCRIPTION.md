# Zenodo public description — Meu Artigo v1.0.0-rc.4

This is the **canonical post-publication description** for the existing Zenodo record [10.5281/zenodo.24453186](https://doi.org/10.5281/zenodo.24453186). It updates the older RC.2 Skill-oriented text for the RC.4 plugin-only distribution. Do **not** create a new Zenodo version or DOI just to amend the text.

The description below is suitable for copying into the existing record's **Description** field through the Zenodo account's **Edit** interface. Updating GitHub alone does **not** automatically modify an existing Zenodo record.

---

**Meu Artigo** is an open-source, experimental ChatGPT plugin designed to assist researchers throughout the development of scientific articles, from defining research questions and selecting methodological strategies to reviewing literature, organizing evidence, preparing manuscripts, and documenting research decisions.

The plugin brings together methodological guidance, research workflow management, scientific governance, and evidence traceability. It is intended to support structured and transparent research while preserving human autonomy, academic responsibility, and accountability for consequential scientific decisions.

### Main Features

- **Methodological guidance:** Support for qualitative, quantitative, mixed-methods, conceptual and theoretical studies, literature reviews (including systematic, integrative, and bibliometric approaches), and design science research. Recommendations should follow the research question, evidence, and methodological requirements rather than impose a single research route.
- **Public methodological knowledge base:** The GitHub repository maintains **174 editorial guidance cards [I]/[P], 475 bibliographic prospecting cards [P], and 51 separately licensed academic PDFs**. The plugin can assist with selective, on-demand consultation when the ChatGPT environment provides authorized access and document-reading tools. Catalog entries are not treated as proof that their underlying publications were read. The academic PDFs are **not bundled with the installable plugin**.
- **Scientific governance:** Seven validation gates remain under the researcher's control. Completing an automated task, recording an event, or choosing an option does not constitute scientific approval.
- **Evidence traceability:** Explicit separation between literature actually examined **[L]**, interpretations or inferences **[I]**, and research proposals or original contributions **[P]**, supported by source provenance, decision records, counterevidence where available, and limitations.
- **Structured decisions:** Methodological alternatives can be presented as **A/B/C/D** options, showing benefits, limitations, and a contextual recommendation. Option D allows an alternative proposed by the researcher. Interactive controls depend on the host interface; no scientific gate is approved automatically.
- **Research workflow management:** The **C.A.D.A.** framework (*Capture, Assign, Define a deadline or next action, and Accompany with evidence*) supports the organization and follow-up of research activities.
- **Research continuity:** Project histories, documented decisions, research milestones, and authorized persistent records can support auditability and resumption of work **when appropriate storage tools and permissions are available**. Plugin installation alone does not enable Google Drive access, persistence, or synchronization.
- **Responsible AI use:** Instructions and checks aim to reduce fabricated references, unsupported claims, unverifiable research actions, unauthorized gate approvals, and confusion between retrieved evidence and generated suggestions.
- **Integrity and provenance:** Source identification, software-version records, archive checksums, and distinctions among bibliographic leads, editorial materials, and actual primary-source evidence.
- **Optional interoperability:** Use within ordinary ChatGPT conversations and ChatGPT Work where the plugin is available, with additional tools or integrations only when supported and explicitly authorized.

### Plugin-Only Distribution and Remote Knowledge Retrieval

Starting with **v1.0.0-rc.4**, Meu Artigo is distributed as **one ChatGPT plugin**, rather than as a standalone downloadable Skill. The scientific workflow instructions are incorporated **inside the plugin** as an internal component; users do not need to install a separate Skill.

The installable plugin package is available from the GitHub RC.4 release. The methodological knowledge base remains in the public GitHub repository and is consulted selectively when actual network retrieval and document-processing capabilities permit. This model avoids bundling the 51 third-party academic PDFs in the plugin and does not imply guaranteed online retrieval in every host.

GitHub provides the public source repository and the installable plugin archive. Zenodo provides a versioned archival record and a persistent DOI. The Zenodo GitHub-source snapshot is **not** the plugin installation package; use the dedicated RC.4 plugin ZIP attached to the GitHub release for installation.

### Intended Audience

Researchers, graduate students, academic professionals, research supervisors, and research teams seeking more structured, methodologically informed, transparent, and accountable assistance with scientific research and writing.

### Version and Validation Status

**Version:** v1.0.0-rc.4 — published **experimental plugin-only release candidate**, November 23, 2026.

**Development status:** Public experimental software. The release passed engineering checks, automated regression tests, and package-integrity verification. These checks do **not** establish independent empirical validation of research quality, scientific effectiveness, or productivity improvements. Full functionality can depend on the ChatGPT environment, available tools, external permissions, and verified access to research materials.

Meu Artigo does **not** replace researchers' methodological judgment, independent source evaluation, academic supervision, ethical responsibilities, editorial requirements, or peer review. All seven scientific validation gates remain under human control.

### Licensing, Sources, and Citation

**Software license:** Apache License 2.0.

**Third-party academic publications:** Retain their original copyright, attribution requirements, and applicable licenses. The public repository's 51 PDFs are not included in the plugin installation ZIP.

**Source code and documentation:** https://github.com/rebsonm/MeuArtigoSkill

**Official RC.4 GitHub release and plugin download:** https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.4

**Public methodological PDF library:** https://github.com/rebsonm/MeuArtigoSkill/tree/main/knowledge/methodology/pdfs

**RC.4 tagged source commit:** `01b63472711bc500eecd94bb9ad012f54bd210b3`

**Version DOI:** https://doi.org/10.5281/zenodo.24453186

**Author:** Rebson de Morais Mendes (citation form: **Mendes, Rebson de Morais**).

**Publication year:** 2026.
