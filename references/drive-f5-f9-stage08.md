# Stage 08 — Drive F5–F9 security review

Scope: synthetic tests and guarded changes only in the PR #78 candidate
branch. No changes to Google Drive, the VPS, the installed distribution, or
the protected main branch.

## Safety invariants

- F5: folder creation is non-idempotent. Any creator exception, including
  an unexpected exception after a remote side effect, is an ambiguous
  outcome. Inspect the provider state again; never issue a blind second POST.
- F5: the local host lock must retain its original device and inode. If
  another actor replaces it, do not claim success or delete the foreign lock.
  This local identity check does not eliminate filesystem TOCTOU races.
- F6: connected search is read-only supporting evidence, not a proof of
  absent file/folder naming collisions across all MIME types.
- F7: an HMAC receipt chain is not authoritative without an independently
  retained latest head. Never silently reinitialize after lost state.
- F8: an external atomic CAS is mandatory before any non-idempotent POST.
  CAS failure, timeout, rejected compare, or inconsistent readback must block
  external creation. A lost response does not prove the write was absent.
- F9: DynamoDB is an optional, independently provisioned trusted-head backend.
  Require an existing table/item, least-privilege credentials, strongly
  consistent reads, an atomic conditional update, and strict response shapes.
  Unexpected response types must fail closed without exposing provider errors.

## Negative tests and limits

The additional tests in `tests/test_drive_f5_f9_stage08.py` use only fake
clients and fictional identifiers. They cover two writers racing on an old
head, a CAS timeout after a committed update, stale signed receipt replay,
lock replacement, an ambiguous post-create exception, failed fresh scans,
and malformed DynamoDB AttributeValue and Error response structures.

No credentials, AWS table, IAM policy, real Google Drive access, or external
create operations are involved. These tests do not establish real service
linearizability, cross-host durability, or end-to-end operator authorization.
The F5 command-line interface deliberately provides no live independent
CAS adapter and cannot enable external writes.

Release integration must keep the scientific human gates intact. The
resulting code must not mark scientific decisions as approved or treat
local fixtures as authenticated provider evidence.
