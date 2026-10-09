# Gemini adapter — Meu Artigo

Start with the shared [Getting started guide](COMECE-AQUI.md).
The scientific instructions are in `SKILL.md`; this document
covers Gemini-specific installation and runtime limitations.

## Installation and documented format

Google documents importing `SKILL.md`, a directory containing
`SKILL.md`, or a ZIP with that file at the root for eligible
Gemini accounts. Availability depends on product, account and
region; see [official guidance](https://support.google.com/gemini/answer/17094296?hl=en).

1. Download `MeuArtigoSkill-v0.9.0-beta.1.zip` from
   [the published release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.1).
2. Open Gemini's Skills section if it is available in your account.
3. Follow the import flow shown by the actual product and choose
   the prepared ZIP (rather than GitHub's source-code archive).
4. Check that `SKILL.md` and supporting files are recognized.

Being able to import the ZIP proves neither access to Drive
nor capability to run the full research workflow.

## Source language versus response language

The repository's English authoring policy is independent of
the conversation: a Portuguese-speaking researcher receives
Portuguese questions and explanations, a Spanish-speaking
researcher receives Spanish, and so forth unless they
explicitly request another language. The manuscript follows
journal or researcher instructions independently. Read
[the language contract](../references/language-policy.md).

Do not translate machine-readable IDs, commands or source
quotations by default.

## Runtime limitations

Google's published guidance notes that scripts requiring
internet access are not supported **inside imported Gemini Skills**;
binary formats such as `.xlsx` are not suitable reference
attachments for the Skill importer. These limitations are
not an instruction to delete the project's canonical spreadsheet,
which can reside in Google Drive if external tools genuinely
support it.

Do **not** assume `agents/openai.yaml` is applicable here.
Inspect the current platform's capabilities and actual
permissions for persistence, academic discovery, publisher
retrieval, indexed database search, local scripts and optional
C.A.D.A. task-mirror integration.

Scopus and Web of Science may require the researcher's real
institutional access and export. Prepare searches and
import verified files without inventing direct connections
or execution counts.

## Storage, research and continuation

The default canonical research store is Google Drive only
after writable access is checked. If it is unavailable,
explain the connection steps, recheck and ask for explicit
affirmative permission before another Work/local store.
Absent approval, do not begin substantive research in a
silently chosen fallback.

Maintain the researcher's actual source, authorized
`CONTINUIDADE.md` and human decisions; record external
operations as unverified until authentic evidence exists.
C.A.D.A. does not require a third-party work manager to
function.

## Verification status

The installable package's source layout was checked.
Actual Gemini import, authenticated Drive writes,
manuscript output, source checks and cross-session
continuation remain to be evaluated on the real platform.
A fluent response or successful importer does not prove
scientific correctness. See [pending evaluations](VALIDACOES-PENDENTES.md).
