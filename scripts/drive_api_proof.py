#!/usr/bin/env python3
"""Read-only authenticated Drive v3 pagination proof (optional external executor).

This does not access ChatGPT's connected Google Drive credentials. Supply a
short-lived authorized access token only in a secure executor's environment.
Never use untrusted AI-generated inventory as provider evidence. No write API.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import drive_delivery as delivery

API = "https://www.googleapis.com/drive/v3/files"
FOLDER_MIME = "application/vnd.google-apps.folder"
MAX_PAGES = 100
MAX_ITEMS = 100000
MAX_RESPONSE_BYTES = 4 * 1024 * 1024


class DriveEvidenceError(ValueError):
    """Sanitized failure; do not expose token, response payload or URL."""


def authenticated_get(token: str, params: dict, *, opener=urlopen) -> dict:
    if not isinstance(token, str) or len(token.strip()) < 10:
        raise DriveEvidenceError("DRIVE_TOKEN_MISSING")
    url = API + "?" + urlencode(params)
    req = Request(url, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
    }, method="GET")
    try:
        with opener(req, timeout=25) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
    except (HTTPError, URLError, OSError, TimeoutError) as exc:
        raise DriveEvidenceError("DRIVE_LIST_REQUEST_FAILED") from None
    if len(raw) > MAX_RESPONSE_BYTES:
        raise DriveEvidenceError("DRIVE_LIST_RESPONSE_OVERSIZED")
    try:
        obj = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        raise DriveEvidenceError("DRIVE_LIST_INVALID_RESPONSE") from None
    if not isinstance(obj, dict) or obj.get("kind") != "drive#fileList":
        raise DriveEvidenceError("DRIVE_LIST_INVALID_RESPONSE")
    if obj.get("incompleteSearch") is True:
        raise DriveEvidenceError("DRIVE_LIST_INCOMPLETE_SEARCH")
    return obj


def complete_parent_scan(parent_id: str, token: str, *, fetch_page=authenticated_get,
                         max_pages: int = MAX_PAGES) -> dict:
    """Collect all pages or fail closed, producing guard-compatible evidence.

    The field 'page_evidence' is built from actual results of 'fetch_page'.
    It cannot independently prove that a remote host did not alter responses.
    """
    delivery.require_drive_id(parent_id)
    if not 1 <= max_pages <= MAX_PAGES:
        raise DriveEvidenceError("INVALID_PAGE_LIMIT")
    children, pages, ids, cursors = [], [], set(), set()
    cursor = None
    for _ in range(max_pages):
        params = {
            "q": "'" + parent_id + "' in parents and trashed = false",
            "corpora": "user",
            "spaces": "drive",
            "supportsAllDrives": "true",
            "includeItemsFromAllDrives": "true",
            "pageSize": "1000",
            "fields": "kind,nextPageToken,incompleteSearch,files(id,name,mimeType,parents,trashed)",
        }
        if cursor is not None:
            params["pageToken"] = cursor
        data = fetch_page(token, params)
        if not isinstance(data, dict) or data.get("kind") != "drive#fileList":
            raise DriveEvidenceError("DRIVE_LIST_INVALID_RESPONSE")
        if data.get("incompleteSearch") is True:
            raise DriveEvidenceError("DRIVE_LIST_INCOMPLETE_SEARCH")
        items = data.get("files")
        if not isinstance(items, list):
            raise DriveEvidenceError("DRIVE_LIST_MISSING_ITEMS")
        page_ids = []
        for entry in items:
            if not isinstance(entry, dict):
                raise DriveEvidenceError("DRIVE_LIST_INVALID_CHILD")
            item_id = delivery.require_drive_id(entry.get("id"))
            name = entry.get("name")
            parents = entry.get("parents")
            mime = entry.get("mimeType")
            if (not isinstance(name, str) or not name or "/" in name or
                    name in (".", "..") or not isinstance(mime, str) or
                    not isinstance(parents, list) or
                    parent_id not in parents or len(parents) != 1 or
                    entry.get("trashed") is True or item_id in ids):
                raise DriveEvidenceError("DRIVE_LIST_INVALID_CHILD_OR_PARENT")
            ids.add(item_id)
            page_ids.append(item_id)
            children.append({"id": item_id, "name": name,
                             "type": "folder" if mime == FOLDER_MIME else "file"})
        if len(children) > MAX_ITEMS:
            raise DriveEvidenceError("DRIVE_LIST_TOO_MANY_ITEMS")
        next_cursor = data.get("nextPageToken")
        if next_cursor is not None and (
                not isinstance(next_cursor, str) or not next_cursor or
                next_cursor in cursors):
            raise DriveEvidenceError("DRIVE_LIST_CURSOR_REPLAY")
        pages.append({
            "source": "GOOGLE_DRIVE_FILES_LIST", "request_page_token": cursor,
            "next_page_token": next_cursor, "item_ids": page_ids,
        })
        if next_cursor is None:
            # This fingerprint is an observation identifier, not an attestation.
            fingerprint = hashlib.sha256(json.dumps(pages, sort_keys=True).encode()).hexdigest()
            return {"parent_id": parent_id, "complete": True,
                    "scan_token": "drive-v3-" + fingerprint[:16] + "-" + secrets.token_hex(8),
                    "children": children, "page_evidence": pages}
        cursors.add(next_cursor)
        cursor = next_cursor
    raise DriveEvidenceError("DRIVE_LIST_PAGE_LIMIT_REACHED")


def merge_parent_scan(drive_root_id: str, parent_path: str, scan: dict,
                      base_inventory: dict | None = None) -> dict:
    """Replace exactly one parent subtree's direct children; keep other rows."""
    delivery.require_drive_id(drive_root_id)
    if parent_path:
        parent_path = delivery.safe_relative(parent_path)
    parent_id = scan["parent_id"]
    if not parent_path:
        if parent_id != drive_root_id:
            raise DriveEvidenceError("DRIVE_ROOT_PARENT_MISMATCH")
    elif base_inventory is None:
        raise DriveEvidenceError("PARENT_PATH_REQUIRES_VERIFIED_BASE_INVENTORY")
    if base_inventory is not None:
        if (base_inventory.get("drive_root_id") != drive_root_id or
                base_inventory.get("observed_via") != "LIVE_DRIVE"):
            raise DriveEvidenceError("INVENTORY_ROOT_OR_ORIGIN_MISMATCH")
        matches = [row for row in base_inventory.get("entries", [])
                   if row.get("path") == parent_path and row.get("type") == "folder"]
        if parent_path and (len(matches) != 1 or matches[0].get("id") != parent_id):
            raise DriveEvidenceError("PARENT_PATH_ID_MISMATCH")
        preserved = [row for row in base_inventory.get("entries", [])
                     if row.get("parent_id") != parent_id]
        scans = [item for item in base_inventory.get("parent_scans", [])
                 if item.get("parent_id") != parent_id]
    else:
        preserved, scans = [], []
    entries = []
    for child in scan["children"]:
        name = child["name"]
        path = (parent_path + "/" + name) if parent_path else name
        entries.append({"path": delivery.safe_relative(path), "type": child["type"],
                        "id": child["id"], "parent_id": parent_id})
    if len({e["path"] for e in entries}) != len(entries):
        # Unlike Drive, the canonical delivery plan cannot uniquely represent
        # duplicate names; refuse rather than collapse the duplicates.
        raise DriveEvidenceError("DRIVE_LIST_DUPLICATE_CHILD_NAMES")
    return {"schema": 1, "drive_root_id": drive_root_id,
            "observed_via": "LIVE_DRIVE", "entries": preserved + entries,
            "parent_scans": scans + [scan]}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--parent-id", required=True)
    p.add_argument("--drive-root-id", required=True)
    p.add_argument("--parent-path", default="")
    p.add_argument("--base-inventory", type=Path)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    try:
        token = os.environ.get("MEU_ARTIGO_DRIVE_ACCESS_TOKEN", "")
        scan = complete_parent_scan(args.parent_id, token)
        previous = (delivery.load_json(args.base_inventory)
                    if args.base_inventory else None)
        payload = merge_parent_scan(args.drive_root_id, args.parent_path, scan, previous)
        delivery.write_json(args.output, payload)
        print(json.dumps({"action": "DRIVE_PARENT_PAGINATION_OBSERVED",
                          "parent_id": args.parent_id, "items": len(scan["children"]),
                          "pages": len(scan["page_evidence"]),
                          "output": str(args.output)}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        # Only constant sanitized errors: never print response bodies or tokens.
        reason = str(exc)
        if not reason.isupper() or " " in reason:
            reason = "DRIVE_SCAN_BLOCKED"
        print(json.dumps({"action": "BLOCKED", "reason": reason}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
