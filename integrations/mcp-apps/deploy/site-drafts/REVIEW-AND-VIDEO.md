# Meu Artigo — release website and demo handoff (DRAFT)

**Source-only preview. DO NOT publish or submit as legally final pages.** The maintainer has identified **Rebson de Morais Mendes (pessoa física)** as responsible for Meu Artigo, with **rebsonm@gmail.com** for support/privacy. Legal bases, operational logging and retention practices, contractual terms and privacy review still require validation. Four static, self-contained HTML files already exist alongside this document:

| Portal field | Source file | Intended meaning |
| --- | --- | --- |
| `websiteURL` | `index.html` | Product description and precise current availability |
| `supportURL` | `suporte.html` | Support channel, problem-reporting guidance |
| `privacyPolicyURL` | `privacidade.html` | Personal-data practices and processor boundaries |
| `termsOfServiceURL` | `termos.html` | Use terms and human scientific responsibility |

The four historical files in this **site-drafts** directory remain source-only draft previews. The separately deployed official website is in `website/` on `main`, using the owner-approved original logo and GitHub Pages URLs. The public ZIP already populates all four listing fields; use its values, not the draft page source. Actual HTTPS responses should be verified in the portal/browser.

## Required single owner decision before publication

The maintainer supplied **rebsonm@gmail.com** as the intended public support, privacy and rights-contact mailbox (19 October 2026); it has been added to the draft HTML pages. This is owner-provided contact information, **not verification of mailbox deliverability or publication approval**. The project owner has confirmed **Rebson de Morais Mendes (individual, not company)** as responsible party and controller for processing performed under the project's responsibility. The responsible publisher must still confirm the legal bases, grounds and retention periods for Auth0 and infrastructure authentication logs, subprocessors, cross-border processing, applicable user rights notices, incident reporting route, terms validity and governing law. A legal/privacy review is necessary. The standalone site was subsequently published from PR #92 and its four listing URLs are already in the generated package. Do not claim independent legal review or independently observed public HTTP 200 until those checks occur.

The maintainer selected **GitHub Pages** for the four static pages on 19 October 2026. GitHub repository metadata now reports `has_pages=true` (Pages enabled), but **no public deployment has been verified**. Intended website: `https://rebsonm.github.io/MeuArtigoSkill/`; intended support, privacy and terms paths: `suporte.html`, `privacidade.html`, `termos.html` under that directory. These URLs are in the deployed GitHub Pages website package but independent HTTP GET verification is pending. The `.github/workflows/meu-artigo-pages.yml` workflow from standalone PR #92 is active on `main`; the Plugin directory remains unpublished. Keep `https://mcp.allflux.com.br/mcp` on its existing isolated authenticated VPS service; never proxy the marketing site through the MCP routes.

## Real reviewer video — pre-submission; NO second researcher needed

Record a 2–3 minute walkthrough in an **authorized dedicated OpenAI review account** using wholly fictional data. Confirm a functioning OAuth session. The video is for the OpenAI reviewer; the external researcher joins only after the Plugin is published.

| Time | Screen/demo | Evidence |
| --- | --- | --- |
| 0:00–0:20 | Introduce the actual Meu Artigo hybrid Skill + MCP and original brand | Installed review draft in ChatGPT, correct beta/source version |
| 0:20–0:45 | Review account Auth0 login/consent; mask URL parameters, accounts and tokens | OAuth account can authenticate with `mcp:read` without a maintainer intervening |
| 0:45–1:10 | Show fictional MINIMAL dashboard and next action | A single permitted `meu_artigo_painel` call, no Google Drive read by MCP |
| 1:10–1:40 | Show FULL dashboard with seven human gates remaining unapproved | No fabricated scientific approvals |
| 1:40–2:05 | Show the C.A.D.A. fictional task and explain the bounded projection | No manuscript or credentials transmitted to MCP |
| 2:05–2:30 | Demonstrate one safe refusal, Portuguese interface and scope/privacy limits | No unauthorized data or claims; explain research use limitations |

**Gate:** no authentic reviewer account, unavailable OAuth, inaccurate claims or private data in capture => NO video success claim. The real recording URL must be accessible to the OpenAI reviewers and verified by the publisher; do not invent a URL. Provide sign-in details through the secure submission dashboard, not the ZIP.

## Researcher study — strictly AFTER Plugin publication

After OpenAI review approval and the owner's Publish action, invite a consenting colleague to test their independent ChatGPT and Drive identity. Only then assess cross-account isolation and usability. These findings guide post-release hardening, not the initial submission gate.

## Current facts vs. pending evidence

- **Observed by VPS operator:** external protected-resource metadata HTTP 200, anonymous MCP HTTP 401, private readiness externally 404, protected persistent runtime, prior cutover success and rollback backup recorded. This is NOT a successful researcher login.
- **Verified in GitHub CI:** hybrid packaging and proposed 5 positive/3 negative tests, synthetic OAuth and host boundary tests. This is NOT a live-scanned or approved public directory plugin.
- **Before initial publication:** reviewer-only mock OAuth account, functional review flow and portal scan, identity/permissions, actual demo recording, real 5+3 reviewer test observations, any required CSP fixes, review decision and human Publish action. **After publication:** second researcher's independent ChatGPT/Drive A/B and usability study; do not block submission on that study.
- **Untouched by this documentation work:** E05 synthetic test plugin, legacy service, source `main`, existing private Plugin installations, effective runtime Auth0 policy, and users' Google Drive data. Historical `DENY_ALL` deployment notes do not supersede the maintainer's later observation of authenticated access; verify the live policy before reviewer onboarding.

The current public-candidate ZIP already contains the four GitHub Pages listing URLs; upload as a draft, then resolve any portal findings before submission. A directory publication requires an OpenAI approval and a separate owner Publish action. This document does not permit skipping any security gate or silently activating public OAuth access.
