# Claim provenance and bounded originality

Source identity, semantic claim support, inference and originality are separate scientific issues.

## Epistemic statuses

- [L] (LITERATURE): literature-grounded assertion; requires existing Evidence_ID and a source locator. A locator match alone is not semantic corroboration.
- [I] (INFERENCE): author interpretation based on evidence. Requires an explicit inference warrant and boundary/limitation.
- [P] (PROPOSITION): original proposal or adaptation; requires identification of nearby prior works, the precise contribution relative to them, the scope of the novelty statement, and a documented novelty Search_ID.
- EMPIRICAL_RESULT: research finding from empirical data; needs additional independent data/protocol review. Never re-label it as a literature statement or proposition merely to pass a control.

The canonical 09_Claims_Ledger.csv and existing 11_CLAIMS worksheet append six fields: Inference_warrant, Nearest_prior_Evidence_IDs, Contribution_delta, Novelty_scope, Novelty_search_ref and Researcher_review_evidence. The previous columns remain unchanged. No new worksheets, ID families or external paid software.

## Free execution

Python 3.10+ and standard library only:

    python scripts/claim_integrity.py PROJECT --strict
    python scripts/claim_integrity.py PROJECT --strict --freeze

New projects enable claim_integrity_required=true and enforce checks at GATE-0006. Older projects remain compatible until deliberate migration; never invent retroactive researcher approval.

## Rules at claim freeze

Literature claims require citations and locators. Inferences require evidence, the reasoning connecting the evidence to the proposed conclusion, and boundaries. Propositions require literature comparators and a documented difference and research scope. Evidence_IDs and Search_IDs must exist in the canonical project. Final claims require a researcher validation state and a reference to the actual response.

The audit flags categorical universal precedence such as 'primeiro estudo', 'inédito', 'first-ever' and 'no prior studies'. A recorded search cannot demonstrate the absence of every prior publication; rewrite claims to a defensible scope rather than merely filling a validation field. The language patterns are incomplete and may flag legitimate historical quotations, so a scientist must still review the text and attribution.

### Search-based novelty conclusions are [I]

Assertions such as “a novidade sobreviveu” or “a busca não identificou estudos anteriores” are **inferences [I]** about a specific corpus, period, strategy and access conditions, not scientific propositions [P] or source-backed facts [L]. Use the existing `Novelty_scope` and `Novelty_search_ref` fields, plus `Inference_warrant` and `Boundary_conditions`, to document what was searched and what remains uncertain. The standalone [P] contribution is a separate claim, compared with nearest prior works. The script catches defined textual patterns but cannot semantically classify every paraphrase. Human confirmation is still mandatory.

Search_ID presence means there is a recorded search, not proof of worldwide novelty or full coverage. The software cannot check conceptual originality, deep logical validity, correctness of an interpretation or actual human authorship. Always use qualified language and document limitations. The empirical quality benchmark remains a separate process.

Google Drive-first remains the workspace rule: local CSV mutations must be synchronized with the authorized canonical project state, preserving historical evidence and actual scientific decisions.
