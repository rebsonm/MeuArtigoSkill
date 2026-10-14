# Initialization hotfix — beta.4 follow-up (2026-10-14)

## Scope and evidence

An external beta.4 reviewer reported that visual matrix generation stalled during project initialization, leaving a partial workspace with no `PROTOCOLO.md`. The report is an operational observation, **not** proof of the exact root cause. The prior initializer called the XLSX subprocess without a timeout and before creating the protocol, which made this failure scenario possible.

This hotfix is limited to local workspace bootstrap and its optional XLSX output. It does not change methodological stages, the seven gates, research decisions, Drive synchronization, or any distribution release.

## Corrected behavior

1. Build the local core: scientific documents, configuration and required CSV registers.
2. Validate core files (nonempty documents, JSON validity, CSV headers, seven gates, and initial tasks).
3. Only after core verification, mark local initialization complete and close the seeded operational C.A.D.A. milestone, without claiming an XLSX or Drive sync happened.
4. Attempt optional visual XLSX construction with a bounded subprocess. Generate a temporary file and promote it only if its XLSX archive is structurally valid.
5. Record the visual matrix result separately in `PROJECT_CONFIG.json`, retaining the project on timeouts, runtime errors, generator failures or invalid XLSX files.

New local metadata:

- `status=INITIALIZING`: generated core work is not yet verified;
- `status=INITIALIZATION_BLOCKED` and `local_core_status=INVALID`: essential files are missing or invalid, so initialization is not successful;
- `status=INITIALIZED` and `local_core_status=VERIFIED`: **local core only**; this is not proof of canonical Google Drive synchronization;
- `visual_matrix_status=CREATED_VERIFIED` or `EXISTS_VERIFIED`: a validated XLSX exists;
- `visual_matrix_status=PENDING_TIMEOUT`, `PENDING_GENERATOR_FAILED`, `PENDING_RUNTIME_ERROR`, `PENDING_BUILDER_MISSING` or `PENDING_INVALID_GENERATED_XLSX`: XLSX not available, core intact;
- `visual_matrix_status=INVALID_EXISTING_XLSX_REQUIRES_REVIEW`: an existing file failed ZIP validation and **was not overwritten**.

## Recovery and reproducibility

- Re-run the same initializer with the original project arguments to complete missing core documents and retry the optional XLSX, provided the canonical storage policy allows it.
- Existing researcher documents and previously populated CSV tables are not silently overwritten. Damaged existing essential tables block initialization pending explicit reconciliation.
- If an existing XLSX is invalid, preserve it for inspection and recovery; do not automatically delete or replace researcher-controlled output.
- A successful local core does not grant a human scientific approval, perform a literature search, prove an external API operation, or bypass Google Drive FIRST storage onboarding.
- Do not promote local staging to canonical Google Drive data without actual sync verification.

## Automated regression cases

`python -m unittest tests.test_initializer_resilience -v` (or full `python -m unittest discover -s tests -v`) verifies:

- a timed-out visual generator does not block `PROTOCOLO.md`;
- failing or partial XLSX output is cleaned up;
- successful XLSX is promoted only after integrity checking;
- project resume retains an existing researcher-edited document;
- a corrupt preexisting XLSX remains untouched;
- corrupted essential CSV headers prevent a false success state;
- all seven scientific gates remain unapproved.

## Release discipline

The branch is a corrective PR candidate. Automated CI and synthetic tests are necessary but cannot replace beta users' reports across actual runtimes and canonical Google Drive. Do not merge, tag, publish, or auto-update the installed plugin as a side effect of this fix. A next beta release is a separate, explicit maintainer decision.
