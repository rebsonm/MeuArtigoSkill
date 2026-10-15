# Host acceptance: Meu Artigo Skill + available MCP tools

**Observation date:** 2026-10-15
**Purpose:** Differentiate an installed Skill coordinating an existing connected
tool from a custom Meu Artigo MCP server or MCP Apps widget deployment.
No credentials, private research content, user IDs, token values or project
records are needed for this check.

## Observed live host check (not a CI simulation)

An assistant working on the Meu Artigo repository in ChatGPT completed:

1. `skills__list({})` enumerated the available Skill catalog and returned
   `skills://plugins/meu-artigo/meu-artigo`.
2. `skills__read({uri:"skills://plugins/meu-artigo/meu-artigo"})`
   returned the actual installed scientific instructions, including the
   instruction to use available connected tools where authorized.
3. A second `skills__read` of the installed Skill's `VERSION` yielded
   `0.9.0-beta.4`.
4. In **the same chat session**, the model invoked the connected
   `mcp__GitHub__fetch` GitHub integration with an approved, public
   repository GET URI and obtained metadata for
   `rebsonm/MeuArtigoSkill`; the response identified the expected
   repository and `main` default branch. The same tool path also
   retrieved PR #67 metadata with the expected branch.
5. No write to a research project was performed. This check cannot infer
   scientific gates, data access, private Drive sync, manuscript content,
   active scopes beyond the returned public resource, or the MCP transport
   used by any internal connector.

**Supported observation:** The installed Meu Artigo Skill instructions were
available to the assistant, and an existing connected GitHub tool returned
real read data during that session. This demonstrates a practical
Skill-instructions + already-connected-tool workflow **in the same
conversation**. It does **not** independently establish that a Skill
installation itself provisions an MCP server, or that a tool call originated
from the Skill rather than from the host assistant executing its workflow.

**Not supported by this observation:** A live connection to Meu Artigo's
*own* MCP Apps server, execution of new PR #67 Skill instructions (which
were not installed), a custom UI rendering in ChatGPT, OAuth on a hosted
Meu Artigo endpoint, an authorized per-researcher canonical Drive adapter,
or independent scientific validation.

This is an **operator-observed smoke check**, not an instrumented host
integration test or a general compatibility certification.

## Evidence levels to use in future tests

| Level | Required evidence | Current result |
| --- | --- | --- |
| HOST-0: Skill exposed | Actual Skill is enumerated and read | OBSERVED (installed beta.4) |
| HOST-1: Existing tool read | Real connected tool returns valid, in-scope data | OBSERVED (GitHub public repo GET) |
| HOST-2: Same-session workflow | Skill available and tool invoked while responding to user | OBSERVED; tool origin cannot be independently attributed to Skill |
| HOST-3: New Skill candidate | Updated PR #67 instructions installed and re-tested | NOT_VERIFIED |
| HOST-4: Own MCP tool call | Meu Artigo server connected, project access authorized, actual tool called | NOT_VERIFIED |
| HOST-5: MCP Apps visualization | ChatGPT renders own interactive MCP UI | NOT_VERIFIED |
| HOST-6: Project isolation/write/read-back | Authenticated project scoped operations and receipts | NOT_VERIFIED |

Never promote a lower evidence level into a higher one. Source-control
commits, npm/stdin MCP handshake, a downloaded Skill ZIP, and a local HTML
snapshot alone do not demonstrate HOST-3 through HOST-6.

## Repeatable non-destructive acceptance script for a maintainer

1. **Select the intended Skill version.** Observe its installed `VERSION`
   from the active host. Compare it to the target commit/ZIP. If different,
   stop claiming that the new candidate was tested.
2. **Load the real installed Skill instructions**, not only the public
   README. Check that the route and human scientific controls are present.
3. **Discover a previously authorized connected tool** exposed in the
   host, using actual tool names and schemas. No tool means report
   `MCP_NOT_CONNECTED` and continue through the Skill-only path.
4. **Read a public, in-scope test resource** using that tool, e.g. a
   public GitHub repository description. Record only the requested
   resource's coarse identifier, successful/failed status and whether
   the result was current. Do not store access tokens or raw private data.
5. **Use a negative scenario:** an unavailable or unauthorized tool must
   not trigger a fictitious success, credential prompt or hidden fallback
   to an unauthorized storage location. Confirm that the Skill still
   supplies methodological guidance with its normal scientific gates.
6. **For the *own* Meu Artigo MCP server (separate stage)** require an
   actual ChatGPT-connected HTTPS server, authorized project-specific
   read-only method, per-user isolation, canonical-store correctness,
   transport/permission error handling and first-hand returned data.
   Only then test host UI support, if included. Never expose a
   `127.0.0.1` local test service to other users or use fictional
   previews as real project data.

## Engineering and approval boundaries

This document is non-secret and reports tool availability without
researcher content. Future real-user or private-project checks must
stay in the authorized account/workspace and must not be published as
public CI fixtures. The Skill does not automatically update from
GitHub. Merge, installing another version, connecting/deploying an MCP
server and publishing a release remain separately authorized actions.

Sources:
- https://developers.openai.com/plugins/concepts/skills
- https://developers.openai.com/plugins/concepts/mcp-server
- https://developers.openai.com/plugins/build/app-quickstart
