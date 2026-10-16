#!/usr/bin/env python3
"""Optional Drive v3 journal readback and in-place checkpoint for one writer.

Requires an independently provisioned private audit JSON file (ID is fixed).
No create_folder, file creation, delete, move, token refresh or silent retry.
The host is responsible for writer serialization; Google Drive does NOT offer
a general, cross-agent atomic compare-and-swap guarantee through this helper.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import drive_delivery as delivery
import drive_create_guard as guard

BASE = "https://www.googleapis.com/drive/v3/files/"
UPLOAD = "https://www.googleapis.com/upload/drive/v3/files/"
MAX_JOURNAL_BYTES = 2 * 1024 * 1024


class JournalSyncError(ValueError):
    """Fixed diagnostic codes; never expose tokens or responses."""


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def request(token: str, url: str, *, method: str = "GET",
            body: bytes | None = None, opener=urlopen) -> bytes:
    if not isinstance(token, str) or len(token.strip()) < 10:
        raise JournalSyncError("DRIVE_TOKEN_MISSING")
    headers = {"Authorization": "Bearer " + token,
               "Accept": "application/json"}
    if body is not None:
        if len(body) > MAX_JOURNAL_BYTES:
            raise JournalSyncError("JOURNAL_EXCEEDS_SIZE_LIMIT")
        headers["Content-Type"] = "application/json; charset=utf-8"
    req = Request(url, headers=headers, data=body, method=method)
    try:
        with opener(req, timeout=25) as response:
            raw = response.read(MAX_JOURNAL_BYTES + 1)
    except (HTTPError, URLError, OSError, TimeoutError):
        raise JournalSyncError("DRIVE_JOURNAL_REMOTE_REQUEST_FAILED") from None
    if len(raw) > MAX_JOURNAL_BYTES:
        raise JournalSyncError("DRIVE_JOURNAL_REMOTE_TOO_LARGE")
    return raw


def verified_metadata(file_id: str, parent_id: str, token: str, *, sender=request) -> dict:
    file_id = delivery.require_drive_id(file_id)
    parent_id = delivery.require_drive_id(parent_id)
    fields = urlencode({"fields": "id,name,mimeType,parents,trashed",
                        "supportsAllDrives": "true"})
    data = sender(token, BASE + file_id + "?" + fields)
    try:
        metadata = json.loads(data)
    except (ValueError, UnicodeDecodeError):
        raise JournalSyncError("JOURNAL_METADATA_INVALID") from None
    if (not isinstance(metadata, dict) or metadata.get("id") != file_id or
            metadata.get("mimeType") not in ("application/json", "text/plain",
                                              "application/octet-stream") or
            metadata.get("parents") != [parent_id] or
            metadata.get("trashed") is True):
        raise JournalSyncError("JOURNAL_REMOTE_IDENTITY_MISMATCH")
    return metadata


def fetch_journal(file_id: str, parent_id: str, token: str, plan: dict,
                  *, sender=request) -> bytes:
    verified_metadata(file_id, parent_id, token, sender=sender)
    raw = sender(token, BASE + file_id + "?alt=media")
    if not raw or len(raw) > MAX_JOURNAL_BYTES:
        raise JournalSyncError("JOURNAL_REMOTE_CONTENT_UNAVAILABLE")
    try:
        journal = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        raise JournalSyncError("JOURNAL_REMOTE_JSON_INVALID") from None
    if not isinstance(journal, dict) or journal.get("schema") != guard.SCHEMA:
        raise JournalSyncError("JOURNAL_REMOTE_SCHEMA_INVALID")
    if (journal.get("drive_root_id") != plan.get("drive_root_id") or
            journal.get("plan_sha256") != guard.plan_hash(plan) or
            not isinstance(journal.get("operations"), dict)):
        raise JournalSyncError("JOURNAL_REMOTE_PLAN_MISMATCH")
    return raw


def remote_matches(file_id: str, parent_id: str, token: str,
                   plan: dict, expected_sha256: str, *, sender=request) -> dict:
    if not isinstance(expected_sha256, str) or not delivery.HASH.fullmatch(expected_sha256):
        raise JournalSyncError("EXPECTED_JOURNAL_SHA_INVALID")
    observed = fetch_journal(file_id, parent_id, token, plan, sender=sender)
    remote_sha = digest(observed)
    if remote_sha != expected_sha256:
        raise JournalSyncError("JOURNAL_REMOTE_SHA_MISMATCH")
    return {"action": "JOURNAL_REMOTE_VERIFIED", "remote_file_id": file_id,
            "sha256": remote_sha, "bytes": len(observed)}


def push_once(file_id: str, parent_id: str, token: str,
              plan: dict, local_path: Path, expected_remote_sha256: str,
              *, sender=request) -> dict:
    """One PATCH against an already-bound file, then read-after-write.

    If PATCH errors, re-read to distinguish completed effect from uncertainty.
    It never retries PATCH; a stale remote or ambiguous result blocks.
    The expected previous hash is a sanity check, not global CAS.
    """
    if not delivery.HASH.fullmatch(expected_remote_sha256):
        raise JournalSyncError("EXPECTED_JOURNAL_SHA_INVALID")
    local_path = Path(local_path)
    if local_path.is_symlink() or not local_path.is_file():
        raise JournalSyncError("JOURNAL_LOCAL_NOT_REGULAR_FILE")
    local = local_path.read_bytes()
    if len(local) > MAX_JOURNAL_BYTES:
        raise JournalSyncError("JOURNAL_EXCEEDS_SIZE_LIMIT")
    try:
        obj = json.loads(local)
    except (ValueError, UnicodeDecodeError):
        raise JournalSyncError("JOURNAL_LOCAL_INVALID") from None
    if (not isinstance(obj, dict) or obj.get("schema") != guard.SCHEMA or
            obj.get("plan_sha256") != guard.plan_hash(plan) or
            obj.get("drive_root_id") != plan["drive_root_id"]):
        raise JournalSyncError("JOURNAL_LOCAL_PLAN_MISMATCH")
    prior = fetch_journal(file_id, parent_id, token, plan, sender=sender)
    if digest(prior) != expected_remote_sha256:
        raise JournalSyncError("JOURNAL_REMOTE_CHANGED_NO_WRITE")
    target_sha = digest(local)
    if target_sha == expected_remote_sha256:
        return {"action": "JOURNAL_ALREADY_VERIFIED", "sha256": target_sha,
                "remote_file_id": file_id}
    url = UPLOAD + file_id + "?uploadType=media&supportsAllDrives=true"
    uncertain = False
    try:
        sender(token, url, method="PATCH", body=local)
    except JournalSyncError:
        uncertain = True
    # Even a successful response needs independent downloaded-byte readback.
    try:
        remote = fetch_journal(file_id, parent_id, token, plan, sender=sender)
    except JournalSyncError:
        raise JournalSyncError("JOURNAL_WRITE_OUTCOME_UNVERIFIED") from None
    if digest(remote) != target_sha:
        raise JournalSyncError("JOURNAL_WRITE_OUTCOME_UNVERIFIED" if uncertain
                               else "JOURNAL_POST_WRITE_SHA_MISMATCH")
    return {"action": "JOURNAL_REMOTE_VERIFIED_AFTER_WRITE",
            "remote_file_id": file_id, "sha256": target_sha,
            "previous_sha256": expected_remote_sha256,
            "ambiguous_response_reconciled": uncertain}


def restore(file_id: str, parent_id: str, token: str,
            plan: dict, destination: Path, *, project_root: Path,
            sender=request) -> dict:
    """Restore matching plan journal into a new local file; no overwrite."""
    destination = Path(destination).absolute()
    root = Path(project_root).resolve()
    if destination.resolve() == root or root in destination.resolve().parents:
        raise JournalSyncError("JOURNAL_MUST_BE_OUTSIDE_PROJECT")
    if destination.exists() or destination.is_symlink():
        raise JournalSyncError("LOCAL_JOURNAL_EXISTS_NO_OVERWRITE")
    raw = fetch_journal(file_id, parent_id, token, plan, sender=sender)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=destination.parent,
                                         prefix=".journal-restore-", delete=False) as f:
            temp = Path(f.name)
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        # Fail closed if a previous restore appeared in the meantime.
        if destination.exists() or destination.is_symlink():
            raise JournalSyncError("LOCAL_JOURNAL_EXISTS_NO_OVERWRITE")
        # Exclusive hard-link registration avoids clobbering concurrent restore.
        os.link(temp, destination)
    finally:
        if temp is not None and temp.exists():
            temp.unlink()
    return {"action": "JOURNAL_RESTORED", "sha256": digest(raw),
            "remote_file_id": file_id, "local_path": str(destination)}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("verify", "push", "restore"))
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--remote-file-id", required=True)
    p.add_argument("--audit-parent-id", required=True)
    p.add_argument("--journal", type=Path, required=True)
    p.add_argument("--project-root", type=Path)
    p.add_argument("--expected-remote-sha256")
    args = p.parse_args()
    try:
        plan = delivery.load_json(args.plan)
        guard.plan_hash(plan)
        token = os.environ.get("MEU_ARTIGO_DRIVE_ACCESS_TOKEN", "")
        if args.command in ("verify", "push") and not args.expected_remote_sha256:
            raise JournalSyncError("EXPECTED_JOURNAL_SHA_REQUIRED")
        if args.command == "verify":
            result = remote_matches(args.remote_file_id, args.audit_parent_id, token,
                                    plan, args.expected_remote_sha256)
        elif args.command == "push":
            result = push_once(args.remote_file_id, args.audit_parent_id, token,
                               plan, args.journal, args.expected_remote_sha256)
        else:
            if args.project_root is None:
                raise JournalSyncError("PROJECT_ROOT_REQUIRED")
            result = restore(args.remote_file_id, args.audit_parent_id, token,
                             plan, args.journal, project_root=args.project_root)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError):
        # Error classes are sanitized; no tokens, response bodies, or URLs.
        print(json.dumps({"action": "BLOCKED",
                          "reason": "JOURNAL_SYNC_BLOCKED_CONSULT_OPERATOR_LOG"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
