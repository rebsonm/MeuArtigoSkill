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

## Evidence matrix schema

Adapt fields to the project, but start from:

```text
Evidence_ID
Citation
DOI_or_persistent_ID
Construct_or_concept
Definition_or_claim
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

Use role labels such as `FOUNDATIONAL`, `CORE`, `SUPPORT`, `CONTEXT`, `METHOD`, `CONTRASTING`, or domain-specific equivalents when useful. Keep these separate from formal quality appraisal scales.


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
