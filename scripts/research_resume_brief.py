#!/usr/bin/env python3
"""Safe, read-only 'continue my research' brief for the standalone Skill.

Project state is projected by the existing native panel, C.A.D.A. router,
and DEC/TRACE decision continuity. This module creates no scientific record,
performs no task or gate transition, and does not verify remote Drive sync.
Returned fields are fixed-status metadata, never researcher prose.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

from decision_continuity import ACTION_EXPLANATIONS
from method_routes import ROUTES
from native_chat_dashboard import panel

SCHEMA="MEU_ARTIGO_CHAT_RESUME_V1"
ID_PATTERNS={
    "decision":re.compile(r"^DEC-[0-9]{4,8}$"),
    "task":re.compile(r"^CADA-[0-9]{4,8}$"),
    "gate":re.compile(r"^GATE-[0-9]{4,8}$"),
}
ACTORS=frozenset({"TECHNICAL_AGENT","HUMAN_RESEARCHER","HUMAN_OR_AUTHORIZED_OPERATOR"})
PREPARATION_ACTION="EXECUTE_RECORDED_CADA_TASK"
NO_DECISION_STATUS="NO_RECORDED_DECISIONS"

def _id(value: object, kind: str) -> str | None:
    """A recorded ID is displayed only if it has an expected technical shape."""
    return value if isinstance(value,str) and ID_PATTERNS[kind].fullmatch(value) else None

def _blockers(*collections: object) -> list[str]:
    out=[]
    for collection in collections:
        if not isinstance(collection,list):
            continue
        for code in collection:
            if (isinstance(code,str) and re.fullmatch(r"[A-Z][A-Z0-9_]{0,95}",code)
                    and code not in out):
                out.append(code)
    return out

def from_panel(snapshot: dict) -> dict:
    """Derive a minimal next-step message from the existing conservative panel."""
    if not isinstance(snapshot,dict) or snapshot.get("schema")!="MEU_ARTIGO_NATIVE_PANEL_V1":
        raise ValueError("A verified native panel projection is required")
    nav=snapshot.get("continuation")
    continuity=snapshot.get("decision_continuity")
    if not isinstance(nav,dict) or not isinstance(continuity,dict):
        raise ValueError("Canonical continuation projection missing")
    last=continuity.get("last_recorded_decision")
    method=continuity.get("method_progress")
    next_action=continuity.get("next_action")
    if not all(isinstance(x,dict) for x in (last,method,next_action)):
        raise ValueError("Canonical decision or method state missing")

    blockers=_blockers(nav.get("blockers"),continuity.get("blockers"))
    storage=snapshot.get("project_storage_recorded")
    local_declared=snapshot.get("local_work_fallback_authorized_in_config") is True
    if storage=="WORK_FALLBACK":
        if not local_declared:
            blockers.append("LOCAL_FALLBACK_AUTHORIZATION_NOT_RECORDED")
    elif storage=="GOOGLE_DRIVE":
        # A local panel cannot verify that this session has read from
        # canonical Drive or synchronized any local staging copy.
        blockers.append("CANONICAL_DRIVE_ACCESS_NOT_VERIFIED_BY_LOCAL_PANEL")
    else:
        blockers.append("CANONICAL_STORAGE_MODE_UNKNOWN")
    if continuity.get("status") == "RECONCILIATION_REQUIRED":
        blockers.append("CANONICAL_CONTINUITY_RECONCILIATION_REQUIRED")
    elif continuity.get("status") != "READ_ONLY_GUIDANCE":
        blockers.append("CANONICAL_DECISION_STATE_UNRECOGNIZED")
    if nav.get("status") != "TECHNICAL_PREPARATION_AVAILABLE" and (
            nav.get("technical_preparation_possible") is True):
        blockers.append("CANONICAL_NAVIGATION_STATUS_CONFLICT")
    if (not isinstance(nav.get("status"),str)
            or nav.get("status") not in {
                "TECHNICAL_PREPARATION_AVAILABLE","HUMAN_TASK_DECISION_REQUIRED",
                "HUMAN_GATE_DECISION_REQUIRED","BLOCKED","BLOCKED_TASK",
                "CANONICAL_STORAGE_RECHECK_REQUIRED",
                "CADA_CONTINUITY_INTEGRITY_REVIEW","RECONCILIATION_REQUIRED",
                "TASK_EXECUTION_PERMISSION_REVIEW","NO_RECORDED_NEXT_ACTION",
                "CONTINUITY_RECONCILIATION_REQUIRED",
            }):
        # A new router status must be inspected before being interpreted.
        blockers.append("CANONICAL_NAVIGATION_STATUS_NOT_RECOGNIZED")

    decision_id=_id(last.get("decision_id"),"decision")
    if last.get("decision_id") is not None and (
            decision_id is None or last.get("trace_link_recorded") is not True):
        blockers.append("RECORDED_DECISION_PROVENANCE_NOT_VERIFIED")
    if last.get("status") in {
            "DECISION_REGISTER_UNAVAILABLE","METHOD_FIELD_DECISION_INCONSISTENT",
            "METHOD_ROUTE_DECISION_INCONSISTENT","UNRECOGNIZED_DECISION_STATUS",
            "INCOMPLETE_HUMAN_DECLARATION"}:
        blockers.append("RECORDED_DECISION_STATE_REQUIRES_REVIEW")
    task_id=_id(next_action.get("existing_cada_task_id"),"task")
    gate_id=_id(next_action.get("existing_scientific_gate_id"),"gate")
    action_code=next_action.get("code")
    actor=next_action.get("responsible")
    if action_code not in ACTION_EXPLANATIONS or actor not in ACTORS:
        blockers.append("NEXT_ACTION_PROJECTION_UNRECOGNIZED")
        action_code="REQUEST_RESEARCHER_REVIEW_OF_CONTINUATION"
        actor="HUMAN_RESEARCHER"

    # Do not announce an available task when its supposedly documented
    # identifier has an untrusted shape or conflicts with the panel view.
    if (next_action.get("existing_cada_task_id") is not None and task_id is None or
        next_action.get("existing_scientific_gate_id") is not None and gate_id is None):
        blockers.append("NEXT_ACTION_IDENTIFIER_REQUIRES_RECONCILIATION")
    if (task_id!=_id(nav.get("next_task_id"),"task") or
        gate_id!=_id(nav.get("next_gate_id"),"gate")):
        blockers.append("NEXT_ACTION_NAVIGATION_MISMATCH")
    if nav.get("technical_preparation_possible") is True and (
        not next_action.get("technical_preparation_already_authorized_by_router") or
        action_code!=PREPARATION_ACTION):
        blockers.append("NEXT_ACTION_AUTHORIZATION_MISMATCH")

    blockers=list(dict.fromkeys(blockers))
    possible=(
        not blockers
        and action_code==PREPARATION_ACTION
        and actor=="TECHNICAL_AGENT"
        and task_id is not None
        and nav.get("status") == "TECHNICAL_PREPARATION_AVAILABLE"
        and nav.get("technical_preparation_possible") is True
        and next_action.get("technical_preparation_already_authorized_by_router") is True
    )
    status=("RECONCILIATION_REQUIRED" if blockers else
            "TECHNICAL_PREPARATION_CANDIDATE" if possible else
            "HUMAN_DECISION_REQUIRED" if actor=="HUMAN_RESEARCHER" else
            "READ_ONLY_GUIDANCE")
    route=method.get("route")
    route=route if route in ROUTES else None
    next_field=method.get("next_missing_field")
    # Canonical fields are identifiers, not arbitrary free-form prose.
    next_field=(next_field if isinstance(next_field,str)
                and re.fullmatch(r"[a-z][a-z0-9_]{0,63}",next_field) else None)
    decision_state=last.get("status")
    return {
        "schema":SCHEMA,
        "status":status,
        "recorded":{
            "last_decision_id":decision_id,
            "last_decision_state":decision_state if isinstance(decision_state,str)
                                  and re.fullmatch(r"[A-Z][A-Z0-9_]{0,95}",decision_state)
                                  else "UNKNOWN",
            "decision_is_authenticated":False,
            "method_route":route,
            "next_missing_method_field":next_field,
            "completed_method_fields":method.get("completed_field_count")
                                       if isinstance(method.get("completed_field_count"),int)
                                       else None,
            "required_method_fields":method.get("required_field_count")
                                      if isinstance(method.get("required_field_count"),int)
                                      else None,
        },
        "next_step":{
            "code":action_code,
            "responsible":actor,
            "existing_cada_id":task_id,
            "existing_gate_id":gate_id,
            "technical_preparation_candidate":possible,
            "task_executed_by_this_brief":False,
            "gate_approved_by_this_brief":False,
        },
        "blockers":blockers,
        "storage":{
            "mode_recorded":storage if storage in {"GOOGLE_DRIVE","WORK_FALLBACK"} else "UNKNOWN",
            "local_fallback_declared_in_config":local_declared,
            "google_drive_access_verified_in_this_session":False,
            "google_drive_sync_verified_in_this_session":False,
        },
        "available_followups":(
            ["REVIEW_BLOCKERS","SHOW_EXISTING_RECORD_IDENTIFIERS"]
            if blockers else
            ["EXPLAIN_NEXT_ACTION","EXPLORE_METHOD_OPTIONS","SHOW_EXISTING_RECORD_IDENTIFIERS"]
        ),
        "scientific_decision_requires_researcher":True,
        "methodological_fitness_verified":False,
        "new_task_created":False,
        "canonical_files_modified":False,
        "source_text_or_private_task_included":False,
        "separate_service_connection_required":False,
    }

LABELS={
    "RECONCILIATION_REQUIRED":"Records or access permissions require reconciliation",
    "TECHNICAL_PREPARATION_CANDIDATE":"A technical preparation candidate exists; nothing has run",
    "HUMAN_DECISION_REQUIRED":"The next scientific decision belongs to the researcher",
    "READ_ONLY_GUIDANCE":"Project continuity needs review before execution",
}
def text(brief: dict) -> str:
    """English-first plain-text fallback; the Skill localizes JSON in chat."""
    if brief.get("schema")!=SCHEMA:
        raise ValueError("Unknown research-resume schema")
    recorded=brief["recorded"]
    step=brief["next_step"]
    rows=[
        "Meu Artigo - recorded continuation (not scientific validation)",
        LABELS.get(brief["status"],"State unavailable"),
        "Last recorded decision: "+str(recorded["last_decision_id"] or "not available")+
        " ("+recorded["last_decision_state"]+"; human identity not authenticated)",
        "Recorded method route: "+str(recorded["method_route"] or "unverified"),
        "Next recorded action: "+step["code"]+"; actor: "+step["responsible"],
        "Existing references: "+str(step["existing_cada_id"] or "none")+
        " / "+str(step["existing_gate_id"] or "none"),
        "Next missing method field: "+str(recorded["next_missing_method_field"] or "not identified"),
        "First blocker: "+(brief["blockers"][0] if brief["blockers"] else "none in this projection"),
        "Technical action performed: NO; scientific gate approved: NO",
        "Drive access/sync in this session: NOT VERIFIED",
    ]
    return "\n".join(rows)


# All guidance is a presentation of the existing router and human gate rules.
# These are completion checks to look for, not automatically satisfied gates.
GUIDED_ACTIONS = {
    "RECONCILE_PENDING_TRANSACTION": (
        "Review the interrupted transaction before resuming research.",
        "Verify original records and complete the authorized recovery procedure."),
    "RECONCILE_CADA_AND_CONTINUITY": (
        "Reconcile the discrepancy between the recorded task and continuity.",
        "Confirm that task, continuity and receipts reflect the same recorded state."),
    "REVIEW_CONFLICTING_METHOD_DECISION_EVIDENCE": (
        "Review the methodological decision and its evidence with the researcher.",
        "Reconcile the original human decision with method and trace records."),
    "VERIFY_AUTHORIZED_CANONICAL_STORAGE": (
        "Verify access to authorized canonical storage.",
        "Directly confirm canonical access without assuming synchronization."),
    "RECONCILE_PROJECT_RECORDS": (
        "Review conflicting or unavailable canonical records.",
        "Resolve the documented discrepancy and repeat continuity checks."),
    "EXECUTE_RECORDED_CADA_TASK": (
        "Continue the previously recorded, eligible operational task.",
        "Provide actual output, execution evidence and the matching completion record."),
    "RESEARCHER_DECIDE_RECORDED_CADA_TASK": (
        "Request only the pending human decision linked to the recorded task.",
        "Record the researcher's actual choice, rationale and task linkage."),
    "RESEARCHER_CHOOSE_AND_JUSTIFY_METHOD_ROUTE": (
        "Compare plausible routes and request the researcher's methodological choice.",
        "Record the actual human choice and rationale without stage approval."),
    "RESEARCHER_REVIEW_PENDING_SCIENTIFIC_GATE": (
        "Present the pending gate and evidence needed for human evaluation.",
        "Obtain an explicit researcher decision and auditable evidence; no automatic approval."),
    "RESEARCHER_REVIEW_NEXT_METHOD_FIELD": (
        "Examine the next recorded outstanding methodological component.",
        "Record the researcher's actual definition and justification."),
    "REQUEST_RESEARCHER_REVIEW_OF_CONTINUATION": (
        "Check for completed work or an as-yet unrecorded next step.",
        "Find actual output or an obstacle; missing tasks do not prove project completion."),
}
BLOCKER_DESCRIPTIONS = {
    "CANONICAL_DRIVE_ACCESS_NOT_VERIFIED_BY_LOCAL_PANEL":
        "This local view does not confirm canonical Drive access.",
    "CANONICAL_STORAGE_NOT_VERIFIED":
        "Canonical storage still requires verification.",
    "LOCAL_FALLBACK_AUTHORIZATION_NOT_RECORDED":
        "Local storage is not authorized in the current record.",
    "PENDING_RESEARCH_TRANSACTION_RECOVERY":
        "An interrupted transaction requires reconciliation.",
    "CADA_CONTINUITY_INTEGRITY_REVIEW":
        "Task and continuity evidence are not reconciled.",
    "CONTINUITY_NEXT_ACTION_MISMATCH":
        "The records point to different next tasks.",
    "DECISION_PROVENANCE_RECONCILIATION_REQUIRED":
        "Scientific decision provenance needs verification.",
    "METHOD_PROFILE_REQUIRES_RECONCILIATION":
        "The methodological profile needs reconciliation.",
    "PRIOR_HUMAN_GATE_NOT_DOCUMENTED":
        "Required human approval for this transition is not documented.",
    "CANONICAL_STORAGE_MODE_UNKNOWN":
        "Project storage mode has not been verified.",
}


def _receipt_for_attempt(root: Path, row: dict) -> dict | None:
    """Read only a hash-linked local receipt in its fixed managed directory.

    Never trust a path from a TRACE row or echo original arguments/output.
    A failed run is evidence of an attempt, not evidence of scientific failure.
    """
    import trace_execution
    raw_tid = row.get("Trace_ID")
    if not isinstance(raw_tid, str) or not re.fullmatch(r"TRACE-[0-9]{4,8}", raw_tid):
        return None
    status = str(row.get("Status") or "").strip().upper()
    if status not in {"FAILED", "PARTIAL"}:
        return None
    if row.get("Verification_method") != "CAPTURED_SUBPROCESS_EXIT_AND_ARTIFACT_HASHES":
        return None
    proof = str(row.get("Reproducibility_information") or "")
    matched = re.fullmatch(
        rf"receipt=00_Gestao_e_Continuidade/TRACE_RECEIPTS/{re.escape(raw_tid)}\.json;sha256=([0-9a-f]{{64}})",
        proof)
    if not matched:
        return None
    file = root / "00_Gestao_e_Continuidade" / "TRACE_RECEIPTS" / (raw_tid + ".json")
    if file.is_symlink() or not file.is_file() or file.stat().st_size > 200_000:
        return None
    raw = file.read_bytes()
    if hashlib.sha256(raw).hexdigest() != matched.group(1):
        return None
    receipt = json.loads(raw.decode("utf-8"))
    if not isinstance(receipt, dict) or (
        receipt.get("trace_id") != raw_tid or receipt.get("status") != status or
        receipt.get("schema_version") != 1 or
        receipt.get("script") not in trace_execution.ALLOWED_SCRIPTS or
        not isinstance(receipt.get("arguments_sha256"), str) or
        not re.fullmatch("[0-9a-f]{64}", receipt["arguments_sha256"]) or
        not isinstance(receipt.get("script_sha256"), str) or
        not re.fullmatch("[0-9a-f]{64}", receipt["script_sha256"])):
        return None
    exit_code = receipt.get("exit_code")
    if (not isinstance(exit_code, int) or isinstance(exit_code, bool)
            or (status == "FAILED" and exit_code == 0)
            or (status == "PARTIAL" and exit_code != 0)):
        return None
    for field in ("inputs_before", "inputs_after", "outputs_before", "outputs_after"):
        if not isinstance(receipt.get(field), list):
            return None
        if not all(isinstance(x, dict) and isinstance(x.get("path"), str)
                   for x in receipt[field]):
            return None
    return receipt


def cycle_diagnostic(root: Path, brief: dict) -> dict:
    """Conservative two-attempt anti-loop signal from existing TRACE receipts.

    No new attempt register, fabricated semantic equivalence, or automatic
    task decision. Missing proof stays unknown rather than calling a loop.
    """
    result = {
        "schema": "MEU_ARTIGO_RECORDED_CYCLE_SIGNAL_V1",
        "status": "INSUFFICIENT_VERIFIED_ATTEMPTS",
        "existing_task_id": None,
        "verified_equivalent_attempts": 0,
        "trace_ids": [],
        "same_operation_and_inputs_verified": False,
        "no_new_output_verified": False,
        "human_diagnostic_advised": False,
        "automatically_blocked": False,
        "legitimate_reopening_prohibited": False,
        "new_canonical_register_created": False,
        "project_modified": False,
        "scientific_gate_approved": False,
    }
    if brief.get("schema") != SCHEMA:
        raise ValueError("Cycle guard requires the existing verified resume brief")
    root = Path(root).resolve()
    storage = brief.get("storage") or {}
    if (storage.get("mode_recorded") != "WORK_FALLBACK" or
            storage.get("local_fallback_declared_in_config") is not True):
        result["status"] = "CANONICAL_STORAGE_NOT_VERIFIED"
        return result
    if brief.get("blockers"):
        result["status"] = "RECONCILIATION_REQUIRED_NO_CYCLE_JUDGMENT"
        return result
    task_id = brief.get("next_step", {}).get("existing_cada_id")
    if not _id(task_id, "task"):
        result["status"] = "NO_CURRENT_RECORDED_TASK"
        return result
    result["existing_task_id"] = task_id
    from next_step_router import (TASKS, MGMT, read_csv, upper, TERMINAL)
    tasks, errors = read_csv(root, TASKS, "CADA_ID")
    if errors:
        result["status"] = "TASK_REGISTER_UNAVAILABLE"
        return result
    selected = next((row for row in tasks if row["CADA_ID"].strip() == task_id), None)
    if not selected or upper(selected.get("Status")) in TERMINAL:
        result["status"] = "NO_ACTIVE_TASK_FOR_CYCLE_CHECK"
        return result
    if upper(selected.get("Item_type")) in {"RECURRING", "MONITORING", "PERIODIC"}:
        result["status"] = "EXEMPT_DECLARED_RECURRENT_TASK"
        return result
    trace_file = root / MGMT / "13_Traceability_Log.csv"
    if (trace_file.is_symlink() or not trace_file.is_file() or
            trace_file.stat().st_size > 2_000_000):
        result["status"] = "TRACE_HISTORY_UNAVAILABLE"
        return result
    try:
        with trace_file.open("r", encoding="utf-8-sig", newline="") as fd:
            reader = csv.DictReader(fd)
            required = {"Trace_ID", "CADA_ID", "Status",
                        "Verification_method", "Reproducibility_information"}
            if not required.issubset(set(reader.fieldnames or [])):
                raise ValueError("Missing TRACE columns")
            rows = list(reader)
        if any(None in x for x in rows):
            raise ValueError("Malformed TRACE")
        matching = [x for x in rows if str(x.get("CADA_ID") or "").strip() == task_id]
        if len(matching) < 2:
            return result
        pair = matching[-2:]
        if any(str(x.get("Status") or "").strip().upper() == "CONFIRMED" for x in pair):
            result["status"] = "RECENT_CONFIRMED_EXECUTION_NO_LOOP_SIGNAL"
            return result
        receipts = [_receipt_for_attempt(root, x) for x in pair]
    except (OSError, UnicodeError, ValueError, TypeError, json.JSONDecodeError, csv.Error):
        result["status"] = "ATTEMPT_PROOF_UNAVAILABLE"
        return result
    if any(x is None for x in receipts):
        result["status"] = "INSUFFICIENT_VERIFIED_ATTEMPTS"
        return result
    a, b = receipts
    # Routine validation and verification can legitimately recur. Evaluate
    # those as individual checks; do not classify them as cycles here.
    if a["script"] in {"validate_project.py", "verify_sources.py"}:
        result["status"] = "EXEMPT_ROUTINE_VERIFICATION"
        return result
    fields = ("script", "script_sha256", "arguments_sha256",
              "inputs_before", "outputs_before", "outputs_after")
    equivalence = all(a.get(x) == b.get(x) for x in fields)
    unchanged = all(x["inputs_before"] == x["inputs_after"] and
                    x["outputs_before"] == x["outputs_after"] for x in receipts)
    if not equivalence or not unchanged:
        result["status"] = "DIFFERENT_ATTEMPT_OR_ARTIFACT_CHANGE"
        return result
    # A matching old receipt does not prove that the executable or its
    # observed workspace files still have the same state now. Check the
    # current source and the final observed files before advising a repeat.
    import trace_execution
    script_path = (trace_execution.SCRIPTS_ROOT / b["script"]).resolve()
    if (not script_path.is_file() or
            not script_path.is_relative_to(trace_execution.SCRIPTS_ROOT)):
        result["status"] = "CURRENT_EXECUTABLE_UNAVAILABLE"
        return result
    try:
        current_script_hash = trace_execution.sha256(script_path)
    except OSError:
        result["status"] = "CURRENT_EXECUTABLE_UNAVAILABLE"
        return result
    if current_script_hash != b["script_sha256"]:
        result["status"] = "EXECUTABLE_CHANGED_SINCE_ATTEMPTS"
        return result
    try:
        for item in b["inputs_after"] + b["outputs_after"]:
            if trace_execution.file_state(root, item["path"]) != item:
                result["status"] = "ARTIFACT_CHANGED_SINCE_ATTEMPTS"
                return result
    except (OSError, ValueError, TypeError, KeyError):
        result["status"] = "CURRENT_ARTIFACT_STATE_UNVERIFIED"
        return result
    result.update({
        "status": "TWO_EQUIVALENT_UNPRODUCTIVE_ATTEMPTS",
        "verified_equivalent_attempts": 2,
        "trace_ids": [x["trace_id"] for x in receipts],
        "same_operation_and_inputs_verified": True,
        "no_new_output_verified": True,
        "human_diagnostic_advised": True,
    })
    return result


def guided_view(brief: dict, *, root: Path | None=None,
                overview: dict | None=None) -> dict:
    """Single-action, English-source projection of the established router."""
    if not isinstance(brief, dict) or brief.get("schema") != SCHEMA:
        raise ValueError("A sanitized resume brief is required")
    step = brief["next_step"]
    key = step["code"]
    if key not in GUIDED_ACTIONS:
        raise ValueError("Unsupported next action code")
    reason, exit_criterion = GUIDED_ACTIONS[key]
    blocked = brief["status"] == "RECONCILIATION_REQUIRED"
    if blocked:
        from research_blocker_guide import explain
        blocker = explain(brief, limit=1)["primary"]
        code = blocker["code"] if blocker else "UNCLASSIFIED_RECONCILIATION_CAUSE"
        issue = BLOCKER_DESCRIPTIONS.get(code, "The records require review before advancing.")
    else:
        code, issue = None, None
    recorded = brief["recorded"]
    complete_count = (overview or {}).get("tasks_reported_done")
    complete_text = (f"{complete_count} task(s) marked complete in the operational register"
                     if isinstance(complete_count, int) and complete_count >= 0
                     else "Number of completed tasks not verified")
    fields = recorded.get("completed_method_fields")
    required = recorded.get("required_method_fields")
    if isinstance(fields, int) and isinstance(required, int) and required:
        complete_text += f"; {fields}/{required} method fields recorded (not scientifically validated)"
    next_field = recorded.get("next_missing_method_field")
    remaining = ("Outstanding methodological field: " + next_field
                 if next_field else "Review scientific and operational requirements in canonical state")
    cycle = (cycle_diagnostic(Path(root), brief) if root is not None else None)
    if cycle and cycle["status"] == "TWO_EQUIVALENT_UNPRODUCTIVE_ATTEMPTS":
        reason = ("Diagnose the task obstacle before repeating the "
                  "same execution; consider an independently authorized alternative.")
        exit_criterion = ("Identify the cause and record new evidence, "
                          "a different approach or a necessary human decision.")
    return {
        "schema": "MEU_ARTIGO_GUIDED_RESEARCH_CONTINUATION_V1",
        "state": "BLOCKED" if blocked else (
            "TECHNICAL_PREPARATION_POSSIBLE" if brief["status"] == "TECHNICAL_PREPARATION_CANDIDATE"
            else "HUMAN_DECISION_PENDING" if brief["status"] == "HUMAN_DECISION_REQUIRED"
            else "READ_ONLY_GUIDANCE"),
        "where_we_are": ("Recorded route: " +
                         (recorded["method_route"] or "unverified") +
                         "; last recorded decision: " +
                         (recorded["last_decision_id"] or "not identified")),
        "what_is_recorded": complete_text,
        "what_is_missing": remaining,
        "one_next_action": reason,
        "why": issue if blocked else (
            "Next action selected by existing router; nothing was executed."),
        "exit_criterion": exit_criterion,
        "primary_blocker_code": code,
        "existing_cada_id": step["existing_cada_id"],
        "existing_gate_id": step["existing_gate_id"],
        "cycle_signal": cycle,
        "more_detail": "Use --format json to view existing detail and record identifiers.",
        "not_an_automatic_task_or_gate_transition": True,
        "scientific_completion_verified": False,
        "canonical_state_modified": False,
        "drive_sync_verified": False,
    }


def guided_text(view: dict) -> str:
    if view.get("schema") != "MEU_ARTIGO_GUIDED_RESEARCH_CONTINUATION_V1":
        raise ValueError("Invalid guided continuation")
    lines = [
        "Meu Artigo - research continuation",
        "Status: " + view["state"],
        "Where we are: " + view["where_we_are"],
        "Already recorded: " + view["what_is_recorded"],
        "Outstanding: " + view["what_is_missing"],
        "Next action: " + view["one_next_action"],
        "Why: " + view["why"],
        "Exit criterion: " + view["exit_criterion"],
    ]
    if view["cycle_signal"] and view["cycle_signal"]["human_diagnostic_advised"]:
        lines.append("Attention: two equivalent executions produced no verified new output.")
    lines.append("Technical details are available on demand. No gate was approved.")
    return "\n".join(lines)


def main(argv: list[str] | None=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project",type=Path,help="Existing authorized local research project")
    parser.add_argument("--mode",choices=["MINIMAL","FULL"])
    parser.add_argument("--format",choices=["json","text","guided","guided-json"],default="text")
    a=parser.parse_args(argv)
    try:
        snapshot = panel(a.project,mode=a.mode)
        result = from_panel(snapshot)
        guided = (guided_view(result,root=a.project,overview=snapshot.get("overview"))
                  if a.format in {"guided","guided-json"} else None)
    except (ValueError,OSError,TypeError,KeyError,csv.Error,json.JSONDecodeError,UnicodeError) as exc:
        print("RESEARCH_RESUME_UNAVAILABLE: "+type(exc).__name__,file=sys.stderr)
        return 2
    if a.format in {"json", "guided-json"}:
        print(json.dumps(result if a.format=="json" else guided,
                         sort_keys=True,ensure_ascii=False,indent=2))
    else:
        print(text(result) if a.format=="text" else guided_text(guided))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
