# Meu Artigo — Conceptual RAG in private Google Drive (experimental pilot)

**Status: source-only prototype.** Not integrated with the official Skill ZIP, not published, not validated inside ChatGPT, and not autonomously connected to Google Drive.

## Architecture and strict separation

Google Drive is an **optional private object store** for the researcher's source documents, page-addressable Markdown and persistent indexes. PDF extraction, indexing and similarity calculations take place in an explicitly authorized local execution environment. Google Drive does not run vector similarity or offer a built-in vector database through this module.

The intended private folder layout is:

- \`01_Fontes_Originais\`: authorized source PDFs, preserved unchanged and never committed to a public repository.
- \`02_Biblioteca_MD\`: one Markdown derivative per source and a matching \`.md.meta.json\` sidecar.
- \`03_Indice_Conceitual\`: researcher-reviewed concepts and relations; **not yet automated** by this initial prototype.
- \`04_Indice_Semantico\`: a versioned index containing \`chunks.jsonl\`, \`lexical.sqlite3\`, optional \`vectors.f32\` and \`manifest.json\`.

Although the folder currently has no public sharing, the owner can still edit it. A read-only consumer requires appropriate platform permissions or enforced access scopes, not merely an instruction to the language model.

**Never ship third-party full text, private source excerpts, a Drive connection token or a populated private index inside the public Skill installer.**

## Local PDF-to-Markdown conversion

Install the optional PyMuPDF dependency on the researcher's authorized local executor; neither a PDF nor a model is sent to an external conversion website:

\`\`\`sh
python -m pip install pymupdf
python experimental/conceptual_rag/pdf_to_md.py /PRIVATE/source.pdf /PRIVATE/02_Biblioteca_MD/source.md --source-id SOURCE001 --title 'Example Source'
\`\`\`

Every extracted page receives a \`<!-- source_page: N -->\` locator. The sidecar contains the source and derivative SHA256 digests, page count, low-text warnings and two **unapproved** statuses: \`extraction_status=REVIEW_REQUIRED\` and \`rights_status=NOT_REVIEWED\`.

The converter never grants a license, verifies an academic claim, validates the whole extraction, runs OCR, removes the original or overwrites an existing derivative. Scanned pages, tables, mathematical formulae, illustrations and edition/page mismatches require separate manual inspection.

Once a human **actually** reviews the Markdown against the source and confirms appropriate permitted use, the sidecar may be explicitly updated with \`extraction_status=HUMAN_REVIEWED\` and \`rights_status=PRIVATE_AUTHORIZED\` (or \`PUBLIC_DOMAIN\` only when supported). Recompute \`md_sha256\` after any correction. No test fixture or assistant-generated metadata authenticates a human review.

## Build and query a private persistent index

The standard-library-only baseline supports SQLite FTS5 full-text retrieval:

\`\`\`sh
python experimental/conceptual_rag/rag.py build --library /PRIVATE/02_Biblioteca_MD --index /PRIVATE/04_Indice_Semantico/index_v001
python experimental/conceptual_rag/rag.py query --index /PRIVATE/04_Indice_Semantico/index_v001 --text 'How do integrative and systematic reviews differ?'
\`\`\`

For **genuine vector retrieval**, provide a separately installed, previously provisioned **local-only** SentenceTransformers model to both build and query operations:

\`\`\`sh
python -m pip install sentence-transformers
python experimental/conceptual_rag/rag.py build --library /PRIVATE/02_Biblioteca_MD --index /PRIVATE/04_Indice_Semantico/index_v002 --local-model /PRIVATE/LOCAL_MODEL
python experimental/conceptual_rag/rag.py query --index /PRIVATE/04_Indice_Semantico/index_v002 --text 'Methodological question' --local-model /PRIVATE/LOCAL_MODEL
\`\`\`

The model loader requests \`local_files_only=True\`; absent local support is a blocker, **never** an invitation to download silently. The query path verifies indexed file hashes. If no compatible query encoder exists, it explicitly returns \`LEXICAL_ONLY\`. Reciprocal Rank Fusion is a ranking technique, not a guarantee that retrieved text semantically supports an academic claim.

The index is created at a **new destination** and never silently overwrites previous versions. It contains source excerpts; therefore any synchronized copy must remain private and properly authorized. It is *not* necessarily smaller than the original PDF library.

## Evidence, tests and unresolved acceptance

Synthetic unit tests are located at \`tests/test_conceptual_rag_pilot.py\`. They cover page markers, hash integrity, refusing unreviewed/unauthorized files, non-overwrite, lexical selection, optional hybrid ranking, explicit semantic fallback and read-only queries. Their in-memory toy vectors are an **engineering fixture, not a validated scientific embedding model**.

Requirements before real use:

1. Select 5–10 documents with individually verified access rights. Do not automatically import a personal library or an unrelated project.
2. Manually inspect source/Markdown parity for pages, tables, diagrams and non-searchable PDFs.
3. Register actual model identity, version and licensing; test realistic paraphrases, negative searches, citation accuracy, recall and false-positive behavior.
4. Verify authorized Drive readback, access boundaries and the actual current host. The module itself does not call the Drive API.
5. Document human assessment; preserve [L]/[I]/[P] distinctions and researcher-controlled scientific gates.
6. Keep this experimental branch separate from v1.0.0 release-candidate acceptance. Integration and publishing require new explicit maintainer approval.

**No substantive methodological or manuscript inference is certified by these local software checks.**