#!/usr/bin/env python3
"""Read-only real Google Drive My Drive -> Meu Artigo -> article resolver.

This optional external-executor helper uses provider GET only. It cannot read
a connected ChatGPT credential and NEVER creates, moves, deletes or uploads.
If a folder is absent it returns a guarded-create request for an authorized
F7/F8 durable-journal executor, NOT a create permission.
"""
from __future__ import annotations

import argparse
import json
import os
from urllib.parse import urlencode

import drive_api_proof as scanner
import drive_delivery as delivery
import drive_journal_checkpoint as checkpoint
import drive_root_anchor as anchor


def read_metadata(file_id: str, token: str, *,
                  sender=checkpoint.request) -> dict:
    if file_id != "root":
        delivery.require_drive_id(file_id)
    params = urlencode({"fields": "id,name,mimeType,parents,trashed",
                        "supportsAllDrives": "true"})
    raw = sender(token,
                 checkpoint.BASE + file_id + "?" + params)
    try:
        data = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        raise anchor.RootAnchorError("ROOT_PROVIDER_METADATA_INVALID") from None
    if not isinstance(data, dict):
        raise anchor.RootAnchorError("ROOT_PROVIDER_METADATA_INVALID")
    return data


def globally_observed_project_matches(name: str, token: str, *,
                                     fetch_page=scanner.authenticated_get) -> list[dict]:
    """Discover mislocated same-name folders, with full pagination or STOP.

    This is a read-only additional warning signal, not absolute assurance that
    every inaccessible or concurrently created folder in Drive was observed.
    """
    if delivery.safe_relative(name) != name or "/" in name:
        raise anchor.RootAnchorError("CANONICAL_PROJECT_NAME_INVALID")
    # Escape backslash and apostrophe within Drive's single-quoted q literal.
    literal = name.replace("\\", "\\\\").replace("'", "\\'")
    q = "name = '" + literal + "' and mimeType = '" + scanner.FOLDER_MIME + "' and trashed = false"
    token_page, observed, cursors, seen = None, [], set(), set()
    for _ in range(scanner.MAX_PAGES):
        params = {
            "q": q, "corpora": "user", "spaces": "drive",
            "supportsAllDrives": "true", "includeItemsFromAllDrives": "true",
            "pageSize": "1000",
            "fields": "kind,nextPageToken,incompleteSearch,files(id,name,mimeType,parents,trashed)",
        }
        if token_page is not None:
            params["pageToken"] = token_page
        data = fetch_page(token, params)
        if (not isinstance(data, dict) or data.get("kind") != "drive#fileList"
                or data.get("incompleteSearch") is True or
                not isinstance(data.get("files"), list)):
            raise anchor.RootAnchorError("PROJECT_GLOBAL_SEARCH_INCOMPLETE")
        for item in data["files"]:
            if not isinstance(item, dict):
                raise anchor.RootAnchorError("PROJECT_GLOBAL_SEARCH_INVALID_ITEM")
            fid = delivery.require_drive_id(item.get("id"))
            if (fid in seen or item.get("mimeType") != scanner.FOLDER_MIME or
                    item.get("name") != name or item.get("trashed") is True or
                    not isinstance(item.get("parents"), list) or
                    len(item["parents"]) != 1):
                raise anchor.RootAnchorError("PROJECT_GLOBAL_SEARCH_INVALID_ITEM")
            parent = delivery.require_drive_id(item["parents"][0])
            seen.add(fid)
            observed.append({"id": fid, "parent_id": parent})
            if len(seen) > scanner.MAX_ITEMS:
                raise anchor.RootAnchorError("PROJECT_GLOBAL_SEARCH_LIMIT")
        next_page = data.get("nextPageToken")
        if next_page is None:
            return observed
        if not isinstance(next_page, str) or not next_page or next_page in cursors:
            raise anchor.RootAnchorError("PROJECT_GLOBAL_SEARCH_CURSOR_INVALID")
        cursors.add(next_page)
        token_page = next_page
    raise anchor.RootAnchorError("PROJECT_GLOBAL_SEARCH_PAGE_LIMIT")


