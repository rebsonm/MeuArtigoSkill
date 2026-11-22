# Preparing an auditable Meu Artigo copy for a future Zenodo version

**Status: deposit-preparation documentation, NOT a Zenodo publication.**

## Canonical public source and existing citation

- Repository: https://github.com/rebsonm/MeuArtigoSkill
- Existing software DOI cited by the project: https://doi.org/10.5281/zenodo.24397699
- Last verified GitHub release: experimental `v1.0.0-rc.1`, published
  22 November 2026 from an **earlier** source commit.
- Subsequent public documentation and methodology-card corrections have
  been merged into `main`. They do **not** alter the already published
  RC.1 installer ZIP, its checksums or the immutable release tag.
- A source-code snapshot prepared from a newer commit is **not an installable
  Skill package** and must not be described as `v1.0.0-rc.1` or as a new
  stable `v1.0.0` release.
- See [current release](CURRENT-RELEASE.md), [citation](../CITATION.cff),
  [rights-holder notice](../RIGHTSHOLDER-NOTICE.md) and
  [English correction report](ALL-MARKDOWN-LANGUAGE-STATUS.md).

## Source snapshot and checksums

The workflow `.github/workflows/prepare-zenodo-copy.yml` prepares one
**public-source-only** ZIP from an exact Git commit on `main`, together
with file-level SHA-256 checksums and source-commit metadata. The archive
excludes the 51 third-party PDF binaries; the publishers' original PDF
links and the independent rights/attribution register remain in the source.

An archive prepared this way is a reviewable copy for a **future Zenodo
version**. Its inclusion of code, methodological notes, archived intake
records, and original card metadata does not mean the content has passed
independent methodological peer review. The original sources and
rights-holder contact pathway remain accessible.

Before depositing, verify that the workflow succeeded and record the
exact ZIP SHA-256, source commit, file count, and excluded-file count.
Inspect the generated manifest, check archive contents and sample the
documents; **do not rely on the file name alone**.

## Updating an existing Zenodo record responsibly

Zenodo distinguishes a **concept DOI** (all versions) from
**version-specific DOIs**. Do not assume the existing project DOI is the
new version DOI or silently overwrite an immutable archived release.

1. Check whether the existing Zenodo record is linked to GitHub releases
   and whether its displayed DOI is the concept DOI or a version DOI.
2. Choose **one** update path: use Zenodo's *New version* operation with
   the reviewed source ZIP, or create an intentionally versioned GitHub
   release if a verified active GitHub–Zenodo integration will archive it
   automatically. Avoid two deposits for the same version.
3. Identify the exact captured Git commit and archival package type.
   Mark a source snapshot as a development/experimental archival copy,
   not an installer or a validated scientific article.
4. Review title, author, description, date, version, Apache-2.0 license,
   related identifiers, exclusions and [rights-holder requests](
   ../RIGHTSHOLDER-NOTICE.md). Metadata for the future deposit is in
   [the draft JSON](zenodo-metadata-draft.json).
5. Verify Zenodo's resulting record, DOI, downloaded bytes, checksum,
   version relationship and published date. Update the project's citation
   metadata **only after** an actual new archival version is verified.

**No Zenodo upload, new DOI, release tag or Skill package is created by
writing this guide or by generating the archival ZIP.**

Zenodo reference: https://zenodo.org/help/versioning
