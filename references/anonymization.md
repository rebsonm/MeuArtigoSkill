# High-rigor anonymization policy

## Purpose

Meu Artigo treats anonymization as a release-control requirement, not as a cosmetic formatting step.

The goal is to prevent a generated or shared artifact from revealing the researcher, coauthors, affiliation, confidential case sites, research participants, account identity, local filesystem paths, hidden document metadata, comments, revision authorship, or other identifiers when those details are not required for the artifact's purpose.

Anonymization must never falsify scientific content. When a detail is methodologically necessary but identity-sensitive, use a neutral placeholder or pseudonym only when scientifically defensible and permitted by the target journal, and preserve the identified original internally.

## Default modes

Use one of three artifact modes:

- `INTERNAL_IDENTIFIED`: internal canonical files may retain identity when operationally necessary.
- `EXTERNAL_ANONYMIZED`: default for files intended for blind review, peer feedback, external circulation, or any sharing where identity is unnecessary.
- `EXTERNAL_IDENTIFIED`: only when the destination explicitly requires identified files, such as a title page, authorship declaration, ORCID form, or non-blind submission artifact.

When the journal or destination is unknown, external/shareable artifacts default to `EXTERNAL_ANONYMIZED`.

Never overwrite the identified canonical source merely to create an anonymous version. Create a separate derivative and preserve both states.

## Confidential anonymization profile

Maintain:

`00_Gestao_e_Continuidade/ANONYMIZATION_PROFILE.json`

This is a confidential control file. It must never be included in a shareable snapshot, provenance package, blinded submission, or external review bundle.

Canonical profile status:

- `TO_CONFIGURE`
- `CONFIGURED`
- `VERIFIED`
- `NOT_REQUIRED`

The profile may contain identity terms that need to be checked before external release:

- author and coauthor names and variants;
- emails;
- ORCID identifiers;
- affiliations, departments and institutional units;
- institutional identifiers that may disclose authorship;
- case-site names when confidentiality/blinding requires masking;
- participant identifiers;
- account usernames;
- local path tokens;
- other project-specific sensitive terms.

Do not infer that the list is complete. Before a blind-review release, a human must confirm the profile or explicitly document why anonymization is not required.

## What must be checked

### Visible content

Check:

- author and coauthor names;
- affiliations and department names;
- emails, phone numbers, ORCID and personal identifiers;
- acknowledgements;
- author-contribution statements;
- funding statements or grant identifiers that disclose identity;
- ethics/institutional references when they disclose the authors or site;
- phrasing such as "our university", "our laboratory", "our organization" or equivalent;
- case-site and participant identifiers;
- self-identifying repository, project or dataset links;
- figure captions, table notes, appendices and supplementary material.

Do not automatically delete legitimate self-citations. Follow the journal's blind-review policy. When needed, write self-citations in a neutral third-person form or use the journal's prescribed placeholder. Do not distort the bibliography solely to conceal identity.

### File and package metadata

Check and, when the output format permits, remove:

- document creator/author;
- last modified by;
- company/organization properties;
- comments and comment authors;
- tracked-change/revision authors;
- hidden notes;
- custom document properties;
- embedded local paths;
- file URLs;
- template paths;
- EXIF or image metadata when relevant;
- spreadsheet hidden sheets/notes containing identity;
- presentation speaker notes/comments containing identity;
- PDF metadata;
- filenames that contain names, initials, affiliations, usernames or institutional identifiers.

A visually anonymous document is not considered anonymous if hidden metadata still discloses identity.

## Participant and case de-identification

When empirical material contains information about human participants, organizations, case sites or third parties:

- do not expose direct identifiers unless scientifically necessary and authorized;
- minimize quasi-identifiers that can make re-identification reasonably possible;
- use stable pseudonyms where analytical consistency requires them;
- preserve any confidential identity mapping separately from shareable research artifacts;
- do not copy confidential mapping files into provenance exports or submission packages;
- do not claim that a dataset is anonymous merely because names were removed.

This policy is about information protection and blind-review hygiene. It does not replace ethics review, consent, data-protection obligations or the research protocol when those are applicable.

## Generation workflow

Before producing an external/shareable file:

1. determine its audience and required artifact mode;
2. load the verified journal rules when a target outlet exists;
3. inspect or configure `ANONYMIZATION_PROFILE.json`;
4. generate the external derivative without unnecessary identity;
5. separate identified title-page/declaration artifacts from the blinded manuscript when required;
6. remove hidden metadata/comments/revisions where the format supports them;
7. run `scripts/audit_anonymization.py` on the actual files to be shared;
8. resolve every HIGH finding;
9. visually inspect PDF/image outputs and any item that automation cannot fully inspect;
10. record the audit report and human review;
11. only then release or submit the files.

Do not claim an artifact is anonymous if the audit is missing, failed, or still requires unresolved human review.

## Audit outputs

Store audit reports in:

`06_Submissao/Anonimizacao/`

Suggested filename:

`ANONYMIZATION_AUDIT_<timestamp>.json`

The audit report must not echo the sensitive term itself. It should record category, location, severity and the fact that a configured token matched.

Automated results:

- `PASS`: no unresolved finding and no pending manual visual review.
- `PASS_WITH_HUMAN_REVIEW`: no HIGH finding; non-deterministic/visual checks were explicitly completed by a human and remaining review items were accepted with rationale.
- `REVIEW_REQUIRED`: manual review or medium-risk finding remains unresolved.
- `FAIL`: one or more HIGH-risk findings remain.

## Submission gate

GATE-0007 cannot be approved for an external submission bundle unless:

- the anonymization profile is `VERIFIED` or explicitly `NOT_REQUIRED`;
- `NOT_REQUIRED` has a documented reason;
- the target-journal anonymization rules were checked when a journal is defined;
- the exact outgoing files have an audit result of `PASS` or `PASS_WITH_HUMAN_REVIEW`;
- identified and anonymized artifacts are not accidentally mixed;
- final human review confirms that the released package does not reveal identity contrary to the destination's rules.

## Provenance and snapshots

Internal traceability can remain identified where necessary. External transparency does not require publishing the full private workspace.

Never include `ANONYMIZATION_PROFILE.json` or a confidential identity map in:

- shareable snapshots;
- RO-Crate/W3C PROV external packages;
- blinded submission bundles;
- reviewer-facing supplementary material.

If a provenance package is to be shared during blind review, generate a dedicated external version and run the anonymization audit on that package before release.

## Scientific non-interference

Anonymization may change identity-bearing presentation but must not silently change:

- findings;
- sample size;
- inclusion/exclusion decisions;
- evidence strength;
- methodological facts;
- limitations;
- claim meaning;
- source attribution needed for scientific integrity.

When removing an identifier would make the method misleading or irreproducible, use a transparent neutral placeholder and preserve restoration instructions for the post-review identified version.
