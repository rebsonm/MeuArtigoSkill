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
7. **Work management** — optional task/issue/card management for the C.A.D.A. operational layer.

## Preferred implementations

When available, these are useful implementations of the roles above:

- Google Drive — persistent workspace;
- Consensus — peer-reviewed discovery;
- Scite — citation context and graph;
- Firecrawl or equivalent web-retrieval capability — publisher/repository/official-source retrieval;
- Scopus and Web of Science — indexed bibliographic databases;
- ClickUp, Jira/Atlassian, or Trello — optional C.A.D.A. work-management mirror.

These names are **not methodological requirements**. Equivalent services may fulfill the same roles.

Para não presumir capacidades de ChatGPT, Claude ou Gemini, consulte
[preflight de capacidades por plataforma](platform-capability-preflight.md).
Uma interface que importa `SKILL.md` não garante Python, acesso a
Scopus, escrita no Drive ou recibo verificável.

## First-run preflight

Storage is a blocking preflight. Resolve it before novelty scanning, protocol construction, screening, synthesis, drafting, or creating a local canonical project.

1. inspect whether Google Drive is actually available, connected, authenticated, and writable;
2. if it is available, find or create the canonical Drive project workspace before substantive work;
3. if it is not connected, surface the platform's Google Drive connect/install flow and explain briefly that Drive is the project's continuity and canonical-storage layer;
4. wait for the user's platform authorization action, then verify the connection again;
5. never claim Google Drive was installed, connected, or writable until verified;
6. if Drive is still unavailable after that attempt, explicitly ask whether the user wants to continue without Google Drive and use only Work/platform/local artifacts;
7. do not infer fallback consent from silence, from the user continuing to discuss the article, or from consent to another tool;
8. only an explicit affirmative answer authorizes fallback storage. Record `storage_policy=GOOGLE_DRIVE_FIRST`, the resulting storage state, the actor, timestamp, and fallback authorization in PROJECT_CONFIG.json and CONTINUIDADE.md;
9. if fallback is not authorized, remain blocked at storage onboarding. Do not initialize a local canonical workspace and do not perform substantive research that would create unsynchronized project state;
10. after storage is resolved, inspect the remaining tools, connectors, apps, MCP servers, browser capabilities, bibliographic sources, and script environments;
11. map each available capability to the roles above and surface useful missing non-storage integrations without blocking independent scientific work unnecessarily;
12. initialize spreadsheet/matrix management as `MATRIX_ONLY`;
13. inspect whether a work-management provider is connected; if the user already works with one or explicitly wants external task management, mirror the C.A.D.A. layer and switch to `MATRIX_PLUS_EXTERNAL`;
14. if the user has no task-management experience or preference, keep `MATRIX_ONLY` and do not pressure them to install another tool;
15. after any connection, resume the workflow without asking the user to repeat the research problem.

Installation, OAuth, account linking, or other third-party authorization always requires the user's explicit platform action.

## Minimum viable research stack

Google Drive is a special case: lack of Drive blocks substantive work until either the connection is verified or the user explicitly authorizes fallback storage.

After that storage decision is resolved, do not block the project merely because other preferred tools are unavailable. A valid minimum is:

- verified Google Drive storage, or an explicitly authorized Work/local fallback;
- at least one credible academic discovery route;
- a way to verify sources against original metadata/publisher records;
- a way to ingest structured bibliographic exports when exhaustive indexed searching is required.

A citation-context tool is valuable but non-blocking when absent. External work-management is also optional: C.A.D.A. must continue in the canonical workspace even without ClickUp, Jira, Trello, or equivalent. Record tool limitations rather than treating them as evidence absence.

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

## Research should start after storage and capability preflight

Do not start substantive research while the storage gate is unresolved. After Google Drive is verified or explicit fallback authorization is recorded, and as soon as the user's research problem is sufficiently specific:

1. persist the original problem in the project workspace;
2. run a small novelty/terminology scan with the available academic tools;
3. identify nearest papers/reviews;
4. propose a refined question/contribution if necessary;
5. log the searches;
6. move into protocol design.

The default behavior is action-oriented research, not a tutorial about research tools.
