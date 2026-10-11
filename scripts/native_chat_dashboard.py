#!/usr/bin/env python3
"""Read-only, presentation-neutral snapshot for ChatGPT-native research panels.

The host (not this script) decides whether to render native UI cards, tables
or a textual fallback. No external hosted service, network, or project mutation is used.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from presentation_mode import read_config
from next_step_router import (TERMINAL, documented_gate, resolve as resolve_next_step)
from cada_continuity_integrity import audit as audit_cada_continuity

MGMT = "00_Gestao_e_Continuidade"
FILES = {
    "tasks": "11_CADA_Control.csv",
    "gates": "18_Human_Validation_Gates.csv",
    "evidence": "05_Evidence_Matrix.csv",
    "claims": "09_Claims_Ledger.csv",
    "trace": "13_Traceability_Log.csv",
    "sync": "12_PM_Sync.csv",
}
def text(value: object, max_length: int = 80) -> str:
    """Limit presentation of technical IDs and state fields only."""
    return str(value or "").strip()[:max_length]


def norm(value: object) -> str:
    return text(value).upper()


def read_table(folder: Path, filename: str) -> list[dict[str, str]] | None:
    file = folder / filename
    if file.is_symlink() or not file.is_file():
        return None
    with file.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        if not headers or len(headers) != len(set(headers)):
            return None
        rows = list(reader)
    # A malformed CSV must not silently become a plausible scientific count.
    return None if any(None in row for row in rows) else rows


def nrows(items: list[dict[str, str]] | None) -> int | None:
    return None if items is None else len(items)


def report_indicator(root: Path) -> str:
    """Report *presence*, not independent verification or science approval."""
    file = root / MGMT / "SOURCE_VERIFICATION.json"
    if not file.is_file():
        return "MISSING"
    try:
        data = json.loads(file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeError):
        return "UNREADABLE"
    if not isinstance(data, dict) or not isinstance(data.get("checks"), list):
        return "UNREADABLE"
    return "PRESENT_NOT_AUDITED"


def panel(root: Path, *, mode: str | None = None) -> dict:
    root = Path(root).resolve()
    # One read of canonical config: do not recompute a second, raw "next"
    # from the legacy presentation layer or read private next-action prose.
    config = read_config(root)
    saved_mode = config.get("presentation_mode", "FULL")
    if saved_mode not in {"MINIMAL", "FULL"}:
        raise ValueError("Unsupported saved presentation mode")
    chosen = norm(mode or saved_mode)
    if chosen not in {"MINIMAL", "FULL"}:
        raise ValueError("Unsupported presentation mode")
    folder = root / MGMT
    tables = {key: read_table(folder, filename) for key, filename in FILES.items()}
    tasks, gates = tables["tasks"], tables["gates"]
    active = [] if tasks is None else [
        row for row in tasks if norm(row.get("Status")) not in TERMINAL
    ]
    gate_items = [] if gates is None else [{
        "id": text(row.get("GATE_ID"), 40),
        "status": norm(row.get("Status")),
        "decision_recorded": norm(row.get("Decision")) or None,
        "approval_documented": documented_gate(row),
        "independently_scientifically_validated": False,
    } for row in gates]
    # Canonical CSV schema (init_project.py): CADA_ID, Title, Assigned_to,
    # Deadline. The separate Excel workbook uses Task/Owner; accept those
    # names only as compatibility aliases for legacy imports. Never use
    # Next_action as the task title or derive a missing responsible person.
    # Status stays internal for counts and selecting the next useful rows.
    def compact_task(row: dict[str, str]) -> dict:
        return {
            "id": text(row.get("CADA_ID"), 40) or None,
            "task": text(row.get("Title") or row.get("Task"), 180) or None,
            "execution_owner": text(row.get("Assigned_to") or row.get("Owner"), 100) or None,
            "deadline": text(row.get("Deadline"), 40) or None,
        }
    task_items = [] if tasks is None else [compact_task(row) for row in tasks]
    active_task_items = [compact_task(row) for row in active]
    # Only the established router decides the next eligible task/gate;
    # task-row order and the raw gate Status alone are not authoritative.
    navigation = resolve_next_step(root)
    integrity = audit_cada_continuity(root)
    # Do not advertise a technical action when the last evidenced
    # completion conflicts with the actual canonical registers.
    if integrity["errors"]:
        navigation["status"] = "CADA_CONTINUITY_INTEGRITY_REVIEW"
        navigation["technical_preparation_possible"] = False
        navigation["blockers"] = sorted(set(
            navigation["blockers"] + ["CADA_CONTINUITY_INTEGRITY_REVIEW"]))
    # MINIMAL lists the actual eligible task first, if present, so a
    # BLOCKED/CAPTURED row cannot conceal it beyond the first three rows.
    active_for_minimal = active_task_items if active_task_items else task_items
    eligible_id = navigation["next_task_id"]
    priority = next((item for item in active_for_minimal
                     if item["id"] == eligible_id), None)
    minimal_tasks = ([priority] if priority else []) + [
        item for item in active_for_minimal if item is not priority
    ][:3 - bool(priority)]
    counts = {
        "registered_tasks": nrows(tasks),
        "tasks_reported_done": None if tasks is None else sum(
            norm(row.get("Status")) in {"DONE", "COMPLETED"} for row in tasks),
        "active_tasks": None if tasks is None else len(active),
        "gates": nrows(gates),
        "documented_gate_approvals": None if gates is None else sum(
            x["approval_documented"] for x in gate_items),
    }
    # Task titles and execution assignees come from the authorized project.
    # Never expose unrelated notes, source paths, protected text or review excerpts.
    return {
        "schema": "MEU_ARTIGO_NATIVE_PANEL_V1",
        "mode": chosen,
        "project_storage_recorded": text(config.get("storage_mode"), 40) or "UNKNOWN",
        "drive_sync_verified_in_this_session": False,
        "scientific_quality_independently_validated": False,
        "overview": {
            **counts,
            # Backwards-compatible field names, now safe aliases of the
            # single authoritative continuation classifier.
            "next_task_id": navigation["next_task_id"],
            "next_gate_id": navigation["next_gate_id"],
            "scientific_progress_percentage": None,
        },
        "continuation": {
            "status": navigation["status"],
            "next_task_id": navigation["next_task_id"],
            "next_gate_id": navigation["next_gate_id"],
            "requires_human_decision": navigation["requires_human_decision"],
            "technical_preparation_possible": navigation["technical_preparation_possible"],
            "blockers": navigation["blockers"],
            "continuity_document_read": navigation["continuity_document_read"],
            "integrity_status": integrity["status"],
            "integrity_error_count": len(integrity["errors"]),
            "last_operational_proof_checked": integrity["last_operational_proof_checked"],
            "scientific_gate_approved_by_navigation": False,
            "drive_sync_verified_in_this_session": False,
        },
        "tasks": {
            "items": (minimal_tasks if chosen == "MINIMAL" else task_items),
            "registered_total": nrows(tasks),
            "items_partial": chosen == "MINIMAL" and len(minimal_tasks) < len(task_items),
        },
        "gates": {
            "items": (gate_items[:3] if chosen == "MINIMAL" else gate_items),
            "registered_total": nrows(gates),
            "items_partial": chosen == "MINIMAL" and len(gate_items) > 3,
        },
        "evidence": {
            "registered_evidence_rows": nrows(tables["evidence"]),
            "registered_claims": nrows(tables["claims"]),
            "source_report_presence": report_indicator(root),
            "verified_sources": None,
            "blocking_conflicts": None,
            "pending_human_reviews": None,
        },
        "history_sync": {
            "registered_trace_events": nrows(tables["trace"]),
            "registered_sync_records": nrows(tables["sync"]),
            "drive_sync_verified_in_this_session": False,
        },
        "missing_registers": [FILES[key] for key, value in tables.items() if value is None],
        "limitations": [
            "A native chat panel is a read-only presentation of recorded state.",
            "Recorded approvals do not independently authenticate human scientific review.",
            "Report presence does not establish integrity; perform the actual source audit.",
            "Local mirror does not prove synchronization with the canonical Google Drive.",
        ],
    }


def task_table(data: dict) -> str:
    """Exactly four visual columns, even in plain-text fallback.

    The caller is responsible for supplying an authorized project; sensitive
    project descriptions must not be sent to a third-party public display.
    """
    tasks = data["tasks"]
    cols = ("ID Tarefa", "Tarefa", "Responsável execução", "Prazo")
    if tasks["registered_total"] is None:
        return "C.A.D.A.: canonical task register unavailable"
    if not tasks["items"]:
        return "C.A.D.A.: no tasks in the selected view"
    lines = [" | ".join(cols), " | ".join("---" for _ in cols)]
    for item in tasks["items"]:
        values = [item["id"], item["task"], item["execution_owner"], item["deadline"]]
        # Keep record values literal but escape table delimiters/newlines.
        cells = [str(value or "Not recorded").replace("|", r"\|").replace("\n", " ") for value in values]
        lines.append(" | ".join(cells))
    return "\n".join(lines)


def fallback(data: dict) -> str:
    """Plain-text fallback for hosts without native visual presentation."""
    overview = data["overview"]
    evidence = data["evidence"]
    history = data["history_sync"]
    return "\n".join([
        "Meu Artigo - recorded project state (not scientific validation)",
        "Presentation mode: " + data["mode"],
        "Tasks recorded / active: " + str(overview["registered_tasks"]) +
        " / " + str(overview["active_tasks"]),
        task_table(data),
        "Human approvals documented: " + str(overview["documented_gate_approvals"]),
        "Next step: " + data["continuation"]["status"] +
        " | C.A.D.A.: " + str(data["continuation"]["next_task_id"]) +
        " | human gate: " + str(data["continuation"]["next_gate_id"]),
        "First blocker: " + (data["continuation"]["blockers"][0]
                             if data["continuation"]["blockers"] else "None recorded"),
        "Evidence / claims recorded: " + str(evidence["registered_evidence_rows"]) +
        " / " + str(evidence["registered_claims"]),
        "Source verification report: " + evidence["source_report_presence"],
        "Trace/sync entries: " + str(history["registered_trace_events"]) +
        " / " + str(history["registered_sync_records"]),
        "Google Drive sync verified: NO (this session)",
    ])


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("project", help="Existing authorized local project")
    p.add_argument("--mode", choices=["MINIMAL", "FULL"])
    p.add_argument("--format", choices=["json", "text"], default="text")
    args = p.parse_args(argv)
    try:
        output = panel(Path(args.project), mode=args.mode)
    except (OSError, ValueError, csv.Error, UnicodeError, json.JSONDecodeError) as exc:
        print("ERROR: cannot read native panel: " + type(exc).__name__, file=sys.stderr)
        return 1
    print(json.dumps(output, ensure_ascii=False, indent=2) if args.format == "json"
          else fallback(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
