# Experimental public beta installation — Meu Artigo

**Experimental beta for external testing:** `0.9.0-beta.4` (prepared for the separate prerelease publication workflow; availability must be checked on GitHub).
**Status:** public experimental beta for voluntary use,
not a scientifically validated research method.

**Previously published experimental beta:** [beta.1 Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.1/MeuArtigoSkill-v0.9.0-beta.1.zip). Until the beta.4 prerelease assets appear, this older beta remains an option. Neither release is stable.

## Obtaining the package

Once available, download the **[prepared beta.4 Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.4/MeuArtigoSkill-v0.9.0-beta.4.zip)** from its published tagged prerelease.
Use that version's `SHA256SUMS.txt` to check integrity. The source file
and prepared metadata alone do not mean this release has been published;
if it is not yet visible, earlier beta releases remain available.
The alternative **Code → Download ZIP** is a repository source snapshot
rather than the specially prepared, versioned Skill installer. The source
on `main` may be newer than the last published distribution.

The Skill ZIP contains `SKILL.md` in its root, plus
`agents/`, `assets/`, `references/`, `scripts/`,
`docs/`, `LICENSE`, `NOTICE`,
`CITATION.cff`, `VERSION` and a SHA-256 manifest.
User data, copyrighted third-party PDFs, access tokens,
temporary working files and real private research corpora
are **not included**. Development benchmarks, tests and release-maintenance
scripts remain in the source repository, not in the prepared installer.

## Installation and first run

Installation mechanisms depend on the platform and the
researcher's actual account. Use the appropriate
[ChatGPT](CHATGPT.md), [Claude](CLAUDE.md) or
[Gemini](GEMINI.md) guide and the
[compatibility matrix](COMPATIBILIDADE-PLATAFORMAS.md).
Not every platform offers Python execution, external
connectors or identical storage.

1. Check the ZIP version and, when appropriate, verify
   its digest against the matching `SHA256SUMS.txt`.
2. Import the official package where Skills are supported.
   For directory-based tools, unpack while keeping
   `SKILL.md` at the Skill root.
3. Start a **new** project with the real research problem;
   never substitute another project's data or decisions.
4. Confirm authenticated, **writable Google Drive** access
   before substantive work. Use an alternative workspace
   only after explicitly affirmative authorization.
5. Supply the target journal and actual author rules
   when already chosen. Never invent AI disclosure
   requirements or journal permissions.
6. Keep substantive scientific choices and real
   evidence under the researcher's responsibility.
   Do not simulate human reviewers.
7. Check PDF redistribution rights and final-file
   anonymization before any external sharing.

The [first-use checklist](CHECKLIST-PRIMEIRO-USO.md)
can guide this process without new worksheets or IDs.

## English source, automatically localized conversation

The English-source migration is included in the official `v0.9.0-beta.1` release. The AI assistant
nevertheless responds in the language of the researcher's
substantive conversation messages unless they explicitly
request otherwise. No translation pack is installed.
The scientific manuscript language follows an independent
journal or researcher decision:
[language policy](../references/language-policy.md).

An earlier beta.1 ZIP does **not** contain the later workflow, optional
bibliographic adapters or C.A.D.A. stabilization. For external testing of
these changes, use the matching beta.4 ZIP **only after it has been
published**, rather than substituting the source checkout.

## Compatibility still requiring evaluation

Vendor documentation that a product supports importing
Skills does **not** demonstrate that this Meu Artigo
beta has completed an actual end-to-end project
in that product. Follow the compatibility matrix
and the [pending validations](VALIDACOES-PENDENTES.md).
The same caveat applies to multilingual replies.

## Offline engineering checks

In the project repository or approved local environment
with Python 3.10+:

```bash
python scripts/release_audit.py
python -m unittest discover -s tests -v
python scripts/smoke_test_provenance.py
python scripts/audit_source_language.py
python scripts/build_skill_bundle.py
```

These scripts test code structure, regression cases,
provenance integrity and release packaging. They may
use disposable test fixtures; that does **not**
constitute empirical research into article quality.

## Updating existing projects

Before adopting a new Skill release, preserve original
research files, frozen decisions, real source exports
and backups. A newer Skill package must not silently
rewrite past scientific records or prove a Google Drive
synchronization that did not occur.

Check the release notes for data/schema migration needs.
The current development source on `main` may contain features not included
in the officially recommended beta.1 Skill ZIP. Refer to [contributing](../CONTRIBUTING.md)
and [security](../SECURITY.md) for safe feedback.

## Scientific limitations

Successful code tests do not prove complete academic
rigor, causal gains from C.A.D.A., general production
reliability, access to paid APIs, universal journal
compliance or identical execution across platforms.
Actual scientific and operational evaluations
remain pending.
