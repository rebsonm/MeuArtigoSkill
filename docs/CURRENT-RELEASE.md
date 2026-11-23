# GitHub experimental release v1.0.0-rc.3 and Zenodo archive verification

**RC.3 publication authorized on 2026-11-23 UTC:** `VERSION=1.0.0-rc.3` identifies the approved GitHub experimental release. The Zenodo DOI and archive must be verified separately after publication. Historical publication status verified on 2026-11-22: [v1.0.0-rc.1](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.1) is the latest **published experimental GitHub prerelease**. It was released at 18:09:28 UTC on 2026-11-22. It is neither stable v1.0.0 nor independently scientifically validated.

**Newer Zenodo archive:** The maintainer has supplied DOI
[10.5281/zenodo.24450459](https://doi.org/10.5281/zenodo.24450459) for
**v1.0.0-rc.2** (experimental). This record is separate from the GitHub
RC.1 release: the published GitHub tag and `OFFICIAL_SKILL_RELEASE` still identify RC.1. The working source `VERSION` is the **unpublished RC.3 candidate**, not a previously published archive. Do not use the historical
RC.1 installable ZIP as evidence that it includes the newer online-consultation
changes. The prior Zenodo DOI cited by the project was
[10.5281/zenodo.24397699](https://doi.org/10.5281/zenodo.24397699).
The two records' exact version relationship and Zenodo file inventory
were not independently read through the public Zenodo API during this update.

**Important archival distinction (22 November 2026):** the public `main`
branch has later English-language card and documentation corrections (PRs
#121, #122 and #124). These changes were not incorporated into the
previously published immutable RC.1 ZIP. A separate, precisely pinned
source-only snapshot is prepared by the review workflow; it is **not** the
published Zenodo RC.2 installer, a new GitHub release, or a stable v1.0.0. See [Zenodo preparation](ZENODO-DEPOSIT-PREPARATION.md) and
[the rights-holder notice](../RIGHTSHOLDER-NOTICE.md).

## RC.3 release

- [GitHub RC.3 experimental release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.3)
- [RC.3 installable Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.3/MeuArtigoSkill-v1.0.0-rc.3.zip)
- [RC.3 SHA256 checksums](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.3/SHA256SUMS.txt)

**This RC.3 release is distinct from earlier RC.1 and Zenodo RC.2.**
The Zenodo RC.3 DOI will be added after the automatic archival is observed
and the version/source identity matches the release tag. No older DOI is
reassigned to RC.3.

## Historical RC.1 downloads

- [Installable Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.1/MeuArtigoSkill-v1.0.0-rc.1.zip)
- [51 third-party PDF archive with author/publisher attribution](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.1/MeuArtigo-PDFs-51-attributed.zip)
- [SHA256SUMS.txt](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v1.0.0-rc.1/SHA256SUMS.txt)

`OFFICIAL_SKILL_RELEASE`, `VERSION` and top-level `CITATION.cff` all identify approved publication of `1.0.0-rc.3` with release date `2026-11-23`. No Zenodo RC.3 DOI is claimed before independent archive readback. The historical RC.1 release date was `2026-11-22`. The previous [v0.9.0-beta.6](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.6) remains available and documented as a **historical release**, not the recommended current installer.

**Installation:** Import **only** the Skill ZIP into a compatible Skills-enabled assistant. The PDF archive is separate scholarly reference material; the GitHub source-code ZIP is not the prepared installer. Existing installed copies never auto-update.

## Scope, evidence and limits

- Public reference library: 51 individually attributed third-party PDFs (50 catalogued as CC BY 4.0; one publisher declares CC BY without a version), with [complete credit register](../knowledge/methodology/PDF-ATTRIBUTIONS.md); the software Apache-2.0 license does not replace individual PDF licenses.
- Public cards: 475 bibliographic [P] records plus 174 editorial [I]/[P] cards. These are not 649 verified primary-source [L] evaluations.
- In the fictional project `TESTE_FINAL_MEU_ARTIGO`, the maintainer reported PASS for eight metadata fields, twenty CSV tables, guidance based on two cards, saved-file readback and preservation of seven PENDING gates with no approved scientific decisions. **Optional XLSX failed** due to an unavailable dependency; the CSV files remained canonical and usable.
- This supports experimental core functionality; it does **not** establish full host byte-for-byte integrity or completed T32/T34 integrated host acceptance. Historical risks [#102](https://github.com/rebsonm/MeuArtigoSkill/issues/102) and [#103](https://github.com/rebsonm/MeuArtigoSkill/issues/103) remain tracked.

## Documentation policy

The [README](../README.md) identifies unpublished source RC.3 and separately lists the last actual published RC.1. The [installation guide](INSTALLATION.md), [ChatGPT guide](CHATGPT.md), [published RC.1 release notes](NOTAS-DA-VERSAO-1.0.0-rc.1.md) and [Wiki source](../wiki/Home.md) must continue to point to the actual published RC.1 installer, not invent a downloadable RC.3. Dated beta.6 work logs and historical acceptance records are preserved as historical evidence, not silently rewritten. The separately hosted GitHub Wiki may need a distinct synchronization step; tracked `wiki/` content is not proof that the live Wiki was published.

This document does not modify, replace or rebuild the already published GitHub release assets.
