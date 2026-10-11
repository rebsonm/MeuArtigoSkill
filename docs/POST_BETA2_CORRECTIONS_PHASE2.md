# Post-beta.2 corrective maintenance — Phase 2 engineering notes

Status: unreleased maintenance branch; original beta.2 release and installed ChatGPT plugin are unchanged. These notes concern software tests only, not independent scientific validation.

## INC-002 / COR-01 — bibliographic ingestion

`scripts/dedupe_records.py` now validates the actual recognized source schema before generating a canonical export. Accepted minimum identity is a syntactically valid DOI, a title with author and year, or a title with a recognized persistent external identifier (OpenAlex, PMID or arXiv). A missing DOI alone is never grounds for exclusion. Unknown columns, malformed rows and incomplete identity cannot silently enter the canonical output.

- `import_diagnostics.json`: structured source-level errors, counts and summary.
- `rejected_records.csv`: source file/row, rejection code and bounded raw record for local quarantine.
- `consolidated_exact_dedup.csv`: valid canonical rows; original `Record_ID` and `Search_ID` preserved, alongside `_merged_Record_IDs`, `_merged_Search_IDs` and `_source_locations` for merged origins.
- `exact_duplicate_audit.csv`: includes both original and canonical Record/Search IDs.
- `near_duplicate_review.csv`: unchanged review-only semantics; fuzzy similarity never triggers automatic removal.

A file with no valid records exits with code 2 and does not create a successful canonical CSV. A file containing both valid and invalid rows can exit 0 with rejected rows explicitly counted. Both are deliberate contracts. An older test expecting title-only rows to remain canonical was updated with this documented migration. Re-running imports does **not** rewrite historic approved scientific decisions or Drive data.

## INC-001 / COR-02 — XLSX optional runtime

`scripts/build_matrix_template.py --help` is independent of `artifact_tool`. `--check-deps` tests optional import and reports whether the dependency can load. If missing, generating XLSX returns code 2 with `XLSX_UNAVAILABLE` and does not create an XLSX file. The generator does **not** silently substitute CSV or report success. Canonical CSV continuity is provided independently by `scripts/init_project.py`; it must be verified before a user can treat it as created.

The supported runtime for optional XLSX generation must have a compatible `artifact_tool` package available. Execution in an arbitrary local Python environment is not guaranteed by plugin installation.

## INC-G4-005 / COR-03 — historical AI use and trace IDs

`validate_project.py` resolves semicolon/comma/whitespace-delimited trace references individually and warns on missing IDs. The legacy `PARTIAL` annotation remains explicitly unfinished, never becomes `ACCEPTED` or a human review, and cannot satisfy substantive human sign-off. A `NOT_EXECUTED` query lacking `Literal_query` gets a non-execution-specific diagnostic, without suggesting the search was actually executed. `UNVERIFIED` events remain unverified.

## INC-006 / COR-05 — build provenance

`scripts/build_skill_bundle.py` records `build_source_commit` only when an exact clean Git HEAD and whitelisted expected origin can be checked. Otherwise the field is null with `source_verification=UNVERIFIED`. The ZIP includes per-file hashes and a non-scientific manifest. The package SHA-256 lives in external `SHA256SUMS.txt` and `BUNDLE_BUILD_RECEIPT.json` (outside the ZIP to avoid hash self-reference). The latter is a skill ZIP receipt, **not** proof that the privately installed plugin has that commit or was updated.

When migrating distribution to a ChatGPT plugin, plugin-specific version/release identity and current release ID must be checked independently; GitHub pushes do not update an installed plugin.

## Reproducible engineering checks

```sh
python -m unittest discover -s tests -v
python scripts/release_audit.py
python scripts/check_documentation_links.py
python scripts/audit_public_docs.py
python scripts/build_matrix_template.py --help
python -S scripts/build_matrix_template.py --check-deps
python scripts/build_skill_bundle.py
python scripts/build_skill_bundle.py --verify "dist/MeuArtigoSkill-v$(cat VERSION).zip"
(cd dist && sha256sum -c SHA256SUMS.txt)
```

Run these against a clean checkout and synthetic test fixtures, never against the real Gate4 scientific corpus. GitHub Actions `post-beta2-regression.yml` temporarily runs them for the maintenance branch without elevating privileges or bypassing the protected release audit.

## Open boundaries for subsequent phases

Provider availability and bibliographic disagreements remain unverified external conditions; claims of live connector operation require receipts. Corpus selection, Gate4, the 734 untouched records, 69 fuzzy pairs, text rights and missing researcher decisions remain **scientific or legal tasks**, not corrective scripts. Integration of the PR #22 MCP Apps visual component is reserved for Phase 3 and must be reconciled with later beta.2 changes. No merge, release or plugin update is authorized by this file.

## Engineering regression evidence (2026-10-11)

At commit `6183355cab1f6e5999d30ce45883aca4cd57b7ed`, GitHub Actions
[run 38111070107](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/38111070107)
passed all active steps. It executed **346 Python tests (0 failures)**, compared with
the **332 historical beta.2 tests**, and passed the static release audit,
local documentation links, public-document sensitivity scan, source-language
audit, provenance smoke test and deterministic ZIP build/verification. These
are software checks on synthetic fixtures, not independent scientific review.

An earlier run on commit `e92347f` failed before Python regression because
the release auditor intentionally expected the literal protected
`branches: [main]` workflow trigger. The original release trigger was
restored unchanged and an independent, read-only, maintenance-branch
workflow was added. The resolved failure is retained in CI history rather
than erased. The correction of the CI harness did not involve bypassing
the release safeguard.

CI-generated ZIP and SHA-256 apply to this branch's engineering smoke tests;
no public release, plugin replacement, or confirmation of an installed
plugin commit occurred. Package candidate versioning is deferred to Phase 5.
