#!/usr/bin/env python3
"""Official, human-acknowledged canonical method-field writer.

Integrates the preventive methodological preflight INTO the supported write
path. Uses the existing five-file method-route journal to record METHOD
decision, TRACE and profile field atomically, without changing the route,
seven gates, or Drive canonical state. Human identity and evidence are
declared, NOT independently authenticated. Direct external edits bypass
this command and must be detected at gate validation.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import io
import json
from pathlib import Path
import sys

from governance_events import record_decision
from method_fill_preflight import (_read_draft, for_existing_project,
                                  normalize, PLACEHOLDER_NORMALIZED)
from method_route_transaction import (
    has_pending_method_route, protect_method_route, PendingMethodRouteTransaction,
    recover_method_route,
)
from method_routes import MGMT, REQUIRED_DESIGN, ROUTES
from transaction_coordinator import require_no_conflict

BLOCKED_GATE_STATUSES={"COMPLETED","NOT_APPLICABLE"}
BLOCKED_GATE_DECISIONS={"APPROVED","APPROVED_WITH_CHANGES","NOT_APPLICABLE"}

def _safe_file(root: Path, name: str) -> Path:
    p=root/MGMT/name
    if p.is_symlink() or not p.is_file():
        raise ValueError("Required canonical governance file unavailable or unsafe")
    return p

def _read_csv(path: Path) -> list[dict[str,str]]:
    with path.open(encoding="utf-8-sig",newline="") as stream:
        return list(csv.DictReader(stream))

def _attestation(value: str, label: str, minimum: int) -> str:
    if not isinstance(value,str) or len(value.strip())<minimum or \
       normalize(value) in PLACEHOLDER_NORMALIZED:
        raise ValueError("Actual researcher "+label+" is required")
    return value.strip()

def _read_state(root: Path, field: str) -> tuple[dict, dict]:
    cfg=json.loads(_safe_file(root,"PROJECT_CONFIG.json").read_text(encoding="utf-8"))
    profile=json.loads(_safe_file(root,"METHOD_PROFILE.json").read_text(encoding="utf-8"))
    if not isinstance(cfg,dict) or not isinstance(profile,dict):
        raise ValueError("Canonical method configuration/profile must be JSON objects")
    route=cfg.get("method_route")
    if cfg.get("method_route_governance_required") is not True:
        raise ValueError("Legacy projects require deliberate migration, not silent edits")
    if (route not in ROUTES or route=="UNDECIDED" or
        profile.get("schema_version")!=1 or profile.get("route")!=route or
        profile.get("route_confirmation")!="HUMAN_CONFIRMED"):
        raise ValueError("A confirmed canonical method route is required before field changes")
    details=profile.get("route_details")
    if not isinstance(details,dict) or field not in REQUIRED_DESIGN[route] or field not in details:
        raise ValueError("The field is not a defined canonical method-route detail")
    for att in ("human_route_reviewer","human_route_decision_evidence","human_route_rationale"):
        if normalize(str(profile.get(att) or "")) in PLACEHOLDER_NORMALIZED:
            raise ValueError("Existing method-route confirmation lacks substantive provenance")
    did=profile.get("route_decision_id")
    if not isinstance(did,str) or not did.startswith("DEC-"):
        raise ValueError("Confirmed route requires a registered DEC_ID")
    decisions=_read_csv(_safe_file(root,"17_Decision_Log.csv"))
    if not any(
        x.get("DEC_ID")==did and x.get("Decision_type")=="METHOD"
        and x.get("Decision")==route and x.get("Status") in {"APPROVED","FROZEN"}
        and (x.get("Decided_by") or "").strip() for x in decisions
    ):
        raise ValueError("Confirmed route lacks matching human-declared METHOD decision")
    gates=_read_csv(_safe_file(root,"18_Human_Validation_Gates.csv"))
    if any(
        x.get("GATE_ID") in {"GATE-0002","GATE-0003","GATE-0004","GATE-0005","GATE-0006","GATE-0007"}
        and ((x.get("Status") or "").upper() in BLOCKED_GATE_STATUSES or
             (x.get("Decision") or "").upper() in BLOCKED_GATE_DECISIONS)
        for x in gates
    ):
        raise ValueError("Approved/closed scientific gate requires explicit reopening/revision before editing")
    return cfg,profile

def commit(root: Path, *, field: str, proposed_text: str,
           decided_by: str, evidence: str, rationale: str,
           confirmed_by_researcher: bool,
           option_id: str|None=None, acknowledge_warnings: bool=False) -> dict:
    """One controlled write after a *declared* genuine human decision.

    This is never called on an AI-generated or fictional human attestation.
    Invariant: failures before or within transaction do not partially update
    the METHOD_PROFILE, DEC log, TRACE or gates.
    """
    root=Path(root).resolve()
    if not confirmed_by_researcher:
        raise ValueError("Explicit real researcher review/authorization required")
    person=_attestation(decided_by,"name",3)
    ref=_attestation(evidence,"decision evidence reference",8)
    why=_attestation(rationale,"scientific rationale",20)
    if len(why.split())<6:
        raise ValueError("Human method rationale must explain the substantive decision")
    if not isinstance(field,str) or not field.strip():
        raise ValueError("Explicit canonical field required")
    if not isinstance(proposed_text,str):
        raise ValueError("Field text must be provided by the researcher")
    # Hash, DEC/TRACE checksum and committed bytes refer to the same text.
    proposed_text=proposed_text.strip()
    require_no_conflict(root)
    if has_pending_method_route(root):
        raise PendingMethodRouteTransaction("METHOD_ROUTE_TRANSACTION_PENDING_RECOVERY_REQUIRED")
    _read_state(root,field)
    first=for_existing_project(root,field=field,proposal=proposed_text,option_id=option_id)
    if first["blocking_finding_count"]:
        raise ValueError("METHOD_PREFLIGHT_BLOCKED: "+
                         ",".join(x["code"] for x in first["findings"] if x["blocking"]))
    if first["warnings_count"] and not acknowledge_warnings:
        raise ValueError("METHOD_PREFLIGHT_WARNINGS_REQUIRE_EXPLICIT_HUMAN_ACKNOWLEDGMENT")
    # Re-evaluate everything while holding the existing recoverable journal.
    # The commit is local ONLY; filesystem journaling cannot protect against
    # unrelated external writers that ignore journal protocols.
    with protect_method_route(root):
        cfg,profile=_read_state(root,field)
        check=for_existing_project(root,field=field,proposal=proposed_text,option_id=option_id)
        if check["blocking_finding_count"]:
            raise ValueError("METHOD_PREFLIGHT_BLOCKED_IN_TRANSACTION")
        if check["warnings_count"] and not acknowledge_warnings:
            raise ValueError("METHOD_PREFLIGHT_WARNINGS_REQUIRE_EXPLICIT_HUMAN_ACKNOWLEDGMENT")
        decision_args=argparse.Namespace(
            project=str(root),type="METHOD",status="APPROVED",stage="02-03",
            question="Researcher methodological detail: "+field,
            decision=field+" formally recorded; declared value checksum "+check["proposed_draft_sha256"],
            alternatives=option_id or "Researcher-provided method choice",
            rationale=why,evidence=ref,decided_by=person,
            evidence_ids="",record_ids="",cada_id="",gate_id="",
            impact="Method field updated locally; not a gate approval",
            artifacts=MGMT+"/METHOD_PROFILE.json",
            resulting_version="",supersedes="",notes="Field entry recorded from declared researcher authorization; not independently authenticated.")
        # The governance writer appends the existing DEC/TRACE; the journal
        # rolls it back if the profile cannot be written afterwards.
        stream=io.StringIO()
        with contextlib.redirect_stdout(stream):
            record_decision(decision_args)
        id_line=next((x for x in stream.getvalue().splitlines()
                      if x.startswith("decision_id=")),None)
        if id_line is None:
            raise ValueError("No DEC_ID returned for method field decision")
        did=id_line.split("=",1)[1]
        profile["route_details"][field]=proposed_text.strip()
        _safe_file(root,"METHOD_PROFILE.json").write_text(
            json.dumps(profile,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return {
        "status":"DECLARED_RESEARCHER_METHOD_FIELD_RECORDED_NOT_AUTHENTICATED",
        "decision_id":did,"route":cfg["method_route"],"field":field,
        "value_sha256":check["proposed_draft_sha256"],
        "preflight_status":check["status"],
        "warning_count_acknowledged":check["warnings_count"],
        "field_value_echoed":False,"real_researcher_identity_independently_authenticated":False,
        "scientific_suitability_validated":False,
        "scientific_gate_approved":False,
        "local_transaction_committed":True,"google_drive_sync_verified":False,
    }

def main(argv=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("project",type=Path)
    p.add_argument("--field")
    p.add_argument("--draft-file",type=Path)
    p.add_argument("--decided-by",default="")
    p.add_argument("--evidence",default="")
    p.add_argument("--rationale",default="")
    p.add_argument("--option-id")
    p.add_argument("--researcher-reviewed",action="store_true")
    p.add_argument("--acknowledge-warnings",action="store_true")
    p.add_argument("--recover-pending",action="store_true")
    a=p.parse_args(argv)
    if a.recover_pending:
        if a.field or a.draft_file or a.decided_by or a.evidence or a.rationale or a.researcher_reviewed:
            p.error("Recovery must not be combined with a new scientific decision")
        try:
            print(json.dumps(recover_method_route(a.project),sort_keys=True))
            return 0
        except (ValueError,OSError,PendingMethodRouteTransaction) as exc:
            p.error(type(exc).__name__)
    if not a.field or a.draft_file is None:
        p.error("--field and --draft-file required")
    try:
        result=commit(a.project,field=a.field,proposed_text=_read_draft(a.draft_file),
                      decided_by=a.decided_by,evidence=a.evidence,
                      rationale=a.rationale,confirmed_by_researcher=a.researcher_reviewed,
                      option_id=a.option_id,acknowledge_warnings=a.acknowledge_warnings)
        print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
        return 0
    except (ValueError,OSError,TypeError,UnicodeError,json.JSONDecodeError,
            PendingMethodRouteTransaction) as exc:
        print("METHOD_WRITE_REJECTED: "+type(exc).__name__,file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
