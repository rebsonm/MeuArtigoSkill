# Structured Google Drive project delivery — Skill operator protocol

This is execution guidance for the **assistant/host**, not a developer checklist for the researcher. The end user should receive one Drive project link, a concise status, and any real blockers.

## Why this exists

One test file, a created Drive folder, and a ZIP upload do **not** prove that the expected project tree was saved. This protocol verifies folders and each permitted file at its intended destination. A ZIP may be retained as an archive *in addition* to the navigable project structure.

The standard-library helper at scripts/drive_delivery.py prepares and checks a manifest. **It cannot connect to Google Drive, upload files, invoke platform tools, or independently authenticate JSON receipts.** The host must call real Drive tools, inspect their responses and collect fresh inventory and downloaded file bytes. Never manufacture tool outcomes.

## Authorization and security

1. Only operate on a designated private project root when the researcher has authorized Google Drive storage and the host has observed real writable access.
2. The local source must be in GOOGLE_DRIVE_STAGING with canonical_storage_backend GOOGLE_DRIVE. The helper rejects WORK_FALLBACK and mismatching root IDs; do not edit project flags to bypass this.
3. Scope operations to the exact authorized root and child IDs. Never access unrelated Drive projects or change folder sharing permissions.
4. Do not upload secrets, arbitrary linked files or unauthorized full-text PDFs. The helper blocks PDF/full-text paths unless the operator expressly supplies the rights-review declaration. That switch is not proof of legal entitlement.
5. Never mark any scientific gate approved as a side effect of file delivery.

## Prepare a plan

Create or confirm the actual Drive project root through the connected tool. From local project staging run:

    python scripts/drive_delivery.py plan --project-root PROJECT_PATH --drive-root-id REAL_DRIVE_FOLDER_ID --output PRIVATE_AUDIT_PATH/delivery-plan.json

The plan has deterministic relative paths, parent references, sizes and SHA-256 values. It is a **local plan, not an upload receipt**. Store the output outside the local project tree to avoid recursively changing hashes.

## Observe actual remote state

List **direct children** of each folder under the root, preserving each object's type, ID and exact parent ID. Build an inventory JSON object (schema=1, drive_root_id=REAL_DRIVE_FOLDER_ID, observed_via=LIVE_DRIVE) with one entry per observed child:

    {
      "schema": 1,
      "drive_root_id": "REAL_DRIVE_FOLDER_ID",
      "observed_via": "LIVE_DRIVE",
      "entries": [
        {
          "path": "00_Gestao_e_Continuidade",
          "type": "folder",
          "id": "REAL_SUBFOLDER_ID",
          "parent_id": "REAL_DRIVE_FOLDER_ID"
        }
      ]
    }

All identifiers above are illustrative. **Never label fixtures as live observations.** Empty or partial search results must not be guessed into a complete inventory. The relative path is built by traversing the actual parent hierarchy; folder names alone cannot identify an object uniquely.

For existing remote files, a SHA-256 value in the inventory must be computed from content **retrieved back from Drive**, not copied from the local manifest or upload result. If remote bytes cannot be read, leave SHA-256 absent. Do not claim content integrity from metadata or a file name.

## Safe folder creation: pre-inspect, persist intent, then reconcile

The host MUST NOT directly repeat a Drive `create_folder` call after an
error, timeout, tool block, interrupted workflow, or unobserved outcome.
Such a call may have succeeded remotely even when the tool response failed.
**A generic "retry" is not a recovery procedure.**

For EVERY missing folder, the ordinary `drive_delivery.py next` now returns
`CHECK_PARENT_FOR_CREATE` (not permission to call Drive). Complete the following
host-assisted guard protocol first:

