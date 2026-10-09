# Claude / Claude Code adapter — Meu Artigo

First-time users should read [Getting started](COMECE-AQUI.md).
This adapter is about runtime capabilities, not a distinct
scientific method. The shared contract is `SKILL.md`.

## Installation

Anthropic documents personal Skills in eligible Claude applications
and local Skills in Claude Code. Check
[official documentation](https://platform.claude.com/docs/pt-BR/agents-and-tools/agent-skills/overview)
for current conditions, permissions and interface wording.

1. Download the prepared ZIP from [the published beta](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.1);
   prefer `MeuArtigoSkill-v0.9.0-beta.1.zip` over GitHub's source archive.
2. If your claude.ai account exposes custom Skills, use its Skill upload
   feature and select the complete bundle.
3. In a supported Claude Code environment, unpack the prepared Skill
   as a directory with `SKILL.md` in its root, normally under
   `~/.claude/skills/` for the user or `.claude/skills/` for a
   particular project.

These installation paths are **not equivalent execution environments**.
Neither upload nor directory placement proves Python execution,
network access, connected MCPs, Drive writes or persistent recovery.

## Always respond in the researcher's language

**Source files and default prompts are in English**, but the
researcher can speak Portuguese, Spanish or another supported
language and receive ordinary answers in that language automatically.
Use the latest substantive direct message, unless the researcher
explicitly requests a fixed output language. See
[automatic language policy](../references/language-policy.md).

The manuscript language is an independent decision based on
journal instructions or the researcher's preference.

## First research session

The researcher only needs to describe the real research problem
in their own language. Before any substantive research, check
that Google Drive is truly authenticated **and writable**. If
it is unavailable, show the connection path and verify again;
request explicit affirmative permission before creating
a local alternative workspace. Never silently replace Drive
with a local file while claiming remote persistence.

Preserve the research question, propose method-appropriate
paths, ask for real human scientific decisions and collect
a target journal's actual instructions when available.

## MCP connectors and scripts

Inspect the MCP servers and native tools **actually installed**.
Map them to persistent storage, academic discovery, citation context,
publisher/document retrieval, indexed search, deterministic scripts
and optional C.A.D.A. task mirroring. Do not copy OpenAI-specific
connector names or pretend an MCP server exists.

Python scripts such as `scripts/init_project.py`,
`scripts/validate_project.py` and
`scripts/dedupe_records.py` can only be executed where the
current Claude product genuinely permits local execution. Otherwise
describe a verifiable alternative without claiming completion.

Scopus/Web of Science are external indexed resources unless
there is authorized real access. The Skill can prepare queries,
filters, exports and validation without inventing search events.

C.A.D.A. remains functional as internal management even without
an external ClickUp/Jira/Trello integration. If one is enabled,
use it only as a task mirror while retaining the canonical
research project records.

## Continuity and evidence

Update `CONTINUIDADE.md` in the authorized canonical workspace
after substantive work. Externally performed actions require
independent receipts; an AI-generated log alone is insufficient.
If the user returns in another session, read their **real**
stored state instead of inventing prior scientific decisions.

The existence of a Skill importer and ZIP-format compatibility
is not scientific validation. Actual cross-platform operation
remains an independent [pending evaluation](VALIDACOES-PENDENTES.md).
