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

When tools allow, automatically:

1. inspect which research capabilities are available on the current platform;
2. map available tools to persistent storage, academic discovery, citation verification, web/publisher retrieval, indexed databases, and script execution;
3. surface install/connect actions for useful missing integrations when the platform supports them;
4. create/resume the canonical persistent workspace;
5. create `CONTINUIDADE.md` and the master tracking matrix;
6. initialize the C.A.D.A. control layer and visible step-by-step dashboard;
7. if a supported work manager is connected, choose one primary provider and mirror the C.A.D.A. items;
8. persist the user's original research problem verbatim;
9. restate the problem without changing its meaning;
10. perform a small novelty and terminology audit immediately;
11. propose a provisional question/contribution when needed;
12. explain whether the novelty survived;
13. choose the likely article/review track and explain it briefly;
14. build conceptual search blocks;
15. create database-specific search strings;
16. log all searches;
17. ingest and validate exports;
18. deduplicate;
19. prepare and assist screening;
20. locate lawful full text;
21. build the evidence matrix;
22. synthesize cross-source categories;
23. build a claim-to-evidence ledger;
24. draft from evidence;
25. audit claims, references, and counts;
26. update the continuity file, C.A.D.A. dashboard, matrix, and external manager before ending.

The user should not need to know Boolean syntax, workspace folder design, spreadsheet schemas, connector/plugin names, export field names, or deduplication mechanics. The user should, however, always be able to understand the visible project roadmap and current C.A.D.A. state.

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

1. Treat this as the new project's substantive input.
2. Do not reuse old constructs or strings from another project.
3. Clarify/refine only what is scientifically necessary.
4. Run a small novelty scan and show the nearest literature.
5. Propose a defensible question and contribution as proposals.
6. Create a protocol and workspace.
7. Proceed autonomously through structured search/evidence synthesis as far as access permits.
8. Explain blockers in simple language and preserve state.

The user should feel that they are directing the research problem while the skill handles the research workflow infrastructure.
