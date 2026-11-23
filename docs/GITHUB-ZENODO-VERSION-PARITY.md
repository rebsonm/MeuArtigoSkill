# GitHub–Zenodo RC version and source-identity lock

## Publication rule

For **every future release candidate**, require a one-to-one identity:
**GitHub tag `vX.Y.Z-rc.N` = `VERSION` `X.Y.Z-rc.N` =
top-level `CITATION.cff` version = preferred-citation version (if
present) = Zenodo version `X.Y.Z-rc.N`**. The code archived in Zenodo
must resolve to the exact **GitHub release tag source commit**.
A version-specific DOI is expected to differ numerically from the
software version: it uniquely identifies that version's Zenodo record.
Neither a DOI nor a GitHub tag is proof that two packages contain the
same code. A GitHub Skill installer and Zenodo's repository snapshot
need not have the same bytes or SHA-256 unless they are the same package
type; do not compare unlike archives as if they were identical.

**Do not use a development merge as a release**, reassign an existing
release tag, fabricate a retrospective RC.2 GitHub release, overwrite
a published archive, or create a second Zenodo deposit for the same
version just to make identifiers appear aligned.

## Present discrepancy and audit limitation

On 2026-11-22, the GitHub release listing showed **v1.0.0-rc.1** as
the latest published RC, with an immutable installer and assets.
The maintainer separately reported Zenodo DOI
[10.5281/zenodo.24450459](https://doi.org/10.5281/zenodo.24450459)
as **RC.2**. The project currently has `VERSION=1.0.0-rc.1`,
top-level `CITATION.cff` RC.1 and its `preferred-citation` RC.2.
This *documents a mismatch of publication channels*, but does **not**
prove identical or different code. Zenodo's own record files,
source-commit provenance and version chain remain to be independently
checked before any historical reconciliation.

Do not relabel RC.1 as RC.2, or make a new GitHub RC.2 release,
without verified exact code and publication evidence. Existing
Zenodo references must remain reachable and historically accurate.
When preparing a future release, use a new unused version and fix
candidate metadata **before** publishing; do not invent a DOI.

## Two-stage offline evidence gate

1. **Before publishing a new GitHub RC:** check out the exact candidate
   source commit, set the intended `VERSION` and matching
   `CITATION.cff` versions, and run:

   ```bash
   python scripts/check_github_zenodo_parity.py preflight --tag v1.0.0-rc.3
   ```

   This blocks mismatched source version, tag or preferred citation.
   Also run the usual full CI, publication rights checks and a real
   GitHub check that the intended tag/release does not already exist.
   Do not interpret an offline preflight as a live GitHub check.

2. **After the GitHub release is actually published and Zenodo has
   archived it:** obtain *real* GitHub release/tag information and
   Zenodo version-specific DOI plus archived-source commit provenance.
   Place verified values in two temporary evidence JSON objects:

   ```json
   {
     "tag": "v1.0.0-rc.3",
     "version": "1.0.0-rc.3",
     "source_commit": "<observed full 40-character Git SHA>",
     "archive_kind": "github-source",
     "archive_sha256": "<observed checksum, if applicable>"
   }
   ```

   ```json
   {
     "version": "1.0.0-rc.3",
     "version_doi": "10.5281/zenodo.<real record id>",
     "source_commit": "<independently verified archived source Git SHA>",
     "archive_kind": "github-source",
     "archive_sha256": "<observed checksum, if applicable>"
   }
   ```

   Run `python scripts/check_github_zenodo_parity.py reconcile
   --github-evidence /path/github.json --zenodo-evidence /path/zenodo.json`.
   The exact `source_commit` and matching software version are mandatory.
   If the archive lacks a trustworthy commit manifest, report
   **NOT_VERIFIED** and inspect actual archived content instead of
   guessing a commit from the title or DOI.
   Verify SHA-256 equality when comparing *the same package kind*;
   different ZIP kinds are not directly hash comparable.

**Scope and limitation:** The script validates supplied evidence for
internal consistency only, not its external authenticity. Real GitHub
and Zenodo records must be opened and verified separately. None of
these checks authenticate a researcher, auto-approve scientific gates,
publish software, change GitHub tags, alter Zenodo records, or prove
scientific validation.

## One publication trigger

Enable GitHub–Zenodo repository integration once in the Zenodo account.
A GitHub **release publication**, not an ordinary push/merge or
the `Sync now` repository-list refresh, triggers automatic archiving.
Avoid additionally depositing that same release manually, which may
create a second DOI series. Keep the GitHub release tag, Zenodo version
field, provenance and `CITATION.cff` in sync.

Reference: https://help.zenodo.org/docs/github/
