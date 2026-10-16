#!/usr/bin/env python3
"""Inspect local CodeQL SARIF without requiring repository settings changes.

This quality gate runs after CodeQL completes with upload disabled. It does not
replace repository Code Scanning default setup; it prevents critical/high
security findings from being silently discarded in the isolated test branch.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def inspect(directory: Path) -> dict:
    folder = Path(directory).resolve()
    if not folder.is_dir():
        raise ValueError("CODEQL_RESULTS_DIRECTORY_MISSING")
    sources = sorted(folder.glob("*.sarif"))
    if not sources:
        raise ValueError("CODEQL_RESULTS_MISSING")
    total, high, other, inspected = 0, 0, 0, 0
    for path in sources:
        if path.is_symlink() or not path.is_file():
            raise ValueError("CODEQL_RESULTS_UNSAFE_PATH")
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("version") != "2.1.0" or not isinstance(data.get("runs"), list):
            raise ValueError("CODEQL_SARIF_INVALID")
        for run in data["runs"]:
            driver = (run.get("tool") or {}).get("driver") or {}
            if driver.get("name") != "CodeQL":
                raise ValueError("CODEQL_SARIF_UNEXPECTED_TOOL")
            inspected += 1
            rules = {v.get("id"): v for v in driver.get("rules", []) if isinstance(v, dict)}
            for alert in run.get("results", []):
                if not isinstance(alert, dict):
                    raise ValueError("CODEQL_ALERT_INVALID")
                total += 1
                rule = rules.get(alert.get("ruleId"), {})
                prop = rule.get("properties") or {}
                raw = (alert.get("properties") or {}).get("security-severity",
                       prop.get("security-severity"))
                try:
                    score = float(raw) if raw is not None else None
                except (TypeError, ValueError) as exc:
                    raise ValueError("CODEQL_ALERT_SEVERITY_INVALID") from exc
                if score is not None and not math.isfinite(score):
                    raise ValueError("CODEQL_ALERT_SEVERITY_INVALID")
                if (score is not None and score >= 7.0) or (
                     score is None and alert.get("level") == "error"):
                    high += 1
                else:
                    other += 1
    if inspected == 0:
        raise ValueError("CODEQL_SARIF_NO_CODEQL_RUN")
    return {"runs": inspected, "results": total, "high": high,
            "other_requires_manual_review": other}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--directory", type=Path, required=True)
    a = ap.parse_args()
    try:
        report = inspect(a.directory)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print("ERROR: "+type(exc).__name__)
        return 2
    print("codeql_runs="+str(report["runs"]))
    print("codeql_results="+str(report["results"]))
    print("codeql_high_security_findings="+str(report["high"]))
    print("codeql_other_requires_manual_review="+str(report["other_requires_manual_review"]))
    return 1 if report["high"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
