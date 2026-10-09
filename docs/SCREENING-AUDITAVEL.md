<a id="screening-auditável-separar-sugestões-da-ia-de-decisões-científicas"></a>
# Auditable screening: separate AI suggestions from scientific decisions

This procedure uses the **same** 03_Screening.csv table and the **same** 07_SCREENING tab of the master matrix. It does not introduce new tabs, ID families, paid accounts, or the requirement for two fictitious human reviewers.

<a id="o-que-significa-cada-etapa"></a>
## What each step means

**Pass1**: title and abstract screening; final human decision INCLUDE, BORDERLINE or EXCLUDE.

**Pass2**: prioritization after the closest title/summary review for records retained in Pass1; FULL TEXT — CORE, FULL TEXT — SUPPORT or EXCLUDE values. Pass2 does not replace the actual full-text eligibility assessment in 04_FullText_Tracker.csv. CORE/SUPPORT priority does not mean methodological quality.

An AI can **propose** each of the decisions, explaining the reason and pointing out where the suggestion was produced. This proposal is never written in the final fields. The decision is only recorded in the final field after an effective response and attributed to the researcher, preserving the reference to the message/document that originated it.

<a id="campos-adicionais-nas-tabelas-já-existentes"></a>
## Additional fields in existing tables

For each Pass1 and Pass2, the matrix has:
- AI_proposal — decision suggested by the AI, still provisional;
- AI_reason — justification of the suggestion, without assuming it to be true;
- AI_source — reference to the actual message or output of the model;
- reviewed_by — identified human reviewer;
- review_evidence — reference to the reviewer’s effective statement;
- disagreement_reason — reason recorded when the human decision diverges from the suggestion.

The old fields Pass1_decision/Pass1_reason and Pass2_decision/Pass2_reason continue to represent the final decision, its motivation and the protocol used. Existing search IDs are preserved.

<a id="execução-gratuita"></a>
## Free execution

Requires Python 3.10+ and standard library. Examples of form of command, not actual decisions:

    python scripts/screening_review.py propose "/project" --stage pass1 --record-id "R-0001" --proposal BORDERLINE --reason "The abstract presents potentially relevant indicators but does not describe the application context." --source "Referência à saída real do agente"

Only after the researcher actually examines the data and expresses his decision:

    python scripts/screening_review.py decide "/project" --stage pass1 --record-id "R-0001" --decision INCLUDE --reason "The abstract meets the predefined inclusion criterion on document governance." --reviewer "Pesquisador" --evidence "Referência à manifestação original do pesquisador" --disagreement-reason "O pesquisador identificou aderência ao conceito central que a recomendação inicial não reconheceu."

When there is disagreement, the last argument will be mandatory. The original decision is preserved: it is not permitted to silently replace an already recorded judgment. Subsequent revisions must have a new record in the existing DEC_ID/TRACE_ID, with justification and a versioned copy of the previous state.

Running the script only confirms that the table has changed. A name entered in --reviewer does not authenticate human identity or prove that the user has read the document; the --evidence field must point to the actual message or review and must be checked externally.

<a id="auditoria-e-congelamento"></a>
## Audit and freeze

    python scripts/screening_review.py audit "/project" --strict

To check if there are pending elements before freezing the corpus:

    python scripts/screening_review.py audit "/project" --strict --freeze

In new projects, the screening_human_decisions_required=true parameter activates cross-validation by the main validate_project.py script. Approved GATE-0004 cannot proceed with unappreciated suggestions, absent reviewers, unjustified deletions, unresolved disagreements, or unduplicated records without decisions completed on applicable passages.

The BORDERLINE state requires a resolution in Pass2 before freezing. Truly identified duplicates require Canonical_record_id link; The model's suggestions do not serve, in isolation, to state that an item is duplicated.

Old projects maintain compatibility as long as they do not activate the rule. If they need to migrate, new columns are added when the first event is registered, **without inventing retroactive revisions**. To audit old records without modifying them, run audit --strict; the correction of records must be based on real human evidence.

<a id="integridade-e-limitações"></a>
## Integrity and limitations- Do not use AI as a second independent human reviewer. If there is only one researcher, inform screening by a single reviewer and rechecking of BORDERLINE and INCLUDE/EXCLUDE sample, according to protocol.
- Do not delete sources just because the full text is inaccessible. This means PENDING ACCESS in the full-text track, not scientific irrelevance.
- Do not transform the AI ​​suggestion into a final decision silently, nor generate a justification or a fictitious human reviewer.
- Require a clear reason for EXCLUDE and re-examine borderline cases; Potentially relevant sources should remain retained until necessary review.
- Batch review is only valid when the protocol documents a human procedure actually performed, with criteria, coverage and reference to the evaluation record. Do not automatically assign individual reviews to the generic approval of a list.
- Without access to the canonical Google Drive, local CSVs and artifacts can only be authorized staging. Sync reviews and evidence references to the original workspace before asserting that the canonical matrix is ​​up to date.

This control is procedural; does not itself measure screening sensitivity/specificity or agreement between human raters. These claims require separate empirical assessment.