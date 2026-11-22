#!/usr/bin/env python3
"""Read-only change signals for existing canonical methodological fields.

Detects literal/enum changes; it DOES NOT determine semantic significance,
revalidate a scientific decision, or traverse actual project dependencies.
"""
from __future__ import annotations

from method_routes import (REQUIRED_DESIGN, INFERENCE_AIMS,
                           MIXED_DESIGNS, INTEGRATION_TYPES)

SCHEMA = "MEU_ARTIGO_METHOD_CHANGE_IMPACT_V1"

ENUM_FIELDS = {
    ("QUANTITATIVE", "inference_aim"): INFERENCE_AIMS,
    ("MIXED_METHODS", "mixed_design"): MIXED_DESIGNS,
    ("MIXED_METHODS", "integration_type"): INTEGRATION_TYPES,
}

# Curated *potential* dependencies. These are not executable dependency edges.
# Fields not listed are still compared, but receive no fabricated downstream map.
ROUTE_REVIEW_HINTS = {
    "INTEGRATIVE_REVIEW": {
        "selection_logic": ("review_scope", "appraisal_logic", "synthesis_logic"),
    },
    "SYSTEMATIC_REVIEW": {
        "eligibility_criteria": ("comprehensive_search_plan", "screening_protocol",
                                 "risk_of_bias_plan", "synthesis_logic"),
    },
    "PROBLEMATIZING_REVIEW": {
        "assumptions_to_question": ("selection_logic", "counterpositions",
                                    "interpretive_strategy"),
    },
    "CONCEPTUAL_THEORY": {
        "theoretical_problem": ("closest_prior_work", "argument_strategy",
                                "boundary_conditions"),
    },
    "QUALITATIVE": {
        "sampling_logic": ("context_or_case", "material_sources", "analysis_logic",
                           "reflexivity_or_positioning"),
    },
    "QUANTITATIVE": {
        "inference_aim": ("population_or_unit", "sampling_logic",
                          "constructs_and_measures", "data_sources",
                          "analysis_plan", "identification_or_inference_limits"),
    },
    "MIXED_METHODS": {
        "mixed_design": ("quantitative_strand", "qualitative_strand",
                         "integration_point", "meta_inference_plan", "discordance_plan"),
        "integration_type": ("integration_point", "meta_inference_plan",
                             "discordance_plan"),
    },
    "DESIGN_SCIENCE": {
        "evaluation_plan": ("design_requirements", "evaluation_criteria",
                            "non_evaluated_claim_limits"),
    },
}

# These are explicitly conditional review topics, NOT extra profile fields,
# decisions, gates, or claims proven to be affected.
POTENTIAL_DOWNSTREAM = {
    ("QUANTITATIVE", "inference_aim"):
        ("claims_and_conclusions_if_any", "prior_gate_decisions_if_any"),
    ("MIXED_METHODS", "mixed_design"):
        ("integration_claims_if_any", "prior_gate_decisions_if_any"),
    ("DESIGN_SCIENCE", "evaluation_plan"):
        ("evaluation_claims_if_any", "prior_gate_decisions_if_any"),
}


def _bounded_outcome(route: str, field: str) -> dict:
    if route not in REQUIRED_DESIGN or field not in REQUIRED_DESIGN[route]:
        raise ValueError("Change preview requires an existing canonical method field")
    return {
        "schema": SCHEMA,
        "route": route,
        "field": field,
        "status": "NO_RECORDED_BASELINE",
        "change_detected": False,
        "comparison_basis": "NO_COMPARISON",
        "potential_review_targets": [],
        "review_map_coverage": "NONE",
        "human_review_may_be_needed": False,
        "recorded_value_disclosed": False,
        "proposed_value_disclosed": False,
        "actual_dependency_edges_verified": False,
        "affected_decisions_or_claims_identified": False,
        "scientific_adequacy_verified": False,
        "scientific_gate_approved": False,
        "project_modified": False,
    }


def preview_change(route: str, field: str, previous: object, proposed: object,
                   *, proposal_eligible: bool = True) -> dict:
    """Preview one requested field change; never log/return private text.

    Conservative comparison: only exact sameness or surrounding whitespace /
    line-ending differences are treated as nonchanges. All other prose edits
    are UNKNOWN in semantic effect and require human evaluation.
    """
    result = _bounded_outcome(route, field)
    old = previous if isinstance(previous, str) else ""
    new = proposed if isinstance(proposed, str) else ""
    if not proposal_eligible or not new.strip():
        result["status"] = "INVALID_OR_BLOCKED_PROPOSAL_NOT_COMPARED"
        return result
    if not old.strip():
        return result
    allowed = ENUM_FIELDS.get((route, field))
    if allowed is not None and (old.strip() not in allowed or new.strip() not in allowed):
        result["status"] = "INVALID_CANONICAL_ENUM_NOT_COMPARED"
        return result
    if old == new:
        result["status"] = "IDENTICAL_FIELD_NO_NEW_REVIEW"
        result["comparison_basis"] = "EXACT_STRING_EQUALITY"
        return result
    if old.replace("\r\n", "\n").strip() == new.replace("\r\n", "\n").strip():
        result["status"] = "BOUNDARY_FORMATTING_ONLY_NO_NEW_REVIEW"
        result["comparison_basis"] = "LINE_ENDINGS_OR_BOUNDARY_WHITESPACE"
        return result

    result["status"] = ("CANONICAL_DESIGN_LABEL_CHANGED_REVIEW_REQUIRED"
                        if allowed is not None else
                        "TEXT_CHANGED_SEMANTIC_IMPACT_UNKNOWN")
    result["comparison_basis"] = ("CANONICAL_ENUM_DIFFERENCE"
                                  if allowed is not None else "TEXT_DIFFERENCE")
    result["change_detected"] = True
    result["human_review_may_be_needed"] = True
    hinted = ROUTE_REVIEW_HINTS.get(route, {}).get(field)
    result["potential_review_targets"] = ([field] + list(hinted or ()) +
                                          list(POTENTIAL_DOWNSTREAM.get((route, field), ())))
    result["review_map_coverage"] = ("CURATED_POTENTIAL_TARGETS"
                                     if hinted else "FIELD_ONLY_UNMAPPED")
    return result
