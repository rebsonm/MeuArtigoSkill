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
    if result["action"] != "CHECK_EXACT_CHILD_METADATA":
        return result
    project_metadata = read_metadata(result["remote_id"], token, sender=sender)
    return anchor.resolve_hierarchy(root, root_scan,
               container_metadata=container_metadata,
               container_scan=container_scan, project_name=project_name,
               project_metadata=project_metadata)


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
