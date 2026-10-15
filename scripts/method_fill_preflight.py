#!/usr/bin/env python3
"""Preventive, read-only preflight for proposed methodological field entries.

This guard checks only *structural* compatibility, known workflow states and
declared route/field. It neither invents a scientific rationale nor certifies
semantic suitability; nothing is ever written to METHOD_PROFILE or any gate.
The proposing researcher's confidential draft is never echoed to output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

from adaptive_method_guide import for_project, preview
from method_decision_dimensions import DIMENSIONS
from method_routes import (
    INFERENCE_AIMS, INTEGRATION_TYPES, MIXED_DESIGNS, REQUIRED_DESIGN, ROUTES
)

SCHEMA="MEU_ARTIGO_METHOD_FILL_PREFLIGHT_V1"
LIMIT_BYTES=12_000
ENUM_FIELDS={
    ("QUANTITATIVE","inference_aim"):INFERENCE_AIMS,
    ("MIXED_METHODS","mixed_design"):MIXED_DESIGNS,
    ("MIXED_METHODS","integration_type"):INTEGRATION_TYPES,
}
# Block only exact placeholder values; a researcher may discuss "pending"
# as an actual subject without it being a fabricated workflow status.
PLACEHOLDER_VALUES={
    "","pending","not executed","not_executed","to do","tbd","todo",
    "a definir","nao definido","não definido","preencher","placeholder",
    "insert text here","lorem ipsum","n/a","na","none","null","unknown",
    "pendente","not available","no data yet","em branco",
    "human confirmed","human_confirmed","approved","aprovado",
    "completed","complete","done","yes","sim",
    "pending_human_decision",
}
def normalize(value: str) -> str:
    text=unicodedata.normalize("NFKD",value.strip().casefold())
    return " ".join("".join(c for c in text if not unicodedata.combining(c)).split())

PLACEHOLDER_NORMALIZED={normalize(x) for x in PLACEHOLDER_VALUES}

def _finding(code: str, reason: str, *, blocking: bool) -> dict:
    return {"code":code,"reason":reason,"blocking":blocking}

def _read_draft(path: Path) -> str:
    if path.is_symlink() or not path.is_file() or path.stat().st_size>LIMIT_BYTES:
        raise ValueError("Draft file is missing, unsafe, or exceeds size limit")
    data=path.read_bytes()
    if len(data)>LIMIT_BYTES:
        raise ValueError("Draft exceeds allowed size limit")
    return data.decode("utf-8")

def inspect(guide: dict, *, proposal: str|None=None,
            option_id: str|None=None) -> dict:
    """Explain field and evaluate a candidate, never write or approve it."""
    if not isinstance(guide,dict):
        raise ValueError("Invalid guide payload")
    route=guide.get("route_recorded") or guide.get("preview_route")
    preview_only=guide.get("bound_to_canonical_project") is False
    # A preview knows the *illustrative* route but cannot authorize writes.
    field=guide.get("target_field")
    cards=guide.get("options") or []
    if not isinstance(cards,list) or not all(isinstance(c,dict) for c in cards):
        raise ValueError("Guide contains invalid option cards")
    card_ids=[c.get("id") for c in cards]
    if any(not isinstance(x,str) or not x for x in card_ids) or len(card_ids)!=len(set(card_ids)):
        raise ValueError("Guide contains missing/duplicate option IDs")
    if option_id is not None and option_id not in card_ids:
        raise ValueError("Option must be one available under the actual method route and field")
    if proposal is not None and not isinstance(proposal,str):
        raise ValueError("Draft must be researcher-supplied plain text")
    if proposal is not None and len(proposal.encode("utf-8"))>LIMIT_BYTES:
        raise ValueError("Draft exceeds size limit")
    blocked=guide.get("mode")=="UNAVAILABLE" or guide.get("status") in {
        "NO_SAFE_METHOD_PROFILE","METHOD_PROFILE_RECONCILIATION_REQUIRED",
        "NO_RECORDED_METHOD_ROUTE","NOT_UNIVERSALLY_APPLICABLE",
    }
    canonical_field=isinstance(field,str) and field in REQUIRED_DESIGN.get(route,())
    already_filled=guide.get("target_field_already_recorded") is True
    findings=[]
    if blocked:
        findings.append(_finding("GUIDANCE_NOT_READY",
            "Canonical method profile is unavailable, inconsistent or this requirement is not applicable.",blocking=True))
    if preview_only:
        findings.append(_finding("PREVIEW_NOT_CANONICAL_AUTHORIZATION",
            "An illustrative preview is not an authorized research project's decision.",blocking=True))
    if field is None or not canonical_field:
        findings.append(_finding("NO_CANONICAL_FIELD",
            "This orientation dimension cannot be written into the current method profile.",blocking=True))
    if already_filled:
        findings.append(_finding("EXISTING_DECISION_REQUIRES_REVIEW",
            "An existing field is already recorded. A deliberate superseding review is needed.",blocking=True))
    if route=="UNDECIDED":
        findings.append(_finding("RESEARCH_METHOD_UNDECIDED",
            "An undecided method cannot authorize a field-level scientific entry.",blocking=True))
    if proposal is not None:
        raw=proposal.strip()
        if normalize(raw) in PLACEHOLDER_NORMALIZED:
            findings.append(_finding("PLACEHOLDER_NOT_EVIDENCE",
                "A status marker or placeholder is not a substantive methodological statement.",blocking=True))
        elif not raw or any(ord(x)<32 and x not in "\n\t\r" for x in raw):
            findings.append(_finding("INVALID_DRAFT_TEXT",
                "Draft is empty or has invalid control characters.",blocking=True))
        else:
            allowed=ENUM_FIELDS.get((route,field))
            if allowed and raw not in allowed:
                findings.append(_finding("INVALID_CANONICAL_ENUM",
                    "Field requires one of the existing canonical design labels.",blocking=True))
            # This can be legitimate prose, not an automatic hard stop.
            if allowed is None and len(raw.split())<4:
                findings.append(_finding("BRIEF_DRAFT_NEEDS_EXPLANATION",
                    "A short entry may lack the scope, rationale and boundaries of the choice.",blocking=False))
            if re.search(r"\b(?:has been (?:validated|proven)|"
                         r"was proven effective|100% reliable|"
                         r"comprovadamente eficaz|validado cientificamente)\b",raw,re.I):
                findings.append(_finding("ASSERTED_VALIDATION_NEEDS_EVIDENCE",
                    "Claims of empirical or scientific validation need authentic, inspectable evidence.",blocking=False))
    if option_id=="OTHER_NOT_LISTED":
        findings.append(_finding("UNLISTED_METHOD_NEEDS_MAPPING",
            "An unlisted tradition needs researcher justification and deliberate methodological mapping.",blocking=True))
    blocking=any(x["blocking"] for x in findings)
    substantive=proposal is not None and bool(proposal.strip())
    status=("BLOCKED_BEFORE_WRITING" if blocking
            else "DRAFT_REQUIRES_HUMAN_REVIEW" if substantive
            else "GUIDANCE_ONLY_NO_DRAFT")
    option=next((x for x in cards if x.get("id")==option_id),None)
    return {
        "schema":SCHEMA,
        "status":status,
        "route_recorded":guide.get("route_recorded"),
        "preview_route":guide.get("preview_route"),
        "bound_to_canonical_project":not preview_only and bool(guide.get("bound_to_canonical_project")),
        "target_field":field,
        "decision_dimension":guide.get("decision_dimension"),
        "route_previously_human_confirmed":guide.get("route_previously_human_confirmed") is True,
        "target_field_already_recorded":already_filled,
        "entry_has_existing_canonical_field":canonical_field,
        "option_id_for_discussion":option_id,
        "option_explanation":None if option is None else {
            "label":option["label"],
            "why_consider":option["when_to_consider"],
            "limits":option["limits"],
            "planning_consequences":option["what_changes_next"],
        },
        "suggested_entry_elements":[
            "State the methodological choice or procedure precisely.",
            "Explain how it addresses the actual research question.",
            "Name required material, assumptions and feasible procedures.",
            "Compare reasonable alternatives and justify the researcher's decision.",
            "State what the design does not establish.",
        ],
        "field_specific_constraints":(
            sorted(ENUM_FIELDS[(route,field)])
            if (route,field) in ENUM_FIELDS else None),
        "findings":findings,
        "blocking_finding_count":sum(x["blocking"] for x in findings),
        "warnings_count":sum(not x["blocking"] for x in findings),
        "proposed_draft_supplied":proposal is not None,
        "proposed_draft_sha256":(
            hashlib.sha256(proposal.encode("utf-8")).hexdigest()
            if proposal is not None else None),
        "draft_text_exported":False,
        "draft_text_persisted":False,
        "researcher_choice_authenticated":False,
        "semantic_suitability_verified":False,
        "source_evidence_checked":False,
        "scientific_gate_approved":False,
        "safe_to_write_automatically":False,
        "canonical_project_modified":False,
        "drive_sync_verified":False,
        "human_action":{
            "required_now_to_view_guidance":False,
            "required_to_accept_or_reject_proposal":True,
            "required_to_authorize_any_real_change":True,
            "independent_scientific_validation_required_later":True,
        },
        "limitations":[
            "Structural preflight cannot establish that the selected method scientifically fits the study.",
            "An absence of flags never authenticates a researcher's choice or source evidence.",
            "A real authorized, transactional write must separately verify gates, consent and canonical storage.",
        ],
    }

def for_existing_project(project: Path, *, field: str|None=None,
                         dimension: str|None=None, proposal: str|None=None,
                         option_id: str|None=None) -> dict:
    # The existing guide detects route/profile inconsistency and does not
    # expose source text or private method rationale.
    g=for_project(project,field=field,dimension=dimension)
    return inspect(g,proposal=proposal,option_id=option_id)

def main(argv=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("project",type=Path,help="An existing authorized research project")
    selection=p.add_mutually_exclusive_group()
    selection.add_argument("--field")
    selection.add_argument("--dimension",choices=DIMENSIONS)
    p.add_argument("--option-id")
    p.add_argument("--draft-file",type=Path,
                   help="Read a locally authorized UTF-8 draft without echoing its text")
    a=p.parse_args(argv)
    try:
        proposal=_read_draft(a.draft_file) if a.draft_file is not None else None
        report=for_existing_project(a.project,field=a.field,
                       dimension=a.dimension,proposal=proposal,option_id=a.option_id)
        print(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True))
        return 2 if report["blocking_finding_count"] else 0
    except (ValueError,OSError,TypeError,UnicodeError,json.JSONDecodeError) as exc:
        print("METHOD_PREFLIGHT_ERROR: "+type(exc).__name__,file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
