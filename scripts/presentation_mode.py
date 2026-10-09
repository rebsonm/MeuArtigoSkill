#!/usr/bin/env python3
"""Progressive presentation of a scientific project, never fewer safeguards.

Minimal and full modes read the SAME canonical registers and gates.
They never manufacture outcomes, alter scientific status, or bypass validation.
"""
from __future__ import annotations
import argparse,csv,json,os,sys,tempfile
from datetime import datetime,timezone
from pathlib import Path

MGMT="00_Gestao_e_Continuidade"
CONFIG=f"{MGMT}/PROJECT_CONFIG.json"
STAGES=f"{MGMT}/18_Human_Validation_Gates.csv"
TASKS=f"{MGMT}/11_CADA_Control.csv"
CLAIMS=f"{MGMT}/09_Claims_Ledger.csv"
ACCEPTED={"MINIMAL","FULL"}

def read_rows(root,path):
    file=root/path
    if not file.exists():
        return [],False
    with file.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f)),True

def read_config(root):
    file=root/CONFIG
    if not file.is_file():
        raise ValueError("Project config unavailable; initialize an authorized project first")
    data=json.loads(file.read_text(encoding="utf-8"))
    if not isinstance(data,dict): raise ValueError("Invalid project config")
    return data

def view(root):
    config=read_config(root)
    mode=config.get("presentation_mode","FULL")
    if mode not in ACCEPTED: raise ValueError("Unsupported presentation mode")
    gates,gs=read_rows(root,STAGES)
    tasks,ts=read_rows(root,TASKS)
    claims,cs=read_rows(root,CLAIMS)
    unresolved=[g for g in gates if (g.get("Status") or "").upper()!="COMPLETED"]
    active=[t for t in tasks if (t.get("Status") or "").upper() not in {"DONE","COMPLETED","CANCELLED"}]
    # Display existing statuses without asserting that an unobserved event happened.
    result={"mode":mode,
            "scientific_gates_pending":len(unresolved) if gs else None,
            "tasks_not_completed":len(active) if ts else None,
            "claims_registered":len(claims) if cs else None,
            "missing_registers":[name for name,ok in ((STAGES,gs),(TASKS,ts),(CLAIMS,cs)) if not ok],
            "scientific_safeguards_unchanged":True,
            "empirical_effect_proven":False}
    if mode=="MINIMAL":
        result["next_scientific_decision"]=next(
            ({"gate_id":g.get("GATE_ID"),"name":g.get("Name") or g.get("Decision_type"),
              "status":g.get("Status")} for g in unresolved),None)
        result["next_action"]=next(
            ({"task_id":t.get("CADA_ID"),"action":t.get("Next_action"),"status":t.get("Status")}
             for t in active),None)
    else:
        result["scientific_gates"]=[{"id":g.get("GATE_ID"),"status":g.get("Status"),
                                     "decision":g.get("Decision")} for g in gates]
        result["tasks"]=[{"id":t.get("CADA_ID"),"status":t.get("Status"),
                          "next_action":t.get("Next_action")} for t in tasks]
    return result

def set_mode(root,mode,confirmed_by):
    if mode not in ACCEPTED: raise ValueError("Choose MINIMAL or FULL")
    if len((confirmed_by or "").strip())<3:
        raise ValueError("Switch requires an actual researcher's explicit request/reference")
    config_path=root/CONFIG
    data=read_config(root)
    data["presentation_mode"]=mode
    data["presentation_mode_reviewed_by"]=confirmed_by.strip()
    data["presentation_mode_updated_at"]=datetime.now(timezone.utc).isoformat()
    # Atomic same-directory replacement; do not touch gates, logs, PDFs or research data.
    fd,temp=tempfile.mkstemp(prefix=".config-",suffix=".json",dir=config_path.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
            f.write("\n")
        os.replace(temp,config_path)
    finally:
        if os.path.exists(temp):os.unlink(temp)
    return view(root)

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("project")
    p.add_argument("--mode",choices=sorted(ACCEPTED))
    p.add_argument("--confirmed-by",default="")
    args=p.parse_args(argv)
    try:
        root=Path(args.project).resolve()
        data=set_mode(root,args.mode,args.confirmed_by) if args.mode else view(root)
        print(json.dumps(data,ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError,json.JSONDecodeError,csv.Error) as e:
        print(f"ERROR: {e}",file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
