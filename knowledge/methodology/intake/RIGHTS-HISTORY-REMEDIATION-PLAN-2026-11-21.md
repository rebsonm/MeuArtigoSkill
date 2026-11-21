# P0 — Rights and Git history decision: SRC-0367 (21 November 2026)

**Scope:** standalone experimental Skill source branch only; GitHub PR [#101](https://github.com/rebsonm/MeuArtigoSkill/pull/101) remains Draft. Decision tracker: [Issue #102](https://github.com/rebsonm/MeuArtigoSkill/issues/102). No deletion, rewrite, forced push, release, tag, scientific-gate approval or public distribution action is authorized by this plan.

## Facts established from connected GitHub data

| Item | Observed evidence |
|---|---|
| Work | Silva & Hernández (2020), DOI `10.1590/0103-3352.2020.33.218584` |
| Publisher license page | <https://www.scielo.br/j/rbcpol/a/QFmq77JnT468fcBKCdh99ms/> |
| License reported | **CC BY-NC 4.0**, not unrestricted CC BY 4.0 |
| Historical file path | `knowledge/methodology/pdfs/silva-hernandez-2020-analise-conteudo-politica-externa.pdf` |
| Git blob ID | `36de02c67d14754ac77c8f6681a5427820763d0e` (Git identifier, **not** a PDF SHA256) |
| Last verified containing commit | `115ba34f168f9efc78da3ff4a79bf61cb608e2d7` |
| Removal commit | `feaf1908008c3ae6e2e554c4c45b6cc25f89b468` |
| Current-tree status | PDF absent from the draft HEAD and from `pdf_catalog.json`; card and bibliographic record retained with a restrictive-license notice |
| Whole-history status | **Not fully audited** for remote refs, pull-request caches, mirrors, clones and forks |

The GitHub commit API confirms the PDF file was deleted by the removal commit from a parent that contained it. Deleting from HEAD does not automatically remove the historical Git object. This is evidence of an *old distribution classification and potential continued accessibility*, not a determination of copyright infringement. No full copy or excerpt of the source is reproduced in this remediation record.

## Legal and policy distinctions

The official [CC BY-NC 4.0 deed](https://creativecommons.org/licenses/by-nc/4.0/) and [legal code](https://creativecommons.org/licenses/by-nc/4.0/legalcode.en) grant reproduction and sharing subject to attribution and **noncommercial** conditions, among others. An NC file need not be unlawful in every public repository. However, the Meu Artigo public PDF corpus deliberately permits downstream unrestricted reuse, so a CC BY-NC PDF cannot remain advertised as an unrestricted catalog entry. The current catalog and readers now exclude it. Whether past attribution, intent and actual use complied with the NC terms requires a case-specific human rights/legal review.

## Alternative A — keep public history with transparent licensing, if lawful

- Preserve existing Git SHAs, links, comparisons and pinned-reader provenance.
- Keep the binary **excluded from HEAD, installation archives and unrestricted catalog**, plus source-specific notice for historical CC BY-NC material.
- Verify the historical distribution contained required author/source/license credit and was legitimately noncommercial. Record reviewer, date, license-version evidence and outcome in [Issue #102](https://github.com/rebsonm/MeuArtigoSkill/issues/102).
- Only clear the release blocker if a documented legal/editorial acceptance of historical retention exists; absence of a takedown request is not proof of compliance.
- **Advantage:** minimizes destructive change; **risk:** old version remains accessible and may not satisfy policy/legal requirements in all deployment contexts.

## Alternative B — rewrite history and coordinate GitHub cleanup, if required

- First document why retention is not acceptable; obtain explicit maintainer authorization and a private backup. Map ALL affected refs, active PRs, pinned immutable hashes, tags, forks, GitHub caches and dependent deployments.
- In a separate authorized maintenance window, use a full clone and a reviewed `git-filter-repo` plan to eliminate the path from history; then coordinate any necessary force-updates, pull-request closures/recreations, invalidated pins, support requests and downstream clone/fork cleanup.
- Verify the object/ref state after rewriting and rerun all tests, documentation checks, rights audit, installable ZIP verification and clean-host trials.
- Reference: [GitHub official history removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository). This is an operational analogy, not a claim the PDF contains secrets.
- **Advantage:** improves history-level removal where properly completed; **risk:** destructive SHA churn, broken review links and continued copies in external clones/forks; **not guaranteed global erasure**.

## Read-only evidence procedure available in this branch

`scripts/audit_methodology_rights_history.py` is source-only and **not in the installable ZIP**. It examines Git object identifiers and local refs *without opening the PDF*. It requires a **complete local clone** and fails closed on shallow history.

- `python scripts/audit_methodology_rights_history.py --repo /path/to/full/checkout` — inventory of observed local reachability, with explicit remote/fork limitations
- `python scripts/audit_methodology_rights_history.py --repo /path/to/full/checkout --require-release-clearance` — returns nonzero while the rights-history release decision is pending

The script has no Git network calls and cannot exhaust hidden pull-request refs, GitHub retained caches or external forks. A separate documented and authorized investigation is needed for those. Automated tests use **synthetic Git specimens**; they do not represent proof of a complete remote audit.

## Current decision and boundaries

**P0 status: OPEN — awaiting documented maintainer/legal editorial decision.** Provisional recommendation is **A only if** historical use and attribution demonstrably meet CC BY-NC conditions and project policy accepts that exception. Otherwise propose B for explicit authorization; do not perform it by assumption. The unresolved incident **blocks a stable-release acceptance claim**. Technical CI success is not an independent rights opinion.

Do not distribute third-party PDFs merely because they are downloadable, do not promote editorial cards to verified [L] evidence, and do not add a hosted dependency or automatic source-reader download to the Skill.
