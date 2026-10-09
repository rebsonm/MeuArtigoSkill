# Beginner mode

## Contents
- Goal
- Minimal user input
- What the agent should do automatically
- What must stay visible to the user
- Plain-language vocabulary
- Example interaction pattern

## Goal

A researcher with little AI or database experience should be able to use the skill through ordinary language while still receiving a methodologically disciplined workflow.

## Minimal user input

A valid starting message can be as simple as:

- "I want to write an article about [specific problem]."
- "My research question is [question]. Help me build the paper."
- "I have this idea and these PDFs. Turn it into a rigorous article workflow."

The user does not need to know Boolean syntax, database export formats, deduplication rules, evidence-matrix design, or tool names.

The agent should not require the user to supply a ready-made search strategy.

## What the agent should do automatically

Follow [the essential beginner flow](fluxo-essencial.md), while preserving
all scientific controls. Do **not** impose a long universal sequence of
bibliographic searches on every article type.

1. Check actual platform/storage capabilities; create or resume a
   canonical workspace **only after** the Drive write preflight or
   explicitly authorized local/Work fallback.
2. Preserve the researcher's original problem and show a provisional,
   bounded question and contribution; run a **small novelty check**
   only when authorized and tools really permit it.
3. Explain the plausible methodological routes in ordinary language,
   then record the researcher's actual choice and limitation at the
   appropriate human gate; leave the route UNDECIDED if unresolved.
4. Prepare **only the method-specific workflow**: reviews use justified
   bibliographic searches, deduplication and screening when applicable;
   empirical projects require actual material/data and analysis; mixed
   designs need genuine integration; design science needs artefact
   construction and separate evaluation.
5. Execute routine operations without unnecessary interruptions,
   verifying any tool results, source identities and file permissions.
   Distinguish proposed, unverified and executed events; never synthesize
   counts, participant statements, outcomes or external confirmations.
6. Keep links to source and claim evidence, contrary findings,
   justifications and journal rules; for any scientific gate
   require the real researcher's response and appropriate proof.
7. Save the observed progress and next valid action in the
   authorized persistent project workspace.

In MINIMAL, show **one next action, one decision if required, and one
material risk/limitation**. In FULL, show the detailed existing state
on demand; neither mode changes actual verification or gate requirements.

## What must stay visible to the user

Keep the user informed of scientific decisions that materially change the paper:

- narrowing/reframing the research question;
- a strong prior paper that threatens novelty;
- a method-label decision;
- a search failure or database-access limitation;
- exclusion rules likely to change conclusions;
- a major contradiction in the evidence;
- a proposed original framework/proposition;
- an unresolved evidence gap before submission.

Do not overwhelm the user with low-level mechanics that were executed correctly.

## Learn through scientific decisions

For scientifically material validation gates, briefly explain *why* a methodological choice is proposed, its closest alternative, and one practical risk. Then ask the researcher, in plain language, why they choose it and which limitation they recognize. The Skill should not write the researcher's answer or present a ready-to-copy response. If the user is unsure, explain the decision more clearly and leave the gate pending until a real response is received. This is not a quiz at every operational step: routine work remains autonomous. Read [formative validation](../docs/VALIDACAO-FORMATIVA.md).

## Plain-language vocabulary

When needed, explain terms simply:

- **search string**: the exact query pasted/executed in a database;
- **conceptual block**: a group of synonyms representing one part of the research question;
- **deduplication**: removing repeated records while preserving their provenance;
- **screening**: deciding which retrieved records are relevant enough to keep;
- **full text**: the complete paper, not only title/abstract;
- **evidence matrix**: a structured table that records exactly what each source contributes;
- **snowballing**: finding earlier/later relevant papers through references and citations;
- **novelty audit**: checking whether the intended contribution has already been made;
- **integrative review**: a review that combines heterogeneous literature to build/refine concepts or frameworks;
- **systematic review**: a review with a stricter comprehensive eligibility process designed to answer a specific review question;
- **C.A.D.A.**: the operational cycle used to capture work, assign it, define a time expectation, and follow it until there is evidence of progress/completion.

## Example interaction pattern

User:
"I want to write an article about why small municipalities struggle to adopt AI in procurement."

Agent behavior:

1. Preserve the original problem and resolve actual Drive storage access
   or explicitly authorized WORK_FALLBACK before substantive research.
2. Map available tools and identify which operations are really possible.
3. Clarify/refine only what is scientifically necessary.
4. Propose a provisional question and contribution, then conduct a
   small novelty scan **only when authorized and technically available**.
5. Present possible qualitative, quantitative, mixed, theoretical or
   review routes, in ordinary language (qualitativo, quantitativo,
   misto, teórico ou revisão), and require the researcher's actual
   method decision before freezing it.
6. Create the route-appropriate protocol and use only pertinent
   acquisition/search, empirical analysis, synthesis or evaluation
   procedures. Do not force a systematic-review sequence on fieldwork
   or conceptual work.
7. Explain blockers plainly, log only demonstrated actions and save
   the authorized canonical state for future continuation.

The user directs the research problem and scientific decisions while
the Skill organizes verifiable workflow infrastructure.
