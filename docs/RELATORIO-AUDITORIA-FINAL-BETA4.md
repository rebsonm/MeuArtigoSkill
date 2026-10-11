# Final development audit — Meu Artigo 0.9.0-beta.4 candidate

**Scope:** engineering closure of the development branch at PR #55 (2026-10-11). This is a **candidate for later consolidated manual homologation**, not an officially published release, certified research method, verified institutionally licensed data source, or installation in a ChatGPT host.

## Scope and baseline

- Public recommendation remains `OFFICIAL_SKILL_RELEASE = 0.9.0-beta.1`; the `VERSION = 0.9.0-beta.4` source line is development only.
- Previously merged PRs #33–54 improved local evidence checks, scientific gate boundaries, optional bibliographic connectors, C.A.D.A. continuity, native presentation and installer integrity. Treat previous green CI as software regression evidence only, not as validation of actual scholarly quality or platform operations.
- **Single scientific governance:** seven preexisting `GATE-0001`–`GATE-0007`; no implicit approval from `próximo`, C.A.D.A. DONE, a simulated respondent, a source metadata match or a generated output.
- **Single canonical continuity:** `00_Gestao_e_Continuidade/CONTINUIDADE.md`. Project-scoped TRACE and journaled C.A.D.A. writes are conditional on real local receipts; a local mirror does not prove Google Drive synchronization.
- **Existing layer reuse:** research-protocol artifacts, Claim/Evidence references, controlled manual Scopus/Web of Science import, optional public metadata providers, stage-aware route, MINIMAL/FULL projections and package verifier.
- The development source is authored in English; researcher conversation language is selected separately and manuscript language depends on explicit user/journal instructions.

## Findings and decisions

| Category | Finding | Disposition |
| --- | --- | --- |
| Packaged-source provenance | The previous `source_provenance()` checked tracked changes but ignored **untracked allowlisted source files**, so an extra new script/Markdown could enter the ZIP while the receipt still claimed a clean Git commit. | **Fixed in PR #55:** attest every member using `git ls-files --error-unmatch` and exact-file dirty checks; report `UNVERIFIED` and null commit on uncertainty. Distributing a ZIP without clean provenance remains possible, but its receipt must not claim verification. |
| Archive runtime usability | A valid ZIP manifest and local-import AST closure are necessary but do not prove that packaged scripts can be invoked after extraction. | **Covered in PR #55:** build the actual development archive and run `--help` for the initializer, next-step resolver, continuity writer, native panel and project validator in a temporary extracted directory. This is an offline smoke test, not a full host installation. |
| Package contents | Tests, copyrighted PDF corpora, optional developer-only benchmarks and source-only release tools are not researcher-facing Skill requirements. | Keep source-only; new final-audit and homologation instructions are explicitly excluded from the installed ZIP. |
| Next-step UX | PR #54 unified the safe next-step recommendation in the panel with the actual router and shared the existing gate/task selection functions. | Preserve; do not introduce an extra frontend, agent, task board or duplicate routing table. |
| Human decision authenticity | Structurally documented validation references do not independently authenticate a researcher or verify interpretation of the research. | Remains a deliberate limitation; requires real external human review. |
| Manual Scopus / WoS | File-import controls cannot prove licensed database access or an actual live Scopus/WoS query. | Manual import remains supported; network APIs must not be claimed operational without checked entitlements. |
| Source semantics | Hashes, DOIs and exact locator text cannot by themselves certify that a reference supports a claim. | Pending independent scientific adjudication under the existing methodology. |
| Release permissions | CI audits use read-only permissions and only produce development artifacts; the separate manual publication workflow has a confirmation gate. | Preserve, do not dispatch publisher or change tags, official version, Skill deployment or endorsement. |

## Candidate acceptance checks

The existing `.github/workflows/release-audit.yml` still runs: static release audit; full synthetic/offline behavioral regressions; local Markdown link checks; public-document leakage audit; language signal audit; provenance smoke test; deterministic installer build and verification; SHA-256 check. PR #55 adds tests for clean/dirty/untracked Git-member provenance and extraction-time commands from the **real** development ZIP. The exact pass/fail counts and SHA-256 of the candidate are those shown by **the PR's completed GitHub Actions run**, not prefilled here.

A `CI successful` conclusion is a criterion for source integration **only**. It is not an approval for research deployment, account changes, license compliance, human-facing usability, public release, or automatic update of an installed Skill integration.

## Open, deliberately unresolved gates

- Full manuscript lifecycle with a real researcher and real, lawfully accessed scholarly sources: **PENDING**.
- Real installation and persistent file/Drive operations on supported ChatGPT/Claude/Gemini accounts: **PENDING**.
- Independent human review of exact quotations, claim provenance, screening reasons, review-method suitability, journal rules and anonymization: **PENDING**.
- A real rights/access determination for user-supplied third-party book/PDF material: **PENDING**.
- C.A.D.A. outcome benefits (time, rework, causal efficacy), multilingual reliability and minimal/full user experience: **PENDING**.
- GitHub repository protections, release-gate settings and actual installed Skill version: **NOT VERIFIED by source-only CI**.

See `docs/VALIDACOES-PENDENTES.md` and `docs/ROTEIRO-HOMOLOGACAO-CONSOLIDADA.md` for the distinct empirical and final human review prerequisites.

## Not performed

No software release or tag, no installed Skill update or deployment, no source publication based solely on chat claims, no external research API login, no licensed Scopus/Web of Science search, no live Google Drive sync and no manual human testing. Do **not** turn a passing engineering check into an alleged scientific validation.
