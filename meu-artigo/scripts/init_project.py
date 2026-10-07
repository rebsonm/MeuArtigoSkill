#!/usr/bin/env python3
"""Initialize a local mirror of the Meu Artigo canonical research workspace.

The Google Drive workspace is preferred. This script creates the same logical
structure locally when Drive is unavailable or when deterministic scaffolding is
useful before synchronization.
"""
from __future__ import annotations
import argparse, csv, json, re
from datetime import date
from pathlib import Path

FOLDERS = [
    "00_Gestao_e_Continuidade",
    "01_Auditoria_de_Novidade/Notas_de_Auditoria",
    "01_Auditoria_de_Novidade/Artigos_Semente",
    "02_Buscas_e_Exports/Scopus",
    "02_Buscas_e_Exports/Web_of_Science",
    "02_Buscas_e_Exports/Outras_Bases",
    "02_Buscas_e_Exports/Snapshots",
    "03_Screening_e_FullText/FullText_Corpus",
    "03_Screening_e_FullText/Pendentes_de_Acesso",
    "03_Screening_e_FullText/Excluidos_com_Justificativa",
    "04_Evidencias_e_Sintese/Notas_de_Sintese",
    "04_Evidencias_e_Sintese/Figuras_e_Modelos",
    "04_Evidencias_e_Sintese/Claims_Ledger",
    "05_Manuscrito/Rascunhos",
    "05_Manuscrito/Versao_Canonica",
    "06_Submissao/Regras_da_Revista",
    "06_Submissao/Arquivos_Finais",
    "06_Submissao/Comprovantes",
    "99_Arquivo_Historico",
]

TABLES = {
"00_Gestao_e_Continuidade/00_Projeto.csv":["Field","Value","Status","Updated","Notes"],
"00_Gestao_e_Continuidade/01_Protocolo.csv":["Item","Decision","Rationale","Status","Version","Updated"],
"00_Gestao_e_Continuidade/02_Search_Log.csv":["Search_ID","Date","Database_or_source","Conceptual_blocks","Literal_query","Filters","Records_found","Records_exported","Export_file_or_URL","Status","Iteration","Notes"],
"00_Gestao_e_Continuidade/03_Screening.csv":["Record_ID","Source_database","Search_ID","Title","Authors","Year","DOI","Other_identifier","Abstract","Document_type","Language","Pass1_decision","Pass1_reason","Pass2_decision","Pass2_reason","Duplicate_status","Canonical_record_id","Notes"],
"00_Gestao_e_Continuidade/04_FullText_Tracker.csv":["Record_ID","Priority","Full_text_status","Version_accessed","Access_source","Access_date","Full_text_decision","Exclusion_reason","Evidence_matrix_id","File_or_URL","Notes"],
"00_Gestao_e_Continuidade/05_Evidence_Matrix.csv":["Evidence_ID","Citation","DOI_or_persistent_ID","Construct_or_concept","Definition_or_claim","Problem_tension_or_risk","Mechanism_relationship_or_finding","Study_design_or_source_type","Sample_data_or_material","Context","Process_or_stage","Actors_or_roles","Decision_right_or_action","Observable_evidence_or_artifact","Boundary_conditions","Limitations","Transferability_to_question","Evidence_role_or_strength","Supporting_locator","Epistemic_label","Notes"],
"00_Gestao_e_Continuidade/06_Journal_Dialogue.csv":["Journal_article","Why_relevant","What_it_already_says","What_new_article_adds","Use_in_manuscript","Citation_status","Notes"],
"00_Gestao_e_Continuidade/07_Normative_Corpus.csv":["ID","Institution","Document","Year","Jurisdiction","Authority_type","Scope","Relevant_constructs","Mechanisms","Lifecycle_stage","Binding_status","URL","Include_status","Version_or_access_date","Notes"],
"00_Gestao_e_Continuidade/08_Synthesis_Log.csv":["Synthesis_ID","Category_or_theme","Evidence_IDs","Cross_source_pattern","Contradictions","Boundary_conditions","Inference","Epistemic_status","Decision","Notes"],
"00_Gestao_e_Continuidade/09_Claims_Ledger.csv":["Claim_ID","Manuscript_section","Claim_text","Claim_type","Evidence_IDs","Locator_status","Strength","Draft_status","Notes"],
"00_Gestao_e_Continuidade/10_Submission_Checklist.csv":["Item","Requirement","Source_of_requirement","Status","Evidence_or_file","Notes"],
}

