<a id="capacidades-reais-por-plataforma-preflight-operacional"></a>
# Actual capabilities by platform — operational preflight

This table must be completed **per project/session with real responses from the tools**,
not by capabilities advertised on the vendor's website. Installation documentation
and result of use are distinct categories. No platform is chosen
as a scientific research method.

<a id="tabela-de-papéis-não-de-nomes-de-ferramentas"></a>
## Table of roles, not tool names

| Paper | Observable Question | No verified access |
| --- | --- | --- |
| Skill Loading | Are the `SKILL.md` resources and required reference accessible in the current environment? | Register format unavailable, do not promise execution |
| Canonical persistence | Is Google Drive authenticated, with access to the project space and proven writing? | View connection flow; unsuccessfully require explicit consent to `WORK_FALLBACK` before substantive search |
| Academic discovery | Is there a tool available and what query was actually executed? | Propose consultation with status PLANNED/UNVERIFIED; do not invent results |
| Scopus/WoS databases | Is there real access to the system and export with origin, date, filters and file checked? | Prepare strategy and instruct researcher authorized access |
| Deterministic execution | Python/filesystem/allowed commands exist in this mode? | Do not report scripts as executed; provide manual instructions, with limitations |
| External confirmation | Is there reliable receipt of uploading, writing, exporting or submitting? | `UNVERIFIED`, not `CONFIRMED` |
| Anonymization / rights | Have the exact files been checked under editorial rules and licenses? | Maintain external file pending audit |

**Do not fill in this table fictitiously in the project.** Use short states:
`AVAILABLE_VERIFIED`, `AVAILABLE_NOT_TESTED`, `UNAVAILABLE`,
`UNKNOWN`. Explicitly distinguish capacity reported by
supplier of operation verified **in this session**. These labels
they are preflight communication, not new spreadsheet or required ID.

<a id="observações-documentais-verificadas-em-outubro-de-2026"></a>
## Documentary observations verified in October 2026

- **ChatGPT:** OpenAI documentation describes Plugins → Skills →
  Create → Upload from computer for eligible accounts. The same source
  informs availability of Skills for qualified accounts
  organizations and subjection to workspace configurations;
  the existence of the menu does not prove connectors, scripts or Drive permissions.
  [Source](https://help.openai.com/pt-br/articles/20001066-skills-in-chatgpt)
- **Claude:** the supplier describes custom Skills on claude.ai and
  in Claude Code. At claude.ai, ZIP and plan conditions matter;
  in Claude Code, Skills are local directories `~/.claude/skills`
  or `.claude/skills` of the project. Installing the Skill is not equivalent to
  install each MCP server, tool, or connector.
  [Source](https://platform.claude.com/docs/pt-BR/agents-and-tools/agent-skills/overview)
- **Gemini:** Google documents `SKILL.md` upload, folder and ZIP with
  root entry into eligible accounts/areas; warns that there is no
  support for scripts that require internet access in Skills and that
  binary attachments like `.xlsx` are not accepted reference formats
  on upload. Resources and availability are gradual.
  [Source](https://support.google.com/gemini/answer/17094296?hl=pt-BR)

The pages list external products subject to change. Don't
declare here import, execution, integration with Drive, writing,
resumption of observed My Article projects or performance
on these platforms. The most recent public version identified in the
repository is `v0.9.0-beta.1`; branch `main` may contain code
later until manual publication of another release.

<a id="falhas-normais-e-resposta-segura"></a>
## Normal faults and safe response1. If connection still requires action from the holder, present the connection process
   authorization; not assert that the Skill clicked or authenticated.
2. If there is no Scopus/WoS tool, register the query
   **planned**, the export path and the absence of proof.
3. If a model wrote that they “uploaded to Drive” but there is no receipt
   reliable, keep the result as `UNVERIFIED`.
4. If Python tool is missing, don't run an imagined replacement
   in natural language nor declare validated scripts.
5. The criterion for closing a gate is methodologically sound evidence
   appropriate and real human decision, not the ease of a platform.

Functional verification of each platform is a different task,
registered in [pending validations](../docs/VALIDACOES-PENDENTES.md).