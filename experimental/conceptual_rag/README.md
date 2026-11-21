# GitHub-hosted conceptual methodology knowledge — experimental

**New architecture (2026-11-21):** the GitHub repository is the home of redistributable methodological knowledge, **not Google Drive**. The historical branch name still contains "drive" but the intended published module has no Drive dependency. The official version `v1.0.0-rc.1` and the stable release remain untouched.

- `knowledge/methodology/catalog.json` is a small, public discovery catalog for original editorial concept cards.
- `knowledge/methodology/cards/` holds only authored summaries and bibliographic leads, never reproduced third-party books, full-text PDF conversions or private research data.
- `scripts/consult_github_methodology.py` is the optional lightweight HTTPS client; it **does not download the library at installation** and reads at most matching cards, by pinned Git SHA and SHA256.
- `references/GITHUB-METHODOLOGY.md` describes host prerequisites, fallback and verification.
- `experimental/conceptual_rag/rag.py` remains a separate local-only, optional hybrid index builder, **not connected to remote vectors by this phase**.

## What changed from the earlier pilot

The Drive folders used in the earlier research experiment are **not part of the new architecture**. No books or PDF-to-Markdown derivatives have been copied into the public repository. Those original files are unchanged. This revision does not delete existing user-owned pilot folders, change permissions or claim all of their copies are gone.

Only original cards and individually approved redistributable public PDFs appear in Git. There is no automatic access to private sources, no MCP, no server and no automatic runtime network entitlement from installing a Skill. ChatGPT, Claude and Gemini require their own observed host permissions and execution support.

## Retrieval contract

1. No remote fetch when the Skill is installed, imported or merely started.
2. On an eligible research question, first fetch an immutable, small catalog from the exact, authorized GitHub repository and commit SHA.
3. Rank metadata locally. Download only up to three matching cards by default, verify hashes and return at most 3,300 characters, without injecting the full corpus into context.
4. If unavailable, do not fabricate network access: fall back to bundled core methodology and declare the limitation.
5. Do not treat retrieved editorial guidance as direct scholarly evidence [L], independent review or a completed scientific gate.

**Open tasks:** verify the actual ChatGPT host's ability to fetch GitHub; test full source permissions; evaluate a genuine local embedding model, negative retrieval queries and specialist human review; decide separately how to publish immutable versioned indices. All branch work is draft and not released.


## PDF-first extension (2026-11-21)

**Canonical source format:** keep permitted full-text methodological sources as original PDFs; do not require PDF-to-Markdown conversion. PDF page rendering/visual review is necessary for diagrams, equations, tables and pages without extractable text. Keep indexes and source metadata small, and only put bounded page content into the model context.

- Public PDF discovery contract: `knowledge/methodology/pdf_catalog.json`, individually licensed and catalogued source PDFs (consult the current catalog for the exact count).
- Proof-of-concept PDF reader: `experimental/conceptual_rag/github_pdf_reader.py`; remains *experimental source only*, **not included in the installed Skill ZIP**.
- Source selection is metadata-first. The local executor downloads at most one matching licensed PDF and checks its exact size and SHA256 before extracting a bounded number of pages. A scanned PDF returns a visual-review requirement rather than fabricated text.
- Private/third-party PDFs, including personal Drive libraries, remain outside the public repository. A private GitHub source would require legitimately authorized use and an authenticated host; no access token is embedded or assumed.
- Public PDFs have individual CC BY 4.0 licence metadata; metadata checks and unit tests do not replace human copyright review or establish scientific support.

See `references/GITHUB-METHODOLOGY.md`. No changes to the v1 release candidate or scientific gates.


## Hybrid editorial-card + licensed-PDF pilot

Run only from an authorized source checkout with Python/HTTPS:

```sh
python experimental/conceptual_rag/hybrid_public_retriever.py --ref <full-40-character-Git-commit> --question 'How to choose a review design?'
```

This opt-in, experimental reader reuses the existing card and PDF clients, with separate rights and citation grades, fixed context budgets, immutable source SHA and conservative failure states. It is **lexical retrieval**, not validated embeddings or general semantic question answering. Cards are original editorial [I] guidance, never direct source [L] evidence; PDF excerpts still need visual and printed-page checks. Protected sources are never fetched from the personal archive by this module. Publication rules: `knowledge/methodology/CARD-POLICY.md`. No installed-host test or release approval is implied.


## Source code versus installable candidate

A small two-channel adapter is now separately packaged in the **draft test ZIP** as `scripts/consult_public_methodology.py` and `scripts/public_method_pdf.py`. This is **not** a live production feature, nor proof of support on any specific host. The original experimental source-only readers stay outside the ZIP. The 88 editorial cards, 38 original licensed PDFs and both remote catalogues remain out of the ZIP and can only be retrieved on demand from a pinned commit after real runtime permission checks. No bulk import of the personal archive is authorized.

A separate public source registry provides 475 bibliography-only prospecting leads (404 matched catalogue titles, 71 unresolved), not source-derived research summaries. See `scripts/consult_source_registry.py` and `knowledge/methodology/source_cards/README.md`. Its indexing does not authorize private-PDF redistribution.
