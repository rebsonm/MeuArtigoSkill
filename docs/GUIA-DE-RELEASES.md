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
The last published version is determined by an **actual GitHub Release and
its uploaded ZIP and SHA-256**, never by `VERSION`, `date-released` or a
merge commit. All public versions remain **experimental prereleases**, not stable
or independently scientifically validated. The historical **beta.4 Pre-release was published** on 2026-10-11 (UTC) from commit
`3ef2bfb1f73c42cb029a2862b2c7959c12fe718f`, with an uploaded
versioned ZIP and `SHA256SUMS.txt`. The **beta.5 Pre-release was published** on 2026-10-14 (UTC) from source commit `267b4239a1aea1ec0d7a6fcf6ba1aa0607e90ccc`, with the versioned ZIP and `SHA256SUMS.txt` attached. At the time of beta.5 publication it was recommended; the current recommendation is **v1.0.0-rc.1** (2026-11-22), not a stable or independently validated release. Historical beta.1/beta.2 tags and
assets are retained.

## Beta.5 maintenance release (2026-10-14)

The beta.5 development line incorporates the initializer hotfix from [PR #62](https://github.com/rebsonm/MeuArtigoSkill/pull/62). It creates and validates essential local research documents before the optional XLSX, bounds the visual-generator execution, preserves prior researcher files and logs the matrix status independently. It does **not** establish that Google Drive data were synchronized or that the research method was scientifically validated.

The beta.5 manual publication workflow completed and its tagged GitHub Pre-release, installation ZIP and checksum were confirmed on 2026-10-14. For future versions, retain the same explicit confirmation and independent asset verification. Earlier beta.4 assets are immutable historical releases.

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

## Phase 6: offline bundle closure audit

The current Skill source is packaged by
`scripts/build_skill_bundle.py`, which calls the source-only
`scripts/bundle_dependency_audit.py`. Before writing the archive, it
checks that links directly navigated from `SKILL.md` are present and
that installed operational scripts do not import excluded source-only
Python modules. It parses all bundled Python files, checks the
fixed allowlist, and fails on missing local references rather than
producing an apparently usable ZIP with broken imports. Optional
external packages (for example openpyxl and xlrd) do not become
mandatory just because an offline metadata adapter exists.

The standalone bundle verifier independently checks allowed ZIP
entry structure, archive size/member limits, symlink/encrypted entries,
manifest membership, SHA-256 digests, syntax of installed Python
sources and accessible entrypoint links. These are *local source and
file-consistency checks*, not package signing, publisher authentication,
operational access to licensed databases, scientific validation or
independent installation tests in ChatGPT/Claude/Gemini. Verify the
separate published SHA256SUMS through the authenticated official release
page when actually installing an authorized public version.

```bash
python scripts/build_skill_bundle.py
python scripts/build_skill_bundle.py --verify "dist/MeuArtigoSkill-v$(cat VERSION).zip"
(cd dist && sha256sum -c SHA256SUMS.txt)
```

A CI-built ZIP on `main` is a **development artifact**, not automatically a GitHub release. RC.1 was separately published and verified on 2026-11-22.
After an authorized manual workflow publishes a *new* tagged beta, verify
its ZIP and checksum first, then update the official recommendation pointer
and user-facing download pages. This follow-up was completed for beta.5;
it did **not** replace or modify historical release assets.
The experimental beta label must be retained; a stable v1.0.0 would
require a separate decision. The redundant discovery of
15 Phase-5 unit tests was corrected; software regression counts are
not measures of scientific validity.

## Historical beta.6 release preparation (2026-10-15)

The maintainer authorized consolidating PR #70 into the final *planned* experimental beta.6 and documenting that status across the repository. This does **not** assert that beta.6 is stable or that the custom external-tool server and external-tool Apps UI have passed authenticated real-host acceptance. The existing manual workflow remains the only publishing route: merge the reviewed PR to `main`, dispatch **Publish beta (manual)** with `publish-beta` on the same UTC day recorded in `CITATION.cff`, then verify the tag, ZIP and SHA-256. Only after successful release verification may `OFFICIAL_SKILL_RELEASE` and download recommendations switch from beta.5 to beta.6. Do not silently update installed Skills or replace archived release assets.

## v1.0.0-rc.1 — published experimental prerelease (2026-11-22)

The [RC.1 GitHub prerelease](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.1) exists with the installable Skill ZIP, 51 attributed third-party PDFs in a separate archive, and matching SHA256SUMS. The [manual RC publisher](../.github/workflows/publish-rc1.yml) was used after CI checks; the beta-only workflow continues to reject release candidates. The version is experimental, not a stable v1.0.0, and its existence does not certify all host integrations.

The repository's current public recommendation is `OFFICIAL_SKILL_RELEASE=1.0.0-rc.1`. `VERSION` matches the released source; `CITATION.cff` and CHANGELOG use its real 2026-11-22 publication date. Keep original beta releases and old tags unchanged. The legacy `--candidate` metadata check is for historical *unpublished* RC fixtures; current CI must instead check published-source metadata without making network claims about installation.

The core CSV/Drive fictional-project run passed while optional XLSX failed for missing dependency. Earlier strict host T02 (151/153) and focused T32/T34 host routes are not fully accepted. The 51 PDFs retain their own licenses and attributions; issues #102/#103 concern historical Git references and remain tracked. Do not infer independent scientific approval of any card or gate.

For future versions, create a new version number and new authorized release rather than overwriting the immutable `v1.0.0-rc.1` tag or assets. Main-branch source documentation may evolve, but it must not falsely describe an already published release as unpublished.
