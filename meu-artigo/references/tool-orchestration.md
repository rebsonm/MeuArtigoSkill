# Tool orchestration

## Contents
- Principle
- Google Drive and files
- Consensus
- Scite
- Scopus and Web of Science
- Web/publishers
- Browser automation
- Tool failure rules
- Automation policy

## Principle

Use each tool for the job it is good at. Never treat a convenient discovery tool as equivalent to an indexed bibliographic database or full-text source.

## Persistent workspace and user files

Use connected persistent storage/user files to:

- recover the user's existing reading corpus;
- locate earlier notes, PDFs, exports, protocols, or templates;
- create/persist project artifacts;
- resume state across chats;
- avoid making the user upload the same material repeatedly.

When a project folder already exists, inspect it before creating new parallel structures. Google Drive is the reference implementation, not a methodological requirement.

Do not import substantive content from an unrelated prior project into a new article. Reuse only templates/process structures unless the user explicitly asks to reuse literature.

## Peer-reviewed discovery tools

Use a peer-reviewed discovery tool (Consensus when available) for:

- quick peer-reviewed discovery;
- terminology calibration;
- finding near-neighbor papers;
- testing whether an apparently novel combination already exists;
- locating reviews/meta-analyses that reveal a field's vocabulary.

Rules:

- Do not present the discovery tool as exhaustive.
- Log important searches when they affect protocol or novelty decisions.
- Fetch the paper record before citing a search result.
- If the monthly limit is reached, record the limitation and continue with other valid sources; never infer absence of literature.

## Citation-context and citation-graph tools

Use a citation-context/citation-graph tool (Scite when available) for:

- targeted literature search;
- reading metadata and indexed full-text passages;
- full-text reading when licensed/available;
- forward/backward citation-graph exploration;
- supporting/contrasting/mentioning citation context;
- bibliography generation from verified DOIs;
- optional source-decision audit.

Check whether `read_fulltext` returned full text or abstract fallback. Do not claim full-text reading from an abstract fallback.

If the preferred citation tool is unavailable, log the tool limitation and use other valid sources. Do not downgrade scientific conclusions because one tool is unavailable.

## Indexed bibliographic databases

Use appropriate indexed sources when required by the field and protocol. Scopus and Web of Science are common implementations, not universal requirements.

For each search:

- preserve the literal query syntax used on that platform;
- record filters separately from conceptual logic;
- export sufficient metadata;
- confirm actual exported row counts and fields;
- preserve raw files;
- mark partial exports as partial;
- re-run incorrect date/type/language filters rather than silently repairing counts afterward.

When the same conceptual family is run in a complementary database, screen only genuinely new records after deduplication while preserving database-overlap statistics.

## Web and publishers

Use academic web search, publisher pages, repositories, and official institutional sites to:

- locate open full text;
- verify DOI/title/metadata;
- retrieve current standards, policies, laws, or journal instructions;
- inspect a target journal archive;
- find accepted manuscripts or author-hosted versions;
- resolve metadata ambiguity.

Prefer original publishers, DOI landing pages, official institutional domains, and recognized repositories for verification.

## Browser automation

Use authenticated browser workflows when a database or publisher requires normal interactive access and the user has authorized access.

Rules:

- never ask the user to paste passwords into chat;
- reuse an authorized browser profile when available;
- do not bypass paywalls or access controls;
- if export UI limits records per batch, record each batch and verify complete coverage;
- treat browser UI results as data that still require logging/validation.

## Tool failure rules

When any source/tool fails:

1. log what failed;
2. distinguish tool unavailability from evidence absence;
3. use an appropriate alternative source;
4. preserve the unresolved status if evidence cannot be obtained;
5. never fabricate the missing result.

## Automation policy

Automate aggressively where the operation is reproducible:

- project scaffolding;
- metadata normalization;
- exact/near-duplicate flagging;
- count checks;
- search-log population;
- screening-table preparation;
- full-text tracker updates;
- evidence-matrix templates;
- citation metadata checks;
- final consistency audits.

Keep human/agent judgment explicit where scientific interpretation is required:

- defining the research problem;
- novelty claims;
- inclusion relevance in ambiguous cases;
- near-duplicate confirmation;
- transferability judgments;
- theoretical integration;
- strength of claims;
- final method label.

## Canonical workspace initialization

When persistent storage is connected, initialize or resume the structure in `drive-workspace.md` before large searches. Reproduce the same logical schema even if the platform uses another storage system. Create the project root, canonical subfolders, `CONTINUIDADE.md`, protocol, and master tracking table. Update them continuously; do not leave state only in the conversation.
