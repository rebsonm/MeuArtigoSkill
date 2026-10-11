# Meu Artigo — v0.9.0-beta.4 (source candidate)

**RELEASE CANDIDATE ONLY — NOT PUBLISHED.** Prepared for engineering and product review on 2026-10-11. This document does not authorize a GitHub Release, a merge, an update to the privately installed plugin or a change to any research project.

## What has actually changed since published v0.9.0-beta.2

- Bibliographic CSV schema/identity validation, structured rejection of malformed and unidentified records, exact-duplicate provenance and review-only fuzzy candidates.
- Optional XLSX dependency diagnostics and portable CLI operation without artifact_tool installed.
- Multi-reference trace parsing with incomplete and unverified states preserved; distinction between logged but unexecuted queries and verified searches.
- Build source identity recorded only when a clean expected Git checkout is observable, plus out-of-archive package hashes/receipts.
- PR #22 scientific source verification/integrity controls, including report staleness, editorial warnings, objective conflicts and no AI substitution for human approval, ported onto maintained beta.2 source.
- Experimental read-only MCP Apps dashboard with nine research modules, guided next-action and onboarding flows, responsive dark-mobile layout and original Meu Artigo SVG icon.
- ChatGPT plugin candidate manifests maintain the historical icon reference and package the complete Skill. The MCP server/UI is developed separately; no unverified production endpoint is fabricated and no hosted MCP connection is included.

## Distribution model (three independent artifacts)

1. **Published skill beta.2** remains available as the historical GitHub Release/tag; unchanged.
2. **Private account plugin beta.3** was separately updated for icon metadata only; not automatically upgraded by this branch or its candidate ZIP.
3. **Unpublished source candidate beta.4** produces a deterministic skill ZIP and separate skills-only plugin ZIP with SHA-256 receipts. Neither archive changes the installed plugin or provides a production live UI.

## Engineering verification and release blockers

The candidate is subject to branch GitHub Actions tests for Python scientific safety, project continuity, source/trace integrity, public documentation, executable MCP stdio smoke, TypeScript build, deterministic skill/plugin ZIP packaging, icon manifest consistency, privacy file allowlists and SHA-256. A passing test suite is **software engineering evidence only**, not experimental scientific validation or an independently verified research outcome.

**Still pending and blocking any production/UX-complete claim:** pixel/render comparisons to the 12 owner-approved conceptual screens, live ChatGPT MCP App connection, OAuth/per-user isolation, genuine Google Drive synchronization, user accessibility tests and actual researcher Gate 4/Gate 7 decisions. External Scopus/WoS and paid research APIs remain governed by real access and evidence.

The source candidate intentionally omits `date-released` from CITATION.cff, contains no new release tag and has no published release link. The publication preflight must block release until the owner authorizes publication and verifies real release metadata.

## How to review

Inspect the draft Pull Request, Phase 4 UX acceptance, the Phase 5 candidate attestation, CI run artifacts and hashes. No files from real research corpora, licensed PDFs, account tokens, Drive exports or illustrative screenshot contents are included in release artifacts. Original authorship and Apache-2.0 license/NOTICE remain unchanged.
