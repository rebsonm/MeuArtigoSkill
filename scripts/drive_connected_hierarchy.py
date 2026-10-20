#!/usr/bin/env python3
"""Read-only Drive connector receipt verifier; never authenticates a provider or writes."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import drive_delivery as delivery
import drive_f6_connected_search as pages

SCHEMA = "MEU_ARTIGO_CONNECTED_CANONICAL_HIERARCHY_V1"
PATTERN = re.compile(r"^ARTIGO_.+_(?:19|20)[0-9]{2}(?:_RECUPERADO)?$")

def metadata(obj: dict, name: str, parent: str | None) -> str:
    if not isinstance(obj, dict):
        raise ValueError("CONNECTED_FOLDER_METADATA_REQUIRED")
    fid = delivery.require_drive_id(obj.get("id"))
    if obj.get("title") != name or obj.get("mime_type") != pages.FOLDER_MIME:
        raise ValueError("CONNECTED_FOLDER_NAME_OR_TYPE_MISMATCH")
    expected = [parent] if parent else None
    if obj.get("parent_ids") != expected:
        raise ValueError("CONNECTED_FOLDER_PARENT_MISMATCH")
    if obj.get("drive_id") is not None:
        raise ValueError("CONNECTED_SHARED_DRIVE_NOT_MY_DRIVE")
    return fid

def verdict(action: str, **extra) -> dict:
    return {"schema": SCHEMA, "action": action,
            "create_permitted": False, "canonical_write_authorized": False,
            "scientific_gate_approved": False,
            "provider_proof_independently_authenticated": False,
            "all_mime_parent_scan_verified": False, **extra}

def inspect(data: dict) -> dict:
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise ValueError("CONNECTED_HIERARCHY_SCHEMA_INVALID")
    if data.get("root_requested_alias") != "root":
        raise ValueError("CONNECTED_ROOT_ALIAS_NOT_OBSERVED")
    root = data.get("root_metadata")
    if not isinstance(root, dict) or root.get("title") not in ("Meu Drive", "My Drive"):
        raise ValueError("CONNECTED_ROOT_METADATA_INVALID")
    rid = metadata(root, root["title"], None)
    folder_receipt = data.get("container_pages")
    first = pages.verify_folder_pages(folder_receipt, "Meu Artigo")
    if folder_receipt["parent_id"] != rid:
        raise ValueError("CONNECTED_ROOT_SCAN_PARENT_MISMATCH")
    if first["action"] != "EXISTING_FOLDER_CANDIDATE_METADATA_READ_REQUIRED":
        return verdict(first["action"], level="MY_DRIVE")
    if data.get("container_metadata") is None:
        return verdict("CHECK_EXACT_CONTAINER_METADATA")
    cid = metadata(data["container_metadata"], "Meu Artigo", rid)
    if cid == rid or cid != first["remote_id"]:
        raise ValueError("CONNECTED_CONTAINER_CANDIDATE_ID_MISMATCH")
    name = data.get("project_name")
    if name is None:
        return verdict("CONNECTED_CANONICAL_CONTAINER_RECONCILED",
                       observed_root_id=rid, observed_container_id=cid)
    if not isinstance(name, str) or not PATTERN.fullmatch(name) or delivery.safe_relative(name) != name:
        raise ValueError("CONNECTED_PROJECT_NAME_INVALID")
    project_receipt = data.get("project_pages")
    second = pages.verify_folder_pages(project_receipt, name)
    if project_receipt["parent_id"] != cid:
        raise ValueError("CONNECTED_PROJECT_SCAN_PARENT_MISMATCH")
    if second["action"] != "EXISTING_FOLDER_CANDIDATE_METADATA_READ_REQUIRED":
        return verdict(second["action"], level="MEU_ARTIGO")
    if data.get("project_metadata") is None:
        return verdict("CHECK_EXACT_PROJECT_METADATA")
    pid = metadata(data["project_metadata"], name, cid)
    if pid in (rid, cid) or pid != second["remote_id"]:
        raise ValueError("CONNECTED_PROJECT_CANDIDATE_ID_MISMATCH")
    return verdict("CONNECTED_CANONICAL_PROJECT_RECONCILED",
                   observed_root_id=rid, observed_container_id=cid,
                   observed_project_id=pid, project_name=name)

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--receipt", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        path = args.receipt
        if path.is_symlink() or path.stat().st_size > 512_000:
            raise ValueError("CONNECTED_RECEIPT_UNSAFE")
        result = inspect(json.loads(path.read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["action"] in ("CONNECTED_CANONICAL_CONTAINER_RECONCILED",
                                         "CONNECTED_CANONICAL_PROJECT_RECONCILED") else 2
    except (OSError, ValueError, TypeError, KeyError):
        print(json.dumps(verdict("BLOCKED_INVALID_CONNECTED_EVIDENCE")))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
