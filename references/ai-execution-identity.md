# AI execution identity and temporal provenance

Mandatory for every relevant AI-assisted activity, from first orientation to submission. Use the existing `AI_Use_ID` and `Trace_ID` linkage; do not create another gate, tab or identifier. Record a separate event when the model, execution environment or execution date changes. An activity executed on 2026-11-24 must not be relabeled with the date or model of a later report.

## Canonical record

In `14_AI_Use_Log.csv` and the existing `12_USO_IA` worksheet, retain all existing columns and append these fields (exact names in the CSV):

- `Platform_or_tool`: actual platform (e.g. ChatGPT, Claude, Gemini); distinguish tools used from the AI platform.
- `Model_provider`: model provider, if known.
- `Model_or_version`: exact exposed model designation including version/revision or snapshot when available. Do not equate a brand with a model. Do not infer internal aliases, hidden routes, model IDs, subscription tier or reasoning effort from the plugin version. `NOT_EXPOSED` when unavailable.
- `Model_configuration`: visible reasoning mode/effort or other material configuration, or `NOT_EXPOSED` / `NOT_APPLICABLE`.
- `Date`: actual execution date, YYYY-MM-DD, not reporting date. `Execution_timestamp`: actual ISO 8601 timestamp with offset when available, otherwise `NOT_EXPOSED` (never fabricate time or timezone).
- `Execution_environment`: `CHAT`, `WORK`, `CODEX`, `API`, `OTHER`, or `NOT_EXPOSED`. This is independent of the client and of the model. ChatGPT Work in a desktop app is WORK + DESKTOP_APP, not a separate model.
- `Client_surface`: `WEB`, `DESKTOP_APP`, `MOBILE_APP`, `CLI`, `IDE`, `API`, `OTHER`, or `NOT_EXPOSED`. Distinguish web chat, mobile app, desktop app, Codex CLI/IDE; specify actual environment rather than assume.
- `Model_identification_source` and `Environment_identification_source`: `HOST_METADATA`, `USER_REPORTED`, `MODEL_SELF_REPORTED`, `NOT_EXPOSED`, or `NOT_RECORDED` for historical gaps. Prefer verified metadata where accessible. A user label or model self-report is not independently authenticated. If the source conflicts, retain the conflict and flag for review. The exact model snapshot may remain undisclosed even if the public model name is known.
- `Meu_Artigo_version`: exact running plugin/skill version if independently readable (not the version of the report generator); otherwise `NOT_EXPOSED`. Record other tools and known versions in Notes where relevant.

In the existing `13_Traceability_Log`, fill `Timestamp`, `AI_platform_or_tool`, `Model_or_version` and document `AI_Use_ID` and execution environment/client in `Notes`, including the source of identity. Preserve the fixed TRACE header and script receipt format; do not claim SCRIPT actor itself is an AI. Link the corresponding AI-use row. On historical projects, append new columns to the existing AI-use table only during an authorized write; preserve old rows and old hashes/snapshots. Do not backfill from the current session. Unknown historical values remain blank or explicitly `NOT_RECORDED` with documented provenance gaps. Reconcile only from genuine dated records, with TRACE evidence and authorization. For new rows, every field is required; explicit unknown values are preferable to inventions. `Date` must reflect a real date or documented unknown for unavailable history. Use current session metadata or actual tool timestamp; a machine clock or upload date is not necessarily the past execution time.

## Reports and declaration

`RASTREABILIDADE.md`, the transparency report and the editorial disclosure must show the recorded provider/platform, model/version, execution date, time/offset if known, mode and client surface, configuration, plugin version and source of identification. E.g., **illustrative, not an actual execution**: ChatGPT / GPT-6.2 / WORK / DESKTOP_APP / 2026-11-24T17:43:00-03:00 / Meu Artigo 1.0.0-rc.5.1. Do not replace actual logs with this example. Multiple events may be summarized by genuinely matching identity, date and purpose; never merge different execution environments or hide dates. Retain full internal audit, protect personal data, and follow the actual journal policy. Unknown fields remain visibly unresolved. Validate new records using `scripts/ai_execution_identity.py` and `scripts/validate_project.py`. Editorial rules demanding exact model identification are not satisfied by generic platform labels or unknown identity. No automatic gate approval, AI-use completeness certification or external publication.
