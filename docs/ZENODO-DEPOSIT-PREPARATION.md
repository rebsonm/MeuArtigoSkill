# Zenodo version records and preparing auditable source snapshots

**Status:** The maintainer provided a new Zenodo RC.2 software DOI,
[10.5281/zenodo.24450459](https://doi.org/10.5281/zenodo.24450459).
The workflow discussed below still creates a separate **source-review
artifact, NOT a Zenodo publication**. This documentation change does not
create or update any Zenodo deposit.

## Canonical public source and version-specific citations

- Repository: https://github.com/rebsonm/MeuArtigoSkill
- Zenodo experimental **RC.2** software DOI (reported by maintainer):
  https://doi.org/10.5281/zenodo.24450459
- Earlier Zenodo DOI retained for the historical citation:
  https://doi.org/10.5281/zenodo.24397699
- These are version references, not a confirmed concept-DOI mapping;
  check Zenodo's version panel before claiming a verified relationship.
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
with file-level SHA-256 checksums and source-commit metadata. That **source
snapshot ZIP only** excludes the 51 third-party PDF binaries. **None of the
PDFs are deleted or removed from GitHub.** The live Skill uses on-demand
GitHub consultation; the original PDFs, publisher links and separate
rights/attribution register remain in the public source repository.

An archive prepared this way is a reviewable copy for a **possible future Zenodo
source snapshot**; it is not the already-archived RC.2 distribution. Its inclusion of code, methodological notes, archived intake
records, and original card metadata does not mean the content has passed
independent methodological peer review. The original sources and
rights-holder contact pathway remain accessible.

Before depositing, verify that the workflow succeeded and record the
exact ZIP SHA-256, source commit, file count, and excluded-file count.
Inspect the generated manifest, check archive contents and sample the
documents; **do not rely on the file name alone**.

## Preparing a subsequent Zenodo record responsibly

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
   [the draft JSON](../zenodo/metadata-draft.json).
5. Verify Zenodo's resulting record, DOI, downloaded bytes, checksum,
   version relationship and published date. Update the project's citation
   metadata **only after** an actual new archival version is verified.

**The RC.2 DOI above was supplied by the maintainer; its record was not
independently retrieved through the public Zenodo API in this update.**
No additional Zenodo upload, DOI, release tag or Skill package is created by
writing this guide or generating the separate source-review ZIP.

Zenodo reference: https://zenodo.org/help/versioning

**Reproduction:** a maintainer can run
`python scripts/build_zenodo_review_copy.py --output /tmp/zenodo-review`
in a checked-out public commit. The generated package includes `READ-FIRST-ZENODO.txt`,
`ZENODO-REVIEW-COPY-MANIFEST.json`, `SHA256SUMS-zenodo-review.txt` and the
source ZIP. The GitHub Actions workflow uploads these four files together as a
90-day review artifact; an artifact download does not itself update Zenodo.
