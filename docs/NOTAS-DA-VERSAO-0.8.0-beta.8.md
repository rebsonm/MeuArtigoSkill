<a id="meu-artigo-versão-beta-080-beta8"></a>
# My Article — beta version 0.8.0-beta.8

Updated **Step 1: Export Security, Attribution, and Distribution Policy**.

<a id="alterações-realizadas"></a>
## Changes made

- Adopted the full **Apache License 2.0** for distribution of the current version, with **NOTICE** file attributing authorship to Rebson de Morais Mendes.
- Updated README, CITATION.cff, CONTRIBUITING, release audit and packager to identify **Apache-2.0** and preserve attribution in ZIP.
- Separation of provenance export into public ones **PRIVATE** (full internal audit, standard), **PUBLIC** (only written technical structure, no research records) and **COLLABORATIVE** (written structure and, optionally, manuscript texts individually reviewed by human and linked to SHA-256).
- Blocking full texts in external packages and rejecting files with improper paths, symbolic links, bytes changed after review or evident patterns of credentials/personal data.
- Added regression adversarial testing and safe export guide.
- Corrected inappropriate residual reference in the security policy; Current documentation should not reveal the names of privately consulted collections.
- Git history and previous releases **have not been rewritten**; Versions already distributed under MIT retain their respective permissions.

<a id="limitações-e-responsabilidades"></a>
## Limitations and responsibilities

Apache-2.0 requires preservation of relevant license notices and NOTICE and indication of modifications, **does not require formal academic citation** as a condition of use. The citation suggested in CITATION.cff is recommended, not required by the license. The code license does not automatically apply to third-party texts, PDFs, and scientific documents.

Redacted external packages **do not replace** complete private records or demonstrate scientific validity of the research. The human review claim is verifiable for the files and their hashes, but the reviewer's identity and authorization are **not authenticated by the code**. Publishing or sharing requires legal, ethical and editorial review on a case-by-case basis.

Mandatory protection of the main branch depends on GitHub administrative configuration; is not claimed to be implemented by this release. Empirical assessments of scientific quality remain pending.