# Meu Artigo

**A scientific writing Skill that helps researchers plan, organize and develop manuscripts with AI while preserving source traceability and human responsibility for scientific decisions.**

Meu Artigo supports the journey from an initial research idea to a submission-ready manuscript. Rather than treating a paper as disconnected AI prompts, it maintains a continuous workflow with verified sources, documented progress, pending decisions, journal requirements and resumable research state.

The project is available in a **public GitHub repository** as an **experimental beta**.

**Current version:** `0.9.0-beta.1` · [Releases and downloads](https://github.com/rebsonm/MeuArtigoSkill/releases). The source code is free; third-party academic databases, platforms and subscriptions may have separate access requirements.

**[Get the beta](https://github.com/rebsonm/MeuArtigoSkill/releases) · [Installation guide](./docs/COMECE-AQUI.md) · [Getting started](#getting-started)**

## English source, your language when you use it

**The repository and its instructions are authored in English. This does not mean you must speak English.** The installed Skill follows the researcher's conversational language automatically and respects any explicit language choice. It can answer Portuguese questions in Portuguese, Spanish questions in Spanish, and English questions in English — without changing its source code or installing a translation pack.

The **manuscript language is chosen separately** according to the researcher's instructions or the selected journal's author guidelines. You may communicate in Portuguese while preparing an English-language article. Machine-readable identifiers, source citations and original quotations are not silently translated. See the [interaction language policy](./references/language-policy.md).

## What you can do

- **Turn an idea into a research project:** delimit the problem, formulate questions, organize objectives and define the intended contribution.
- **Choose a suitable research design:** theoretical and conceptual studies, reviews, qualitative, quantitative and mixed-method approaches, or design science, subject to researcher decisions.
- **Organize bibliographic research:** design searches, record actual retrieval, track duplicates and document human selection decisions when needed.
- **Use sources responsibly:** check bibliographic identity, distinguish consulted passages from metadata-only records and record supporting evidence and limitations.
- **Develop arguments:** link statements to sources, distinguish literature [L], inference [I] and original proposals [P], and consider counterevidence.
- **Write and prepare the manuscript:** follow real journal instructions, apply relevant anonymization and disclose actual AI assistance.
- **Resume work safely:** preserve authorized project state between sessions without inventing earlier actions.
- **Track responsibilities and deadlines:** use C.A.D.A. to show the next task and outstanding decisions.

Specific functions depend on the AI platform, the tools actually connected, institutional database access and lawful availability of sources.

## C.A.D.A. — operational research workflow management

Meu Artigo uses **C.A.D.A.** (*Capturar, Atribuir, Definir prazo, Acompanhar*) for documenting and following through on administrative research tasks. The name is maintained as a proper name; in English, its four stages mean **Capture, Assign, Set a deadline and Follow up**.

| Stage | Practical meaning |
| --- | --- |
| Capture | Record a relevant task or open issue |
| Assign | Identify responsibility for completing or deciding |
| Set a deadline | Record a realistic due date or dependency |
| Follow up | Track progress and document completion |

C.A.D.A. supports **operational management**. It does not replace research methods, critical source appraisal, researcher judgment or scientific validation.

## Optional in-chat visual dashboard

The experimental [Meu Artigo Visual](docs/MEU-ARTIGO-VISUAL.md) is a
read-only MCP Apps companion to the Skill. It can display tasks, next actions,
scientific review gates and evidence-register counts in a conversational
interface when a compatible host and authorized MCP server are configured.
It does **not** auto-install with the Skill, access Google Drive on its own,
change research decisions, or claim that registered actions were externally
verified. A compact CLI/text view works without MCP Apps.

## How it works

1. **Describe your research idea** in your usual language.
2. **Agree on the research direction** with method-specific guidance and explicit human decisions at consequential steps.
3. **Build a traceable workspace** with sources, justified actions, evidence and next steps in an authorized persistent store.
4. **Retain scientific responsibility.** The assistant may propose alternatives, but the researcher decides the design, interpretation and approval.
5. **Prepare and review the paper** according to the chosen journal's verified rules and the actual scientific evidence.

## Getting started

1. Go to [Releases](https://github.com/rebsonm/MeuArtigoSkill/releases) and choose the latest published beta's **installable ZIP**, not the automatically generated repository source archive.
2. Follow the [installation and first-use guide](./docs/COMECE-AQUI.md) for your AI platform.
3. Start a conversation using your own language and describe the research problem. For example, in English: *“I want to write a research article about difficulties in AI adoption in small public organizations. Help me develop the research question and organize the workflow.”* Equally, Portuguese and Spanish requests work under the same language policy.

Platform guides: [ChatGPT](./docs/CHATGPT.md) · [Claude](./docs/CLAUDE.md) · [Gemini](./docs/GEMINI.md)

Importing a Skill does not confirm authenticated Google Drive access, direct Scopus/Web of Science access or the ability to execute Python in the current platform. The project must verify each capability before treating the corresponding action as completed.

## Who is this for?

Undergraduate and graduate students, researchers, faculty and professionals preparing academic manuscripts, literature reviews and structured scientific studies. It also supports teams resuming existing projects and retrieving actual prior scientific decisions.

## Research integrity and limitations

**Meu Artigo assists research; it does not replace the researcher.** It must not fabricate references, data, source access, executed searches, peer review, human decisions or findings. Verified bibliographic metadata does not by itself support a claim's interpretation. Source consultation, interpretation and empirical results have separate evidence requirements.

Full-text use must respect copyright and access conditions. Any AI disclosure must reflect actual assistance and the journal's instructions.

**This is an experimental beta.** Engineering tests have been run, but independent empirical evidence of scientific article quality, effectiveness and productivity improvements is still pending. No manuscript publication or editorial acceptance is guaranteed.

## More information

- [Getting started](./docs/COMECE-AQUI.md)
- [First-use checklist](./docs/CHECKLIST-PRIMEIRO-USO.md)
- [Development history](./CHANGELOG.md)
- [How to cite this software](./CITATION.cff)
- [License](./LICENSE)
- [Contributing and reporting problems](./CONTRIBUTING.md)
- [Automatic conversation language](./references/language-policy.md)

The project's current code and original documentation are distributed under the **Apache License 2.0**, retaining original author attribution in [NOTICE](./NOTICE). Applicable license and modification notices must be preserved. The scholarly software citation in `CITATION.cff` is recommended, not a condition imposed by Apache-2.0. Earlier MIT-licensed versions retain previously granted rights. The code license does not cover unrelated third-party research documents or PDFs.
