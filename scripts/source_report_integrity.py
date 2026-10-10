#!/usr/bin/env python3
"""Read-only integrity assessment for SOURCE_VERIFICATION.json.

This module does not authenticate a reviewer or validate claim semantics.
It checks exact input bindings and attributable exception *records*, keeping
the underlying source checks unchanged. No new register or ID family.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

MGMT = "00_Gestao_e_Continuidade"
INPUTS = {
    "evidence": "05_Evidence_Matrix.csv",
    "screening": "03_Screening.csv",
    "fulltext": "04_FullText_Tracker.csv",
}
LOCAL_FIELDS = ("Source_path", "PDF_path", "FullText_path", "Full_text_path", "File_path")
BAD_LOCATORS = {"PAGE_MISMATCH", "PASSAGE_NOT_FOUND", "OUTSIDE_WORKSPACE"}
EXPECTED_SUCCESS = "METADATA_AND_LOCATOR_CHECKED"
SOURCE_REPORT = "SOURCE_VERIFICATION.json"
RESPONSE_PREFIX = "ORIGINAL_RESPONSE_REF="
LIMIT_PREFIX = "SOURCE_REVIEW_LIMITATIONS="

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))

def tokens(value: str) -> list[str]:
    return [x for x in re.split(r"[\s,;]+", value or "") if x]

def is_remote(value: str) -> bool:
    return value.lower().startswith(("https://", "http://", "drive:", "s3:"))

def local_entry(root: Path, raw: str) -> dict | None:
    raw = raw.strip()
    if not raw or is_remote(raw):
        return None
    # Store paths only in the internal report, not in user-facing MCP results.
    root = root.resolve()
    path = (root / raw).resolve()
    if not path.is_relative_to(root):
        return {"path": raw, "state": "OUTSIDE_WORKSPACE", "sha256": None}
    relative = path.relative_to(root).as_posix()
    if not path.is_file():
        return {"path": relative, "state": "MISSING", "sha256": None}
    if path.suffix.lower() not in {".pdf", ".txt", ".md"}:
        return {"path": relative, "state": "UNSUPPORTED_FORMAT", "sha256": None}
    if path.stat().st_size > 30 * 1024 * 1024:
        return {"path": relative, "state": "FILE_TOO_LARGE", "sha256": None}
    return {"path": relative, "state": "PRESENT", "sha256": sha256(path)}

def manifest(root: Path) -> dict:
    """Canonical input snapshot includes the entire 3 CSVs and every referenced local file.

    Appearances/disappearances are discovered by re-enumerating current rows,
    not only by checking paths that were recorded in the old report.
    """
    root = Path(root).resolve()
    base = root / MGMT
    csvs = {}
    for name, filename in INPUTS.items():
        path = base / filename
        csvs[name] = sha256(path) if path.is_file() else None
    evidence = load_csv(base / INPUTS["evidence"])
    screening = load_csv(base / INPUTS["screening"])
    fulltext = load_csv(base / INPUTS["fulltext"])
    issues = []
    for title, records, key in [
        ("evidence", evidence, "Evidence_ID"), ("screening", screening, "Record_ID"),
        ("fulltext", fulltext, "Record_ID")
    ]:
        seen = Counter(str(r.get(key) or "").strip() for r in records)
        if any(not str(r.get(key) or "").strip() for r in records):
            issues.append(f"{title}: missing {key}")
        if any(count > 1 for name, count in seen.items() if name):
            issues.append(f"{title}: duplicate {key}")
    evidence_ids = [str(r.get("Evidence_ID") or "").strip() for r in evidence]
    screening_ids = {str(r.get("Record_ID") or "").strip() for r in screening}
    tracker_ids = {str(r.get("Record_ID") or "").strip() for r in fulltext}
    links: dict[str, set[str]] = {}
    for r in fulltext:
        record = str(r.get("Record_ID") or "").strip()
        for e_id in tokens(str(r.get("Evidence_matrix_id") or "")):
            links.setdefault(e_id, set()).add(record)
            if e_id not in evidence_ids:
                issues.append("fulltext: unknown Evidence_ID link")
    bindings = []
    for r in evidence:
        eid = str(r.get("Evidence_ID") or "").strip()
        own = str(r.get("Record_ID") or "").strip()
        linked = links.get(eid, set())
        if own and linked and linked != {own}:
            issues.append("evidence/fulltext: Record_ID link conflict")
        if len(linked) > 1:
            issues.append("fulltext: ambiguous Evidence_ID to Record_ID")
        rid = own or (next(iter(linked)) if len(linked) == 1 else "")
        if rid and rid not in screening_ids and rid not in tracker_ids:
            issues.append("evidence: Record_ID absent from screening and fulltext")
        bindings.append({"Evidence_ID": eid, "Record_ID": rid})
    local = {}
    # Cover referenced local files regardless of whether they have a locator.
    for r in evidence:
        for field in LOCAL_FIELDS:
            if str(r.get(field) or "").strip():
                entry = local_entry(root, str(r[field]))
                if entry:
                    local[entry["path"]] = entry
    for r in fulltext:
        raw = str(r.get("File_or_URL") or "").strip()
        if raw:
            entry = local_entry(root, raw)
            if entry:
                local[entry["path"]] = entry
    for r in screening:
        raw = str(r.get("File_or_URL") or "").strip()
        if raw:
            entry = local_entry(root, raw)
            if entry:
                local[entry["path"]] = entry
    # File contents are never included. Do not leak raw paths via MCP.
    return {
        "csv_sha256": csvs,
        "files": [local[k] for k in sorted(local)],
        "bindings": bindings,
        "screening_record_ids": sorted(screening_ids - {""}),
        "fulltext_record_ids": sorted(tracker_ids - {""}),
        "identity_issues": sorted(set(issues)),
    }

def recorded_exceptions(root: Path, report_sha: str) -> dict[str, bool]:
    """Read only existing DEC_ID evidence decisions; never infer consent from notes alone."""
    result = {}
    path = root / MGMT / "17_Decision_Log.csv"
    for r in load_csv(path):
        if (r.get("Decision_type") or "").upper().strip() != "EVIDENCE":
            continue
        if (r.get("Status") or "").upper().strip() != "APPROVED":
            continue
        if (r.get("Gate_ID") or "").strip() != "GATE-0006":
            continue
        if (r.get("Affected_artifacts") or "").strip() != f"{SOURCE_REPORT}#sha256={report_sha}":
            continue
        ids = tokens(r.get("Evidence_IDs") or "")
        if len(ids) != 1 or not (r.get("Decided_by") or "").strip():
            continue
        rationale = (r.get("Rationale") or "").strip()
        notes = r.get("Notes") or ""
        lines = [x.strip() for x in notes.splitlines()]
        limitations = next((x[len(LIMIT_PREFIX):].strip() for x in lines if x.startswith(LIMIT_PREFIX)), "")
        original = next((x[len(RESPONSE_PREFIX):].strip() for x in lines if x.startswith(RESPONSE_PREFIX)), "")
        if len(rationale) < 40 or len(limitations) < 20 or len(original) < 8:
            continue
        result[ids[0]] = True
    return result

def assess(root: Path, *, require_complete: bool = True) -> dict:
    """Fail closed on stale input, objectively conflicting locators, or missing approvals.

    Returns sanitized counts/status only. Errors are generic and have no local
    paths, copied excerpts, DOI, free-text rationales or file contents.
    """
    root = Path(root).resolve()
    report_path = root / MGMT / SOURCE_REPORT
    current = manifest(root)
    state = {
        "status": "MISSING", "report_sha256": None,
        "checked": 0, "pending_review": 0, "blocked": 0,
        "editorial_retraction_alerts": 0, "editorial_correction_alerts": 0,
        "editorial_updates": 0, "provider_warnings": 0,
        "reviewed_limitations": 0, "report_missing": True,
        "report_stale": False, "errors": [], "warnings": [],
        "approved_with_unresolved_controls": False,
    }
    if not report_path.is_file():
        if require_complete:
            state["errors"].append("source report missing")
        return state
    state["report_missing"] = False
    try:
        report_bytes = report_path.read_bytes()
        report = json.loads(report_bytes)
        if not isinstance(report, dict):
            raise ValueError("Invalid report")
    except (OSError, ValueError, TypeError):
        state.update(status="BLOCKED", blocked=1)
        state["errors"].append("source report unreadable")
        return state
    report_sha = hashlib.sha256(report_bytes).hexdigest()
    state["report_sha256"] = report_sha
    if report.get("schema_version") != 2 or not isinstance(report.get("input_manifest"), dict):
        state["status"] = "STALE"
        state["report_stale"] = True
        state["errors"].append("source report schema must be regenerated")
        return state
    snapshot = report["input_manifest"]
    if snapshot != current:
        state["report_stale"] = True
        state["status"] = "STALE"
        state["errors"].append("source report inputs changed or identifiers differ")
        return state
    if any(value is None for value in current["csv_sha256"].values()):
        state["errors"].append("source report lacks canonical CSV inputs")
    if current["identity_issues"]:
        state["errors"].append("ambiguous or duplicated Evidence_ID/Record_ID links")
    if any(f["state"] == "OUTSIDE_WORKSPACE" for f in current["files"]):
        state["errors"].append("local source path outside authorized workspace")
    entries = report.get("checks")
    if not isinstance(entries, list):
        entries = []
        state["errors"].append("source report checks missing")
    observed = [{"Evidence_ID": str(x.get("Evidence_ID") or "").strip(),
                 "Record_ID": str(x.get("Record_ID") or "").strip()}
                for x in entries if isinstance(x, dict)]
    if len(observed) != len(entries) or observed != snapshot["bindings"]:
        state["errors"].append("source report entries do not match exact canonical IDs")
    if Counter(x["Evidence_ID"] for x in observed) != Counter(
        x["Evidence_ID"] for x in snapshot["bindings"]
    ):
        state["errors"].append("source report missing, extra, or duplicated Evidence_ID")
    exceptions = recorded_exceptions(root, report_sha)
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        state["checked"] += 1
        if entry.get("retraction_alert"):
            state["editorial_retraction_alerts"] += 1
        if entry.get("correction_alert"):
            state["editorial_correction_alerts"] += 1
        if entry.get("update_alert"):
            state["editorial_updates"] += 1
        state["provider_warnings"] += len(entry.get("provider_warnings") or [])
        locator = str(entry.get("locator_status") or "")
        outcome = str(entry.get("result") or "")
        meta = str(entry.get("metadata_status") or "")
        if (outcome == "FAIL" or locator in BAD_LOCATORS
                or meta in {"INVALID_DOI", "MISMATCH", "NOT_FOUND"}
                or (not entry.get("Evidence_ID"))):
            state["blocked"] += 1
        elif outcome != EXPECTED_SUCCESS or entry.get("provider_warnings"):
            state["pending_review"] += 1
            if exceptions.get(str(entry.get("Evidence_ID") or "")):
                state["reviewed_limitations"] += 1
    if state["blocked"] or state["errors"]:
        state["status"] = "BLOCKED"
    elif state["pending_review"]:
        if state["pending_review"] == state["reviewed_limitations"]:
            state["status"] = "REVIEWED_LIMITATIONS"
        else:
            state["status"] = "REVIEW_REQUIRED"
            if require_complete:
                state["errors"].append("source reviews pending documented human assessment")
    else:
        state["status"] = "RECORDED_CLEAR"
    if state["blocked"] and require_complete:
        state["errors"].append("objective source conflicts block scientific approval")
    # A review exception never upgrades row results to VERIFIED.
    return state
