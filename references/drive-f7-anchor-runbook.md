# F7 — independently anchored Drive journal receipts (EXPERIMENTAL)

## Result and evidence boundaries

The assistant has implemented optional
\`scripts/drive_f7_anchor.py\` with offline regression tests. It seals
provider-downloaded journal SHA-256 checkpoints into immutable numbered
HMAC-SHA256 receipts, stored in a pre-existing secure executor directory.
This is a **trust-anchor proposal**, not proof of production OAuth access,
a remote journal update, or real restart recovery.

The user's original scientific project, scientific judgments, validation gates,
authorized Drive data, project governance and publication decisions remain
the researcher's domain. New implementation, tests and this document are
assistant-generated technical work, requiring human maintainer review.
GitHub Actions provides CI evidence only; Google API evidence is only present
where explicitly identified as a connected observation.

## Threat and why an HMAC receipt chain matters

Plan/hash validation alone accepts a legitimate but **old** journal. If the
last unresolved create attempt disappears, blind retry can create duplicates.
An HMAC key held outside Drive makes forged journal-reference receipts harder,
and chaining each receipt to the preceding file lets the verifier detect
changes in history. The independent **latest head SHA-256** is still essential:
without it, an old internally valid subset of receipts could be replayed.

This mechanism does not make the remote journal immutable or supply atomic
compare-and-swap, distributed locks, Google Drive snapshots or trusted
cross-session persistence on its own. A separate, access-controlled executor
and durable external trusted high-watermark are needed. If those are absent,
**fail closed**; do not initialize a new journal or issue create_folder.

## Files and required secrets

- \`scripts/drive_f7_anchor.py\` — optional read-only remote verification
  plus local signed receipts; **never writes to Google Drive**.
- \`tests/test_drive_f7_anchor.py\` — synthetic mocks; no API credentials.
- \`MEU_ARTIGO_DRIVE_ACCESS_TOKEN\` — separate authorized OAuth token in the
  secure executor only. ChatGPT-connected Drive credentials are not exposed
  to these scripts.
- \`MEU_ARTIGO_DRIVE_AUDIT_HMAC_KEY\` — random secret key, at least 32 bytes
  represented as base64 in the secure executor; independent of the OAuth
  bearer token. Generate and retain it using the executor's secret manager;
  never paste it into chat, GitHub source, CI logs or a research project.
- \`--archive\` — existing private directory outside the project, owner-only
  permissions (0700), retained between executor sessions; each numbered
  receipt is written with 0600 permissions using exclusive creation.
- \`--expected-head\` — the SHA-256 of the latest receipt bytes, independently
  saved in a separate trusted monotonic state store. **Do not obtain it from
  the untrusted chain or Drive file being examined.**

The trust-anchor record binds the exact plan hash, Google Drive root ID,
audit file ID, audit parent ID, journal hash, sequence number and prior
receipt hash. The file contains **no OAuth or HMAC secrets**.

## Protocol — external authorized executor only

1. Use an already-provisioned, isolated **synthetic** Google Drive root
   and private audit file. Verify exact remote IDs, parent, MIME type and
   readback bytes with the existing Drive adapter. Keep all test data fictional.
2. In a newly established empty private receipt directory, verify the
   preprovisioned initial journal remotely and issue exactly one first
   receipt (without \`--expected-head\`):

       python scripts/drive_f7_anchor.py seal --attest-initial-anchor --plan PRIVATE/plan.json --project-root SYNTHETIC_PROJECT --archive PRIVATE/receipt-archive --audit-file-id REAL_AUDIT_FILE_ID --audit-parent-id REAL_AUDIT_PARENT_ID --journal-sha256 VERIFIED_INITIAL_SHA256

   The explicit `--attest-initial-anchor` flag is mandatory for this first
   creation. It must never be used after an interruption or loss of an
   existing archive. The script cannot independently establish that the
   caller has not previously created receipts on a different host.
3. Before any further operation, persist the output \`head_sha256\` in the
   **independent trusted high-watermark authority**, and verify its readback.
   This script emits \`external_head_persistence_required:true\`, not a claim
   that an external trusted store was actually updated.
4. After a later successful journal \`push\` and genuine downloaded-byte
   readback, seal the new journal SHA with \`--expected-head\` equal to the
   independently retained previous head:

       python scripts/drive_f7_anchor.py seal --plan PRIVATE/plan.json --project-root SYNTHETIC_PROJECT --archive PRIVATE/receipt-archive --audit-file-id REAL_AUDIT_FILE_ID --audit-parent-id REAL_AUDIT_PARENT_ID --journal-sha256 VERIFIED_NEW_JOURNAL_SHA256 --expected-head PREVIOUS_TRUSTED_HEAD_SHA256

5. Independently retain and verify the newly returned head **before** the
   host might perform a non-idempotent folder creation. If the head write,
   remote journal update or readback fails, do not create anything.
   F8 now **calls this F7 anchor mandatorily** from the F5 host code before
   a simulated synthetic create and after a resolved operation, but only when
   a host provides a durable independent CAS trusted-head backend. The
   repository CLI **does not implement a real external CAS adapter**, so
   `--execute-synthetic-create` remains blocked there. Do not treat passing
   synthetic tests as live acceptance; backend atomicity, actual independent
   persistence and OAuth integration remain to be implemented and approved.
6. After restarting the external executor, obtain the latest head from the
   trusted store and verify all numbered receipt files plus the exact remote
   journal content:

       python scripts/drive_f7_anchor.py verify --plan PRIVATE/plan.json --project-root SYNTHETIC_PROJECT --archive PRIVATE/receipt-archive --audit-file-id REAL_AUDIT_FILE_ID --audit-parent-id REAL_AUDIT_PARENT_ID --expected-head LATEST_TRUSTED_HEAD_SHA256

7. The verifier emits \`ANCHOR_AND_REMOTE_MATCH\` with
   \`create_permitted:false\`. Recovery does **not** authorize another folder
   create; the ordinary guarded reconciliation still needs a fresh complete
   all-MIME parent scan. If the remote is valid but has an unexpected new
   journal version, or a receipt file is missing or stale, STOP and perform
   manual authenticated reconciliation without rewriting the archive.

## Remaining acceptance criteria

- A secure external OAuth executor exists, with pre-provisioned private audit
  file and a durable independent trusted high-watermark service.
- Explicit high-watermark persistence is verified by readback across
  separate executor lifetimes, not just a local temporary directory.
- F7 anchor is integrated as a mandatory prerequisite of the F5 create path;
  the call is fail-closed when independent checkpoint storage cannot confirm.
- Use genuine Drive v3 all-MIME pagination with terminal \`nextPageToken\` and
  parent/ID checks; never promote a connected folder-only search to complete
  all-types coverage.
- Inject an ambiguous error **after** one remote side effect and recover
  through a fresh real scan, without a second create.
- Independently review the multi-writer risk, default read-only behavior,
  secret scoping, receipts, release boundary and scientific gates.

## Go/no-go

**NO-GO** on live folder-create acceptance, merge and release until the
external trust authority, OAuth integration and end-to-end evidence exist.
The original published beta and installed Skill remain unchanged.
