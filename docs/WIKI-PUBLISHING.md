# Native GitHub Wiki publication — maintainer runbook

## Source and live Wiki

The reviewed 15 Markdown pages live under the main repository's wiki/ directory.
The native Wiki tab is backed by a separate Git repository: MeuArtigoSkill.wiki.git.
Merging files into main/wiki/ alone never publishes the native Wiki.

The maintainer created the first native Home page on October 12, 2026,
with the short placeholder text "# Meu Artigo". This initializes the Wiki Git repository.

## Approved one-time bootstrap

[Publish Wiki (bootstrap and manual)](../.github/workflows/publish-wiki.yml)
performs an initial publication when the workflow file itself is first
added to main. This particular bootstrap was requested by the maintainer
after initializing the Home page. The workflow also provides a manual
Run workflow option for future explicitly authorized publications.

The workflow:
- Uses a short-lived GITHUB_TOKEN with job-scoped contents: write permission.
- Uses an immutable SHA-pinned checkout action and does not persist checkout credentials.
- Checks the existing Home and copies 15 reviewed Wiki Markdown pages into the Wiki Git root.
- Refuses to replace independently edited pages. The sole exception is the
  exact initialized placeholder Home with content "# Meu Artigo".
- Uses an ordinary fast-forward Git push (never force-push), does not remove unrelated files,
  modify Skill code, touch a beta release or alter canonical research records.
- Does not automatically publish future changes to wiki/*.md.

The workflow can fail if repository policy blocks GITHUB_TOKEN write,
the Home page has diverged, a concurrent Wiki edit occurred, or Wiki Git
authentication is unavailable. Its presence in main or a green Release audit
is not proof of actual native Wiki publication.

## Verify or rerun

1. Check the dedicated Publish Wiki GitHub Actions workflow for a successful run.
2. Open https://github.com/rebsonm/MeuArtigoSkill/wiki and confirm Home
   contains the introduction and that sidebar and footer actually render.
3. Navigate between all 15 Wiki pages. Verify the release links and
   that the current version is described only as an experimental public beta.
4. Confirm existing unrelated Wiki edits and the history were preserved.
5. If needed, a maintainer can select Actions -> Publish Wiki -> Run workflow
   on main. If a page mismatch is reported, reconcile edits manually first.

## Manual alternative

With appropriate GitHub Git authentication, clone
https://github.com/rebsonm/MeuArtigoSkill.wiki.git, inspect the current
pages and history, copy only the reviewed Markdown files from main/wiki/
into that clone's root, review the diff, commit, and push normally.
Never force-push or silently overwrite community edits.

## Maintenance policy

Review source updates through a Pull Request first. Subsequent native Wiki
publishing remains an explicit manual action; avoid unconditional auto-sync.
The primary scientific contract remains SKILL.md; Wiki changes do not
automatically update the installed Skill or the published release.
