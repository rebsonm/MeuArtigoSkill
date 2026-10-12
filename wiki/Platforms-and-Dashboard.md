# Platforms, integrations and dashboard

The **Skill is the methodological core**; hosting platforms, external connectors and visual interfaces are separate capabilities.

## Platforms

| Environment | Reference | Required caution |
| --- | --- | --- |
| ChatGPT / compatible Skills environments | [ChatGPT guide](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/CHATGPT.md) | Confirm the actual account's import, tools and permissions |
| Claude / Claude Code | [Claude guide](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/CLAUDE.md) | Follow its supported installation and execution model |
| Gemini | [Gemini guide](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/GEMINI.md) | Do not presume feature parity |
| Local Python helpers | [Skill scripts](https://github.com/rebsonm/MeuArtigoSkill/tree/main/scripts) | Requires local execution; outputs still need scientific review |

Availability in a vendor's general documentation is **not** independent proof of a completed end-to-end Meu Artigo run on that platform.

## Integrations

- **Google Drive:** canonical storage only when actual authorized write access is established.
- **Bibliographic discovery:** connector/API availability varies; search execution requires verifiable results. The workflow can process authentic manual exports when direct database access is unavailable.
- **ClickUp/Jira/Trello:** optional C.A.D.A. mirrors, not independent scientific databases.
- **Journal portals:** verify actual instructions, rights, files and submission receipts.

## Native visual projection

The experimental ChatGPT Skill-only dashboard may present up to five views: **overview, C.A.D.A., human gates, evidence, history/synchronization**. It reads from authorized canonical records when available; it is **not** a persistent deployed application.

Two display modes are supported: `MINIMAL` prioritizes the next eligible step and a material risk; `FULL` shows more underlying information. Neither changes the seven scientific gates or relaxes evidence rules. The native dashboard and its project-data view must not be presented as independently validated UX.

An optional external application concept discussed in [PR #22](https://github.com/rebsonm/MeuArtigoSkill/pull/22) is a **separate implementation path**, not proof that an external plugin or MCP dashboard has been deployed. Check current PR status before describing it as released.

**References:** [Platform comparison](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/COMPATIBILIDADE-PLATAFORMAS.md) · [Native dashboard](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/NATIVE-CHAT-DASHBOARD.md) · [Minimal/full mode](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/MODO-NUCLEO-MINIMO.md).
