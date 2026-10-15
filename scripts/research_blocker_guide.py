#!/usr/bin/env python3
"""Explain recorded research continuation blockers without performing repairs.

Standalone Skill guidance: uses only the existing sanitized resume brief.
No canonical write, task execution, permission grant or scientific approval.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

from native_chat_dashboard import panel
from research_resume_brief import SCHEMA as RESUME_SCHEMA, from_panel

SCHEMA="MEU_ARTIGO_BLOCKER_GUIDANCE_V1"
ALLOWED_STATUSES=frozenset({
    "RECONCILIATION_REQUIRED","TECHNICAL_PREPARATION_CANDIDATE",
    "HUMAN_DECISION_REQUIRED","READ_ONLY_GUIDANCE",
})
# All descriptions and paths are static. Never interpolate externally
# provided continuity text, task titles, original evidence or rationales.
RECORDS={
    "CONFIG":"00_Gestao_e_Continuidade/PROJECT_CONFIG.json",
    "CONTINUITY":"00_Gestao_e_Continuidade/CONTINUIDADE.md",
    "CADA":"00_Gestao_e_Continuidade/11_CADA_Control.csv",
    "GATES":"00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv",
    "DEC":"00_Gestao_e_Continuidade/17_Decision_Log.csv",
    "TRACE":"00_Gestao_e_Continuidade/13_Traceability_Log.csv",
    "METHOD":"00_Gestao_e_Continuidade/METHOD_PROFILE.json",
}
# (priority, heading, explanation, owner, check, next read-only step).
# Advice does not certify that the named record is itself corrupt.
CATALOG={
    "CANONICAL_DRIVE_ACCESS_NOT_VERIFIED_BY_LOCAL_PANEL":(0,
        "Canonical Drive access not verified",
        "This local view cannot show that the actual authorized Drive records were read or synchronized.",
        "AUTHORIZED_OPERATOR",("CONFIG","CONTINUITY"),
        "Check the authorized Drive project and its actual source records through a connected Drive tool; do not overwrite the canonical workspace."),
    "CANONICAL_STORAGE_NOT_VERIFIED":(0,
        "Canonical storage needs verification",
        "The router could not establish that this local view represents authorized canonical storage.",
        "AUTHORIZED_OPERATOR",("CONFIG",),
        "Identify the authorized storage and verify current access before continuing."),
    "LOCAL_FALLBACK_AUTHORIZATION_NOT_RECORDED":(0,
        "Local fallback authorization not recorded",
        "A local copy is not authorized as canonical merely because files are present.",
        "HUMAN_RESEARCHER",("CONFIG",),
        "Review the original storage decision; only the researcher can authorize a documented fallback."),
    "CANONICAL_STORAGE_MODE_UNKNOWN":(0,
        "Canonical storage mode is unknown",
        "The current projection cannot determine a supported storage choice.",
        "AUTHORIZED_OPERATOR",("CONFIG",),
        "Check the project configuration and original storage decision without changing either."),
    "CANONICAL_STORAGE_RECHECK_REQUIRED":(0,
        "Storage needs another check",
        "An earlier local status cannot establish current access to the project's canonical workspace.",
        "AUTHORIZED_OPERATOR",("CONFIG",),
        "Check current authorized canonical storage directly."),
    "PENDING_RESEARCH_TRANSACTION_RECOVERY":(1,
        "An interrupted research transaction may exist",
        "A pending scientific transaction journal must be inspected before another change.",
        "AUTHORIZED_OPERATOR",("CONFIG","DEC","TRACE"),
        "Inspect the existing journal and use only its documented recovery procedure after verifying the original records; do not delete it automatically."),
    "CADA_CONTINUITY_INTEGRITY_REVIEW":(2,
        "Operational completion and continuity do not agree",
        "Completion records, receipts or the saved next step require comparison.",
        "AUTHORIZED_OPERATOR",("CADA","CONTINUITY","TRACE"),
        "Compare the original C.A.D.A. entry, its completion evidence and the continuity note without marking anything complete."),
    "CONTINUITY_NEXT_ACTION_MISMATCH":(2,
        "The recorded next steps disagree",
        "The continuity note points to a different task from the router's eligible C.A.D.A. entry.",
        "AUTHORIZED_OPERATOR",("CADA","CONTINUITY"),
        "Read the existing CADA_ID references in both records and verify which recorded state is current."),
    "CONTINUITY_NEXT_ACTION_NOT_CURRENT":(2,
        "The continuity note may be stale",
        "The recorded next action does not match the current gate/task state.",
        "AUTHORIZED_OPERATOR",("CONTINUITY","CADA","GATES"),
        "Compare the continuity note with original task and gate records before changing the summary."),
    "ROOT_CONTINUITY_COPY_REQUIRES_RECONCILIATION":(2,
        "Conflicting continuity copies need review",
        "A root-level copy exists in addition to the canonical management record.",
        "AUTHORIZED_OPERATOR",("CONTINUITY",),
        "Compare both copies with their history; do not silently select or delete either one."),
    "CONTINUITY_MISSING_OR_UNSAFE":(2,
        "Canonical continuity record is missing or unsafe",
        "The selected project lacks a trustworthy canonical continuity document.",
        "AUTHORIZED_OPERATOR",("CONTINUITY","CADA"),
        "Inspect the authorized workspace and its recorded history; do not reconstruct decisions from the chat."),
    "CONTINUITY_EMPTY":(2,
        "Canonical continuity record is empty",
        "The source record does not contain a usable saved continuation.",
        "AUTHORIZED_OPERATOR",("CONTINUITY","CADA"),
        "Review the original recorded events and task evidence before preparing a new attributable note."),
    "CONTINUITY_CONFLICTING_NEXT_ACTIONS":(2,
        "More than one next step is recorded",
        "The continuity document contains incompatible C.A.D.A. identifiers.",
        "AUTHORIZED_OPERATOR",("CONTINUITY","CADA"),
        "Read both recorded references and compare them to current task state."),
    "DECISION_PROVENANCE_RECONCILIATION_REQUIRED":(3,
        "Scientific decision provenance needs reconciliation",
        "At least one decision or its TRACE link cannot currently be trusted.",
        "HUMAN_RESEARCHER",("DEC","TRACE","METHOD"),
        "Review the original decision, its TRACE_ID and associated method profile with the researcher; do not reconstruct consent."),
    "RECORDED_DECISION_PROVENANCE_NOT_VERIFIED":(3,
        "Decision event link is not verified",
        "A displayed DEC_ID is missing a confirmed link to its recorded trace.",
        "HUMAN_RESEARCHER",("DEC","TRACE"),
        "Check the original event linkage and the researcher's actual evidence."),
    "RECORDED_DECISION_STATE_REQUIRES_REVIEW":(3,
        "The last decision state needs review",
        "The last decision is malformed, unrecognized or inconsistent with its method evidence.",
        "HUMAN_RESEARCHER",("DEC","TRACE","METHOD"),
        "Inspect the original DEC record and associated provenance with the researcher."),
    "METHOD_PROFILE_REQUIRES_RECONCILIATION":(3,
        "Method profile needs reconciliation",
        "The recorded route or method profile is unavailable or inconsistent.",
        "HUMAN_RESEARCHER",("METHOD","CONFIG","DEC"),
        "Compare the recorded route, original human choice and method-profile fields; do not select a route automatically."),
    "SEVEN_GATES_NOT_PRESENT_OR_UNEXPECTED":(3,
        "Scientific gate register is incomplete",
        "The expected seven gate identifiers cannot be established from this record.",
        "HUMAN_RESEARCHER",("GATES","DEC"),
        "Inspect gate records and previous human decisions without manufacturing approvals."),
    "PRIOR_HUMAN_GATE_NOT_DOCUMENTED":(3,
        "A prior human gate is not documented",
        "The proposed task belongs beyond the next unresolved researcher-reviewed stage.",
        "HUMAN_RESEARCHER",("GATES","CADA"),
        "Review the original gate evidence and obtain the researcher's actual scientific judgment."),
    "UNKNOWN_TASK_DEPENDENCY":(4,
        "A task dependency is not registered",
        "The task names a prerequisite not found in the existing task register.",
        "AUTHORIZED_OPERATOR",("CADA",),
        "Compare the dependency identifiers in the canonical task register."),
    "UNFINISHED_TASK_DEPENDENCY":(4,
        "A prerequisite task is not documented as complete",
        "A required task has not reached an eligible recorded completion state.",
        "AUTHORIZED_OPERATOR",("CADA",),
        "Review prerequisite status and its real completion evidence; do not mark it done."),
    "UNVERIFIED_TASK_DEPENDENCY_COMPLETION":(4,
        "Dependency completion evidence is missing",
        "A prerequisite has an apparent completion state but lacks required evidence.",
        "AUTHORIZED_OPERATOR",("CADA","TRACE"),
        "Check original receipts and task records before accepting the dependency."),
    "MISSING_RECORDED_NEXT_ACTION":(4,
        "The next task has no recorded action",
        "The task register does not identify a sufficiently recorded next action.",
        "HUMAN_RESEARCHER",("CADA","CONTINUITY"),
        "Review the intended next action with the researcher; no automatic task is assigned."),
    "TASK_NOT_READY":(4,
        "The task is not in an eligible state",
        "The saved C.A.D.A. task is not recorded as ready for technical preparation.",
        "AUTHORIZED_OPERATOR",("CADA",),
        "Check its actual status and dependencies before considering a change."),
    "CANONICAL_CONTINUITY_RECONCILIATION_REQUIRED":(5,
        "The consolidated research state needs reconciliation",
        "The current scientific continuation view reports unresolved inconsistencies.",
        "AUTHORIZED_OPERATOR",("CONTINUITY","DEC","TRACE"),
        "Use the more specific recorded reasons first, then re-read the canonical records."),
    "NEXT_ACTION_NAVIGATION_MISMATCH":(3,
        "The action and navigation projections disagree",
        "Two read-only views point to different next task/gate identifiers.",
        "AUTHORIZED_OPERATOR",("CADA","GATES","CONTINUITY"),
        "Re-read the original router inputs and check the differences without executing either proposal."),
    "NEXT_ACTION_AUTHORIZATION_MISMATCH":(3,
        "Task eligibility claims do not agree",
        "One projection claims technical preparation while the other does not.",
        "AUTHORIZED_OPERATOR",("CADA","GATES"),
        "Re-check the current router and real execution permissions."),
    "CANONICAL_NAVIGATION_STATUS_CONFLICT":(3,
        "Navigation status contradicts preparation permission",
        "The saved read-only status is incompatible with the displayed permission flag.",
        "AUTHORIZED_OPERATOR",("CADA","GATES"),
        "Check the original C.A.D.A. task and its gate dependencies."),
    "NEXT_ACTION_IDENTIFIER_REQUIRES_RECONCILIATION":(3,
        "An action identifier cannot be trusted",
        "The next reference is malformed or unsupported.",
        "AUTHORIZED_OPERATOR",("CADA","GATES"),
        "Inspect original identifiers in the canonical task and gate registers."),
    "CANONICAL_NAVIGATION_STATUS_NOT_RECOGNIZED":(3,
        "Navigation status is not recognized",
        "A routing state appeared that this guidance layer cannot safely interpret.",
        "AUTHORIZED_OPERATOR",("CADA","GATES"),
        "Review the router output and compatibility before taking action."),
    "NEXT_ACTION_PROJECTION_UNRECOGNIZED":(3,
        "Next action is not recognized",
        "The reported action or responsible actor does not match the supported classifications.",
        "AUTHORIZED_OPERATOR",("CADA","GATES"),
        "Review the actual source register and update the software mapping separately if appropriate."),
    "CANONICAL_DECISION_STATE_UNRECOGNIZED":(3,
        "Decision continuity state is not recognized",
        "The reported decision-continuity state is not supported by this guide.",
        "AUTHORIZED_OPERATOR",("DEC","TRACE"),
        "Re-read the existing decision records before choosing an action."),
}
# Some unknown reasons originate in canonical validation and must *not*
# be displayed as trusted or harmless instructions.
UNKNOWN=(6,
    "An unresolved or unsupported record conflict exists",
    "This version cannot classify one or more blocker codes reliably.",
    "AUTHORIZED_OPERATOR",("CONFIG","CONTINUITY"),
    "Read original records with an authorized operator; do not infer a repair.")

def _card(code: str | None, entry: tuple) -> dict:
    priority,heading,explanation,owner,records,next_read=entry
    return {
        "code":code if code in CATALOG else "UNCLASSIFIED_RECONCILIATION_CAUSE",
        "priority":priority,
        "heading":heading,
        "reason":explanation,
        "responsible":owner,
        "canonical_records_to_review":[RECORDS[k] for k in records],
        "safe_read_only_next_step":next_read,
        "automatic_repair_authorized":False,
        "scientific_gate_approved":False,
        "storage_write_authorized":False,
    }

def explain(brief: dict, *, limit: int=3) -> dict:
    """Pure interpretation of the sanitized resume brief."""
    if not isinstance(brief,dict) or brief.get("schema")!=RESUME_SCHEMA:
        raise ValueError("Only a real Skill resume projection may be explained")
    if brief.get("status") not in ALLOWED_STATUSES:
        raise ValueError("Unsupported research status")
    if not isinstance(limit,int) or isinstance(limit,bool) or not 1<=limit<=8:
        raise ValueError("Invalid presentation limit")
    codes=brief.get("blockers")
    if not isinstance(codes,list) or any(not isinstance(x,str) for x in codes):
        raise ValueError("Blocker list is not structurally valid")
    ordered=[]
    seen=set()
    for code in codes:
        canonical=code if code in CATALOG else "UNCLASSIFIED_RECONCILIATION_CAUSE"
        if canonical in seen:
            continue
        seen.add(canonical)
        item=_card(code,CATALOG.get(code,UNKNOWN))
        ordered.append(item)
    if brief["status"]=="RECONCILIATION_REQUIRED" and not ordered:
        ordered.append(_card(None,UNKNOWN))
    ordered.sort(key=lambda x:x["priority"])
    primary=ordered[0] if ordered else None
    details=ordered[:limit]
    status=("BLOCKED_REVIEW_ONLY" if primary else
            "NO_RECORDED_BLOCKER_NOT_AN_EXECUTION_APPROVAL")
    return {
        "schema":SCHEMA,
        "status":status,
        "source_resume_status":brief["status"],
        "primary":primary,
        "issues":details,
        "issues_total":len(ordered),
        "issues_not_shown":max(0,len(ordered)-len(details)),
        "what_can_be_done_now":[
            "Explain recorded blocker types using only verified technical metadata",
            "Inspect authorized canonical records read-only",
            "Compare existing technical identifiers without overwriting records",
            "Discuss possible methodological alternatives without recording a choice",
        ],
        "what_requires_human_or_operator":[
            "Resolve access to the real canonical storage with the authorized account",
            "Approve consequential scientific choices with actual researcher review",
            "Use documented journal recovery only after inspecting original evidence",
        ],
        "next_conversation_option":(
            "REVIEW_PRIMARY_BLOCKER_WITH_ORIGINAL_RECORDS"
            if primary else "DISCUSS_RECORDED_NEXT_ACTION_WITH_RESEARCHER"
        ),
        "no_new_task_created":True,
        "no_automatic_repair":True,
        "no_task_executed":True,
        "no_gate_approved":True,
        "no_canonical_write":True,
        "drive_sync_verified":False,
        "new_server_required":False,
        "project_changed":False,
        "private_source_content_exported":False,
    }

def text(view: dict) -> str:
    """Compact English-first CLI presentation, localizable in Skill chat."""
    if view.get("schema")!=SCHEMA:
        raise ValueError("Invalid blocker-guidance view")
    lines=["Meu Artigo - safe continuation guidance",
           "Status: "+view["status"]]
    if view["primary"]:
        p=view["primary"]
        lines.extend([
            "First issue: "+p["heading"],
            "Why: "+p["reason"],
            "Responsible: "+p["responsible"],
            "Read-only next step: "+p["safe_read_only_next_step"],
            "Canonical records to check: "+", ".join(p["canonical_records_to_review"]),
        ])
        if view["issues_not_shown"]:
            lines.append("Additional issues not shown: "+str(view["issues_not_shown"]))
    else:
        lines.append("No classified blocker in this view; the next action still requires current permission checks.")
    lines.append("No repairs, task executions or scientific approvals were performed.")
    return "\n".join(lines)

def main(argv: list[str] | None=None) -> int:
    arg=argparse.ArgumentParser(description=__doc__)
    arg.add_argument("project",type=Path,help="Authorized existing local research project")
    arg.add_argument("--mode",choices=("MINIMAL","FULL"))
    arg.add_argument("--format",choices=("text","json"),default="text")
    arg.add_argument("--limit",type=int,default=3)
    a=arg.parse_args(argv)
    try:
        view=explain(from_panel(panel(a.project,mode=a.mode)),limit=a.limit)
    except (ValueError,TypeError,KeyError,OSError,UnicodeError,csv.Error,
            json.JSONDecodeError) as exc:
        print("BLOCKER_GUIDANCE_UNAVAILABLE: "+type(exc).__name__,file=sys.stderr)
        return 2
    print(json.dumps(view,ensure_ascii=False,sort_keys=True,indent=2)
          if a.format=="json" else text(view))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