1. **List the exact parent folder** using the authorized Drive connector.
   Collect all direct children through every pagination page, preserving IDs,
   names and types. Record `parent_scans` in the existing inventory:
   `[{"parent_id":"REAL_ID","complete":true,"scan_token":"FRESH_UNIQUE_SCAN_ID","children":[{"id":"CHILD_ID","name":"FOLDER_NAME","type":"folder"}],"page_evidence":[{"source":"GOOGLE_DRIVE_FILES_LIST","request_page_token":null,"next_page_token":null,"item_ids":["CHILD_ID"]}]}]`.
   Every actual Drive API listing page must be recorded in `page_evidence`:
   the first `request_page_token` is null; each subsequent request token
   matches the previous `next_page_token`; the final page explicitly returns
   null, and the union of `item_ids` matches the complete children list.
   The `scan_token` identifies a completed, actual observation, **not** an
   AI-invented nonce proving an API response. A boolean `complete:true` on
   its own is insufficient. Incomplete, unpaged or unsupported tool responses
   MUST block creation (`PARENT_PAGE_EVIDENCE_REQUIRED`,
   `PARENT_PAGINATION_INCOMPLETE` or a related validation error).
2. **Initialize the journal for an expressly confirmed new project** (once):

       python scripts/drive_create_guard.py initialize --attest-new-project --plan PRIVATE_AUDIT_PATH/delivery-plan.json --inventory PRIVATE_AUDIT_PATH/observed-drive.json --journal PRIVATE_AUDIT_PATH/create-journal.json --path RELATIVE_FOLDER_PATH --project-root PROJECT_PATH

   This attestation MUST NOT be used as a recovery path after a crash, loss of
   temporary files or an uncertain Drive create. Restore the original journal
   from durable shared storage instead. A missing journal blocks ordinary
   `prepare` and `resolve` with `JOURNAL_MISSING_RECOVERY_REQUIRED`.
3. **Persist one create intent before calling Drive** using:

       python scripts/drive_create_guard.py prepare --plan PRIVATE_AUDIT_PATH/delivery-plan.json --inventory PRIVATE_AUDIT_PATH/observed-drive.json --journal PRIVATE_AUDIT_PATH/create-journal.json --path RELATIVE_FOLDER_PATH --project-root PROJECT_PATH

   Only `CREATE_FOLDER_ONCE` authorizes **one** attempt with the exact
   name and parent ID returned. The guard journals `OUTCOME_UNKNOWN`
   before emitting that action. Store its audit file outside the research
   tree, **persist it in the designated durable shared location and verify the
   remote copy BEFORE issuing the external create call**. An unverified or
   unreachable durable copy blocks external creation. A concurrent or repeated
   attempt is blocked, not retried.
4. **Call the real Drive create tool at most once.** Regardless of whether
   it returns success, failure or an ambiguous tool error, re-list the
   parent completely and regenerate the inventory with a **new scan token**
   grounded in that actual observation.
5. **Reconcile the pending intent**:

       python scripts/drive_create_guard.py resolve --plan PRIVATE_AUDIT_PATH/delivery-plan.json --inventory PRIVATE_AUDIT_PATH/observed-drive.json --journal PRIVATE_AUDIT_PATH/create-journal.json --path RELATIVE_FOLDER_PATH --project-root PROJECT_PATH

   - `RESOLVED_EXISTING_REMOTE_FOLDER`: exactly one folder of that
     name and correct parent was observed; reuse its actual ID.
   - `REINSPECT_PARENT`: the evidence is stale; list again.
   - `BLOCKED_AMBIGUOUS_OUTCOME`: no folder observed after an uncertain
     call. **Do not blindly retry**. A human or explicit authorized
     recovery procedure must resolve this ambiguity.
   - `BLOCKED_DUPLICATE_NAME` or `BLOCKED_TYPE_CONFLICT`: stop; never
     delete, rename or move existing objects without authorized reconciliation.
   - `BLOCKED_PARENT_DRIFT`: the recorded parent is no longer the verified
     parent of the target path. Stop; never resolve an old attempt beneath a
     replaced or moved parent.
   - `BLOCKED_INCONSISTENT_TARGET_PATH`: a scanned child is not reconciled to
     the exact canonical path and remote ID expected for this project.
   - `BLOCKED_PREVIOUS_RESOLUTION_DRIFT`: a prior resolution is no longer
     observed at the same parent and ID. Never accept an earlier resolution as
     proof of current presence.
   - `REINSPECT_PARENT`: the remote observation is reused or stale. Re-list
     the actual parent and submit a new, evidence-grounded scan token.

### Interrupted sessions, journals and connector limits

