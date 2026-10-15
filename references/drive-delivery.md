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

## Execute each safe next step

With up-to-date observations recorded outside the source project, run:

    python scripts/drive_delivery.py next --plan PRIVATE_AUDIT_PATH/delivery-plan.json --inventory PRIVATE_AUDIT_PATH/observed-drive.json

Interpret the next action:

- CREATE_FOLDER: use the connected host Drive tool and its exact parent ID; retrieve the created ID.
- UPLOAD_FILE: send that single local file into the verified parent folder only if its exact relative path is not already present.
- READ_BACK_FILE: fetch the remote file using its ID; compute SHA-256 from actual bytes and update the observed inventory.
- BLOCKED_CONFLICT: stop, preserve existing remote files, and explain duplicate names, wrong parents, size/content disagreement or type mismatch. Never silently overwrite or delete.
- DONE: all expected folders and files have been reported in the requested hierarchy, and all expected file bytes have been read back and compared.

**Re-list relevant folders after each external action**, refresh the inventory and call next again. If the action fails or times out, perform fresh inspection before retrying. A retried run must skip already verified files, not upload them again. Use real tool receipts where possible; the locally written inventory is not independently authenticated.

## Final verification and reporting

    python scripts/drive_delivery.py verify --plan PRIVATE_AUDIT_PATH/delivery-plan.json --inventory PRIVATE_AUDIT_PATH/observed-drive.json --output PRIVATE_AUDIT_PATH/delivery-result.json

If anything is missing, duplicated, inconsistent or not read back, the check returns INCOMPLETE (nonzero exit code) and explains why. Extra remote paths are reported, not deleted. If the host cannot download a binary to verify its contents, keep READBACK_REQUIRED and do not claim fully verified delivery.

The user-facing report must distinguish:

- Produced locally: the file exists in staging.
- Persisted and verified in Drive: correct remote parent, identity and readback content match.
- Scientifically validated: human scientific gates have actually been reviewed; this is **independent of** file delivery.

Never report the Drive tree as complete solely because the project's ZIP was uploaded. Do not elevate local staging to canonical scientific authority just because an inventory JSON says COMPLETE.

## Acceptance and real-world evidence

Offline regression tests in tests/test_drive_delivery.py cover nested folders, partial delivery/resume, duplicate names, conflicts, missing content readback, wrong root, restricted PDF, unsafe paths and non-modification of scientific gates. A **real end-to-end test through an authorized connected Drive host**, using disposable synthetic data, is still necessary. A local fixture cannot establish live Drive integration, content access or independent user acceptance.
