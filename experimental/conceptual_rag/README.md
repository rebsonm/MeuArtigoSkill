# GitHub-hosted conceptual methodology knowledge — experimental

**New architecture (2026-11-21):** the GitHub repository is the home of redistributable methodological knowledge, **not Google Drive**. The historical branch name still contains "drive" but the intended published module has no Drive dependency. The official version `v1.0.0-rc.1` and the stable release remain untouched.

- `knowledge/methodology/catalog.json` is a small, public discovery catalog for original editorial concept cards.
- `knowledge/methodology/cards/` holds only authored summaries and bibliographic leads, never reproduced third-party books, full-text PDF conversions or private research data.
- `scripts/consult_github_methodology.py` is the optional lightweight HTTPS client; it **does not download the library at installation** and reads at most matching cards, by pinned Git SHA and SHA256.
- `references/GITHUB-METHODOLOGY.md` describes host prerequisites, fallback and verification.
- `experimental/conceptual_rag/rag.py` remains a separate local-only, optional hybrid index builder, **not connected to remote vectors by this phase**.

## What changed from the earlier pilot

The Drive folders used in the earlier research experiment are **not part of the new architecture**. No books or PDF-to-Markdown derivatives have been copied into the public repository. Those original files are unchanged. This revision does not delete existing user-owned pilot folders, change permissions or claim all of their copies are gone.

Only public redistributable cards appear in Git. There is no automatic access to private sources, no MCP, no server and no automatic runtime network entitlement from installing a Skill. ChatGPT, Claude and Gemini require their own observed host permissions and execution support.

## Retrieval contract

1. No remote fetch when the Skill is installed, imported or merely started.
2. On an eligible research question, first fetch an immutable, small catalog from the exact, authorized GitHub repository and commit SHA.
3. Rank metadata locally. Download only up to three matching cards by default, verify hashes and return at most 3,300 characters, without injecting the full corpus into context.
4. If unavailable, do not fabricate network access: fall back to bundled core methodology and declare the limitation.
5. Do not treat retrieved editorial guidance as direct scholarly evidence [L], independent review or a completed scientific gate.

**Open tasks:** verify the actual ChatGPT host's ability to fetch GitHub; test full source permissions; evaluate a genuine local embedding model, negative retrieval queries and specialist human review; decide separately how to publish immutable versioned indices. All branch work is draft and not released.
