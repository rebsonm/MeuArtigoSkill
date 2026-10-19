#!/usr/bin/env python3
"""Privacy-bounded REG-013 scientific diagnostic projection.

Never expose passages, evidence titles, researchers, paths or gate decisions.
This is a read-only technical inventory, not an assurance of scientific merit.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from scientific_diagnostic import compose

SCHEMA = "MEU_ARTIGO_SCIENTIFIC_ADVISORY_PANEL_V1"
SAFE_CODE = re.compile(r"[A-Z][A-Z0-9_]{0,63}\Z")
STATUSES = {"MISSING", "STALE", "RECORDED_CLEAR",
            "BLOCKED", "REVIEW_REQUIRED", "UNAVAILABLE"}

def unavailable() -> dict:
    return {
        "schema": SCHEMA, "status": "INPUTS_UNAVAILABLE",
        "verdict": None, "objective_blockers": None,
        "review_occurrences": None, "advisory_occurrences": None,
        "strict_required_occurrences": None, "priority_codes": [],
        "source_report_status": "UNAVAILABLE",
        "human_review_required": True,
        "semantic_support_proven": False,
        "scientific_quality_validated": False,
        "scientific_gate_approved": False,
        "reports_written": False, "drive_sync_verified": False,
    }

def project(root: Path) -> dict:
    # REG-013 checks current canonical source hashes. Never emit the
    # unsanitized diagnostic or an exception message to a UI/host.
    try:
        raw = compose(Path(root))
        counts = raw["counts"]
        if raw.get("scientific_quality_validated") is not False or (
            raw.get("semantic_entailment_automated") is not False):
            return unavailable()
        vals = {}
        for key in ("blocking_occurrences", "review_occurrences",
                    "strict_required_occurrences",
                    "heuristic_advisory_occurrences",
                    "contextual_advisory_occurrences"):
            value = counts.get(key)
            if type(value) is not int or value < 0 or value > 1_000_000:
                return unavailable()
            vals[key] = value
        codes = []
        for item in raw.get("priority_findings", []):
            code = item.get("code") if isinstance(item, dict) else None
            if not isinstance(code, str) or not SAFE_CODE.fullmatch(code):
                return unavailable()
            codes.append(code)
        if len(codes) > 6 or raw.get("verdict") not in {
                "CORRECAO_REQUERIDA", "REVISAO_CIENTIFICA_PENDENTE"}:
            return unavailable()
        source_status = raw.get("source_verification")
        if source_status not in STATUSES:
            return unavailable()
        return {
            "schema": SCHEMA, "status": "RECORDED_UNASSESSED",
            "verdict": raw["verdict"],
            "objective_blockers": vals["blocking_occurrences"],
            "review_occurrences": vals["review_occurrences"],
            "advisory_occurrences":
                vals["heuristic_advisory_occurrences"] +
                vals["contextual_advisory_occurrences"],
            "strict_required_occurrences":
                vals["strict_required_occurrences"],
            "priority_codes": codes,
            "source_report_status": source_status,
            "human_review_required": True,
            "semantic_support_proven": False,
            "scientific_quality_validated": False,
            "scientific_gate_approved": False,
            "reports_written": False, "drive_sync_verified": False,
        }
    except (OSError, ValueError, KeyError, TypeError,
            csv.Error, json.JSONDecodeError):
        return unavailable()
