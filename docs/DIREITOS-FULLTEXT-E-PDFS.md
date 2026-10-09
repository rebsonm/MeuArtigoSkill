<a id="uso-de-textos-completos-licenças-e-direitos-de-redistribuição"></a>
# Full text usage, licenses and redistribution rights

<a id="quatro-permissões-diferentes"></a>
## Four different permissions

1. **Bibliographic discovery:** a DOI, a Crossref/OpenAlex record or a found link identifies a publication. DOES NOT determine license or download permission.
2. **Local access:** reading via institutional library, CAPES/CAFe, repository, publisher or legitimately received file. Legitimate access does not automatically grant permission to publish the PDF.
3. **Scientific analysis:** examine, record and cite excerpts to the extent applicable to the authorization and applicable standards. Do not upload or send full PDFs to external APIs without appropriate authorization.
4. **External Redistribution:** Placing the full copy in ZIP, RO-Crate, website, public repository or shareable file requires compatible authorization **for that specific file**.

The Skill code is public; This does NOT make the PDFs downloaded by the researcher public or licensed under the same license as the code. Metadata, listings and citations do not automatically convey the right to republish the full text.

<a id="registros-sem-novas-planilhas"></a>
## Records without new sheets

The control leverages records with Record_ID from the canonical file
\`00_Gestao_e_Continuidade/04_FullText_Tracker.csv\` and the existing tab
\`08_FULL_TEXT\`. Nine columns were added, preserving the previous ones:

- Access_basis — OPEN_ACCESS, INSTITUTIONAL_ACCESS, PERSONAL_AUTHORIZED, DIRECT_PERMISSION or UNKNOWN;
- Rights_basis — UNKNOWN, ALL_RIGHTS_RESERVED, CC0_1_0, CC_BY_4_0, CC_BY_SA_4_0, PUBLIC_DOMAIN, DIRECT_PERMISSION, INSTITUTIONAL_ACCESS or PERSONAL_ACCESS;
- License_URI — license applicable to the exact version, when applicable;
- Rights_evidence — publication page with specific license or reference to documentary authorization;
- Permission_scope — precise scope, including PUBLIC_REDISTRIBUTION when an individual permission authorizes;
- Attribution_text — credit, license and required notices;
- Source_sha256 — SHA-256 of the document actually stored;
- Rights_reviewed_by — attribution of the document review to a person, NOT independent authentication;
- Rights_review_evidence — verifiable reference to the original review statement.

Documents must remain in the \`03_Screening_e_FullText/FullText_Corpus\` area, linked to the existing column \`File_or_URL\` by **path relative to the workspace**. External links may appear as an access reference, but do not authorize packaging without the verified file.

<a id="conduta-operacional"></a>
## Operational conduct

To register a source, confirm who made the file available, which version was accessed and its access base. Search for a license on the publication's own website or specific authorization from whoever holds the rights; the generic Creative Commons license address **does not demonstrate that a specific article is under that license**. Save the reference to this check in the tracker, keeping the authorization file out of shareable packages when it contains personal information.

**For internal analysis**: authorized files may remain in the private corpus according to effective access rights. In case of uncertain access, register UNKNOWN and do not assume that access was permitted. Lack of full text access should remain \`PENDING ACCESS\`, not DELETE.

**For external export**: The default of \`scripts/export_provenance.py\` remains **no PDFs/full texts**. The \`--include-fulltext\` option now fails without explicit confirmation and without a positive file-by-file hash, license/permission, evidence source, and human review evaluation.It is not allowed to export documents with unknown license, all rights reserved, personal or institutional access as the only basis through the automated flow. The CC BY-NC and CC BY-ND licenses are not treated as general authorization for public redistribution because they carry contextual restrictions; Special cases require legal/human analysis and specific authorization. For CC BY/CC BY-SA you need credit and meet the applicable conditions. Automated verification only ensures consistency of annotations; does not certify the legal validity of the license, the existence of the permittee or that all equal sharing obligations have been fulfilled.

Official support pages:
- CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
- CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
- CC licenses in Brazil: https://br.creativecommons.net/licencas/

<a id="comandos-gratuitos"></a>
## Free commands

Tracker and corpus audit (does not publish files):

\`\`\`bash
python scripts/rights_audit.py /path/of/project
python scripts/rights_audit.py /path/of/project --strict
python scripts/rights_audit.py /path/of/project --check-export
\`\`\`

Export only provenance and standard artifacts without raw PDFs:

\`\`\`bash
python scripts/export_provenance.py /path/of/project
\`\`\`

Only when each document is demonstrably authorized for broad redistribution and the researcher has actually examined the rights documents:

\`\`\`bash
python scripts/export_provenance.py /path/of/project \
  --include-fulltext --confirm-rights-review
\`\`\`

The exporter stops the operation **before** recording the TRACE/EXPORT event, creating ZIPs, or copying fonts when there is not enough documentation. In allowed exports, includes \`provenance/FULLTEXT_RIGHTS.json\` with the document assignments and hashes. The manifesto of rights is an auditable attestation, **not a legal opinion, new authorization or license granted by Skill**.

ZIPs and nested compressed files are omitted from the default package: they could contain unidentified PDFs and bypass rights analysis. Source files with symlinks or paths outside the corpus are also rejected.

<a id="transparência-e-privacidade"></a>
## Transparency and privacy

- Do not store CAFe passwords, library tokens, credentials and cookies in records.
- Do not circumvent paywalls or technological controls to obtain content.
- Do not submit restricted PDFs to templates, AI services, or external repositories without a compatible legal basis and authorization.
- Do not incorporate long protected passages into the public report just to demonstrate traceability.
- The license and review fields are researcher notes; a text attributed to a human can be forged and requires checking.
- The registration of works in the public domain depends on assessment by jurisdiction, protection period and version of the document. A PUBLIC_DOMAIN tag alone is not legal evidence.
- Anonymization controls and journal-specific rules continue to be mandatory and independent.

**Scope of security:** control is conservative, does not replace legal advice and may block distribution that may be legally permitted in a certain context. In this case, review the rights and register an appropriate authorization; Do not remove the block or mark a false license to move forward.

In old projects, new fields remain blank until genuine review. Do not retrospectively complete permissions that were never granted. In new projects, \`fulltext_rights_audit_required=true\` binds warnings and inconsistencies to canonical validation, and the exporter protects redistribution regardless of project configuration.