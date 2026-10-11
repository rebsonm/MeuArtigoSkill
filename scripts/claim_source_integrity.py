"""Cross-check frozen [L] citations against the exact source-verification report.

This reconciles literal-locator assertions only. It never claims a quoted
passage semantically supports a claim, authenticates a reviewer, or validates
scientific novelty. Reuses the existing IDs; no new evidence register.
"""
from __future__ import annotations

import csv
from pathlib import Path

from claim_integrity import FINAL, clean, refs, type_of
from source_report_integrity import assess, load_csv, MGMT, SOURCE_REPORT


def audit(root: Path, *, freeze: bool = False) -> dict:
    root = Path(root).resolve()
    claims = load_csv(root / MGMT / "09_Claims_Ledger.csv")
    state = assess(root, require_complete=freeze)
    errors, warnings = [], []
    result = {"errors": errors, "warnings": warnings,
              "checked_literature_claims": 0,
              "source_report_status": state["status"],
              "semantic_support_proven": False}
    if not freeze:
        return result
    if state["status"] not in {"RECORDED_CLEAR", "REVIEWED_LIMITATIONS"}:
        errors.append("verified source report unavailable or incomplete for frozen literature claims")
        return result
    import json
    report = json.loads((root / MGMT / SOURCE_REPORT).read_text(encoding="utf-8"))
    items = {}
    for row in report["checks"]:
        eid = clean(row.get("Evidence_ID"))
        items.setdefault(eid, []).append(row)
    for claim in claims:
        cid = clean(claim.get("Claim_ID"))
        if not cid or type_of(claim.get("Claim_type")) != "L":
            continue
        result["checked_literature_claims"] += 1
        listed = refs(claim.get("Evidence_IDs"))
        if not listed:
            errors.append(f"{cid}: no Evidence_ID recorded for source comparison")
            continue
        linked = []
        for eid in listed:
            candidates = items.get(eid, [])
            if len(candidates) != 1:
                errors.append(f"{cid}: Evidence_ID {eid} absent or ambiguous in source verification")
            else:
                linked.append(candidates[0])
        if len(linked) != len(listed):
            continue
        locators = [str(x.get("locator_status") or "").upper() for x in linked]
        declared = clean(claim.get("Locator_status")).upper()
        if all(x == "MATCHED" for x in locators):
            if declared != "MATCHED":
                errors.append(f"{cid}: final [L] locator status contradicts all confirmed literal passage checks")
        else:
            if declared == "MATCHED":
                errors.append(f"{cid}: final [L] claims MATCHED but source report lacks matched literal passage")
            elif declared not in {"REVIEW_REQUIRED", "UNVERIFIED", *locators}:
                errors.append(f"{cid}: final [L] locator status is not supported by source report")
            if state["status"] != "REVIEWED_LIMITATIONS":
                errors.append(f"{cid}: unmatched literal source requires documented review of limitations")
        if any(str(x.get("result") or "") == "FAIL" for x in linked):
            errors.append(f"{cid}: objective source conflict cannot be waived by a review note")
    return result
