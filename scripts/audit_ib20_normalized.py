#!/usr/bin/env python3
"""Audit 20 independent IB receipts normalized into two public, ID-free parts.

This checks document-identity declarations, NOT scientific validation or PDF rights.
Run: python scripts/audit_ib20_normalized.py
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "knowledge" / "methodology" / "intake"
NORMALIZED = INTAKE / "reconciliation"
CATALOG = ROOT / "knowledge" / "methodology" / "source_registry_catalog.json"
LEDGER_FILES = [INTAKE / f"rights-ledger-part-{i:02d}.json" for i in range(1, 6)]
PART_FILES = [
    NORMALIZED / "IB20-NORMALIZED-01-10.json",
    NORMALIZED / "IB20-NORMALIZED-11-20.json",
]
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_SRC = re.compile(r"^SRC-\d{4}$")
_PRIVATE_URL = re.compile(r"https?://(?:drive|docs)\.google\.com/(?:file|document|spreadsheets)/d/", re.I)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise AssertionError(f"Expected object: {path}")
    return data


def audit(root: Path = ROOT) -> dict:
    intake = root / "knowledge" / "methodology" / "intake"
    norm = intake / "reconciliation"
    catalog = load_json(root / "knowledge" / "methodology" / "source_registry_catalog.json")
    expected = {
        d["source_id"]
        for d in catalog["documents"]
        if d["bibliography_match_status"] == "CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED"
    }
    ledger = {}
    for index in range(1, 6):
        part = load_json(intake / f"rights-ledger-part-{index:02d}.json")
        for doc in part["records"]:
            ident = doc["id"]
            assert ident not in ledger, f"Duplicate ledger ID: {ident}"
            ledger[ident] = doc
    assert len(ledger) == len(catalog["documents"]) == 475

    seen = set()
    cards = []
    count_by_lot = Counter()
    for name in ["IB20-NORMALIZED-01-10.json", "IB20-NORMALIZED-11-20.json"]:
        path = norm / name
        payload = load_json(path)
        assert payload.get("schema") == "MEUARTIGO_IB20_NORMALIZED_PUBLIC_V1", path
        raw = path.read_text(encoding="utf-8")
        assert not _PRIVATE_URL.search(raw), f"Private Drive URL in {path}"
        assert "drive_file_id" not in raw.lower(), f"Private Drive field in {path}"
        records = payload["records"]
        assert payload["total"] == len(records)
        assert payload["verified"] == sum(r["identity_confirmed"] is True for r in records)
        assert payload["blocked"] == sum(r["identity_confirmed"] is False for r in records)
        for rec in records:
            ident = rec["source_id"]
            assert _SRC.fullmatch(ident), f"Bad ID: {ident}"
            assert ident not in seen, f"Duplicate across lots: {ident}"
            seen.add(ident)
            lot = rec["batch_id"]
            assert re.fullmatch(r"IB-\d{2}/20", lot), f"Invalid lot {lot}"
            lot_num = int(lot[3:5])
            assert 1 <= lot_num <= 20
            count_by_lot[lot_num] += 1
            assert isinstance(rec["identity_confirmed"], bool), ident
            assert rec["identity_confirmed"] or bool(rec["blocked_reason"]), ident
            assert _SHA256.fullmatch(rec["card_sha256"]), ident
            assert rec["filename"] == ledger[ident]["filename"], ident
            assert rec["size_bytes"] == ledger[ident]["size_bytes"], ident
            assert rec["card_path"].endswith(f"/src-{ident[-4:]}.md"), ident
            assert rec["scientific_review"] == "PENDING", ident
            assert rec["public_pdf_approved_by_batch"] is False, ident
        cards.extend(records)

    assert seen == expected, (
        f"Missing {sorted(expected - seen)}; unexpected {sorted(seen - expected)}"
    )
    assert count_by_lot == Counter(
        {i: 18 if i <= 3 else 17 for i in range(1, 21)}
    ), count_by_lot
    verified = sum(r["identity_confirmed"] for r in cards)
    blocked = sorted(r["source_id"] for r in cards if not r["identity_confirmed"])
    return {
        "source_records": len(cards),
        "verified_documentary_claims": verified,
        "blocked_identification": len(blocked),
        "blocked_ids": blocked,
        "global_registry_updated": False,
        "rights_or_scientific_review_approved": False,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
