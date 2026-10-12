# GitHub Wiki publishing — maintainer runbook

## Purpose and status

The project keeps the proposed GitHub Wiki pages in `wiki/*.md` for code review, auditable authoring and synchronization with the versioned scientific contract.

**Important:** GitHub's native **Wiki** tab is backed by a **separate Git repository** (`MeuArtigoSkill.wiki.git`). Committing pages to this main repository or merging this documentation PR does **not** publish the live Wiki automatically. The connected GitHub REST integration does not provide a native Wiki-write endpoint.

## One-time initialization

1. Visit [the native GitHub Wiki](https://github.com/rebsonm/MeuArtigoSkill/wiki) while signed into an account with edit rights.
2. If the Wiki has no Home page, create an initial `Home` page using the web editor and save it. This initializes the separate Wiki repository.
3. Before publishing, check for preexisting Wiki edits and reconcile them against the proposed source mirror.

## Publishing without destructive history changes

On an authorized machine with Git and appropriate GitHub authentication:

```bash
git clone https://github.com/rebsonm/MeuArtigoSkill.wiki.git MeuArtigoSkill-wiki
cd MeuArtigoSkill-wiki
# Inspect existing pages and history; merge rather than overwrite user edits.
```

Copy the **reviewed** Markdown files from the project's `wiki/` folder into the root of the Wiki clone. Include `Home.md`, `_Sidebar.md`, `_Footer.md` and the topical pages. Do not copy `docs/WIKI-PUBLISHING.md` into the live Wiki.

```bash
git status
git diff --check
git diff
git add -- '*.md'
git commit -m "docs(wiki): publish Meu Artigo researcher guide"
git push origin HEAD
```

Only the Wiki's default branch is published. Check the Wiki's actual default branch before pushing; avoid force-push and do not overwrite newly edited pages without reconciliation.

## Verify the result

1. Open `https://github.com/rebsonm/MeuArtigoSkill/wiki`; ensure the landing page and sidebar render.
2. Follow every Wiki-to-Wiki link, check release ZIP links and official-document references.
3. Verify the current release wording against the **actual tagged GitHub release**, not just `VERSION`.
4. Review public pages for sensitive information, third-party copyrights and false validation claims.
5. Record the Wiki commit and responsible publisher in the maintenance history.

## Maintenance policy

- Prefer a main-repository PR for content changes and scientific accuracy review.
- Publishing source-to-Wiki remains an **explicit separate maintainer action**.
- The Skill package does not automatically include or deploy Wiki changes.
- Never enable a silent auto-publish process or grant broad Wiki permissions merely to simplify documentation.
- If the live Wiki diverges from `wiki/`, reconcile content and history before synchronizing.
