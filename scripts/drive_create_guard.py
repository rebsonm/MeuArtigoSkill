#!/usr/bin/env python3
"""Fail-closed guard for non-idempotent, host-executed Drive folder creation.

This tool NEVER calls Google Drive. It journals an intent BEFORE the host
issues create_folder and blocks repeated creates after ambiguous outcomes.
Host-provided scans are not independently authenticated by this script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

import drive_delivery as delivery

SCHEMA = "MEU_ARTIGO_DRIVE_CREATE_GUARD_V1"


def plan_hash(plan: dict) -> str:
    delivery.check_plan(plan)
    return hashlib.sha256(json.dumps(plan, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()


def direct_scan(plan: dict, inventory: dict, parent_id: str) -> dict:
    """Require complete direct-child listing reconciled to inventory rows."""
    delivery.check_inventory(plan, inventory)
    delivery.require_drive_id(parent_id)
    scans = inventory.get("parent_scans")
    if not isinstance(scans, list):
        raise ValueError("PARENT_COMPLETE_SCAN_REQUIRED")
    selected = [x for x in scans if isinstance(x, dict) and x.get("parent_id") == parent_id]
    if len(selected) != 1:
        raise ValueError("PARENT_COMPLETE_SCAN_REQUIRED")
    scan = selected[0]
    token = scan.get("scan_token")
    if scan.get("complete") is not True or not isinstance(token, str) or len(token) < 8:
        raise ValueError("PARENT_COMPLETE_SCAN_REQUIRED")
    children = scan.get("children")
    if not isinstance(children, list):
        raise ValueError("PARENT_SCAN_CHILDREN_REQUIRED")
    seen_ids, children_by_id = set(), {}
    for child in children:
        if not isinstance(child, dict):
            raise ValueError("INVALID_PARENT_SCAN_CHILD")
        cid = delivery.require_drive_id(child.get("id"))
        name = child.get("name")
        kind = child.get("type")
        if (not isinstance(name, str) or not name or "/" in name or
                name in (".", "..") or kind not in ("folder", "file") or cid in seen_ids):
            raise ValueError("INVALID_PARENT_SCAN_CHILD")
        seen_ids.add(cid)
        children_by_id[cid] = (name, kind)
    actual = [e for e in inventory["entries"] if e["parent_id"] == parent_id]
    if len(actual) != len(children_by_id):
        raise ValueError("PARENT_SCAN_INVENTORY_MISMATCH")
    for e in actual:
        if children_by_id.get(e["id"]) != (e["path"].split("/")[-1], e["type"]):
            raise ValueError("PARENT_SCAN_INVENTORY_MISMATCH")
    return scan


def inspect_target(plan: dict, inventory: dict, path: str, parent_id: str) -> dict:
    scan = direct_scan(plan, inventory, parent_id)
    name = path.split("/")[-1]
    matches = [c for c in scan["children"] if c["name"] == name]
    if len(matches) > 1:
        return {"action": "BLOCKED_DUPLICATE_NAME", "path": path, "count": len(matches)}
    if matches and matches[0]["type"] != "folder":
        return {"action": "BLOCKED_TYPE_CONFLICT", "path": path}
    if matches:
        return {"action": "REUSE_EXISTING", "path": path,
                "id": matches[0]["id"], "parent_id": parent_id}
    return {"action": "NOT_FOUND_AFTER_COMPLETE_SCAN", "path": path,
            "parent_id": parent_id, "scan_token": scan["scan_token"]}


def initial_journal(plan: dict) -> dict:
    return {"schema": SCHEMA, "drive_root_id": plan["drive_root_id"],
            "plan_sha256": plan_hash(plan), "operations": {}}


def read_journal(plan: dict, journal_path: Path) -> dict:
    if journal_path.is_symlink():
        raise ValueError("UNSAFE_JOURNAL_LINK")
    if not journal_path.exists():
        return initial_journal(plan)
    data = delivery.load_json(journal_path)
    if (data.get("schema") != SCHEMA or data.get("drive_root_id") != plan["drive_root_id"]
            or data.get("plan_sha256") != plan_hash(plan)
            or not isinstance(data.get("operations"), dict)):
        raise ValueError("JOURNAL_PLAN_OR_ROOT_MISMATCH")
    return data


def create_preflight(plan: dict, inventory: dict, journal: dict, path: str) -> tuple[dict, dict]:
    """Reserve a single create intent before the external call. No blind retries."""
    if journal.get("schema") != SCHEMA or journal.get("plan_sha256") != plan_hash(plan):
        raise ValueError("INVALID_CREATE_JOURNAL")
    path = delivery.safe_relative(path)
    entry = next((e for e in plan["entries"] if e["path"] == path), None)
    if entry is None or entry["type"] != "folder":
        raise ValueError("FOLDER_NOT_IN_PLAN")
    # A guarded operation must be the exact next action from reconciliation.
    action = delivery.next_action(plan, inventory)
    if action.get("path") != path or action.get("action") != "CHECK_PARENT_FOR_CREATE":
        return {"action": "BLOCKED_NOT_NEXT_MISSING_FOLDER", "path": path}, journal
    parent_id = action["parent_id"]
    observed = inspect_target(plan, inventory, path, parent_id)
    if observed["action"] != "NOT_FOUND_AFTER_COMPLETE_SCAN":
        return observed, journal
    previous = journal["operations"].get(path)
    if previous:
        return {"action": "REINSPECT_NO_RETRY", "path": path,
                "reason": "PREVIOUS_CREATE_INTENT", "attempt_id": previous["attempt_id"]}, journal
    if any(op.get("state") == "OUTCOME_UNKNOWN" for op in journal["operations"].values()):
        return {"action": "BLOCKED_OTHER_UNRESOLVED_OPERATION", "path": path}, journal
    attempt_id = hashlib.sha256((plan_hash(plan) + "|" + path + "|" +
                                 parent_id + "|" + observed["scan_token"]).encode()).hexdigest()[:24]
    journal["operations"][path] = {
        "attempt_id": attempt_id, "parent_id": parent_id, "state": "OUTCOME_UNKNOWN",
        "before_scan_token": observed["scan_token"], "observed_remote_id": None
    }
    return {"action": "CREATE_FOLDER_ONCE", "path": path, "parent_id": parent_id,
            "name": path.split("/")[-1], "attempt_id": attempt_id,
            "warning": "Persisted intent; NEVER retry create directly after timeout/error."}, journal


def resolve_create(plan: dict, inventory: dict, journal: dict, path: str) -> tuple[dict, dict]:
    """Reconcile after an uncertain return. No new create action is emitted."""
    if journal.get("schema") != SCHEMA or journal.get("plan_sha256") != plan_hash(plan):
        raise ValueError("INVALID_CREATE_JOURNAL")
    path = delivery.safe_relative(path)
    op = journal["operations"].get(path)
    if not isinstance(op, dict):
        raise ValueError("UNKNOWN_CREATE_INTENT")
    if op["state"] == "RESOLVED":
        return {"action": "ALREADY_RESOLVED", "path": path,
                "remote_id": op["observed_remote_id"]}, journal
    if op["state"] != "OUTCOME_UNKNOWN":
        raise ValueError("INVALID_CREATE_STATE")
    scan = direct_scan(plan, inventory, op["parent_id"])
    if scan["scan_token"] == op["before_scan_token"]:
        return {"action": "REINSPECT_PARENT", "path": path,
                "reason": "STALE_PRE_OPERATION_SCAN"}, journal
    result = inspect_target(plan, inventory, path, op["parent_id"])
    if result["action"] == "REUSE_EXISTING":
        op["state"] = "RESOLVED"
        op["observed_remote_id"] = result["id"]
        op["after_scan_token"] = scan["scan_token"]
        return {"action": "RESOLVED_EXISTING_REMOTE_FOLDER", "path": path,
                "remote_id": result["id"], "parent_id": op["parent_id"]}, journal
    if result["action"] == "NOT_FOUND_AFTER_COMPLETE_SCAN":
        return {"action": "BLOCKED_AMBIGUOUS_OUTCOME", "path": path,
                "reason": "NO_AUTOMATIC_RETRY_AFTER_POSSIBLE_EXTERNAL_SIDE_EFFECT"}, journal
    return result, journal


def locked_update(plan: dict, inventory: dict, journal_path: Path, path: str, command: str) -> dict:
    """Exclusive journal lock prevents simultaneous local agents issuing same create."""
    journal_path = Path(journal_path).absolute()
    if journal_path.is_symlink():
        raise ValueError("UNSAFE_JOURNAL_LINK")
    journal_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = journal_path.with_name(journal_path.name + ".lock")
    fd = None
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(fd)
        fd = None
        data = read_journal(plan, journal_path)
        if command == "prepare":
            result, data = create_preflight(plan, inventory, data, path)
        else:
            result, data = resolve_create(plan, inventory, data, path)
        if result["action"] in ("CREATE_FOLDER_ONCE", "RESOLVED_EXISTING_REMOTE_FOLDER"):
            delivery.write_json(journal_path, data)
        return result
    finally:
        if fd is not None:
            os.close(fd)
        # A failed create of the lock must not remove someone else's lock.
        if lock_path.exists():
            try:
                if fd is None and 'result' in locals():
                    lock_path.unlink()
                elif fd is None and 'data' in locals():
                    lock_path.unlink()
            except OSError:
                pass


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["prepare", "resolve"])
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--inventory", type=Path, required=True)
    p.add_argument("--journal", type=Path, required=True)
    p.add_argument("--path", required=True)
    args = p.parse_args()
    try:
        plan = delivery.load_json(args.plan)
        inventory = delivery.load_json(args.inventory)
        # No fixture bypass on the CLI.
        result = locked_update(plan, inventory, args.journal, args.path, args.command)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["action"] in (
            "CREATE_FOLDER_ONCE", "RESOLVED_EXISTING_REMOTE_FOLDER", "ALREADY_RESOLVED") else 2
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"action": "BLOCKED", "reason": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
