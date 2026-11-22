# Public methodology intake and safe publication

**Maintainer instruction:** Publish new author-written methodology cards and properly licensed source PDFs without a **draft PR** step. Direct commits to the public default branch are preferred *where repository rules permit*. Current protected-branch rules require a **non-draft pull request and the audit status check**, which must be respected rather than bypassed.

1. **Deduplicate** using title, author, edition, DOI, source URL, filenames and hash.
2. **Review exact-copy rights** before adding a PDF. Private access and an internet link are not redistribution licenses. Keep attribution, CC variants/NC/ND restrictions and the exact edition explicit. A card's original prose has separate rights from the underlying source.
3. **Keep evidence grades honest:** [L] localizable primary evidence, [I] interpretation and [P] proposal. Do not infer permission or scientific fidelity from file availability.
4. **Maintain catalog and reader integrity:** compute SHA-256, update indexed card records and preserve ID semantics. Pinned clients with fixed 649-card cardinality need a deliberately compatible version update before new card IDs are added.
5. **Verify publication:** use conflict-aware pushes, inspect public readback and audit/CI checks; do not claim success when a tool reports a blocker.

Do not copy private course handouts, unlicensed books, restricted PDFs or personal student information. Public project guidance is written in English without unnecessary institutional affiliation. Do not update installed releases or scientific GATE-0001..0007 without their independent controls.
