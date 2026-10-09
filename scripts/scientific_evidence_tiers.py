#!/usr/bin/env python3
"""Distinguish four evidentiary layers without treating logging as scientific proof.

Conservative structural audit. Documentation of human review is an assertion
with a reference, not independent authentication. Metadata and literal
locators do not verify source interpretation or empirical scientific results.
Uses existing IDs and existing tables; creates no permanent result files.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from claim_integrity import type_of
from method_routes import EMPIRICAL_ROUTES, load as load_method

MGMT = "00_Gestao_e_Continuidade"


def csv_rows(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def audit(project: Path, *, freeze: bool = False) -> dict:
    root = Path(project).resolve()
    config = root / MGMT / "PROJECT_CONFIG.json"
    cfg = json.loads(config.read_text(encoding="utf-8")) if config.is_file() else {}
    evidence_file = root / MGMT / "05_Evidence_Matrix.csv"
    report_file = root / MGMT / "SOURCE_VERIFICATION.json"
    claims = csv_rows(root / MGMT / "09_Claims_Ledger.csv")
    gates = {
        x.get("GATE_ID"): x for x in csv_rows(root / MGMT / "18_Human_Validation_Gates.csv")
    }
    issues: list[str] = []
    warnings: list[str] = []
    tiers = {
        "bibliographic_identity_checked": 0,
        "literal_passage_matched": 0,
        "researcher_review_recorded": 0,
        "empirical_result_claims": 0,
    }
    if report_file.is_file() and evidence_file.is_file():
        try:
            report = json.loads(report_file.read_text(encoding="utf-8"))
            if report.get("input_sha256") == hashlib.sha256(evidence_file.read_bytes()).hexdigest():
                for item in report.get("checks", []):
                    if item.get("metadata_status") == "VERIFIED":
                        tiers["bibliographic_identity_checked"] += 1
                    if item.get("locator_status") == "MATCHED":
                        tiers["literal_passage_matched"] += 1
            else:
                warnings.append("source verification report does not match current Evidence Matrix")
        except (ValueError, TypeError):
            warnings.append("source verification report is not readable")
    for row in claims:
        if not (row.get("Claim_ID") or "").strip():
            continue
        kind = type_of(row.get("Claim_type"))
        if (row.get("Human_validation") or "").strip().upper() in {"VALIDATED", "REVISED"} and (
            row.get("Researcher_review_evidence") or "").strip():
            tiers["researcher_review_recorded"] += 1
        if kind != "E":
            continue
        tiers["empirical_result_claims"] += 1
        if not (freeze and cfg.get("method_route_governance_required") is True):
            continue
        cid = (row.get("Claim_ID") or "").strip()
        route = cfg.get("method_route")
        if route not in EMPIRICAL_ROUTES:
            issues.append(f"{cid}: empirical result is not linked to an empirical/design-science method route")
            continue
        try:
            profile = load_method(root)
        except (OSError, ValueError, TypeError):
            issues.append(f"{cid}: method evidence profile is unavailable")
            continue
        if profile.get("route") != route or profile.get("evidence_status") != "ANALYSIS_DOCUMENTED":
            issues.append(f"{cid}: method route has no recorded completed analysis/evaluation")
        for field in ("material_evidence_ref", "analysis_evidence_ref"):
            if not str(profile.get(field) or "").strip():
                issues.append(f"{cid}: {field} is absent; planning text does not prove a result")
        if route == "MIXED_METHODS" and not str(profile.get("integration_evidence_ref") or "").strip():
            issues.append(f"{cid}: quantitative/qualitative integration evidence reference is absent")
        for gate in ("GATE-0004", "GATE-0005"):
            state = gates.get(gate) or {}
            if state.get("Status") != "COMPLETED" or state.get("Decision") not in (
                "APPROVED", "APPROVED_WITH_CHANGES"
            ):
                issues.append(f"{cid}: {gate} lacks actual human approval")
        if not (row.get("Trace_IDs") or "").strip():
            issues.append(f"{cid}: empirical claim has no existing TRACE_ID reference to analytic provenance")
        if not (row.get("Researcher_review_evidence") or "").strip():
            issues.append(f"{cid}: no original researcher review reference for this empirical result")

    return {
        "layers": tiers,
        "errors": issues,
        "warnings": warnings,
        "bibliographic_identity_proves_text_read": False,
        "literal_locator_proves_claim_semantics": False,
        "human_review_record_authenticates_reviewer": False,
        "empirical_scientific_result_independently_validated": False,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--freeze", action="store_true",
                        help="Enforce empirical-result provenance for new route-aware projects")
    args = parser.parse_args(argv)
    try:
        report = audit(Path(args.project), freeze=args.freeze)
    except (OSError, ValueError, TypeError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
