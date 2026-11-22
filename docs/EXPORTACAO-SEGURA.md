<a id="exportação-segura-de-proveniência-separação-por-público"></a>
# Secure provenance export — separation by audience

This document defines three **distribution profiles**, implemented in `scripts/export_provenance.py`.
No profile grants rights to share protected academic material, confidential
manuscripts, personal data, or embargoed content.

<a id="1-private-auditoria-interna-padrão"></a>
## 1. PRIVATE — internal audit (standard)

```bash
python scripts/export_provenance.py /path/to/project --audience PRIVATE
```

This profile maintains the full provenance package, internal records, controls,
and eligible canonical files, according to the rights rules for full texts.
The package has the prefix `RO_CRATE_PRIVATE_` and **must not be redistributed**
without a separate authorization and confidentiality review. Your data may include names, decision history,
citations, comments, documents under review, and personal identifiers.
The fact that a SHA-256 matches the files does not mean the absence of sensitive data.

To include full texts in the **private** export, it is still required
`--include-fulltext --confirm-rights-review` and the individual rights records,
as per [full file rights](DIREITOS-FULLTEXT-E-PDFS.md).
**Nor does this mechanism legally authenticate redistribution permission.**

<a id="2-public-estrutura-neutra-sem-dados-da-pesquisa"></a>
## 2. PUBLIC — neutral structure, without research data

```bash
python scripts/export_provenance.py /path/to/project --audience PUBLIC
```

Generates RO-Crate structure with technical description and PROV graph **deliberately
redacted**, without project names, records, evidence, searches, texts,
documents, metadata of scientific identifiers or corpus. Not accepted
inclusion of full texts nor exceptions per file manifest.

**Explicit functional limitation:** is an artifact of transparency about the
export limit, **not an auditable public reproduction of the research**.
It should not be described as a complete package or independent evidence
the quality of the manuscript.

<a id="3-collaborative-colaboração-com-arquivos-especificamente-autorizados"></a>
## 3. COLLABORATIVE — collaboration with specifically authorized files

```bash
python scripts/export_provenance.py /path/to/project \
  --audience COLLABORATIVE \
  --approved-files-manifest collaboration-approval.json
```

Without an approved-files manifest, the result is only the neutral structure.
With manifest, it only supports textual files `.md` and `.txt` within the
canonical folder `05_Manuscrito/Versao_Canonica/`, each linked to a
Accurate SHA-256, with declared content review and human authorization.

**Structure of the manifesto, to be completed with true assessment:**

```json
{
  "schema_version": 1,
  "audience": "COLLABORATIVE",
  "reviewed_by": "Actual identity of the authorized reviewer",
  "reviewed_at": "2026-10-09T17:00:00-03:00",
  "review_scope": "Describe exactly what was reviewed: confidentiality, authorization, and intended recipients",
  "files": [
    {
      "path": "05_Manuscrito/Versao_Canonica/ACTUAL_FILE_NAME.md",
      "sha256": "REPLACE_WITH_ACTUAL_64_CHARACTER_SHA256"
    }
  ]
}
```

The example is **an empty template**, not a review performed statement.
The files must be checked manually before creating the manifest.
Byte changes invalidate the previous approval. Symbolic links,
files outside the folder, binary files, obvious personal data and
Typical credential indicators are declined.

Technical standards checking does not detect all forms of information
confidential, moral rights, unpublished material, protected excerpts, data
indirectly identifiable figures or commitments to periodicals. A
**responsibility for this analysis remains human**. The fields
`reviewed_by`/`reviewed_at` are statements, not proof of identity.

<a id="limites-comuns-e-consistência-dos-relatos"></a>
## Common limits and consistency of reports

- Exporting is different from **publishing**. Permission must consider purpose
  and specific recipients.
- External modes never include the complete PROV graph of individual events,
  even when a manuscript has been authorized, to avoid re-identification by
  crossing of IDs and auxiliary fields.
- The report includes the audience profile and warns that external exports
  are reduced; do not declare full coverage of the research.
- Do not place names, private URLs or sensitive documents in public Issues,
  tests, installation packages or release notes.
- For full private interoperability, use `PRIVATE` with restricted distribution
  and the relevant institutional and editorial checks.
- Choosing Apache-2.0 for the **Skill code** does not modify the licenses,
  rights, or confidentiality requirements of **research data and third-party works**.