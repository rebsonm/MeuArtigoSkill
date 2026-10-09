<a id="anonimização-de-arquivos"></a>
# File anonymization

My Article adopts anonymization by default for external files when the identity of the authors is not necessary.

The rule is simple:

`arquivo interno identificado -> derivado externo anonimizado -> auditoria -> revisão humana -> envio`

<a id="o-que-é-verificado"></a>
## What is checked

Before sharing or submitting a file for blind review, Skill must check visible content and hidden information, including:

- names of authors and co-authors;
- affiliations, departments and institutions;
- emails, ORCID, telephone and other identifiers;
- acknowledgments, financing and copyright contributions that reveal authorship;
- names of organizations, participants or locations when confidentiality requires;
- comments and change control;
- author/creator and "last modified by" in the file properties;
- local computer paths;
- private links;
- names of the files themselves;
- notes, hidden sheets and image/PDF metadata where applicable.

Skill should not consider a document anonymous just because the name does not appear on the first page. In `EXTERNAL_ANONYMIZED` files, the default is `ZERO_NONESSENTIAL_METADATA`: no identification of the software or generation process can remain. Fields such as Author, Creator, Producer, Generator, Application, Company, creation/modification, XMP, EXIF, IPTC and equivalents should be removed when they are not technically necessary to render the file. Therefore, “generated with Python”, `pypdf`, ReportLab, Matplotlib, LibreOffice or another generator is also treated as a metadata leak.

<a id="perfil-confidencial"></a>
## Confidential profile

Each project has an internal file:

`00_Gestao_e_Continuidade/ANONYMIZATION_PROFILE.json`

It records the terms that need to be searched for before an external release. This file is confidential and does not appear in packages sent to the magazine, evaluator or third party.

<a id="arquivos-internos-e-externos"></a>
## Internal and external files

Internal files can maintain authorship when this is necessary for project management.

For external circulation, the default rule is `EXTERNAL_ANONYMIZED`.

Identified files, such as cover page, declaration of authorship, ORCID or journal form, are generated separately when required.

<a id="auto-citação"></a>
## Self-citation

The Skill does not automatically remove self-citations. The journal's policy must be followed to prevent anonymization from damaging the integrity of references.

<a id="sanitização-e-auditoria"></a>
## Sanitization and audit

The sequence for anonymized files is:

`python scripts/sanitize_metadata.py <arquivos> --in-place`

followed by:

`python scripts/audit_anonymization.py <projeto> <arquivos>`

The sanitizer removes descriptive properties/provenance and normalizes package metadata when this can be done without altering the scientific content. If a format cannot be safely cleaned, it fails and the file remains locked. Comments or revisions that may change the content are not silently accepted/rejected.

The auditor analyzes the files actually intended for sharing and generates reports on:

`06_Submissao/Anonimizacao/`

GATE-0007 release for submission should not be approved while there is a high-risk finding or unresolved required review.

The full specification is at [references/anonymization.md](../references/anonymization.md).