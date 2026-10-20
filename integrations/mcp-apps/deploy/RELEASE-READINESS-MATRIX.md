# Meu Artigo — public release and post-publication matrix | 2026-10-19

**Owner's explicit sequencing decision (confirmed 2026-10-19):** the *independent researcher's A/B experience and usability test happens AFTER the Plugin is published*. Do not put that researcher, a second ChatGPT account, or a second researcher's Google Drive ahead of submission or directory publication. This instruction supersedes historical internal A/B pre-release gates. Preserve security, privacy, OAuth isolation and honest status claims; do not waive OpenAI's own review requirements.

**Source candidate:** 0.9.0-beta.9; PR #91 (`release/prepare-public-mcp-20261018`, currently not merged). **Read-only MCP:** https://mcp.allflux.com.br/mcp (`mcp:read`). **Individual publisher:** Rebson de Morais Mendes. **Support:** rebsonm@gmail.com. **Current public website:** https://rebsonm.github.io/MeuArtigoSkill/ ; GitHub Pages build and deploy SUCCESS on PR #92 (run 39328997760; independent browser HTTP status not verified here).

| Stage | Completed evidence | Next action / timing | Status |
| --- | --- | --- | --- |
| **01 — Consolidate and technically audit candidate** | PR #91 source candidate, automated CodeQL and CI 7/7 SUCCESS at reviewed commit; package checked for secrets, false approvals and forbidden mappings. | Preserve security controls; independent expert review is recommended but is not described as an OpenAI-specific mandatory A/B test. Do not merge a large unreleased code change by implication. | **Engineering checks passed; independent review unrecorded** |
| **02 — Hosted MCP and visual interface** | Owner's ChatGPT MCP calls work, ten screens owner-confirmed; bounded fictional views, all seven gates pending, out-of-contract input rejected. OAuth Auth0 exists with `mcp:read` and pilot subject restrictions. | Resolve any real tool-scan, Auth0 reviewer-login or CSP findings during OpenAI's draft validation. Do not falsely claim real iframe CSP audit is done. | **Operational pilot working; official scan still pending** |
| **03 — External researcher A/B and experience evaluation** | Owner A has connected and used their own account; mock and isolated input exercises completed. | **AFTER directory publication** invite consenting researcher B, evaluate independent Google Drive connections, isolation, onboarding, A→B→A state, usability and scientific workflows. Only fictional/sample data initially. | **PLANNED POST-PUBLICATION — NOT A SUBMISSION BLOCKER** |
| **04 — Distribution ZIP and provenance** | Source package version `0.9.0-beta.9` zipped with complete Skill, official logo, one remote MCP, four official listing URLs, owner name, five positive and three negative review scenarios; no `.app.json`/secrets. | Upload candidate ZIP as a **new directory draft**; fix any portal validator findings. Do not confuse a private Plugin Creator upload with a directory submission. | **SOURCE ZIP PASSED; WEB DISTRIBUTION FAILED (#93)** |
| **05 — Product website and privacy** | Owner approved original `assets/icon.svg` design; PR #92 merged into main; GitHub Pages deployment succeeded and four HTTPS URLs were included in ZIP metadata. | Validate URLs from the actual submission portal/browser. Independent legal review is prudent; avoid claiming externally audited data retention or company identity. | **SITE DEPLOYED; LIVE EXTERNAL/LGL REVIEW UNCONFIRMED** |
| **06 — Official OpenAI review and publish** | Listing and review materials assembled; GitHub CI confirms package contract. | Verify **publisher's individual OpenAI identity** and organization/project permission, upload ZIP in Plugins portal, complete OAuth/server verification and tool scan, set up **one dedicated reviewer test account** with fictional sample data and no interactive MFA, run five positive and three negative cases with the review identity, provide real demo video URL, submit for OpenAI review, then **publish when approved**. | **CURRENT STAGE — BLOCKED BY WEB UX FAILURE (#93) AND PORTAL SETUP** |


## P0 user acceptance regression — actual web installation (2026-10-19)

**Maintainer-reported failure:** Importing the source-only beta.9 public candidate ZIP as a **personal plugin** in ChatGPT Web displays **"Abrir no aplicativo para desktop"** and does not display the embedded ten-screen panel. See [#93](https://github.com/rebsonm/MeuArtigoSkill/issues/93). This is a **real user experience FAIL** despite 7/7 source/CI success.

- `WEB_INSTALL_SUPPORTED=NOT_VERIFIED / OBSERVED_DESKTOP_ONLY` for this imported package.
- `REAL_EMBEDDED_MCP_UI=FAIL_ON_IMPORTED_PERSONAL_PLUGIN`; the UI resource remains implemented and was previously accepted through the registered private app, but not through this distributor.
- `DISTRIBUTION_READY=NO`, `PUBLIC_PLUGIN_RELEASE_GO=NO` until an actual supported browser installation preserves both the full Skill and ten-route embedded UI.
- **Do not tell researchers to import this ZIP expecting ChatGPT Web or to rely on a bare MCP connection as a full-featured substitute**. A remote HTTPS entry in `mcp.json` is only configuration, not evidence of browser support.
- Focus on the personal ZIP import vs registered app vs official With MCP submission distinction, and verify actual ChatGPT Web iframe rendering rather than repeating backend synthetic checks.
- The independent researcher B study remains **POST-publication**, per owner instruction; that does not waive basic browser UI acceptance of the distribution path.

## Exact official sequence, distinct from post-publication research

1. **Upload draft** — Select verified individual developer identity and project in the Plugins directory, choose Upload new or existing plugin, upload the built ZIP (metadata and server MCP are already present). Successful upload creates a **private draft**, not a public listing.
2. **Validation & access** — Resolve automated metadata, Skill, OAuth and tool scan issues. Supply one dedicated OpenAI **reviewer test identity** with fixed fictional data through secure Review details (never inside ZIP or GitHub). Configure only the minimum Auth0 access needed by a real reviewer. A second researcher is NOT required for this.
3. **Review submission** — Run five positive/three negative sample scenarios in actual ChatGPT with the review identity, collect honest outputs, record a real accessible demonstration and submit. The **OpenAI team** decides approval; do not invent PASS or video URL.
4. **Publish after approval** — The publisher clicks Publish plugin, making it discoverable in the directory. Until then, product website deployment and owner pilot do not make it public.
5. **POST-PUBLICATION external researcher study** — Invite consenting researcher B, perform A/B permissions and real-workflow tests, record improvements and fixes. If a serious security defect is discovered, limit access or roll back in accordance with incident response; do not expose other users' Drive.

**Do not make external researcher tests a GO/NO-GO requirement for directory submission.** The separate OpenAI reviewer-account requirement remains binding, together with platform validation and its approval. CI-green is not equivalent to formal security sign-off or public approval.

**References:** https://developers.openai.com/plugins/deploy/submission ; https://developers.openai.com/plugins/deploy/app-review ; `PUBLIC-DIRECTORY-REVIEW-PACKET.md` ; `site-drafts/REVIEW-AND-VIDEO.md`.
