# Meu Artigo — release website and demo handoff (DRAFT)

**Source-only preview. DO NOT publish or submit as legally final pages.** The maintainer has identified **Rebson de Morais Mendes (pessoa física)** as responsible for Meu Artigo, with **rebsonm@gmail.com** for support/privacy. Legal bases, operational logging and retention practices, contractual terms and privacy review still require validation. Four static, self-contained HTML files already exist alongside this document:

| Portal field | Source file | Intended meaning |
| --- | --- | --- |
| `websiteURL` | `index.html` | Product description and precise current availability |
| `supportURL` | `suporte.html` | Support channel, problem-reporting guidance |
| `privacyPolicyURL` | `privacidade.html` | Personal-data practices and processor boundaries |
| `termsOfServiceURL` | `termos.html` | Use terms and human scientific responsibility |

All four files share relative navigation, Portuguese copy, responsive CSS, keyboard focus, no JavaScript and no trackers. A prominent DRAFT banner, `noindex,nofollow` and placeholders keep them unsuitable for public portal submission until approved. Their GitHub preview addresses are *not* verified product website URLs; **do not fill manifest fields with guesses**.

## Required single owner decision before publication

The maintainer supplied **rebsonm@gmail.com** as the intended public support, privacy and rights-contact mailbox (19 October 2026); it has been added to the draft HTML pages. This is owner-provided contact information, **not verification of mailbox deliverability or publication approval**. The project owner has confirmed **Rebson de Morais Mendes (individual, not company)** as responsible party and controller for processing performed under the project's responsibility. The responsible publisher must still confirm the legal bases, grounds and retention periods for Auth0 and infrastructure authentication logs, subprocessors, cross-border processing, applicable user rights notices, incident reporting route, terms validity and governing law. A legal/privacy review is necessary. Then deploy all four pages on an owned HTTPS origin, remove the DRAFT banners/noindex, verify every page with public GET 200 (valid certificate, no authentication) and only then populate the four manifest URL fields.

The maintainer selected **GitHub Pages** for the four static pages on 19 October 2026. GitHub repository metadata now reports `has_pages=true` (Pages enabled), but **no public deployment has been verified**. Intended website: `https://rebsonm.github.io/MeuArtigoSkill/`; intended support, privacy and terms paths: `suporte.html`, `privacidade.html`, `termos.html` under that directory. These are **planned URLs, not publicly verified submission links**. The `.github/workflows/meu-artigo-pages.yml` workflow is manually gated to the reviewed `main` branch and deliberately refuses unapproved legal drafts. Keep `https://mcp.allflux.com.br/mcp` on its existing isolated authenticated VPS service; never proxy the marketing site through the MCP routes.

## Recording script — 2–3 minutes; ONLY after consented real A/B verification

Record the following using a dedicated reviewer test account and entirely fictional material, never real academic files, tokens or student data. Do not substitute synthetic E05 recordings for actual hosted OAuth validation.

| Duration | Screen and spoken demonstration | Pass evidence |
| --- | --- | --- |
| 0:00–0:20 | Introduce Meu Artigo in ChatGPT, explain seven scientific gates and C.A.D.A. task tracking; show the actual plugin name and confirmed current version | Real ChatGPT installation, not synthetic UI mock |
| 0:20–0:45 | Show permitted Auth0 authorization-code + PKCE consent for a designated review account; redact account names, redirect codes and token values | Successful `mcp:read` login reported by ChatGPT |
| 0:45–1:20 | Open approved fictional project A through its own ChatGPT Drive connection, display minimal/complete sanitized panel with gates pending | One bounded `meu_artigo_painel` call and current task state |
| 1:20–1:45 | In separate consenting account B, display only fictional project B; attempt to access A's private project and demonstrate denial | Independent identity and Drive permission boundary; no shared content |
| 1:45–2:10 | Reopen the A dashboard; demonstrate no cross-account cached state and no automatic gate approval | Human gates still pending, no data leakage |
| 2:10–2:30 | Show keyboard and locale behavior, evidence that iframe host CSP allows required UI resource, and close with explicit research limitations | Real host console/policy observation recorded without secrets |

**Recording gate:** if either account has not consented, live plugin OAuth is not working, effective CSP is unresolved, or the runtime remains `MEU_ARTIGO_MCP_PILOT_SUBS=DENY_ALL`, do **not** record a fictional “success” video. The video URL must be reachable by the reviewer, and any reviewer credentials must be supplied only via the secure OpenAI portal.

## Current facts vs. pending evidence

- **Observed by VPS operator:** external protected-resource metadata HTTP 200, anonymous MCP HTTP 401, private readiness externally 404, protected persistent runtime, prior cutover success and rollback backup recorded. This is NOT a successful researcher login.
- **Verified in GitHub CI:** hybrid packaging and proposed 5 positive/3 negative tests, synthetic OAuth and host boundary tests. This is NOT a live-scanned or approved public directory plugin.
- **Still pending:** two independent consented ChatGPT/Drive accounts, Auth0 PKCE and permission scope in actual ChatGPT, real CSP, legal/privacy review (contact and responsible individual already identified), four actually published/verified HTTPS URLs, demonstration recording, reviewed security risk acceptances, explicit owner approval to submit and platform review outcome.
- **Untouched by this documentation work:** E05 synthetic test plugin, legacy service, source `main`, existing private Plugin installations, effective runtime Auth0 policy, and users' Google Drive data. Historical `DENY_ALL` deployment notes do not supersede the maintainer's later observation of authenticated access; verify the live policy before reviewer onboarding.

Upon successful public validation and owner sign-off, repack with valid **real** URLs and the verified version. This document does not permit skipping any security gate or silently activating public OAuth access.
