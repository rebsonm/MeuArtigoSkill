# Stage 17 — isolated visual-rendering forensics (E00–E05)

## E00. Frozen baseline (2026-10-17)
- Repository: `rebsonm/MeuArtigoSkill`.
- Parent Draft PR: #79, branch `feature/mcp-multiuser-readonly-isolation`.
- Parent SHA (reported deployed and checked with `git rev-parse HEAD`): `fab60a8a2a254461d1fcd1fc66e67d7e109ed760`.
- Researcher-provided local VPS evidence: `npm run test:smoke` PASS; `node --check dist/bridge.js` PASS; both services active.
- ChatGPT tool call with synthetic projection: returned `structuredContent.site` and the expected seven gates.
- ChatGPT UI: FAILURE, "Não foi possível exibir Meu Artigo — MCP Piloto".
- Browser: CSP violation `runner.html:366` in ChatGPT runner; not proven to originate in our app.
- No host `resources/read` trace, no iframe-specific exception trace, no A/B real-user acceptance.

## E01. Candidate isolation
- Candidate branch `fix/stage17-mcp-ui-contract-diagnostics-20261017`, forked EXACTLY from the SHA above.
- Draft PR stacked on #79; do not merge either PR or overwrite the deployed services.
- Do not change Auth0, Nginx, Drive, published plugin, security allowlists or multiuser feature flag.
- Rollback for this phase: stop using the new branch; deployed service continues at frozen SHA.

## E02. Contract stabilization
- `ui_output_schema.mjs` defines structured result shape under `site` without changing the tool's actual data generation.
- `outputSchema` is declared on `meu_artigo_painel`. Input keeps `z.unknown()` to preserve existing secure custom rejection semantics and existing adverse-input regression tests. Refining inputSchema requires its own compatibility test and is not claimed complete here.
- Never transfer documents, Google tokens, source URLs, or private researcher identifiers into UI snapshots.
- Seven human gates cannot be automatically approved.

## E03. Full resource assembly test
- Run `npm ci --ignore-scripts --no-audit --no-fund && npm run build && npm run test:ui-resource-contract` in `integrations/mcp-apps`.
- Tests `tools/list`, `tools/call` with synthetic data, `resources/read`, URI, MIME, size, body marker removal, bundle inclusion, syntax of inline scripts, CSP metadata, dashboard initialization, all 10 screens and A/B synthetic data clearing.
- Log SHA-256 and size of generated HTML only; no actual research data.
- These checks do NOT prove that ChatGPT actually fetched the resource or created a functioning iframe.

## E04. Browser-level reproduction with official basic-host
Use official MCP Apps reference test host under a local test environment, never the production VPS.
- Source: https://github.com/modelcontextprotocol/ext-apps/blob/main/docs/testing-mcp-apps.md
- Start candidate MCP locally on `127.0.0.1` with a synthetic bearer token; do not expose this port publicly.
- Configure basic-host to authenticate against the local endpoint and deliver a synthetic fixture. The reference host may need a local proxy or configured request authentication. Do not expose the bearer token in URLs or screenshots.
- Capture three events: resource read, iframe initialization/bridge connect, tool result propagation.
- Repeat in Chromium with Console violations, unhandled exceptions and screenshot of the actual UI.
- This stage is NOT accepted merely because jsdom tests pass.

## E05. Three-way failure isolation
1. Minimal HTML-only screen in a separate test fixture, no SDK or Drive.
2. Minimal HTML plus official `App.connect()` bridge and one synthetic event.
3. Full composed dashboard with the bundled bridge and the same synthetic fixture.

Evaluate each with the same pinned host, SDK, locale, security policy and browser.
Report `RESOURCE_READ`, `IFRAME_CREATED`, `APP_CONNECT`, `TOOL_RESULT`, `DASHBOARD_RENDER` separately, never infer a cause from an unrelated `runner.html` violation.

### Decision rule
- If (1) fails: investigate host CSP/resource registration and delivery.
- If (1) passes and (2) fails: investigate MCP Apps handshake/runtime.
- If (2) passes and (3) fails: investigate our composed dashboard, script order, event handlers and CSP.
- If all three pass in basic-host but ChatGPT fails: compare host implementations, URI cache and browser version; do not conclude platform fault without reproducible trace.
- E06 code-level fix is not authorized by conjecture: require a failing reproduction test, candidate fix and passing regression.

## Reversibility / public rollout hold
No remote deploy, npm dependency upgrade, origin-wide CSP relaxation, removal of Auth0 subject allowlist, merge, release or plugin update without a separate explicit human approval.
