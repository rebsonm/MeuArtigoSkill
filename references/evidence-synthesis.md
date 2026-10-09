# Evidence extraction and synthesis

## Contents
- Principle
- Evidence matrix schema
- L/I/P discipline
- From papers to cross-source synthesis
- Category consolidation
- Contradictions and boundaries
- Writing provenance
- Evidence-strength cautions

## Principle

Do not let the manuscript become a sequence of paper summaries. Convert each source into comparable analytical units and synthesize relationships across sources.

Choose source appraisal and research-design requirements using [methodological foundations](methodological-foundations.md). For integrative reviews, quality appraisal is an identifiable analytical stage, not a synonym for CORE/SUPPORT or DOI verification. Distinguish scientific relevance from methodological trustworthiness and from legal authority.

## Independent source and locator checks

Read [source verification](source-verification.md). Use the deterministic script for DOI/metadata reconciliation and exact local passage matching when code execution is available. Record findings under the existing Evidence_IDs; do not create more ID families. A legitimate source lacking a DOI is not excluded automatically. Bibliographic identity and quotation presence are distinct from the claim's meaning, evidence quality and human scientific judgment. Never self-certify an [L] assertion using only a model-generated report.

## Critical appraisal by source type

Bibliographic identity, textual presence, methodological quality and claim support are separate dimensions. See [critical appraisal](../docs/AVALIACAO-CRITICA-FONTES.md). Use `scripts/appraise_evidence.py` to record design-specific human judgments on quantitative, qualitative, mixed-methods, review, conceptual, normative or other materials in existing evidence rows. Do not compute a universal automated quality score or present normative authority as empirical proof. Evidence with recorded limitations can still be used when claims are appropriately qualified. The code validates recorded basis and consistency, not the truth of reviewer conclusions.

## Evidence matrix schema

Adapt fields to the project, but start from:

```text
Evidence_ID
Citation
DOI_or_persistent_ID
Construct_or_concept
Definition_or_claim
Literature_role
Role_classification_basis
Primary_source_status
Conceptual_lineage_or_relation
Problem_tension_or_risk
Mechanism_relationship_or_finding
Study_design_or_source_type
Sample_data_or_material
Context
Process_or_stage
Actors_or_roles
Decision_right_or_action
Observable_evidence_or_artifact
Boundary_conditions
Limitations
Transferability_to_question
Evidence_role_or_strength
Supporting_locator
Epistemic_label
Notes
```

Not every field fits every discipline. Remove irrelevant fields rather than filling them with invented content.

## Conceptual lineage and classic literature

For material concepts, theories, constructs, mechanisms, and methods, do not treat the literature as a flat list of citations. Reconstruct the relevant conceptual lineage when the evidence supports it:

`origin/foundation -> consolidation -> important critique -> contemporary development/use`

Not every concept requires every link. Do not manufacture a lineage merely to fill fields.

Use the existing `09_MATRIZ_EVID` and classify the role of each source where relevant:

- `FOUNDATIONAL` — introduces or materially formulates the concept, theory, mechanism, or framework;
- `CANONICAL` — consolidates a formulation that became a central reference in the field;
- `CLASSIC_CRITIQUE` — a historically important critique that materially redirected or bounded the debate;
- `METHOD_FOUNDATIONAL` — foundational source for a method, design, measurement approach, or analytical procedure;
- `CONTEMPORARY_UPDATE` — updates, extends, revises, or recontextualizes the concept in current literature;
- `EMPIRICAL_SUPPORT` — provides empirical support relevant to the concept/mechanism without being foundational;
- `CONTRARY_EVIDENCE` — provides evidence or argument that contradicts, limits, or challenges the dominant formulation;
- `CONTEXT` — provides background/context without carrying the conceptual lineage;
- `OTHER` — use only with an explicit explanation.

Do not classify a source as classic merely because it is old, highly cited, or frequently repeated by later papers. The classification must be justified in `Role_classification_basis` using evidence such as original formulation, recognized consolidation, field-shaping critique, or repeated treatment as a foundational reference in authoritative literature.

For historical or conceptual attribution claims such as “X introduced”, “X proposed”, “X defined”, or “the original formulation”, prefer the primary source. Record `Primary_source_status` as:

- `PRIMARY_VERIFIED` — the primary source was actually consulted;
- `SECONDARY_ONLY` — attribution is currently supported only by a secondary source;
- `NOT_VERIFIED` — primary-source status remains unresolved;
- `NOT_APPLICABLE` — the row does not make an origin/foundation attribution.

Never imply direct consultation of a classic work when only a secondary source was read. If the primary source is unavailable, preserve the secondary attribution transparently and avoid wording that overstates verification.

Use `Conceptual_lineage_or_relation` to record how the source relates to the lineage of the concept, for example: original formulation, consolidation of definition, critique of boundary conditions, contemporary extension, transfer to a new context, or methodological adaptation.

The purpose is dual anchoring: where appropriate, a material theoretical claim should be able to connect both to its foundational/canonical basis and to the contemporary state of the discussion. Do not enforce mechanical citation quotas such as “one classic plus two recent sources per paragraph”.

This is part of the evidence architecture, not a new review method, new sheet, or new ID family.

## Concept operationalization traceability

When an article adopts, adapts, combines, or creates constructs, dimensions, categories, indicators, or interpretation rules, preserve the operationalization chain explicitly.

For each material construct/category, record where applicable:

