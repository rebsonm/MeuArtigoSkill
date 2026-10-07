# Research-process traceability

## Purpose

Traceability answers a different question from project management.

- **C.A.D.A.** answers: what work exists, who owns it, what happens next, when, and what proves progress?
- **Traceability** answers: how was the scientific product constructed, what changed, why, by whom/what, from which source, with which tool, and how was the result verified?

Both are required.

The canonical principle is:

> `CONTINUIDADE.md` explains **where the project is now**.
> `RASTREABILIDADE.md` and `13_Traceability_Log` explain **how the project got there**.

## Why this matters in AI-assisted research

AI can accelerate searching, classification, synthesis, drafting, and editing, but it can also make the construction process opaque.

Meu Artigo therefore treats process provenance as a first-class artifact.

The goal is not to archive every conversational token. The goal is to preserve enough information for a researcher, coauthor, reviewer, editor, or future agent to reconstruct material methodological and intellectual steps.

## Canonical artifacts

### `RASTREABILIDADE.md`

Human-readable chronological/process summary.

Maintain:

- project identity;
- methodological design and versions;
- major research decisions;
- executed search versions and exports;
- dedup/screening milestones;
- full-text and evidence milestones;
- synthesis decisions;
- manuscript version milestones;
- AI-assisted steps;
- human validation points;
- submission versions;
- unresolved provenance gaps.

This file can later be adapted into supplementary material or an AI-use/method-transparency statement when appropriate.

### `13_Traceability_Log`

Structured event-level provenance table:

```text
Trace_ID
Timestamp
Scientific_stage
CADA_ID
Actor
AI_platform_or_tool
Model_or_version
Action_type
Action_summary
Input_or_source
Source_or_artifact_IDs
Decision_or_output
Rationale
Artifact_before
Artifact_after
Verification_method
Human_validation
Related_Search_IDs
Related_Record_IDs
Related_Evidence_IDs
Related_Claim_IDs
Prompt_or_instruction_summary
Reproducibility_information
Materiality
Status
Notes
```

Use stable `TRACE-####` identifiers.

### `14_AI_Use_Log`

AI-specific disclosure/provenance table:

```text
AI_Use_ID
Date
Scientific_stage
CADA_ID
Trace_ID
Platform_or_tool
Model_or_version
Purpose
Input_category
Output_category
Materiality
Human_review_method
Human_decision
Accepted_modified_or_rejected
Related_artifacts
Disclosure_required
Disclosure_text_or_note
Notes
```

Use stable `AIUSE-####` identifiers.

## What counts as a traceability event

Log material actions such as:

- research question materially reframed;
- article/review design selected or changed;
- search family created or changed;
- literal search executed;
- export validated or invalidated;
- dedup rule applied to a corpus;
- screening rule modified;
- full-text decision that changes corpus scope;
- evidence category created/merged/split;
- analytical inference accepted;
- proposition/framework element introduced;
- important claim drafted or materially revised;
- source/citation corrected;
- AI output accepted, modified, or rejected after review;
- manuscript canonical version frozen;
- submission made;
- reviewer request and response decision.

Do not log trivial wording changes unless they alter meaning, evidence, or disclosure.

## Actor vocabulary

Use values such as:

- `HUMAN`
- `AI`
- `HUMAN+AI`
- `DATABASE`
- `SCRIPT`
- `EXTERNAL_REVIEWER`
- `EDITOR`
- `OTHER`

The final intellectual responsibility remains human even when AI performs an operational action.

## AI materiality

Classify AI use:

- `ASSISTIVE` — formatting, language polishing, syntax transformation, mechanical extraction with human verification;
- `SUBSTANTIVE` — literature discovery, screening assistance, evidence extraction, synthesis support, methodological reasoning, analytical categorization, substantive drafting;
- `ADMINISTRATIVE` — file naming, task tracking, project-status updates;
- `NOT_APPLICABLE`.

When in doubt, prefer transparency.

## Human validation

Material AI-assisted events should record how they were checked.

Examples:

- source opened and verified;
- DOI/metadata checked against publisher;
- full text inspected;
- count reconciled against export;
- screening sample manually rechecked;
- inference compared against evidence IDs;
- claim reviewed against supporting passages;
- manuscript paragraph edited/rejected by author.

Do not write `human validated` without a real verification action.

## Prompt recording

Do not require raw storage of every prompt.

Default:

- store a concise `Prompt_or_instruction_summary` for material AI actions;
- preserve exact prompts only when scientifically necessary, requested by the user, required by policy, or needed to reproduce an important transformation;
- never persist secrets, passwords, confidential data, or third-party protected material merely for traceability.

## Reproducibility information

For an action to be reproducible where possible, record enough of:

- tool/database;
- date/time;
- model/version if known;
- query/string;
- filters/parameters;
- input artifact;
- output artifact;
- script/version/commit;
- decision rule;
- human verification.

Not every generative output is perfectly reproducible. In those cases, preserve **procedural reproducibility and provenance** rather than pretending deterministic reproduction.

## Relationship to C.A.D.A.

A C.A.D.A. item may generate multiple traceability events.

Example:

```text
CADA-0042 — Validate WoS export

TRACE-0104 — export received
TRACE-0105 — row/field validation executed by script
TRACE-0106 — date-filter problem detected
TRACE-0107 — corrected export accepted after human verification
```

The CADA item manages the work.
The TRACE items preserve how the work happened.

## Relationship to Claims Ledger

Important manuscript claims should be traceable backwards:

```text
Claim_ID
  ↓
Evidence_ID(s) / empirical result
  ↓
Record_ID / source / locator
  ↓
Search_ID / acquisition path
  ↓
Trace_ID(s)
  ↓
CADA_ID / protocol decision
```

This creates a provenance chain from manuscript assertion back to construction process.

## Final traceability audit

Before submission:

1. verify every canonical search has a trace event;
2. verify reported counts reconcile with traceable artifacts;
3. verify important method changes have rationale;
4. verify substantive AI uses appear in `14_AI_Use_Log`;
5. verify human-validation actions are real and recorded;
6. verify key manuscript claims link to evidence;
7. generate/update `RASTREABILIDADE.md`;
8. prepare a journal-specific AI-use declaration if required;
9. do not disclose sensitive/private information unnecessarily.

## External communication

Traceability is not the same as publishing the entire private workspace.

When sharing with reviewers/editors, prepare an appropriate transparency artifact containing the necessary methodological provenance without exposing passwords, confidential material, copyrighted full texts, or unrelated private notes.
