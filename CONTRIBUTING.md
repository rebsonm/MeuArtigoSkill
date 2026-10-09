# Contributing to Meu Artigo

The repository is public and distributed under Apache License 2.0.
This experimental beta welcomes documentation corrections,
engineering contributions and methodologically grounded feedback.
**Contributing does not authorize disclosure of protected academic
texts, third-party projects, account credentials or personal data.**

## Before contributing

1. Read the [beta installation guide](docs/IMPLANTACAO-BETA.md),
   [pending validations](docs/VALIDACOES-PENDENTES.md) and
   [security policy](SECURITY.md).
2. Check existing Issues. Describe the observed behavior, exact
   Skill version, steps, expected and actual results.
   Do not claim human participants or evaluations that did not occur.
3. For source changes, create a branch and a pull request to
   protected `main`. Preserve established schema and ID
   compatibility; do not introduce new sheets or paid services
   without a documented need and review.
4. Run `python scripts/release_audit.py`,
   `python -m unittest discover -s tests -v` and
   `python scripts/smoke_test_provenance.py`. Describe
   which controls were affected, without publishing sensitive data.
5. Distinguish engineering regression tests from independent
   scientific evaluation. Synthetic fixtures are suitable for
   disposable **software tests only**, never evidence presented
   as a real research corpus or publication.

## English source and user-language interaction

All maintained contributor documentation, source instructions and
software-provided human-facing text should be authored in **English**.
A researcher **does not have to interact in English**: the installed
Skill follows their direct conversation language automatically.
The manuscript language is independently chosen by the
researcher or required by the journal. Consult
[language policy](references/language-policy.md).

When modifying language-sensitive behavior, preserve
technical identifiers, original source quotations and existing
files' scientific provenance. Run
`python scripts/audit_source_language.py` to identify
untranslated documents. The manual release workflow requires
`python scripts/audit_source_language.py --strict`,
followed by editorial review; no automated language detector
proves translation equivalence or live multilingual accuracy.

## Scientific integrity requirements

Every consulted source, executed query, decision and conclusion
needs authentic evidence appropriate to its claim. Never invent
a DOI, execution, reviewer, study, efficiency metric,
comparative result, editorial acceptance or causal effect.
Document uncertainty, bias, full-text rights and genuinely
performed human review.

A proposed change to methodology must identify the actual
foundation, the problem being addressed and its consequences
for existing decision and evidence safeguards. Do not copy
substantial copyrighted third-party text into the repository.

## Security incidents

Do not use public Issues to disclose tokens, private user
data, confidential PDFs or vulnerability exploitation details.
Follow [SECURITY.md](SECURITY.md), using a private report
channel where available.

## Maintenance and attribution

Contributions are technically reviewed; submission is not
automatic acceptance. Beta versions use explicit identifiers.
Backward-incompatible changes require changelog entries
and consideration of real existing research workspaces.

The current repository is licensed under **Apache-2.0**.
Redistributors of modified work must preserve applicable
copyright and NOTICE attribution, include the license and
indicate changed files as required by the terms. The software
citation suggested in `CITATION.cff` is recommended, **not**
an additional license obligation. Respect third-party
copyright and independent contribution rights.

## Release workflow

Changes follow branch → pull request → required
`audit` → protected `main`. Follow
[releases and versioning](docs/GUIA-DE-RELEASES.md)
for metadata synchronization and deliberate manual publishing.
Merging to `main` does not publish a new beta.
No successful CI job justifies claiming real scientific
validation or operational benefit.
