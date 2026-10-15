#!/usr/bin/env python3
"""Append-only software-evaluation registry, not scientific validation."""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys

ACTIONS = {"BLOCK", "FLAG", "PASS", "NOT_EVALUATED"}
EXPECTED = {"BLOCK", "FLAG", "PASS"}

def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")

def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def load(path):
    x = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(x, dict):
        raise ValueError("JSON object required")
    return x

def validate_catalog(c):
    if c.get("schema_version") != 1 or c.get("purpose") != "SYNTHETIC_ADVERSARIAL_CASES":
        raise ValueError("Unsupported case catalog")
    if not isinstance(c.get("cases"), list) or not c["cases"]:
        raise ValueError("Nonempty cases required")
    seen = {}
    for x in c["cases"]:
        if not isinstance(x, dict):
            raise ValueError("Invalid case object")
        cid = x.get("case_id")
        if not isinstance(cid, str) or not re.fullmatch(r"[A-Z]+-[0-9]{3}", cid) or cid in seen:
            raise ValueError("Invalid/duplicate case_id")
        if x.get("synthetic") is not True or x.get("expected_action") not in EXPECTED:
            raise ValueError("Only declared synthetic BLOCK/FLAG/PASS cases permitted")
        if any(not isinstance(x.get(k), str) or not x[k].strip()
               for k in ("scenario", "control", "category")):
            raise ValueError("Missing case documentation")
        seen[cid] = x
    return seen

def validate_observations(o, catalog):
    if o.get("schema_version") != 1 or not isinstance(o.get("cases"), list):
        raise ValueError("Invalid observations structure")
    items = {}
    for x in o["cases"]:
        if not isinstance(x, dict):
            raise ValueError("Invalid observation")
        cid = x.get("case_id")
        if cid not in catalog or cid in items:
            raise ValueError("Unknown/duplicate observation")
        action = x.get("observed_action")
        if action not in ACTIONS:
            raise ValueError("Invalid observed_action")
        ref = x.get("evidence_reference", "")
        if not isinstance(ref, str) or len(ref) > 1024 or (action != "NOT_EVALUATED" and not ref.strip()):
            raise ValueError("An observed action requires a nonempty evidence reference")
        items[cid] = {"observed_action": action, "evidence_reference": ref}
    return items

def summarize(catalog, observations):
    details = []
    good = bad = total = 0
    for cid, item in catalog.items():
        obs = observations.get(cid, {"observed_action": "NOT_EVALUATED", "evidence_reference": ""})
        action = obs["observed_action"]
        checked = action != "NOT_EVALUATED"
        total += int(checked)
        good += int(checked and action == item["expected_action"])
        bad += int(checked and action != item["expected_action"])
        details.append({"case_id": cid, "expected_action": item["expected_action"],
                        "observed_action": action, "matches_expected":
                        action == item["expected_action"] if checked else None,
                        "evidence_reference": obs["evidence_reference"]})
    return {"case_count": len(catalog), "observed": total,
            "not_evaluated": len(catalog)-total, "matches_expected": good,
            "mismatches": bad, "match_rate_on_observed": round(good/total, 6) if total else None,
            "scientific_validity_established": False,
            "independent_reviewer_authenticated": False,
            "scope": "SELF_REPORTED_SOFTWARE_OBSERVATIONS", "details": details}

def read_ledger(path):
    path = Path(path)
    if not path.exists():
        return []
    rows, previous, ids = [], None, set()
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            raise ValueError("Empty ledger entry")
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError("Invalid ledger object")
        unsigned = {k:v for k,v in row.items() if k != "entry_sha256"}
        if row.get("entry_sha256") != digest(unsigned) or row.get("previous_entry_sha256") != previous:
            raise ValueError("Ledger integrity/chain broken at line " + str(i))
        if row.get("run_id") in ids:
            raise ValueError("Duplicate ledger run_id")
        ids.add(row["run_id"])
        rows.append(row)
        previous = row["entry_sha256"]
    return rows

@contextmanager
def locked(ledger):
    marker = ledger.with_name(ledger.name + ".lock")
    try:
        fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError("Ledger is already locked") from exc
    os.close(fd)
    try:
        yield
    finally:
        marker.unlink(missing_ok=True)

def record(catalog_path, observed_path, ledger, run_id, commit):
    if not re.fullmatch(r"[A-Za-z0-9_.-]{3,100}", run_id):
        raise ValueError("Invalid run_id")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Exact 40-hex lowercase Skill commit required")
    source = load(catalog_path)
    cases = validate_catalog(source)
    observations = load(observed_path)
    submitted = validate_observations(observations, cases)
    ledger = Path(ledger)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with locked(ledger):
        old = read_ledger(ledger)
        if any(r["run_id"] == run_id for r in old):
            raise ValueError("Duplicate run_id; append-only ledger")
        row = {"schema_version":1,"event_type":"SOFTWARE_CASE_EVALUATION",
               "run_id":run_id,"recorded_at_utc":datetime.now(timezone.utc).isoformat(),
               "skill_commit":commit,"case_set_sha256":digest(source),
               "observations_sha256":digest(observations),
               "previous_entry_sha256":old[-1]["entry_sha256"] if old else None,
               "result":summarize(cases, submitted)}
        row["entry_sha256"] = digest(row)
        with ledger.open("ab") as stream:
            stream.write(canonical(row) + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
    return row

def compare(ledger, baseline, candidate):
    found = {x["run_id"]:x for x in read_ledger(ledger)}
    if baseline not in found or candidate not in found:
        raise ValueError("Unknown run identifier")
    b, c = found[baseline], found[candidate]
    if b["case_set_sha256"] != c["case_set_sha256"]:
        raise ValueError("Cannot compare changed case catalogs")
    previous = {x["case_id"]:x for x in b["result"]["details"]}
    current = {x["case_id"]:x for x in c["result"]["details"]}
    changes = [{"case_id":cid,"before":v["observed_action"],
                "after":current[cid]["observed_action"]}
               for cid,v in previous.items()
               if v["observed_action"] != current[cid]["observed_action"]]
    return {"baseline":baseline,"candidate":candidate,"changes":changes,
            "baseline_observed":b["result"]["observed"],
            "candidate_observed":c["result"]["observed"],
            "scientific_validity_established":False}

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("record")
    a.add_argument("--catalog", type=Path, required=True)
    a.add_argument("--observations", type=Path, required=True)
    a.add_argument("--ledger", type=Path, required=True)
    a.add_argument("--run-id", required=True)
    a.add_argument("--skill-commit", required=True)
    b = sub.add_parser("verify")
    b.add_argument("--ledger", type=Path, required=True)
    c = sub.add_parser("compare")
    c.add_argument("--ledger", type=Path, required=True)
    c.add_argument("--baseline", required=True)
    c.add_argument("--candidate", required=True)
    args = p.parse_args(argv)
    try:
        if args.command == "record":
            result = record(args.catalog, args.observations, args.ledger, args.run_id, args.skill_commit)
        elif args.command == "verify":
            result = {"verified_ledger_records":len(read_ledger(args.ledger)), "scientific_validity_established":False}
        else:
            result = compare(args.ledger, args.baseline, args.candidate)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
