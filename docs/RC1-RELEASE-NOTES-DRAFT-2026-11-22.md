# Meu Artigo v1.0.0-rc.1 — Release notes (DRAFT, NOT PUBLISHED)

> **Release candidate / proposed experimental prerelease.** This document is for maintainer review **before** any tag, merge into `main`, or GitHub Release. Do not describe the candidate as stable, independently scientifically approved, or accepted on a real host.

## Overview

**Meu Artigo** is a Skill supporting the development, continuation, audit, and documentation of scientific research papers using C.A.D.A. (Capture, Assign, Define the next step and deadline, Follow up), evidence governance, human scientific decisions, and traceability between sources and claims. The researcher retains responsibility for scientific decisions and validation.

**v1.0.0-rc.1** is an experimental candidate for testing in compatible environments. The earlier public experimental **v0.9.0-beta.6** remains unchanged until a separate publication decision.

## Changes in this candidate

Conservative summary of the [CHANGELOG.md](../CHANGELOG.md) and subsequent integration on the draft PR:

- Operational integration and documentary reconciliation of 15 V1 and 20 IB work packages, including inventories of **475 bibliographic [P] records**, **174 editorial [I]/[P] cards**, and a catalog of **51 PDFs** external to the default installation ZIP, accessible only within available capabilities and applicable rights.
- Corrections and rechecks of 13 editorial notes in the disposition ledger, while maintaining quarantine for blocked records and never confusing editorial cards with primary scientific evidence or independent review.
- More conservative continuity: routing to the recorded next step, highlighting the highest-priority blocker, preserving DEC and TRACE decisions, and keeping all seven human-controlled gates `GATE-0001..0007`.
- Stronger storage isolation: preference for **each researcher's own Google Drive**, permission checks, readback after writes, refusal to presume synchronization, and a local fallback only with explicit consent.
- Version and integrity diagnostics, including SHA-256 verification for every payload and a procedure to observe host modifications to `agents/openai.yaml` and `assets/icon.svg` after saving the Skill, without changing the source manifest or automatically accepting an unreviewed receipt.
- Additional synthetic tests, tracked-source credential scans, link/provenance checks, and a **fictional** interactive map demonstration without a production connection.
- Multiplatform installation guidance and conversational language adaptation to the researcher; no assumed Web of Science, Scopus, Drive, external protocol tool, or paid-service access.

## Compatibility and dependencies

- **ChatGPT:** Skill import and script execution depend on the actual account and host capabilities. RC.1 does **not** yet have an accepted certificate of installation, persistence/readback, or end-to-end execution on a live ChatGPT host.
- **Claude/Claude Code and Gemini:** use is conditional on supported import, file, and tool capabilities. This candidate has **not** been accepted in those real platforms.
- **Python and HTTPS:** optional readers may require Python and HTTPS access to an immutable GitHub commit. Without those capabilities, only the documented methodological core remains available; do not claim external retrieval.
- **Optional libraries:** `artifact_tool` for XLSX visualization (CSV remains canonical); `pypdf` or `PyMuPDF (fitz)` for PDFs; `Pillow` for images; `openpyxl` for XLSX; and `xlrd` for legacy XLS, subject to actual module availability and execution. No dependency is assumed to be installed on every host.
- **Storage:** each researcher connects **their own** Drive if needed. Installing the Skill does not grant access to the maintainer's Drive or install or automatically connect a project-managed external tool server. The public GitHub methodological catalog is an optional read-only resource, **not** canonical memory for private research projects.

## Evidence available on 22 November 2026

The evidence below refers to its **specific previous CI source tree**, not automatically to the latest PR HEAD. After every new commit, CI and bundle provenance must be rechecked.

