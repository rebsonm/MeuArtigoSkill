#!/usr/bin/env python3
"""Read-only, conversational projections of the adaptive method choice guide.

No personal source texts are read into the result. This is deterministic
navigation over authored, unranked catalogue alternatives; it NEVER
selects a method, authenticates a researcher, writes to canonical project
files, or approves any scientific gate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from adaptive_method_guide import preview, for_project
from method_decision_dimensions import DIMENSIONS
from method_routes import ROUTES

ACTIONS=("suggest","explore","compare","all","decision")
SCHEMA="MEU_ARTIGO_METHOD_DIALOGUE_V1"

def _identity(card):
    return {"id":card["id"],"label":card["label"],
            "when_to_consider":card["when_to_consider"],
            "limits":card["limits"],
            "scientific_approval":False}

def _details(card):
    return {
        **card,
        "scientific_approval":False,
        "reflective_questions":[
            "Which specific part of your research question would this route address?",
            "What assumptions and evidence would make this choice defensible?",
            "Which alternative could reasonably challenge your choice?",
            "Which claims would the selected design not justify?",
        ],
        "required_human_decision":True,
    }

def dialogue(guide: dict, *, action: str="suggest",
             option_id: str|None=None,
             compare_ids: tuple[str,str]|None=None) -> dict:
    """Project a safe navigation step from an already vetted guide result.

    The conversation itself is ephemeral. It does NOT move a proposal
    between scientific states or submit a canonical selection.
    """
    if action not in ACTIONS:
        raise ValueError("Unknown conversational action")
    cards=guide.get("options") or []
    ids=[x["id"] for x in cards]
    if len(ids)!=len(set(ids)):
        raise ValueError("Guide contains duplicate option IDs")
    if any(not isinstance(x,str) or not x for x in ids):
        raise ValueError("Guide contains invalid option IDs")
    if action=="explore" and (option_id is None or option_id not in ids):
        raise ValueError("Explore requires an existing option ID")
    if action=="compare":
        if (not isinstance(compare_ids,tuple) or len(compare_ids)!=2 or
            compare_ids[0]==compare_ids[1] or
            any(x not in ids for x in compare_ids)):
            raise ValueError("Compare requires two distinct existing option IDs")
    if action not in ("explore","compare") and (option_id or compare_ids):
        raise ValueError("Option identifiers are only allowed in explore/compare")
    blocked=guide.get("mode")=="UNAVAILABLE" or (
        guide.get("status") in {
            "NO_RECORDED_METHOD_ROUTE",
            "NO_SAFE_METHOD_PROFILE",
            "METHOD_PROFILE_RECONCILIATION_REQUIRED",
        })
    if blocked and action!="suggest":
        raise ValueError("Reconcile unavailable project guidance before exploring options")

    # First three in documented catalogue order, NOT the top three by
    # goodness, similarity, popularity or evidence-based ranking.
    other=next((x for x in cards if x["id"]=="OTHER_NOT_LISTED"),None)
    primary=[x for x in cards if x["id"]!="OTHER_NOT_LISTED"][:3]
    shown=primary + ([other] if other else [])
    response={
        "schema":SCHEMA,"action":action,"status":guide.get("status"),
        "mode":guide.get("mode"),
        "target_field":guide.get("target_field"),
        "decision_dimension":guide.get("decision_dimension"),
        "route_recorded":guide.get("route_recorded"),
        "cards":[],
        "compared":[],
        "selected_for_exploration":None,
        "option_count":len(cards),
        "shown_as_unranked_catalogue_examples":True,
        "researcher_question_inferred_from_text":False,
        "method_recommended_or_selected":False,
        "selection_written":False,
        "gate_approved":False,
        "human_reviewer_authenticated":False,
        "source_evidence_verified_by_dialogue":False,
        "canonical_state_modified":False,
        "drive_sync_verified":False,
        "human_action":{
            "required_now_to_explore":False,
            "required_to_commit_scientific_choice":True,
            "required_for_independent_academic_validation":True,
            "required_for_merge_or_publication":True,
        },
        "next_choices":[],
        "limitations":[
            "The alternatives come from a curated catalogue, not a semantic assessment of the research question.",
            "None is automatically the best, complete, or scientifically validated route.",
            "The researcher can reject the catalogue and propose another method.",
        ],
    }
    if blocked:
        response["status"]="GUIDANCE_UNAVAILABLE_RECONCILIATION_REQUIRED"
        response["next_choices"]=[]
        response["human_action"]["required_now_to_explore"]=True
        return response

    # Not applicable is not the same as a missing canonical field.
    if guide.get("status")=="NOT_UNIVERSALLY_APPLICABLE":
        response["cards"]=[_identity(other)] if other else []
        response["next_choices"]=["describe_another_tradition","change_dimension"]
        return response

    if action=="suggest":
        response["cards"]=[_identity(c) for c in shown]
        response["next_choices"]=["explore_option","compare_two_options",
                                  "show_all_options","describe_another_tradition",
                                  "defer_decision"]
        response["navigation_question"]="Which approach would you like to explore or compare? You may also propose your own."
    elif action=="all":
        response["cards"]=[_identity(c) for c in cards]
        response["next_choices"]=["explore_option","compare_two_options",
                                  "describe_another_tradition","defer_decision"]
    elif action=="explore":
        card=next(x for x in cards if x["id"]==option_id)
        response["cards"]=[_details(card)]
        response["selected_for_exploration"]=option_id
        response["next_choices"]=["compare_with_another","return_to_options",
                                  "request_human_decision","defer_decision"]
        response["navigation_question"]="What makes this path appropriate to your actual question and evidence?"
    elif action=="compare":
        left,right=(next(x for x in cards if x["id"]==name) for name in compare_ids)
        response["compared"]=[_details(left),_details(right)]
        response["next_choices"]=["explore_option","compare_another_pair",
                                  "request_human_decision","defer_decision"]
        response["navigation_question"]="Which assumptions, evidence requirements, and limitations matter most in your research?"
    else:  # decision
        response["cards"]=[_identity(c) for c in shown]
        response["decision_status"]="HUMAN_DECISION_NOT_YET_OBTAINED"
        response["navigation_question"]=(
            "Please state your chosen approach (including an unlisted one, if needed), "
            "your scientific rationale, alternatives considered and its limitations. "
            "Only an actual attributable researcher decision may be registered "
            "through the existing authorized method-decision workflow.")
        response["next_choices"]=["researcher_states_own_decision","defer_decision",
                                  "compare_two_options"]
    return response

def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project",nargs="?",type=Path)
    parser.add_argument("--preview-route",choices=ROUTES)
    group=parser.add_mutually_exclusive_group()
    group.add_argument("--dimension",choices=DIMENSIONS)
    group.add_argument("--field")
    parser.add_argument("--action",choices=ACTIONS,default="suggest")
    parser.add_argument("--option-id")
    parser.add_argument("--compare",nargs=2,metavar=("OPTION_A","OPTION_B"))
    args=parser.parse_args(argv)
    if args.project and args.preview_route:
        parser.error("Project and preview route are mutually exclusive")
    try:
        g=(for_project(args.project,dimension=args.dimension,field=args.field)
           if args.project else
           preview(args.preview_route or "UNDECIDED",
                   dimension=args.dimension,field=args.field))
        out=dialogue(g,action=args.action,option_id=args.option_id,
                     compare_ids=tuple(args.compare) if args.compare else None)
    except (OSError,ValueError,TypeError,UnicodeError,json.JSONDecodeError) as exc:
        print("METHOD_DIALOGUE_ERROR: "+type(exc).__name__+": "+str(exc),file=sys.stderr)
        return 2
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
