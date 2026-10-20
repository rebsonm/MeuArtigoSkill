# Meu Artigo — ChatGPT packaging and publication gates

Status: source-only Draft PR. This document authorizes no installation, merge, release, deployment, or researcher-data access.

## Two distribution channels with different contracts

| Channel | ZIP artifact | MCP association |
| --- | --- | --- |
| Maintainer's private pilot | Skill bundle plus OpenAI manifest with a registered app reference | .app.json only after the production app is independently verified |
| Public ChatGPT directory | Skill bundle, manifest AND portable `mcp.json` (no `.app.json`) | Submit With MCP through the OpenAI portal, using an independently validated stable HTTPS endpoint |

The public submission portal rejects ZIPs containing .app.json or apps references to registered private integrations. Include portable root `mcp.json` for the remote HTTPS server and complete the OAuth connection and domain verification through the With MCP submission workflow. Never embed secrets or OAuth client secrets. The E05 private tunnel is synthetic-only and does not meet public-hosting requirements.

Official documentation:
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/deploy/submission-errors
- https://developers.openai.com/plugins/deploy/app-review
- https://developers.openai.com/plugins/build/mcp-server

## Prepare a source-only candidate, without publishing

Public candidate, bundling the Skill and remote OAuth MCP declaration. The URL below is the INTENDED endpoint only; DO NOT submit until it has passed real HTTPS, OAuth, CSP and two-account acceptance:

    python integrations/mcp-apps/scripts/build_chatgpt_plugin_candidate.py --channel public --mcp-url https://mcp.allflux.com.br/mcp

Private candidate, ONLY with a separately verified production registered app:

    python integrations/mcp-apps/scripts/build_chatgpt_plugin_candidate.py --channel private --app-id asdk_app_PRODUCTION_VERIFIED_ID

The example app ID is not real. Syntax validation alone cannot prove that a registered app exists or that the destination workspace authorizes it. Never install the structural-test placeholder candidate in a user's account.

The builder reuses the original Skill ZIP allowlist and BUNDLE_MANIFEST checks, preserves the canonical source version, and includes a reviewed SVG icon. Package inspection rejects version drift, tampered bundle members, unsafe ZIP paths, synthetic E05 app reuse, public/private manifest cross-contamination, hooks, and unexpected development files. The tests use only repository content and fictional mappings.

## Version blocker confirmed during review

- Candidate Git source at PR #82: VERSION 0.9.0-beta.6.
- Installed maintainer Plugin metadata: 0.9.0-beta.8; internal Skill VERSION 0.9.0-beta.6.
- Do NOT downgrade the installed beta.8 Plugin with a beta.6 source candidate. Choose the next version after the cumulative integration review, and reconcile all version manifests, BUNDLE_MANIFEST, CHANGELOG, release notes, and build receipts.
- The OFFICIAL_SKILL_RELEASE pointer and release evidence must never be advanced before a real verified publication.

## Critical path to initial release

1. After separate approval, update only the isolated E05 stage and retest ALPHA/BRAVO, ten hovered menu interactions, keyboard focus, resize, locale, CSP and teardown in real ChatGPT.
2. Independently review the cumulative PR #78–#82 diff and the absorption of overlapping older PRs. Avoid redundant merges.
3. Freeze the reviewed HEAD and require release audit, MCP Apps tests, Chromium, security contracts, and CodeQL at the SAME SHA.
4. Obtain explicit merge authorization, incorporate the single reviewed integration candidate into main, and validate the resulting main SHA.
5. Deploy the production MCP HTTPS server (not E05) with reviewed Auth0/PKCE, authorizations, secret handling, health checks and rollback.
6. Test two independently authorized ChatGPT/Drive accounts, guarded F1–F9 storage operations, journals, readback, permission denial and user isolation.
7. Package the reconciled version for the maintainer's own plugin, inspect the existing release ID, and explicitly authorize update only after the full real-host workflow succeeds.
8. Conduct a controlled volunteer pilot and document security, privacy, first-run behavior, and rollback without enabling additional usage analytics.
9. Verify publisher identity, submit With MCP to the public directory, address the OpenAI review, then confirm actual approval and installation by a separate researcher.

## Go/no-go decisions

- GO_PACKAGE: Valid ZIP and consistent versions. This is not deployment acceptance.
- GO_MCP: Real HTTPS transport and OAuth reviewed in the actual ChatGPT host.
- GO_DRIVE: Independent A/B identities and remote readback verified.
- GO_PLUGIN_PRIVATE: The new plugin actually works in the maintainer's account.
- GO_PUBLIC: Public review and directory publication independently confirmed.

User analytics, academic-profile telemetry, centralized article metadata, and ML remain outside the initial release scope. No real gate may be approved based only on synthetic CI.

## Public v1.0.0 packaging release evidence (source-only)

- Source `--channel public` MUST include `--mcp-url` naming an independently reviewed `https://HOST/mcp`; synthetic E05, loopback, HTTP, malformed paths, credentials, ports and URL query/fragment are rejected before any ZIP is written.
- Root `mcp.json` MUST use Agent Plugins schema, `type=streamable-http`, the exact reviewed endpoint and `extensions.com.openai.auth={type:oauth,baseScopes:[mcp:read]}`. The ZIP MUST NOT include `.app.json` or an existing private integration identifier. The manifest is a configuration, NOT live authentication proof.
- Public listing metadata checks include display name <=30 chars, short description <=30, long description <=4000, at most 3 unique starter prompts <=128 chars. Before submission, add real verified `websiteURL`, `supportURL`, `privacyPolicyURL`, `termsOfServiceURL`, screenshots of the actual UI, demo recording, release notes and publisher identity; do not invent these URLs.
- One tool `meu_artigo_painel`: `readOnlyHint=true` (does not alter Drive or files), `openWorldHint=false` (no web/open-ended searches), `destructiveHint=false` (does not erase persistent data), `idempotentHint=true` (repeat same input has no persistent side effect). These are code-declared values; provide these explanations in the review portal for each annotation.
- Draft five POSITIVE human-confirmable review cases: (1) start a project in researcher's own authorized Drive; (2) compare methodological routes without automatic scientific approval; (3) resume that same project's verified canonical state; (4) display a bounded seven-gate panel without declaring false Drive sync; (5) track a C.A.D.A. task and documented next action, requiring explicit permission before any canonical writes. The MCP UI by itself does not perform Drive operations; the Skill/host integration must be included in end-to-end tests.
- Draft three NEGATIVE human-confirmable review cases: (1) A cannot access B's individual Drive project; (2) secret, source document and invalid projection are rejected from panel input; (3) unauthenticated/expired and insufficient-scope OAuth access are denied without leaking account details. These require real approved two-user staging and should remain NOT_TESTED until executed.
- Do not submit an incomplete hybrid ZIP as a published release, change `VERSION` to v1.0.0, open /mcp publicly, or update an installed Plugin until the independent readiness checks and user authorization are recorded.
