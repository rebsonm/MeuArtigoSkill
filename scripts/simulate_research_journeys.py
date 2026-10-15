#!/usr/bin/env python3
"""Fictional end-to-end researcher-journey tests (NOT a human study).

Execute existing unranked guidance, exploration, comparison, hypothetical
human-like fixture choice, safe field proposal and conservative continuation
across method families. NO actual method decision, science-gate approval,
researcher identity, C.A.D.A. or canonical workspace is ever created.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

from adaptive_method_guide import preview
from method_choice_dialogue import dialogue
from method_decision_dimensions import DIMENSIONS, existing_field
from method_routes import REQUIRED_DESIGN, ROUTES, new_profile, profile_issues

SCHEMA = "MEU_ARTIGO_FICTIONAL_JOURNEY_V1"
ACTOR = "SYNTHETIC_FIXTURE_NOT_A_REAL_RESEARCHER"

# Explicitly fictional *questions*, not academic sources or real participants.
# A research question is a setup context; no classifier claims to have read it.
CASES = (
    ("JRN-001", "QUALITATIVE", "sampling", "PURPOSIVE", "MAX_VARIATION",
     "Fictional inquiry into professional experiences with a new work interface."),
    ("JRN-002", "QUANTITATIVE", "analysis", "DESCRIPTIVE_COMPARISON", "REGRESSION_OR_MODELLING",
     "Fictional description of administrative completion rates in a bounded sample."),
    ("JRN-003", "SYSTEMATIC_REVIEW", "sampling", "DOCUMENT_ELIGIBILITY", "PILOT_CRITERIA",
     "Fictional review of papers on administrative transparency."),
    ("JRN-004", "CONCEPTUAL_THEORY", "analysis", "LOGICAL_ARGUMENT", "CONCEPTUAL_RECONSTRUCTION",
     "Fictional conceptual argument about accountability."),
    ("JRN-005", "MIXED_METHODS", "analysis", "JOINT_DISPLAY", "SEQUENTIAL_INTEGRATION",
     "Fictional joint interpretation of service statistics and interviews."),
    ("JRN-006", "DESIGN_SCIENCE", "analysis", "CONTROLLED_ARTIFACT_TEST", "REAL_CONTEXT_EVALUATION",
     "Fictional evaluation of a research-management prototype."),
    ("JRN-007", "INTEGRATIVE_REVIEW", "analysis", "THEMATIC_INTEGRATION", "EXPLANATORY_COMPARISON",
     "Fictional integrative synthesis of work-related technology studies."),
    ("JRN-008", "PROBLEMATIZING_REVIEW", "inference", "BOUNDED_CRITIQUE", "CONDITIONAL_PROPOSITION",
     "Fictional questioning of institutional efficiency assumptions."),
)

def _validate_fixture(case: dict) -> None:
    if not isinstance(case,dict) or case.get("actor_type") != ACTOR:
        raise ValueError("Only explicitly labeled fictional actors are allowed")
    route=case.get("route")
    if route not in ROUTES or route=="UNDECIDED":
        raise ValueError("Known supported route required; unlisted routes need human mapping")
    if case.get("dimension") not in DIMENSIONS:
        raise ValueError("Unrecognized methodological decision dimension")
    if not isinstance(case.get("question"),str) or not (20<=len(case["question"])<=500):
        raise ValueError("Fictional question must be bounded and recorded")
    if not case["question"].startswith("Fictional "):
        raise ValueError("Only fabricated questions are allowed in this test")
    if not isinstance(case.get("rationale"),str) or len(case["rationale"].split())<6:
        raise ValueError("Explicit fictional rationale required before proposing continuation")

def _event(step: str, status: str, *, actor: str="SOFTWARE", next_actor: str="SOFTWARE") -> dict:
    return {"step":step,"status":status,"performed_by":actor,
            "next_responsible":next_actor,"scientific_gate_approved":False,
            "real_human_decision_obtained":False}

def fictional_case(case: dict) -> dict:
    """Evaluate a complete *virtual* trajectory in memory, not project files."""
    _validate_fixture(case)
    code,route,dimension=case["id"],case["route"],case["dimension"]
    # The initial question is considered an unverified fictional proposal.
    events=[_event("question","SYNTHETIC_QUESTION_PROPOSED")]
    families=dialogue(preview(),action="suggest")
    if route not in {x["id"] for x in dialogue(preview(),action="all")["cards"]}:
        raise ValueError("Route not offered; cannot silently remap it")
    if families["gate_approved"]:
        raise ValueError("Scientific gate erroneously approved during discovery")
    events.append(_event("family_options","UNRANKED_ALTERNATIVES_SHOWN"))
    guide=preview(route,dimension=dimension)
    intro=dialogue(guide,action="suggest")
    all_cards=dialogue(guide,action="all")
    codes={x["id"] for x in all_cards["cards"]}
    a,b=case.get("choice_id"),case.get("comparison_id")
    if not isinstance(a,str) or not isinstance(b,str) or a==b or a not in codes or b not in codes:
        raise ValueError("Choice and comparator must be distinct existing catalogue options")
    # This action is an engineering fixture, NOT genuine researcher consent.
    exploration=dialogue(guide,action="explore",option_id=a)
    comparison=dialogue(guide,action="compare",compare_ids=(a,b))
    events.append(_event("method_options","UNRANKED_DIMENSION_OPTIONS_SHOWN"))
    events.append(_event("explore","CHOICE_EXPLAINED_WITH_LIMITS"))
    events.append(_event("compare","TWO_ALTERNATIVES_CONTRASTED"))
    human_prompt=dialogue(guide,action="decision")
    if human_prompt.get("decision_status")!="HUMAN_DECISION_NOT_YET_OBTAINED":
        raise ValueError("Dialogue must not simulate a genuine researcher approval")
    # This is intentionally NOT passed to choose_method_route.py; the actor
    # is fictional, and that script is reserved for real human declarations.
    events.append(_event("fictional_choice","FIXTURE_ONLY_CHOICE_NOT_AUTHENTICATED",
                         actor=ACTOR,next_actor="SOFTWARE"))
    profile=new_profile(route)
    next_fields=list(REQUIRED_DESIGN[route])
    mapped=existing_field(route,dimension)
    # Propose the correct canonical location without writing a value.
    proposal={"target_existing_field":mapped,
              "is_additional_canonical_field":False,
              "proposed_entry_status":"NOT_WRITTEN",
              "choice_id_for_illustration":a,
              "researcher_must_validate_and_write":True,
              "suggested_content_elements":[
                  "How this approach fits the research question",
                  "Evidence/material requirements",
                  "Why competing approaches are less appropriate",
                  "Limits of permitted conclusions",
              ]}
    if mapped is None:
        proposal["proposal_kind"]="EXPLORATION_WITHOUT_CANONICAL_FIELD"
    else:
        if mapped not in profile["route_details"]:
            raise ValueError("Unrecognized target field; refuse unsafe write")
        proposal["proposal_kind"]="EXISTING_METHOD_PROFILE_FIELD_ONLY"
    events.append(_event("prepare_fill","ILLUSTRATIVE_INPUT_ONLY_NOT_WRITTEN",
                         next_actor="HUMAN_RESEARCHER"))
    if not profile_issues(profile,route,gate="GATE-0002"):
        raise ValueError("A blank unconfirmed method profile cannot pass gate-2")
    # A genuine canonical next step must be obtained separately from the
    # existing next_step_router with actual canonical continuity and gates.
    continuation={
        "status":"HUMAN_METHOD_DECISION_REQUIRED_FOR_REAL_PROJECT",
        "researcher_next_action":"State and justify the actual methodological choice before canonical recording.",
        "next_unfilled_canonical_method_field":next_fields[0] if next_fields else None,
        "method_field_value_written":False,
        "method_route_confirmation":"PENDING_HUMAN_DECISION",
        "actual_next_step_router_executed":False,
        "can_preapprove_gate_0002":False,
        "technical_work_possible":"Prepare method comparisons and field explanations only",
        "requires_authorized_storage_for_persistent_writes":True,
        "requires_real_human_researcher_choice":True,
        "independent_method_validation_required_to_claim_accuracy":True,
    }
    events.append(_event("continuation","REAL_HUMAN_DECISION_STILL_REQUIRED",
                         next_actor="HUMAN_RESEARCHER"))
    # No raw fictional questions or rationale even in synthetic CI artifacts.
    result={
        "schema":SCHEMA,"case_id":code,"research_route":route,
        "decision_dimension":dimension,
        "fictional_question_sha256":hashlib.sha256(case["question"].encode("utf-8")).hexdigest(),
        "fixture_label":"SYNTHETIC_AUTHOR_CONSTRUCTED_NOT_A_HUMAN_STUDY",
        "illustrative_approach":a,
        "exploration_verified":bool(exploration["cards"] and exploration["cards"][0].get("limits")),
        "compared_ids":[x["id"] for x in comparison["compared"]],
        "options_shown_count":len(intro["cards"]),
        "option_catalogue_count":len(all_cards["cards"]),
        "unlisted_route_available":any(x["id"]=="OTHER_NOT_LISTED" for x in all_cards["cards"]),
        "events":events,
        "proposal":proposal,"continuation":continuation,
        "original_canonical_profile_unchanged":profile["route_confirmation"]=="PENDING_HUMAN_DECISION",
        "researcher_decision_authenticated":False,
        "researcher_decision_saved":False,
        "semantic_method_suitability_validated":False,
        "gate_approved":False,
        "project_created_or_modified":False,
        "source_evidence_checked":False,
        "external_academic_data_accessed":False,
        "google_drive_sync_verified":False,
        "real_participants_involved":False,
    }
    return result

def simulated_cases() -> list[dict]:
    return [
      {"id":id,"route":route,"dimension":dimension,
       "choice_id":choice_id,"comparison_id":comparison_id,"question":question,
       "rationale":"This fictional decision compares methodological alternatives and acknowledges limits of scientific inference.",
       "actor_type":ACTOR}
      for id,route,dimension,choice_id,comparison_id,question in CASES
    ]

def run() -> dict:
    inputs=simulated_cases()
    if len({x["id"] for x in inputs})!=len(inputs):
        raise ValueError("Synthetic case identifiers must be unique")
    cases=[fictional_case(c) for c in inputs]
    return {
        "schema":"MEU_ARTIGO_SYNTHETIC_JOURNEY_EVALUATION_V1",
        "case_count":len(cases),
        "scenarios_performed":len(cases),
        "virtual_trajectory_steps_each":6,
        "route_coverage":sorted(x["research_route"] for x in cases),
        "human_decision_is_only_a_simulated_fixture":True,
        "independent_academic_validation":False,
        "real_human_judgments_collected":0,
        "canonical_workspace_mutated":False,
        "seven_scientific_gates_modified":False,
        "google_drive_synced":False,
        "actual_next_step_router_executed":False,
        "all_cases_preserve_human_gate":all(not x["gate_approved"] for x in cases),
        "case_results":cases,
        "limitations":[
            "Scenario questions and decisions are fictional developer-authored inputs.",
            "This reports deterministic software flow coverage, NOT academic suitability or actual researcher usability.",
            "No real human chose or authenticated a research method.",
            "A real project must check authorized storage and canonical continuity before any persisted change.",
        ],
    }

def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,
                        help="New nonexisting path for synthetic results (otherwise print JSON)")
    args=parser.parse_args(argv)
    try:
        result=run()
        data=json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n"
        if args.output is None:
            print(data,end="")
        else:
            dest=args.output
            if dest.exists() or dest.is_symlink() or not dest.parent.is_dir():
                raise ValueError("Output must be a new file in an existing directory")
            with dest.open("x",encoding="utf-8") as stream:
                stream.write(data)
            print(json.dumps({"status":"SYNTHETIC_REPORT_WRITTEN",
                              "output_file":dest.name,
                              "case_count":len(result["case_results"]),
                              "academic_validation":False},sort_keys=True))
        return 0
    except (ValueError,OSError,TypeError,KeyError,json.JSONDecodeError) as exc:
        print("JOURNEY_EVALUATION_ERROR: "+type(exc).__name__+": "+str(exc),file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
