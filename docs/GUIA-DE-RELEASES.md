# Releases and versioning — secure maintainer procedure

The repository uses **Apache License 2.0** with original author attribution
preserved in `NOTICE`. Publishing a software release is **not evidence**
that research results, methodology or operational benefits have been
scientifically validated.

## Separate CI and publishing responsibilities

1. **Release audit** (`.github/workflows/release-audit.yml`) runs on
   pull requests and pushes to the main branch. Its required
   check remains named `audit`. It checks software regression tests,
   copyright/privacy controls, documentation, provenance and bundle
   integrity with `contents: read`. It cannot publish releases.
2. **Publish beta (manual)** (`.github/workflows/publish-beta.yml`)
   runs only through **Actions → Publish beta (manual) → Run workflow**
   on `main`. The maintainer must type `publish-beta`. This job
   rechecks all safety controls before receiving the write permission
   needed for release creation. It will not overwrite existing tags.
3. **English-source completeness:** the manual workflow additionally
   runs `python scripts/audit_source_language.py --strict`.
   An English-source release must not ship while the repository
   still contains substantial untranslated Portuguese prose.

## Prepare a new release safely

1. Work in a development branch, recording **actual implemented**
   changes in the `Unreleased` CHANGELOG section.
2. Write accurate notes at
   `docs/NOTAS-DA-VERSAO-<version>.md`. Document real
   capabilities and limitations; do not invent participants,
   results, corpus sizes, validation or scientific benefit.
3. Once ready to release, update the **single canonical `VERSION`**
   identifier. A code-only candidate may have its own version identifier,
   but do not call it a published release until the manual publication
   workflow creates and verifies the corresponding GitHub assets.
4. Synchronize README, citation version/date and historical
   changelog metadata:

   ```bash
   python scripts/sync_version.py --date YYYY-MM-DD
   ```

   An unpublished source candidate may omit `date-released` from `CITATION.cff`.
   Populate it only during authorized release preparation, with the
   actual publication date rather than a development commit date.

   Verify the **actual publication date** when issuing a release and
   ensure citation metadata reflect it; preparing candidate metadata
   ahead of time does not establish a published date. The script must
   not manufacture a scientific narrative or initiate publishing.

5. Run engineering, documentation, source-language and package checks
   locally or in an authorized CI environment:

   ```bash
   python scripts/release_audit.py
   python -m unittest discover -s tests -v
   python scripts/check_documentation_links.py
   python scripts/audit_public_docs.py
   python scripts/audit_source_language.py --strict
   python scripts/smoke_test_provenance.py
   python scripts/build_skill_bundle.py
   ```

   Before starting the manual publication workflow, verify that the
   release notes no longer describe the version as an unpublished candidate,
   `CITATION.cff` carries the actual publication date, and README links
   explicitly to the version being published. The manual workflow will
   fail closed if these documentary conditions are not met:

   ```bash
   python scripts/check_release_metadata.py --require-today
   ```

6. Open a pull request and require the `audit` check to pass.
   Review version metadata, license, author attribution,
   package source, source-language completeness and public notes.
   Merge into `main` only after applying the repository's actual,
   verified review and branch-protection requirements.
7. Manually dispatch `Publish beta` from `main` and enter the
   required confirmation. Inspect the newly created immutable
   release, `MeuArtigoSkill-v<version>.zip`, SHA-256 digest and
   `SHA256SUMS.txt` attachment.

**Merging source code does not automatically publish it.**
The last published version is determined by an actual GitHub Release, not
by `VERSION` or a merge commit. The **official public Skill recommendation** is `v0.9.0-beta.1` with its
prepared release ZIP. Later `v0.9.0-beta.2` remains a historical prerelease;
`main` is separate unreleased development source. A newer published tag does
not change the official recommendation automatically. No tags or assets are
deleted by this decision. Historical rights and downloads remain intact.

## Platform and language compatibility

The repository is authored in English, while installed
researcher-facing conversations follow the researcher's
language automatically; see
[language policy](../references/language-policy.md).
Manuscript language follows the actual journal or researcher's
independent decision. Software checks do not establish
correct real-world cross-platform language behavior.

## Security and publishing limits

- Pin external GitHub Actions to reviewed immutable commit SHAs.
- Routine audits are read-only. Manual release creation has
  minimal explicit write permissions; checkout credentials
  are not persisted unnecessarily.
- The source-language scanner is a conservative heuristic,
  not human semantic review or a certified translation process.
- Public document checks may identify accidental personal
  or project provenance, but cannot prove exhaustive redaction
  or erase information in Git history.
- Private full text, institutionally licensed PDFs and
  participant documents do **not** inherit the software's
  Apache-2.0 license.
