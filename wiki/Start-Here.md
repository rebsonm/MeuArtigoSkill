# Start here


> **Last planned experimental beta: `v0.9.0-beta.6` (release preparation, 2026-10-15).** The cumulative continuity, conversational resume and safe blocker guidance update is documented in [beta.6 release notes](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/NOTAS-DA-VERSAO-0.9.0-beta.6.md). **Beta.5 remains the latest published installer until GitHub actually publishes beta.6 and its checksum.** This last-beta designation is a plan, not stable certification; the project-owned MCP service and MCP Apps UI are not live-validated. Existing installations do not auto-update.

> **Publication status:** [v0.9.0-beta.5](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.5) is the **recommended published experimental beta** (October 14, 2026), with its installable ZIP and checksum available. It is not a stable or scientifically validated release. Installed Skills do not automatically update.

Meu Artigo supports researchers who want an **auditable path from a research question to a manuscript**. You do not need to know Git or Python to use a published Skill package, but you do need a supported assistant and authorized storage.

## Five steps

1. **Download the correct release.** The recommended published experimental installer is [MeuArtigoSkill-v0.9.0-beta.5.zip](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.5/MeuArtigoSkill-v0.9.0-beta.5.zip), not GitHub's generic source-code ZIP.
2. **Install where supported.** Use the platform's real Skills import, or a supported local Skill directory. Not all accounts/platforms offer the same tools. See [[Installation]].
3. **Describe your own research problem.** The Skill should preserve the original wording and may propose research questions for your review.
4. **Check connectivity and storage.** The default `GOOGLE_DRIVE_FIRST` policy requires a confirmed Drive **write** (and an actual read-after-write where used); merely seeing a connected app is not sufficient. A fallback needs your explicit authorization.
5. **Confirm substantive scientific choices.** In particular, the method, source inclusion, interpretation and submission decisions belong to a real researcher.

## A reusable first message

```text
I want to develop a scientific article with Meu Artigo.
My research problem is: [write the real problem].
First verify the actual available tools, Google Drive read/write
access, and the canonical location of the project.
Preserve my original wording. Propose appropriate methodological
routes and explain the trade-offs without treating a proposed
choice as my approval. Show the next useful step.
```

A project already under way should **not** be restarted from scratch. Ask the assistant to locate its authorized `CONTINUIDADE.md`, protocol, canonical matrix and last genuinely recorded decisions. Do not substitute another project's documents or reconstruct prior work from chat memory.

## What to expect during research

- Evidence claims tagged **[L]**, **[I]** or **[P]** according to their provenance.
- Method-specific steps rather than one mandatory literature-review recipe.
- C.A.D.A. tasks with an actionable next step, owner and deadline.
- Clear notices about blocked external access, inaccessible full text and pending human gates.
- A manuscript checked against **verified** journal instructions when a target journal exists.

The assistant may prepare technical material between decision points, but it must not pretend that a database search, independent human screening, empirical analysis or submission occurred.

**Deep reference:** [Getting started](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/COMECE-AQUI.md) · [First-use checklist](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/CHECKLIST-PRIMEIRO-USO.md) · [[Research workflow|Research-Workflow]].
