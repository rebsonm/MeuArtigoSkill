#!/usr/bin/env python3
"""Commit an evidenced technical C.A.D.A. completion across three local files.

Explicit authorized WORK_FALLBACK only; uses a verified receipt from the
allowlisted local executor. Technical execution does not imply scientific
validity, researcher judgment, external provider access, or Drive sync.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from io import StringIO
import json
from pathlib import Path
import re
import sys

import cada_continuity_transaction as tx
from next_step_router import (EXECUTABLE, TERMINAL, clean, resolve,
                              pending_human_gate, next_eligible_task, upper)
from trace_execution import (ALLOWED_SCRIPTS, CANONICAL_ACTIONS, RECEIPTS,
                             file_state, sha256, trace_rows)

MGMT = tx.MGMT
TASKS = tx.FILES[0]
CONTINUITY = tx.FILES[1]
DASH = tx.FILES[2]
GATES = f"{MGMT}/18_Human_Validation_Gates.csv"
CONFIG = f"{MGMT}/PROJECT_CONFIG.json"
TRACE = f"{MGMT}/13_Traceability_Log.csv"


def parse_csv(path: Path, mandatory: str) -> tuple[list[str], list[dict]]:
    if path.is_symlink() or not path.is_file():
        raise ValueError("CANONICAL_CSV_MISSING_OR_UNSAFE")
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        if mandatory not in headers or len(headers) != len(set(headers)):
            raise ValueError("INVALID_CANONICAL_CSV_HEADER")
        rows = list(reader)
    if any(None in row or any(isinstance(v, (list, dict)) for v in row.values()) for row in rows):
        raise ValueError("MALFORMED_CANONICAL_CSV_ROW")
    return headers, rows


def encode_csv(headers: list[str], rows: list[dict]) -> bytes:
    memory = StringIO(newline="")
    writer = csv.DictWriter(memory, fieldnames=headers, extrasaction="raise", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return memory.getvalue().encode("utf-8-sig")


def confirm_local_execution(root: Path, trace_id: str, cada_id: str,
                            task: dict) -> tuple[str, dict]:
    """Check only local operational provenance, not semantic task success."""
    if not re.fullmatch(r"TRACE-\d{4,}", trace_id):
        raise ValueError("INVALID_TRACE_ID")
    trace_file = root / TRACE
    if trace_file.is_symlink() or not trace_file.is_file():
        raise ValueError("CANONICAL_TRACE_MISSING")
    rows = [row for row in trace_rows(root) if clean(row.get("Trace_ID")) == trace_id]
    if len(rows) != 1:
        raise ValueError("TRACE_ID_MISSING_OR_AMBIGUOUS")
    trace = rows[0]
    if (upper(trace.get("Status")) != "CONFIRMED"
            or clean(trace.get("CADA_ID")) != cada_id
            or clean(trace.get("Scientific_stage")) != clean(task.get("Scientific_stage"))
            or clean(trace.get("Action_type")) not in set(CANONICAL_ACTIONS.values())):
        raise ValueError("TRACE_NOT_CONFIRMED_FOR_THIS_TASK")

    proof = dict(pair.split("=", 1) for pair in
                 clean(trace.get("Reproducibility_information")).split(";")
                 if "=" in pair)
    receipt_rel = f"{RECEIPTS}/{trace_id}.json"
    expected_sha = proof.get("sha256", "")
    if proof.get("receipt") != receipt_rel or not re.fullmatch(r"[a-f0-9]{64}", expected_sha):
        raise ValueError("TRACE_RECEIPT_REFERENCE_INVALID")
    path = root / receipt_rel
    if path.is_symlink() or not path.is_file() or sha256(path) != expected_sha:
        raise ValueError("TRACE_RECEIPT_MISSING_OR_CHANGED")
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError, UnicodeError) as exc:
        raise ValueError("TRACE_RECEIPT_UNREADABLE") from exc
    if (not isinstance(receipt, dict) or receipt.get("trace_id") != trace_id
            or receipt.get("status") != "CONFIRMED" or receipt.get("exit_code") != 0
            or receipt.get("timed_out")
            or receipt.get("script") not in ALLOWED_SCRIPTS
            or clean(trace.get("Action_type")) != CANONICAL_ACTIONS[receipt["script"]]
            or receipt.get("inputs_before") != receipt.get("inputs_after")):
        raise ValueError("TRACE_RECEIPT_DOES_NOT_CONFIRM_LOCAL_EXECUTION")
    outputs_before, outputs_after = receipt.get("outputs_before"), receipt.get("outputs_after")
    if (not isinstance(outputs_before, list) or not isinstance(outputs_after, list)
            or not outputs_after or len(outputs_before) != len(outputs_after)
            or outputs_before == outputs_after):
        raise ValueError("TRACE_NO_CHANGED_OUTPUT_ARTIFACT")
    expected_artifact = clean(task.get("Related_artifact")).replace("\\", "/").rstrip("/")
    if not expected_artifact or ".." in Path(expected_artifact).parts or expected_artifact.startswith("/"):
        raise ValueError("TASK_REQUIRES_SAFE_RELATED_ARTIFACT")
    matched = False
    for item in outputs_after:
        if not isinstance(item, dict) or not item.get("exists"):
            raise ValueError("TRACE_OUTPUT_EVIDENCE_MISSING")
        relative = clean(item.get("path"))
        if relative == expected_artifact or relative.startswith(expected_artifact + "/"):
            matched = True
        if file_state(root, relative) != item:
            raise ValueError("TRACE_OUTPUT_CHANGED_AFTER_VERIFICATION")
    if not matched:
        raise ValueError("TRACE_OUTPUT_DOES_NOT_MATCH_CADA_ARTIFACT")
    return receipt_rel, receipt


def choose_next(rows: list[dict], gates: list[dict]) -> tuple[dict | None, str | None]:
    """Use the same conservative task/gate selection as the read-only router."""
    gate = pending_human_gate(gates)
    task, _ = next_eligible_task(rows, gate)
    return task, clean(gate.get("GATE_ID")) if gate else None


def update_continuity(text: str, *, previous: str, next_task: dict | None,
                      next_gate: str | None, trace_id: str, date: str) -> str:
    new_id = clean(next_task.get("CADA_ID")) if next_task else "NONE"
    new_action = (clean(next_task.get("Next_action")) if next_task
                  else f"Researcher scientific review pending: {next_gate}" if next_gate
                  else "No verified next action; review canonical project")
    owner = clean(next_task.get("Assigned_to")) if next_task else "RESEARCHER" if next_gate else "TO_DEFINE"
    due = clean(next_task.get("Deadline")) if next_task else ""
    replacements = {"CADA_ID": new_id, "Action": new_action,
                    "Owner": owner, "Due": due or "TO_DEFINE"}
    out = []
    inside = False
    replaced_ids = []
    heading = re.compile(r"^#{2,3}\s+")
    for line in text.splitlines(keepends=True):
        stripped = line.rstrip("\r\n")
        if heading.match(stripped):
            inside = bool(re.search(
                r"next valid action|pr[oó]xima a[cç][aã]o v[aá]lida",
                stripped, flags=re.IGNORECASE))
        updated = line
        if inside:
            m = re.fullmatch(r"(\s*-\s*)(CADA_ID|Action|Owner|Due):[ \t]*(.*)", stripped)
            if m:
                if m.group(2) == "CADA_ID":
                    replaced_ids.append(clean(m.group(3)))
                new_value = replacements[m.group(2)].replace("\r", " ").replace("\n", " ")
                updated = m.group(1) + m.group(2) + ": " + new_value
                updated += "\n" if line.endswith("\n") else ""
        out.append(updated)
    if not replaced_ids or any(record != previous for record in replaced_ids):
        raise ValueError("CONTINUITY_NEXT_ACTION_NOT_RECONCILED")
    # Keep every other paragraph intact. Do not manufacture a methodological
    # stage transition or scientific review by editing prose in bulk.
    message = (f"- {date} — Technical C.A.D.A. {previous} recorded DONE with "
               f"local {trace_id}; scientific gates unchanged.")
    # Existing 15. Change log is a durable provenance note; do not append
    # if the canonical template lacks the section.
    combined = "".join(out)
    match = re.search(r"(?m)^## 15\. Change log[^\n]*\n", combined)
    if match:
        before, after = combined[:match.end()], combined[match.end():]
        boundary = re.search(r"(?m)^## ", after)
        if boundary:
            history, remainder = after[:boundary.start()], after[boundary.start():]
        else:
            history, remainder = after, ""
        return before + history.rstrip("\n") + "\n" + message + "\n\n" + remainder
    return combined


def update_dashboard(headers: list[str], rows: list[dict], tasks: list[dict],
                     next_task: dict | None, next_gate: str | None,
                     complete_id: str, trace_id: str, date: str) -> list[dict]:
    if "Metric" not in headers or "Value" not in headers:
        raise ValueError("INVALID_CADA_DASHBOARD_SCHEMA")
    metrics = [clean(x.get("Metric")) for x in rows]
    if len(metrics) != len(set(metrics)):
        raise ValueError("AMBIGUOUS_CADA_DASHBOARD_METRIC")
    not_terminal = [task for task in tasks if upper(task.get("Status")) not in TERMINAL]
    values = {
        "Total_active_items": str(len(not_terminal)),
        "Ready_items": str(sum(upper(t.get("Status")) == "READY" for t in tasks)),
        "In_progress_items": str(sum(upper(t.get("Status")) == "IN_PROGRESS" for t in tasks)),
        "Waiting_items": str(sum(upper(t.get("Status")) == "WAITING" for t in tasks)),
        "Blocked_items": str(sum(upper(t.get("Status")) == "BLOCKED" for t in tasks)),
        "Done_items": str(sum(upper(t.get("Status")) in {"DONE", "COMPLETED"} for t in tasks)),
        "Next_CADA_ID": clean(next_task.get("CADA_ID")) if next_task else "",
        "Next_action": (clean(next_task.get("Next_action")) if next_task else
                        f"HUMAN_GATE_DECISION_REQUIRED:{next_gate}" if next_gate else
                        "REVIEW_REQUIRED"),
        "Next_owner": clean(next_task.get("Assigned_to")) if next_task else
                       "RESEARCHER" if next_gate else "",
        "Next_due": clean(next_task.get("Deadline")) if next_task else "",
        "Next_human_gate": next_gate or "",
        "Last_completed_CADA_ID": complete_id,
        "Last_trace_event": trace_id,
    }
    by_metric = {clean(x["Metric"]): x for x in rows}
    for key, value in values.items():
        if key not in by_metric:
            row = {h: "" for h in headers}
            row["Metric"] = key
            rows.append(row)
            by_metric[key] = row
        by_metric[key]["Value"] = value
        if "Last_updated" in headers:
            by_metric[key]["Last_updated"] = date
    return rows


def complete(root: Path, cada_id: str, trace_id: str) -> dict:
    root = Path(root).resolve()
    path = root / CONFIG
    if path.is_symlink() or not path.is_file():
        raise ValueError("PROJECT_CONFIG_MISSING")
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError, UnicodeError) as exc:
        raise ValueError("PROJECT_CONFIG_INVALID") from exc
    if (not isinstance(cfg, dict) or cfg.get("storage_mode") != "WORK_FALLBACK"
            or cfg.get("fallback_authorized") is not True):
        raise ValueError("LOCAL_WORK_FALLBACK_AUTHORIZATION_REQUIRED")
    if not re.fullmatch(r"CADA-\d{4,}", cada_id):
        raise ValueError("INVALID_CADA_ID")

    # Never compound an already broken C.A.D.A. state into a second
    # apparently successful transition. Legacy projects without a PR-49
    # completion marker are not grandfathered into an approval.
    from cada_continuity_integrity import audit as audit_continuity
    previous = audit_continuity(root)
    if previous["errors"]:
        raise ValueError("CADA_PREVIOUS_CONTINUITY_INTEGRITY_REVIEW_REQUIRED")

    # A verified next-step route must already permit technical preparation
    # for the *same* CADA_ID. This also enforces journal interlocks.
    current = resolve(root)
    if (current["status"] != "TECHNICAL_PREPARATION_AVAILABLE"
            or current["next_task_id"] != cada_id or current["blockers"]):
        raise ValueError("CADA_NEXT_ACTION_NOT_AUTHORIZED_OR_RECONCILED")

    task_headers, tasks = parse_csv(root / TASKS, "CADA_ID")
    dash_headers, dashboard = parse_csv(root / DASH, "Metric")
    gate_headers, gates = parse_csv(root / GATES, "GATE_ID")
    candidates = [t for t in tasks if clean(t.get("CADA_ID")) == cada_id]
    if len(candidates) != 1:
        raise ValueError("CADA_ID_MISSING_OR_AMBIGUOUS")
    task = candidates[0]
    if upper(task.get("Status")) not in EXECUTABLE:
        raise ValueError("CADA_TASK_NOT_ELIGIBLE_FOR_COMPLETION")
    receipt_rel, _ = confirm_local_execution(root, trace_id, cada_id, task)

    date = datetime.now(timezone.utc).date().isoformat()
    task["Status"] = "DONE"
    task["Completion_evidence"] = f"{trace_id};receipt={receipt_rel}"
    if "Evidence_of_progress" in task:
        task["Evidence_of_progress"] = f"Local artifact confirmed by {trace_id}"
    task["Last_updated"] = date

    candidate, gate_id = choose_next(tasks, gates)
    continuity_path = root / CONTINUITY
    if continuity_path.is_symlink() or not continuity_path.is_file():
        raise ValueError("CANONICAL_CONTINUITY_MISSING")
    continuity_before = continuity_path.read_text(encoding="utf-8")
    continuity_after = update_continuity(
        continuity_before, previous=cada_id, next_task=candidate,
        next_gate=gate_id, trace_id=trace_id, date=date)
    dashboard = update_dashboard(dash_headers, dashboard, tasks, candidate,
                                 gate_id, cada_id, trace_id, date)

    tx.apply(root, {
        TASKS: encode_csv(task_headers, tasks),
        CONTINUITY: continuity_after.encode("utf-8"),
        DASH: encode_csv(dash_headers, dashboard),
    })
    # TRACE + its receipt already exist; never forge another TRACE/GATE.
    return {
        "status": "OPERATIONAL_COMPLETION_RECORDED",
        "cada_id": cada_id,
        "trace_id": trace_id,
        "next_cada_id": clean(candidate.get("CADA_ID")) if candidate else None,
        "next_gate_id": gate_id,
        "scientific_gate_approved": False,
        "scientific_result_validated": False,
        "drive_sync_verified": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--cada-id")
    parser.add_argument("--trace-id")
    parser.add_argument("--recover-pending", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.recover_pending:
            result = tx.recover(args.project)
        else:
            if not args.cada_id or not args.trace_id:
                raise ValueError("CADA_AND_CONFIRMED_TRACE_REQUIRED")
            result = complete(args.project, args.cada_id, args.trace_id)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, RuntimeError, csv.Error) as exc:
        # No private research notes, subprocess output or credentials.
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
