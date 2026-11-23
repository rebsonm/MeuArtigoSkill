# Meu Artigo in ChatGPT — RC.4 plugin

RC.4 is an **unpublished plugin-only release candidate**. The existing public RC.3 remains a historical Skill ZIP, not an RC.4 plugin.

## One plugin, two ChatGPT surfaces

The maintainer's independent **Meu Artigo Lab** feasibility test demonstrated a plugin selectable in both ordinary conversation and Work in their environment. RC.4 is intended to keep that **one-plugin** installation experience: activate the same official plugin in normal chat or in Work when supported and authorized. Do not claim cross-plan access, host-wide UI consistency or actual RC.4 acceptance until tested.

**Do not install a separate RC.4 Skill.** The nested `skills/meu-artigo/SKILL.md` is packaged inside `MeuArtigoPlugin-v1.0.0-rc.4.zip` and retains the scientific workflow; it is not an independent installer. The official plugin URL is pending actual release.

## First interaction

> I want to work on a scientific article with Meu Artigo. Read my research question exactly, verify which tools and storage you can actually access, and then present the next useful methodological alternatives with pros, cons, one recommendation and D for another answer.

The assistant must use [L] only for sources actually inspected, distinguish [I] and [P], keep all seven scientific gates pending until specific researcher review, and never invent source access, storage writes or approvals.

## Decisions A/B/C/D

A/B/C are three genuine alternatives, with explicit trade-offs and one recommendation; D accepts the user's own text. Native radio controls, a visible free-text field and a submit button are expected **only if the host can actually render them**. Otherwise use ordinary chat input, not fake widgets. A decision menu is not scientific or storage authorization.

## Limits

An instruction-only plugin gives no automatic Drive authentication, remote database access, external MCP services, Python execution, host-embedded App view or file persistence. Use real connected capabilities where available. Source rights, data privacy, journal rules, AI disclosure and provenance controls still apply. A project may resume only from the verified, authorized canonical records.

See [installation](INSTALLATION.md), [RC.4 packaging](RC4-PLUGIN-DISTRIBUTION.md), and [supported modes](COMPATIBILIDADE-PLATAFORMAS.md).
