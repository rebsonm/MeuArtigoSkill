# Meu Artigo — optional ChatGPT-first MCP Apps UI (experimental)

## What was built

An **optional separate** MCP Apps companion now exposes:
- \`meu_artigo_painel\` as a standard read-only MCP tool;
- \`ui://meu-artigo/site-v1.html\` as an MCP Apps HTML resource;
- the user-approved blue website, with the byte-accurate repository logo,
  ten navigable sections, accessible method selection, and fictional data
  disabled by default when running in a connected host;
- the same tool's **meaningful text response**, independent of rendering;
- a single authorized local-project reader that never accepts a filesystem
  path from tool arguments.

When a client supports MCP Apps, the host can render the UI resource in
its chat interface. When it does not, the tool's text remains useful. If
the tool itself is unavailable, the Skill's ordinary conversation plus
existing native/text dashboard guidance must continue to work and must
not imply that a project was opened.

This is **implemented code**, not proof of a live ChatGPT installation:
a remote, authenticated HTTPS MCP endpoint, user isolation, permitted
project-source access and actual ChatGPT connection are still required.

## Supported UI languages and deliberate fallback

The site selects interaction language from the host's mirrored
\`document.documentElement.lang\` (when provided), the browser language,
or the explicitly supplied tool locale, and also offers a visible manual
picker. The current offline UI has authored localization for Portuguese,
English, Spanish and French, with **English as an explicit fallback** for
other language tags. It does not use IP, nationality or manuscript language
to guess language preferences.

Not every long contextual paragraph has independent professional
translations in all four languages yet; the UI is an experimental
multilingual candidate, not a universal translated/validated localization
catalog. The assistant's conversational response should follow the
researcher's language through \`references/language-policy.md\`, including
languages not yet covered by the static UI.

**Never translate source passages, participant statements or a researcher's
original task titles to match a UI setting.** The manuscript's language
remains separately governed by journal requirements or a deliberate choice.
Translation does not validate a method, reference, gate or scientific claim.

## Local use and verification

Requires Node 20+ and Python 3.10+ on an authorized workstation. Do not
put protected full texts or passwords in application packages.

    cd integrations/mcp-apps
    npm install
    npm run build
    npm run test:smoke
    npm run test:synthetic
    npm run test:i18n

Then configure \`MEU_ARTIGO_PROJECT_ROOT\` as **one absolute existing
authorized project** in the local environment and register the standard
stdio MCP server (entrypoint \`node server.mjs --stdio\`) with an
MCP Apps-compatible local host.

The optional Node server delegates to the already-reviewed read-only
\`scripts/build_research_site.py --project … --json-only\` projection;
the model cannot select arbitrary projects or request writes. The
host's tool arguments may specify a UI locale and MINIMAL/FULL display
depth, which never authorize actions or gate decisions.

### No project / unavailable or unsupported UI

The tool returns \`isError:true\` with a concise localized recovery
message **without any fictional research data** when no project has
been authorized or an authorized snapshot cannot be read.

The registered HTML resource also initializes in
\`HOST_NOT_CONNECTED\` state, not a demo with fabricated progress.
Only a valid \`CANONICAL_LOCAL_SNAPSHOT\` tool result populates it.
The UI cannot approve gates, update tasks, execute Drive writes, access
browsing/search APIs or store user decisions.

A client that cannot load MCP Apps still receives the ordinary
\`content\` text summary alongside optional \`structuredContent\`.
This is deliberate cross-client backward compatibility, not a request
to fake a tool response inside the conversation.

## ChatGPT deployment still requires an authorized external service

The stdio transport is for local host development/testing only; a
ChatGPT-connected remote MCP service needs an accessible HTTPS transport,
authentication appropriate for each user, verified tenant/project
isolation, secure data adapter, UI resource inspection and acceptance
in the actual ChatGPT client. The currently installed private Meu Artigo
Skills-based package **does not magically register this separate MCP
server**. Merely merging, updating a Skill ZIP or editing a plugin's
first-run metadata will not enable the MCP Apps iframe.

A withdrawn experimental PR #22 provided historical design input only.
Its server was not merged or silently activated; this new
\`integrations/mcp-apps/\` implementation is isolated from the public
Skill ZIP. Cross-provider support is contingent on each host accepting
MCP tools, the MCP Apps UI extension and the specific credentials.

Do **not** expose a localhost server publicly, invent a hosted URL, or
send protected project content to a shared test instance.
A managed deployment and account-specific authentication decision
must precede any ChatGPT live activation.

## Ownership and evidence

- **Researcher:** original Meu Artigo software/research concept, approved
  blue layout, methodology, data ownership and seven human gates.
- **Assistant:** proposed language adaptation, optional MCP Apps companion,
  tool/text fallback, tests, packaging docs and non-scientific UI code.
- **Provider/CI:** source tests and local MCP handshake are software
  checks; they do not establish a user-facing ChatGPT host rendering,
  Google Drive authorization, a release, or scientific efficacy.

References:
- https://developers.openai.com/plugins/build/app-quickstart
- https://developers.openai.com/plugins/build/chatgpt-ui
- https://apps.extensions.modelcontextprotocol.io/
