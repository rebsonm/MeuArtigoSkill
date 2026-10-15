# ChatGPT MCP Apps research map — fictional-only adapter (experimental)

**Status:** unmerged engineering prototype on PR #66, not part of the
published beta.5 package. Not deployed, linked to a ChatGPT account, authenticated,
authorized for real research, or scientifically validated.

## Why this adapter exists

The existing Skill is the scientific and methodological authority. The
experimental local bridge binds to `127.0.0.1` and is not a ChatGPT cloud
integration. The earlier PR #22 had a withdrawn standalone MCP UI prototype;
do not revive its `visual_dashboard.py` or separate scientific model.
This adapter instead calls the current PR #66
`build_research_workspace.model(route=..., mode=...)` through
`scripts/mcp_preview_projection.py`. It uses the same
`adaptive_method_guide`, decision dimensions and project-independent
fictional model as the offline research workspace. No methodological catalogue
or gate logic is reimplemented in JavaScript.

The Node MCP server uses the official `@modelcontextprotocol/sdk` plus
`@modelcontextprotocol/ext-apps` to register:
- `meu_artigo_preview`: a read-only tool returning structured fictional
  research-map data for one supported route and presentation mode;
- `ui://meu-artigo/research-map.html`: a UI resource with MCP Apps MIME type
  displayed within compatible hosts, using `ui/initialize`,
  `ui/notifications/initialized`, `ui/notifications/tool-result` and
  `tools/call`.

The embedded page supports route exploration, five decision dimensions,
unranked alternatives, an `OTHER_NOT_LISTED` option within catalogues,
side-by-side comparison, a local ephemeral rationale draft and clearly fictional
continuity. `OTHER_NOT_LISTED` is **not** a ninth canonical route. A draft
completeness hint is not the authoritative `method_fill_preflight.inspect`
validator. No actual scientific choice is submitted or accepted.

## Run a disposable local software demonstration

Requires Python 3.12+, Node.js 20+ and npm, with dependencies installable
on the operator's machine:

```sh
cd mcp-preview
npm install --no-audit --no-fund
npm test
npm start
```

The HTTP server binds **only** to `127.0.0.1:8787`, with MCP at
`http://127.0.0.1:8787/mcp`. It does not enable public or multiuser access,
even if an operator later chooses to expose a development tunnel.
For a headless transport smoke, `node mcp-preview/server.mjs --stdio` is
available. Python alone can inspect the exact same data projection:

```sh
python scripts/mcp_preview_projection.py --route MIXED_METHODS --mode FULL
python -m unittest discover -s tests -p 'test_mcp_preview_projection.py' -v
```

A remote ChatGPT instance cannot access private localhost directly.
Connecting this app in ChatGPT requires the operator to expose a suitable HTTPS
MCP endpoint, configure a development plugin and install/link it explicitly.
**No such connection or installation is performed by this PR.** For now,
any remotely reachable adapter must remain fictional-only; never pass it
research paths, source text, Drive files or tokenized local URLs.

## Explicit security boundary

This prototype:
- takes only `route` and `mode` from the model or UI; never accepts
  arbitrary paths, source texts, project identifiers, researchers or login data;
- starts from `model(project=None, route=..., mode=...)` and checks its
  fictional-only response contract before returning structured content;
- does not expose `commit_method_field.py`, gate actions, DEC/TRACE mutation,
  project continuity, Drive sync or real-user preflight tools;
- uses DOM `textContent` rather than injecting model data into HTML;
- rejects unsupported routes and dimensions without casting traditions into
  a different research design;
- explicitly distinguishes software tests from real scientific validation.

The page's local rationale draft never leaves the iframe through an app tool.
The only `tools/call` request asks for a fictional research-map snapshot.

This does not provide OAuth, authorization, tenancy or a protected production
service. Do not set `MEU_ARTIGO_PROJECT_ROOT` or add real-project arguments
to the anonymous tool. The existing local bridge is a separate opt-in
experiment, not a backend for remote ChatGPT calls.

## Real projects: future authorization boundary

Before enabling actual project continuity or writes, design and test
**a separate, authenticated service adapter**, including:
1. OAuth 2.1 / MCP resource metadata, scopes and verified identity;
2. explicit per-researcher and per-project authorization, path and
   canonical-storage containment, and isolation tests;
3. server-side Drive state verification and least-privilege data projection;
4. existing canonical `method_fill_preflight` before an independent,
   explicit researcher confirmation for `commit_method_field`;
5. no inferential substitution for DEC/TRACE evidence or gate approval;
6. consent expiration/revocation, audit controls and redaction of private
   sources/justifications from the chat-side response;
7. test coverage for concurrent users, replay, origin, CSRF, authorization
   bypass, denial cases and erroneous provenance claims;
8. actual installation/dogfood testing by authorized operators before
   deployment, and later independent methodological evaluation.

**Humans needed now:** none for synthetic implementation and CI tests.
**Researcher:** must decide and justify real choices before any canonical write;
that functionality is deliberately unavailable today.
**External experts:** needed later to validate disciplinary suitability.
**Maintainer:** must authorize merge, deployment, connected plugin installation,
public release or mixing PR #65 with #66. These approvals do **not** block
continued read-only engineering tests.

## Verification and limitations

`mcp-preview/test.mjs` exercises an actual SDK stdio handshake, tool
listing, UI resource reading and route-specific fictional responses.
`tests/test_mcp_preview_projection.py` checks all canonical routes and
the no-private-project boundary. These establish only engineering behavior
under the tested versions/environment, not that the HTML was rendered in a
live ChatGPT host, that the server is production-ready or that methodological
guidance is valid.

Documentation:
- [MCP server quickstart](https://developers.openai.com/plugins/build/app-quickstart)
- [MCP UI bridge](https://developers.openai.com/plugins/build/chatgpt-ui)
- [OAuth authentication](https://developers.openai.com/plugins/build/auth)
- [Adaptive research map](ADAPTIVE-METHOD-MAP.md)