def slug(v:str)->str:
    v=re.sub(r"[^a-zA-Z0-9]+","-",v.strip()).strip("-")
    return v or "artigo"

def write_csv(path:Path, headers:list[str]):
    if path.exists(): return
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8-sig") as f: csv.writer(f).writerow(headers)

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--path",default=".")
    ap.add_argument("--name",required=True)
    ap.add_argument("--problem",default="")
    ap.add_argument("--article-type",default="undecided")
    a=ap.parse_args()
    root=Path(a.path).resolve()/f"ARTIGO_{slug(a.name)}_{date.today().year}"
    root.mkdir(parents=True,exist_ok=True)
    for f in FOLDERS:(root/f).mkdir(parents=True,exist_ok=True)
    cfg=root/"00_Gestao_e_Continuidade/PROJECT_CONFIG.json"
    if not cfg.exists():
        cfg.write_text(json.dumps({"project_name":a.name,"research_input":a.problem,"article_type":a.article_type,"created":date.today().isoformat(),"status":"INITIALIZED"},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    cont=root/"00_Gestao_e_Continuidade/CONTINUIDADE.md"
    if not cont.exists():
        cont.write_text(f"# CONTINUIDADE — {a.name}\nUpdated: {date.today().isoformat()}\n\n## 1. User research input\n{a.problem or '[USER INPUT REQUIRED]'}\n\n## 2. Current research object\n- Current question: [TO REFINE]\n- Objective: [TO REFINE]\n- Intended contribution: [TO REFINE]\n- Article/review design: {a.article_type}\n- Scope and exclusions: [TO DEFINE]\n\n## 3. Tool and plugin status\n- Google Drive: UNKNOWN\n- Consensus: UNKNOWN\n- Scite: UNKNOWN\n- Firecrawl/web: UNKNOWN\n- Scopus access: UNKNOWN\n- Web of Science access: UNKNOWN\n\n## 4. Canonical workspace links\n- Project root: local mirror\n- Master matrix: CSV mirror\n- Protocol: 00_Gestao_e_Continuidade/PROTOCOLO.md\n- Manuscript: not started\n\n## 5. Frozen decisions\n- None yet.\n\n## 6. Search status\n- Not started.\n\n## 7. Deduplication and screening status\n- Not started.\n\n## 8. Full-text status\n- Not started.\n\n## 9. Evidence-matrix status\n- Not started.\n\n## 10. Synthesis status\n- Not started.\n\n## 11. Manuscript status\n- Not started.\n\n## 12. Journal/submission status\n- Not started.\n\n## 13. Open issues and blockers\n- Refine research object and run novelty audit.\n\n## 14. Next valid action\n- Run first novelty/terminology scan and freeze protocol v1.\n\n## 15. Change log\n- {date.today().isoformat()} — workspace initialized.\n",encoding="utf-8")
    prot=root/"00_Gestao_e_Continuidade/PROTOCOLO.md"
    if not prot.exists():
        prot.write_text(f"# PROTOCOLO — {a.name}\n\n## Original research input\n{a.problem or '[TO DEFINE]'}\n\n## Current research question\n[TO REFINE]\n\n## Objective\n[TO REFINE]\n\n## Intended contribution\n[TO REFINE AFTER NOVELTY AUDIT]\n\n## Article/review design\n{a.article_type}\n\n## Scope and exclusions\n[TO DEFINE]\n\n## Databases and source roles\n[TO DEFINE]\n\n## Date/language/document-type rules\n[TO DEFINE]\n\n## Inclusion criteria\n[TO DEFINE]\n\n## Exclusion criteria\n[TO DEFINE]\n\n## Search families\n[TO DEFINE AND VERSION]\n\n## Screening and full-text rules\n[TO DEFINE]\n\n## Synthesis/stopping rule\n[TO DEFINE]\n",encoding="utf-8")
    for rel,h in TABLES.items():write_csv(root/rel,h)
    print(root); return 0
if __name__=="__main__": raise SystemExit(main())
