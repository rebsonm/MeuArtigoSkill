#!/usr/bin/env python3
"""Read-only verification of ChatGPT connected Drive *folder-only* search pages.

This checks host-supplied metadata; it does not call/authenticate Google Drive.
The connected search supports provider-owned pagination when item_type=folder,
but this excludes files, so absence cannot authorize create_folder. It can
identify candidate EXISTING folders for separate metadata checks, never create.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import drive_delivery as delivery

SCHEMA = "MEU_ARTIGO_DRIVE_CONNECTED_FOLDER_SEARCH_V1"
FOLDER_MIME = "application/vnd.google-apps.folder"
MAX_PAGES = 200
MAX_CANDIDATES = 200000


def verify_folder_pages(data: dict, path: str) -> dict:
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise ValueError("CONNECTED_FOLDER_RECEIPT_SCHEMA_INVALID")
    parent = delivery.require_drive_id(data.get("parent_id"))
    target = delivery.safe_relative(path)
    if "/" in target:
        raise ValueError("CONNECTED_FOLDER_SEARCH_EXPECTS_CHILD_NAME")
    pages = data.get("pages")
    if not isinstance(pages, list) or not pages or len(pages) > MAX_PAGES:
        raise ValueError("CONNECTED_FOLDER_PAGINATION_REQUIRED")
    expected_cursor, observed_ids, matched = None, set(), []
    seen_page_tokens = set()
    for n, page in enumerate(pages):
        if not isinstance(page, dict):
            raise ValueError("CONNECTED_FOLDER_PAGE_INVALID")
        request, response = page.get("request"), page.get("response")
        if not isinstance(request, dict) or not isinstance(response, dict):
            raise ValueError("CONNECTED_FOLDER_PAGE_INVALID")
        if (request.get("parent_id") != parent or
                request.get("item_type") != "folder" or
                "page_token" not in request or
                request["page_token"] != expected_cursor):
            raise ValueError("CONNECTED_FOLDER_PAGE_SCOPE_OR_CURSOR_MISMATCH")
        q = request.get("special_filter_query_str")
        if q != f"'{parent}' in parents and trashed = false":
            raise ValueError("CONNECTED_FOLDER_PARENT_QUERY_MISMATCH")
        # A keyword query or viewed-only switch could hide other folders.
        # A folder-only page is incomplete if any additional filtering is set.
        if request.get("query") not in (None, "") or request.get("require_viewed_by_user") is True:
            raise ValueError("CONNECTED_FOLDER_HIDDEN_FILTERS_FORBIDDEN")
        if request.get("best_effort_fetch") is True:
            raise ValueError("CONNECTED_FOLDER_CONTENT_FETCH_UNNECESSARY")
        result = response.get("results")
        if not isinstance(result, list) or "next_page_token" not in response:
            raise ValueError("CONNECTED_FOLDER_RESPONSE_INCOMPLETE")
        for child in result:
            if not isinstance(child, dict):
                raise ValueError("CONNECTED_FOLDER_ITEM_INVALID")
            rid = delivery.require_drive_id(child.get("id"))
            name = child.get("title")
            mime = child.get("mime_type")
            parent_ids = child.get("parent_ids")
            if (not isinstance(name, str) or not name or "/" in name or
                    mime != FOLDER_MIME or parent_ids != [parent] or
                    rid in observed_ids):
                raise ValueError("CONNECTED_FOLDER_ID_OR_PARENT_CONFLICT")
            observed_ids.add(rid)
            if len(observed_ids) > MAX_CANDIDATES:
                raise ValueError("CONNECTED_FOLDER_RESULT_LIMIT")
            if name == target:
                matched.append({"id": rid, "name": name, "parent_id": parent})
        next_token = response["next_page_token"]
        if next_token is not None and (
                not isinstance(next_token, str) or not next_token or
                next_token in seen_page_tokens):
            raise ValueError("CONNECTED_FOLDER_CURSOR_REPLAY")
        if next_token is None and n != len(pages)-1:
            raise ValueError("CONNECTED_FOLDER_PREMATURE_TERMINAL_PAGE")
        if next_token is not None:
            seen_page_tokens.add(next_token)
        expected_cursor = next_token
    if expected_cursor is not None:
        raise ValueError("CONNECTED_FOLDER_PAGINATION_NOT_EXHAUSTED")
    if len(matched) > 1:
        return {"action": "BLOCKED_DUPLICATE_EXISTING_FOLDERS",
                "target": target, "matched_ids": [x["id"] for x in matched],
                "create_permitted": False}
    if len(matched) == 1:
        return {"action": "EXISTING_FOLDER_CANDIDATE_METADATA_READ_REQUIRED",
                "target": target, "remote_id": matched[0]["id"],
                "parent_id": parent, "create_permitted": False,
                "note": "Folder-only paginated scan; other MIME types not covered."}
    return {"action": "BLOCKED_ABSENT_IN_FOLDER_ONLY_SCAN",
            "target": target, "parent_id": parent,
            "create_permitted": False,
            "reason": "CANNOT_PROVE_NONFOLDER_TYPE_CONFLICT_ABSENT"}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--receipt", type=Path, required=True)
    p.add_argument("--folder-name", required=True)
    args = p.parse_args()
    try:
        result = verify_folder_pages(
            delivery.load_json(args.receipt), args.folder_name)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["action"] == (
            "EXISTING_FOLDER_CANDIDATE_METADATA_READ_REQUIRED") else 2
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        print(json.dumps({"action": "BLOCKED", "reason": "CONNECTED_FOLDER_RECEIPT_INVALID"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
