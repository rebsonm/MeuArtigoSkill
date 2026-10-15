#!/usr/bin/env python3
"""REG-018: read-only citation/evidence reconciliation for canonical Meu Artigo CSVs.

Works from recorded bibliographic evidence, [L] claim links and the existing
verified source report. Never infers semantic claim support from source identity.
Does not query the network, mutate canonical registers or invent reviewer data.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

from claim_integrity import clean, refs, type_of
from report_output_guard import write_report
from source_report_integrity import MGMT, SOURCE_REPORT, assess
from verify_sources import doi_of

EVIDENCE = "05_Evidence_Matrix.csv"
CLAIMS = "09_Claims_Ledger.csv"
BLOCKERS = {"MISSING_REFERENCE_ID", "DUPLICATE_REFERENCE_ID",
            "UNKNOWN_REFERENCE", "AMBIGUOUS_REFERENCE", "MISSING_CLAIM_ID",
            "DUPLICATE_CLAIM_ID", "LITERATURE_CLAIM_WITHOUT_REFERENCE",
            "BIBLIOGRAPHIC_IDENTITY_MISSING", "INVALID_DOI",
            "SOURCE_METADATA_MISMATCH", "SOURCE_DOI_NOT_FOUND",
            "SOURCE_LOCATOR_CONFLICT", "UNTRUSTWORTHY_SOURCE_REPORT",
            "SOURCE_REPORT_STALE"}
REVIEW = {"REFERENCE_WITHOUT_DOI", "CITATION_NOT_COMPLETE", "DUPLICATE_DOI",
          "SOURCE_REPORT_MISSING", "SOURCE_NOT_CHECKED", "SOURCE_UNVERIFIED",
          "SOURCE_RETRACTION_ALERT", "SOURCE_CORRECTION_ALERT",
          "SOURCE_UPDATE_ALERT", "SOURCE_PROVIDER_PARTIAL",
          "SOURCE_LOCATOR_PENDING"}

def _table(root: Path, name: str, required: set[str]) -> list[dict]:
    path = root / MGMT / name
    if not path.is_file() or path.is_symlink():
        raise ValueError("Required canonical table unavailable: " + name)
    with path.open(newline="", encoding="utf-8-sig") as inp:
        reader = csv.DictReader(inp)
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("Canonical headers incomplete: " + name)
        data = list(reader)
    if any(None in row for row in data):
        raise ValueError("Malformed canonical CSV input: " + name)
    return data

def _issue(code: str, *, evidence_id: str = "", claim_id: str = "") -> dict:
    return {"code": code, "severity": "BLOCK" if code in BLOCKERS else "REVIEW",
            "evidence_id": evidence_id or None, "claim_id": claim_id or None}

def _trusted_report(root: Path):
    state = assess(root, require_complete=False)
    status = state["status"]
    # A report may legitimately be BLOCKED by source mismatch. Its rows can
    # still support that finding if its manifest and internal logic are sound.
    trusted = status not in {"MISSING", "STALE"} and not state["errors"]
    if not trusted:
        return state, {}
    file = root / MGMT / SOURCE_REPORT
    data = json.loads(file.read_text(encoding="utf-8"))
    index = defaultdict(list)
    for item in data.get("checks", []):
        if isinstance(item, dict):
            index[clean(item.get("Evidence_ID"))].append(item)
    return state, index

def audit(root: Path) -> dict:
    root = Path(root).resolve()
    evidence = _table(root, EVIDENCE, {"Evidence_ID", "Citation", "DOI_or_persistent_ID"})
    claims = _table(root, CLAIMS, {"Claim_ID", "Claim_type", "Evidence_IDs"})
    state, checks = _trusted_report(root)
    items = []
    counts = Counter()
    evidence_ids = Counter(clean(r.get("Evidence_ID")) for r in evidence)
    claim_ids = Counter(clean(r.get("Claim_ID")) for r in claims)
    doi_map = defaultdict(set)
    referenced = set()

    for r in evidence:
        eid = clean(r.get("Evidence_ID"))
        if not eid:
            items.append(_issue("MISSING_REFERENCE_ID"))
            continue
        if evidence_ids[eid] > 1:
            items.append(_issue("DUPLICATE_REFERENCE_ID", evidence_id=eid))
        citation = clean(r.get("Citation"))
        raw_doi = clean(r.get("DOI_or_persistent_ID"))
        doi = doi_of(raw_doi)
        if not citation and not raw_doi:
            items.append(_issue("BIBLIOGRAPHIC_IDENTITY_MISSING", evidence_id=eid))
        elif not citation:
            items.append(_issue("CITATION_NOT_COMPLETE", evidence_id=eid))
        if raw_doi and not doi and (
            raw_doi.lower().startswith(("doi:", "10.", "https://doi.org/", "http://doi.org/"))
        ):
            items.append(_issue("INVALID_DOI", evidence_id=eid))
        elif not doi:
            items.append(_issue("REFERENCE_WITHOUT_DOI", evidence_id=eid))
        else:
            doi_map[doi].add(eid)

        report_rows = checks.get(eid, [])
        if state["status"] == "MISSING":
            items.append(_issue("SOURCE_REPORT_MISSING", evidence_id=eid))
        elif state["status"] == "STALE":
            items.append(_issue("SOURCE_REPORT_STALE", evidence_id=eid))
        elif state["errors"]:
            items.append(_issue("UNTRUSTWORTHY_SOURCE_REPORT", evidence_id=eid))
        elif len(report_rows) != 1:
            items.append(_issue("SOURCE_NOT_CHECKED", evidence_id=eid))
        else:
            source = report_rows[0]
            source_doi = doi_of(source.get("doi") or "")
            if doi and source_doi and doi != source_doi:
                items.append(_issue("SOURCE_METADATA_MISMATCH", evidence_id=eid))
            metadata = source.get("metadata_status")
            if metadata in {"INVALID_DOI", "MISMATCH"}:
                items.append(_issue("SOURCE_METADATA_MISMATCH", evidence_id=eid))
            elif metadata == "NOT_FOUND":
                items.append(_issue("SOURCE_DOI_NOT_FOUND", evidence_id=eid))
            elif metadata != "VERIFIED":
                items.append(_issue("SOURCE_UNVERIFIED", evidence_id=eid))
            if source.get("retraction_alert"):
                items.append(_issue("SOURCE_RETRACTION_ALERT", evidence_id=eid))
            if source.get("correction_alert"):
                items.append(_issue("SOURCE_CORRECTION_ALERT", evidence_id=eid))
            if source.get("update_alert"):
                items.append(_issue("SOURCE_UPDATE_ALERT", evidence_id=eid))
            if source.get("provider_warnings"):
                items.append(_issue("SOURCE_PROVIDER_PARTIAL", evidence_id=eid))
            loc = source.get("locator_status")
            if loc in {"PAGE_MISMATCH", "PASSAGE_NOT_FOUND", "OUTSIDE_WORKSPACE"}:
                items.append(_issue("SOURCE_LOCATOR_CONFLICT", evidence_id=eid))
            elif loc != "MATCHED":
                items.append(_issue("SOURCE_LOCATOR_PENDING", evidence_id=eid))

    for doi, linked in doi_map.items():
        if len(linked) > 1:
            for eid in sorted(linked):
                items.append(_issue("DUPLICATE_DOI", evidence_id=eid))

    for r in claims:
        cid = clean(r.get("Claim_ID"))
        if not cid:
            items.append(_issue("MISSING_CLAIM_ID"))
            continue
        if claim_ids[cid] > 1:
            items.append(_issue("DUPLICATE_CLAIM_ID", claim_id=cid))
        linked = refs(r.get("Evidence_IDs"))
        if type_of(r.get("Claim_type")) == "L" and not linked:
            items.append(_issue("LITERATURE_CLAIM_WITHOUT_REFERENCE", claim_id=cid))
        for eid in set(linked):
            referenced.add(eid)
            if evidence_ids[eid] == 0:
                items.append(_issue("UNKNOWN_REFERENCE", evidence_id=eid, claim_id=cid))
            elif evidence_ids[eid] > 1:
                items.append(_issue("AMBIGUOUS_REFERENCE", evidence_id=eid, claim_id=cid))

    for item in items:
        counts[item["severity"]] += 1
    return {
        "schema_version": 1, "audit": "REG-018_CANONICAL_CITATION_RECONCILIATION",
        "source_report_status": state["status"],
        "source_report_sha256": state.get("report_sha256"),
        "evidence_count": len(evidence), "claim_count": len(claims),
        "referenced_evidence_count": len(referenced),
        "finding_counts": dict(counts), "findings": items,
        "bibliographic_coverage": "CANONICAL_EVIDENCE_AND_CLAIMS_ONLY",
        "full_manuscript_citations_audited": False,
        "semantic_support_proven": False,
        "independent_scientific_review_completed": False,
        "google_drive_sync_verified": False,
        "disclaimer": "Identity, DOI, source-report and Evidence_ID checks are not semantic corroboration.",
    }

def _write_output(root: Path, raw: Path, result: dict):
    write_report(root, raw, json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                 allowed_extensions=frozenset({".json"}))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_path")
    parser.add_argument("--output", type=Path, help="Optional local report, never an asserted Drive sync")
    parser.add_argument("--strict", action="store_true", help="Return 2 for any blockers/reviews")
    args = parser.parse_args(argv)
    try:
        root = Path(args.project_path).resolve()
        result = audit(root)
        if args.output is not None:
            _write_output(root, args.output, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.strict and any(result["finding_counts"].values()):
            return 2
        return 0
    except (ValueError, OSError, json.JSONDecodeError, csv.Error) as exc:
        print("REFERENCE_AUDIT_ERROR: " + str(exc), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
