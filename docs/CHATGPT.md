# ChatGPT / Codex adapter — Meu Artigo

If this is your first GitHub Skill, start with
[Getting started](COMECE-AQUI.md).

The common scientific instructions remain in `SKILL.md`.
The adapter is a product configuration, not a separate academic method.

## Installation and availability

OpenAI documents Skill availability for eligible ChatGPT accounts and
environments; workspace and product settings may constrain the option.
See [official instructions](https://help.openai.com/pt-br/articles/20001066-skills-in-chatgpt).
Where available, look for **Plugins → Skills → Create → Upload from computer**
(or equivalent localized labels in the current interface).

1. Open [the current published beta](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.1).
2. Download the specifically prepared `MeuArtigoSkill-v0.9.0-beta.1.zip`
   and optionally check the `SHA256SUMS.txt` digest.
3. Import the complete ZIP, **not** GitHub's automatic source-code archive.
4. Review the platform's result rather than assuming every integrated
   tool is immediately authenticated or available.

A prior successful import of another version does **not** demonstrate
functional compatibility of the current beta. An available Skill menu
does not establish Python execution, persistence or app entitlements.

## Conversation language and manuscript language

**This adapter and the whole repository are authored in English.**
The default activation text is English but is **not a request to
respond to the researcher in English**. Follow the person's
current substantive conversation language (for example Portuguese
for a Portuguese message), subject to any explicit preference.
Apply [the language policy](../references/language-policy.md)
on every interaction, including onboarding questions and error
explanations. The paper itself uses the language chosen by the
researcher or required by the journal.

No install-time translation pack, localization option or
translation of canonical IDs is necessary.

## Starting a research project

After importing, ask to use `$meu-artigo` and supply a real research
question or idea in the user's own language. The Skill must first
verify that Google Drive is **connected and writable**. If it is not,
it should guide the required connection step, recheck the access
and request **explicit affirmative permission** before proceeding
with a Work/local fallback.

Only then should it begin novelty examination, method selection,
source retrieval, analysis or drafting. If the target journal is
known, obtain **official author guidelines and template** before
claiming journal-aware formatting. Keep the actual researcher's
scientific decisions and evidence requirements distinct from
C.A.D.A. operational tasks.

## Installed package contents

The prepared bundle has `SKILL.md` at its root, with
`references/`, `scripts/`, `docs/` and an optional
`agents/openai.yaml` adapter. This structure is technically
checked; execution of those scripts is product/surface dependent.

## Preferred external capabilities

- **Google Drive:** canonical persistent research workspace; actual
  read/write permission and synchronization must be verified.
- **Consensus:** academic discovery when available; not an exhaustive
  bibliographic database or a second human reviewer.
- **Scite:** citation context and bibliographic support where accessible.
- **Firecrawl / web:** journal, publisher and official-source retrieval.
- **Scopus / Web of Science:** use authorized platform access or
  real user exports; do not claim an invented direct connector.
- **ClickUp, Jira / Atlassian, Trello:** optional alternatives for
  an external C.A.D.A. task mirror. One provider is sufficient.

The provided `agents/openai.yaml` advertises preferred integrations,
but installing the Skill never installs/authenticates third-party
accounts on the user's behalf. Where a connector is absent, explain
a lawful manual path and record an unverified action correctly.

## ChatGPT-native visual dashboard

A user may ask `$meu-artigo` to show project progress directly in the
conversation. Use native UI cards, tables or charts when the active host
supports them; otherwise fall back to clear Markdown. This feature is
**part of the Skill's presentation contract** and does not require a new
MCP app, hosting or a custom plugin. Use real authorized Drive state
or an explicitly authorized local project; preserve human scientific
decisions, unknown data and read-only navigation.

See [native dashboard pilot](NATIVE-CHAT-DASHBOARD.md).
Importing a different or older Skill package does not automatically
install these changed instructions. A generated native view does not
establish that a permanent custom app was installed.

## Functional limitations

For the installed version, verify actual first-run behavior,
source/locator checks, research storage, metadata handling and
cross-session recovery before claiming they work in this account.
The [platform capability preflight](../references/platform-capability-preflight.md)
separates documented product support from actions observed in the
current session.

A functional multilingual demonstration and installed beta evaluation
remain [pending](VALIDACOES-PENDENTES.md), even when software tests pass.

If Skills are not available for the current account, consult the
provider's current eligibility guidance or the other supported
platform guides; do not invent a hidden menu or subscription right.
