# Integration onboarding (platform-neutral)

> Legacy filename retained for compatibility: `plugin-onboarding.md`.

## Goal

A user should not need to know which research integrations are required. On the first run, inspect the capabilities available on the current AI platform and map them to the roles required by the methodology.

## Capability roles

Prefer these capabilities when available:

1. **Persistent project storage** — folders, PDFs, documents, spreadsheets/tables, exports, continuity state, and stable links.
2. **Peer-reviewed discovery** — terminology calibration, novelty scanning, nearby literature, and source discovery.
3. **Citation-context / citation-graph verification** — citation relationships, contextual verification, and full-text support where legitimately available.
4. **Academic web / publisher / repository retrieval** — official metadata, journal instructions, lawful full text, standards, and institutional sources.
5. **Indexed bibliographic databases** — structured, reproducible searches and exports when required by the review design.
6. **Local/script execution** — deterministic scaffolding, validation, and deduplication where the platform supports it.

## Preferred implementations

When available, these are useful implementations of the roles above:

- Google Drive — persistent workspace;
- Consensus — peer-reviewed discovery;
- Scite — citation context and graph;
- Firecrawl or equivalent web-retrieval capability — publisher/repository/official-source retrieval;
- Scopus and Web of Science — indexed bibliographic databases.

These names are **not methodological requirements**. Equivalent services may fulfill the same roles.

## First-run preflight

Before large-scale research:

1. inspect what tools, connectors, apps, MCP servers, browser capabilities, file stores, and script environments are actually available;
2. map each available capability to the roles above;
3. if a useful missing integration exists in that platform's install/connect flow, surface it to the user;
4. explain in one short sentence why it is useful;
5. never claim it was installed or connected until verified;
6. continue any independent work while the user authorizes connections;
7. after connection, resume the workflow without asking the user to repeat the research problem.

Installation, OAuth, account linking, or other third-party authorization always requires the user's explicit platform action.

## Minimum viable research stack

Do not block the project merely because the preferred tools are unavailable. A valid minimum is:

- persistent storage or a local fallback;
- at least one credible academic discovery route;
- a way to verify sources against original metadata/publisher records;
- a way to ingest structured bibliographic exports when exhaustive indexed searching is required.

A citation-context tool is valuable but non-blocking when absent. Record the limitation rather than treating it as evidence absence.

## Scopus and Web of Science

Do not describe Scopus or Web of Science as installable platform plugins unless a real connector is available to that user.

When the protocol requires them and direct integration is unavailable:

1. generate the exact database-specific query;
2. direct the user to the correct search interface or use an authorized browser workflow when available;
3. specify export settings and fields;
4. ingest the exported file;
5. validate row counts and required metadata;
6. record the exact run in the Search Log.

The agent should do as much as the platform allows; the user should only perform steps that require institutional authentication, explicit consent, or capabilities the platform cannot automate.

## Platform adapters

Platform-specific setup belongs outside the core methodology:

- ChatGPT/OpenAI: see `../../docs/CHATGPT.md`;
- Claude: see `../../docs/CLAUDE.md`;
- Gemini: see `../../docs/GEMINI.md`.

If those repository-level documents are not available in an installed copy of the Skill, follow the capability-role rules in this file instead.

## Research should start after preflight

Do not stop after setup. As soon as the user's research problem is sufficiently specific:

1. persist the original problem in the project workspace;
2. run a small novelty/terminology scan with the available academic tools;
3. identify nearest papers/reviews;
4. propose a refined question/contribution if necessary;
5. log the searches;
6. move into protocol design.

The default behavior is action-oriented research, not a tutorial about research tools.
