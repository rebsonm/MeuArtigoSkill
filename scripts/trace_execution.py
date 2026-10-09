#!/usr/bin/env python3
"""Capture real local script executions and audit TRACE evidence receipts.

Free, offline, stdlib-only. This is an execution recorder, not a verifier
of scientific truth or proof that a third-party service was queried.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from governance_events import TRACE_FILE, TRACE_HEADERS, append, next_trace

MGMT = "00_Gestao_e_Continuidade"
RECEIPTS = f"{MGMT}/TRACE_RECEIPTS"
SCRIPTS_ROOT = Path(__file__).resolve().parent
ALLOWED_SCRIPTS = {
    "verify_sources.py": True,
    "validate_project.py": True,
    "dedupe_records.py": False,
}
CANONICAL_ACTIONS = {
    "verify_sources.py": "LOCAL_SOURCE_VERIFICATION",
    "validate_project.py": "LOCAL_PROJECT_VALIDATION",
    "dedupe_records.py": "LOCAL_DEDUPLICATION",
}
STATUSES = {"CONFIRMED", "UNVERIFIED", "PARTIAL", "FAILED"}
MAX_FILE_SIZE = 100 * 1024 * 1024


def timestamp():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256(path):
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def safe_file(root, relative):
    """Require an existing or prospective file under the project root."""
    if not relative or "://" in relative:
        raise ValueError("Expected a project-relative file path")
    path = (root / relative).resolve()
    if path == root or not path.is_relative_to(root):
        raise ValueError("File path escapes the project workspace")
    return path


def file_state(root, relative):
    file = safe_file(root, relative)
    if not file.exists():
        return {"path": file.relative_to(root).as_posix(), "exists": False}
    if not file.is_file():
        raise ValueError("Expected a regular file: " + relative)
    if file.stat().st_size > MAX_FILE_SIZE:
        raise ValueError("File exceeds the recording size limit: " + relative)
    return {
        "path": file.relative_to(root).as_posix(), "exists": True,
        "bytes": file.stat().st_size, "sha256": sha256(file)
    }


def trace_rows(root):
    trace = root / TRACE_FILE
    if not trace.is_file():
        return []
    with trace.open("r", newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def write_trace(root, record):
    trace = root / TRACE_FILE
    trace.parent.mkdir(parents=True, exist_ok=True)
    # Only the existing canonical columns and TRACE IDs are used.
    append(trace, TRACE_HEADERS, record)


def base_row(tid, args, status, *, verification="", reproducibility="", artifact="", note=""):
    return {
        "Trace_ID": tid, "Timestamp": timestamp(),
        "Scientific_stage": args.stage, "CADA_ID": args.cada_id,
        "Actor": "SCRIPT" if status != "UNVERIFIED" else "OTHER",
        "AI_platform_or_tool": getattr(args, "script", "") or "",
        "Action_type": args.action, "Action_summary": args.summary,
        "Input_or_source": "Executed allowlisted script" if status != "UNVERIFIED" else "Unverified declaration",
        "Decision_or_output": status,
        "Artifact_after": artifact,
        "Verification_method": verification,
        "Reproducibility_information": reproducibility,
        "Materiality": args.materiality,
        "Status": status, "Notes": note,
    }


def run_script(args):
    root = Path(args.project).resolve()
    script = args.script
    if script not in ALLOWED_SCRIPTS:
        raise ValueError("Script is not on the execution allowlist")
    script_path = (SCRIPTS_ROOT / script).resolve()
    if not script_path.is_file() or not script_path.is_relative_to(SCRIPTS_ROOT):
        raise ValueError("Executable script is not available")

    argv = list(args.script_args)
    if argv and argv[0] == "--":
        argv = argv[1:]
    # No shell or generic command execution.
    command = [sys.executable, str(script_path)]
    if ALLOWED_SCRIPTS[script]:
        command.append(str(root))
    command.extend(argv)
    # The recorder—not the language model—sets the action associated with a
    # confirmed execution. Callers cannot attest an unrelated external search.
    args.action = CANONICAL_ACTIONS[script]
    if script != "validate_project.py" and not args.outputs:
        raise ValueError("This script requires explicit expected output artifacts")
    if script == "dedupe_records.py":
        if "--out-dir" not in argv or argv.index("--out-dir") + 1 >= len(argv):
            raise ValueError("Deduplication requires an output directory inside the workspace")
        output_dir = (root / argv[argv.index("--out-dir") + 1]).resolve()
        if not output_dir.is_relative_to(root):
            raise ValueError("Deduplication output directory must remain inside the workspace")
    if not root.is_dir():
        raise ValueError("Project folder not found")
    for field in args.inputs + args.outputs:
        safe_file(root, field)
    # Collect genuine before-state (not a model-supplied digest).
    before = [file_state(root, field) for field in args.inputs]
    outputs_before = [file_state(root, field) for field in args.outputs]
    start = timestamp()
    timed_out = False
    stdout_hash = stderr_hash = ""
    try:
        completed = subprocess.run(
            command, cwd=str(root), capture_output=True,
            timeout=150, check=False
        )
        returncode = completed.returncode
        stdout_hash = hashlib.sha256(completed.stdout).hexdigest()
        stderr_hash = hashlib.sha256(completed.stderr).hexdigest()
    except subprocess.TimeoutExpired as exc:
        returncode = 124
        timed_out = True
        stdout_hash = hashlib.sha256(exc.stdout or b"").hexdigest()
        stderr_hash = hashlib.sha256(exc.stderr or b"").hexdigest()
    outputs_after = [file_state(root, field) for field in args.outputs]
    inputs_after = [file_state(root, field) for field in args.inputs]

    outputs_exist = all(entry["exists"] for entry in outputs_after)
    outputs_changed = any(a != b for a, b in zip(outputs_before, outputs_after))
    inputs_stable = before == inputs_after
    if returncode != 0:
        status = "FAILED"
    elif not outputs_exist or (args.outputs and not outputs_changed) or not inputs_stable:
        status = "PARTIAL"
    else:
        status = "CONFIRMED"

    tid = next_trace(root)
    receipt = {
        "schema_version": 1,
        "trace_id": tid,
        "recorded_at": timestamp(),
        "started_at": start,
        "status": status,
        "script": script,
        "script_sha256": sha256(script_path),
        # Do not store raw argv or stdout: they can contain secrets or copyrighted data.
        "arguments_sha256": hashlib.sha256(json.dumps(argv, ensure_ascii=False).encode("utf-8")).hexdigest(),
        "exit_code": returncode, "timed_out": timed_out,
        "stdout_sha256": stdout_hash, "stderr_sha256": stderr_hash,
        "inputs_before": before, "inputs_after": inputs_after,
        "outputs_before": outputs_before, "outputs_after": outputs_after,
        "limits": "Confirms a local script execution only, not an external service result or scientific conclusion.",
    }
    relative = f"{RECEIPTS}/{tid}.json"
    receipt_path = safe_file(root, relative)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    with receipt_path.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    receipt_hash = sha256(receipt_path)
    proof = f"receipt={relative};sha256={receipt_hash}"
    row = base_row(
        tid, args, status,
        verification="CAPTURED_SUBPROCESS_EXIT_AND_ARTIFACT_HASHES",
        reproducibility=proof,
        artifact=";".join(x["path"] for x in outputs_after if x["exists"]),
        note="Local execution only. Third-party data and interpretation require separate verification.",
    )
    write_trace(root, row)
    print(json.dumps({"trace_id": tid, "status": status, "receipt": relative,
                      "exit_code": returncode}, ensure_ascii=False))
    return 0 if status == "CONFIRMED" else 2 if status == "PARTIAL" else 1


def declare(args):
    root = Path(args.project).resolve()
    if not root.is_dir():
        raise ValueError("Project folder not found")
    tid = next_trace(root)
    row = base_row(
        tid, args, "UNVERIFIED", verification="DECLARATION_ONLY",
        note="No direct executable or trusted provider receipt was captured. Never count as a confirmed event.",
    )
    write_trace(root, row)
    print(json.dumps({"trace_id": tid, "status": "UNVERIFIED"}, ensure_ascii=False))
    return 0


def audit_receipts(root, *, strict=False):
    root = Path(root).resolve()
    errors, warnings = [], []
    counts = {"confirmed": 0, "unverified": 0, "legacy_complete": 0, "partial": 0, "failed": 0}
    for row in trace_rows(root):
        tid = (row.get("Trace_ID") or "").strip()
        status = (row.get("Status") or "").strip().upper()
        if status == "COMPLETE":
            counts["legacy_complete"] += 1
            (errors if strict else warnings).append(f"{tid}: legacy COMPLETE without machine receipt")
            continue
        if status == "UNVERIFIED":
            counts["unverified"] += 1
            continue
        if status in {"PARTIAL", "FAILED"}:
            counts[status.lower()] += 1
            continue
        if status != "CONFIRMED":
            continue
        counts["confirmed"] += 1
        proof = (row.get("Reproducibility_information") or "").strip()
        kv = dict(token.split("=", 1) for token in proof.split(";") if "=" in token)
        rel, expected = kv.get("receipt", ""), kv.get("sha256", "")
        if not rel or len(expected) != 64:
            errors.append(f"{tid}: confirmed without a complete receipt reference")
            continue
        try:
            receipt_path = safe_file(root, rel)
            if not receipt_path.is_file() or sha256(receipt_path) != expected:
                errors.append(f"{tid}: receipt missing or modified")
                continue
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            if receipt.get("trace_id") != tid or receipt.get("status") != "CONFIRMED" or receipt.get("exit_code") != 0:
                errors.append(f"{tid}: receipt does not substantiate a completed execution")
                continue
            if receipt.get("script") not in ALLOWED_SCRIPTS:
                errors.append(f"{tid}: unrecognized script in receipt")
                continue
            if receipt.get("script_sha256") != sha256(SCRIPTS_ROOT / receipt["script"]):
                warnings.append(f"{tid}: source code changed since execution; retain versioned script for reproduction")
            if not receipt.get("inputs_before") == receipt.get("inputs_after"):
                errors.append(f"{tid}: execution changed input files unexpectedly")
            before = receipt.get("outputs_before") or []
            after = receipt.get("outputs_after") or []
            if len(before) != len(after) or not all(x.get("exists") for x in after) or (after and before == after):
                errors.append(f"{tid}: output evidence is missing or unchanged")
            for item in after:
                current = file_state(root, item.get("path") or "")
                if current != item:
                    errors.append(f"{tid}: recorded output is missing or no longer matches its receipt")
        except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            errors.append(f"{tid}: unreadable or unsafe receipt ({type(exc).__name__})")
    return {"counts": counts, "errors": errors, "warnings": warnings}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="command", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("project")
    common.add_argument("--stage", default="")
    common.add_argument("--cada-id", default="")
    common.add_argument("--action", required=True)
    common.add_argument("--summary", required=True)
    common.add_argument("--materiality", default="ADMINISTRATIVE",
                        choices=["ADMINISTRATIVE", "ASSISTIVE", "SUBSTANTIVE", "NOT_APPLICABLE"])
    run = actions.add_parser("run", parents=[common])
    run.add_argument("--script", required=True, choices=sorted(ALLOWED_SCRIPTS))
    run.add_argument("--input", dest="inputs", action="append", default=[])
    run.add_argument("--output", dest="outputs", action="append", default=[])
    run.add_argument("script_args", nargs=argparse.REMAINDER)
    dec = actions.add_parser("declare", parents=[common])
    audit = actions.add_parser("audit")
    audit.add_argument("project")
    audit.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "run":
            return run_script(args)
        if args.command == "declare":
            return declare(args)
        result = audit_receipts(Path(args.project), strict=args.strict)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result["errors"] else 0
    except (OSError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
