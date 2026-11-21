#!/usr/bin/env python3
"""Read-only audit of historical third-party PDF exposure in a full Git clone.

This source-only tool never downloads, reads or reproduces a third-party PDF.
It cannot establish legal compliance or exhaust remote caches and forks.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
INCIDENTS = Path("knowledge/methodology/intake/rights-history-incidents.json")
HEX40 = re.compile(r"[a-f0-9]{40}\Z")
SAFE_PATH = re.compile(r"knowledge/methodology/pdfs/[a-z0-9][a-z0-9_-]*\.pdf\Z")


def _git(root: Path, *arguments: str, allow_missing: bool = False) -> str | None:
    try:
        process = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=False, capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError("GIT_HISTORY_UNAVAILABLE") from exc
    if process.returncode != 0:
        if allow_missing:
            return None
        raise ValueError("GIT_HISTORY_COMMAND_FAILED")
    return process.stdout.strip()


def load_manifest(root: Path) -> dict:
    data = json.loads((root / INCIDENTS).read_text(encoding="utf-8"))
    if (data.get("schema") != "MEU_ARTIGO_RIGHTS_HISTORY_INCIDENTS_V1"
            or not isinstance(data.get("incidents"), list)
            or len(data["incidents"]) < 1):
        raise ValueError("RIGHTS_INCIDENT_MANIFEST_INVALID")
    for item in data["incidents"]:
        if not isinstance(item, dict) or not SAFE_PATH.fullmatch(str(item.get("path", ""))):
            raise ValueError("RIGHTS_INCIDENT_PATH_UNSAFE")
        for field in ("last_known_containing_commit", "deletion_commit", "historical_git_blob_sha"):
            if not HEX40.fullmatch(str(item.get(field, ""))):
                raise ValueError("RIGHTS_INCIDENT_GIT_ID_INVALID")
        if item.get("rewrite_authorized") is not False and item.get("owner_decision") == "PENDING":
            raise ValueError("UNAUTHORIZED_HISTORY_REWRITE_FLAG")
    return data


def audit(root: Path, data: dict | None = None) -> dict:
    root = Path(root)
    data = data if data is not None else load_manifest(root)
    if _git(root, "rev-parse", "--is-shallow-repository") != "false":
        raise ValueError("FULL_GIT_HISTORY_REQUIRED")
    records = []
    for item in data["incidents"]:
        path = item["path"]
        previous = item["last_known_containing_commit"]
        known_blob = item["historical_git_blob_sha"]
        blob_present = _git(root, "cat-file", "-e", known_blob + "^{blob}",
                            allow_missing=True) is not None
        parent_contains = _git(root, "cat-file", "-e", previous + ":" + path,
                               allow_missing=True) is not None
        current_tree_contains = bool(_git(root, "ls-tree", "-r", "--name-only",
                                          "HEAD", "--", path))
        refs = _git(root, "for-each-ref", "--format=%(refname)",
                    "--contains", previous) or ""
        records.append({
            "source_id": item["source_id"],
            "path": path,
            "historic_blob_locally_present": blob_present,
            "last_containing_commit_has_path": parent_contains,
            "current_head_has_path": current_tree_contains,
            "local_refs_containing_historic_commit": sorted(refs.splitlines()) if refs else [],
            "historical_rights_review_status": item["history_review_status"],
            "owner_decision": item["owner_decision"],
        })
    return {
        "schema": "MEU_ARTIGO_RIGHTS_HISTORY_READONLY_AUDIT_V1",
        "source": "local_git_full_clone_not_remote_or_forks",
        "no_pdf_content_accessed": True,
        "remote_caches_pull_refs_and_forks_exhaustively_checked": False,
        "license_compliance_legally_determined": False,
        "release_clearance": data["release_clearance"],
        "records": records,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=str(ROOT), help="Complete local Git checkout")
    parser.add_argument("--require-release-clearance", action="store_true",
                        help="Fail closed while the owner/rights decision remains pending")
    args = parser.parse_args(argv)
    root = Path(args.repo)
    try:
        document = load_manifest(root)
        result = audit(root, document)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    if args.require_release_clearance and document["release_clearance"] != "CLEARED_WITH_RECORDED_REVIEW":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