```text
Concept_or_construct
Canonical_definition
Definition_source_Evidence_IDs
Mechanism_or_relationship
Dimension_or_category
Indicator_or_observable
Interpretation_rule
Boundary_or_exclusion_rule
Epistemic_label
Trace_IDs
Human_validation
Notes
```

Expected chain: `concept -> definition -> source -> mechanism -> dimension/category -> indicator/observable -> interpretation rule`.

Do not invent an indicator merely to complete the chain. Keep a source definition [L], an analytical operationalization [I], and an original construct/category [P] distinguishable. If a construct is adapted, preserve both the source definition and the project's operational definition with the rationale. If categories are merged, split, renamed, or superseded, record the decision and linked evidence rather than silently rewriting history.

This traceability belongs inside the existing evidence/synthesis architecture; it does not create a new canonical sheet or ID family. Use `09_MATRIZ_EVID`, `10_SINTESE`, `17_DECISOES`, `18_VALIDACOES`, and TRACE events as appropriate.

## Originality and inference integrity

Read [claim integrity](../docs/CONTROLE-CLAIMS-E-ORIGINALIDADE.md). The free deterministic script checks the difference between source-supported [L], inferential [I] and originally proposed [P] claims using the canonical Claims Ledger. [L] requires existing evidence IDs and locators; [I] requires an explicit warranted reasoning step and stated conditions; [P] requires related prior works, contribution delta, search trace and a bounded novelty scope. Originality is not proved by a negative search or an abstract-only comparison. Statements of universal precedence ('first study', 'inédito', 'never studied') should be revised before claim freeze. Preserve empirical findings as a distinct type, not as unverified [P] proposals. Human review is still essential.

## L/I/P discipline

Use internal epistemic labels:

### `[L]` Literature/source-supported
The source directly supports the statement at the level claimed.

### `[I]` Analytical inference
The statement arises from comparing or integrating sources. It may be well reasoned but is not a verbatim finding of a single source.

### `[P]` Proposition/original contribution
The author introduces the relationship, construct, framework element, hypothesis, typology, mechanism, or recommendation.

Keep the labels through synthesis and drafting. They may be removed from the final prose, but their provenance should remain recoverable.

## From papers to cross-source synthesis

For each analytic question, compare sources horizontally:

- Do multiple sources define the same construct differently?
- Do they propose the same mechanism in different contexts?
- Is a mechanism theoretical in one study and empirically observed in another?
- What evidence contradicts the dominant view?
- What contextual boundary limits transferability?
- Which claims are merely technical performance claims versus organizational/institutional claims?
- Which findings are direct versus extrapolated?

Create synthesis notes by construct/mechanism, not by paper.

## Category consolidation

Before creating a higher-order category, require an explicit justification such as:

- multiple independent scientific sources;
- independent theoretical and empirical support;
- scientific + institutional convergence where institutionally relevant;
- a distinct problem/mechanism not already captured elsewhere;
- an observable implication or artifact;
- a defensible conceptual distinction.

Avoid proliferating categories just because source terminology differs.

Record merged aliases and why they were merged.

## Contradictions and boundaries

A strong synthesis records disagreement, not only convergence.

For each category, ask:

- what evidence supports it;
- what evidence limits it;
- in which contexts it may not transfer;
- whether the source studied the same unit of analysis;
- whether causal language is warranted;
- whether the evidence is conceptual, observational, experimental, technical benchmark, qualitative, or institutional.

Do not flatten heterogeneous evidence into a false consensus.

## Writing provenance

Every important manuscript claim should map to one of:

- one or more evidence IDs;
- an explicit analytical inference built from evidence IDs;
- an original proposition built from identified literature gaps;
- actual empirical results from the user's study.

Draft methods from the protocol/search log, not from memory.

Draft results/synthesis from the evidence matrix, not from abstracts alone when full text was available and used.

Draft discussion by comparing the new synthesis with the nearest neighboring literature and the article's stated contribution.

## Evidence-strength cautions

Do not treat these as equivalent:

- conceptual proposal vs empirical validation;
- prototype vs production deployment;
- technical benchmark vs organizational outcome;
- regulation/standard vs empirical research;
- abstract-only evidence vs full-text evidence;
- citation presence vs causal influence;
- high citation count vs methodological quality.

Use the controlled literature-role labels defined above when the conceptual lineage matters. Keep literature role separate from methodological quality, evidence strength, citation count, and publication age.


## Adversarial claim robustness audit

Before a material Claim_ID is frozen, do more than confirm that at least one source supports it.

Audit:

- supporting Evidence_IDs;
- counter-evidence or contradictory findings in the retained corpus;
- plausible alternative explanations;
- boundary conditions;
- single-source dependence;
- whether the wording is stronger than the evidence;
- whether the claim is [L], [I], or [P];
- what would change if a central supporting source/evidence item were removed.

Suggested claims-ledger fields:

```text
Claim_ID
Manuscript_section
Claim_text
Claim_type
Evidence_IDs
Counter_Evidence_IDs
Locator_status
Alternative_explanations
Boundary_conditions
Single_source_dependency
Strength
Robustness_status
Robustness_notes
Trace_IDs
Gate_ID
Human_validation
Draft_status
Notes
```

Robustness status:

- NOT_AUDITED
- ROBUST
- QUALIFIED
- REVISE
- REJECT
- NOT_APPLICABLE

`QUALIFIED` means the claim may remain, but its boundary/qualification must appear in the manuscript.

Do not treat disagreement as noise to be removed. Contradictory evidence may expose heterogeneity, boundary conditions, or a more precise theoretical contribution.

The purpose is to test whether a claim survives reasonable contestation, not to manufacture certainty.
