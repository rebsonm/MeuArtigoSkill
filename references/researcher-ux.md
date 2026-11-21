# Researcher experience — progressive interface contract

## Approved full website (optional interface)

The user-approved blue site is implemented in `assets/research_site.html`
with a read-only generator `scripts/build_research_site.py`; see
[site operation and safety](research-site-ux.md). It is a **separate
web/browser presentation**, not a claim that a hosted ChatGPT app surface is
already deployed. It reuses the authorized local read-only data projection
and displays unverified cloud status honestly. The original official blue
icon replaces the earlier monogram, and selected methodological alternatives
remain legible with explicit selection styling. Every page preserves the
researcher's decision authority.

## Goal

Meu Artigo must function as a conversational research assistant whether loaded
as a reusable Skill or exposed by the host through an application entry point.
This document governs presentation only. It is not a new scientific method,
a new project state, a hidden screen, or a request for extra source collection.

The researcher never has to understand internal file names or command syntax
before seeing meaningful progress. Keep the dialogue in the language of the
researcher's current messages; choose terminology for their disciplinary
context without changing original research questions.

## Four useful entrances

| Researcher request | First response | Next optional interaction |
| --- | --- | --- |
| Start a paper | Identify the exact original idea and explain the storage prerequisite; ask **one** decision only if needed | Explore disciplinary and methodological paths, with justification and limitations |
| Continue / next | Load actual authorized continuity records; show current safe action and its blocker | Open C.A.D.A., source evidence, or the required human decision |
| Show my project | Display the grounded overview; mark unavailable items honestly | Toggle between overview, methods, tasks and full details |
| Compare approaches | Show 2–3 legitimate alternatives with applicability, trade-offs and consequences; never rank as universally best | Researcher chooses, proposes another option, or requests further evidence |

Never force the researcher through a rigid wizard when they already specified
the research question, target journal, method, or desired step. User messages
update named choices only; do not repeatedly request answered information.
New projects still respect the Drive-first authorization gate.

## Storage-location disclosure

On new projects, first explain that the intended location is
**My Drive / Meu Artigo / [each article's own folder]**. Show whether the
container was reused, requires a guarded first creation, has duplicates,
or is not yet verified. Do not ask researchers to choose arbitrary
Drive parent folders. If a project exists in an old nested location,
explain the discrepancy and offer a documented migration decision;
viewing a control never moves folders or overrides scientific work.

## Overview: one first-screen briefing

- **Which paper/project?** Actual name and source, or "no authorized project selected".
- **Where am I?** Actual recorded stage, not inferred from chat activity.
- **What can happen now?** One safe next action from recorded continuity,
  stating who must act (researcher versus technical assistant).
- **What blocks it?** The most important verified dependency with why it matters.
- **Can I trust this screen?** The observation source, last verified timestamp
  if actually available, synchronization state and important unknowns.

Only show a compact operating fraction when both numerator and denominator are
recorded (for example 2/5 *method fields*). Never show a total paper quality
score, "87% article complete", invented productivity benefit, editorial
acceptance, approval not observed, or "connected" just because an icon exists.

## Guided methodological choices

For each consequential choice, use a short selectable comparison based on the
actual method route and eligible evidence, not a random catalog. Offer
"other / none of these" and a concise explanation of the consequences.
Separate method proposal from researcher decision: merely pressing, selecting,
viewing or drafting a card is NOT authorization to write a canonical record.
If a host can capture a selection, treat it as draft until the governed human
decision process captures attribution and evidence in authorized storage.
Avoid stacked questionnaires and huge forms; ask one useful decision at a time.

## Information architecture and accessibility

Default visual order: Overview → Methods → My justification → C.A.D.A. →
All details. Native hosts may use compact tabs or segmented controls; the
offline research workspace offers real keyboard-accessible focus buttons.
Changing tabs, filtering, opening a detail, preparing a message and toggling
MINIMAL/FULL are read-only presentation operations.

C.A.D.A. must remain the four existing columns:
ID Tarefa | Tarefa | Responsável execução | Prazo.
All seven scientific gates are preserved in the underlying canonical state;
the panel may report their verified summaries but cannot approve them.

Use plain language for errors and missing capabilities:
- "Aguardando autorização para gravar no Drive" instead of a silent failure.
- "A última sincronização não foi verificada" instead of "Tudo atualizado".
- "Falta validar a decisão metodológica" instead of "Erro GATE-0002".
- Keep technical IDs available in expandable detail or grounded evidence,
  not as the user's only explanation.

## Explicit next-action contract

When a user asks "next" or "próximo", respond with exactly one recommended
next action, its actual recorded evidence and one blocker if relevant.
If blocked, explain the dependency and give a *read-only* safe alternative.
Do not execute a scientifically consequential write because the user clicked
a navigation action or asked to see a screen. Require the same attribution,
authorization and evidence that the canonical workflow already requires.

## Continuation prompt privacy

The offline workspace has a button to prepare a continuation message for
the researcher to copy manually into chat. It uses the safe continuation
action code and generic directions only; it never includes private source
text, task descriptions, personal notes, names of reviewers, access tokens
or original scientific conclusions. This control does not send any network
request or silently save a decision.

## Native interaction fallback

When the active host offers actual interactive controls, use only supported
components and enable state only for presentation or clearly identified draft
choices. Never render fake buttons. If the host cannot render widgets,
give the same brief, actionable overview in text. A richer host does not
require a new login or a second authoritative research workspace.

## Prohibited claims

The UI does not prove that the external connection exists, canonical files
were retrieved, the method was validated, a human reviewed the gate, or the
researcher gained productivity. Measure those separately with a prospective
research design. Tests here validate software behavior only.