def current_structure(token: str, *, project_name: str | None = None,
                      sender=checkpoint.request,
                      fetch_page=scanner.authenticated_get) -> dict:
    """Provider-backed lookup, all-MIME pages and independent metadata reads."""
    if project_name is not None:
        project_name = delivery.safe_relative(project_name)
        if "/" in project_name:
            raise anchor.RootAnchorError("CANONICAL_PROJECT_NAME_INVALID")
    root = read_metadata("root", token, sender=sender)
    root_id = anchor.check_root(root)
    root_scan = scanner.complete_parent_scan(root_id, token, fetch_page=fetch_page)
    top = anchor.resolve_hierarchy(root, root_scan)
    if top["action"] != "CHECK_EXACT_CHILD_METADATA":
        return top
    container_id = top["remote_id"]
    container_metadata = read_metadata(container_id, token, sender=sender)
    result = anchor.resolve_hierarchy(root, root_scan,
                    container_metadata=container_metadata, project_name=project_name)
    if project_name is None:
        return result
    container_scan = scanner.complete_parent_scan(
        container_id, token, fetch_page=fetch_page)
    result = anchor.resolve_hierarchy(root, root_scan,
               container_metadata=container_metadata,
               container_scan=container_scan, project_name=project_name)
    if result["action"] == "CHECK_PARENT_FOR_GUARDED_CREATE":
        # A past, incorrectly nested article of the same name must be
        # reconciled, not silently duplicated under the correct container.
        candidates = globally_observed_project_matches(
            project_name, token, fetch_page=fetch_page)
        if candidates:
            if any(c["parent_id"] != container_id for c in candidates):
                return {"action": "BLOCKED_EXISTING_PROJECT_OUTSIDE_CONTAINER",
                        "expected_parent_id": container_id,
                        "observed_matching_folders": len(candidates),
                        "create_permitted": False}
            return {"action": "BLOCKED_PARENT_SCAN_GLOBAL_CONFLICT",
                    "expected_parent_id": container_id,
                    "create_permitted": False}
        return result
    if result["action"] != "CHECK_EXACT_CHILD_METADATA":
        return result
    project_metadata = read_metadata(result["remote_id"], token, sender=sender)
    verified = anchor.resolve_hierarchy(root, root_scan,
               container_metadata=container_metadata,
               container_scan=container_scan, project_name=project_name,
               project_metadata=project_metadata)
    # Even if canonical folder exists, detect duplicates in other parents.
    # Global search must be exhaustive or the identity remains uncertain.
    matches = globally_observed_project_matches(
        project_name, token, fetch_page=fetch_page)
    if any(m["parent_id"] != container_id for m in matches):
        return {"action": "BLOCKED_EXISTING_PROJECT_OUTSIDE_CONTAINER",
                "expected_parent_id": container_id,
                "observed_matching_folders": len(matches),
                "create_permitted": False}
    if (len(matches) != 1 or matches[0]["id"] != verified["project_id"]
            or matches[0]["parent_id"] != container_id):
        return {"action": "BLOCKED_PARENT_SCAN_GLOBAL_CONFLICT",
                "expected_parent_id": container_id, "create_permitted": False}
    return verified


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project-name", help="Existing article folder under Meu Artigo")
    args = p.parse_args()
    try:
        token = os.environ.get("MEU_ARTIGO_DRIVE_ACCESS_TOKEN", "")
        result = current_structure(token, project_name=args.project_name)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["action"] in ("CANONICAL_CONTAINER_VERIFIED",
                                         "CANONICAL_PROJECT_VERIFIED") else 2
    except (OSError, ValueError, KeyError, TypeError):
        print(json.dumps({"action": "BLOCKED", "reason": "ROOT_PROVIDER_PREFLIGHT_FAILED"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
