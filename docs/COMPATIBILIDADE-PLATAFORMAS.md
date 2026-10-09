# Cross-platform compatibility — Meu Artigo

**Vendor support for the Skill format is not evidence that every Meu Artigo
workflow works on that platform.** This document separates supplier
documentation from verified performance of this particular beta.

| Platform | Documented installation mechanism | What was technically checked here | What still needs actual use |
| --- | --- | --- | --- |
| **ChatGPT** | Eligible environments can import Skills, subject to workspace and product settings | Installable ZIP structure, entrypoint and offline source-code regression tests | Actual installation, tool execution, writable Google Drive, real research state and cross-session continuation |
| **Claude** | Personal Skills via supported Claude applications and Claude Code, with product-specific restrictions | `SKILL.md`, reference layout and static file/package checks | Installed runtime, available MCP servers, scripts, write permissions and persistent recovery |
| **Gemini** | Eligible accounts can import `SKILL.md`, folder or ZIP with root `SKILL.md`, subject to eligibility and changing capabilities | Valid bundle structure and static package checks | Actual import, execution limitations, Drive, references and conversation continuation |

## Installed capability versus observed operation

For each actual session, use the [capability preflight](../references/platform-capability-preflight.md).
Installation is one operation; verified workspace creation, academic
retrieval and publication are separate ones. If no authoritative
receipt exists, an external action stays `UNVERIFIED` even if the
assistant describes it confidently.

Vendor documentation available in October 2026 described:
- ChatGPT Skills in eligible environments, subject to product and
  workspace configuration;
- distinct Claude Skill installation paths for Claude applications
  and Claude Code;
- gradual Gemini availability, restricted reference formats and
  lack of support for network-dependent scripts inside imported Skills.

These are **vendor statements**, not an independent compatibility
certification of Meu Artigo.

## Official vendor documentation

- [Skills in ChatGPT — OpenAI](https://help.openai.com/pt-br/articles/20001066-skills-in-chatgpt)
- [Agent Skills — Anthropic](https://platform.claude.com/docs/pt-BR/agents-and-tools/agent-skills/overview)
- [Creating and managing Skills — Google Gemini](https://support.google.com/gemini/answer/17094296?hl=en)

Account and runtime capabilities can change; follow the official
documentation and verify the current user environment.

## Storage and language policy

Google Drive is the standard persistent research workspace. Check
actual connection and **write permission** before substantive work.
If Drive cannot be used after attempted connection, obtain an
**explicit affirmative** choice for an alternative Work/local
workspace. An available connector is not proof of synchronization.

The repository is authored in English, but conversational prompts,
onboarding and answers follow the researcher's language; the
manuscript follows journal/author requirements independently.
See [language policy](../references/language-policy.md).

## Reporting future functional evaluations

Record the exact software version, platform and surface, available
features, completed real actions, receipts or verified continued
state and limitations. Successful import is not a scientific
validation. Functional comparisons among platforms remain
**PENDING** in the [evaluation register](VALIDACOES-PENDENTES.md).

The individual [getting started](COMECE-AQUI.md) and platform
guides explain supported approaches; they are not performance
reports.
