# Getting started with Meu Artigo on GitHub

## Public access and experimental status

Meu Artigo is an **experimental public beta**. Its source and project
documentation can be consulted without an invitation or a GitHub
account. Download and installation do not grant permission to
redistribute third-party research PDFs or claim that the Skill has
been scientifically validated.

This guide is designed for researchers who have **never used GitHub**.
You do not need programming skills, Git, a command line, or a pull request
to use the published installer.

## 1. What this repository contains

A GitHub repository is a project folder with a public change history.
Here it includes the main `SKILL.md` instructions, methodological
references, helper scripts, platform guides, public-beta installation
notes, the C.A.D.A. management layer and license/attribution records.

The automatically displayed `README.md` introduces the project
rather than reproducing all technical documentation.

## 2. Do I need a GitHub account?

Not to read, inspect or download a public release. You may need
a GitHub account to contribute, create issues or collaborate.
Connection to third-party apps or academic sources is a **separate**
authorization process and may require a different account.

## 3. Choose the installable release ZIP

Open the [published beta release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.8.0-beta.8),
then download the specifically prepared
`MeuArtigoSkill-v0.8.0-beta.8.zip` attachment. Verify its SHA-256
digest using `SHA256SUMS.txt` if appropriate.

**Do not confuse** that installable ZIP with GitHub's automatically
generated `Source code (zip)` archive. The published Skill ZIP
has the expected installation layout and a validated manifest.

The downloaded package contains a tree similar to:

```text
MeuArtigoSkill/
├── SKILL.md
├── agents/
├── references/
├── scripts/
├── docs/
└── README.md
```

When the platform permits ZIP import, retain the entire package
so reference documents remain available. Only unpack if you want
to inspect contents or your platform requires a directory.

## 4. Which file matters?

`SKILL.md` is the Skill entrypoint. The `references/` folder
contains detailed method and process guidance; `scripts/` contains
deterministic helper programs; `agents/` contains optional adapters
for particular products. The `docs/` folder includes installation,
limits, provenance, scientific safeguards and source-licensing policy.

You **do not** need to read or understand every file to begin.
The Skill follows a progressive approach, opening relevant
instructions only when that research stage actually requires them.

## 5. Choose your AI platform

The Skill's scientific contract is shared, but specific installation
and execution capabilities vary by account and product:

- [ChatGPT / Codex](./CHATGPT.md)
- [Claude / Claude Code](./CLAUDE.md)
- [Gemini](./GEMINI.md)

Consult the [compatibility matrix](COMPATIBILIDADE-PLATAFORMAS.md)
to distinguish vendor features from Meu Artigo actions
that have actually been evaluated.

## 6. Start in your own language — automatically

**The repository is written in English; you do not have to be.**

If your account supports installing Skills, import the full ZIP
following the platform guide. Open a new conversation and describe
the research problem **in your usual language**.

Examples of what a researcher might say, without any language pack:

- A Portuguese-speaking researcher may directly describe the study
  in Portuguese, and the assistant should respond in Portuguese.
- A Spanish-speaking researcher may begin in Spanish and receive
  Spanish explanations.
- An English-speaking researcher may begin in English and receive
  English responses.

If you prefer a specific language, state it directly in the
conversation. The **manuscript language is independent**: you can
discuss the project in Portuguese while preparing the paper in
English for an international journal. See the
[language policy](../references/language-policy.md).

The Skill may ask for the *research problem* and whether you have
a *target journal* with official author rules and a template.
You are not expected to prepare your own Boolean search strings,
spreadsheets, evidence matrix, deduplication logic or complete
research protocol before the first interaction.

## 7. Storage is an explicit prerequisite

Before substantive literature searching or drafting, the Skill
checks whether Google Drive is connected and **actually writable**.
Drive is the standard canonical location for the project's
continuity, research documents, protocols, matrix and manuscript.

If Drive is unavailable, the Skill should explain how to connect it
and check again. If access still fails, the assistant must ask
whether you **explicitly authorize** an alternative local/Work
workspace. Without your affirmative decision, it must not pretend
that files were saved to Drive or begin substantive research in
a default local workspace.

## 8. Research workflow and decisions

Once authorized storage is available, the Skill should preserve
the original question, propose method-appropriate options and
organize source searches, analysis and writing according to the
actual research design. A bibliographic literature review has
different controls from a qualitative interview study, a
quantitative analysis or design science evaluation.

The management method C.A.D.A. tracks responsibilities, the next
task and deadlines without replacing scientific decisions.

When producing material for journals, reviewers or external
collaborators, follow the journal's verified instructions and
the [anonymization policy](./ANONIMIZACAO.md), including visible
and hidden document metadata, source rights and truthful AI-use
disclosure.

An external management app such as ClickUp, Jira or Trello is
optional. The default canonical matrix can manage the project
without these services.

## 9. Check continuity of your research project

The assistant should preserve a real, updated `CONTINUIDADE.md`,
original research input, material decisions, pending scientific
gates, progress and the next valid action in the authorized
workspace. To resume in another session, ask to continue the
existing article and inspect the actual persistent state rather
than recreating the project from a guessed conversation history.

Successful local generation is **not** proof that a Google Drive
upload occurred. Ask for the verifiable source when there is doubt.

## 10. Updating to a newer version

Check the [Releases page](https://github.com/rebsonm/MeuArtigoSkill/releases)
and choose the version's prepared ZIP. Review its release notes,
the [CHANGELOG](../CHANGELOG.md) and any migration requirements.
Keep the research project's real source files and canonical
records; installing a newer Skill must not silently rewrite
earlier scientific decisions.

## 11. If you want to explore GitHub

- **Repository:** project and development history.
- **README.md:** plain-language project overview.
- **Release:** an immutable named distribution with notes.
- **Source code archive:** a repository copy that may differ from
  the tested Skill installer.
- **Issue:** a report or discussion about a problem.
- **Pull request:** a proposed change requiring review/checks.
- **Commit:** a recorded source revision.

## 12. Feedback, support and further reading

You can inspect the files, use a supported beta installer,
or report confusing behavior and evidence problems through the
repository's issue and contribution mechanisms.

See [contributing](../CONTRIBUTING.md), [security](../SECURITY.md),
[release details](IMPLANTACAO-BETA.md), and the
[method-specific guides](ROTAS-METODOLOGICAS.md).
Neither a successful installation nor a completed software
audit guarantees academic publication or scientific quality.
