# Meu Artigo — v0.9.0-beta.4

**Experimental public beta for external evaluation.** This release is not a
stable or scientifically validated method, a substitute for a researcher, or a
guarantee of article quality. It provides a **Skill ZIP** for supported
environments; actual account/platform capabilities vary.

## What changed since the earlier experimental betas

- **More dependable project continuity:** a new project uses one canonical
  continuity document. Resuming work derives a safe next action from
  persisted tasks, dependencies and researcher review boundaries rather than
  treating chat history or the first active row as authoritative.
- **Simpler C.A.D.A. presentation:** a compact four-column task view,
  consistent next-action status in minimal and full modes, and a readable
  blocker when the workflow cannot safely proceed.
- **Better operational traceability:** local technical task completion must
  be supported by a confirmed execution receipt and matching output artifact.
  Related task, continuity and dashboard updates use recoverable local writes
  and refuse inconsistent or interrupted states.
- **Stronger source and claim safeguards:** improved bibliographic identity,
  input validation, partial-import diagnostics, source/provenance checks,
  evidence-to-claim boundaries and explicit uncertainty about what a
  retrieved passage establishes.
- **Scientific control remains human-led:** seven researcher decision gates,
  visible separation of consulted literature [L], analysis/inference [I]
  and original proposals [P], responsible screening and honest method naming.
- **Optional bibliographic tools:** metadata adapters and manual
  CSV/RIS/BibTeX import remain subject to actual source permissions, network
  availability and permitted use. Licensed database/API access is not
  provided automatically.
- **Installer integrity:** a deterministic Skill ZIP, file checksums,
  packaged Python dependency checks and an offline extraction/smoke test
  for core commands. Development test fixtures and third-party articles
  are not included.

## What was actually checked

The final software regression run completed **595 automated tests** in
GitHub Actions on the development line before release preparation. The
separate publication workflow reruns tests, documentation and archive
checks and blocks release when they fail. These checks use synthetic
or controlled inputs; they do **not** demonstrate live scholarly
database access, researcher authentication, independent academic
quality, real-world productivity improvements or universal usability.

## Known limitations

- **No independent scientific validation:** a DOI, local content hash, quoted
  passage, or successfully executed script cannot establish that an argument
  is scientifically sound or that a human reviewer approved it.
- **Real installations remain to be observed:** ChatGPT, Claude and Gemini
  support and scripts depend on the actual account, permissions and host
  capabilities. A ZIP being buildable is not proof of installation.
- **Google Drive must be verified in context:** read/write access, canonical
  persistence and read-back are not inferred from a local test. A local
  alternative needs explicit authorization.
- **External metadata sources are not universally available:** no automatic
  authenticated Scopus or Web of Science access, institutional entitlement,
  licensed full-text access or live coverage guarantees.
- **Local recovery is not distributed storage:** recoverable technical file
  updates assume an authorized single local writer and do not synchronize
  external accounts by themselves.
- **Researcher responsibility:** design choices, inclusion decisions,
  scientific interpretation, journal compliance and submission remain under
  genuine human authority. No automatic publishing of research work.
- **Rights and privacy:** do not upload unpublished confidential material,
  credentials, research participants' information or copyrighted books
  unless access and processing are explicitly permitted.

## Install and join the testing round

1. On the [matching release page](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.4),
   download **`MeuArtigoSkill-v0.9.0-beta.4.zip`** and **`SHA256SUMS.txt`**
   when the prerelease assets have been published. Do not install GitHub's
   generic automatic *Source code (zip)* in their place.
2. Check the SHA-256, then follow the [installation instructions](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/INSTALLATION.md).
3. In a supported environment, begin with a new, low-risk research question
   and ask the Skill to verify integration/storage capabilities before work.
4. Use the [short beta-test guide](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/TESTE-BETA-PESQUISADORES.md)
   and report non-sensitive problems through
   [GitHub Issues](https://github.com/rebsonm/MeuArtigoSkill/issues/new/choose).
   Protect confidential manuscripts, credentials and sensitive source data.

This **pre-release** is intended to collect real feedback. A successful
public beta does not make it a stable `v1.0.0` release. Prior prereleases
are retained for reproducibility and their existing licenses/rights.
