#!/usr/bin/env python3
"""Read-only canonical My Drive root and project parent guard.

Required hierarchy:
My Drive (provider-verified root ID) / Meu Artigo / ARTIGO_<title>_<year> /
  the existing per-project folders.

No automatic create/move/delete: a missing folder produces a guarded-create
*request*, not permission to call the provider. The host must complete the
existing durable journal / F7-F8 signed CAS before any external create.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import drive_api_proof as proof
import drive_delivery as delivery

CONTAINER = "Meu Artigo"
SCHEME = "MY_DRIVE_MEU_ARTIGO_V1"
FOLDER_MIME = proof.FOLDER_MIME


class RootAnchorError(ValueError):
    """Safe, fixed diagnostics; no provider token or private content."""


def check_root(root: dict) -> str:
    if not isinstance(root, dict):
        raise RootAnchorError("MY_DRIVE_ROOT_METADATA_REQUIRED")
    root_id = delivery.require_drive_id(root.get("id"))
    if (root.get("mimeType") != FOLDER_MIME or
            root.get("trashed") is True or
            root.get("parents") not in (None, [])):
        raise RootAnchorError("MY_DRIVE_ROOT_IDENTITY_INVALID")
    # The provider response MUST come from files.get(fileId="root").
    # A caller-supplied metadata object is not authenticated by this function.
    return root_id


def check_scan(scan: dict, parent_id: str) -> list[dict]:
    """Verify exact parent and terminal all-types Drive v3 page evidence."""
    delivery.require_drive_id(parent_id)
    if not isinstance(scan, dict) or scan.get("parent_id") != parent_id or scan.get("complete") is not True:
        raise RootAnchorError("CANONICAL_PARENT_SCAN_REQUIRED")
    children, pages = scan.get("children"), scan.get("page_evidence")
    if not isinstance(children, list) or not isinstance(pages, list) or not pages or len(pages) > 100:
        raise RootAnchorError("CANONICAL_PARENT_SCAN_INCOMPLETE")
    seen, items = set(), {}
    for child in children:
        if not isinstance(child, dict):
            raise RootAnchorError("CANONICAL_SCAN_INVALID_CHILD")
        cid = delivery.require_drive_id(child.get("id"))
        name = child.get("name")
        if (cid in seen or not isinstance(name, str) or not name or
                "/" in name or name in (".", "..") or
                child.get("type") not in ("file", "folder")):
            raise RootAnchorError("CANONICAL_SCAN_INVALID_CHILD")
        seen.add(cid)
        items[cid] = child
    cursor, covered, cursors = None, set(), set()
    for i, page in enumerate(pages):
        if (not isinstance(page, dict) or page.get("source") != "GOOGLE_DRIVE_FILES_LIST" or
                "request_page_token" not in page or
                page.get("request_page_token") != cursor or
                "next_page_token" not in page or
                not isinstance(page.get("item_ids"), list)):
            raise RootAnchorError("CANONICAL_PAGINATION_INVALID")
        for item_id in page["item_ids"]:
            delivery.require_drive_id(item_id)
            if item_id in covered:
                raise RootAnchorError("CANONICAL_PAGINATION_DUPLICATE_ID")
            covered.add(item_id)
        next_token = page["next_page_token"]
        if next_token is not None and (not isinstance(next_token, str) or
                                       not next_token or next_token in cursors):
            raise RootAnchorError("CANONICAL_PAGINATION_CURSOR_REPLAY")
        if next_token is None and i != len(pages) - 1:
            raise RootAnchorError("CANONICAL_PAGINATION_INVALID")
        if next_token is not None:
            cursors.add(next_token)
        cursor = next_token
    if cursor is not None or seen != covered:
        raise RootAnchorError("CANONICAL_PAGINATION_INCOMPLETE")
    return children


def verify_folder(metadata: dict, expected_name: str, expected_parent: str,
                  expected_id: str) -> None:
    delivery.require_drive_id(expected_parent)
    delivery.require_drive_id(expected_id)
    if not isinstance(metadata, dict) or (
            metadata.get("id") != expected_id or
            metadata.get("name") != expected_name or
            metadata.get("parents") != [expected_parent] or
            metadata.get("mimeType") != FOLDER_MIME or
            metadata.get("trashed") is True):
        raise RootAnchorError("CANONICAL_FOLDER_PARENT_IDENTITY_MISMATCH")


def resolve_child(scan: dict, parent_id: str, name: str, *,
                  metadata: dict | None = None) -> dict:
    if (not isinstance(name, str) or delivery.safe_relative(name) != name or
            "/" in name or name == CONTAINER and parent_id != scan.get("parent_id")):
        raise RootAnchorError("CANONICAL_CHILD_NAME_INVALID")
    children = check_scan(scan, parent_id)
    matches = [c for c in children if c["name"] == name]
    if len(matches) > 1:
        return {"action": "BLOCKED_DUPLICATE_SAME_NAME", "parent_id": parent_id,
                "folder_name": name, "create_permitted": False, "count": len(matches)}
    if matches and matches[0]["type"] != "folder":
        return {"action": "BLOCKED_NAME_NOT_FOLDER", "parent_id": parent_id,
                "folder_name": name, "create_permitted": False}
    if not matches:
        # A terminal parent scan alone NEVER bypasses F7-F8 journal trust gate.
        return {"action": "CHECK_PARENT_FOR_GUARDED_CREATE", "parent_id": parent_id,
                "folder_name": name, "create_permitted": False,
                "required_guard": "REMOTE_INTENT_F7_F8_CAS"}
    matched_id = matches[0]["id"]
    if metadata is None:
        return {"action": "CHECK_EXACT_CHILD_METADATA", "parent_id": parent_id,
                "remote_id": matched_id, "folder_name": name,
                "create_permitted": False}
    verify_folder(metadata, name, parent_id, matched_id)
    return {"action": "REUSE_EXISTING_EXACT_FOLDER", "parent_id": parent_id,
            "remote_id": matched_id, "folder_name": name, "create_permitted": False}


def resolve_hierarchy(my_drive: dict, root_scan: dict,
                      *, container_metadata: dict | None = None,
                      project_name: str | None = None,
                      container_scan: dict | None = None,
                      project_metadata: dict | None = None) -> dict:
    """Return exactly one next safe action and optional fully checked scope."""
    root_id = check_root(my_drive)
    top = resolve_child(root_scan, root_id, CONTAINER, metadata=container_metadata)
    if top["action"] != "REUSE_EXISTING_EXACT_FOLDER":
        return {"level": "MY_DRIVE", **top}
    container_id = top["remote_id"]
    if project_name is None:
        return {"action": "CANONICAL_CONTAINER_VERIFIED", "level": "MY_DRIVE",
                "my_drive_root_id": root_id, "container_id": container_id,
                "create_permitted": False}
    project_name = delivery.safe_relative(project_name)
    if "/" in project_name or project_name == CONTAINER:
        raise RootAnchorError("CANONICAL_PROJECT_NAME_INVALID")
    if container_scan is None:
        return {"action": "SCAN_CANONICAL_CONTAINER", "level": "MEU_ARTIGO",
                "parent_id": container_id, "create_permitted": False}
    result = resolve_child(container_scan, container_id, project_name,
                           metadata=project_metadata)
    if result["action"] != "REUSE_EXISTING_EXACT_FOLDER":
        return {"level": "MEU_ARTIGO", **result}
    return {"action": "CANONICAL_PROJECT_VERIFIED",
            "scheme": SCHEME, "my_drive_root_id": root_id,
            "container_id": container_id,
            "project_id": result["remote_id"],
            "project_name": project_name, "create_permitted": False}


def attach_scope(plan: dict, hierarchy: dict) -> dict:
    """Bind a staged delivery plan to verified root/container/project IDs."""
    delivery.check_plan(plan)
    if (not isinstance(hierarchy, dict) or
            hierarchy.get("action") != "CANONICAL_PROJECT_VERIFIED" or
            hierarchy.get("scheme") != SCHEME):
        raise RootAnchorError("CANONICAL_PROJECT_NOT_VERIFIED")
    root = delivery.require_drive_id(hierarchy.get("my_drive_root_id"))
    container = delivery.require_drive_id(hierarchy.get("container_id"))
    project = delivery.require_drive_id(hierarchy.get("project_id"))
    if (len({root, container, project}) != 3 or
            plan["drive_root_id"] != project or
            plan["project_folder"] != hierarchy.get("project_name")):
        raise RootAnchorError("CANONICAL_DELIVERY_PLAN_SCOPE_MISMATCH")
    scoped = dict(plan)
    scoped["root_scope"] = {"scheme": SCHEME, "my_drive_root_id": root,
                            "container_id": container, "project_id": project,
                            "project_name": hierarchy["project_name"]}
    delivery.check_plan(scoped)
    return scoped


def require_scope(plan: dict) -> dict:
    """Every *new* real Drive delivery must have a bound canonical scope."""
    delivery.check_plan(plan)
    scope = plan.get("root_scope")
    if not isinstance(scope, dict) or scope.get("scheme") != SCHEME:
        raise RootAnchorError("CANONICAL_ROOT_SCOPE_REQUIRED")
    if (scope.get("project_id") != plan["drive_root_id"] or
            scope.get("project_name") != plan["project_folder"] or
            len({scope.get("my_drive_root_id"), scope.get("container_id"),
                 scope.get("project_id")}) != 3):
        raise RootAnchorError("CANONICAL_ROOT_SCOPE_MISMATCH")
    for name in ("my_drive_root_id", "container_id", "project_id"):
        delivery.require_drive_id(scope.get(name))
    return scope


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root-metadata", type=Path, required=True)
    p.add_argument("--root-scan", type=Path, required=True)
    p.add_argument("--container-metadata", type=Path)
    p.add_argument("--container-scan", type=Path)
    p.add_argument("--project-metadata", type=Path)
    p.add_argument("--project-name")
    p.add_argument("--plan", type=Path)
    p.add_argument("--scoped-plan-output", type=Path,
                   help="Create a new scoped plan outside the scientific project")
    p.add_argument("--project-root", type=Path)
    args = p.parse_args()
    try:
        result = resolve_hierarchy(
            delivery.load_json(args.root_metadata),
            delivery.load_json(args.root_scan),
            container_metadata=(delivery.load_json(args.container_metadata)
                                if args.container_metadata else None),
            container_scan=(delivery.load_json(args.container_scan)
                            if args.container_scan else None),
            project_metadata=(delivery.load_json(args.project_metadata)
                              if args.project_metadata else None),
            project_name=args.project_name)
        if args.scoped_plan_output and not args.plan:
            raise RootAnchorError("SCOPED_PLAN_INPUT_REQUIRED")
        if args.plan:
            if result["action"] != "CANONICAL_PROJECT_VERIFIED":
                raise RootAnchorError("CANONICAL_PROJECT_NOT_VERIFIED")
            planned = attach_scope(delivery.load_json(args.plan), result)
            if args.scoped_plan_output:
                if args.project_root is None:
                    raise RootAnchorError("PROJECT_ROOT_REQUIRED_FOR_SCOPED_PLAN")
                output = args.scoped_plan_output.absolute()
                if (output.is_symlink() or output.exists() or
                        not output.parent.is_dir()):
                    raise RootAnchorError("SCOPED_PLAN_OUTPUT_MUST_BE_NEW")
                delivery.write_json(output, planned, root=args.project_root)
            result = {"action": "CANONICAL_PLAN_SCOPE_VERIFIED",
                      "root_scope": planned["root_scope"],
                      "scoped_plan_written": bool(args.scoped_plan_output),
                      "create_permitted": False}
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["action"] in ("CANONICAL_PROJECT_VERIFIED",
                   "CANONICAL_CONTAINER_VERIFIED",
                   "CANONICAL_PLAN_SCOPE_VERIFIED",
                   "REUSE_EXISTING_EXACT_FOLDER") else 2
    except (OSError, ValueError, KeyError, TypeError):
        print(json.dumps({"action": "BLOCKED", "reason": "CANONICAL_ROOT_GUARD_FAILED"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
