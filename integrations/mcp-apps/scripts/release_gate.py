#!/usr/bin/env python3
"""Fail-closed documentary gate inventory for the Meu Artigo go-live.

Reports *records*, never validates the underlying real-world evidence or
authorizes merges, installations, deployment or publication. No network.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SHA = re.compile(r"[a-f0-9]{40}\\Z")
REF = re.compile(r"EVID-[A-Za-z0-9_-]{6,64}\\Z")
ROLES = {
    "R01": "INDEPENDENT_REVIEWER",
    "R02": "TEST_OPERATOR",
    "R03": "MAINTAINER",
    "R04": "CI_OPERATOR",
    "R05": "OPERATOR",
    "R06": "TEST_OPERATOR",
    "R07": "TEST_OPERATOR",
    "R08": "MAINTAINER",
    "R09": "MAINTAINER",
    "R10": "PLATFORM_REVIEWER",
}
PHASES = {
    "R01": "CUMULATIVE_SECURITY_REVIEW",
    "R02": "CHATGPT_E05_UI_CSP",
    "R03": "SHA_SPECIFIC_MERGE_AUTHORIZATION",
    "R04": "POST_MERGE_CI_AND_BUNDLE",
    "R05": "PRODUCTION_HTTPS_OPERATION",
    "R06": "REAL_AUTH0_PKCE_AB",
    "R07": "REAL_DRIVE_AB_F1_F9",
    "R08": "REAL_E2E_PRIVACY_ROLLBACK",
    "R09": "PRIVATE_PLUGIN_AND_PILOT",
    "R10": "PUBLIC_REVIEW_AND_EXTERNAL_INSTALL",
}
FIELDS = {"status", "source_sha", "evidence_ref", "observer_role"}


def assess(source_sha: str, records: dict | None = None) -> dict:
    if not isinstance(source_sha, str) or not SHA.fullmatch(source_sha):
        raise ValueError("SOURCE_SHA_INVALID")
    if records is None:
        records = {}
    if not isinstance(records, dict) or set(records) - set(PHASES):
        raise ValueError("UNKNOWN_GATE_OR_BAD_RECORDS")
    gates = []
    for key, title in PHASES.items():
        entry = records.get(key)
        status = "NOT_VERIFIED"
        if entry is not None:
            if not isinstance(entry, dict) or set(entry) != FIELDS:
                raise ValueError("EVIDENCE_SHAPE_INVALID")
            raw = entry.get("status")
            if raw not in {"PASS", "FAIL", "PENDING"}:
                raise ValueError("EVIDENCE_STATUS_INVALID")
            if entry.get("observer_role") != ROLES[key]:
                raise ValueError("EVIDENCE_ROLE_INVALID")
            ref = entry.get("evidence_ref")
            if not isinstance(ref, str) or not REF.fullmatch(ref):
                raise ValueError("EVIDENCE_REFERENCE_INVALID")
            observed_sha = entry.get("source_sha")
            if not isinstance(observed_sha, str) or not SHA.fullmatch(observed_sha):
                raise ValueError("EVIDENCE_SHA_INVALID")
            status = "STALE" if observed_sha != source_sha else (
                "RECORDED_PASS" if raw == "PASS" else
                "RECORDED_FAIL" if raw == "FAIL" else "NOT_VERIFIED"
            )
        gates.append({"id": key, "name": title, "status": status})
    remaining = sum(row["status"] != "RECORDED_PASS" for row in gates)
    return {
        "schema": "MEU_ARTIGO_RELEASE_GATE_REGISTER_V1",
        "source_sha": source_sha,
        "remaining": remaining,
        "total": len(gates),
        "documentary_inputs_independently_authenticated": False,
        "merge_authorized": False,
        "deployment_authorized": False,
        "plugin_update_authorized": False,
        "publication_authorized": False,
        "decision": ("RECORDED_ONLY_REQUIRES_EXTERNAL_APPROVAL"
                     if remaining == 0 else "NO_GO_MISSING_OR_STALE_EVIDENCE"),
        "gates": gates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--records", type=Path, default=None)
    args = parser.parse_args()
    try:
        records = (json.loads(args.records.read_text(encoding="utf-8"))
                   if args.records is not None else None)
        report = assess(args.source_sha, records)
    except (ValueError, TypeError, OSError, json.JSONDecodeError) as exc:
        # Fixed error code only: never print evidence paths or contents.
        print('{"decision":"INVALID_EVIDENCE_INPUT","all_go":false}')
        return 2
    print(json.dumps(report, sort_keys=True, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
