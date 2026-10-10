#!/usr/bin/env python3
"""Read-only, evidence-aware view of the canonical Meu Artigo project.

The view is derived afresh from canonical CSV/JSON files. It is NOT an
independent workspace or a scientific validation/certification.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

from source_report_integrity import assess as assess_source_report

MGMT = "00_Gestao_e_Continuidade"
FILES = {
    "tasks": "11_CADA_Control.csv",
    "gates": "18_Human_Validation_Gates.csv",
    "searches": "02_Search_Log.csv",
    "records": "03_Screening.csv",
    "evidence": "05_Evidence_Matrix.csv",
    "claims": "09_Claims_Ledger.csv",
    "trace": "13_Traceability_Log.csv",
    "ai": "14_AI_Use_Log.csv",
    "sync": "12_PM_Sync.csv",
    "submissions": "10_Submission_Checklist.csv",
}
TERMINAL = {"DONE", "CANCELLED", "CANCELED", "SUPERSEDED"}
APPROVALS = {"APPROVED", "APPROVED_WITH_CHANGES"}
PRIORITY = {"CRITIQUE": 0, "CRITICAL": 0, "HIGH": 1, "AVERAGE": 2, "MEDIUM": 2, "LOW": 3}
ACTIONABLE = {"IN_PROGRESS": 0, "READY": 1, "ASSIGNED": 2, "CAPTURED": 3}
EXTERNAL_SUCCESS = {"CONFIRMED", "COMPLETE"}  # Reported statuses only, never independent proof.

def short(value: object, limit: int = 180) -> str:
    """Bound text exposed in the panel, preserving the original file unchanged."""
    return str(value or "").strip()[:limit]

def csv_rows(base: Path, name: str) -> list[dict[str, str]] | None:
    path = base / FILES[name]
    if not path.is_file():
        return None
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def norm(value: object) -> str:
    return str(value or "").strip().upper()

def metric(rows: list[dict[str, str]] | None) -> int | None:
    return None if rows is None else len(rows)

def gate_is_documented(gate: dict[str, str]) -> bool:
    """Registered approval, not proof of identity or scientific validity."""
    return (norm(gate.get("Status")) == "COMPLETED"
            and norm(gate.get("Decision")) in APPROVALS
            and bool(short(gate.get("Validated_by")))
            and bool(short(gate.get("Validation_evidence"))))

def parse_due(value: str) -> date | None:
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None

def task_key(task: dict[str, str], today: date) -> tuple:
    due = parse_due(task.get("Deadline", ""))
    return (ACTIONABLE.get(norm(task.get("Status")), 9),
            PRIORITY.get(norm(task.get("Priority")), 4),
            due or date.max, short(task.get("CADA_ID")))

def view(project: Path, *, today: date | None = None, mode: str | None = None) -> dict:
    """Pure read-only projection. Caller must choose an authorized project root."""
    today = today or date.today()
    root = Path(project).resolve()
    cfg_path = root / MGMT / "PROJECT_CONFIG.json"
    if not cfg_path.is_file():
        raise ValueError("Canonical PROJECT_CONFIG.json not found; no demo data substituted")
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    if not isinstance(cfg, dict):
        raise ValueError("Invalid canonical project configuration")
    storage = norm(cfg.get("storage_mode"))
    storage_state = norm(cfg.get("storage_state"))
    if storage not in {"GOOGLE_DRIVE", "GOOGLE_DRIVE_STAGING", "WORK_FALLBACK"}:
        # Legacy workspaces are viewable but lack verified storage configuration.
        storage = "UNKNOWN"
    if mode is None:
        mode = norm(cfg.get("presentation_mode") or "FULL")
    mode = norm(mode)
    if mode not in {"MINIMAL", "FULL"}:
        raise ValueError("presentation mode must be MINIMAL or FULL")

    base = root / MGMT
    tables = {key: csv_rows(base, key) for key in FILES}
    # Read-only integrity check; do not expose paths, DOI or source passages.
    source_state = assess_source_report(root, require_complete=True)
    source_public = {key: source_state[key] for key in (
        "status", "checked", "pending_review", "blocked", "reviewed_limitations",
        "editorial_retraction_alerts", "editorial_correction_alerts",
        "editorial_updates", "provider_warnings", "report_missing", "report_stale")}
    tasks = tables["tasks"]
    gates = tables["gates"]
    active = [] if tasks is None else [t for t in tasks if norm(t.get("Status")) not in TERMINAL]
    available = sorted((t for t in active if norm(t.get("Status")) in ACTIONABLE), key=lambda t: task_key(t, today))
    current = available[0] if available else None

    scope = [] if tasks is None else [t for t in tasks if norm(t.get("Status")) not in {"CANCELLED", "CANCELED", "SUPERSEDED"}]
    done = None if tasks is None else sum(norm(t.get("Status")) == "DONE" for t in scope)
    percentage = None if not scope else round(100 * (done or 0) / len(scope))
    overdue = None if tasks is None else sum(
        1 for t in active if (parse_due(t.get("Deadline", "")) or date.max) < today
    )
    blocked = None if tasks is None else sum(norm(t.get("Status")) == "BLOCKED" for t in active)
    with_proof = None if tasks is None else sum(
        norm(t.get("Status")) == "DONE" and bool(short(t.get("Completion_evidence"))) for t in scope
    )

    rows_gates = [] if gates is None else [{
        "id": short(g.get("GATE_ID"), 40), "name": short(g.get("Name")),
        "stage": short(g.get("Scientific_stage"), 40),
        "status": short(g.get("Status"), 40),
        "decision": short(g.get("Decision"), 50),
        "documented_approval": gate_is_documented(g)
    } for g in gates]
    ready_gates = [g for g in rows_gates if g["status"].upper() == "READY"]
    # Gate is never shown as "approved" without decision, validator and evidence recorded.
    for gate in rows_gates:
        if gate["id"] == "GATE-0006":
            gate["source_controls_status"] = source_public["status"]
            gate["approval_with_open_source_controls"] = (
                gate["documented_approval"]
                and source_public["status"] not in {"RECORDED_CLEAR", "REVIEWED_LIMITATIONS"})
    approved_gates = sum(g["documented_approval"] for g in rows_gates) if gates is not None else None

    task_view = lambda t: {
        "id": short(t.get("CADA_ID"), 40), "title": short(t.get("Title")),
        "action": short(t.get("Next_action")) or short(t.get("Title")),
        "owner": short(t.get("Assigned_to"), 80),
        "status": short(t.get("Status"), 40), "priority": short(t.get("Priority"), 40),
        "deadline": short(t.get("Deadline"), 40),
        "deadline_type": short(t.get("Deadline_type"), 40),
        "blocker": short(t.get("Blocker")),
        "completion_evidence_recorded": bool(short(t.get("Completion_evidence")))
    }
    search_rows = tables["searches"]
    search_reported = None if search_rows is None else sum(
        norm(s.get("Status")) in EXTERNAL_SUCCESS for s in search_rows
    )
    trace = tables["trace"]
    ai_rows = tables["ai"]
    ai_review_pending = None if ai_rows is None else sum(
        norm(a.get("Materiality")) == "SUBSTANTIVE"
        and norm(a.get("Human_decision")) not in {"ACCEPTED", "MODIFIED", "REJECTED"}
        for a in ai_rows
    )
    claims = tables["claims"]
    needs_claim_review = None if claims is None else sum(
        norm(c.get("Human_validation")) not in {"VALIDATED", "REVISED", "REJECTED"}
        or norm(c.get("Robustness_status")) in {"NOT_AUDITED", "REVISE", "REJECT", ""}
        for c in claims
    )
    sync_rows = tables["sync"]
    sync_conflicts = None if sync_rows is None else sum(bool(short(s.get("Conflict"))) and norm(s.get("Conflict")) not in {"NONE", "NO", "FALSE"} for s in sync_rows)

    result = {
        "schema": "meu-artigo-visual/v1",
        "mode": mode,
        "project": {
            "title": short(cfg.get("project_name") or cfg.get("project_title") or cfg.get("title") or root.name),
            "method_route": short(cfg.get("method_route") or cfg.get("research_route") or "UNDECIDED", 60),
            "storage_mode": storage,
            "storage_state": storage_state or "UNKNOWN",
            "storage_verified_in_this_session": False,
        },
        "operational": {
            "tasks_total": len(scope) if tasks is not None else None,
            "tasks_done_reported": done,
            "tasks_done_with_evidence_recorded": with_proof,
            "tasks_active": len(active) if tasks is not None else None,
            "tasks_blocked": blocked, "tasks_overdue": overdue,
            "completion_percent": percentage,
            "next_action": task_view(current) if current else None,
            "tasks": [task_view(t) for t in sorted(active, key=lambda t: task_key(t, today))[:30]] if mode == "FULL" else [],
        },
        "scientific": {
            "gates_total": metric(gates), "gates_approved_documented": approved_gates,
            "next_ready_gate": ready_gates[0] if ready_gates else None,
            "gates": rows_gates,
            "searches_logged": metric(search_rows),
            "searches_marked_complete_in_register": search_reported,
            "screening_records_registered": metric(tables["records"]),
            "evidence_rows_registered": metric(tables["evidence"]),
            "claims_registered": metric(claims),
            "claims_needing_review": needs_claim_review,
            "ai_uses_registered": metric(ai_rows),
            "substantive_ai_uses_pending_review": ai_review_pending,
            "submission_checks_registered": metric(tables["submissions"]),
            "source_verification": source_public,
            "gates_approved_with_source_conflicts": sum(
                bool(g.get("approval_with_open_source_controls")) for g in rows_gates),
        },
        "traceability": {
            "events_registered": metric(trace),
            "latest_events": [{
                "id": short(t.get("Trace_ID"), 40), "when": short(t.get("Timestamp"), 40),
                "summary": short(t.get("Action_summary")), "status": short(t.get("Status"), 40),
            } for t in (trace or [])[-5:][::-1]] if mode == "FULL" else [],
        },
        "synchronization": {
            "external_manager_links_registered": metric(sync_rows),
            "conflicts_registered": sync_conflicts,
            "drive_synchronized_now": None,
            "note": "Storage state is declared in config; live external synchronization is not verified by this read-only view.",
        },
        "missing_registers": [FILES[key] for key, table in tables.items() if table is None],
        "warnings": [
            "C.A.D.A. completion is operational progress, not scientific validity.",
            "Counts, gate approvals and events are statements found in canonical records, not independent proof.",
        ],
    }
    return result

def plain_text(data: dict) -> str:
    """Compact host/chat fallback with no unsupported success claims."""
    op, sc = data["operational"], data["scientific"]
    nxt = op["next_action"]
    return "\n".join([
        "Meu Artigo — " + data["project"]["title"],
        "Tarefas concluídas (registro): " + str(op["tasks_done_reported"]) + "/" + str(op["tasks_total"]),
        "Bloqueadas: " + str(op["tasks_blocked"]) + " | Vencidas: " + str(op["tasks_overdue"]),
        "Validações científicas documentadas: " + str(sc["gates_approved_documented"]) + "/" + str(sc["gates_total"]),
        "Próxima ação: " + (nxt["action"] + " [" + nxt["id"] + "]" if nxt else "Não identificada nos registros"),
        "Próximo gate pronto: " + (sc["next_ready_gate"]["name"] if sc["next_ready_gate"] else "Nenhum marcado como READY"),
        "Integridade das fontes: " + sc["source_verification"]["status"]
        + " | divergências: " + str(sc["source_verification"]["blocked"])
        + " | revisão pendente: " + str(sc["source_verification"]["pending_review"]),
        "Estado do armazenamento (declarado): " + data["project"]["storage_state"],
        "Importante: progresso C.A.D.A. não equivale a validação científica.",
    ])

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("project", help="Authorized local mirror path; does not connect to Google Drive")
    p.add_argument("--mode", choices=["MINIMAL", "FULL"])
    p.add_argument("--format", choices=["json", "text"], default="json")
    args = p.parse_args(argv)
    try:
        data = view(Path(args.project), mode=args.mode)
        print(plain_text(data) if args.format == "text" else json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, csv.Error, json.JSONDecodeError) as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
