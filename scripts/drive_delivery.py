#!/usr/bin/env python3
"""Plan and check an authorized Google Drive project-tree delivery.

Offline standard-library helper. It NEVER connects to Drive, uploads, writes
canonical project files, or authenticates receipts. The host must perform real
Drive operations and supply fresh, independently observed inventory/readback.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile

SCHEMA = 1
DRIVE_ID = re.compile(r"[A-Za-z0-9_-]{10,128}\Z")
HASH = re.compile(r"[a-f0-9]{64}\Z")
FORBIDDEN = {".git", ".env", ".secrets", "credentials.json", "token.json",
             "__pycache__", ".DS_Store"}
SKIP_DIRS = {"__pycache__"}
SKIP_FILES = {".DS_Store"}


def safe_relative(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ValueError("INVALID_RELATIVE_PATH")
    p = PurePosixPath(value)
    if p.is_absolute() or any(part in (".", "..", "") for part in value.split("/")):
        raise ValueError("INVALID_RELATIVE_PATH")
    return p.as_posix()


def parent_of(value: str) -> str:
    parent = PurePosixPath(value).parent
    return "" if parent == PurePosixPath(".") else parent.as_posix()


def require_drive_id(value: str) -> str:
    if not isinstance(value, str) or not DRIVE_ID.fullmatch(value):
        raise ValueError("INVALID_DRIVE_ID")
    return value


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("INVALID_JSON_OBJECT")
    return data


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def project_config(root: Path) -> dict:
    cfg = load_json(root / "00_Gestao_e_Continuidade" / "PROJECT_CONFIG.json")
    if (cfg.get("storage_mode") != "GOOGLE_DRIVE_STAGING"
            or cfg.get("canonical_storage_backend") != "GOOGLE_DRIVE"):
        raise ValueError("DRIVE_CANONICAL_PROJECT_REQUIRED")
    if cfg.get("fallback_authorized") is True:
        raise ValueError("CONFLICTING_STORAGE_AUTHORITY")
    return cfg


def build_plan(root: Path, drive_root_id: str, *, allow_restricted: bool = False) -> dict:
    root = root.absolute()
    if not root.is_dir() or root.is_symlink():
        raise ValueError("INVALID_OR_LINKED_PROJECT_ROOT")
    drive_root_id = require_drive_id(drive_root_id)
    cfg = project_config(root)
    url = cfg.get("drive_workspace_url") or ""
    if url:
        match = re.search(r"/folders/([A-Za-z0-9_-]+)", url)
        if match and match.group(1) != drive_root_id:
            raise ValueError("DRIVE_ROOT_MISMATCH")
    entries = []
    for parent, dirs, files in os.walk(root, followlinks=False):
        parent_path = Path(parent)
        # No symlinks, hidden credentials, or unrequested metadata leaves scope.
        for name in list(dirs):
            if name in SKIP_DIRS:
                dirs.remove(name)
                continue
            if name in FORBIDDEN or name.startswith(".") or (parent_path / name).is_symlink():
                raise ValueError("UNSAFE_PROJECT_DIRECTORY")
        dirs.sort()
        for name in dirs:
            rel = safe_relative((parent_path / name).relative_to(root).as_posix())
            entries.append({"type": "folder", "path": rel,
                            "parent": parent_of(rel)})
        for name in sorted(files):
            if name in SKIP_FILES:
                continue
            p = parent_path / name
            if name in FORBIDDEN or name.startswith(".") or p.is_symlink() or not p.is_file():
                raise ValueError("UNSAFE_PROJECT_FILE")
            if p.stat().st_nlink > 1:
                raise ValueError("HARD_LINKED_PROJECT_FILE")
            rel = safe_relative(p.relative_to(root).as_posix())
            if (not allow_restricted and
                    (p.suffix.lower() == ".pdf" or "FullText_Corpus" in p.parts)):
                raise ValueError("RESTRICTED_MATERIAL_REQUIRES_RIGHTS_REVIEW")
            entries.append({"type": "file", "path": rel,
                            "parent": parent_of(rel),
                            "sha256": sha256(p), "size": p.stat().st_size})
    entries.sort(key=lambda x: (x["path"].count("/"), x["path"], x["type"]))
    return {"schema": SCHEMA, "kind": "MEU_ARTIGO_DRIVE_DELIVERY_PLAN",
            "drive_root_id": drive_root_id, "project_folder": root.name,
            "restricted_materials_review_declared": allow_restricted, "entries": entries,
            "notice": "Plan only; not evidence of upload or scientific validation."}


def check_plan(plan: dict) -> None:
    if plan.get("schema") != SCHEMA or plan.get("kind") != "MEU_ARTIGO_DRIVE_DELIVERY_PLAN":
        raise ValueError("INVALID_DELIVERY_PLAN")
    require_drive_id(plan.get("drive_root_id"))
    scope = plan.get("root_scope")
    if scope is not None:
        if not isinstance(scope, dict) or set(scope) != {
                "scheme", "my_drive_root_id", "container_id",
                "project_id", "project_name"}:
            raise ValueError("CANONICAL_ROOT_SCOPE_INVALID")
        if scope["scheme"] != "MY_DRIVE_MEU_ARTIGO_V1":
            raise ValueError("CANONICAL_ROOT_SCOPE_INVALID")
        for key in ("my_drive_root_id", "container_id", "project_id"):
            require_drive_id(scope.get(key))
        if (len({scope["my_drive_root_id"], scope["container_id"],
                 scope["project_id"]}) != 3 or
                scope["project_id"] != plan["drive_root_id"] or
                scope["project_name"] != plan.get("project_folder") or
                not isinstance(scope["project_name"], str) or
                safe_relative(scope["project_name"]) != scope["project_name"] or
                "/" in scope["project_name"] or
                scope["project_name"] == "Meu Artigo"):
            raise ValueError("CANONICAL_ROOT_SCOPE_MISMATCH")
    seen = set()
    folders = {""}
    for e in plan.get("entries", []):
        path = safe_relative(e.get("path"))
        if path in seen:
            raise ValueError("DUPLICATE_PLAN_PATH")
        seen.add(path)
        typ = e.get("type")
        parent = parent_of(path)
        if e.get("parent") != parent or typ not in ("file", "folder"):
            raise ValueError("INVALID_PLAN_ENTRY")
        if typ == "folder":
            folders.add(path)
        elif (not isinstance(e.get("size"), int) or isinstance(e["size"], bool)
              or e["size"] < 0 or not isinstance(e.get("sha256"), str)
              or not HASH.fullmatch(e["sha256"])):
            raise ValueError("INVALID_PLAN_HASH")
    if any(e["parent"] not in folders for e in plan["entries"]):
        raise ValueError("MISSING_PLAN_PARENT")


def check_inventory(plan: dict, inventory: dict, *, allow_fixture: bool = False) -> dict:
    if inventory.get("schema") != SCHEMA or inventory.get("drive_root_id") != plan["drive_root_id"]:
        raise ValueError("INVENTORY_ROOT_OR_SCHEMA_MISMATCH")
    origin = inventory.get("observed_via")
    if origin not in (("LIVE_DRIVE", "FIXTURE") if allow_fixture else ("LIVE_DRIVE",)):
        raise ValueError("LIVE_DRIVE_INVENTORY_REQUIRED")
    index = {}
    for e in inventory.get("entries", []):
        path = safe_relative(e.get("path"))
        if e.get("type") not in ("file", "folder"):
            raise ValueError("INVALID_REMOTE_TYPE")
        require_drive_id(e.get("id"))
        require_drive_id(e.get("parent_id"))
        if "sha256" in e and (not isinstance(e["sha256"], str)
                              or not HASH.fullmatch(e["sha256"])):
            raise ValueError("INVALID_REMOTE_HASH")
        if "size" in e and (not isinstance(e["size"], int)
                            or isinstance(e["size"], bool) or e["size"] < 0):
            raise ValueError("INVALID_REMOTE_SIZE")
        index.setdefault(path, []).append(e)
    return index


def reconcile(plan: dict, inventory: dict, *, allow_fixture: bool = False) -> dict:
    check_plan(plan)
    remote = check_inventory(plan, inventory, allow_fixture=allow_fixture)
    expected = {e["path"] for e in plan["entries"]}
    parent_ids = {"": plan["drive_root_id"]}
    statuses = []
    for entry in sorted(plan["entries"], key=lambda e:
                        (e["path"].count("/"), e["type"] != "folder", e["path"])):
        path = entry["path"]
        copies = remote.get(path, [])
        parent_id = parent_ids.get(entry["parent"])
        if len(copies) > 1:
            status = "DUPLICATE_REMOTE_PATH"
        elif not copies:
            status = "MISSING" if parent_id else "PARENT_UNVERIFIED"
        else:
            actual = copies[0]
            if actual["type"] != entry["type"]:
                status = "TYPE_CONFLICT"
            elif not parent_id or actual["parent_id"] != parent_id:
                status = "PARENT_CONFLICT"
            elif entry["type"] == "folder":
                status = "VERIFIED"
                parent_ids[path] = actual["id"]
            elif "size" in actual and actual["size"] != entry["size"]:
                status = "SIZE_CONFLICT"
            elif "sha256" not in actual:
                status = "READBACK_REQUIRED"
            elif actual["sha256"] != entry["sha256"]:
                status = "CONTENT_CONFLICT"
            else:
                status = "VERIFIED"
        statuses.append({"path": path, "type": entry["type"], "status": status,
                         "remote_id": copies[0]["id"] if len(copies) == 1 else None,
                         "parent_id": parent_id})
    other = sorted(set(remote) - expected)
    all_ok = all(s["status"] == "VERIFIED" for s in statuses)
    return {"schema": SCHEMA, "drive_root_id": plan["drive_root_id"],
            "complete": all_ok, "status": "COMPLETE_WITH_REPORTED_READBACK"
            if all_ok else "INCOMPLETE", "verified": sum(s["status"] == "VERIFIED" for s in statuses),
            "total": len(statuses), "unexpected_remote_paths": other,
            "entries": statuses,
            "notice": "Inventory is provided by the host; this script cannot authenticate external tool actions."}


def next_action(plan: dict, inventory: dict, *, allow_fixture: bool = False) -> dict:
    report = reconcile(plan, inventory, allow_fixture=allow_fixture)
    by_path = {e["path"]: e for e in plan["entries"]}
    unsafe = {"DUPLICATE_REMOTE_PATH", "TYPE_CONFLICT", "PARENT_CONFLICT",
              "SIZE_CONFLICT", "CONTENT_CONFLICT"}
    for row in report["entries"]:
        if row["status"] in unsafe:
            return {"action": "BLOCKED_CONFLICT", "path": row["path"],
                    "reason": row["status"], "no_overwrite": True}
    for row in report["entries"]:
        typ = row["type"]
        if row["status"] == "MISSING":
            entry = by_path[row["path"]]
            if typ == "folder":
                return {"action": "CHECK_PARENT_FOR_CREATE", "path": row["path"],
                        "parent_id": row["parent_id"],
                        "required_guard": "scripts/drive_create_guard.py prepare"}
            return {"action": "UPLOAD_FILE", "path": row["path"],
                    "parent_id": row["parent_id"],
                    "sha256": entry["sha256"], "size": entry["size"],
                    "no_overwrite": True}
        if row["status"] == "READBACK_REQUIRED":
            return {"action": "READ_BACK_FILE", "path": row["path"],
                    "remote_id": row["remote_id"]}
    if report["complete"]:
        return {"action": "DONE", "status": report["status"],
                "verified": report["verified"], "total": report["total"]}
    return {"action": "BLOCKED", "reason": "PARENT_UNVERIFIED_OR_MISSING_INVENTORY"}


def write_json(destination: Path, payload: dict, *, root: Path | None = None) -> None:
    if root is not None and (destination.resolve() == root.resolve()
                             or root.resolve() in destination.resolve().parents):
        raise ValueError("REPORT_MUST_REMAIN_OUTSIDE_PROJECT_ROOT")
    destination.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=destination.parent,
                                         prefix=".drive-delivery-", delete=False) as stream:
            temp = Path(stream.name)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, destination)
    finally:
        if temp is not None and temp.exists():
            temp.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    make = sub.add_parser("plan", help="Hash local project tree; no Drive operation")
    make.add_argument("--project-root", type=Path, required=True)
    make.add_argument("--drive-root-id", required=True)
    make.add_argument("--output", type=Path, required=True)
    make.add_argument("--allow-restricted-materials", action="store_true")
    for name in ("next", "verify"):
        p = sub.add_parser(name, help="Interpret actual host-provided Drive inventory")
        p.add_argument("--plan", type=Path, required=True)
        p.add_argument("--inventory", type=Path, required=True)
        p.add_argument("--allow-fixture", action="store_true",
                       help="ONLY for synthetic offline tests; never for real completion")
        p.add_argument("--output", type=Path)
    a = parser.parse_args()
    try:
        if a.command == "plan":
            result = build_plan(a.project_root, a.drive_root_id,
                                allow_restricted=a.allow_restricted_materials)
            write_json(a.output, result, root=a.project_root)
            print(json.dumps({"status": "PLAN_READY_NOT_UPLOADED",
                              "files": sum(e["type"] == "file" for e in result["entries"]),
                              "folders": sum(e["type"] == "folder" for e in result["entries"]),
                              "plan_path": str(a.output)}, ensure_ascii=False))
            return 0
        plan, inventory = load_json(a.plan), load_json(a.inventory)
        result = (next_action(plan, inventory, allow_fixture=a.allow_fixture)
                  if a.command == "next"
                  else reconcile(plan, inventory, allow_fixture=a.allow_fixture))
        if a.output:
            write_json(a.output, result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        if (a.command == "verify" and not result["complete"]) or result.get("action", "").startswith("BLOCKED"):
            return 2
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False),
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
