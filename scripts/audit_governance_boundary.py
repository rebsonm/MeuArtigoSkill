#!/usr/bin/env python3
"""Audit the distinction between C.A.D.A. work tracking and scientific evidence.

This deterministic, offline report measures recorded administrative state
only. It cannot establish research quality or a causal C.A.D.A. benefit.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

MGMT="00_Gestao_e_Continuidade"
FILES={
    "cada":"11_CADA_Control.csv",
    "gates":"18_Human_Validation_Gates.csv",
    "decisions":"17_Decision_Log.csv",
    "evidence":"05_Evidence_Matrix.csv",
    "claims":"09_Claims_Ledger.csv",
    "trace":"13_Traceability_Log.csv",
}
GATE_APPROVAL={"APPROVED","APPROVED_WITH_CHANGES"}
DONE={"DONE"}
# A task ID, an attestation or a bare completion flag is not source evidence.
TAUTOLOGIES={"DONE","COMPLETE","COMPLETED","APPROVED","APROVADO","CONCLUIDO",
             "CONCLUÍDO","CADA DONE","TASK COMPLETE","TASK COMPLETED",
             "CADA","CADA APPROVED","TASK CLOSED"}
SCIENCE_ONLY={
    "QUESTION","METHOD","SEARCH","ELIGIBILITY","EVIDENCE","SYNTHESIS",
    "CONCLUSION","VALIDATION",
}

def clean(value):
    return " ".join(str(value or "").split())

def normalized(value):
    return clean(value).upper()

def rows(root, filename):
    path=Path(root)/MGMT/filename
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig",newline="") as stream:
        reader=csv.DictReader(stream)
        records=list(reader)
    if any(None in r for r in records):
        raise ValueError(f"CSV has unexpected columns: {filename}")
    return records

def management_only(value):
    text=normalized(value)
    return text in TAUTOLOGIES or bool(re.fullmatch(r"CADA-\d{4,}",text))

def audit(root,*,strict=False):
    root=Path(root).resolve()
    records={name:rows(root,file) for name,file in FILES.items()}
    errors,warnings=[],[]
    tasks=[r for r in records["cada"] if clean(r.get("CADA_ID"))]
    done=[r for r in tasks if normalized(r.get("Status")) in DONE]
    purported=[r for r in done if management_only(r.get("Completion_evidence")) or
               not clean(r.get("Completion_evidence"))]
    for row in purported:
        (errors if strict else warnings).append(
            f"{row['CADA_ID']}: DONE lacks verifiable operational completion evidence"
        )
    gates=[r for r in records["gates"] if clean(r.get("GATE_ID"))]
    approved=[r for r in gates if normalized(r.get("Status"))=="COMPLETED"
              and normalized(r.get("Decision")) in GATE_APPROVAL]
    for gate in approved:
        gid=clean(gate.get("GATE_ID"))
        if management_only(gate.get("Validation_evidence")) or management_only(gate.get("Validation_method")):
            (errors if strict else warnings).append(
                f"{gid}: scientific approval cites only C.A.D.A. task status, not review evidence"
            )
    decisions=[r for r in records["decisions"] if clean(r.get("DEC_ID"))]
    evidenced=[r for r in records["evidence"] if clean(r.get("Evidence_ID"))]
    claims=[r for r in records["claims"] if clean(r.get("Claim_ID"))]
    traces=[r for r in records["trace"] if clean(r.get("Trace_ID"))]
    # Deliberately no combined quality score. Counts reflect recorded claims,
    # without endorsing source accuracy, research validity or human identity.
    return {
        "schema_version":1,
        "audit_kind":"MANAGEMENT_SCIENCE_BOUNDARY",
        "generated_at_utc":datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "management_activity":{
            "recorded_tasks":len(tasks),
            "tasks_marked_done":len(done),
            "done_without_meaningful_completion_evidence":len(purported),
            "scope":"Administrative work tracking only; not scientific outcomes.",
        },
        "scientific_registers":{
            "material_decisions_recorded":len(decisions),
            "gate_approvals_recorded":len(approved),
            "evidence_records":len(evidenced),
            "claims_registered":len(claims),
            "scope":"Counts of assertions and approvals, not independent scientific quality checks.",
        },
        "execution_provenance":{
            "trace_events":len(traces),
            "locally_confirmed":sum(normalized(r.get("Status"))=="CONFIRMED" for r in traces),
            "unverified":sum(normalized(r.get("Status"))=="UNVERIFIED" for r in traces),
            "scope":"Captured actions do not prove validity of literature or conclusions.",
        },
        "integrity":{"errors":errors,"warnings":warnings},
        "scientific_quality_validated":False,
        "causal_CADA_effect_established":False,
        "human_decision_authenticated":False,
        "interpretation":"C.A.D.A. can track process accountability, not certify research methods or demonstrate efficiency gains without independent comparisons.",
    }

def protocol_check(path):
    document=json.loads(Path(path).read_text(encoding="utf-8"))
    errors=[]
    if document.get("schema_version")!=1 or document.get("status")!="PROTOCOL_ONLY_NOT_EXECUTED":
        errors.append("comparison plan must declare a versioned, unexecuted protocol")
    arms=document.get("arms")
    if not isinstance(arms,list) or len(arms)!=2 or {
        str(a.get("id")) for a in arms
    }!={"CADA_ON","CADA_OFF"}:
        errors.append("comparison needs exactly two arms: CADA_ON and CADA_OFF")
    else:
        for a in arms:
            if a.get("scientific_protocol")!="SAME_FROZEN_RESEARCH_PROTOCOL":
                errors.append("both arms must retain identical scientific procedures")
            if a.get("scientific_gates")!="SAME_REQUIRED_GATES":
                errors.append("both arms must retain independent scientific validation safeguards")
        if arms[0].get("management_layer_enabled")==arms[1].get("management_layer_enabled"):
            errors.append("comparison arms must differ on the C.A.D.A. management layer")
    for key in ("paired_units","allocation","measurement_sources","primary_outcomes",
                "scientific_safety_outcomes","threats_to_validity"):
        if not document.get(key):
            errors.append(f"comparison plan missing {key}")
    if document.get("results") not in (None,{},[]):
        errors.append("unexecuted protocol must not include measured results")
    if document.get("observations") not in (None,{},[]):
        errors.append("unexecuted protocol must not contain observational rows")
    if document.get("effect_estimate") is not None:
        errors.append("unexecuted protocol must not claim a causal effect")
    return {"errors":errors,"status":"PROTOCOL_STRUCTURE_VALID" if not errors else "INVALID_PROTOCOL",
            "scientific_effect_established":False,"comparison_executed":False}

def safe_output(root,output):
    if not output:
        return None
    path=(root/output).resolve()
    if not path.is_relative_to(root) or path==root:
        raise ValueError("Audit report must be inside project workspace")
    return path

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    cmd=p.add_subparsers(dest="mode",required=True)
    a=cmd.add_parser("audit")
    a.add_argument("project")
    a.add_argument("--strict",action="store_true")
    a.add_argument("--output",default="")
    c=cmd.add_parser("check-plan")
    c.add_argument("protocol")
    args=p.parse_args(argv)
    try:
        if args.mode=="check-plan":
            result=protocol_check(args.protocol)
        else:
            root=Path(args.project).resolve()
            if not root.is_dir():
                raise ValueError("Project folder not found")
            result=audit(root,strict=args.strict)
            destination=safe_output(root,args.output)
            if destination:
                destination.parent.mkdir(parents=True,exist_ok=True)
                destination.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",
                                       encoding="utf-8")
        print(json.dumps(result,ensure_ascii=False,indent=2))
        if result.get("errors") or result.get("integrity",{}).get("errors"):
            return 1
        return 0
    except (ValueError,OSError,TypeError,json.JSONDecodeError) as exc:
        print("ERROR: "+str(exc),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
