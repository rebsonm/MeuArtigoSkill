# Grounded Corpus Mode

## Purpose

Grounded Corpus Mode allows the AI to answer analytical questions **only from the validated scientific corpus**, instead of mixing the project corpus with model memory or unrestricted web knowledge.

It is a behavior of the Skill, not a separate methodological design.

## Entry condition

Use only sources that the project has legitimately retained for full-text analysis.

Default eligible states are FULL TEXT — CORE and FULL TEXT — SUPPORT, with full text actually available.

Do not treat abstracts/snippets as full-text grounding.

## Core rule

For a grounded-corpus answer:

1. retrieve only eligible canonical sources;
2. identify the supporting Record_IDs;
3. use Evidence_IDs where extraction already exists;
4. provide an exact locator when available;
5. distinguish literature support [L] from analytical inference [I] and original proposition [P];
6. say when the corpus does not support an answer.

Do not silently supplement from model memory.

If external literature is needed, leave Grounded Corpus Mode explicitly and tell the user the answer is being expanded beyond the frozen corpus.

## Output contract

A substantive answer should be traceable in a form equivalent to:

```text
Analytical statement
  ↳ Record_ID: R-...
  ↳ Evidence_ID: E-...
  ↳ locator: page/section/paragraph when available
  ↳ epistemic status: [L] or [I]
```

For synthesis across records, list the contributing Evidence_IDs.

## Refusal / uncertainty behavior

Say the corpus does not currently support the answer when no eligible full text addresses the question, evidence extraction lacks the relevant passage, the answer would require outside knowledge, or a claim cannot be linked to canonical evidence.

Do not convert absence of evidence into evidence of absence.

## AI traceability

For material grounded analysis, record TRACE_ID, AI_Use_ID when AI participation is substantive, query/purpose summary, eligible source set or SNAP_ID, Record_ID/Evidence_ID set used, output artifact/Claim_ID when applicable, human review method, and accepted/modified/rejected decision.

Do not store every conversational prompt by default.

## Human validation

Grounded Corpus Mode does not remove human responsibility.

AI may retrieve, compare, summarize, propose categories, and identify candidate contradictions.

Human review is required before freezing a synthesis, accepting a new theoretical category, accepting a material inference, turning the result into a key manuscript claim, or passing the relevant human validation gate.

## Relationship to the Corpus Map

Corpus Map answers: **How is the corpus structured?**

Grounded Corpus Mode answers: **What does the validated corpus support?**

They share the same corpus but are different functions.

## Anti-Frankenstein rule

Do not introduce a mandatory vector database, RAG vendor, or reference manager into the core.

Use the retrieval mechanism available on the current platform, provided it can enforce the eligibility and provenance rules above.
