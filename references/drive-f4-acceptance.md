# F4 — Drive authentication and continuity acceptance protocol

Status: **F4 code-contract tests passed; live authenticated end-to-end acceptance NOT VERIFIED**.
Source: PR #74, commit 460b31c2e220f8ed1494a4272acd0c280e76cce2.
CI run: https://github.com/rebsonm/MeuArtigoSkill/actions/runs/38834078556 (861 Python tests, PASS).

## Responsibility and authorship boundaries

| Role | Contribution / responsibility | Status |
|---|---|---|
| Repository owner / researcher (user) | Original Meu Artigo concept and scientific requirements, choice of deployment, rights to connected Drive resources, decisions about real credentials, scientific approvals, merge and publication | USER AUTHORITY; never inferred from a test result |
| ChatGPT assistant | Incremental proposed/committed code, regression tests and technical documentation for this F4 phase, including SHA-256 recovery pin and synthetic end-to-end suite | ASSISTANT-IMPLEMENTED; requires maintainer review |
| GitHub Actions | Executes automated test and packaging workflows | CI EVIDENCE, not scientific or real provider acceptance |
| Google Drive API / connected provider | Returns actual remote resource IDs, parent metadata, pagination and file bytes if accessed through an authorized client | PROVIDER OBSERVATIONS; scope and completeness must be demonstrated |
| Independent human reviewer | Evaluates behavior, security posture, concurrency and go/no-go decision | NOT PERFORMED BY THIS PHASE |

This is an accountability split, not a transfer or determination of legal copyright.
Do not attribute AI-produced source patches to the researcher as personally written
without review. Do not attribute the original scientific concept or prior software to the
assistant. Human scientific decisions remain entirely with the researcher.

## Evidence available

- The synthetic Google Drive test root was independently re-read via the
  connected ChatGPT Drive tool: 1C6RvyN9XTKtEX8UYHRwCvNRK14dY2mNM.
  The subfolder 01_Dados (1V7u7LsbUAAf5s8tSpJhhkh9yGLjMw-BQ) still has
  the expected parent ID. This verifies an existing resource relationship,
  not a full authenticated API pagination / journal restore test.
- New test file: tests/test_drive_f4_integrated_contract.py. It invokes the
  actual production guard, pagination and checkpoint modules against in-memory
  simulated Drive behaviors: error after side effect, error without side effect,
  and interruption after intent persistence but before create. No live OAuth used.
- Recovery hardening: scripts/drive_journal_checkpoint.py now requires an
  independently retained expected_remote_sha256 when restoring a journal.
  A valid but older journal with an empty operations map is refused if its
  digest differs. The supplied digest must not be copied from the same
  untrusted remote file being restored.
- CI: 861 Python tests passed; packaging verification passed on audited head
  460b31c2e220f8ed1494a4272acd0c280e76cce2. A passing CI remains
  synthetic evidence, not proof of production readiness.

## Live acceptance checklist (NOT YET PASSED)

1. An expressly authorized secure executor with official Google Drive API access,
   scoped to an isolated synthetic project and private audit folder, is available.
   Tokens remain in that executor's secure environment. Nothing is pasted into
   chats, issues, PRs or scientific project folders.
2. Read each direct parent using Drive v3 files.list, retaining all authoritative
   nextPageToken receipts through a terminal response and checking incompleteSearch.
   The connected ChatGPT list_folder tool alone does not currently expose them.
3. An audit journal file is explicitly provisioned once, its fixed ID and exact
   parent ID recorded securely, and a separate trusted checkpoint digest retained.
   A missing journal or lost trusted SHA prevents automatic recovery.
4. The executor serializes writes as a single authorized writer. The helpers do
   not implement a global atomic compare-and-swap, distributed lease or Drive
   transaction. Independent concurrent writers remain out of scope.
5. Before create_folder: persist OUTCOME_UNKNOWN locally, upload the exact
   serialized journal to the fixed audit file, download its bytes again and
   independently verify its SHA-256. Withhold create if this step fails.
6. Under synthetic host fault injection, execute exactly one create attempt.
   Simulate an ambiguous response after a remotely successful side effect:
   fresh parent scan, reuse exactly one observed folder ID, record RESOLVED,
   checkpoint the updated journal and verify its readback.
7. Under fault injection with no side effect: preserve OUTCOME_UNKNOWN and
   report BLOCKED_AMBIGUOUS_OUTCOME without a second create attempt.
8. Simulate session restart using only the known journal ID and the independently
   retained SHA-256: restore into a new local audit path, verify the remote
   plan/root binding and check that no duplicate create can be authorized.
9. Verify parent drift, duplicate names, stale cursor, remote journal rollback
   and readback mismatches block cleanly; preserve all scientific gates pending.
10. Capture time-stamped receipts for each real operation, redacting access
    tokens and protected research information. Do not claim success from
    a generated inventory, fake screenshot or a local fixture.

Only after a maintainer independently reviews these receipts and confirms the
single-writer model may the PR be considered for merge. An authorized merge
and any release/publication must remain separate deliberate actions.

## Decision

**NO-GO for merge today.** F4 programmatic simulation and a separate existing
Drive metadata read have been performed; genuine API OAuth scanning, real
persisted checkpoint recovery and fault injection through the intended host
remain unverified. Keep PR #74 in Draft and do not update the installed Skill.

The following work is still a tool/infrastructure obligation, not a request
to manually conduct the research: provide a secure OAuth-capable executor,
provision a private audit JSON file in a disposable folder, and run the
recorded acceptance protocol with genuine authenticated receipts.
