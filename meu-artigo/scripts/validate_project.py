#!/usr/bin/env python3
"""Validate the canonical local mirror of a Meu Artigo project."""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

REQUIRED=[
"00_Gestao_e_Continuidade/CONTINUIDADE.md",
"00_Gestao_e_Continuidade/PROTOCOLO.md",
"00_Gestao_e_Continuidade/02_Search_Log.csv",
"00_Gestao_e_Continuidade/03_Screening.csv",
"00_Gestao_e_Continuidade/04_FullText_Tracker.csv",
"00_Gestao_e_Continuidade/05_Evidence_Matrix.csv",
"00_Gestao_e_Continuidade/11_CADA_Control.csv",
"00_Gestao_e_Continuidade/12_PM_Sync.csv",
"00_Gestao_e_Continuidade/13_Traceability_Log.csv",
"00_Gestao_e_Continuidade/14_AI_Use_Log.csv",
"00_Gestao_e_Continuidade/15_CADA_Dashboard.csv",
"00_Gestao_e_Continuidade/RASTREABILIDADE.md",
]
PASS1={"","INCLUDE","BORDERLINE","EXCLUDE"}
PASS2={"","FULL TEXT — CORE","FULL TEXT — SUPPORT","EXCLUDE","FULL TEXT - CORE","FULL TEXT - SUPPORT"}
EPI={"","L","I","P","[L]","[I]","[P]"}
CADA_STATUS={"CAPTURED","ASSIGNED","READY","IN_PROGRESS","WAITING","BLOCKED","DONE","CANCELLED","SUPERSEDED"}
CADA_TERMINAL={"DONE","CANCELLED","SUPERSEDED"}
DEADLINE_TYPES={"EXTERNAL","USER_SET","INTERNAL_TARGET","DEPENDENCY","TO_DEFINE"}
TRACE_STATUS={"PLANNED","IN_PROGRESS","COMPLETE","INVALID","SUPERSEDED"}
AI_MATERIALITY={"ASSISTIVE","SUBSTANTIVE","ADMINISTRATIVE","NOT_APPLICABLE"}
AI_DECISION={"","ACCEPTED","MODIFIED","REJECTED","PENDING"}

