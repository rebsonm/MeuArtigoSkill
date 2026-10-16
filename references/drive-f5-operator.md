# F5 — isolated host orchestrator for one guarded folder create

Status: assistant-authored experimental code, tested with simulated Drive
responses only. User/researcher remains the project owner and decision maker.
Do not treat a green CI run as real installed-Skill/OAuth acceptance.

## Ownership of contributions

- **Researcher/project maintainer (user):** original Meu Artigo project and
  scientific methods, project requirements, permission decisions, real
  research data, human scientific gates, choice to review/merge/publish.
- **Assistant (this F5 phase):** new
  `scripts/drive_f5_operator.py`, its unit/integration test contracts,
  operational runbook, future recommendations and any corrective commits.
- **Provider/CI evidence:** GitHub Actions can test the source with mocks.
  Actual Google Drive folder names, IDs and parent relationships require
  authorized provider observations. Neither represents human scientific approval.
- No legal copyright assignment is implied by this division.

## Why one operator?

Before F5, an authorized host would need to call pagination, guard and journal
checkpoint helpers in a precisely ordered sequence. The operator now performs
this sequence in one process for a **single immediate child folder** of an
already existing, isolated synthetic project root.

### Safety invariants

1. Uses OAuth supplied by a separately authorized external executor. It cannot
   access ChatGPT connected-plugin OAuth. Never paste tokens into chat or GitHub.
2. Checks the remote project root ID and requires its actual provider-observed
   name to begin with `MEU_ARTIGO_PR74_TESTE_SINTETICO_`. The requested folder
   must be an immediate child in the canonical delivery plan.
3. Validates the independently known previous remote journal SHA-256 and
   requires local journal bytes to match that remote checkpoint.
4. Lists the exact root via the official Google Drive v3 API, following every
   `nextPageToken`, validating IDs, type and page evidence.
5. **Default execution is read-only precheck**, producing
   `PRECHECK_ONLY_NO_CREATE`. It creates no journal intent or Drive folder.
6. Only the distinct CLI flag `--execute-synthetic-create` enables mutations.
   Under a local host lock the operator rechecks root, checkpoint and inventory.
   It writes `OUTCOME_UNKNOWN` to a local private journal, checkpoints the
   exact bytes remotely, reads them back and verifies SHA-256 **before** one
   folder-create POST is allowed.
7. Whether the POST succeeds or fails ambiguously, it scans again, reconciles
   the exact remote folder ID and checkpoints a RESOLVED journal. On absent,
   duplicate or inconsistent evidence it blocks; it does not repeat POST.
8. If interrupted, a persisted intent blocks retries. A local `.f5-host.lock`
   left after a crash is not automatically broken. An external writer on another
   machine can still bypass this local lock; distributed concurrency is not
   solved by Google Drive.
9. Neither the operator nor its tests modify scientific gates, actual research
   projects or the installed beta.6 Skill.

## Preconditions for authorized live acceptance

An independent operator must first create a dedicated disposable synthetic
project and a separate private audit folder and **existing JSON journal file**,
record their real Drive IDs, and retain the journal's prior expected SHA-256
independently. The local journal must match the preprovisioned remote journal
bit-for-bit and match the canonical plan. Use a secure sandbox; do not place
credentials or private research corpus in test folders.

The ChatGPT Drive connector does not expose a credential that can be copied
to Python; this process needs separately authorized OAuth in a secure executor
with only the scopes and folder access it requires.

Example safe, read-only precheck:

    python scripts/drive_f5_operator.py --plan PRIVATE/plan.json --journal PRIVATE/create-journal.json --project-root SYNTHETIC_PROJECT --path 01_Dados --audit-parent-id REAL_AUDIT_PARENT_ID --audit-file-id REAL_AUDIT_FILE_ID --expected-remote-sha256 INDEPENDENTLY_RETAINED_SHA256

The above reads metadata, remote journal and paginated children; it performs
no create or checkpoint mutation. It must return PRECHECK_ONLY_NO_CREATE
for a missing and authorizable first-level folder.

**Only following explicit operator authorization for the disposable test**
may the same command be invoked with `--execute-synthetic-create`.
This issues at most one Drive folder POST after remote intent readback,
and records the outcome. The user in this chat has authorized continued
development, not exposure of credentials or mutation of research projects.
No authenticated F5 POST has been executed here.

## Acceptance evidence classification

| Step | Synthetic test | Live authenticated |
|---|---|---|
| Root ID and synthetic folder name verification | Included | Not executed |
| Complete API pagination and exact parent child scan | Included | Not executed |
| Local + remote journal initial digest match | Included | Not executed |
| Read-only by default / explicit mutation gate | Included | Not executed |
| Persist and read back intent before one POST | Included | Not executed |
| Timeout with side effect / without side effect | Included | Not executed |
| New resolved journal remote readback | Included | Not executed |
| Cross-session recovery with trusted pinned SHA | F4 synthetic tests | Not executed |
| Multi-host concurrent writers / global exactly-once | Outside proof | Not guaranteed |
| Scientific review by researcher | Not a technical test | Requires human decisions |

## Exit criteria

Until a separate authorized environment executes and records the real API
trace, this phase remains **integration-ready code, not deployment proof**.
Leave PR #74 Draft; do not merge, release, alter connected permissions,
or update the installed Skill without user authorization.
