# Stage 17 — E05 post-acceptance and public CSP hold

Status: source-only Draft PR stacked on #84. No merge, Plugin update, release,
production deployment, Auth0 changes, Drive access, or public submission.

## Grounded operator evidence

- The operator executed E05 staging preflight at SHA
  `f7bdf1b92d62163b1530549361416fc0789cf98b` and supplied terminal
  output ending with `E05_STAGING_PREFLIGHT_PASS`. The staged source was
  detached to that SHA; the primary Stage 17 source SHA had been observed
  unchanged immediately before.
- The isolated `tunnel-client` profile initially failed because the file
  was supplied through the wrong path, then because its environment-sourced
  runtime API key was absent. The operator supplied a runtime key **locally**
  and later shared logs showing `doctor RESULT ok`, MCP stdio startup, and
  tunnel-client initiation. No credential value is included here.
- In real ChatGPT, both fixed fictional `SYN-E05-A-01` and
  `SYN-E05-B-01` invocations returned `HOST_AUTHORIZED_SNAPSHOT` with
  all seven human gates false, no claimed Drive synchronization, no
  scientific auto-approval, and no canonical writes.
- The user's screenshot shows the ChatGPT-embedded dashboard, sidebar,
  a synthetic task count of one, zero documented gates, and advisory
  `Não avaliado` labels. The user confirmed **"Tremida desapareceu"**,
  and subsequently reported **"Tudo ok"** when asked to review all ten
  screens, BRAVO replacement, and responsiveness.
- The statements above support **human-reported visual acceptance**
  for E05 hover/navigation. They are not independent browser-console traces,
  DOM recordings of all ten screens, proof of BRAVO replacing ALPHA in
  the same instance, or production user isolation.
- The ChatGPT screenshot visibly displayed **"CSP desativada"**.
  The source of that host badge is **unknown**. It is not evidence that
  `_meta.ui.csp` was absent, nor proof that the host enforced a
  browser content security policy.

## E05 security contract

`npm run test:e05-csp` calls the real local `createServer()` through an
in-memory MCP transport, reads the actual `site-v3.html` UI resource after
the normal bridge build, and checks:

1. Tool resource URI, MIME type, resource metadata and UI template identity.
2. Exactly two declared widget CSP fields: empty `connectDomains` and
   `resourceDomains`; no `frameDomains` or unreviewed metadata keys.
3. A single, restrictive HTML CSP meta directive (including
   `default-src 'none'` and `connect-src 'none'`).
4. No nested iframes, remote scripts, link-href resources, embeds,
   active forms, foreign image URLs, stylesheet imports, or external CSS URLs.
5. Seven negative mutation cases that must each fail closed.

The check is mandatory in the MCP Apps CI and produces only
`E05_CSP_DECLARATION_GATE_PASS`, the **synthetic UI hash**, and the
explicit labels `host_iframe_csp=NOT_OBSERVED` and
`public_release=HOLD`. It does **not** disable any host policy or
interact with runtime credentials.

## Browser/host CSP remains a hard release gate

The OpenAI Plugin docs require exact widget domain declarations, a
publicly reachable non-test production MCP endpoint, and a dedicated
widget origin for a submitted Plugin with UI:

- https://developers.openai.com/plugins/build/chatgpt-ui
- https://developers.openai.com/plugins/reference
- https://developers.openai.com/plugins/deploy/app-review
- https://developers.openai.com/plugins/guides/security-privacy

Current E05 is a private synthetic tunnel, not the production MCP server.
The component has empty CSP domain allowlists appropriate to its
self-contained UI, but its published `_meta.ui.domain` is **not yet
configured as a unique verified production origin**.

Before moving to external researchers:

- [ ] Determine what the ChatGPT **"CSP desativada"** badge means in that
  host/test connection, and obtain browser or host evidence showing
  an effective, reviewed CSP with no unexpected external network calls.
- [ ] Validate the actual sandbox iframe policies with CSP enabled (not
  merely declared metadata), test denials and browser-console violation
  **categories** without logging URLs, tokens or private source text.
- [ ] Review any required dedicated `_meta.ui.domain` for a submitted
  Plugin with UI; do not invent a production origin or broaden the policy
  to make a private test work.
- [ ] Verify the real HTTPS MCP, OAuth scopes, A/B account isolation,
  original Drive write protections and explicit user authorization.
- [ ] Reconcile version metadata and the complete integration chain,
  re-run all required CI on the final merge candidate, then request
  separate approval for merge, private Plugin update and public submission.

## Evidence and decisions

| Gate | Current result |
| --- | --- |
| E05 private synthetic tool ALPHA/BRAVO | PASS (observed) |
| E05 hover tremor | HUMAN PASS |
| E05 ten screens, replacement and responsive view | HUMAN REPORTED OK; independent instrumentation unavailable |
| Declared widget/HTML CSP | REQUIRED AUTOMATED CI, once tested at this PR's SHA |
| Effective ChatGPT CSP in browser | NOT VERIFIED — visible host badge needs explanation |
| Dedicated public UI origin | NOT CONFIGURED |
| Production real-user A/B Drive and OAuth | NOT VERIFIED |
| Merge / release / public directory | NO-GO |

Never upgrade the last four gates based only on a synthetic tunnel, unit tests,
a host badge, or general user feedback about the visual interface.
