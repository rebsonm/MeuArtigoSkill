# Contributing and maintaining the Wiki

This Wiki is an **orientation layer** over versioned project documentation; it does not override [SKILL.md](https://github.com/rebsonm/MeuArtigoSkill/blob/main/SKILL.md) or the researcher's canonical project files.

## Ways to contribute

- Report installation or reproducible behavior problems through [Issues](https://github.com/rebsonm/MeuArtigoSkill/issues).
- Propose corrections to documentation, explicit methodology limits, examples and links.
- Submit code changes through a pull request against the project repository, following [CONTRIBUTING.md](https://github.com/rebsonm/MeuArtigoSkill/blob/main/CONTRIBUTING.md).
- Share sanitized beta testing observations following the [beta reporting guide](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/TESTE-BETA-PESQUISADORES.md).

Never include passwords, private Drive contents, identifiable research participants, restricted PDFs or unverifiable claims of human approval.

## Editorial rules for Wiki pages

1. Match the real published release, not an unpublished `main` candidate.
2. Link to primary, versioned reference documents for technical detail.
3. Clearly separate **implemented software behavior**, **proposed design**, **tested capability** and **pending validation**.
4. Keep the researcher as final authority over consequential scientific decisions.
5. Avoid implying that GitHub Wiki changes automatically update the installed Skill or its releases.
6. Preserve internal Wiki page names and sidebar navigation when reorganizing.

## How pages are maintained

The proposed source mirror lives in the main repository's `wiki/` folder. The **live GitHub Wiki is a different Git repository** at `https://github.com/rebsonm/MeuArtigoSkill.wiki.git`; changes in `wiki/` do not publish themselves.

To initialize and publish the native Wiki, a maintainer with GitHub credentials first creates the Wiki Home page using GitHub's Wiki interface and then follows [the maintainer publication instructions](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/WIKI-PUBLISHING.md) once those instructions are merged into `main`. Review pages before every update; never force-push over community edits. This mirror is meant to provide an auditable source and readable revision history, not an automatic deployment claim.

**Attribution:** [LICENSE](https://github.com/rebsonm/MeuArtigoSkill/blob/main/LICENSE) · [NOTICE](https://github.com/rebsonm/MeuArtigoSkill/blob/main/NOTICE) · [CITATION.cff](https://github.com/rebsonm/MeuArtigoSkill/blob/main/CITATION.cff).