def rows(path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        yield from csv.DictReader(f)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_path")
    a=ap.parse_args()
    root=Path(a.project_path).resolve()
    errors=[];warnings=[]
    cfg_data={}

    for rel in REQUIRED:
        if not (root/rel).exists():
            errors.append(f"missing required artifact: {rel}")

    cfg=root/"00_Gestao_e_Continuidade/PROJECT_CONFIG.json"
    if cfg.exists():
        try:
            cfg_data=json.loads(cfg.read_text(encoding="utf-8"))
            if not str(cfg_data.get("research_input","")).strip():
                warnings.append("PROJECT_CONFIG research_input is empty")
            if cfg_data.get("cada_governance") is not True:
                warnings.append("PROJECT_CONFIG cada_governance is not true")
            if cfg_data.get("traceability_enabled") is not True:
                warnings.append("PROJECT_CONFIG traceability_enabled is not true")
            mode=cfg_data.get("work_management_mode")
            if mode not in {"MATRIX_ONLY","MATRIX_PLUS_EXTERNAL"}:
                warnings.append(f"PROJECT_CONFIG unexpected work_management_mode={mode!r}")
        except Exception as e:
            errors.append(f"invalid PROJECT_CONFIG.json: {e}")

    log=root/"00_Gestao_e_Continuidade/02_Search_Log.csv"
    if log.exists():
        for i,r in enumerate(rows(log),2):
            st=(r.get("Status") or "").upper()
            if st and st not in {"PLANNED","INVALID","SUPERSEDED"} and not (r.get("Literal_query") or "").strip():
                errors.append(f"search row {i}: executed search lacks Literal_query")

    scr=root/"00_Gestao_e_Continuidade/03_Screening.csv"
    if scr.exists():
        ids=set()
        for i,r in enumerate(rows(scr),2):
            rid=(r.get("Record_ID") or "").strip()
            if rid and rid in ids:
                errors.append(f"screening row {i}: duplicate Record_ID {rid}")
            if rid: ids.add(rid)
            p1=(r.get("Pass1_decision") or "").strip().upper()
            p2=(r.get("Pass2_decision") or "").strip().upper()
            if p1 not in PASS1:
                warnings.append(f"screening row {i}: nonstandard Pass1_decision {p1!r}")
            if p2 not in {x.upper() for x in PASS2}:
                warnings.append(f"screening row {i}: nonstandard Pass2_decision {p2!r}")

    ev=root/"00_Gestao_e_Continuidade/05_Evidence_Matrix.csv"
    if ev.exists():
        ids=set()
        for i,r in enumerate(rows(ev),2):
            eid=(r.get("Evidence_ID") or "").strip()
            lab=(r.get("Epistemic_label") or "").strip().upper()
            if eid and eid in ids:
                errors.append(f"evidence row {i}: duplicate Evidence_ID {eid}")
            if eid: ids.add(eid)
            if lab not in EPI:
                warnings.append(f"evidence row {i}: unexpected Epistemic_label {lab!r}")

    cada=root/"00_Gestao_e_Continuidade/11_CADA_Control.csv"
    cada_ids=set()
    if cada.exists():
        for i,r in enumerate(rows(cada),2):
            cid=(r.get("CADA_ID") or "").strip()
            status=(r.get("Status") or "").strip().upper()
            next_action=(r.get("Next_action") or "").strip()
            deadline_type=(r.get("Deadline_type") or "").strip().upper()
            completion=(r.get("Completion_evidence") or "").strip()
            if not cid:
                errors.append(f"CADA row {i}: missing CADA_ID")
                continue
            if cid in cada_ids:
                errors.append(f"CADA row {i}: duplicate CADA_ID {cid}")
            cada_ids.add(cid)
            if not cid.startswith("CADA-"):
                warnings.append(f"CADA row {i}: nonstandard ID {cid!r}")
            if status not in CADA_STATUS:
                warnings.append(f"CADA row {i}: unexpected Status {status!r}")
            if status not in CADA_TERMINAL and not next_action:
                errors.append(f"CADA row {i}: active item {cid} lacks Next_action")
            if status not in CADA_TERMINAL and deadline_type not in DEADLINE_TYPES:
                errors.append(f"CADA row {i}: active item {cid} lacks valid Deadline_type")
            if status=="DONE" and not completion:
                warnings.append(f"CADA row {i}: DONE item {cid} lacks Completion_evidence")

    sync=root/"00_Gestao_e_Continuidade/12_PM_Sync.csv"
    if sync.exists():
        keys=set()
        for i,r in enumerate(rows(sync),2):
            cid=(r.get("CADA_ID") or "").strip()
            provider=(r.get("Provider") or "").strip().lower()
            if not cid and not provider:
                continue
            key=(cid,provider)
            if key in keys:
                errors.append(f"PM sync row {i}: duplicate CADA_ID/provider pair {key}")
            keys.add(key)
            if cid and cada_ids and cid not in cada_ids:
                warnings.append(f"PM sync row {i}: CADA_ID {cid} not found in 11_CADA_Control")

    pm=(cfg_data.get("work_management_provider") if cfg_data else None)
    if pm and sync.exists():
        sync_rows=list(rows(sync))
        if not sync_rows:
            warnings.append(f"PROJECT_CONFIG selects work_management_provider={pm!r} but 12_PM_Sync has no rows yet")

    trace=root/"00_Gestao_e_Continuidade/13_Traceability_Log.csv"
    trace_ids=set()
    if trace.exists():
        for i,r in enumerate(rows(trace),2):
            tid=(r.get("Trace_ID") or "").strip()
            status=(r.get("Status") or "").strip().upper()
            action=(r.get("Action_summary") or "").strip()
            if not tid:
                errors.append(f"trace row {i}: missing Trace_ID")
                continue
            if tid in trace_ids:
                errors.append(f"trace row {i}: duplicate Trace_ID {tid}")
            trace_ids.add(tid)
            if not tid.startswith("TRACE-"):
                warnings.append(f"trace row {i}: nonstandard Trace_ID {tid!r}")
            if not action:
                errors.append(f"trace row {i}: {tid} lacks Action_summary")
            if status and status not in TRACE_STATUS:
                warnings.append(f"trace row {i}: unexpected Status {status!r}")
            cid=(r.get("CADA_ID") or "").strip()
            if cid and cada_ids and cid not in cada_ids:
                warnings.append(f"trace row {i}: CADA_ID {cid} not found in 11_CADA_Control")

    ai=root/"00_Gestao_e_Continuidade/14_AI_Use_Log.csv"
    ai_ids=set()
    if ai.exists():
        for i,r in enumerate(rows(ai),2):
            aid=(r.get("AI_Use_ID") or "").strip()
            if not aid:
                continue
            if aid in ai_ids:
                errors.append(f"AI-use row {i}: duplicate AI_Use_ID {aid}")
            ai_ids.add(aid)
            if not aid.startswith("AIUSE-"):
                warnings.append(f"AI-use row {i}: nonstandard AI_Use_ID {aid!r}")
            materiality=(r.get("Materiality") or "").strip().upper()
            if materiality and materiality not in AI_MATERIALITY:
                warnings.append(f"AI-use row {i}: unexpected Materiality {materiality!r}")
            decision=(r.get("Accepted_modified_or_rejected") or "").strip().upper()
            if decision not in AI_DECISION:
                warnings.append(f"AI-use row {i}: unexpected decision {decision!r}")
            trace_id=(r.get("Trace_ID") or "").strip()
            if trace_id and trace_ids and trace_id not in trace_ids:
                warnings.append(f"AI-use row {i}: Trace_ID {trace_id} not found in 13_Traceability_Log")
            review=(r.get("Human_review_method") or "").strip()
            if materiality=="SUBSTANTIVE" and not review:
                errors.append(f"AI-use row {i}: substantive AI use {aid} lacks Human_review_method")
            if materiality=="SUBSTANTIVE" and decision in {"","PENDING"}:
                warnings.append(f"AI-use row {i}: substantive AI use {aid} has no final human decision")

    dashboard=root/"00_Gestao_e_Continuidade/15_CADA_Dashboard.csv"
    if dashboard.exists():
        metrics={(r.get("Metric") or "").strip():(r.get("Value") or "").strip() for r in rows(dashboard)}
        for metric in ["Management_mode","Current_scientific_stage","Next_CADA_ID","Next_action","Traceability_gaps"]:
            if metric not in metrics:
                warnings.append(f"CADA dashboard lacks metric {metric!r}")

    rast=root/"00_Gestao_e_Continuidade/RASTREABILIDADE.md"
    if rast.exists():
        rs=rast.read_text(encoding="utf-8",errors="replace")
        for heading in ["## Process provenance","## AI use","## Human validation checkpoints","## Provenance gaps"]:
            if heading not in rs:
                warnings.append(f"RASTREABILIDADE.md lacks {heading!r}")

    cont=root/"00_Gestao_e_Continuidade/CONTINUIDADE.md"
    if cont.exists():
        s=cont.read_text(encoding="utf-8",errors="replace")
        for heading in [
            "## 14. Next valid action",
            "## 15. Change log",
            "## 16. C.A.D.A. dashboard",
            "## 3. Tool and plugin status",
        ]:
            if heading not in s:
                warnings.append(f"CONTINUIDADE.md lacks {heading!r}")

    for w in warnings: print("WARNING:",w)
    for e in errors: print("ERROR:",e)
    print(f"validation_errors={len(errors)}")
    print(f"validation_warnings={len(warnings)}")
    return 1 if errors else 0

if __name__=="__main__":
    raise SystemExit(main())
