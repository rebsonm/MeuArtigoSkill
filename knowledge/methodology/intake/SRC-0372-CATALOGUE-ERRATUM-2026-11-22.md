# SRC-0372 — corrected original-work catalogue identity (2026-11-22)

## Verified inconsistency

The source registry previously assigned the article title belonging to **SRC-0373** to **SRC-0372**. This is an erroneous title-level join, not a verified same-work duplicate. The existing source card `knowledge/methodology/source_cards/src-0372.md` and the documentary receipt `knowledge/methodology/intake/parallel/IB-15-DELTA.json` both record a **different** source, authored by **Danielle Costa da Silva (2017)**, a conference contribution associated with the **2017 ALACIP meeting**. SRC-0373 is a distinct methodological article by **Márcio C. Carlomagno and Leonardo Caetano da Rocha (2016)**.

## Corrective action in this draft PR

- Correct only the `SRC-0372` title and search keywords in `knowledge/methodology/source_registry_catalog.json` to match the inspected source card and its documentary receipt.
- Preserve the source ID, original card file SHA/hash, `CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED`, scientific review status, redistribution restrictions and all **474 other entries** without changing their interpretation.
- Do not merge the distinct SRC-0372 and SRC-0373 works; neither is a scientific [L] claim.
- This correction **does not** establish DOI, permission to redistribute the source or full-text scientific reading.
- The previous duplicate-title triage in PPGA draft PR #116 must be annotated to mark this pair as a **false match produced by the incorrect registry title**.

## Outstanding independent checks

Verify the source's actual conference citation, edition and page locator from the original front matter if citing this work. Keep rights and bibliographic identity separate from scientific methodological approval. No change to the researcher's seven pending gates, other catalogued articles or release artifacts.
