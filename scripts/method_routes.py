#!/usr/bin/env python3
"""Method-aware research routes and existing-gate semantics for Meu Artigo.

This is a *structural* check, not semantic appraisal or scientific validation.
Never infer an executed study from a filled field; the recorded human decision
and original evidence remain necessary and independently auditable.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

MGMT = "00_Gestao_e_Continuidade"
PROFILE = f"{MGMT}/METHOD_PROFILE.json"
ROUTES = (
    "UNDECIDED", "INTEGRATIVE_REVIEW", "SYSTEMATIC_REVIEW",
    "PROBLEMATIZING_REVIEW", "CONCEPTUAL_THEORY", "QUALITATIVE",
    "QUANTITATIVE", "MIXED_METHODS", "DESIGN_SCIENCE",
)
REVIEW_ROUTES = {"INTEGRATIVE_REVIEW", "SYSTEMATIC_REVIEW", "PROBLEMATIZING_REVIEW"}
EMPIRICAL_ROUTES = {"QUALITATIVE", "QUANTITATIVE", "MIXED_METHODS", "DESIGN_SCIENCE"}
DATA_ROUTES = {"QUALITATIVE", "QUANTITATIVE", "MIXED_METHODS"}
EVIDENCE_STAGES = {"GATE-0004", "GATE-0005"}
INFERENCE_AIMS = {"DESCRIPTIVE", "ASSOCIATIONAL", "PREDICTIVE", "CAUSAL"}
MIXED_DESIGNS = {"CONVERGENT", "EXPLANATORY_SEQUENTIAL", "EXPLORATORY_SEQUENTIAL", "EMBEDDED"}
INTEGRATION_TYPES = {"CONNECTING", "BUILDING", "MERGING", "EMBEDDING"}
REQUIRED_DESIGN = {
    "INTEGRATIVE_REVIEW": ("review_scope", "selection_logic", "appraisal_logic", "synthesis_logic"),
    "SYSTEMATIC_REVIEW": ("review_scope", "eligibility_criteria", "comprehensive_search_plan",
                          "screening_protocol", "risk_of_bias_plan", "synthesis_logic"),
    "PROBLEMATIZING_REVIEW": ("assumptions_to_question", "selection_logic",
                               "counterpositions", "interpretive_strategy"),
    "CONCEPTUAL_THEORY": ("theoretical_problem", "closest_prior_work",
                          "argument_strategy", "boundary_conditions"),
    "QUALITATIVE": ("tradition", "context_or_case", "sampling_logic",
                    "material_sources", "analysis_logic", "reflexivity_or_positioning"),
    "QUANTITATIVE": ("inference_aim", "population_or_unit", "sampling_logic",
                     "constructs_and_measures", "data_sources", "analysis_plan",
                     "identification_or_inference_limits"),
    "MIXED_METHODS": ("mixed_design", "quantitative_strand", "qualitative_strand",
                      "integration_reason", "integration_type", "integration_point",
                      "meta_inference_plan", "discordance_plan"),
    "DESIGN_SCIENCE": ("problem_context", "artefact_type", "design_requirements",
                       "construction_plan", "evaluation_plan",
                       "evaluation_criteria", "non_evaluated_claim_limits"),
}
# Existing IDs/columns are deliberately retained; no new scientific gates.
GATE_VARIANTS = {
    "INTEGRATIVE_REVIEW": {
        "GATE-0003": ("SEARCH_STRATEGY", "Search strategy", "Document the structured search, sources and selection rationale.", "Literal searches, scope, filters, actual executions and declared limits."),
        "GATE-0004": ("CORPUS_FREEZE", "Eligible review corpus", "Screened sources and actually accessed material reconciled.", "Eligible corpus, human decisions and source counts, without overstating coverage."),
        "GATE-0005": ("SYNTHESIS", "Integrative synthesis", "Genuine comparison and integration of consulted evidence.", "Tensions, convergences, alternatives and bounded propositions."),
    },
    "SYSTEMATIC_REVIEW": {
        "GATE-0003": ("SEARCH_STRATEGY", "Systematic-review search", "Comprehensive strategy appropriate to the real protocol and question.", "Executed queries, databases, dates, updates and known limitations."),
        "GATE-0004": ("CORPUS_FREEZE", "Eligibility and final corpus", "Selection of eligible candidate records completed and checked.", "Eligibility criteria, conflicts, exclusions, reconciled counts and appraisal."),
        "GATE-0005": ("SYNTHESIS", "Systematic-review synthesis", "Synthesis executed according to the declared appropriate protocol.", "Eligible evidence, risk of bias, heterogeneity and inference limits."),
    },
    "PROBLEMATIZING_REVIEW": {
        "GATE-0003": ("SELECTIVE_LITERATURE", "Critical selective literature", "Justified theoretical source selection without presumed exhaustiveness.", "Assumptions, counterpositions, selection logic and documented boundaries."),
        "GATE-0004": ("THEORETICAL_MATERIALS", "Interpreted theoretical material", "Relevant original sources and positions compared with provenance.", "Material actually consulted and important positions not examined."),
        "GATE-0005": ("THEORETICAL_ARGUMENT", "Problematization and synthesis", "Assumptions and alternatives explicitly argued.", "Revised assumptions, analytical inferences and counterarguments."),
    },
    "CONCEPTUAL_THEORY": {
        "GATE-0003": ("THEORETICAL_POSITIONING", "Literature positioning", "Bound the actual scholarly conversation and nearby articles.", "Relevant selection and verifiable gaps without mandatory exhaustive retrieval."),
        "GATE-0004": ("THEORETICAL_MATERIALS", "Conceptual foundation", "Concepts and intellectual antecedents actually consulted.", "Prior work, counterexamples, boundaries and source provenance."),
        "GATE-0005": ("THEORETICAL_ARGUMENT", "Theoretical contribution", "Conceptual argument examined against the literature.", "Propositions, mechanisms, alternatives, implications and limits."),
    },
    "QUALITATIVE": {
        "GATE-0003": ("LITERATURE_POSITIONING", "Literature and context", "Position the phenomenon without imposing a systematic review.", "Relevant works, epistemological perspective and bounded gaps."),
        "GATE-0004": ("EMPIRICAL_MATERIALS", "Qualitative empirical material", "Real material, access and selection decisions documented.", "Context, empirical corpus, applicable consent/ethics and materials trail."),
        "GATE-0005": ("QUALITATIVE_ANALYSIS", "Qualitative analysis and interpretation", "Actual analytic procedures documented and examined.", "Evidence, interpretive reasoning, reflexivity, disagreements and transferability."),
    },
    "QUANTITATIVE": {
        "GATE-0003": ("LITERATURE_POSITIONING", "Theory and hypotheses", "Bound the question, models and relevant comparisons.", "Relevant constructs, prior work and hypotheses; no automatic exhaustive review."),
        "GATE-0004": ("EMPIRICAL_MATERIALS", "Data and measurement", "Actual data and sampling procedures documented.", "Units, observed sample, instruments, variables, data quality and ethics."),
        "GATE-0005": ("QUANTITATIVE_ANALYSIS", "Statistical analysis and inference", "Analyses really performed and their limitations examined.", "Results, assumptions, uncertainty and causal identification limits."),
    },
    "MIXED_METHODS": {
        "GATE-0003": ("LITERATURE_POSITIONING", "Rationale for both strands", "The research question warrants combined methodological strands.", "Relevant foundations and specific purpose of each strand."),
        "GATE-0004": ("EMPIRICAL_MATERIALS", "Materials for both strands", "Genuine QUAN and QUAL components, not only planned labels.", "Sampling and collection, ethics and intended strand sequencing."),
        "GATE-0005": ("MIXED_INTEGRATION", "Integration and meta-inference", "Actual integration documented, not mere juxtaposition.", "Integration point, convergences, contradictions and bounded meta-inference."),
    },
    "DESIGN_SCIENCE": {
        "GATE-0003": ("PROBLEM_KNOWLEDGE", "Requirements and prior knowledge", "Defensible problem requirements and literature identified.", "Knowledge base, stakeholders and justified requirements."),
        "GATE-0004": ("ARTEFACT_CONSTRUCTION", "Artifact construction", "Actual artifact and design choices documented.", "Versions, requirements, technical decisions, constraints and source materials."),
        "GATE-0005": ("ARTEFACT_EVALUATION", "Artifact evaluation", "An evaluation procedure actually executed.", "Criteria, real results, limitations and unsupported claims."),
    },
}


def infer_route(article_type: str) -> str:
    """Backward-compatible suggestions; ambiguous labels remain UNDECIDED."""
    import unicodedata
    value = unicodedata.normalize("NFKD", str(article_type or "").casefold())
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = " ".join(value.replace("-", " ").replace("_", " ").split())
    if not value or value in {"undecided", "indefinido", "a definir", "empirico", "empirical", "artigo"}:
        return "UNDECIDED"
    if "mixed" in value or "misto" in value or "mista" in value:
        return "MIXED_METHODS"
    if "design science" in value or "design based research" in value:
        return "DESIGN_SCIENCE"
    if "problematiz" in value:
        return "PROBLEMATIZING_REVIEW"
    if "sistemat" in value or "systematic" in value:
        return "SYSTEMATIC_REVIEW"
    if "integrativ" in value or "integrative" in value:
        return "INTEGRATIVE_REVIEW"
    if "quantit" in value:
        return "QUANTITATIVE"
    if "qualit" in value:
        return "QUALITATIVE"
    if "conceptual" in value or "conceitual" in value or "teoric" in value or "theor" in value:
        return "CONCEPTUAL_THEORY"
    return "UNDECIDED"


def new_profile(route: str, article_type: str = "") -> dict:
    if route not in ROUTES:
        raise ValueError(f"unsupported method route: {route}")
    return {
        "schema_version": 1,
        "route": route,
        "route_confirmation": "PENDING_HUMAN_DECISION",
        "route_decision_id": "",
        "human_route_reviewer": "",
        "human_route_decision_evidence": "",
        "human_route_rationale": "",
        "initial_article_label": article_type,
        "research_question": "",
        "intended_inference": "",
        "study_limits": "",
        "onion": {
            "philosophical_position_if_relevant": "",
            "theory_development_logic": "",
            "methodological_choice": "",
            "research_strategy": "",
            "time_horizon": "",
            "techniques_and_procedures": "",
            "coherence_rationale": "",
        },
        "route_details": {key: "" for key in REQUIRED_DESIGN.get(route, ())},
        "material_evidence_ref": "",
        "analysis_evidence_ref": "",
        "integration_evidence_ref": "",
        "evidence_status": "NOT_EXECUTED",
        "notes": "Planning template only; no data collection, evaluation or analysis is implied.",
    }


def gate_rows(route: str, base_rows: list[list[str]]) -> list[list[str]]:
    """Adapt the Name/type/entry/validation fields of existing gate rows."""
    if route not in ROUTES:
        raise ValueError(f"unsupported method route: {route}")
    out = [list(row) for row in base_rows]
    if route == "UNDECIDED":
        return out
    for row in out:
        gid = row[0]
        if gid == "GATE-0002":
            row[5] = ("Pergunta, inferência visada, abordagem e protocolo coerentes; "
                      "decisão do pesquisador e limites documentados.")
            row[4] = "Perfil metodológico preparado e escolhas justificadas pelo pesquisador."
            row[18] = 'Step relevant to the chosen design'
        elif gid in GATE_VARIANTS[route]:
            typ, name, entry, controls = GATE_VARIANTS[route][gid]
            row[1], row[3], row[4], row[5] = typ, name, entry, controls
    return out


def load(root: Path) -> dict:
    path = Path(root) / PROFILE
    if not path.is_file() or path.is_symlink():
        raise ValueError("METHOD_PROFILE.json absent or linked")
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError("method profile must be a JSON object")
    return doc


def profile_issues(doc: dict, route: str, *, gate: str | None = None) -> list[str]:
    """Syntactic/structural consistency only. Does not certify actual science."""
    problems = []
    if route not in ROUTES:
        return [f"unknown route: {route}"]
    if doc.get("schema_version") != 1 or doc.get("route") != route:
        return ["method profile schema/route diverges from PROJECT_CONFIG"]
    if gate is None:
        return problems
    if gate == "GATE-0002":
        if route == "UNDECIDED":
            return ["cannot approve method before researcher selects a specific route"]
        if doc.get("route_confirmation") != "HUMAN_CONFIRMED":
            problems.append("researcher has not confirmed route classification")
        for attestation in ("route_decision_id","human_route_reviewer",
                            "human_route_decision_evidence","human_route_rationale"):
            if not str(doc.get(attestation) or "").strip():
                problems.append(f"confirmed route lacks {attestation}")
        for field in ("research_question", "intended_inference", "study_limits"):
            if not str(doc.get(field) or "").strip():
                problems.append(f"method profile lacks {field}")
        details = doc.get("route_details") or {}
        if not isinstance(details, dict):
            return problems + ["route_details must be a record"]
        for field in REQUIRED_DESIGN[route]:
            if not str(details.get(field) or "").strip():
                problems.append(f"method profile lacks {field} for {route}")
        onion = doc.get("onion") or {}
        if route in EMPIRICAL_ROUTES:
            if not isinstance(onion, dict):
                problems.append("onion must be an object")
            else:
                for field in ("research_strategy", "techniques_and_procedures", "coherence_rationale"):
                    if not str(onion.get(field) or "").strip():
                        problems.append(f"onion planning lacks {field}")
        if route == "QUANTITATIVE" and details.get("inference_aim") not in INFERENCE_AIMS:
            problems.append("quantitative inference aim must be one of descriptive/associational/predictive/causal")
        if route == "MIXED_METHODS":
            if details.get("mixed_design") not in MIXED_DESIGNS:
                problems.append("mixed design needs a declared convergent/sequential/embedded structure")
            if details.get("integration_type") not in INTEGRATION_TYPES:
                problems.append("mixed design requires connecting/building/merging/embedding")
            if str(details.get("quantitative_strand") or "").strip() == str(details.get("qualitative_strand") or "").strip():
                problems.append("mixed strands cannot be identical placeholder descriptions")
    elif gate in EVIDENCE_STAGES and route in EMPIRICAL_ROUTES:
        evidence_status = doc.get("evidence_status")
        if gate == "GATE-0004":
            if evidence_status not in {"MATERIALS_DOCUMENTED", "ANALYSIS_DOCUMENTED"}:
                problems.append("empirical materials are not documented as collected/constructed")
            if not str(doc.get("material_evidence_ref") or "").strip():
                problems.append("empirical materials have no inspectable original evidence reference")
        elif gate == "GATE-0005":
            if evidence_status != "ANALYSIS_DOCUMENTED":
                problems.append("cannot approve results without documented executed analysis/evaluation")
            if not str(doc.get("analysis_evidence_ref") or "").strip():
                problems.append("analysis/evaluation has no original evidence reference")
            if route == "MIXED_METHODS" and not str(doc.get("integration_evidence_ref") or "").strip():
                problems.append("mixed methods has no documented integration evidence reference")
    return problems


def approval_issues(root: Path, cfg: dict, gate: str) -> list[str]:
    """Enforced only on approvals for new route-aware projects."""
    if cfg.get("method_route_governance_required") is not True:
        return []
    route = str(cfg.get("method_route") or "").strip()
    try:
        doc = load(root)
    except (ValueError, OSError, TypeError, json.JSONDecodeError) as exc:
        return [f"method profile unavailable: {type(exc).__name__}"]
    issues = profile_issues(doc, route, gate=gate)
    gate_path = Path(root)/MGMT/"18_Human_Validation_Gates.csv"
    with gate_path.open("r",encoding="utf-8-sig",newline="") as f:
        gates = {row.get("GATE_ID"):row for row in csv.DictReader(f)}
    previous = {
        "GATE-0002":"GATE-0001", "GATE-0003":"GATE-0002",
        "GATE-0004":"GATE-0003", "GATE-0005":"GATE-0004",
        "GATE-0006":"GATE-0005", "GATE-0007":"GATE-0006",
    }.get(gate)
    if previous:
        earlier=gates.get(previous) or {}
        if (earlier.get("Status") or "").upper() not in {"COMPLETED","NOT_APPLICABLE"} or (
            (earlier.get("Decision") or "").upper()
            not in {"APPROVED","APPROVED_WITH_CHANGES","NOT_APPLICABLE"}
        ):
            issues.append(f"prior scientific gate {previous} is not approved")
    if gate in {"GATE-0002", "GATE-0003", "GATE-0004", "GATE-0005", "GATE-0006", "GATE-0007"}:
        decision_file=Path(root)/MGMT/"17_Decision_Log.csv"
        try:
            with decision_file.open("r",encoding="utf-8-sig",newline="") as f:
                decisions=list(csv.DictReader(f))
            if not any(
                row.get("DEC_ID")==doc.get("route_decision_id")
                and row.get("Decision_type")=="METHOD"
                and row.get("Decision")==route
                and row.get("Status") in {"APPROVED","FROZEN"}
                and (row.get("Decided_by") or "").strip()
                and (row.get("Notes") or "").strip()
                for row in decisions
            ):
                issues.append("route lacks matching approved and attributable DEC_ID in decision log")
        except OSError:
            issues.append("route decision log cannot be read")
    if gate in {"GATE-0003", "GATE-0004", "GATE-0005", "GATE-0006", "GATE-0007"}:
        if route == "UNDECIDED":
            issues.append("method route still undecided")
        if cfg.get("method_route") != doc.get("route"):
            issues.append("project method route and profile disagree")
    return issues