- Draft [PR #112](https://github.com/rebsonm/MeuArtigoSkill/pull/112), earlier candidate commit `cc74f7f738db39dce19f5d1253dd17e295dd8146`.
- Historical [Release audit #45033085251](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/45033085251): `completed/success`, **1,041 tests, 0 failures, 2 skipped** on its original source tree.
- Historical temporary [MeuArtigoSkill-rc-test-only](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/45033085251/artifacts/14757923364) CI artifact — **not** a GitHub Release. Extract the outer CI artifact first; the installable file inside it is `MeuArtigoSkill-v1.0.0-rc.1.zip`.
- SHA-256 of that **historical inner installer ZIP**: `c023560c0e1fbedfce72c963b98d8f930cd99adc1f5a07b3765361c968a53539`.
- SHA-256 of its **inner BUNDLE_MANIFEST.json**: `ed06446142d2473d21258a4f0a4a611aeb8408d9fc70f9b47759938e434ebd80`.
- That package contained **152 verified payloads (152/152)** plus the manifest, for 153 entries, excluding third-party PDFs and external reference cards. `SHA256SUMS.txt`, `VERSION`, `CITATION.cff`, the build receipt, and the manifest matched that artifact.
- The historical build receipt identified `79deb997e1208db90190be7905421b3036c2dbd1`, a temporary merge of `cc74f7f7` into `29458793`; GitHub file comparison with that PR HEAD found no differences.
- `scripts/verify_installed_bundle.py` returned `status=PASS`, `integrity_mode=ALL_BUNDLE_BYTES_EXACT`, and `payload_count=152` when run against the **ZIP-extracted copy**, with the manifest and expected version explicitly pinned. **This was not a live-host installation test.**

## Known limitations and conditions before RC.1 acceptance

- **T01/T02 HOST NOT_RUN:** actual persisted executable identification, saved file hashes, and post-save readback remain unverified. If the host transforms YAML/SVG, require an external receipt with substantive review, named reviewer, and exact observed bytes; never set `reviewed=true` automatically.
- **T05/T06 HOST NOT_RUN:** local tests passed with eight CSV records and a 21-tab XLSX, but `artifact_tool` availability depends on the host. Preserve the CSV fallback.
- **T32:** a synthetic parser test passed; no behavioral proof yet exists for the **actual installed model** when facing malicious retrieved content.
- **T34:** documentary readback of a fictional project on Drive passed; end-to-end integration between the **installed Skill** and the connected Drive has not been demonstrated.
- **Multiuser isolation:** logic and guidance use individual Drives; an independent cross-account real-host test has not been completed.
- **Issues [#102](https://github.com/rebsonm/MeuArtigoSkill/issues/102) and [#103](https://github.com/rebsonm/MeuArtigoSkill/issues/103):** historical public-file and private-metadata risks remain open. A clean current HEAD does not establish that historical commits, refs, or forks were remediated.
- The Skill does not replace peer validation or approve research gates automatically. The software's Apache-2.0 license does not extend to third-party works. No external materials are released by assumption.

## Controlled test installation (no release)

1. Download the **CI artifact** named `MeuArtigoSkill-rc-test-only` from its specific workflow run.
2. Extract the outer artifact and check `SHA256SUMS.txt` and `BUNDLE_BUILD_RECEIPT.json`.
3. Import **only** the inner `MeuArtigoSkill-v1.0.0-rc.1.zip` into a compatible host. Do not import the repository's “Code → Download ZIP” or the outer Actions artifact.
4. Identify the **actual executed version** and the researcher's authorized storage before testing any project. Do not use sensitive research data in acceptance tests.
5. For host acceptance, follow [HOST_PRESENTATION_ATTESTATION.md](HOST_PRESENTATION_ATTESTATION.md). Never modify the manifest to conceal a hash mismatch.

## Status of these notes

**DRAFT_ONLY / NOT_PUBLISHED.** This document does not create a `v1.0.0-rc.1` tag, GitHub Release, PR merge, live installation acceptance, or new scientific authorization. A public prerelease requires a later explicit maintainer decision and verified evidence for the exact candidate commit.
