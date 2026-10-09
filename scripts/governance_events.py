#!/usr/bin/env python3
"""Record scientific decisions and human validation gates in a Meu Artigo project.

This script intentionally handles only governance events. It does not make
scientific judgments on behalf of the researcher.

Examples:
  python governance_events.py decision PROJECT \
    --type METHOD \
    --question "Which review design best fits the research purpose?" \
    --decision "Integrative review" \
    --rationale "The project synthesizes heterogeneous conceptual and empirical literature."

  python governance_events.py gate PROJECT \
    --gate-id GATE-0002 \
    --decision APPROVED \
    --validated-by "Researcher" \
    --method "Reviewed protocol v1 and search criteria." \
    --evidence "Reference to the actual reviewer response"
"""
from __future__ import annotations

import argparse
import json
import csv
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from formative_gates import SCIENTIFIC_GATES, APPROVALS, response_issues, encode_formative

MGMT="00_Gestao_e_Continuidade"
DEC_FILE=f"{MGMT}/17_Decision_Log.csv"
GATE_FILE=f"{MGMT}/18_Human_Validation_Gates.csv"
TRACE_FILE=f"{MGMT}/13_Traceability_Log.csv"

DEC_HEADERS=[
"DEC_ID","Timestamp","Scientific_stage","Decision_type","Decision_question",
"Decision","Alternatives_considered","Rationale","Evidence_IDs","Record_IDs",
"CADA_ID","Trace_ID","Gate_ID","Status","Decided_by","Impact",
"Affected_artifacts","Resulting_version","Supersedes_DEC_ID","Notes"
]

GATE_HEADERS=[
"GATE_ID","Gate_type","Scientific_stage","Name","Entry_condition",
"Items_to_validate","DEC_IDs","CADA_IDs","Evidence_IDs","Snapshot_before",
"Decision","Validated_by","Validation_date","Validation_method",
"Validation_evidence","Trace_ID","Snapshot_after","Status",
"Blocking_transition","Notes"
]

TRACE_HEADERS=[
"Trace_ID","Timestamp","Scientific_stage","CADA_ID","Actor",
"AI_platform_or_tool","Model_or_version","Action_type","Action_summary",
"Input_or_source","Source_or_artifact_IDs","Decision_or_output","Rationale",
"Artifact_before","Artifact_after","Verification_method","Human_validation",
"Related_Search_IDs","Related_Record_IDs","Related_Evidence_IDs",
"Related_Claim_IDs","Prompt_or_instruction_summary",
"Reproducibility_information","Materiality","Status","Notes"
]

DEC_TYPES={
"QUESTION_CONTRIBUTION","METHOD","SCOPE","SEARCH","SCREENING","FULL_TEXT",
"EVIDENCE","SYNTHESIS","CLAIM","MANUSCRIPT","JOURNAL","SUBMISSION","OTHER"
}
DEC_STATUS={"PROPOSED","APPROVED","REJECTED","FROZEN","SUPERSEDED"}
GATE_DECISIONS={"APPROVED","APPROVED_WITH_CHANGES","REJECTED","NOT_APPLICABLE","PENDING"}

def now_iso()->str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def ensure_csv(path:Path, headers:list[str])->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists() or path.stat().st_size==0:
        with path.open("w",encoding="utf-8-sig",newline="") as f:
            csv.writer(f).writerow(headers)

def rows(path:Path)->list[dict[str,str]]:
    if not path.exists(): return []
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def append(path:Path, headers:list[str], row:dict[str,str])->None:
    ensure_csv(path,headers)
    with path.open("a",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=headers)
        w.writerow({h:row.get(h,"") for h in headers})

def next_id(path:Path, field:str, prefix:str)->str:
    n=0
    pat=re.compile(rf"^{re.escape(prefix)}-(\d+)$")
    for r in rows(path):
        m=pat.match((r.get(field) or "").strip())
        if m: n=max(n,int(m.group(1)))
    return f"{prefix}-{n+1:04d}"

def next_trace(root:Path)->str:
    return next_id(root/TRACE_FILE,"Trace_ID","TRACE")

def record_trace(root:Path, *, stage:str, cada_id:str, action_type:str,
                 summary:str, decision_output:str, rationale:str,
                 record_ids:str="", evidence_ids:str="", human_validation:str="")->str:
    tid=next_trace(root)
    append(root/TRACE_FILE,TRACE_HEADERS,{
        "Trace_ID":tid,
        "Timestamp":now_iso(),
        "Scientific_stage":stage,
        "CADA_ID":cada_id,
        "Actor":"HUMAN" if human_validation else "HUMAN+AI",
        "AI_platform_or_tool":"",
        "Model_or_version":"",
        "Action_type":action_type,
        "Action_summary":summary,
        "Input_or_source":"Canonical scientific governance state",
        "Source_or_artifact_IDs":"",
        "Decision_or_output":decision_output,
        "Rationale":rationale,
        "Artifact_before":"",
        "Artifact_after":DEC_FILE if action_type=="SCIENTIFIC_DECISION" else GATE_FILE,
        "Verification_method":"Canonical governance record; execution receipt not captured",
        "Human_validation":human_validation,
        "Related_Search_IDs":"",
        "Related_Record_IDs":record_ids,
        "Related_Evidence_IDs":evidence_ids,
        "Related_Claim_IDs":"",
        "Prompt_or_instruction_summary":"",
        "Reproducibility_information":"Governance event recorded by governance_events.py",
        "Materiality":"SUBSTANTIVE",
        "Status":"UNVERIFIED",
        "Notes":"Decision or gate must be checked against its original human response.",
    })
    return tid

