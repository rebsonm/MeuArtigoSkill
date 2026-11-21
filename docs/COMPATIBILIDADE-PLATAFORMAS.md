# Where can I use Meu Artigo?

Meu Artigo is distributed as a **Skill**, but installing Skills and accessing external research services depend on your assistant and account.

| Platform | How you may use Meu Artigo | What to check |
| --- | --- | --- |
| ChatGPT | Import the prepared Skill ZIP if Skills import is offered | Installed version; access to saved files and connected services |
| Claude / Claude Code | Import a custom Skill or use a supported local Skill directory | Whether the product can run scripts and preserve project files |
| Gemini | Import the Skill where the product supports it | Supported files, available tools and reliable storage |

[ChatGPT guide](CHATGPT.md) · [Claude guide](CLAUDE.md) · [Gemini guide](GEMINI.md) · [Installation](INSTALLATION.md)

## Optional portable visual integration

The optional `integrations/mcp-apps/` companion follows the standard
MCP Apps tool-to-UI resource protocol, with a full textual result for
clients without graphical widgets. ChatGPT is the primary target and
requires a separate authenticated HTTPS server connection before the
component can appear in the conversation. Other assistants may render
the same component only if their host actually supports MCP Apps. The
Skill itself stays useful as a text-only research assistant if an MCP App
cannot load. This portability is architectural, not proof of live tests
in every provider.

The UI follows the user's preferred interaction language where supported
(PT/EN/ES/FR static translations and an English website fallback);
it does not change manuscript language, source evidence or the scientific
approval rules. See [integration documentation](../integrations/mcp-apps/README.md).

## What is independent of the platform?

You can describe a research problem, discuss methodological options, review source evidence and control your own scientific decisions. Seven significant scientific checkpoints remain under researcher responsibility.

## What varies?

- **Storage:** a displayed Drive connection is not proof of a successful file write.
- **Academic research access:** paid databases and licensed articles require your own authorized access and a real query.
- **Scripts and files:** some assistant environments cannot run Python or handle all file types directly.
- **External connections:** available connectors can differ even between accounts on the same platform.
- **Visual presentation:** the Skill's conversational guidance is the primary path; any richer interface depends on actual host support.

Compatibility testing remains **PENDING** for platforms and accounts not yet observed. For an explanation of how capabilities are checked, see [the platform access guide](../references/platform-capability-preflight.md). The software's automated tests do not certify full real-world compatibility on ChatGPT, Claude or Gemini. If a feature cannot be verified, the correct status is **not verified**, not completed.

**Version:** beta.6 is the source candidate; beta.5 is the latest confirmed published package until a complete beta.6 release is visible.
