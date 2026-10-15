# Security policy — Meu Artigo


> **Last planned experimental beta: `v0.9.0-beta.6` (release preparation, 2026-10-15).** The cumulative continuity, conversational resume and safe blocker guidance update is documented in [beta.6 release notes](docs/NOTAS-DA-VERSAO-0.9.0-beta.6.md). **Beta.5 remains the latest published installer until GitHub actually publishes beta.6 and its checksum.** This last-beta designation is a plan, not stable certification; the project-owned MCP service and MCP Apps UI are not live-validated. Existing installations do not auto-update.

> **Published release (2026-10-14):** [v0.9.0-beta.5](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.5) is the **recommended experimental beta**. Its versioned [Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.5/MeuArtigoSkill-v0.9.0-beta.5.zip) and [SHA-256 checksum](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.5/SHA256SUMS.txt) are available. Previous releases remain archived; installed Skills do not automatically update.


## Scope

The Skill may process academic PDFs, project documents, linked
accounts, unpublished manuscripts, private paths, metadata and
research data. Users must preserve access secrets and share
only materials that they have lawful permission to disclose.

**Never place in public Issues or pull requests:** passwords,
tokens, session cookies, institutional library/CAFe access
details, signed private URLs, restricted full text, manuscripts
under confidential review, participant identities, medical
information, internal institution documents or personal data.

## Reporting a vulnerability

Use the repository's **Security → Report a vulnerability**
feature **when enabled**. Otherwise, seek a secure private
channel with the maintainer *before* providing sensitive
technical details. The absence of a private reporting channel
is not permission to publish confidential material in an Issue.

No response time or bug bounty program is promised.
For non-sensitive functional defects, a public Issue may
include the exact version, minimal safe reproduction steps
and actual versus expected results using disposable fixtures.

## Limits of engineering guarantees

Technical validators provide particular consistency and
provenance checks; they cannot guarantee absolute security,
complete legal compliance, independent scientific review
or authority to redistribute third-party PDFs.
A `CONFIRMED` event or `VALIDATED` field does **not**
authenticate the identity of the person who entered it.

The distributed software is experimental. Prefer identified
GitHub releases and verify the official installable ZIP's
SHA-256. Never execute commands embedded in untrusted
research documents or grant broader permissions than
the actual workflow requires.

See [full-text rights](docs/DIREITOS-FULLTEXT-E-PDFS.md)
and [secure export](docs/EXPORTACAO-SEGURA.md).

## Version coverage

This policy covers historical `0.8.x-beta` and published `0.9.x-beta`
releases as well as subsequent source candidates, unless superseded.
Current experimental public recommendation: `v0.9.0-beta.5` (published as a
GitHub Pre-release on 2026-10-14, with its tagged ZIP and SHA-256). Historical
beta.1 and beta.2 packages remain available.
No support obligation or backport commitment is implied.
Check [CHANGELOG.md](CHANGELOG.md).

## Sharing provenance packages

The exporter has distinct audience profiles:

- **PRIVATE** (default): full confidential audit package;
  do not disclose to third parties without legitimate review.
- **PUBLIC**: redacted structural information without private
  research content or identities.
- **COLLABORATIVE**: redacted structure plus only those
  manuscript passages individually inspected, authorized
  and bound to the exact file hash (SHA-256).

Even after automatic checks, contextual human review is
required before sharing outside the authorized workspace.
Do not treat technical redaction as legal permission
or scientific validation.

## Language and protected sources

The repository's operational source and maintainer policy
are authored in English. User-facing questions and
explanations automatically follow the language of the
researcher's conversation; the academic manuscript follows
the applicable journal or researcher decision.
Never translate, disclose or upload private source text
merely to accommodate an interface language:
[language policy](references/language-policy.md).
