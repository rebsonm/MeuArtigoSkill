#!/usr/bin/env python3
"""F7 independent, HMAC-authenticated, append-only journal checkpoint receipts.

No Drive mutations or token storage. The already existing remote journal is
read back before sealing. The local receipt directory is a *separate trusted
executor store*, outside research outputs. A trusted high-watermark (latest
receipt SHA-256) MUST persist in a separate secure authority across sessions.
A valid older chain remains indistinguishable if that head is lost.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import stat

import drive_create_guard as guard
import drive_delivery as delivery
import drive_journal_checkpoint as checkpoint

SCHEMA = "MEU_ARTIGO_DRIVE_CHECKPOINT_ANCHOR_V1"
FILE_NAME = re.compile(r"[0-9]{8}\.json\Z")
MAX_RECEIPTS = 10000


class AnchorError(ValueError):
    """Fixed, non-sensitive errors."""


def key_from_env() -> bytes:
    encoded = os.environ.get("MEU_ARTIGO_DRIVE_AUDIT_HMAC_KEY", "")
    try:
        key = base64.b64decode(encoded, validate=True)
    except (ValueError, base64.binascii.Error):
        raise AnchorError("ANCHOR_KEY_UNAVAILABLE") from None
    if len(key) < 32:
        raise AnchorError("ANCHOR_KEY_UNAVAILABLE")
    return key


def canonical(value: dict) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False) + "\n").encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def mac_for(payload: dict, key: bytes) -> str:
    if not isinstance(key, bytes) or len(key) < 32:
        raise AnchorError("ANCHOR_KEY_UNAVAILABLE")
    return hmac.new(key, canonical(payload), hashlib.sha256).hexdigest()


def archive_files(directory: Path, project_root: Path) -> list[Path]:
    directory = Path(directory).absolute()
    root = Path(project_root).resolve()
    if (directory.resolve() == root or root in directory.resolve().parents or
            directory.is_symlink() or not directory.is_dir()):
        raise AnchorError("ANCHOR_PRIVATE_DIRECTORY_REQUIRED")
    if stat.S_IMODE(directory.stat().st_mode) & 0o077:
        raise AnchorError("ANCHOR_DIRECTORY_PERMISSIONS_TOO_BROAD")
    entries = list(directory.iterdir())
    if len(entries) > MAX_RECEIPTS or any(
            item.is_symlink() or not item.is_file() or not FILE_NAME.fullmatch(item.name)
            for item in entries):
        raise AnchorError("ANCHOR_UNEXPECTED_OR_UNSAFE_ENTRY")
    return sorted(entries, key=lambda item: item.name)


def read_verified_chain(directory: Path, plan: dict, audit_parent_id: str,
                        audit_file_id: str, key: bytes, project_root: Path,
                        expected_head: str | None) -> dict:
    delivery.check_plan(plan)
    delivery.require_drive_id(audit_parent_id)
    delivery.require_drive_id(audit_file_id)
    files = archive_files(directory, project_root)
    if not files:
        if expected_head is not None:
            raise AnchorError("ANCHOR_HISTORY_MISSING")
        return {"count": 0, "head_sha256": None, "journal_sha256": None}
    if (not isinstance(expected_head, str) or
            not delivery.HASH.fullmatch(expected_head)):
        raise AnchorError("ANCHOR_PINNED_HEAD_REQUIRED")
    previous_head = None
    previous_journal = None
    for n, path in enumerate(files, 1):
        if path.name != f"{n:08d}.json":
            raise AnchorError("ANCHOR_HISTORY_GAP")
        if stat.S_IMODE(path.stat().st_mode) & 0o077:
            raise AnchorError("ANCHOR_RECEIPT_PERMISSIONS_TOO_BROAD")
        raw = path.read_bytes()
        if len(raw) > 8192:
            raise AnchorError("ANCHOR_RECEIPT_TOO_LARGE")
        try:
            doc = json.loads(raw)
        except (ValueError, UnicodeDecodeError):
            raise AnchorError("ANCHOR_RECEIPT_INVALID") from None
        if not isinstance(doc, dict) or set(doc) != {"payload", "mac"}:
            raise AnchorError("ANCHOR_RECEIPT_INVALID")
        payload = doc["payload"]
        if not isinstance(payload, dict) or not isinstance(doc["mac"], str):
            raise AnchorError("ANCHOR_RECEIPT_INVALID")
        if not hmac.compare_digest(mac_for(payload, key), doc["mac"]):
            raise AnchorError("ANCHOR_HMAC_INVALID")
        if (payload.get("schema") != SCHEMA or payload.get("sequence") != n or
                payload.get("drive_root_id") != plan["drive_root_id"] or
                payload.get("plan_sha256") != guard.plan_hash(plan) or
                payload.get("audit_file_id") != audit_file_id or
                payload.get("audit_parent_id") != audit_parent_id or
                payload.get("previous_head_sha256") != previous_head or
                not isinstance(payload.get("journal_sha256"), str) or
                not delivery.HASH.fullmatch(payload["journal_sha256"])):
            raise AnchorError("ANCHOR_CHAIN_OR_SCOPE_INVALID")
        if previous_journal == payload["journal_sha256"]:
            raise AnchorError("ANCHOR_REPEATED_JOURNAL_STATE")
        previous_journal = payload["journal_sha256"]
        previous_head = sha(raw)
    if not hmac.compare_digest(expected_head, previous_head):
        raise AnchorError("ANCHOR_TRUSTED_HEAD_MISMATCH")
    return {"count": len(files), "head_sha256": previous_head,
            "journal_sha256": previous_journal}


def seal_remote_checkpoint(directory: Path, project_root: Path, plan: dict,
                           audit_parent_id: str, audit_file_id: str, token: str,
                           journal_sha256: str, key: bytes, expected_head: str | None,
                           *, authorized_initial_bootstrap: bool = False,
                           sender=checkpoint.request) -> dict:
    """Seal a remotely verified SHA once, writing a new non-overwriting receipt.

    expected_head is the trusted value held separately by the executor.
    On first receipt only, expected_head is null and the directory MUST be empty.
    """
    if not isinstance(key, bytes) or len(key) < 32:
        raise AnchorError("ANCHOR_KEY_UNAVAILABLE")
    if expected_head is None and not authorized_initial_bootstrap:
        raise AnchorError("ANCHOR_NEW_HISTORY_ATTESTATION_REQUIRED")
    if expected_head is not None and authorized_initial_bootstrap:
        raise AnchorError("ANCHOR_BOOTSTRAP_ONLY_FOR_NEW_HISTORY")
    chain = read_verified_chain(directory, plan, audit_parent_id, audit_file_id,
                                key, project_root, expected_head)
    if (not isinstance(journal_sha256, str) or
            not delivery.HASH.fullmatch(journal_sha256)):
        raise AnchorError("ANCHOR_JOURNAL_SHA_INVALID")
    if chain["journal_sha256"] == journal_sha256:
        raise AnchorError("ANCHOR_REPEATED_JOURNAL_STATE")
    # Real provider-downloaded bytes must match BEFORE storing a receipt.
    checkpoint.remote_matches(audit_file_id, audit_parent_id, token, plan,
                              journal_sha256, sender=sender)
    n = chain["count"] + 1
    if n > MAX_RECEIPTS:
        raise AnchorError("ANCHOR_RECEIPT_LIMIT")
    payload = {
        "schema": SCHEMA, "sequence": n,
        "drive_root_id": plan["drive_root_id"],
        "plan_sha256": guard.plan_hash(plan),
        "audit_parent_id": audit_parent_id, "audit_file_id": audit_file_id,
        "journal_sha256": journal_sha256,
        "previous_head_sha256": chain["head_sha256"],
    }
    raw = canonical({"payload": payload, "mac": mac_for(payload, key)})
    path = Path(directory).absolute() / f"{n:08d}.json"
    fd = None
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "wb") as stream:
            fd = None
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        dir_fd = os.open(str(Path(directory).absolute()), flags)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    finally:
        if fd is not None:
            os.close(fd)
    return {"action": "ANCHOR_RECEIPT_SEALED", "sequence": n,
            "head_sha256": sha(raw), "journal_sha256": journal_sha256,
            "external_head_persistence_required": True}


def verify_remote_against_anchor(directory: Path, project_root: Path,
                                 plan: dict, audit_parent_id: str,
                                 audit_file_id: str, token: str,
                                 expected_head: str, key: bytes, *,
                                 sender=checkpoint.request) -> dict:
    if not isinstance(key, bytes) or len(key) < 32:
        raise AnchorError("ANCHOR_KEY_UNAVAILABLE")
    chain = read_verified_chain(directory, plan, audit_parent_id,
                                audit_file_id, key, project_root, expected_head)
    if chain["count"] == 0:
        raise AnchorError("ANCHOR_HISTORY_MISSING")
    checkpoint.remote_matches(audit_file_id, audit_parent_id, token, plan,
                              chain["journal_sha256"], sender=sender)
    return {"action": "ANCHOR_AND_REMOTE_MATCH", **chain,
            "create_permitted": False}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("seal", "verify"))
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--project-root", type=Path, required=True)
    p.add_argument("--archive", type=Path, required=True)
    p.add_argument("--audit-parent-id", required=True)
    p.add_argument("--audit-file-id", required=True)
    p.add_argument("--journal-sha256")
    p.add_argument("--expected-head")
    p.add_argument("--attest-initial-anchor", action="store_true",
                   help="Only first checkpoint of an explicitly new archive; never for recovery.")
    args = p.parse_args()
    try:
        plan = delivery.load_json(args.plan)
        key = key_from_env()
        token = os.environ.get("MEU_ARTIGO_DRIVE_ACCESS_TOKEN", "")
        if args.command == "verify":
            if not args.expected_head:
                raise AnchorError("ANCHOR_PINNED_HEAD_REQUIRED")
            result = verify_remote_against_anchor(args.archive,
                        args.project_root, plan, args.audit_parent_id,
                        args.audit_file_id, token, args.expected_head, key)
        else:
            if not args.journal_sha256:
                raise AnchorError("ANCHOR_JOURNAL_SHA_REQUIRED")
            result = seal_remote_checkpoint(args.archive, args.project_root,
                     plan, args.audit_parent_id, args.audit_file_id,
                     token, args.journal_sha256, key, args.expected_head,
                     authorized_initial_bootstrap=args.attest_initial_anchor)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError):
        print(json.dumps({"action": "BLOCKED", "reason": "ANCHOR_OPERATOR_BLOCKED"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
