#!/usr/bin/env python3
"""Read-only control of the source archive versus public methodology products.

This inventory progress report does not read private PDFs, infer copyright,
validate bibliography, approve editorial cards or alter any project.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "knowledge" / "methodology"
SOURCE_PARTS = "drive-source-candidates-part-*.json"


def audit(root: Path = ROOT) -> dict:
    base = Path(root) / "knowledge" / "methodology"
    parts = sorted((base / "inventory").glob(SOURCE_PARTS))
    if len(parts) != 5:
        raise ValueError("SOURCE_ARCHIVE_INVENTORY_INCOMPLETE")
    source_filenames = []
    categories = 0
    for part in parts:
        batch = json.loads(part.read_text(encoding="utf-8"))
        if batch.get("rights_status") != "NOT_REVIEWED":
            raise ValueError("SOURCE_RIGHTS_CLASSIFICATION_CHANGED")
        for folder in batch.get("folders", []):
            categories += 1
            for item in folder.get("entries", []):
                if item.get("kind") == "PDF":
                    if not isinstance(item.get("filename"), str):
                        raise ValueError("INVALID_SOURCE_FILENAME")
                    source_filenames.append(item["filename"])
    c = json.loads((base / "catalog.json").read_text(encoding="utf-8"))
    p = json.loads((base / "pdf_catalog.json").read_text(encoding="utf-8"))
    if c.get("contains_third_party_full_text") is not False:
        raise ValueError("THIRD_PARTY_TEXT_PRESENT_IN_CARDS_CATALOG")
    if p.get("installer_includes_pdfs") is not False:
        raise ValueError("PUBLIC_PDF_BUNDLE_BOUNDARY_CHANGED")
    card_states = {}
    for item in c.get("documents", []):
        state = item.get("editorial_status", "NOT_INDEPENDENTLY_REVIEWED")
        card_states[state] = card_states.get(state, 0) + 1
    public = p.get("documents", [])
    if any(item.get("rights") != "PUBLIC_REDISTRIBUTION_REVIEWED"
           for item in public):
        raise ValueError("PUBLIC_PDF_WITH_UNREVIEWED_RIGHTS")
    return {
        "schema": "MEU_ARTIGO_METHOD_SOURCE_CURATION_PROGRESS_V1",
        "metadata_only_source_archive": True,
        "archive_folders_including_nested": categories,
        "archive_pdf_records": len(source_filenames),
        "archive_distinct_filenames": len(set(source_filenames)),
        "archive_rights_status": "NOT_REVIEWED_AS_A_GROUP",
        "public_editorial_cards": len(c.get("documents", [])),
        "card_editorial_states": card_states,
        "published_source_pdf_records_on_draft_branch": len(public),
        "original_pdf_bytes_in_installer": False,
        "source_to_card_exact_coverage_verified": False,
        "private_pdf_full_text_inspected": False,
        "legal_and_scientific_review_completed": False,
        "note": (
            "Archive and public sources may overlap. Never subtract public PDFs "
            "from archive file counts without exact source identity reconciliation. "
            "Filename metadata does not prove a full-text reading or rights clearance."
        ),
    }


def main() -> int:
    try:
        result = audit()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "BLOCKED", "kind": type(exc).__name__}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
