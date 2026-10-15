#!/usr/bin/env python3
"""Read-only adaptive methodological choices for a research canvas-like view.

This is an *orientation interface* backed by existing method profile fields,
NOT a research-design validator, scientific method ontology or a replacement
for an accountable researcher decision. Every candidate is non-ranking and
context-dependent; unlisted methods remain possible. No model inference,
network, persistence, gateway change, or automatic selection occurs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from method_routes import MGMT, PROFILE, ROUTES, REQUIRED_DESIGN

FIELD_MENU = {
    ("INTEGRATIVE_REVIEW", "review_scope"): [
        ("CONCEPTUAL_BOUNDARY", "Scope by concepts and explanatory tensions",
         "When an explanatory conversation rather than exhaustive effect estimation is central.",
         "Supports thematic integration across relevant traditions.",
         "Selection is selective; disclose important unavailable or excluded traditions.",
         "Define conceptual boundaries, inclusion rationale and how divergent studies will be integrated."),
        ("CONTEXT_BOUNDARY", "Scope by phenomenon, setting and period",
         "When a bounded setting or period makes interpretation coherent.",
         "Facilitates transparent source selection and transferability limits.",
         "A narrow setting cannot justify universal conclusions.",
         "Record setting/period boundaries and a transparent synthesis plan."),
    ],
    ("SYSTEMATIC_REVIEW", "review_scope"): [
        ("EFFECT_OR_INTERVENTION", "Question focused on intervention or association",
         "When the review asks about an effect, intervention or measurable comparison.",
         "Permits an explicit eligibility structure, where appropriate.",
         "No design or checklist guarantees complete retrieval or causal certainty.",
         "Define concepts, comparators if relevant, outcomes and a search/quality protocol."),
        ("PHENOMENON_OR_EXPERIENCE", "Question focused on a phenomenon or experience",
         "When qualitative evidence or contexts rather than effects are central.",
         "Allows a transparent systematic synthesis of appropriate qualitative studies.",
         "An intervention-only framework may exclude relevant interpretive evidence.",
         "Define eligible perspectives, contexts, study types and suitable appraisal."),
    ],
    ("PROBLEMATIZING_REVIEW", "assumptions_to_question"): [
        ("DOMINANT_ASSUMPTION", "Interrogate a dominant assumption",
         "When a field rests on a premise that deserves explicit challenge.",
         "Opens new theoretical questions and conceptual alternatives.",
         "Selective sampling needs a transparent rationale, not fictitious exhaustiveness.",
         "Identify the assumption, intellectual antecedents and defensible counterpositions."),
        ("CONTRADICTORY_POSITIONS", "Compare competing theoretical positions",
         "When different traditions give incompatible accounts of a phenomenon.",
         "Makes conceptual tensions and alternative framings visible.",
         "Avoid treating a difference in terminology as a substantive contradiction.",
         "Select original works representing competing positions and compare their premises."),
    ],
    ("CONCEPTUAL_THEORY", "theoretical_problem"): [
        ("CONCEPTUAL_INCONSISTENCY", "Resolve a conceptual tension",
         "When definitions or conceptual boundaries conflict.",
         "Supports careful construct clarification and bounded propositions.",
         "A definitional difference alone does not establish an original contribution.",
         "Identify rival definitions, original sources and boundary conditions."),
        ("MECHANISM_EXPLANATION", "Develop or critique an explanatory mechanism",
         "When existing accounts leave a causal or generative mechanism underspecified.",
         "Supports explicit premises, counterexamples and explanatory scope.",
         "A proposed mechanism is not an empirically verified effect.",
         "List assumptions, closest prior models, counterarguments and testable implications if appropriate."),
    ],
    ("QUALITATIVE", "tradition"): [
        ("PHENOMENOLOGY", "Phenomenological inquiry",
         "When the central question concerns lived experience and meaning.",
         "Provides detailed attention to experiential accounts.",
         "Specific philosophical variants differ; do not equate all interviews with phenomenology.",
         "Choose the phenomenological tradition, materials and coherent interpretation strategy."),
        ("CASE_STUDY", "Qualitative case study",
         "When a bounded case and its context are central.",
         "Supports multiple relevant materials and contextual explanation.",
         "A case requires defensible boundaries; case studies are not all alike.",
         "Define case, unit of analysis, access and case-specific analysis."),
        ("ETHNOGRAPHY", "Ethnographic inquiry",
         "When situated practices and cultural processes require sustained engagement.",
         "Permits observation of practices and meanings in context.",
         "Requires appropriate access, positioning and ethical safeguards.",
         "Specify field engagement, observations and reflexivity."),
        ("GROUNDED_THEORY", "Grounded theory approach",
         "When the goal is developing theory grounded in systematically analyzed material.",
         "Offers iterative data collection, comparison and conceptual development.",
         "Versions differ; coding alone does not make research grounded theory.",
         "Justify the tradition, sampling, constant comparison and saturation/adequacy logic."),
        ("NARRATIVE", "Narrative inquiry",
         "When stories and their organization over time are the object of inquiry.",
         "Supports interpretation of temporality, voice and plot.",
         "Needs appropriate ethical treatment of identifiable narratives.",
         "Clarify narrative perspective, materials and analytic treatment."),
    ],
    ("QUALITATIVE", "material_sources"): [
        ("INTERVIEWS", "Interviews or conversational material",
         "When accounts of experience or practice are needed.",
         "Can produce rich participant perspectives.",
         "Recruitment, ethics and response bias may apply.",
         "Define inclusion, consent where applicable and analysis strategy."),
        ("DOCUMENTS", "Documentary material",
         "When records, texts or artifacts directly inform the question.",
         "Can support research without direct participant interaction.",
         "Document provenance, access rights and representativeness still matter.",
         "Define corpus boundaries, provenance and source criticism."),
        ("OBSERVATION", "Observation or field records",
         "When actual practices and interactions matter.",
         "Captures situated action, not only retrospective accounts.",
         "Access, positioning and privacy may constrain observation.",
         "Define the setting, observation strategy and ethical safeguards."),
    ],
    ("QUANTITATIVE", "inference_aim"): [
        ("DESCRIPTIVE", "Descriptive estimation",
         "When the goal is to estimate characteristics or frequencies.",
         "Makes a target quantity and relevant uncertainty explicit.",
         "Non-representative sampling limits population generalization.",
         "Specify target population, measures, denominator and missingness."),
        ("ASSOCIATIONAL", "Associational analysis",
         "When the question concerns co-occurrence or statistical relations.",
         "Can investigate relationships under declared assumptions.",
         "Association alone is not a causal effect.",
         "Specify constructs, confounding risks, sample and model."),
        ("PREDICTIVE", "Prediction",
         "When performance on future or unseen cases is the primary aim.",
         "Supports held-out evaluation and calibration.",
         "Predictive accuracy does not explain causes or prove deployment safety.",
         "Specify prediction target, validation design, leakage prevention and drift risks."),
        ("CAUSAL", "Causal inference",
         "When an intervention or exposure effect must be identified.",
         "Encourages explicit counterfactual assumptions and identification.",
         "Causal claims require credible design; a regression alone is insufficient.",
         "Specify treatment, comparator, assumptions and an identification strategy."),
    ],
    ("MIXED_METHODS", "mixed_design"): [
        ("CONVERGENT", "Convergent design",
         "When qualitative and quantitative strands address complementary dimensions concurrently.",
         "Allows comparison or merging of findings.",
         "Parallel strands without genuine integration are not mixed-method inference.",
         "State where evidence will merge and how discrepancies will be handled."),
        ("EXPLANATORY_SEQUENTIAL", "Explanatory sequential design",
         "When quantitative findings need qualitative follow-up explanation.",
         "Provides deeper interpretation of quantitative patterns.",
         "Sampling for the second strand must follow the first for a defensible reason.",
         "Specify QUAN-to-QUAL connection, sampling and meta-inference."),
        ("EXPLORATORY_SEQUENTIAL", "Exploratory sequential design",
         "When qualitative exploration informs later measurement or testing.",
         "Links construct development to subsequent quantitative work.",
         "New measures still need appropriate validation.",
         "Specify QUAL-to-QUAN building and validation steps."),
        ("EMBEDDED", "Embedded mixed-method design",
         "When one strand serves a defined purpose within another design.",
         "Can illuminate processes alongside outcomes.",
         "The supporting strand cannot simply be decorative.",
         "Describe the embedding, interfaces and inferential boundaries."),
    ],
    ("DESIGN_SCIENCE", "problem_context"): [
        ("DEFINED_USE_CASE", "Bounded use-case and requirements",
         "When an artifact addresses a clearly delimited task or user need.",
         "Supports traceable requirements and evaluation criteria.",
         "An implemented prototype is not evidence of effectiveness.",
         "Specify user context, task conditions, constraints and evaluation."),
        ("STAKEHOLDER_TENSIONS", "Competing stakeholder requirements",
         "When several roles have different needs, risks or success criteria.",
         "Makes trade-offs and evaluation claims explicit.",
         "Requirements elicitation does not prove that an artifact meets them.",
         "Specify stakeholders, traceable constraints and comparison criteria."),
    ],
}

ROUTE_MENU = [
    ("INTEGRATIVE_REVIEW", "Integrative literature review",
     "When critical integration across a bounded body of literature is the research aim.",
     "Can synthesize distinct evidence and explanatory tensions.",
     "Does not imply that every source has been retrieved.",
     "Justify review scope, source selection and synthesis logic."),
    ("SYSTEMATIC_REVIEW", "Systematic review",
     "When explicit eligibility, planned retrieval and auditable synthesis answer the question.",
     "Enables transparent study identification and appraisal.",
     "A checklist alone does not establish review quality or completeness.",
     "Specify protocol, information sources, quality appraisal and synthesis."),
    ("PROBLEMATIZING_REVIEW", "Problematizing review",
     "When assumptions in an existing theoretical conversation are under question.",
     "Can expose hidden premises and generate alternative framings.",
     "Requires justified selective reading rather than automatic exhaustive screening.",
     "Identify assumptions, opposed accounts and interpretive strategy."),
    ("CONCEPTUAL_THEORY", "Conceptual/theoretical research",
     "When the contribution is conceptual clarification, argument or model building.",
     "Makes theoretical premises and counterarguments explicit.",
     "Does not imply participant recruitment or statistical tests.",
     "Specify closest prior work, logic of argument and its limits."),
    ("QUALITATIVE", "Qualitative inquiry",
     "When meaning, context, processes or experiences require interpretation.",
     "Supports situated understanding of phenomena.",
     "No single qualitative tradition or coding procedure fits every question.",
     "Choose a defensible tradition, material and analytic strategy."),
    ("QUANTITATIVE", "Quantitative inquiry",
     "When units, measurements and bounded estimates or models address the question.",
     "Supports explicit quantities and uncertainty.",
     "Method selection depends on inference aim, not on available software.",
     "Define population, measures, sampling and inferential limits."),
    ("MIXED_METHODS", "Mixed-method inquiry",
     "When a reasoned integration of qualitative and quantitative strands is necessary.",
     "Allows complementary perspectives and integrated inference.",
     "Two adjacent methods alone do not constitute integration.",
     "Explain the integration purpose, sequence and meta-inference."),
    ("DESIGN_SCIENCE", "Design science",
     "When construction and evaluation of an artifact form part of the inquiry.",
     "Connects requirements, design rationale and observed evaluation results.",
     "Building a solution alone does not demonstrate its effectiveness.",
     "Define the artifact, requirements, evaluation criteria and limitations."),
]

# Applicability of suggestions is NOT inferred from researcher prose.
def _card(row: tuple[str, str, str, str, str, str]) -> dict:
    key, label, when, potential, limits, consequences = row
    return {"id":key,"label":label,"when_to_consider":when,
            "potential":potential,"limits":limits,
            "what_changes_next":consequences,
            "recommendation_rank":None,"scientific_approval":False}

OTHER = _card((
    "OTHER_NOT_LISTED", "Another approach / discipline-specific tradition",
    "When no offered path adequately describes the scientific problem or epistemology.",
    "Preserves researcher-defined, hybrid, normative, historical, philosophical, mathematical or other designs.",
    "The existing route taxonomy may need deliberate extension; do not silently force a category.",
    "Ask the researcher to name the tradition and justify fit; map it explicitly before applying route-specific gates."))

def _read_json(path: Path) -> dict:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 1_000_000:
        raise ValueError("Required canonical configuration/profile unavailable or unsafe")
    data=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data,dict):
        raise ValueError("Canonical configuration/profile must be an object")
    return data

def _field_candidates(route: str, field: str) -> list[dict]:
    choices=FIELD_MENU.get((route,field))
    if not choices:
        # Honest unranked prompts rather than inventing domain-specific choices
        choices=[
            ("BOUNDED_DESIGN", "Make a bounded, justified design decision",
             "When a clear, narrow design can address the stated research question.",
             "Creates a defensible basis for further work.",
             "Needs explicit epistemological and practical justification.",
             "Describe the intended procedure, alternatives and limits."),
            ("COMPARE_FRAMEWORKS", "Compare established traditions before deciding",
             "When competing approaches differ in assumptions or procedures.",
             "Keeps the design choice open while alternatives are investigated.",
             "No tradition can be selected solely from its name or popularity.",
             "Consult appropriate methodological literature and request a researcher decision."),
        ]
    return [_card(row) for row in choices]+[OTHER]

def preview(route: str="UNDECIDED", field: str|None=None) -> dict:
    """Source-neutral, illustrative map with no claims about any real project."""
    if route not in ROUTES:
        raise ValueError("Unrecognized existing route; use OTHER_NOT_LISTED instead")
    requirements=REQUIRED_DESIGN.get(route,())
    if field is not None and field not in requirements:
        raise ValueError("Field does not belong to the declared methodology")
    selected=field or (requirements[0] if requirements else None)
    return _response(route, selected, {}, "ILLUSTRATIVE_PREVIEW", False,
                     project_bound=False, route_confirmed=False)

def _response(route: str, field: str|None, completed: dict,
              status: str, can_explore: bool, *,
              project_bound: bool, route_confirmed: bool) -> dict:
    mode="DISCOVER_METHOD_FAMILY" if route=="UNDECIDED" else "EXPLORE_METHOD_FIELD"
    options=[_card(row) for row in ROUTE_MENU]+[OTHER] if mode=="DISCOVER_METHOD_FAMILY" \
            else _field_candidates(route,field)
    return {
        "schema":"MEU_ARTIGO_ADAPTIVE_METHOD_GUIDE_V1",
        "mode":mode,"status":status,"route_recorded":route if project_bound else None,
        "route_previously_human_confirmed":route_confirmed if project_bound else False,
        "target_field":field,"field_value_exported":False,
        "researcher_goal_inferred_from_prose":False,
        "options":options,"option_count":len(options),
        "all_options_unranked":True,"provisional_only":True,
        "other_method_allowed":True,"custom_combination_requires_justification":True,
        "researcher_selection_recorded":False,
        "selection_persists_to_project":False,
        "human_scientific_gate_approved":False,
        "drive_sync_confirmed":False,
        "technical_preparation_possible":can_explore,
        "human_action":{
            "needed_now_to_browse":False,
            "needed_to_confirm_scientific_choice":True,
            "needed_for_independent_method_validation":True,
            "can_defer_independent_validation_during_prototype":True,
            "responsibility":"RESEARCHER_FOR_REAL_DECISION",
        },
        "map":[
            {"id":"PURPOSE","status":"NOT_EVALUATED_BY_GUIDE"},
            {"id":"PRIOR_KNOWLEDGE","status":"NOT_EVALUATED_BY_GUIDE"},
            {"id":"RESEARCH_DESIGN","status":
             "HUMAN_RECORDED_NOT_INDEPENDENTLY_VALIDATED" if route_confirmed
             else "PROVISIONAL_OR_UNDECIDED"},
            {"id":"MATERIALS","status":"NOT_EVALUATED_BY_GUIDE"},
            {"id":"ANALYSIS_AND_EVIDENCE","status":"NOT_EVALUATED_BY_GUIDE"},
            {"id":"CONTRIBUTION_AND_LIMITS","status":"NOT_EVALUATED_BY_GUIDE"},
        ],
        "route_detail_progress":{
            "fields_completed_structurally":completed.get("filled",0),
            "fields_expected":completed.get("total",len(REQUIRED_DESIGN.get(route,()))),
            "does_not_certify_methodological_correctness":True},
        "limitations":[
            "Static options explain possible approaches; they are not tailored semantic recommendations.",
            "Researcher may reject all suggestions or use an unlisted tradition.",
            "Only actual recorded researcher decisions may authorize a methodological gate.",
            "This read-only view does not modify the project or verify Google Drive writes.",
        ],
    }

def for_project(root: Path, *, field: str|None=None) -> dict:
    """Read the actual method route without leaking confidential project text."""
    root=Path(root).resolve()
    config=_read_json(root/MGMT/"PROJECT_CONFIG.json")
    route=config.get("method_route")
    if route not in ROUTES:
        raise ValueError("Invalid or unknown canonical methodology")
    profile_path=root/PROFILE
    if profile_path.is_symlink() or not profile_path.is_file():
        return {"schema":"MEU_ARTIGO_ADAPTIVE_METHOD_GUIDE_V1",
                "status":"NO_SAFE_METHOD_PROFILE","mode":"UNAVAILABLE",
                "options":[],"option_count":0,
                "human_scientific_gate_approved":False,
                "selection_persists_to_project":False,
                "technical_preparation_possible":False}
    profile=_read_json(profile_path)
    if (profile.get("schema_version")!=1 or
        profile.get("route")!=route or
        not isinstance(profile.get("route_details"),dict)):
        return {"schema":"MEU_ARTIGO_ADAPTIVE_METHOD_GUIDE_V1",
                "status":"METHOD_PROFILE_RECONCILIATION_REQUIRED",
                "mode":"UNAVAILABLE","options":[],"option_count":0,
                "human_scientific_gate_approved":False,
                "selection_persists_to_project":False,
                "technical_preparation_possible":False}
    needed=REQUIRED_DESIGN.get(route,())
    if field is not None and field not in needed:
        raise ValueError("Requested field not in canonical method route")
    values=profile["route_details"]
    next_missing=next((name for name in needed
                       if not str(values.get(name) or "").strip()),None)
    selected=field if field is not None else next_missing
    done=sum(bool(str(values.get(name) or "").strip()) for name in needed)
    status="OPTIONS_FOR_HUMAN_EXPLORATION"
    if not needed:
        status="METHOD_FAMILY_UNDECIDED"
    elif selected is None:
        status="ALL_DESIGN_FIELDS_RECORDED_NOT_SCIENTIFICALLY_APPROVED"
        selected=needed[0]
    elif str(values.get(selected) or "").strip():
        status="FIELD_ALREADY_RECORDED_REVIEW_BEFORE_CHANGE"
    confirmed=profile.get("route_confirmation")=="HUMAN_CONFIRMED"
    result=_response(route,selected,{"filled":done,"total":len(needed)},status,
                     True,project_bound=True,route_confirmed=confirmed)
    result["target_field_already_recorded"]=bool(str(values.get(selected) or "").strip()) if selected else False
    return result

def main(argv=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("project",nargs="?",type=Path)
    p.add_argument("--preview-route",choices=ROUTES)
    p.add_argument("--field")
    p.add_argument("--all-options",action="store_true",
                   help="Retain all route options (default already includes every supported route)")
    args=p.parse_args(argv)
    if args.project and args.preview_route:
        p.error("A project and an illustrative --preview-route are mutually exclusive")
    try:
        doc=for_project(args.project,field=args.field) if args.project else \
            preview(args.preview_route or "UNDECIDED",field=args.field)
    except (OSError,ValueError,UnicodeError,json.JSONDecodeError) as exc:
        print("METHOD_GUIDE_ERROR: "+type(exc).__name__,file=sys.stderr)
        return 2
    print(json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
