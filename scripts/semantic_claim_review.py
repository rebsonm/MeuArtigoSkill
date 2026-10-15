#!/usr/bin/env python3
"""REG-011: bounded claim-to-passage review, explicitly requiring human judgment.

The program checks identifiers, current source hashes and literal quotations;
it CANNOT infer semantic entailment or authenticate the claimed human reviewer.
Outputs are read-only observations unless a local report is explicitly requested.
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

from report_output_guard import write_report
from claim_integrity import clean, refs, type_of
from source_report_integrity import MGMT, SOURCE_REPORT, assess
from verify_sources import check_locator

CLAIMS = "09_Claims_Ledger.csv"
EVIDENCE = "05_Evidence_Matrix.csv"
VERDICTS = {"SUPPORTED", "PARTIALLY_SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE"}
ALIGNMENTS = {"ALIGNED", "OVERGENERALIZED", "MISREPRESENTED", "UNKNOWN"}

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def local_json(root: Path, raw: Path) -> dict:
    target = (raw if raw.is_absolute() else root / raw).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        raise ValueError("Assessment file unavailable inside authorized project")
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Assessment input must be a JSON object")
    return data

def read_csv(root: Path, filename: str, required: set[str]) -> list[dict]:
    path = root / MGMT / filename
    if not path.is_file() or path.is_symlink():
        raise ValueError("Required canonical register unavailable: " + filename)
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Invalid canonical headers: " + filename)
        rows = list(reader)
    if any(None in row for row in rows):
        raise ValueError("Malformed canonical records: " + filename)
    return rows

def snapshot(root: Path) -> dict:
    result = {}
    for name in (CLAIMS, EVIDENCE, SOURCE_REPORT):
        path = root / MGMT / name
        result[name] = sha(path.read_bytes()) if path.is_file() else None
    return result

def valid_annotation(entry: dict, claim_hash: str, source_hash: str,
                     report_hash: str) -> str | None:
    if entry.get("reviewer_kind") != "HUMAN_DECLARED":
        return "HUMAN_REVIEW_NOT_DECLARED"
    if any(not isinstance(entry.get(k), str) or not entry[k].strip()
           for k in ("reviewer", "response_reference", "rationale", "limitations")):
        return "REVIEW_ATTESTATION_INCOMPLETE"
    if len(clean(entry["rationale"])) < 40 or len(clean(entry["limitations"])) < 20:
        return "REVIEW_RATIONALE_TOO_BRIEF"
    if entry.get("claim_sha256") != claim_hash or entry.get("source_sha256") != source_hash \
            or entry.get("source_report_sha256") != report_hash:
        return "REVIEW_BOUND_TO_STALE_OR_DIFFERENT_INPUT"
    if entry.get("judgment") not in VERDICTS:
        return "INVALID_SEMANTIC_JUDGMENT"
    if any(entry.get(k) not in ALIGNMENTS for k in ("scope_alignment", "method_alignment", "context_alignment")):
        return "MISSING_DIMENSIONAL_REVIEW"
    if type(entry.get("counterevidence_considered")) is not bool:
        return "COUNTEREVIDENCE_REVIEW_NOT_RECORDED"
    if entry["judgment"] == "SUPPORTED" and (
            not entry["counterevidence_considered"] or
            any(entry[k] != "ALIGNED" for k in ("scope_alignment", "method_alignment", "context_alignment"))):
        return "UNQUALIFIED_SUPPORT_CONTRADICTS_REVIEW"
    return None

def review(root: Path, assessments: dict | None = None) -> dict:
    root = Path(root).resolve()
    initial = snapshot(root)
    claims = read_csv(root, CLAIMS, {"Claim_ID", "Claim_type", "Claim_text", "Evidence_IDs"})
    evidence = read_csv(root, EVIDENCE, {"Evidence_ID"})
    evidence_counts = Counter(clean(e.get("Evidence_ID")) for e in evidence)
    claim_counts = Counter(clean(c.get("Claim_ID")) for c in claims)
    state = assess(root, require_complete=False)
    report_hash = state.get("report_sha256")
    report_rows = defaultdict(list)
    # Source metadata is used only when its input bindings are current and
    # internally consistent. Objective source failures may coexist with clean
    # other records, but an inconsistent/stale report is not trusted at all.
    trustworthy = state["status"] not in {"MISSING", "STALE"} and not state["errors"]
    if trustworthy:
        report = json.loads((root / MGMT / SOURCE_REPORT).read_text(encoding="utf-8"))
        for row in report["checks"]:
            report_rows[clean(row.get("Evidence_ID"))].append(row)

    claimed = {}
    if assessments is not None:
        if assessments.get("schema_version") != 1 or not isinstance(assessments.get("reviews"), list):
            raise ValueError("Expected schema_version 1 and reviews array")
        for row in assessments["reviews"]:
            if not isinstance(row, dict):
                raise ValueError("Invalid review item")
            key = (clean(row.get("claim_id")), clean(row.get("evidence_id")))
            if not all(key) or key in claimed:
                raise ValueError("Duplicate or incomplete claim/evidence review")
            claimed[key] = row
    result = []
    valid_pairs = set()
    ids = set()
    for claim in claims:
        if type_of(claim.get("Claim_type")) != "L":
            continue
        cid = clean(claim.get("Claim_ID"))
        if not cid:
            raise ValueError("Blank literature Claim_ID")
        ids.add(cid)
        if claim_counts[cid] != 1:
            raise ValueError("Duplicate literature Claim_ID")
        references = refs(claim.get("Evidence_IDs"))
        claim_hash = sha(clean(claim.get("Claim_text")).encode("utf-8"))
        if not references:
            result.append({"claim_id": cid, "evidence_id": None,
                           "status": "MISSING_EVIDENCE_LINK", "declared_judgment": None})
            continue
        if len(set(references)) != len(references):
            raise ValueError("Duplicate Evidence_ID in one claim")
        for eid in references:
            key = (cid, eid)
            valid_pairs.add(key)
            row = {"claim_id": cid, "evidence_id": eid,
                   "claim_sha256": claim_hash,
                   "status": "PENDING_HUMAN_REVIEW", "declared_judgment": None,
                   "semantic_support_proven": False}
            if evidence_counts[eid] != 1:
                row["status"] = "EVIDENCE_MISSING_OR_AMBIGUOUS"
            elif not trustworthy:
                row["status"] = "SOURCE_REPORT_UNAVAILABLE_OR_STALE"
            elif len(report_rows[eid]) != 1:
                row["status"] = "SOURCE_CHECK_MISSING_OR_AMBIGUOUS"
            else:
                source = report_rows[eid][0]
                row["source_sha256"] = source.get("source_sha256")
                if (source.get("metadata_status") != "VERIFIED"
                        or source.get("locator_status") != "MATCHED"
                        or source.get("result") != "METADATA_AND_LOCATOR_CHECKED"
                        or source.get("retraction_alert") or source.get("correction_alert")
                        or source.get("update_alert") or source.get("provider_warnings")):
                    row["status"] = "SOURCE_REQUIRES_REVIEW"
                elif key in claimed:
                    annotation = claimed[key]
                    verdict = annotation.get("judgment")
                    row["declared_judgment"] = verdict if verdict in VERDICTS else None
                    problem = valid_annotation(annotation, claim_hash, source.get("source_sha256"), report_hash)
                    if problem:
                        row["status"] = problem
                    else:
                        passage = annotation.get("quoted_passage")
                        if not isinstance(passage, str) or len(clean(passage)) < 35:
                            row["status"] = "EXACT_SOURCE_PASSAGE_REQUIRED"
                        else:
                            locator = check_locator(root, source.get("source_path") or "", passage)
                            row["passage_sha256"] = sha(clean(passage).encode("utf-8"))
                            row["passage_check_status"] = locator["status"]
                            if locator["status"] != "MATCHED" or locator.get("source_sha256") != source.get("source_sha256"):
                                row["status"] = "QUOTED_PASSAGE_NOT_CONFIRMED"
                            else:
                                row["status"] = "HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED"
                                row["review_rationale_sha256"] = sha(clean(annotation["rationale"]).encode("utf-8"))
                                row["review_response_sha256"] = sha(clean(annotation["response_reference"]).encode("utf-8"))
                                row["reviewer_authentication"] = "NOT_VERIFIED"
            result.append(row)
    unknown = set(claimed) - valid_pairs
    if unknown:
        raise ValueError("Review contains claim/evidence linkage absent from the canonical literature ledger")
    if snapshot(root) != initial:
        raise ValueError("Canonical source or claims changed during assessment")
    counts = Counter(row["status"] for row in result)
    claims_summary = []
    for cid in sorted(ids):
        entries = [x for x in result if x["claim_id"] == cid]
        claimed_outcomes = [x.get("declared_judgment") for x in entries]
        claims_summary.append({
            "claim_id": cid, "linked_evidence_items": len(entries),
            "all_human_judgments_recorded": bool(entries) and all(
                e["status"] == "HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED" for e in entries),
            "one_or_more_not_supported": "NOT_SUPPORTED" in claimed_outcomes,
            "one_or_more_partially_supported": "PARTIALLY_SUPPORTED" in claimed_outcomes,
            "one_or_more_inconclusive": "INCONCLUSIVE" in claimed_outcomes,
            "scientific_claim_approved": False,
        })
    return {"schema_version": 1, "audit": "REG-011_HUMAN_ASSISTED_CLAIM_REVIEW",
            "canonical_snapshot_sha256": initial,
            "source_report_status": state["status"], "source_report_sha256": report_hash,
            "counts": dict(counts), "review_items": result, "claim_summaries": claims_summary,
            "semantic_support_proven": False, "researcher_authenticated": False,
            "gate_approval_performed": False, "independent_scientific_validation": False,
            "google_drive_sync_verified": False,
            "disclaimer": "Literal passage existence and declared human interpretation are not automated semantic proof or authenticated independent review."}

def save_local(root: Path, output: Path, data: dict, assessments_file: Path | None):
    write_report(root, output, json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                 allowed_extensions=frozenset({".json"}))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("project_path")
    p.add_argument("--assessments", type=Path, help="User-prepared review JSON inside project")
    p.add_argument("--output", type=Path, help="Optional local report (no implied Drive sync)")
    p.add_argument("--strict", action="store_true", help="2 when any judgment is missing/invalid")
    args = p.parse_args(argv)
    try:
        root = Path(args.project_path).resolve()
        data = local_json(root, args.assessments) if args.assessments else None
        report = review(root, data)
        if args.output:
            save_local(root,args.output,report,
                       (root/args.assessments) if args.assessments else None)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if args.strict and any(row["status"] != "HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED"
                               for row in report["review_items"]):
            return 2
        return 0
    except (ValueError, OSError, json.JSONDecodeError, csv.Error) as exc:
        print("CLAIM_REVIEW_ERROR: " + str(exc), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
