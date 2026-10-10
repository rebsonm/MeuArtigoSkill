# English-source migration — historical record and continuing release gate

## Objective

Move the **maintained repository content** to English while allowing
the installed Skill to converse automatically in the researcher's own
language. This is a repository-language change, **not** a request to
translate the user's study data, source quotations, paper title or
the manuscript itself. See [language policy](../references/language-policy.md).

The Skill remains **Meu Artigo**; C.A.D.A. stays C.A.D.A.; existing schema
values, original filenames/identifiers, paths in integrations and old links
must remain compatible unless a separately documented safe migration
changes their consumers. Original published license grants and Git
history are not rewritten.

## Translation targets and acceptance criteria

1. The root `SKILL.md`, `README.md`, contributor-facing files,
   OpenAI/Claude/Gemini adapters and installation guides are in English.
2. Current methodological, privacy, research-governance and security
   documentation is in English **without weakening or silently
   reconciling its scientific claims**.
3. Human-readable strings and instructional comments in maintained
   Python, YAML and relevant JSON sources use English where they are
   software-provided UI text. User-provided research input remains
   untouched; technical enums/IDs/CLI flags are stable.
4. Historical release notes and changelog contents are translated
   faithfully when included as maintained repository documentation.
   Preserve scientific bibliography entries in their correct published
   titles and original direct quotations, clearly labeled as such.
5. All local Markdown links, legal notices, generated ZIP contents,
   canonical table schemas and tests remain valid.
6. A conservative Portuguese indicator scan reports **zero outstanding
   substantial source documents**; human review is still required
   because heuristic language detection cannot prove translation quality.
7. Verify automatic replies from the researcher's current direct
   message and distinct journal/manuscript language with real
   interactions before claiming cross-platform behavior has been
   empirically demonstrated.

## Engineering controls

The source inventory can be run with:

```bash
python scripts/audit_source_language.py
python scripts/audit_source_language.py --strict
```

The first command **reports** outstanding files without blocking
incremental engineering Pull Requests. The second returns a nonzero
status if significant Portuguese prose remains. The manual
`Publish beta` workflow runs `--strict`, therefore a repository
with incomplete English migration **cannot publish a beta advertised
as English-source-complete**.

The detector counts distinctive Portuguese-language indicators. It
does **not** inspect semantic equivalence, prove a particular source
was translated correctly, detect all languages, or interpret
bibliographic titles. Its findings need human editorial review.
Previous published beta packages are retained and not rewritten.

## Release preparation and public claims

This was the preparation plan for the English-source migration that shipped
in the published `v0.9.0-beta.1` on 2026-10-09. It is retained to document
historical decisions and the ongoing English-source release gate; it is not
an instruction to republish `v0.9.0-beta.1`. On 2026-10-10, `main` includes
an **unpublished** `v0.9.0-beta.2` source candidate. Passing source-language
scans does not replace independent editorial or installed-platform tests.

When the migration is actually complete:

- create truthful notes describing implemented engineering features,
  not fabricated research quality or empirical outcomes;
- update the canonical `VERSION`, README, `CITATION.cff`, changelog,
  published-version links and the real release date together;
- pass `audit`, bundle/hash verification, language strict check,
  privacy and link checks;
- publish a **new immutable prerelease** using the manual GitHub
  workflow; never replace or force-move existing tags;
- inspect the published ZIP, checksum and release description.

The experimental scientific validation items remain pending and
are **not** prerequisites for releasing accurately labeled beta code.