def record_decision(args)->int:
    root=Path(args.project).resolve()
    dtype=args.type.upper()
    status=args.status.upper()
    if dtype not in DEC_TYPES:
        raise SystemExit(f"invalid decision type: {dtype}")
    if status not in DEC_STATUS:
        raise SystemExit(f"invalid decision status: {status}")
    if status in {"APPROVED","FROZEN"} and not args.rationale.strip():
        raise SystemExit("approved/frozen decision requires --rationale")

    if status in {"APPROVED","FROZEN","REJECTED"}:
        if not args.decided_by.strip() or not args.evidence.strip():
            raise SystemExit("human decision requires --decided-by and --evidence")

    path=root/DEC_FILE
    ensure_csv(path,DEC_HEADERS)
    did=next_id(path,"DEC_ID","DEC")
    tid=record_trace(
        root,
        stage=args.stage,
        cada_id=args.cada_id,
        action_type="SCIENTIFIC_DECISION",
        summary=f"{did}: {args.question}",
        decision_output=args.decision,
        rationale=args.rationale,
        record_ids=args.record_ids,
        evidence_ids=args.evidence_ids,
        human_validation=args.decided_by if status in {"APPROVED","FROZEN","REJECTED"} else "",
    )
    append(path,DEC_HEADERS,{
        "DEC_ID":did,
        "Timestamp":now_iso(),
        "Scientific_stage":args.stage,
        "Decision_type":dtype,
        "Decision_question":args.question,
        "Decision":args.decision,
        "Alternatives_considered":args.alternatives,
        "Rationale":args.rationale,
        "Evidence_IDs":args.evidence_ids,
        "Record_IDs":args.record_ids,
        "CADA_ID":args.cada_id,
        "Trace_ID":tid,
        "Gate_ID":args.gate_id,
        "Status":status,
        "Decided_by":args.decided_by,
        "Impact":args.impact,
        "Affected_artifacts":args.artifacts,
        "Resulting_version":args.resulting_version,
        "Supersedes_DEC_ID":args.supersedes,
        "Notes":args.notes + (f"\nHuman decision evidence: {args.evidence}" if args.evidence else ""),
    })
    print(f"decision_id={did}")
    print(f"trace_id={tid}")
    return 0

