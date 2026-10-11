# Approved UX reference — 12 experiences (desktop and mobile)

Status: **product UX acceptance baseline; parity NOT yet achieved**.
Source: 12 conceptual, expressly illustrative screens supplied by the product owner on 2026-10-11 in the project conversation. This document is a textual acceptance map, not an archive of those privately supplied images. Screens show demonstration data only. No actual project metrics, gates or scientific results can be inferred from the mockups.

## Approved visual system

- ChatGPT-integrated visual experience, *not* a second authoritative database.
- Desktop: bright spacious research dashboard, gentle green/neutral canvas, left module navigation, four metric cards, strong central next-action guidance, colored decision/pending distinction, visible distinction between operational and scientific state.
- Mobile: dark-mode responsive **compact** panel; prioritized next action and pending decisions without losing the non-approval disclaimer.
- Rounded surfaces, legible restrained status colors, evidence/provenance footers and explicit badges identifying demonstrations or unverified external state.
- Approved modules visibly include Visão geral, Etapas, Tarefas C.A.D.A., Fontes e buscas, Evidências, Validações, Rastreabilidade, Submissão and Sincronização.
- Twelve screenshots are **experiences/states** — not twelve mandatory navigation tabs. They include an expanded next-action experience, onboarding and mobile variation.
- User-visible CTAs must be honest: navigate to a governed action or request a real researcher decision; they must not claim completion, independent human approval, successful upload or external database access without receipts.

## Parity review against maintenance branch PR #22 port

Inspected source: `visual-app/src/mcp-app.ts`, `visual-app/mcp-app.html`, `scripts/visual_dashboard.py`, and original PR #22, on the corrective maintenance branch.

| # | Approved UX experience | Current code coverage | Parity gap / acceptance requirement |
|---|---|---|---|
| 01 | Painel geral | PARTIAL: `overview` KPIs, next operational task, pending gate | Reproduce card hierarchy, scientific progress map, prioritization and desktop brand layout; only show real canonical metrics |
| 02 | Próxima ação | PARTIAL: overview's next task and next ready gate | Dedicated guided detail state with prerequisites, blockers, accountable owner and **navigation-only** CTA unless governed actions exist |
| 03 | Mapa científico | NOT IMPLEMENTED: gate list is not a visual stage map | Interactive/read-only route and seven gates; no implication all gates are equally ready or that an approval was independently authenticated |
| 04 | Quadro C.A.D.A. | PARTIAL: `tasks` is a flat list | Kanban-style cards grouped by real status, blocked states, ownership and overdue cues; no silent task mutations |
| 05 | Buscas e fontes | PARTIAL: aggregate source counts/health shown under `sources`, labeled 'Evidências' | Separate journal/database search status and verified execution receipts; do not convert `PLANNED`/`NOT_EXECUTED` to executed |
| 06 | Evidências [L]/[I]/[P] | PARTIAL: only notes and aggregate integrity data | Separate epistemic classes with traceable claim/evidence counts and review state, without invented coverage or verification |
| 07 | Validação humana | PARTIAL: `gates` list | Single-decision workflow presentation, human attribution, rationale, source and gate constraints; genuine authorization and proof required before any write |
| 08 | Linha do tempo | PARTIAL: `history` displays up to five events in FULL | Chronological, provenance-aware timeline grouped by meaningful scientific and operational events; retain UNVERIFIED indicators |
| 09 | Prontidão editorial | NOT IMPLEMENTED: registered submission count alone | Journal policy checks, anonymization, disclosure, Gate 7 and unmet dependencies, never a fake 'ready to submit' |
| 10 | Sincronização | PARTIAL: declared storage state + registered mirror conflicts in history | Dedicated Drive continuity/snapshot/last-confirmed-sync view that distinguishes declaration from actual authenticated verification |
| 11 | Primeiro uso | NOT IMPLEMENTED | Guided setup with real permissions and canonical Drive verification; no silent initialization, fabricated remote access or accidental reset |
| 12 | Mobile escuro | PARTIAL: responsive grid and CSS `prefers-color-scheme: dark` exist | Test compact actionable mobile layout and detailed dark hierarchy against approved reference, including accessibility/readability |

**Current code has exactly five tab IDs:** `overview`, `tasks`, `gates`, `sources`, `history`.
These are an **MVP subset**, not fulfillment of all 12 approved UX experiences.
Successful Python/Node/MCP smoke tests establish read-only service operation;
they **do not** establish mockup parity or on-host visual rendering.

## Acceptance conditions before claiming UX parity

1. Map all nine approved desktop navigation modules to reachable, genuinely data-backed UI states. The next-action detail and onboarding may be embedded flows, not necessarily separate tabs.
2. Demonstrate the twelve approved screens/states with representative **clearly labeled synthetic** fixtures, including mobile dark mode, and inspect screenshot outputs for layout fidelity.
3. Every displayed scientific count/status must derive from authorized registers, never fixed examples like `12/20`, `2/7` or `8 fontes verificadas` unless actual verified test fixture data supports the label.
4. Keep project Drive canonical: remote sync, external search, human review and deployment require real receipts and permissions. Read-only UI cannot take an approval by itself.
5. Verify absent/partial/unavailable values use honest states (indisponível, pendente, não verificado), and keep scientific gates separate from task completion.
6. Validate keyboard access, responsive dimensions, light/dark color contrast and safe strings; never inject uncontrolled project content as HTML.
7. Test initial configuration/empty data/blocked external providers without placeholder scientific success.
8. Keep the original icon asset `assets/icon.svg` and both plugin presentation manifest paths intact, without replacing the approved brand with demo initials as the full listing icon.
9. When connected to a real host, separately validate MCP tool discovery, UI resource rendering and actual canonical storage adapter. Local stdio smoke is insufficient.
10. Do not merge, publish releases or update installed plugin scientific logic until the owner authorizes release procedures.

## Delivery sequence

- **Phase 4:** treat this 12-experience reference as the acceptance baseline; implement and test the incomplete modules and responsive UX in source, providing explicit pass/fail by screen.
- **Phase 5:** candidate build, hashes, user review of screenshots, PR, and controlled release steps. This document itself does not approve a release.

The screenshots supplied by the owner remain in the original conversation. Their illustrative project data is not the factual state of any project.
