# Meu Artigo in ChatGPT — RC.4 plugin

RC.4 is a **published experimental plugin-only release candidate** ([GitHub](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.4); [Zenodo](https://doi.org/10.5281/zenodo.24453186)). The existing public [RC.3 release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.3) remains a historical Skill ZIP, not an RC.4 plugin.

## One plugin, two ChatGPT surfaces

The maintainer's independent **Meu Artigo Lab** feasibility test demonstrated a plugin selectable in both ordinary conversation and Work in their environment. RC.4 is intended to keep that **one-plugin** installation experience: activate the same official plugin in normal chat or in Work when supported and authorized. Do not claim cross-plan access, host-wide UI consistency or actual RC.4 acceptance until tested.

**Do not install a separate RC.4 Skill.** The nested `skills/meu-artigo/SKILL.md` is packaged inside `MeuArtigoPlugin-v1.0.0-rc.4.zip` and retains the scientific workflow; it is not an independent installer. Official [public plugin package](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.4) is published; an account-installed plugin listing is distinct and may remain private. The screenshot from the maintainer's account showed a generic icon even though bundled logo and composerIcon references were present; UI display is NOT_VERIFIED as resolved.

## First interaction

> I want to work on a scientific article with Meu Artigo. Read my research question exactly, verify which tools and storage you can actually access, and then present the next useful methodological alternatives with pros, cons, one recommendation and D for another answer.

The assistant must use [L] only for sources actually inspected, distinguish [I] and [P], keep all seven scientific gates pending until specific researcher review, and never invent source access, storage writes or approvals.

## Decisions A/B/C/D

A/B/C are three genuine alternatives, with explicit trade-offs and one recommendation; D accepts the user's own text; type your free-text answer below D when the host supports the field. Native radio controls, a visible free-text field and a submit button are expected **only if the host can actually render them**. Otherwise use ordinary chat input, not fake widgets. A decision menu is not scientific or storage authorization.

## Native four-choice behavior and honest preflight

At a meaningful decision point, show **four clickable radio buttons** for A, B, C and **Option D** when the host provides real interactive controls. There must be an **always-visible, enabled text field** immediately under D, and **typing automatically selects D**. One contextual recommended option is advisory only: **no option should** be selected by default. An actual **Submit answer** button must be available and it **does not send anything until** the user explicitly clicks it. Valid user choices do not approve a scientific gate. When native controls are unavailable, use a real plain-chat A/B/C/D answer and the ordinary platform message composer; do not fake widgets.

For tool/storage preflight, use a **short, readable explanation rather than empty tables**. Report authenticated access and permissions based on actual operations, and confirm persistent storage through **read-after-write** where applicable. Do not change a project's canonical store merely to make the preflight pass. Otherwise report **NOT_VERIFIED** or NOT_RUN explicitly.

If no MCP connection is available, continue with the plugin's internal scientific guidance and authorized native tools where possible; do not invent an MCP tool or claim an MCP Apps view was launched. Installing this plugin does **not** activate MCP Apps UI automatically.

## Limits

An instruction-only plugin gives no automatic Drive authentication, remote database access, external MCP services, Python execution, host-embedded App view or file persistence. Use real connected capabilities where available. Source rights, data privacy, journal rules, AI disclosure and provenance controls still apply. A project may resume only from the verified, authorized canonical records.

See [installation](INSTALLATION.md), [RC.4 packaging](RC4-PLUGIN-DISTRIBUTION.md), and [supported modes](COMPATIBILIDADE-PLATAFORMAS.md).
