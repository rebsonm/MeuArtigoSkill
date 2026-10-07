# Plugin and source onboarding

## Goal

A user should not need to know which research integrations are required. On the first run, inspect available tools and guide installation/connection before the research becomes dependent on them.

## Declared research integrations

The skill expects these integrations when available:

- Google Drive — persistent workspace, PDFs, Docs, Sheets, exports, continuity state.
- Consensus — peer-reviewed discovery, terminology calibration, novelty scanning, nearby literature.
- Scite — citation context, citation graph, literature verification, full-text support where licensed.
- Firecrawl — web/publisher/repository/official-source retrieval and structured extraction.

Scite may require a paid plan or active trial. Its absence must not block the entire workflow; record the limitation and continue with valid alternatives.

## First-run preflight

Before large-scale research:

1. inspect whether the declared integrations are available and connected;
2. if a missing integration exists in the plugin directory, surface the install/connect action to the user;
3. explain in one short sentence why it is useful;
4. never claim it was installed or connected until verified;
5. continue any independent work while the user authorizes connections;
6. after connection, immediately resume the research workflow without asking the user to repeat the research problem.

Installation/connection requires the user's explicit platform action. Do not pretend that a Skill can silently authorize third-party services.

## Minimum viable research stack

Do not block the project merely because every integration is unavailable. A valid minimum is:

- persistent storage or a local fallback;
- at least one credible academic discovery route;
- web/publisher verification capability;
- a way to ingest structured bibliographic exports when exhaustive indexed searching is required.

## Scopus and Web of Science

Do not describe Scopus or Web of Science as installable ChatGPT plugins unless a real connector is available to that user.

When the protocol requires them and direct integration is unavailable:

1. generate the exact database-specific query;
2. direct the user to the correct search interface or use an authorized browser workflow when available;
3. specify export settings and fields;
4. ingest the exported file;
5. validate row counts and required metadata;
6. record the exact run in the Search Log.

The Skill should do as much of the work as tools allow; the user should only perform steps that require their institutional authentication or explicit consent.

## Research should start after preflight

Do not stop after setup. As soon as the user's research problem is sufficiently specific:

1. persist the original problem in the project workspace;
2. run a small novelty/terminology scan with available academic tools;
3. identify nearest papers/reviews;
4. propose a refined question/contribution if necessary;
5. log the searches;
6. move into protocol design.

The default behavior is action-oriented research, not a tutorial about research tools.
