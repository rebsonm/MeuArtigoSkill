#!/usr/bin/env python3
"""Smoke-test the Meu Artigo provenance export using a synthetic project."""
from __future__ import annotations
import csv,json,subprocess,sys,tempfile
from pathlib import Path

def write_csv(path:Path,headers:list[str],rows:list[list[str]]):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(rows)

def main()->int:
    here=Path(__file__).resolve().parent
    exporter=here/"export_provenance.py"
    validator=here/"validate_provenance_package.py"
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)/"ARTIGO_smoke_2026"
        mgmt=root/"00_Gestao_e_Continuidade"
        out=root/"06_Submissao/Arquivos_Finais"
        mgmt.mkdir(parents=True);out.mkdir(parents=True)
        (mgmt/"PROJECT_CONFIG.json").write_text(json.dumps({"project_name":"Smoke Test"},indent=2),encoding="utf-8")
        write_csv(mgmt/"11_CADA_Control.csv",
            ["CADA_ID","Title","Scientific_stage","Next_action","Status","Completion_evidence"],
            [["CADA-0001","Initialize","00","Continue","DONE","Workspace created"]])
        write_csv(mgmt/"13_Traceability_Log.csv",
            ["Trace_ID","Timestamp","Scientific_stage","CADA_ID","Actor","AI_platform_or_tool","Action_type","Action_summary","Input_or_source","Source_or_artifact_IDs","Artifact_before","Artifact_after","Verification_method","Human_validation","Related_Evidence_IDs","Related_Record_IDs","Materiality","Status"],
            [["TRACE-0001","2026-10-07T03:00:00Z","00","CADA-0001","SCRIPT","init_project.py","WORKSPACE_INITIALIZATION","Initialize","Input","","","Matrix","file check","PENDING","","","ADMINISTRATIVE","COMPLETE"]])
        write_csv(mgmt/"02_Search_Log.csv",
            ["Search_ID","Date","Database_or_source","Literal_query","Filters","Records_found","Records_exported","Status"],
            [["S-0001","2026-10-07","Scopus","TITLE-ABS-KEY(test)","","1","1","VALID"]])
        write_csv(mgmt/"03_Screening.csv",
            ["Record_ID","Search_ID","Title","DOI","Other_identifier"],
            [["R-0001","S-0001","Paper test","10.0000/test",""]])
        write_csv(mgmt/"05_Evidence_Matrix.csv",
            ["Evidence_ID","Citation","Epistemic_label","Supporting_locator","Construct_or_concept"],
            [["E-0001","Paper test","[L]","p. 1","Test"]])
        write_csv(mgmt/"09_Claims_Ledger.csv",
            ["Claim_ID","Claim_text","Claim_type","Evidence_IDs"],
            [["CL-0001","Test claim","LITERATURE","E-0001"]])
        write_csv(mgmt/"14_AI_Use_Log.csv",
            ["AI_Use_ID","Materiality","Human_review_method","Accepted_modified_or_rejected"],[])

        ex=subprocess.run([sys.executable,str(exporter),str(root)],capture_output=True,text=True)
        if ex.returncode!=0:
            print(ex.stdout);print(ex.stderr,file=sys.stderr);return 1
        zips=list(out.glob("RO_CRATE_*.zip"))
        if len(zips)!=1:
            print(f"Expected one ZIP, found {len(zips)}",file=sys.stderr);return 1
        va=subprocess.run([sys.executable,str(validator),str(zips[0])],capture_output=True,text=True)
        print(ex.stdout.strip())
        print(va.stdout.strip())
        return va.returncode

if __name__=="__main__":
    raise SystemExit(main())
