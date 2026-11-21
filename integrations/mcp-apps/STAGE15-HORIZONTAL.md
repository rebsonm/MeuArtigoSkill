# Stage 15 — Historical horizontal acceptance and adapted host projection

This is a **synthetic engineering baseline** and must not be promoted
to live ChatGPT/MCP Apps compatibility, a Google Drive read receipt or
scientific validation.

## Four presentation surfaces, after the October 2026 adaptation

1. **Skill science core**: `build_research_workspace.model` derives
   state from authorized canonical records.
2. **Chat-native view**: `native_chat_dashboard.panel` is a local
   synthetic projection method; in a real ChatGPT session the assistant
   may use authorized native host tools to present its own research data.
3. **Blue HTML interface**: `research_site.html` has ten screens and
   supports display-only models, with four-language static UI behavior.
4. **One MCP Apps server**: `meu_artigo_painel` accepts only a
   **bounded per-call snapshot prepared by ChatGPT**, not project files,
   Google tokens, Drive IDs or any MCP-side read of Google storage.
   It returns `HOST_AUTHORIZED_SNAPSHOT` for the current call and
   provides `ui://meu-artigo/site-v1.html`. A failed or absent call
   clears the previous snapshot.

## Original synthetic acceptance vs current claim

The Stage15 synthetic project tests still validate the Skill, native
dashboard and HTML canonical projections against fictional local
files; that does NOT mean the public MCP server reads those files.
The adapted MCP call uses `references/mcp-tool-use.md` for
host-side projection from the current researcher's own Drive.

`npm run test:host-projection` verifies bounded display fields,
A/B result separation, no cross-request cache, seven gates and
rejection of extra records; `npm run test:host-projection-ui`
checks the ten-screen browser renderer for A/B display replacement
and disconnection; `npm run test:host-boundary` denies
direct project/Drive access. All are synthetic.

## Scientific and platform safeguards

- All seven scientific gates need researcher decisions; a displayed
  `approval_documented` flag is not independent scientific proof.
- C.A.D.A. dates and statuses describe records, not research quality.
- REG sidecars are advisory; missing evidence is null/unknown, not zero.
- Drive F1–F9 prohibits unsafe creation and uncertain retries.
- Host-side connected Google Drive belongs solely to the current user;
  the MCP never loads another user's storage connection or secrets.
- The MCP receives a small, temporary dashboard projection, and
  processes that data in memory; it is **not** a zero-knowledge service.
- OAuth/JWKS test fixtures do not prove a live Auth0 tenant.
- The Skill release archive excludes server source, dev-only scripts,
  private project data and credentials.

## Not yet verified

Live host installation of this GitHub candidate, ChatGPT-native Drive
content extraction under two independent users, actual call to our
`mcp.allflux.com.br/mcp` endpoint, MCP Apps rendering in ChatGPT,
real OAuth/PKCE on the external host, private-network/log containment,
production rollout, and independent scientific quality evaluation.

Plan status remains **delivery 16/18 under review**, without merge,
deployment, external account changes, Plugin update or release.
See `PLANO-MESTRE-18-ENTREGAS.md`.
