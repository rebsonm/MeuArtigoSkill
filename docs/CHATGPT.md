# ChatGPT / Codex adapter — Meu Artigo

If this is your first GitHub Skill or plugin, begin with the
**[installation decision guide](INSTALLATION.md)** (correct file, exact
menu and error recovery). Then consult the [full beginner guide](COMECE-AQUI.md).
The public Skill and the private account plugin are **not the same install**.

The common scientific instructions remain in `SKILL.md`.
The plugin migration uses a namespaced copy at
`skills/meu-artigo/SKILL.md`, retaining the same seven gates and
researcher decisions. This adapter is a product configuration, not a new
academic method.

## Private plugin and MCP Apps distinction

The private ChatGPT plugin is a separate installation identity from the
public Skill release. It was **updated to `0.9.0-beta.4`** through the
authorized account plugin-update workflow. Its manifest still references the
original `assets/icon.svg` using `logo` and `composerIcon`, and its
scientific Skill now includes the corrected beta.4 code. This update does
**not** activate the separately developed visual MCP server or grant live
Google Drive access.

The beta.4 source candidate includes the read-only visual dashboard
reconciled from PR #22 through consolidated PR #27, together with
`scripts/build_plugin_bundle.py` for review-only plugin packaging. Main
source integration does **not** deploy `visual-app`, register a live MCP
connection, enable writable Drive, or update the installed private plugin. For a custom visual dashboard,
an authorized remote MCP deployment/connection and actual read access to
the user's canonical project must be verified. See
[plugin migration](PLUGIN_MIGRATION_PHASE3.md) and
[visual integration](MEU-ARTIGO-VISUAL.md).

## ZIP selection — Skill versus plugin

**GitHub's `Code → Download ZIP` is not a valid ChatGPT plugin package.**
It contains the repository checkout, with development files and an extra
top-level directory. Uploading it through **Plugins → Add plugin** or
**Upload new version** can fail with a missing plugin manifest error.

For **an existing personal plugin**, use its own **Upload new version** dialog
with the prepared *plugin distribution ZIP* containing, at the plugin package
root, `plugin.json`, `.codex-plugin/plugin.json`, `assets/icon.svg` and
`skills/meu-artigo/SKILL.md`. Use the existing plugin instead of creating a
duplicate. The plugin can also be updated through an authorized account
integration. The beta.4 private update has already been completed, so no
second manual upload is required.

For **standalone Skills**, the public
[beta.2 Skill release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.2)
is still the published installable download; beta.4 is currently a GitHub
source version, not a new public release.

## Installation and availability

OpenAI documents Skill availability for eligible ChatGPT accounts and
environments; workspace and product settings may constrain the option.
See [official instructions](https://help.openai.com/pt-br/articles/20001066-skills-in-chatgpt).
Where available, look for **Plugins → Skills → Create → Upload from computer**
(or equivalent localized labels in the current interface).

1. Open [the current published beta](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.2).
2. Download the specifically prepared `MeuArtigoSkill-v0.9.0-beta.2.zip`
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

## Optional bibliographic API automation (not required)

The default scientific workflow **never requires** a bibliographic API
credential. At the actual literature-search phase, the Skill may briefly
offer optional help connecting the researcher's own sources; refusal or
silence must never interrupt manual importing and scientific review.

An opt-in CLI pilot for OpenAlex/Crossref metadata, private CSV staging and
the existing hybrid deduplicator is described in the
[optional bibliography guide](OPTIONAL-BIBLIOGRAPHIC-APIS.md) and its
[Skill source contract](../references/bibliographic-connectors.md).
This command-line tool is NOT a remotely hosted ChatGPT plugin.
Scopus/WoS and other licensed sources are not falsely described as
authenticated or live-testable without the researcher's own entitlements.
Never paste tokens or passwords into this chat or a project document.

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