def record_gate(args)->int:
    root=Path(args.project).resolve()
    decision=args.decision.upper()
    if decision not in GATE_DECISIONS:
        raise SystemExit(f"invalid gate decision: {decision}")
    path=root/GATE_FILE
    ensure_csv(path,GATE_HEADERS)
    gate_rows=rows(path)
    target=None
    for r in gate_rows:
        if (r.get("GATE_ID") or "").strip()==args.gate_id:
            target=r
            break
    if not target:
        raise SystemExit(f"gate not found: {args.gate_id}")

    # New workspaces require the researcher's own explanation at scientific gates.
    cfg_path=root/MGMT/"PROJECT_CONFIG.json"
    try:
        cfg=json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.is_file() else {}
    except (OSError, ValueError) as exc:
        raise SystemExit(f"invalid project configuration: {type(exc).__name__}")
    formative=(
        cfg.get("formative_gates_required") is True
        and args.gate_id in SCIENTIFIC_GATES
        and decision in APPROVALS
    )
    if formative:
        problems=response_issues(args.researcher_rationale, args.researcher_limitation)
        if problems:
            raise SystemExit("; ".join(problems))
        # An LLM cannot authenticate authorship from a CLI argument.
        # The response reference is preserved for external human review.
        if not args.evidence.strip() or not args.validated_by.strip():
            raise SystemExit("formative gate requires source of the actual researcher response")

    if decision not in {"PENDING","NOT_APPLICABLE"}:
        if not args.validated_by.strip():
            raise SystemExit("completed human validation requires --validated-by")
        if not args.evidence.strip():
            raise SystemExit("completed human validation requires --evidence")
        if not args.method.strip():
            raise SystemExit("completed human validation requires --method")

    formative_notes=args.notes
    if formative:
        encoded=encode_formative(
            rationale=args.researcher_rationale,
            limitation=args.researcher_limitation,
            source=args.evidence,
            validated_by=args.validated_by,
            decision=decision,
        )
        formative_notes=(args.notes.rstrip()+"\n" if args.notes.strip() else "")+encoded

    # A corpus may only be frozen when every nonduplicate screened record
    # has a defensible selection decision backed by human review evidence.
    if args.gate_id=="GATE-0004" and decision in {"APPROVED","APPROVED_WITH_CHANGES"} and cfg.get("screening_human_decisions_required") is True:
        from screening_review import read_table, audit_rows as screening_audit
        try:
            _, headers, screening_rows=read_table(root)
        except ValueError as exc:
            raise SystemExit(f"cannot approve corpus freeze: {exc}")
        if not screening_rows:
            raise SystemExit("cannot approve corpus freeze: screened corpus has no records")
        findings=screening_audit(screening_rows,enforce=True,freeze=True,headers=headers)
        if findings["errors"]:
            raise SystemExit("cannot approve corpus freeze: "+"; ".join(findings["errors"][:5]))

    tid=record_trace(
        root,
        stage=target.get("Scientific_stage") or "",
        cada_id=(target.get("CADA_IDs") or ""),
        action_type="HUMAN_VALIDATION_GATE",
        summary=f"{args.gate_id}: {target.get('Name') or target.get('Gate_type')}",
        decision_output=decision,
        rationale=args.notes or target.get("Items_to_validate") or "",
        evidence_ids=target.get("Evidence_IDs") or "",
        human_validation=args.validated_by,
    )

    updated=[]
    for r in gate_rows:
        if (r.get("GATE_ID") or "").strip()!=args.gate_id:
            updated.append(r); continue
        r=dict(r)
        r["Decision"]=decision
        r["Validated_by"]=args.validated_by
        r["Validation_date"]=now_iso() if decision!="PENDING" else ""
        r["Validation_method"]=args.method
        r["Validation_evidence"]=args.evidence
        r["Trace_ID"]=tid
        r["Status"]="NOT_APPLICABLE" if decision=="NOT_APPLICABLE" else ("COMPLETED" if decision!="PENDING" else "READY")
        r["Notes"]=formative_notes
        updated.append(r)

    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=GATE_HEADERS)
        w.writeheader()
        w.writerows([{h:r.get(h,"") for h in GATE_HEADERS} for r in updated])

    snapshot_id=""
    if decision in {"APPROVED","APPROVED_WITH_CHANGES"} and not args.no_snapshot:
        snap_script=Path(__file__).with_name("create_snapshot.py")
        if snap_script.exists():
            cmd=[
                sys.executable,str(snap_script),str(root),
                "--milestone",target.get("Name") or args.gate_id,
                "--stage",target.get("Scientific_stage") or "",
                "--trigger","HUMAN_GATE",
                "--gate-id",args.gate_id,
                "--dec-ids",target.get("DEC_IDs") or "",
                "--cada-ids",target.get("CADA_IDs") or "",
                "--change-summary",args.notes or f"State frozen after {args.gate_id} {decision}."
            ]
            run=subprocess.run(cmd,check=True,capture_output=True,text=True)
            for line in run.stdout.splitlines():
                if line.startswith("snapshot_id="):
                    snapshot_id=line.split("=",1)[1].strip()
                    break

    print(f"gate_id={args.gate_id}")
    print(f"trace_id={tid}")
    print(f"decision={decision}")
    if snapshot_id:
        print(f"snapshot_id={snapshot_id}")
    return 0

def main()->int:
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="command",required=True)

    d=sub.add_parser("decision")
    d.add_argument("project")
    d.add_argument("--type",required=True)
    d.add_argument("--stage",default="")
    d.add_argument("--question",required=True)
    d.add_argument("--decision",required=True)
    d.add_argument("--alternatives",default="")
    d.add_argument("--rationale",default="")
    d.add_argument("--evidence-ids",default="")
    d.add_argument("--record-ids",default="")
    d.add_argument("--cada-id",default="")
    d.add_argument("--gate-id",default="")
    d.add_argument("--status",default="PROPOSED")
    d.add_argument("--decided-by",default="")
    d.add_argument("--evidence",default="",help="Reference to the actual human decision")
    d.add_argument("--impact",default="")
    d.add_argument("--artifacts",default="")
    d.add_argument("--resulting-version",default="")
    d.add_argument("--supersedes",default="")
    d.add_argument("--notes",default="")
    d.set_defaults(func=record_decision)

    g=sub.add_parser("gate")
    g.add_argument("project")
    g.add_argument("--gate-id",required=True)
    g.add_argument("--decision",required=True)
    g.add_argument("--validated-by",default="")
    g.add_argument("--method",default="")
    g.add_argument("--evidence",default="")
    g.add_argument("--notes",default="")
    g.add_argument("--researcher-rationale",default="",help="Researcher\x27s own explanation of the scientific choice")
    g.add_argument("--researcher-limitation",default="",help="Researcher\x27s own description of a relevant limitation")
    g.add_argument("--no-snapshot",action="store_true")
    g.set_defaults(func=record_gate)

    args=ap.parse_args()
    return args.func(args)

if __name__=="__main__":
    raise SystemExit(main())
