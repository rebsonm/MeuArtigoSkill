# Meu Artigo RC.1 — three-step closure decision, 2026-11-22

**Scope:** public GitHub content, methodological safeguards and final release. This is a factual release-decision record, not a GitHub Release, copyright opinion, scientific gate approval or installation attestation.

## Step 1 — Public PDFs and editorial cards

**Observed in public PR #112 development branch:** 51 third-party PDFs in `knowledge/methodology/pdf_catalog.json`; 649 cards comprising 475 [P] bibliographic metadata cards and 174 [I]/[P] editorial cards. On `main`, the RC.1 catalogue and CARD-POLICY are not present; public access to a PR branch is NOT a release or merge.

**Rights triage:** 49 PDF entries claim `CC BY 4.0`, two have unresolved `CC BY` version: `silva-barbosa-lima-2020-analise-tematica-administracao.pdf` and `figueiredo-filho-et-al-2019-seven-reasons-transparency.pdf`. These two are **NOT RELEASE-CLEARED**; full-text lookup is now refused by both Python readers until exact-license review, without falsifying catalogue metadata or removing traceability. Any public binary already reachable through Git history requires separate containment/legal review. The 49 labelled CC BY 4.0 are NOT independently cleared by these automated checks.

**Editorial status:** operational validations `635 VALIDADO_COM_RESTRICOES + 13 CORRIGIDO_E_REVALIDADO + 1 EXCLUIDO_COM_JUSTIFICATIVA` do not equate to 649 scientific acceptances. The user waiver for stage V1-05 closes only documentary triage. Preserve [L]/[I]/[P], source editions, SRC-0385 quarantine, human scientific gates and rights distinctions.

**Distribution decision:** software-only installer with no third-party PDF binaries. The separate PDF repository history/issues #102/#103 must not be claimed resolved or licensed by that software-only boundary.

## Step 2 — Methodological corrections actually committed

1. `knowledge/methodology/CARD-POLICY.md`: explicitly differentiates public branch vs final release, 475 [P]/174 [I]/[P] cards vs checked primary works [L], conditional operational validations vs independent scientific acceptance and two unversioned PDF licenses.
2. `scripts/public_method_pdf.py` and `experimental/conceptual_rag/github_pdf_reader.py`: fail closed for PDF full-text retrieval when only an unversioned `CC BY` label exists. Metadata may remain visible; no PDF is downloaded.
3. `tests/test_pdf_license_version_retrieval.py`: synthetic no-network regression for both readers, covering metadata-only unversioned references and positive selection of explicit CC BY 4.0. `docs/RC1-RELEASE-NOTES-DRAFT-2026-11-22.md` now distinguishes host T01 PASS, T02 FAIL strict, T32/T34 NOT_RUN and Drive-only PASS.

All checks are software/metadata safeguards. No reviewed primary-source [L] claims, journal acceptance, human gate or publication license is created.

## Step 3 — Final GitHub publication decision

**Current status: RELEASE BLOCKED / NO-GO.** The public software source is already visible in the PR branch. The user's request to publish is not sufficient to establish third-party redistribution rights or attest a failed host-integrity test.

Before any final merge, tag, GitHub Release or new release asset, **all** of the following must be proved against the *new HEAD*:

- Passing CI/release audit on the final commit, plus matching new installable ZIP and SHA256 manifest/build receipt. Earlier ZIP build `ff7889ad528670075c81b02dd975d3320008a8a5` is now historical because new source files changed. Do not deploy it as if it included the current code.
- Public-source rights and privacy disposition for open issues #102 (historic CC BY-NC file/attribution) and #103 (historic Drive identifiers), without secretly rewriting commits or publishing protected PDFs. The two unversioned PDF entries require independent exact-license/attribution confirmation or exclusion from release.
- Clear written separation of **software experimental release** from scientific/card/source-PDF approval and from the failed actual-host T02 (151/153 with YAML/SVG transformations; unsigned/UNREVIEWED receipt; T32/T34 host NOT_RUN). A stable or fully accepted v1.0.0 label would be misleading.
- Use the established manual release workflow from `main` ONLY after these requirements and version/date/readme metadata are reconciled. The workflow requires an explicit GitHub maintainer dispatch and confirmation; GitHub source ZIP is not the installable Skill archive.

**What was deliberately NOT done:** merge; tag; final/preview release; deletion/rewrite of public Git history; force-push; sending emails; third-party PDF copying; auto-approval of scientific gates or rights; reinstalling to manufacture T02 PASS.

**Next executable action:** review new PR HEAD CI. If green, hold an explicit software-only publication candidate with unresolved third-party PDFs excluded; dispose of #102/#103 and documented blockers before final Git publication. No further T32/T34 test loops are needed for this rights/candidate separation.
