#!/usr/bin/env python3
"""Read-only intelligent research continuity from existing canonical records.

This is a *presentation* of already-recorded METHOD decisions, method fields,
GATE and C.A.D.A. next-action routing. It neither authenticates humans nor
infers scientific completion, repeats private rationale, invents follow-up
tasks, writes project files, or claims Google Drive synchronization.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re

from method_routes import MGMT, REQUIRED_DESIGN, ROUTES
from method_fill_preflight import normalize, PLACEHOLDER_NORMALIZED
from next_step_router import resolve as resolve_next_step

REQUIRED_DECISION_FIELDS={"DEC_ID","Decision_type","Decision",
                          "Status","Decided_by","Trace_ID"}
VALID_STATUSES={"PROPOSED","APPROVED","REJECTED","FROZEN","SUPERSEDED"}
METHOD_FIELD_QUESTION="Researcher methodological detail: "
METHOD_FIELD_VALUE_RE=re.compile(
    r"^([a-z_]+) formally recorded; declared value checksum ([a-f0-9]{64})$"
)
MAX_FILE_BYTES=2_000_000

# These are consequences of the declared *route family*, not claims that
# any particular method choice or empirical procedure is scientifically sound.
ROUTE_IMPLICATIONS={
    "INTEGRATIVE_REVIEW":("Bound literature selection, appraise varied evidence, and justify integrative synthesis."),
    "SYSTEMATIC_REVIEW":("Define auditable eligibility, execute planned retrieval, appraise evidence and synthesize with limits."),
    "PROBLEMATIZING_REVIEW":("Identify assumptions, original intellectual positions, counterarguments and bounded reframing."),
    "CONCEPTUAL_THEORY":("Specify conceptual premises, source lineage, rival explanations and theoretical boundaries."),
    "QUALITATIVE":("Justify tradition, context, material selection, interpretive analysis and researcher reflexivity."),
    "QUANTITATIVE":("Define units, measures, sampling, analytic assumptions and permitted statistical inferences."),
    "MIXED_METHODS":("Justify both research strands, integration points, discordance and bounded meta-inference."),
    "DESIGN_SCIENCE":("Trace problem requirements to artifact construction, evaluation criteria, results and limits."),
}
ACTION_EXPLANATIONS={
    "RECONCILE_PENDING_TRANSACTION":"Reconcile the unfinished local transaction using the authorized recovery procedure before any new scientific write.",
    "RECONCILE_CADA_AND_CONTINUITY":"Compare canonical continuity against C.A.D.A. task completion and original receipts; do not execute an inconsistent task.",
    "REVIEW_CONFLICTING_METHOD_DECISION_EVIDENCE":"Researcher reviews the original recorded method decision and its profile/TRACE evidence before proceeding.",
    "VERIFY_AUTHORIZED_CANONICAL_STORAGE":"Confirm current authorized canonical storage and synchronization before treating local records as authoritative.",
    "RECONCILE_PROJECT_RECORDS":"Reconcile missing or conflicting canonical registers before declaring a new action executable.",
    "EXECUTE_RECORDED_CADA_TASK":"Proceed only with the task identified by the existing CADA_ID and its approved Next_action field; this panel does not run it.",
    "RESEARCHER_DECIDE_RECORDED_CADA_TASK":"Researcher must decide the item recorded at the existing CADA_ID; the assistant may prepare neutral alternatives.",
    "RESEARCHER_CHOOSE_AND_JUSTIFY_METHOD_ROUTE":"Researcher chooses and justifies a methodological family and documents the actual decision reference.",
    "RESEARCHER_REVIEW_PENDING_SCIENTIFIC_GATE":"Researcher evaluates the indicated gate against original evidence; this view cannot approve it.",
    "RESEARCHER_REVIEW_NEXT_METHOD_FIELD":"Researcher reviews the indicated canonical method field and its methodological alternatives.",
    "REQUEST_RESEARCHER_REVIEW_OF_CONTINUATION":"Review the project state and choose the next documented course without assuming it is complete.",
}

def _json(path: Path) -> dict | None:
    if path.is_symlink() or not path.is_file() or path.stat().st_size>MAX_FILE_BYTES:
        return None
    try:
        obj=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,UnicodeError,ValueError):
        return None
    return obj if isinstance(obj,dict) else None

def _csv(path: Path, required: set[str], identifier: str):
    if path.is_symlink() or not path.is_file() or path.stat().st_size>MAX_FILE_BYTES:
        return None,"MISSING_OR_UNSAFE_REGISTER"
    try:
        with path.open(encoding="utf-8-sig",newline="") as stream:
            reader=csv.DictReader(stream)
            heads=reader.fieldnames or []
            if (not required.issubset(set(heads)) or len(heads)!=len(set(heads))):
                return None,"INVALID_REGISTER_HEADERS"
            rows=list(reader)
        if any(None in row for row in rows):
            return None,"MALFORMED_REGISTER_ROWS"
        vals=[str(row.get(identifier) or "").strip() for row in rows]
        if len(vals)!=len(set(vals)) or any(not value for value in vals):
            return None,"DUPLICATE_OR_MISSING_RECORD_IDENTIFIER"
        return rows,None
    except (OSError,UnicodeError,csv.Error,ValueError):
        return None,"UNREADABLE_REGISTER"

def _last_decision(root: Path, route: str, profile: dict | None) -> dict:
    view={
        "status":"NO_AUTHENTICATED_DECISION_CLAIM",
        "decision_id":None,"decision_type":None,"recorded_status":None,
        "detail_field":None,"trace_link_recorded":False,
        "field_checksum_matches_canonical":None,
        "decision_order":"LAST_CANONICAL_APPEND_ROW_NOT_VERIFIED_CHRONOLOGY",
        "human_identity_independently_authenticated":False,
        "human_scientific_approval_verified":False,
        "raw_decision_text_exported":False,
        "raw_researcher_rationale_exported":False,
        "warnings":[],
    }
    records,error=_csv(root/MGMT/"17_Decision_Log.csv",REQUIRED_DECISION_FIELDS,"DEC_ID")
    if error:
        view["status"]="DECISION_REGISTER_UNAVAILABLE"
        view["warnings"].append(error)
        return view
    if not records:
        view["status"]="NO_RECORDED_DECISIONS"
        return view
    last=records[-1]
    status=str(last.get("Status") or "").strip().upper()
    decision_type=str(last.get("Decision_type") or "").strip().upper()
    view.update({
        "decision_id":last["DEC_ID"],
        "decision_type":decision_type if decision_type else None,
        "recorded_status":status if status else None,
        "status":"LATEST_RECORD_PRESENT_NOT_HUMAN_AUTHENTICATED",
    })
    if status not in VALID_STATUSES:
        view["status"]="UNRECOGNIZED_DECISION_STATUS"
        view["warnings"].append("INVALID_DECISION_STATUS")
    if status in {"APPROVED","FROZEN","REJECTED"} and not str(last.get("Decided_by") or "").strip():
        view["status"]="INCOMPLETE_HUMAN_DECLARATION"
        view["warnings"].append("MISSING_DECLARED_DECISION_MAKER")
    trace_id=str(last.get("Trace_ID") or "").strip()
    trace_rows,trace_error=_csv(root/MGMT/"13_Traceability_Log.csv",{"Trace_ID"},"Trace_ID")
    if trace_error:
        view["warnings"].append("TRACE_REGISTER_"+trace_error)
    elif trace_id and any(x.get("Trace_ID")==trace_id for x in trace_rows):
        view["trace_link_recorded"]=True
    else:
        view["warnings"].append("DECISION_TRACE_NOT_FOUND")
    # Decision question supplies *structural* provenance. Don't export
    # original research question, decision prose or human rationale.
    question=str(last.get("Decision_question") or "")
    if decision_type=="METHOD" and question.startswith(METHOD_FIELD_QUESTION):
        field=question[len(METHOD_FIELD_QUESTION):]
        declared=str(last.get("Decision") or "")
        parsed=METHOD_FIELD_VALUE_RE.fullmatch(declared)
        view["detail_field"]=field if (route in REQUIRED_DESIGN
                                        and field in REQUIRED_DESIGN[route]) else None
        if (not parsed or parsed.group(1)!=field or
            not view["detail_field"] or profile is None or
            not isinstance(profile.get("route_details"),dict)):
            view["status"]="METHOD_FIELD_DECISION_INCONSISTENT"
            view["warnings"].append("FIELD_DECISION_SCHEMA_OR_ROUTE_CONFLICT")
        else:
            current=profile["route_details"].get(field)
            digest=(hashlib.sha256(current.encode("utf-8")).hexdigest()
                    if isinstance(current,str) else None)
            same=digest==parsed.group(2)
            view["field_checksum_matches_canonical"]=same
            if not same:
                view["status"]="METHOD_FIELD_DECISION_INCONSISTENT"
                view["warnings"].append("FIELD_VALUE_NO_LONGER_MATCHES_RECORDED_DECISION")
    elif decision_type=="METHOD" and str(last.get("Decision") or "") in ROUTES:
        if str(last.get("Decision"))!=route or (
            profile and profile.get("route_decision_id")==last.get("DEC_ID")
            and profile.get("route_confirmation")!="HUMAN_CONFIRMED"
        ):
            view["status"]="METHOD_ROUTE_DECISION_INCONSISTENT"
            view["warnings"].append("METHOD_ROUTE_OR_CONFIRMATION_MISMATCH")
    return view

def project_method_progress(route: str, profile: dict | None) -> dict:
    required=REQUIRED_DESIGN.get(route,())
    output={
        "route":route if route in ROUTES else None,
        "route_confirmed_in_record":False,
        "status":"UNAVAILABLE",
        "required_field_count":len(required),
        "completed_field_count":0,
        "remaining_fields":[],
        "next_missing_field":None,
        "completion_is_scientific_validation":False,
        "progress_is_an_unvalidated_structural_count":True,
        "private_method_content_exported":False,
    }
    if profile is None or route not in ROUTES or profile.get("route")!=route or \
       profile.get("schema_version")!=1 or \
       not isinstance(profile.get("route_details"),dict):
        return output
    output["route_confirmed_in_record"]=profile.get("route_confirmation")=="HUMAN_CONFIRMED"
    if route=="UNDECIDED":
        output["status"]="RESEARCHER_ROUTE_DECISION_REQUIRED"
        return output
    details=profile["route_details"]
    remaining=[field for field in required if not isinstance(details.get(field),str)
               or normalize(details[field]) in PLACEHOLDER_NORMALIZED]
    output["remaining_fields"]=remaining
    output["completed_field_count"]=len(required)-len(remaining)
    output["next_missing_field"]=remaining[0] if remaining else None
    output["status"]=("RESEARCHER_ROUTE_DECISION_REQUIRED"
                      if not output["route_confirmed_in_record"]
                      else "METHOD_DETAILS_REMAIN" if remaining
                      else "ALL_REQUIRED_FIELDS_RECORDED_NOT_SCIENTIFICALLY_VALIDATED")
    return output

def compose(root: Path, *, navigation: dict | None=None) -> dict:
    """One conservative continuation projection; never update task state."""
    root=Path(root).resolve()
    nav=resolve_next_step(root) if navigation is None else navigation
    cfg=_json(root/MGMT/"PROJECT_CONFIG.json")
    route=cfg.get("method_route") if cfg else None
    profile=_json(root/MGMT/"METHOD_PROFILE.json")
    progress=project_method_progress(route,profile)
    last=_last_decision(root,route,profile)
    blockers=list(nav.get("blockers") or [])
    if cfg is None:
        blockers.append("PROJECT_CONFIG_NOT_READABLE")
    if progress["status"]=="UNAVAILABLE" and route in ROUTES:
        blockers.append("METHOD_PROFILE_REQUIRES_RECONCILIATION")
    # A malformed/missing decision register or an unlinked TRACE is not a
    # trustworthy "no decisions" state. Fail closed before resuming a task.
    # A legitimately empty, readable decision register remains supported.
    if last["status"] in {
        "DECISION_REGISTER_UNAVAILABLE",
        "METHOD_FIELD_DECISION_INCONSISTENT",
        "METHOD_ROUTE_DECISION_INCONSISTENT",
        "UNRECOGNIZED_DECISION_STATUS",
        "INCOMPLETE_HUMAN_DECLARATION",
    } or (last["decision_id"] is not None and
          not last["trace_link_recorded"]):
        blockers.append("DECISION_PROVENANCE_RECONCILIATION_REQUIRED")
    blockers=list(dict.fromkeys(blockers))
    next_task_id=nav.get("next_task_id")
    next_gate_id=nav.get("next_gate_id")
    trust_block=bool(blockers)
    storage_block=("CANONICAL_STORAGE_NOT_VERIFIED" in blockers or
                   nav.get("status")=="CANONICAL_STORAGE_RECHECK_REQUIRED")
    if "PENDING_RESEARCH_TRANSACTION_RECOVERY" in blockers:
        action="RECONCILE_PENDING_TRANSACTION"
        owner="HUMAN_OR_AUTHORIZED_OPERATOR"
    elif "CADA_CONTINUITY_INTEGRITY_REVIEW" in blockers or \
         any(s.startswith("CONTINUITY_") for s in blockers):
        action="RECONCILE_CADA_AND_CONTINUITY"
        owner="HUMAN_OR_AUTHORIZED_OPERATOR"
    elif "DECISION_PROVENANCE_RECONCILIATION_REQUIRED" in blockers:
        action="REVIEW_CONFLICTING_METHOD_DECISION_EVIDENCE"
        owner="HUMAN_RESEARCHER"
    elif storage_block:
        action="VERIFY_AUTHORIZED_CANONICAL_STORAGE"
        owner="HUMAN_OR_AUTHORIZED_OPERATOR"
    elif blockers:
        # Even when the C.A.D.A. router would permit a technical task,
        # a separate method/profile provenance conflict must be resolved.
        action="RECONCILE_PROJECT_RECORDS"
        owner="HUMAN_OR_AUTHORIZED_OPERATOR"
    elif nav.get("status")=="TECHNICAL_PREPARATION_AVAILABLE" and next_task_id:
        action="EXECUTE_RECORDED_CADA_TASK"
        owner="TECHNICAL_AGENT"
    elif nav.get("status")=="HUMAN_TASK_DECISION_REQUIRED" and next_task_id:
        action="RESEARCHER_DECIDE_RECORDED_CADA_TASK"
        owner="HUMAN_RESEARCHER"
    elif progress["status"]=="RESEARCHER_ROUTE_DECISION_REQUIRED":
        action="RESEARCHER_CHOOSE_AND_JUSTIFY_METHOD_ROUTE"
        owner="HUMAN_RESEARCHER"
    elif next_gate_id and nav.get("status")=="HUMAN_GATE_DECISION_REQUIRED":
        action="RESEARCHER_REVIEW_PENDING_SCIENTIFIC_GATE"
        owner="HUMAN_RESEARCHER"
    elif progress["next_missing_field"]:
        action="RESEARCHER_REVIEW_NEXT_METHOD_FIELD"
        owner="HUMAN_RESEARCHER"
    else:
        action="REQUEST_RESEARCHER_REVIEW_OF_CONTINUATION"
        owner="HUMAN_RESEARCHER"
    # Not a second task board: refer only to existing C.A.D.A. row and
    # established next-step router, never expose raw Next_action content.
    can_execute=(
        action=="EXECUTE_RECORDED_CADA_TASK"
        and nav.get("status")=="TECHNICAL_PREPARATION_AVAILABLE"
        and nav.get("technical_preparation_possible") is True
        and not trust_block)
    return {
        "schema":"MEU_ARTIGO_DECISION_CONTINUITY_V1",
        "status":"RECONCILIATION_REQUIRED" if trust_block else "READ_ONLY_GUIDANCE",
        "last_recorded_decision":last,
        "method_progress":progress,
        "route_implications":{
            "summary":ROUTE_IMPLICATIONS.get(route),
            "describes_recorded_route_family_only":True,
            "does_not_prove_real_world_design_fit":True,
            "scientific_adequacy_review_required":True,
        },
        "next_action":{
            "code":action,
            "explanation":ACTION_EXPLANATIONS[action],
            "responsible":owner,
            "existing_cada_task_id":next_task_id,
            "existing_scientific_gate_id":next_gate_id,
            "canonical_cada_next_action_column_requires_lookup":bool(next_task_id),
            "method_field_for_next_researcher_decision":progress["next_missing_field"],
            "action_title_or_private_task_text_exported":False,
            "execution_authorized_by_this_view":False,
            "technical_preparation_already_authorized_by_router":can_execute,
            "human_action_required_for_scientific_decision":owner!="TECHNICAL_AGENT",
            "blocks_substantive_progress_until_resolved":trust_block,
        },
        "blockers":blockers,
        "review_only_not_a_new_task_record":True,
        "scientific_gate_approved":False,
        "human_identity_authenticated":False,
        "project_changed":False,
        "drive_sync_verified":False,
        "limitations":[
            "Latest decision is the final canonical log row; chronological ordering is not independently verified.",
            "Private question, rationale and C.A.D.A. Next_action prose are not exported.",
            "Existing DEC/TRACE records are declarations, not authentication of scientific judgment.",
            "C.A.D.A. router alone authorizes technical preparation; method-field guidance cannot override it.",
        ],
    }
