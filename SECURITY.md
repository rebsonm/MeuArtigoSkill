# Security policy — Meu Artigo

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

This policy covers the published `0.8.x-beta` line and
subsequent releases unless explicitly superseded.
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