Keep the create journal and its lock in an access-controlled, **durable shared
location** across retries and sessions. A temporary Python/container directory
that disappears at session end cannot reliably enforce create-once semantics.
The local helper verifies its local journal only; it cannot perform or certify
remote journal synchronization itself. The host is responsible for write and
read-back of the durable copy, and must **withhold CREATE_FOLDER_ONCE** until
its integrity and identity have been independently checked. On session restart,
restore the existing journal with the same plan hash before any further writes.
Never silently initialize a new journal to retry a previously uncertain
operation. If a leftover `.lock` exists after a crash, do not delete it
automatically: confirm that no process still owns it, preserve the journal
and audit trail, then authorize manual lock recovery. The unresolved intent
must still be reconciled, not recreated.

The connected Drive interface may expose bounded `list_folder(top_k)`
without an explicit `nextPageToken` or completeness receipt. **Do not
invent `complete:true` or `page_evidence`** based only on the returned array
length or on an
AI-generated scan token. When exhaustive listing cannot be established,
return `PARENT_PAGE_EVIDENCE_REQUIRED` (or another page-validation failure)
and report live acceptance as blocked.
A successful manual folder-creation smoke test is not evidence that this
guard was executed end-to-end by the installed Skill.

There is no Google Drive atomic compare-and-create primitive supplied by
this Skill. The guard reduces duplicate risk for a **cooperating serial
host**, but cannot prove global exactly-once behavior or independently
authenticate its user-provided observations. A concurrent actor or a
fabricated host inventory remains outside its assurance.

## Execute each safe next step

With up-to-date observations recorded outside the source project, run:

    python scripts/drive_delivery.py next --plan PRIVATE_AUDIT_PATH/delivery-plan.json --inventory PRIVATE_AUDIT_PATH/observed-drive.json

Interpret the next action:

- CHECK_PARENT_FOR_CREATE: follow the guarded pre-inspection and journal protocol above before the host may issue CREATE_FOLDER_ONCE. A bare create or blind retry is forbidden.
- UPLOAD_FILE: send that single local file into the verified parent folder only if its exact relative path is not already present.
- READ_BACK_FILE: fetch the remote file using its ID; compute SHA-256 from actual bytes and update the observed inventory.
- BLOCKED_CONFLICT: stop, preserve existing remote files, and explain duplicate names, wrong parents, size/content disagreement or type mismatch. Never silently overwrite or delete.
- DONE: all expected folders and files have been reported in the requested hierarchy, and all expected file bytes have been read back and compared.

**Re-list relevant folders after each external action**, refresh the inventory and call next again. If an external action fails or times out, inspect the actual parent and consult the persisted guard intent; never repeat folder creation automatically. A retried run must skip already verified files, not upload them again. Use real tool receipts where possible; the locally written inventory is not independently authenticated.

## Final verification and reporting

    python scripts/drive_delivery.py verify --plan PRIVATE_AUDIT_PATH/delivery-plan.json --inventory PRIVATE_AUDIT_PATH/observed-drive.json --output PRIVATE_AUDIT_PATH/delivery-result.json

If anything is missing, duplicated, inconsistent or not read back, the check returns INCOMPLETE (nonzero exit code) and explains why. Extra remote paths are reported, not deleted. If the host cannot download a binary to verify its contents, keep READBACK_REQUIRED and do not claim fully verified delivery.

The user-facing report must distinguish:

- Produced locally: the file exists in staging.
- Persisted and verified in Drive: correct remote parent, identity and readback content match.
- Scientifically validated: human scientific gates have actually been reviewed; this is **independent of** file delivery.

Never report the Drive tree as complete solely because the project's ZIP was uploaded. Do not elevate local staging to canonical scientific authority just because an inventory JSON says COMPLETE.

## Acceptance and real-world evidence

Offline regression tests in tests/test_drive_delivery.py and tests/test_drive_create_guard.py cover nested folders, partial delivery/resume, duplicate names, conflicts, missing content readback, wrong root, restricted PDF, unsafe paths and non-modification of scientific gates. A **real end-to-end test through an authorized connected Drive host**, using disposable synthetic data, is still necessary. A local fixture cannot establish live Drive integration, content access or independent user acceptance.
