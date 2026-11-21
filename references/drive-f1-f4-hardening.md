# Stage 07: Drive F1-F4 journal and pagination hardening (synthetic)

Source of truth remains the independently authenticated Google Drive v3
all-MIME listing, exact parent ID, and a durable journal anchored by F7-F9.
The host must not interpret a folder-only connector result as permission to create.

## Contract extensions
- Every operation in a journal must refer to an existing folder path in the
  immutable delivery plan. File paths and unknown paths block recovery.
- Parent IDs, attempt IDs, scan observations, state transitions, and resolved
  remote IDs are validated. Root children cannot silently change parent.
- There may be at most one unresolved create intent. A resolved journal
  must identify a different later scan, not replay its pre-create evidence.
- Missing journal requires restore from a separately trusted pinned digest.
  A matching plan hash is insufficient to prove the journal is the latest.
- Remote checkpoint PATCH is single-attempt. Any timeout or readback mismatch
  results in an unresolved state; no automatic retry is permitted.
- No code can treat a field value `create_permitted` or `CREATE_FOLDER_ONCE`
  as authorization to bypass F7-F8 signed external CAS and human authorization.

## Evidence and limits
`tests/test_drive_f1_f4_hardening.py` includes negative fixtures for malformed
intents, name/type collisions, incomplete pagination, wrong parents, and a
tampered remote journal. CI proof remains synthetic and cannot establish live
Google Drive race freedom, remote high-watermark atomicity, or OAuth scopes.
Do not enable real Drive writes during this stage.
