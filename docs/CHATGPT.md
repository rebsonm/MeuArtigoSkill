# ChatGPT — Meu Artigo Skill

> **Release status (2026-10-14):** `0.9.0-beta.5` is the current source candidate and still requires manual tagged publication. Until its ZIP and checksum are confirmed, install the [published beta.4 Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.4/MeuArtigoSkill-v0.9.0-beta.4.zip). The beta.5 documentation describes the upcoming corrective release, not an installed upgrade.


Meu Artigo is distributed as a **Skill**. Check whether your account supports Skills import and what external tools and storage are actually authorized.

## Install

Get the [published beta.4 Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.4/MeuArtigoSkill-v0.9.0-beta.4.zip) and [SHA-256](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.4/SHA256SUMS.txt) until beta.5 assets are published. This is an **experimental Pre-release**, not a stable or independently validated research tool. The [historical beta.1 ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.1/MeuArtigoSkill-v0.9.0-beta.1.zip) remains archived. Do **not** use GitHub's **Code → Download ZIP** source snapshot as the user-installation archive. See [installation help](INSTALLATION.md).

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

A Skill's operation and generated artifacts depend on the real tools available. It cannot assert external article submission, publisher content access or data synchronization without evidence.
