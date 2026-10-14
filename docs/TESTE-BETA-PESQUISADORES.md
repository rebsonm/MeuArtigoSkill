# Meu Artigo — short external beta-testing guide

> **Release status (2026-10-14):** `0.9.0-beta.5` is the current source candidate and still requires manual tagged publication. Until its ZIP and checksum are confirmed, install the [published beta.4 Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.4/MeuArtigoSkill-v0.9.0-beta.4.zip). The beta.5 documentation describes the upcoming corrective release, not an installed upgrade.


**Upcoming corrective release under evaluation:** `v0.9.0-beta.5` (source candidate, not
stable or independently scientifically validated).

Thank you for evaluating a research-support Skill. The goal is to find
practical usability and scientific-governance problems, **not** to provide a
testimonial or endorse the quality of generated articles.

## Getting started (about 10 minutes of setup)

1. Download the ZIP and `SHA256SUMS.txt` from the
   [currently published beta.4 tagged release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.4) until the beta.5 release assets exist.
   The beta.5 release candidate cannot be installed from a published beta.5 ZIP until the manual publication succeeds. If a download
   is temporarily inaccessible, do not substitute a source tree or claim
   to have installed it; check the actual published release status.
2. Check the SHA-256 when you can. Import the ZIP using your platform's
   supported Skill mechanism. A ZIP alone does not grant external services
   or account permissions.
3. Start a **new** conversation and use a public or synthetic research
   problem. Suggested first message:

   > Quero iniciar um artigo científico usando Meu Artigo. Antes de avançar,
   > verifique quais conexões e formas de armazenamento estão realmente
   > disponíveis. Não simule buscas, decisões humanas nem arquivos salvos.

4. Follow the flow naturally. Say `próximo` when appropriate, and
   observe whether the next step is clear. If a human methodological
   decision is required, make it deliberately; do not treat an AI
   recommendation as approval.
5. When convenient, compare the simplified and full project views in
   your supported host. Record if tasks, dates or blockers appear incorrect.

## Initializer resilience — focus of beta.5

- Start with a public or synthetic research topic and confirm that the research protocol and continuity records are available before the visual matrix is ready.
- If optional spreadsheet generation times out or fails, check whether the core project remains usable and that the failure is reported honestly.
- Reopen a partially initialized test workspace and observe whether existing researcher notes are preserved.
- Report whether the system distinguishes a locally generated workspace from a **verified canonical Google Drive** save.
- Never attempt destructive recovery of an existing research workspace solely for beta testing; work in a disposable test project.

## Optional 20–30 minute research tasks

- **Getting started:** from a real problem to a clearly bounded question.
- **Source honesty:** plan a search without claiming it was executed;
  when authorized, import a real small public bibliographic export.
- **Methodology:** check whether the proposed article/review route fits the
  research question; note unsupported claims or invented criteria.
- **Continuity:** close and reopen the conversation, then request
  `próximo`; check that it reads actual project state and respects pending
  human review.
- **Transparency:** inspect whether [L] literature, [I] inference and [P]
  original proposal are clearly separated.
- **Usability:** note any step where you do not understand what happens next.

These are invitations to observe behavior, not a requirement to complete an
article. **Do not fabricate sources, interviews, scientific approval or
participants in order to finish a test.**

## What to report

Use the repository's
[beta feedback form](https://github.com/rebsonm/MeuArtigoSkill/issues/new/choose).
A helpful report includes:

- Actual Skill version, environment/platform and installation method.
- What you tried, what you expected and what actually happened.
- Whether this blocked progress, risked an incorrect claim, exposed data or
  merely caused confusion.
- Sanitized reproduction steps and a non-sensitive example, if possible.

**Please do not post access tokens, personal/participant information,
unpublished manuscripts, institutionally restricted PDFs, or private Drive
links.** For a security or privacy vulnerability use
[SECURITY.md](../SECURITY.md) instead of public Issues.

## What happens to feedback

Reports are grouped by impact and recurrence, triaged, and corrected only
when justified. Suggested features do not become automatic development
commitments. Public issue visibility does not waive copyright, privacy or
intellectual-property rights.

**Beta feedback does not constitute independent academic validation**.
Publication of a `v1.0.0` stable release would require a separate decision.
