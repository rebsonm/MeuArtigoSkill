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
]
PASS1={"","INCLUDE","BORDERLINE","EXCLUDE"}
PASS2={"","FULL TEXT — CORE","FULL TEXT — SUPPORT","EXCLUDE","FULL TEXT - CORE","FULL TEXT - SUPPORT"}
EPI={"","L","I","P","[L]","[I]","[P]"}
def rows(path):
    with path.open("r",encoding="utf-8-sig",newline="") as f: yield from csv.DictReader(f)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("project_path");a=ap.parse_args();root=Path(a.project_path).resolve();errors=[];warnings=[]
    for rel in REQUIRED:
        if not (root/rel).exists():errors.append(f"missing required artifact: {rel}")
    cfg=root/"00_Gestao_e_Continuidade/PROJECT_CONFIG.json"
    if cfg.exists():
        try:
            d=json.loads(cfg.read_text(encoding="utf-8"))
            if not str(d.get("research_input","")).strip():warnings.append("PROJECT_CONFIG research_input is empty")
        except Exception as e:errors.append(f"invalid PROJECT_CONFIG.json: {e}")
    log=root/"00_Gestao_e_Continuidade/02_Search_Log.csv"
    if log.exists():
        for i,r in enumerate(rows(log),2):
            st=(r.get("Status") or "").upper()
            if st and st not in {"PLANNED","INVALID","SUPERSEDED"} and not (r.get("Literal_query") or "").strip(): errors.append(f"search row {i}: executed search lacks Literal_query")
    scr=root/"00_Gestao_e_Continuidade/03_Screening.csv"
    if scr.exists():
        ids=set()
        for i,r in enumerate(rows(scr),2):
            rid=(r.get("Record_ID") or "").strip()
            if rid and rid in ids:errors.append(f"screening row {i}: duplicate Record_ID {rid}")
            ids.add(rid) if rid else None
            p1=(r.get("Pass1_decision") or "").strip().upper();p2=(r.get("Pass2_decision") or "").strip().upper()
            if p1 not in PASS1:warnings.append(f"screening row {i}: nonstandard Pass1_decision {p1!r}")
            if p2 not in {x.upper() for x in PASS2}:warnings.append(f"screening row {i}: nonstandard Pass2_decision {p2!r}")
    ev=root/"00_Gestao_e_Continuidade/05_Evidence_Matrix.csv"
    if ev.exists():
        ids=set()
        for i,r in enumerate(rows(ev),2):
            eid=(r.get("Evidence_ID") or "").strip();lab=(r.get("Epistemic_label") or "").strip().upper()
            if eid and eid in ids:errors.append(f"evidence row {i}: duplicate Evidence_ID {eid}")
            ids.add(eid) if eid else None
            if lab not in EPI:warnings.append(f"evidence row {i}: unexpected Epistemic_label {lab!r}")
    cont=root/"00_Gestao_e_Continuidade/CONTINUIDADE.md"
    if cont.exists():
        s=cont.read_text(encoding="utf-8",errors="replace")
        for heading in ["## 14. Next valid action","## 15. Change log","## 3. Tool and plugin status"]:
            if heading not in s:warnings.append(f"CONTINUIDADE.md lacks {heading!r}")
    for w in warnings:print("WARNING:",w)
    for e in errors:print("ERROR:",e)
    print(f"validation_errors={len(errors)}");print(f"validation_warnings={len(warnings)}")
    return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
