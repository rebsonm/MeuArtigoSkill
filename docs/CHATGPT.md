# ChatGPT — Meu Artigo Skill

> **Published release (2026-10-14):** [v0.9.0-beta.5](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.5) is the **recommended experimental beta**. Its versioned [Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.5/MeuArtigoSkill-v0.9.0-beta.5.zip) and [SHA-256 checksum](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.5/SHA256SUMS.txt) are available. Previous releases remain archived; installed Skills do not automatically update.


Meu Artigo is distributed as a **Skill**. Check whether your account supports Skills import and what external tools and storage are actually authorized.

## Install

Get the [published beta.5 Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.5/MeuArtigoSkill-v0.9.0-beta.5.zip) and [SHA-256](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.5/SHA256SUMS.txt). This is an **experimental Pre-release**, not a stable or independently validated research tool. The [historical beta.1 ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.1/MeuArtigoSkill-v0.9.0-beta.1.zip) remains archived. Do **not** use GitHub's **Code → Download ZIP** source snapshot as the user-installation archive. See [installation help](INSTALLATION.md).

## First connection diagnosis

Use one concise status line per service in the researcher's language. Avoid empty Markdown tables and do not promote installed tools to successful checks. Distinguish **authenticated access**, a confirmed read, a confirmed write, **read-after-write**, an actually executed academic query, and observed provider quota/entitlement.

Without an authenticated receipt report `NOT_VERIFIED`. A successful Drive read is not a verified write. Display final verified state, and the next valid storage decision. Such capability reporting is not a scientific gate approval.

Illustrative statuses — **not actual test results**:

- Google Drive — **not verified**: authorized write still needs a test.
- Literature discovery — **not tested**: no real query was confirmed.
- Python — **not tested**: script execution in this session unconfirmed.

## Scientific contract

Read [SKILL.md](../SKILL.md). The Skill preserves the researcher's question and requires a real human decision at each consequential scientific gate. `GOOGLE_DRIVE_FIRST` storage must be authorized and tested before storing a project. If it is unavailable, obtain explicit user approval before `WORK_FALLBACK`.

For a project already in progress, read its actual `CONTINUIDADE.md`, logs and gates from the authorized workspace. If no project is selected, ask which article to continue rather than generate made-up progress counters.

## Resume safety: one answer from the canonical records

When a researcher asks to continue an existing authorized project, use
`CONTINUIDADE.md`, the canonical C.A.D.A. register, seven human gates,
`17_Decision_Log.csv`, `13_Traceability_Log.csv`, and
`METHOD_PROFILE.json`. The Skill's `native_chat_dashboard.py` projects
these existing records, with `next_step_router.py` selecting the operational
step and `decision_continuity.py` checking recorded method/provenance.
Do **not** start a second project dashboard or infer progress from the chat.

If the DEC register is missing/malformed or the latest recorded decision
lacks an existing TRACE link, report a **reconciliation blocker**. A
structurally eligible C.A.D.A. action is not safely resumable while those
records disagree. In the plain-text view the same blocker must disable
`technical_preparation_possible`. A correctly initialized, readable,
header-only DEC register is different: it means no recorded decision, not
automatically a corrupted file.

Show briefly what is actually known (last decision ID and status, next
existing CADA/GATE ID, actor, first blocker, verification needed), without
exposing private decision prose. A human must decide scientific choices;
the local view neither authenticates people nor verifies Drive sync.
No user action is required for synthetic engineering tests; a real
researcher/operator must reconcile damaged project evidence before work.

A Skill's operation and generated artifacts depend on the real tools available. It cannot assert external article submission, publisher content access or data synchronization without evidence.
