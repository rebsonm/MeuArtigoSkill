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
    return "\\n".join(rows)

def main(argv: list[str] | None=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project",type=Path,help="Existing authorized local research project")
    parser.add_argument("--mode",choices=["MINIMAL","FULL"])
    parser.add_argument("--format",choices=["json","text"],default="text")
    a=parser.parse_args(argv)
    try:
        result=from_panel(panel(a.project,mode=a.mode))
    except (ValueError,OSError,TypeError,KeyError,csv.Error,json.JSONDecodeError,UnicodeError) as exc:
        print("RESEARCH_RESUME_UNAVAILABLE: "+type(exc).__name__,file=sys.stderr)
        return 2
    print(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)
          if a.format=="json" else text(result))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
