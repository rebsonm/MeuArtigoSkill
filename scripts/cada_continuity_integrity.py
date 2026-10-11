"""Read-only integrated integrity audit of the last local C.A.D.A. transition.

A matching SHA-256 checks *local operational provenance*, not scientific
truth, human approval, external database execution, or Google Drive sync.
Existing projects without a PR-49 completion marker remain legacy/unassessed.
"""
from __future__ import annotations

from pathlib import Path

from next_step_router import TERMINAL, clean, recorded_next_ids, resolve, upper
from transaction_coordinator import active_journals


MGMT = "00_Gestao_e_Continuidade"
TASKS = MGMT + "/11_CADA_Control.csv"
DASH = MGMT + "/15_CADA_Dashboard.csv"
CONTINUITY = "CONTINUIDADE.md"


def audit(root: Path) -> dict:
    root = Path(root).resolve()
    report = {
        "schema": "MEU_ARTIGO_CADA_INTEGRITY_V1",
        "status": "NOT_APPLICABLE_LEGACY",
        "errors": [],
        "last_operational_proof_checked": False,
        "human_gate_approved": False,
        "scientific_quality_proven": False,
        "drive_sync_verified": False,
    }
    issues = report["errors"]
    if "cada_continuity" in active_journals(root):
        issues.append("PENDING_CADA_CONTINUITY_TRANSACTION")
        report["status"] = "BLOCKED"
        return report
    # Never read untrusted/unmounted Drive state as if it were canonical.
    path = root / DASH
    if path.is_symlink() or not path.is_file():
        return report
    try:
        from update_cada_continuity import parse_csv
        d_headers, d_rows = parse_csv(path, "Metric")
    except (OSError, UnicodeError, ValueError):
        # No completion sentinel can be trusted from an illegible report.
        issues.append("UNREADABLE_CADA_DASHBOARD")
        report["status"] = "BLOCKED"
        return report
    metrics = [clean(row.get("Metric")) for row in d_rows]
    if len(metrics) != len(set(metrics)):
        issues.append("AMBIGUOUS_CADA_DASHBOARD_METRIC")
        report["status"] = "BLOCKED"
        return report
    state = {clean(row["Metric"]): clean(row.get("Value")) for row in d_rows}
    tid = state.get("Last_trace_event", "")
    cid = state.get("Last_completed_CADA_ID", "")
    if not tid and not cid:
        return report

    report["status"] = "CHECKED"
    if not tid or not cid:
        issues.append("INCOMPLETE_CADA_TRANSITION_MARKERS")
        report["status"] = "BLOCKED"
        return report

    try:
        from update_cada_continuity import confirm_local_execution
        _, rows = parse_csv(root / TASKS, "CADA_ID")
        if len({clean(x["CADA_ID"]) for x in rows}) != len(rows):
            raise ValueError("DUPLICATE_CADA_ID")
        completed = [r for r in rows if clean(r.get("CADA_ID")) == cid]
        if len(completed) != 1:
            issues.append("LAST_COMPLETED_CADA_ID_MISSING_OR_AMBIGUOUS")
        elif upper(completed[0].get("Status")) not in {"DONE", "COMPLETED"}:
            issues.append("LAST_COMPLETED_CADA_NOT_DONE")
        elif tid not in clean(completed[0].get("Completion_evidence")):
            issues.append("LAST_COMPLETION_TRACE_LINK_MISSING")
        else:
            try:
                confirm_local_execution(root, tid, cid, completed[0])
                report["last_operational_proof_checked"] = True
            except (ValueError, OSError, TypeError):
                issues.append("LAST_TECHNICAL_RECEIPT_INVALID_OR_CHANGED")

        active = sum(upper(r.get("Status")) not in TERMINAL for r in rows)
        counts = {
            "Total_active_items": active,
            "Ready_items": sum(upper(r.get("Status")) == "READY" for r in rows),
            "In_progress_items": sum(upper(r.get("Status")) == "IN_PROGRESS" for r in rows),
            "Waiting_items": sum(upper(r.get("Status")) == "WAITING" for r in rows),
            "Blocked_items": sum(upper(r.get("Status")) == "BLOCKED" for r in rows),
            "Done_items": sum(upper(r.get("Status")) in {"DONE", "COMPLETED"} for r in rows),
        }
        for key, expected in counts.items():
            if state.get(key) != str(expected):
                issues.append("CADA_DASHBOARD_COUNT_MISMATCH_" + key.upper())

        route = resolve(root)
        if route["status"] == "BLOCKED" or route["status"] == "CANONICAL_STORAGE_RECHECK_REQUIRED":
            issues.append("CADA_NAVIGATION_BLOCKED_OR_STORAGE_UNVERIFIED")
        if state.get("Next_CADA_ID", "") != (route["next_task_id"] or ""):
            issues.append("CADA_DASHBOARD_NEXT_TASK_MISMATCH")
        if state.get("Next_human_gate", "") != (route["next_gate_id"] or ""):
            issues.append("CADA_DASHBOARD_NEXT_GATE_MISMATCH")

        continuity_path = root / CONTINUITY
        if continuity_path.is_symlink() or not continuity_path.is_file():
            issues.append("CADA_CONTINUITY_MISSING_OR_UNSAFE")
        else:
            current_text = continuity_path.read_text(encoding="utf-8")
            saved = set(recorded_next_ids(current_text))
            if len(saved) > 1:
                issues.append("CADA_CONTINUITY_CONFLICTING_NEXT_IDS")
            elif route["next_task_id"] and saved != {route["next_task_id"]}:
                issues.append("CADA_CONTINUITY_NEXT_TASK_MISMATCH")
            elif not route["next_task_id"] and saved:
                issues.append("CADA_CONTINUITY_STALE_NEXT_TASK")
            # The new updater records TRACE evidence in the change log, not
            # as a fabricated gate approval or hidden task completion.
            if f"local {tid}; scientific gates unchanged." not in current_text:
                issues.append("CADA_CONTINUITY_CHANGE_LOG_MISSING")
    except (OSError, UnicodeError, ValueError, TypeError):
        issues.append("CADA_CANONICAL_INTEGRITY_INPUT_UNREADABLE")
    if issues:
        report["status"] = "BLOCKED"
    return report
