# Stage 17 — Version and single-PR integration register (0.9.0-beta.9)

Status: source-only decision evidence for [PR #89](https://github.com/rebsonm/MeuArtigoSkill/pull/89). It authorizes no merge, Plugin modification, account access, VPS deployment or publication.

## Git ancestry

- Verified main base `5c7bf4ff599d73a660bb709616a689140b2edbe7`.
- Historical Draft PR #87 carries the first 242 accumulated commits; Draft #88 and #89 add the last ten commits on top.
- PR #89 was retargeted to `main` as the **only integration decision PR**, keeping the original history. Before this version commit its HEAD was `d0be8cb5b093a2681fc8991dd36a2862d51bd1f9`, 252 commits ahead, zero behind, 154 changed files; verify again after each update.
- Historical PR #87/#88 remain Draft, open, and must not be merged independently. No PR is closed without explicit maintainer approval.

## Verified version matrix and next candidate

| Surface | Before this source-only commit | Candidate after this commit | Interpretation |
| --- | --- | --- | --- |
| Source Skill `VERSION` | `0.9.0-beta.6` | `0.9.0-beta.9` | Source only, not a published tag |
| README/CITATION/release notes | beta.6 metadata | beta.9 source-only metadata | `date-released` intentionally absent; beta.6 published link preserved |
| Installed personal Plugin `meu-artigo` | Manifest beta.8, embedded Skill beta.6 | **UNCHANGED** | Exact current release must be rechecked before any update |
| GitHub public Skill release | beta.6 reported published | **UNCHANGED** | Never rewrite historical beta.6 or move official pointer |
| MCP Apps `package.json` / lock | `0.1.0` | `0.3.0` | Independent private Node package version |
| MCP `McpServer` and UI `App` | `0.2.0` / `0.3.0` | `0.3.0` / `0.3.0` | Technical protocol component metadata only |
| `MEU_ARTIGO_SITE_V1` | V1 | V1 | Display projection data contract remains stable |
| UI resource | `ui://meu-artigo/site-v3.html` | unchanged | Resource identifier is not a software semver |
| E05 synthetic test Plugin | separately installed 1.0.0 | **UNCHANGED** | Never substitute it for the public MCP server |

## Packaging and rollback gates

1. For the source candidate, build the deterministic Skill ZIP and public ChatGPT candidate from the exact, reviewed Git HEAD. Compare two SHA-256 builds and validate the generated `BUNDLE_MANIFEST.json` file digests; never confuse the generated manifest with an installed host manifest.
2. The private candidate requires a **verified production app ID and owner authorization**. The synthetic E05 app and fictional structural-test app are not production identifiers. Do not embed `.app.json` in the public package.
3. Publish the resulting version only after manual GO and a real UTC publication date; `check_release_metadata.py` must block a premature release because beta.9 has no `date-released`.
4. Rollback must restore the prior, owner-approved private Plugin release ID and independently restore the prior endpoint configuration. No rollback action is authorized by this document.
5. CI success is an engineering gate only, not scientific validation, actual Auth0 OAuth acceptance, actual multiuser Drive isolation, proof of enforced host CSP or independent review.
