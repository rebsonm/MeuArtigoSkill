# Meu Artigo — consolidated public-release readiness matrix | 2026-10-19

**Evidence scope:** engineering and operational readiness only. Passing CI is not an independent security sign-off, a multiuser acceptance test, scientific validation, or OpenAI approval. This file neither authorizes merging PR #91 nor public distribution of the Plugin.

- **Publisher:** Rebson de Morais Mendes, an individual; **contact:** rebsonm@gmail.com.
- **Plugin source candidate:** `0.9.0-beta.9`; package generated for review but **not a published version**.
- **MCP candidate:** `https://mcp.allflux.com.br/mcp`, read-only `meu_artigo_painel`, OAuth scope `mcp:read`.
- **App integration:** PR #91, based on `main`, **not merged**.
- **Public informational website:** PR #92, merged into `main` with commit `bd399a12b59acca151ffce3ab186fdc86b6901c1`. GitHub Pages build/deploy SUCCESS in run `39328997760`. Independent external HTTPS GET checks have not been confirmed.
- **Important boundary:** A public product website is not a public Plugin release, and does not grant access to private Drive data.

## Six macro stages

| Stage | Evidence completed | Remaining binding gate | Status |
| --- | --- | --- | --- |
| **01 — Consolidation / CI / security** | One integration PR (#91); release, security contracts, CodeQL and synthetic Chromium suites previously passed on reviewed heads. | Independent, documented security review (R01; GitHub PR has no separate human review); rerun all checks after any source change. | **PARTIAL** |
| **02 — Real ChatGPT MCP / interface** | Real MCP calls: no snapshot, empty fictional snapshot, seven-gate FULL fictional snapshot, invalid extra-field rejection. Owner confirmed all ten UI routes work. | Effective host-enforced CSP validation; do not confuse Cloudflare challenge errors with Plugin UI violations. | **PARTIAL** |
| **03 — Two independent researchers** | Researcher A's personal Drive connector returned folder metadata only; no files accessed or modified. | Researcher B with consent, OAuth PKCE and scopes, A→B→A no cross-access and no stale cache, invalid and unauthorized token denials. | **PARTIAL — B NOT TESTED** |
| **04 — Release package and integration** | Skill + MCP beta.9 ZIP with per-file digests verified earlier; latest ZIP builder now writes exactly four public listing URLs and the legal publisher name, covered by tests. | Fresh CI and package integrity for exact current HEAD; independent review and owner approval for merging #91, deployment and release. | **CANDIDATE ONLY** |
| **05 — Website, visual brand and policies** | Owner approved the exact existing `assets/icon.svg` design; standalone PR #92 merged; GitHub Pages workflow SUCCESS. | Public HTTPS 200 checks for four pages from an independent client; formal privacy/terms review and updated operational retention assurances where necessary. | **DEPLOYED; EXTERNAL/LEGAL CHECKS OPEN** |
| **06 — OpenAI Plugin directory submission** | Five positive and three negative reviewer cases specified, demo script drafted, publication package metadata populated and reviewer packet prepared. | Individual identity verification, `api.apps.write` permission, reviewer test account and credentials in secure portal, correct OAuth registration/PKCE, domain challenge, live scan, CSP, real 5+3 execution, demonstration URL, explicit owner submission decision, and OpenAI review. | **NOT SUBMITTED** |

## Public listing metadata (source candidate, not independently HTTP verified)

- `websiteURL`: https://rebsonm.github.io/MeuArtigoSkill/
- `supportURL`: https://rebsonm.github.io/MeuArtigoSkill/suporte.html
- `privacyPolicyURL`: https://rebsonm.github.io/MeuArtigoSkill/privacidade.html
- `termsOfServiceURL`: https://rebsonm.github.io/MeuArtigoSkill/termos.html

The public ZIP must not contain a private `.app.json`, bearer secrets, reviewer passwords, synthetic test identifiers, or a fabricated video URL. It retains the existing OAuth MCP URL.

## One consolidated external acceptance session

After a second researcher gives informed consent, execute **one** bounded final session rather than repeating earlier CI:
1. Record independent security assessment of the current PR with findings and explicit owner risk decisions.
2. Check enforced CSP from the actual ChatGPT-hosted UI. Clearly distinguish host policy vs third-party browser challenges.
3. Configure two narrowly permitted Auth0 subjects through an authorized, rollback-ready process; verify live PKCE and scope without logging JWTs.
4. Use only fictional separate Drive materials for subject A and subject B; check A→B→A isolation, logged-out behavior, no MCP persistence, no automatic scientific-gate approval, plus required 401/403 denials.
5. Run all **five positive plus three negative** reviewer prompts in real ChatGPT; record exact outcomes and rerun only failures.
6. Record an authenticated reviewer video with no private data; verify all four website URLs with external HTTPS GET 200; finish domain and developer-identity checks; upload and submit only after explicit owner GO.

## Non-negotiable release decision

**PUBLIC_PLUGIN_RELEASE_GO = NO** until the above critical evidence is complete. Site publication and package metadata updates are not authority to merge #91, deploy a new VPS build, open Auth0 access to arbitrary users, read another person's Drive, or publish a Plugin.

Related source records: `PUBLIC-DIRECTORY-REVIEW-PACKET.md`, `site-drafts/REVIEW-AND-VIDEO.md`. Official guidance: https://developers.openai.com/plugins/deploy/submission and https://developers.openai.com/plugins/deploy/app-review.
