#!/usr/bin/env python3
"""F5 isolated Drive API test harness: read-only precheck or ONE guarded create.

NEVER use in a real scientific project. Only already provisioned synthetic
Drive roots named MEU_ARTIGO_PR74_TESTE_SINTETICO_* are accepted; no folders,
journals, tokens or credentials are provisioned here. Live mutation requires
the separate --execute-synthetic-create switch and authorized OAuth executor.
Single-writer operation only: no global Drive transaction/CAS exists.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from pathlib import Path
from urllib.parse import urlencode

import drive_api_proof as scanner
import drive_create_guard as guard
import drive_delivery as delivery
import drive_journal_checkpoint as checkpoint
import drive_f8_trust_gate as trust_gate

FOLDER_MIME = "application/vnd.google-apps.folder"
SYNTHETIC_PREFIX = "MEU_ARTIGO_PR74_TESTE_SINTETICO_"
GET_URL = "https://www.googleapis.com/drive/v3/files/"
UPLOAD_URL = "https://www.googleapis.com/drive/v3/files"


class HostBlock(ValueError):
    """Sanitized blocking reason, never a provider URL/token/body."""


def verify_synthetic_root(root_id: str, token: str, *,
                          sender=checkpoint.request) -> None:
    root_id = delivery.require_drive_id(root_id)
    fields = urlencode({"fields": "id,name,mimeType,trashed",
                        "supportsAllDrives": "true"})
    try:
        raw = sender(token, GET_URL + root_id + "?" + fields)
        doc = json.loads(raw)
    except (ValueError, TypeError, OSError):
        raise HostBlock("SYNTHETIC_ROOT_UNVERIFIED") from None
    if (not isinstance(doc, dict) or doc.get("id") != root_id or
            doc.get("mimeType") != FOLDER_MIME or
            doc.get("trashed") is True or
            not isinstance(doc.get("name"), str) or
            not doc["name"].startswith(SYNTHETIC_PREFIX)):
        raise HostBlock("SYNTHETIC_ROOT_IDENTITY_MISMATCH")


def api_create_folder_once(token: str, parent_id: str, name: str, *,
                           sender=checkpoint.request) -> dict:
    """Issue ONE non-idempotent POST; any API error is an ambiguous outcome."""
    delivery.require_drive_id(parent_id)
    if not isinstance(name, str) or not name or "/" in name:
        raise HostBlock("INVALID_FOLDER_NAME")
    payload = json.dumps({
        "name": name, "mimeType": FOLDER_MIME, "parents": [parent_id]
    }, sort_keys=True).encode("utf-8")
    # Caller must persist and independently read back OUTCOME_UNKNOWN first.
    raw = sender(token, UPLOAD_URL + "?fields=id,name,mimeType,parents",
                 method="POST", body=payload)
    try:
        result = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        raise HostBlock("CREATE_RESPONSE_AMBIGUOUS") from None
    if not isinstance(result, dict) or result.get("mimeType") != FOLDER_MIME or (
            result.get("name") != name or
            result.get("parents") != [parent_id]):
        raise HostBlock("CREATE_RESPONSE_AMBIGUOUS")
    delivery.require_drive_id(result.get("id"))
    return result


def live_root_inventory(root_id: str, token: str, *,
                        fetch_page=scanner.authenticated_get) -> dict:
    scan = scanner.complete_parent_scan(root_id, token, fetch_page=fetch_page)
    return scanner.merge_parent_scan(root_id, "", scan)


def guarded_synthetic_create(plan: dict, journal: Path, project_root: Path,
                             path: str, audit_parent_id: str, audit_file_id: str,
                             token: str, expected_remote_sha: str, *,
                             execute: bool = False,
                             trusted_head=None, anchor_archive: Path | None = None,
                             anchor_key: bytes | None = None,
                             fetch_page=scanner.authenticated_get,
                             sender=checkpoint.request,
                             creator=api_create_folder_once) -> dict:
    """Gate a single external create; return observed result, not optimistic success.

    All write steps run under ONE local host lock that is never force-broken.
    Remote journal is independently read back BEFORE invoking folder create.
    On any ambiguous outcome, there is no second folder POST.
    """
    # Before F8 secure host configuration there must be no live writes.
    # Real CLI intentionally has no trusted CAS adapter and thus cannot POST.
    if execute:
        trust_gate.require_configuration(trusted_head, anchor_archive, anchor_key)
    delivery.check_plan(plan)
    path = delivery.safe_relative(path)
    if "/" in path:
        raise HostBlock("F5_ROOT_CHILD_ONLY")
    root_id = plan["drive_root_id"]
    journal = Path(journal).absolute()
    project_root = Path(project_root).resolve()
    if journal.resolve() == project_root or project_root in journal.resolve().parents:
        raise HostBlock("JOURNAL_MUST_BE_OUTSIDE_PROJECT")
    if journal.is_symlink() or not journal.is_file():
        raise HostBlock("EXISTING_JOURNAL_REQUIRED")
    verify_synthetic_root(root_id, token, sender=sender)
    # Verify the known remote checkpoint before relying on a local copy.
    anchored = checkpoint.remote_matches(audit_file_id, audit_parent_id, token,
                                         plan, expected_remote_sha, sender=sender)
    if execute:
        # Refuse a stale signed chain before reserving any create intent.
        trust_gate.verify_current(
            trusted_head, anchor_archive, anchor_key, project_root,
            plan, audit_parent_id, audit_file_id, token,
            expected_remote_sha, sender=sender)
    local_sha = checkpoint.digest(journal.read_bytes())
    if local_sha != anchored["sha256"]:
        raise HostBlock("LOCAL_AND_REMOTE_JOURNAL_DIFFER")
    # This scan is real only when fetch_page is bound to authenticated_get.
    inventory = live_root_inventory(root_id, token, fetch_page=fetch_page)
    action = delivery.next_action(plan, inventory)
    if action.get("path") != path or action.get("action") != "CHECK_PARENT_FOR_CREATE":
        return {"action": "BLOCKED_OR_NOT_NEEDED", "detail": action["action"],
                "path": path}
    observed = guard.inspect_target(plan, inventory, path, root_id)
    if observed["action"] != "NOT_FOUND_AFTER_COMPLETE_SCAN":
        return observed
    # A prior uncertain creation must not be misreported as a clean precheck
    # merely because a new scan still shows no target folder.
    existing_intent = guard.read_journal(plan, journal).get("operations", {}).get(path)
    if existing_intent:
        return {"action": "BLOCKED_PREVIOUS_CREATE_INTENT_REQUIRES_RECONCILIATION",
                "path": path, "create_permitted": False}
    # Read-only default does not reserve an intent or call the provider.
    if not execute:
        return {"action": "PRECHECK_ONLY_NO_CREATE", "path": path,
                "root_id": root_id, "journal_sha256": local_sha}
    # A left-behind host lock blocks retry and requires manual reconciliation.
    host_lock = journal.with_name(journal.name + ".f5-host.lock")
    fd = None
    try:
        fd = os.open(host_lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        lock_identity = os.fstat(fd)
        own_lock = True
        os.close(fd)
        fd = None
        # Fresh remote observations under the local host lock, to limit races.
        verify_synthetic_root(root_id, token, sender=sender)
        checkpoint.remote_matches(audit_file_id, audit_parent_id, token,
                                  plan, expected_remote_sha, sender=sender)
        previous_head = trust_gate.verify_current(
            trusted_head, anchor_archive, anchor_key, project_root,
            plan, audit_parent_id, audit_file_id, token,
            expected_remote_sha, sender=sender)
        inventory = live_root_inventory(root_id, token, fetch_page=fetch_page)
        prepare = guard.locked_update(
            plan, inventory, journal, path, "prepare", project_root=project_root)
        if prepare["action"] != "CREATE_FOLDER_ONCE":
            return {"action": prepare["action"], "path": path}
        # A side-effect can occur only after this write and downloaded readback.
        persisted = checkpoint.push_once(
            audit_file_id, audit_parent_id, token, plan, journal,
            expected_remote_sha, sender=sender)
        if persisted.get("sha256") != prepare["journal_sha256"]:
            raise HostBlock("REMOTE_INTENT_NOT_VERIFIED")
        # Mandatory F7-F8 gate: pin signed proof in an independent CAS-backed
        # high-watermark and read it back BEFORE the non-idempotent POST.
        committed_head = trust_gate.pin_checkpoint(
            trusted_head, anchor_archive, anchor_key, project_root,
            plan, audit_parent_id, audit_file_id, token,
            previous_head, persisted["sha256"], sender=sender)
        # Host supports exactly one attempt; a timeout with side effect is
        # handled identically to success: re-scan, never blindly repeat POST.
        call_error = False
        try:
            creator(token, prepare["parent_id"], prepare["name"], sender=sender)
        except Exception:
            # An unexpected sender failure can occur AFTER Drive performed
            # the POST. Never issue another POST; reconcile by fresh GET.
            call_error = True
        # A foreign process must not replace our local lock while the remote
        # intent is unresolved. Local lock is secondary to external F8 CAS.
        try:
            current_lock = os.stat(host_lock, follow_symlinks=False)
        except OSError:
            raise HostBlock("F5_HOST_LOCK_OWNERSHIP_LOST") from None
        if (not stat.S_ISREG(current_lock.st_mode) or
                current_lock.st_dev != lock_identity.st_dev or
                current_lock.st_ino != lock_identity.st_ino):
            raise HostBlock("F5_HOST_LOCK_OWNERSHIP_LOST")
        try:
            after_inv = live_root_inventory(root_id, token, fetch_page=fetch_page)
            resolution = guard.locked_update(
                plan, after_inv, journal, path, "resolve", project_root=project_root)
        except Exception:
            # A failed post-create read is ambiguous, even for unexpected
            # transport/library exceptions. Durable intent remains pending.
            raise HostBlock("POST_CREATE_RECONCILIATION_BLOCKED") from None
        if resolution["action"] != "RESOLVED_EXISTING_REMOTE_FOLDER":
            return {"action": resolution["action"], "path": path,
                    "remote_intent_sha256": persisted["sha256"],
                    "create_return_was_ambiguous": call_error}
        # The new resolved journal must also be durable before claiming done.
        final = checkpoint.push_once(
            audit_file_id, audit_parent_id, token, plan, journal,
            persisted["sha256"], sender=sender)
        if final.get("sha256") != resolution["journal_sha256"]:
            raise HostBlock("RESOLVED_JOURNAL_NOT_DURABLE")
        # No claim of resolution until the final signed receipt and external
        # CAS reference are both durably verified as the latest state.
        last_head = trust_gate.pin_checkpoint(
            trusted_head, anchor_archive, anchor_key, project_root,
            plan, audit_parent_id, audit_file_id, token,
            committed_head, final["sha256"], sender=sender)
        return {"action": "VERIFIED_SINGLE_SYNTHETIC_CREATE",
                "path": path, "remote_id": resolution["remote_id"],
                "journal_sha256": final["sha256"],
                "receipt_head_sha256": last_head,
                "create_return_was_ambiguous": call_error}
    finally:
        if fd is not None:
            os.close(fd)
        # A crash leaves a lock behind; an ordinary return may remove only
        # this invocation's lock. Never remove an existing owner lock.
        if "own_lock" in locals() and own_lock:
            # Never delete a lock path that has been replaced by another
            # actor. The independent CAS remains authoritative cross-host.
            try:
                current = os.stat(host_lock, follow_symlinks=False)
                if (stat.S_ISREG(current.st_mode) and
                        current.st_dev == lock_identity.st_dev and
                        current.st_ino == lock_identity.st_ino):
                    host_lock.unlink()
            except FileNotFoundError:
                pass


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--journal", type=Path, required=True)
    p.add_argument("--project-root", type=Path, required=True)
    p.add_argument("--path", required=True)
    p.add_argument("--audit-parent-id", required=True)
    p.add_argument("--audit-file-id", required=True)
    p.add_argument("--expected-remote-sha256", required=True)
    p.add_argument("--execute-synthetic-create", action="store_true")
    args = p.parse_args()
    try:
        plan = delivery.load_json(args.plan)
        token = os.environ.get("MEU_ARTIGO_DRIVE_ACCESS_TOKEN", "")
        # There is intentionally NO CLI adapter for independent durable CAS.
        # Even --execute-synthetic-create MUST block instead of running on
        # a convenient same-process/local-file mock of trusted state.
        result = guarded_synthetic_create(
            plan, args.journal, args.project_root, args.path,
            args.audit_parent_id, args.audit_file_id, token,
            args.expected_remote_sha256,
            execute=args.execute_synthetic_create)
        print(json.dumps(result, sort_keys=True))
        return 0 if result["action"] in (
            "PRECHECK_ONLY_NO_CREATE", "VERIFIED_SINGLE_SYNTHETIC_CREATE") else 2
    except (OSError, ValueError, TypeError, KeyError):
        # The CLI deliberately exposes no token or provider response content.
        print(json.dumps({"action": "BLOCKED", "reason": "F5_OPERATOR_BLOCKED"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
