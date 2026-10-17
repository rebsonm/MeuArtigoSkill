#!/usr/bin/env python3
"""Audit local CodeQL SARIF, including rules declared in tool.extensions.

Does not access or claim to close GitHub Advanced Security alerts.
The narrowly acknowledged synthetic fixture findings remain counted as HIGH.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

# These deliberately insecure chmod calls are negative tests validating that
# archive integrity rejects world-readable receipt files. They are NOT
# production sinks. Every other HIGH finding, including any moved line, blocks.
_SYNTHETIC_F7_FIXTURES = frozenset({
    ("py/overly-permissive-file", "tests/test_drive_f7_anchor.py", 203),
    ("py/overly-permissive-file", "tests/test_drive_f7_anchor.py", 228),
})


def _codeql_rule(tool: dict, alert: dict) -> dict:
    driver = tool.get("driver") or {}
    extensions = tool.get("extensions") or []
    if not isinstance(extensions, list):
        raise ValueError("CODEQL_SARIF_INVALID_EXTENSIONS")
    ref = alert.get("rule") or {}
    tc = ref.get("toolComponent") or {}
    ci = tc.get("index")
    ri = ref.get("index")
    if ci is not None and ri is not None:
        if not isinstance(ci, int) or not 0 <= ci < len(extensions):
            raise ValueError("CODEQL_RULE_COMPONENT_INVALID")
        selected = extensions[ci].get("rules") or []
        if not isinstance(ri, int) or not 0 <= ri < len(selected):
            raise ValueError("CODEQL_RULE_INDEX_INVALID")
        rule = selected[ri]
        if rule.get("id") != alert.get("ruleId"):
            raise ValueError("CODEQL_RULE_REFERENCE_MISMATCH")
        return rule
    for component in [driver, *extensions]:
        for rule in component.get("rules") or []:
            if rule.get("id") == alert.get("ruleId"):
                return rule
    raise ValueError("CODEQL_RULE_METADATA_MISSING")


def _location(alert: dict) -> tuple[str, int | None]:
    locations = alert.get("locations") or []
    physical = (locations[0].get("physicalLocation") or {}) if locations else {}
    uri = (physical.get("artifactLocation") or {}).get("uri") or ""
    line = (physical.get("region") or {}).get("startLine")
    return uri, line


def inspect(directory: Path, *, acknowledge_synthetic_drive_f7_fixtures: bool = False) -> dict:
    folder = Path(directory).resolve()
    if not folder.is_dir():
        raise ValueError("CODEQL_RESULTS_DIRECTORY_MISSING")
    sources = sorted(folder.glob("*.sarif"))
    if not sources:
        raise ValueError("CODEQL_RESULTS_MISSING")
    total = high = other = inspected = acknowledged = 0
    for path in sources:
        if path.is_symlink() or not path.is_file():
            raise ValueError("CODEQL_RESULTS_UNSAFE_PATH")
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("version") != "2.1.0" or not isinstance(data.get("runs"), list):
            raise ValueError("CODEQL_SARIF_INVALID")
        for run in data["runs"]:
            tool = run.get("tool") or {}
            if (tool.get("driver") or {}).get("name") != "CodeQL":
                raise ValueError("CODEQL_SARIF_UNEXPECTED_TOOL")
            inspected += 1
            for alert in run.get("results") or []:
                if not isinstance(alert, dict):
                    raise ValueError("CODEQL_ALERT_INVALID")
                total += 1
                rule = _codeql_rule(tool, alert)
                prop = rule.get("properties") or {}
                raw = (alert.get("properties") or {}).get(
                    "security-severity", prop.get("security-severity"))
                try:
                    score = float(raw) if raw is not None else None
                except (TypeError, ValueError) as exc:
                    raise ValueError("CODEQL_ALERT_SEVERITY_INVALID") from exc
                if score is not None and not math.isfinite(score):
                    raise ValueError("CODEQL_ALERT_SEVERITY_INVALID")
                severe = ((score is not None and score >= 7.0)
                          or (score is None and alert.get("level") == "error"))
                if severe:
                    high += 1
                    uri, line = _location(alert)
                    if (acknowledge_synthetic_drive_f7_fixtures
                            and (alert.get("ruleId"), uri, line)
                            in _SYNTHETIC_F7_FIXTURES):
                        acknowledged += 1
                else:
                    other += 1
    if not inspected:
        raise ValueError("CODEQL_SARIF_NO_CODEQL_RUN")
    return {"runs": inspected, "results": total, "high": high,
            "acknowledged_synthetic_test_high": acknowledged,
            "blocking_high": high - acknowledged,
            "other_requires_manual_review": other}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--directory", type=Path, required=True)
    ap.add_argument("--acknowledge-synthetic-drive-f7-fixtures", action="store_true",
                    help="Acknowledge ONLY two exact HIGH negative-test fixtures; report both")
    a = ap.parse_args()
    try:
        report = inspect(
            a.directory,
            acknowledge_synthetic_drive_f7_fixtures=a.acknowledge_synthetic_drive_f7_fixtures)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print("ERROR: " + type(exc).__name__)
        return 2
    print("codeql_runs=" + str(report["runs"]))
    print("codeql_results=" + str(report["results"]))
    print("codeql_high_security_findings=" + str(report["high"]))
    print("codeql_acknowledged_synthetic_test_high=" +
          str(report["acknowledged_synthetic_test_high"]))
    print("codeql_blocking_high_security_findings=" + str(report["blocking_high"]))
    print("codeql_other_requires_manual_review=" +
          str(report["other_requires_manual_review"]))
    return 1 if report["blocking_high"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
