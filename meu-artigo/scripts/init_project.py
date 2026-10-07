#!/usr/bin/env python3
"""Initialize a local mirror of the Meu Artigo canonical research workspace.

The canonical schema is platform-neutral. Google Drive is the reference cloud
implementation. C.A.D.A. is the operational governance layer; an external work
manager (ClickUp/Jira/Trello) is optional and remains a mirror.
"""
from __future__ import annotations
import argparse, csv, json, re, subprocess, sys
from datetime import date
from pathlib import Path

FOLDERS = [
    "00_Gestao_e_Continuidade",
    "00_Gestao_e_Continuidade/Snapshots",
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
"00_Gestao_e_Continuidade/11_CADA_Control.csv":["CADA_ID","Item_type","Title","Description","Scientific_stage","Captured_at","Source_or_trigger","Assigned_to","Execution_mode","Priority","Dependency_IDs","Next_action","Deadline","Deadline_type","Status","Evidence_of_progress","Completion_evidence","Related_artifact","Related_research_IDs","Blocker","Last_updated","External_manager","External_item_ID","Notes"],
"00_Gestao_e_Continuidade/12_PM_Sync.csv":["CADA_ID","Provider","Workspace_or_site","Container_ID","External_item_ID","External_URL","External_status","External_assignee","External_due","Canonical_status","Canonical_assignee","Canonical_deadline","Last_pushed_at","Last_pulled_at","Sync_status","Conflict","Notes"],
"00_Gestao_e_Continuidade/13_Traceability_Log.csv":["Trace_ID","Timestamp","Scientific_stage","CADA_ID","Actor","AI_platform_or_tool","Model_or_version","Action_type","Action_summary","Input_or_source","Source_or_artifact_IDs","Decision_or_output","Rationale","Artifact_before","Artifact_after","Verification_method","Human_validation","Related_Search_IDs","Related_Record_IDs","Related_Evidence_IDs","Related_Claim_IDs","Prompt_or_instruction_summary","Reproducibility_information","Materiality","Status","Notes"],
"00_Gestao_e_Continuidade/14_AI_Use_Log.csv":["AI_Use_ID","Date","Scientific_stage","CADA_ID","Trace_ID","Platform_or_tool","Model_or_version","Purpose","Input_category","Output_category","Materiality","Human_review_method","Human_decision","Accepted_modified_or_rejected","Related_artifacts","Disclosure_required","Disclosure_text_or_note","Notes"],
"00_Gestao_e_Continuidade/15_CADA_Dashboard.csv":["Metric","Value","Last_updated","Notes"],
"00_Gestao_e_Continuidade/16_Interoperabilidade.csv":["Export_ID","Timestamp","Standards","Package_path_or_URL","Package_SHA256","Validation_status","Trace_events","Prov_entities","Prov_activities","Prov_agents","RO_Crate_files","Warnings","Notes"],
"00_Gestao_e_Continuidade/17_Decision_Log.csv":["DEC_ID","Timestamp","Scientific_stage","Decision_type","Decision_question","Decision","Alternatives_considered","Rationale","Evidence_IDs","Record_IDs","CADA_ID","Trace_ID","Gate_ID","Status","Decided_by","Impact","Affected_artifacts","Resulting_version","Supersedes_DEC_ID","Notes"],
"00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv":["GATE_ID","Gate_type","Scientific_stage","Name","Entry_condition","Items_to_validate","DEC_IDs","CADA_IDs","Evidence_IDs","Snapshot_before","Decision","Validated_by","Validation_date","Validation_method","Validation_evidence","Trace_ID","Snapshot_after","Status","Blocking_transition","Notes"],
"00_Gestao_e_Continuidade/19_Snapshots.csv":["SNAP_ID","Timestamp","Milestone","Scientific_stage","Trigger","Gate_ID","DEC_IDs","CADA_IDs","Previous_SNAP_ID","Snapshot_path_or_URL","Manifest_path","Manifest_SHA256","Canonical_artifacts","Change_summary","Validation_status","EXPORT_ID","Notes"],
}

def slug(v:str)->str:
    v=re.sub(r"[^a-zA-Z0-9]+","-",v.strip()).strip("-")
    return v or "artigo"

def write_csv(path:Path, headers:list[str]):
    if path.exists(): return
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8-sig") as f:
        csv.writer(f).writerow(headers)

def seed_cada(path:Path, project_name:str, pm_provider:str):
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        existing=list(csv.DictReader(f))
    if existing:
        return
    today=date.today().isoformat()
    rows=[
        {
            "CADA_ID":"CADA-0001","Item_type":"MILESTONE","Title":"Inicializar workspace de pesquisa",
            "Description":"Criar os artefatos canônicos e a camada de gestão C.A.D.A.","Scientific_stage":"00",
            "Captured_at":today,"Source_or_trigger":"project initialization","Assigned_to":"AGENT",
            "Execution_mode":"AUTONOMOUS","Priority":"HIGH","Dependency_IDs":"",
            "Next_action":"Confirmar artefatos canônicos e iniciar auditoria de novidade.","Deadline":"",
            "Deadline_type":"TO_DEFINE","Status":"DONE","Evidence_of_progress":"Workspace scaffold created.",
            "Completion_evidence":"CONTINUIDADE.md, PROTOCOLO.md e matriz local criados.",
            "Related_artifact":"00_Gestao_e_Continuidade/","Related_research_IDs":"","Blocker":"",
            "Last_updated":today,"External_manager":pm_provider or "NONE","External_item_ID":"",
            "Notes":f"Project: {project_name}",
        },
        {
            "CADA_ID":"CADA-0002","Item_type":"TASK","Title":"Executar auditoria inicial de novidade e terminologia",
            "Description":"Localizar literatura próxima e testar a contribuição proposta antes da busca extensiva.",
            "Scientific_stage":"01","Captured_at":today,"Source_or_trigger":"project initialization",
            "Assigned_to":"AGENT","Execution_mode":"AUTONOMOUS_WITH_USER_DECISIONS","Priority":"HIGH",
            "Dependency_IDs":"CADA-0001","Next_action":"Executar busca inicial de novidade e registrar artigos próximos.",
            "Deadline":"","Deadline_type":"TO_DEFINE","Status":"READY","Evidence_of_progress":"",
            "Completion_evidence":"Nota de auditoria + contribuição/pergunta atualizadas no workspace.",
            "Related_artifact":"01_Auditoria_de_Novidade/","Related_research_IDs":"","Blocker":"",
            "Last_updated":today,"External_manager":pm_provider or "NONE","External_item_ID":"",
            "Notes":"",
        },
        {
            "CADA_ID":"CADA-0003","Item_type":"TASK","Title":"Definir e congelar desenho metodológico e protocolo v1",
            "Description":"Classificar o tipo de artigo/revisão e congelar critérios e estratégia antes da busca em escala.",
            "Scientific_stage":"02-03","Captured_at":today,"Source_or_trigger":"project initialization",
            "Assigned_to":"AGENT+RESEARCHER","Execution_mode":"DECISION_REQUIRED","Priority":"HIGH",
            "Dependency_IDs":"CADA-0002","Next_action":"Aguardar auditoria de novidade; então propor desenho e protocolo v1.",
            "Deadline":"","Deadline_type":"DEPENDENCY","Status":"CAPTURED","Evidence_of_progress":"",
            "Completion_evidence":"PROTOCOLO.md versionado e decisão metodológica registrada.",
            "Related_artifact":"00_Gestao_e_Continuidade/PROTOCOLO.md","Related_research_IDs":"",
            "Blocker":"CADA-0002","Last_updated":today,"External_manager":pm_provider or "NONE",
            "External_item_ID":"","Notes":"",
        }
    ]
    with path.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=TABLES["00_Gestao_e_Continuidade/11_CADA_Control.csv"])
        w.writeheader(); w.writerows(rows)


def seed_gates(path:Path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        existing=list(csv.DictReader(f))
    if existing:
        return
    rows=[
        ["GATE-0001","QUESTION_CONTRIBUTION","01","Pergunta e contribuição","Auditoria inicial de novidade concluída.","Pergunta, objetivo, contribuição e limites propostos.","","CADA-0002","","","PENDING","","","","","","","PENDING","Definição do desenho metodológico",""],
        ["GATE-0002","METHOD_PROTOCOL","02-03","Método e protocolo","Desenho metodológico e protocolo v1 preparados.","Método, critérios, escopo, papéis das bases e regras de screening.","","CADA-0003","","","PENDING","","","","","","","PENDING","Busca em escala",""],
        ["GATE-0003","SEARCH_STRATEGY","03-04","Estratégia de busca","Strings e filtros preparados e testados.","Blocos conceituais, strings literais, filtros e bases.","","","","","PENDING","","","","","","","PENDING","Execução das buscas canônicas",""],
        ["GATE-0004","CORPUS_FREEZE","08-09","Congelamento do corpus","Screening/full text encerrados e contagens reconciliadas.","Corpus elegível, exclusões, duplicatas e contagens finais.","","","","","PENDING","","","","","","","PENDING","Extração/síntese final do corpus",""],
        ["GATE-0005","SYNTHESIS","10","Síntese e produto teórico","Síntese entre fontes estabilizada.","Categorias, contradições, inferências e proposições/modelo.","","","","","PENDING","","","","","","","PENDING","Redação substantiva do manuscrito",""],
        ["GATE-0006","CLAIMS_AUDIT","12-13","Claims e auditoria científica","Claims principais ligados às evidências e auditoria final executada.","Claims, Evidence_IDs, locators, limites e uso de IA.","","","","","PENDING","","","","","","","PENDING","Liberação da versão final",""],
        ["GATE-0007","SUBMISSION_RELEASE","14","Liberação para submissão","Versão canônica, checklist e transparência prontos.","Manuscrito final, relatório de transparência, disclosures e arquivos de submissão.","","","","","PENDING","","","","","","","PENDING","Submissão externa",""],
    ]
    with path.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f)
        w.writerow(TABLES["00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv"])
        w.writerows(rows)

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--path",default=".")
    ap.add_argument("--name",required=True)
    ap.add_argument("--problem",default="")
    ap.add_argument("--article-type",default="undecided")
    ap.add_argument("--pm-provider",default="",help="Optional primary work manager: clickup, jira, trello, or equivalent")
    a=ap.parse_args()

    pm=(a.pm_provider or "").strip().lower()
    root=Path(a.path).resolve()/f"ARTIGO_{slug(a.name)}_{date.today().year}"
    root.mkdir(parents=True,exist_ok=True)
    for f in FOLDERS:(root/f).mkdir(parents=True,exist_ok=True)

    cfg=root/"00_Gestao_e_Continuidade/PROJECT_CONFIG.json"
    if not cfg.exists():
        cfg.write_text(json.dumps({
            "project_name":a.name,
            "research_input":a.problem,
            "article_type":a.article_type,
            "created":date.today().isoformat(),
            "status":"INITIALIZED",
            "cada_governance":True,
            "work_management_mode":"MATRIX_PLUS_EXTERNAL" if pm else "MATRIX_ONLY",
            "work_management_provider":pm or None,
            "work_management_role":"OPTIONAL_OPERATIONAL_MIRROR",
            "traceability_enabled":True,
            "interoperable_provenance_enabled":True,
            "provenance_standards":["W3C PROV-O","RO-Crate 1.3","SHA-256"],
            "scientific_decision_log_enabled":True,
            "human_validation_gates_enabled":True,
            "scientific_snapshots_enabled":True,
            "corpus_map_enabled":True,
            "grounded_corpus_mode_enabled":True,
        },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    for rel,h in TABLES.items():write_csv(root/rel,h)
    seed_cada(root/"00_Gestao_e_Continuidade/11_CADA_Control.csv",a.name,pm)
    seed_gates(root/"00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv")

    trace=root/"00_Gestao_e_Continuidade/13_Traceability_Log.csv"
    with trace.open("r",encoding="utf-8-sig",newline="") as f:
        trace_rows=list(csv.DictReader(f))
    if not trace_rows:
        with trace.open("w",newline="",encoding="utf-8-sig") as f:
            w=csv.DictWriter(f,fieldnames=TABLES["00_Gestao_e_Continuidade/13_Traceability_Log.csv"])
            w.writeheader()
            w.writerow({
                "Trace_ID":"TRACE-0001","Timestamp":date.today().isoformat(),"Scientific_stage":"00",
                "CADA_ID":"CADA-0001","Actor":"SCRIPT","AI_platform_or_tool":"init_project.py",
                "Model_or_version":"","Action_type":"WORKSPACE_INITIALIZATION",
                "Action_summary":"Initialized canonical workspace, C.A.D.A. matrix, traceability and management artifacts.",
                "Input_or_source":"User project name/problem","Source_or_artifact_IDs":"",
                "Decision_or_output":"Canonical project structure created.","Rationale":"Start persistent provenance before substantive research.",
                "Artifact_before":"","Artifact_after":"00_Gestao_e_Continuidade/",
                "Verification_method":"File/table creation","Human_validation":"PENDING",
                "Related_Search_IDs":"","Related_Record_IDs":"","Related_Evidence_IDs":"","Related_Claim_IDs":"",
                "Prompt_or_instruction_summary":"Initialize article research project.","Reproducibility_information":"Run init_project.py with project arguments.",
                "Materiality":"ADMINISTRATIVE","Status":"COMPLETE","Notes":""
            })

    dash=root/"00_Gestao_e_Continuidade/15_CADA_Dashboard.csv"
    with dash.open("r",encoding="utf-8-sig",newline="") as f:
        dash_rows=list(csv.DictReader(f))
    if not dash_rows:
        today=date.today().isoformat()
        metrics=[
            ("Management_mode","MATRIX_PLUS_EXTERNAL" if pm else "MATRIX_ONLY","Spreadsheet is always canonical."),
            ("Current_scientific_stage","01 — Novelty audit",""),
            ("Current_stage_outcome","Nearest literature assessed and contribution/question refined.",""),
            ("Total_active_items","2",""),
            ("Ready_items","1",""),
            ("In_progress_items","0",""),
            ("Waiting_items","0",""),
            ("Blocked_items","0",""),
            ("Next_CADA_ID","CADA-0002",""),
            ("Next_action","Run first novelty/terminology scan.",""),
            ("Next_owner","AGENT",""),
            ("Next_due","TO_DEFINE",""),
            ("Traceability_gaps","0","Initial trace event created."),
            ("Substantive_AI_uses_unreviewed","0",""),
            ("External_PM_provider",pm or "NONE",""),
            ("External_PM_sync_health","NOT_APPLICABLE" if not pm else "NOT_INITIALIZED",""),
            ("Material_decisions","0",""),
            ("Next_human_gate","GATE-0001","Question & contribution"),
            ("Snapshots","0",""),
        ]
        with dash.open("w",newline="",encoding="utf-8-sig") as f:
            w=csv.DictWriter(f,fieldnames=TABLES["00_Gestao_e_Continuidade/15_CADA_Dashboard.csv"])
            w.writeheader()
            for metric,value,notes in metrics:
                w.writerow({"Metric":metric,"Value":value,"Last_updated":today,"Notes":notes})

    rast=root/"00_Gestao_e_Continuidade/RASTREABILIDADE.md"
    if not rast.exists():
        rast.write_text(f"""# RASTREABILIDADE — {a.name}

Updated: {date.today().isoformat()}

## Purpose

This file explains how the article is being constructed. It complements CONTINUIDADE.md, which explains the current state and next action.

## Project origin
- Original research input: {a.problem or '[USER INPUT REQUIRED]'}
- Article/review design: {a.article_type}

## Management mode
- C.A.D.A.: enabled
- Spreadsheet/matrix: canonical
- External work manager: {pm or 'none'}
- Mode: {'MATRIX_PLUS_EXTERNAL' if pm else 'MATRIX_ONLY'}

## Process provenance
- TRACE-0001 — canonical workspace initialized before substantive research.

## AI use
- No substantive AI-use event has yet been recorded in 14_AI_Use_Log.

## Method and search provenance
- Not started.

## Corpus and evidence provenance
- Not started.

## Synthesis and manuscript provenance
- Not started.

## Human validation checkpoints
- Initial workspace creation: pending researcher review.

## Provenance gaps
- None known at initialization.
""",encoding="utf-8")

    cont=root/"00_Gestao_e_Continuidade/CONTINUIDADE.md"
    if not cont.exists():
        cont.write_text(f"""# CONTINUIDADE — {a.name}
Updated: {date.today().isoformat()}

## 1. User research input
{a.problem or '[USER INPUT REQUIRED]'}

## 2. Current research object
- Current question: [TO REFINE]
- Objective: [TO REFINE]
- Intended contribution: [TO REFINE]
- Article/review design: {a.article_type}
- Scope and exclusions: [TO DEFINE]

## 3. Tool and plugin status
- Persistent workspace: LOCAL MIRROR
- Academic discovery: UNKNOWN
- Citation context: UNKNOWN
- Academic web/publisher retrieval: UNKNOWN
- Scopus access: UNKNOWN
- Web of Science access: UNKNOWN
- Work-management mode: {'MATRIX_PLUS_EXTERNAL' if pm else 'MATRIX_ONLY'}
- Spreadsheet/matrix management: ACTIVE
- Work-management provider: {pm or 'NONE / OPTIONAL'}
- Traceability: ACTIVE
- Interoperable provenance: ACTIVE — W3C PROV-O / RO-Crate 1.3 / SHA-256
- Scientific decision log: ACTIVE
- Human validation gates: ACTIVE
- Scientific snapshots: ACTIVE
- Corpus Map: AVAILABLE AFTER RETAINED CORPUS
- Grounded Corpus Mode: AVAILABLE AFTER VALIDATED FULL TEXT

## 4. Canonical workspace links
- Project root: local mirror
- Master matrix: 00_Gestao_e_Continuidade/MATRIZ_MESTRA_{slug(a.name)}.xlsx when generator is available; CSV mirrors remain canonical-compatible
- Protocol: 00_Gestao_e_Continuidade/PROTOCOLO.md
- C.A.D.A. control: 00_Gestao_e_Continuidade/11_CADA_Control.csv
- PM sync: 00_Gestao_e_Continuidade/12_PM_Sync.csv
- Traceability log: 00_Gestao_e_Continuidade/13_Traceability_Log.csv
- AI use log: 00_Gestao_e_Continuidade/14_AI_Use_Log.csv
- C.A.D.A. dashboard: 00_Gestao_e_Continuidade/15_CADA_Dashboard.csv
- Traceability summary: 00_Gestao_e_Continuidade/RASTREABILIDADE.md
- Interoperability export log: 00_Gestao_e_Continuidade/16_Interoperabilidade.csv
- Scientific decisions: 00_Gestao_e_Continuidade/17_Decision_Log.csv
- Human validation gates: 00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv
- Scientific snapshots: 00_Gestao_e_Continuidade/19_Snapshots.csv
- Snapshot directory: 00_Gestao_e_Continuidade/Snapshots/
- Corpus Map: 04_Evidencias_e_Sintese/MAPA_CORPUS.md (generated only when real retained corpus exists)
- Corpus Map data: 04_Evidencias_e_Sintese/MAPA_CORPUS.json
- Manuscript: not started

## 5. Frozen decisions
- C.A.D.A. operational governance enabled.
- Spreadsheet/matrix management is the universal default.
- External work manager is an optional operational mirror, never the scientific source of truth.
- Scientific-process traceability is enabled from project initialization.
- W3C PROV / RO-Crate export is available for audit snapshots and submission packages.
- Material scientific decisions receive DEC_ID values.
- Seven default human validation gates govern critical scientific transitions without interrupting routine autonomy.
- Frozen project states receive SNAP_ID values and SHA-256 manifests.
- Corpus mapping remains data-driven and exploratory unless the research design explicitly adopts bibliometrics.
- Grounded Corpus Mode is restricted to validated full text and never silently supplements from model memory.

## 6. Search status
- Not started.

## 7. Deduplication and screening status
- Not started.

## 8. Full-text status
- Not started.

## 9. Evidence-matrix status
- Not started.

## 10. Synthesis status
- Not started.

## 11. Manuscript status
- Not started.

## 12. Journal/submission status
- Not started.

## 13. Open issues and blockers
- Refine research object and run novelty audit.

## 14. Next valid action
- CADA_ID: CADA-0002
- Action: Run first novelty/terminology scan.
- Owner: AGENT
- Due: TO_DEFINE

## 15. Change log
- {date.today().isoformat()} — workspace initialized with C.A.D.A. governance.

## 16. C.A.D.A. dashboard

### Current stage
- Stage: 01 — Novelty audit
- Stage outcome required: nearest literature assessed and contribution/question refined.

### Active work
- READY: CADA-0002
- IN_PROGRESS: none
- WAITING/BLOCKED: CADA-0003 waits for CADA-0002

### Deadlines
- Hard/external: none known
- Internal targets: TO_DEFINE

### Next valid action
- CADA_ID: CADA-0002
- Action: Run first novelty/terminology scan.
- Owner: AGENT
- Due: TO_DEFINE

### Recently completed
- CADA-0001 — workspace scaffold created.

### Management sync
- Provider: {pm or 'NONE / TO DETECT'}
- Container: not initialized
- Last sync: never
- Conflicts: none

## 17. Scientific governance
- Material decisions: none yet
- Next human validation gate: GATE-0001 — Question & contribution
- Frozen snapshots: none yet
- Gate policy: routine actions remain autonomous; approval is requested only when a required gate becomes READY
""",encoding="utf-8")

    # Generate the official visual workbook when the reference spreadsheet
    # implementation is available. CSV mirrors remain as a compatibility layer.
    matrix=root/f"00_Gestao_e_Continuidade/MATRIZ_MESTRA_{slug(a.name)}.xlsx"
    matrix_status="EXISTS" if matrix.exists() else "NOT_CREATED"
    if not matrix.exists():
        builder=Path(__file__).with_name("build_matrix_template.py")
        if builder.exists():
            cmd=[
                sys.executable,str(builder),
                "--output",str(matrix),
                "--project-name",a.name,
                "--problem",a.problem,
                "--article-type",a.article_type,
                "--pm-provider",(pm or "NONE"),
            ]
            try:
                subprocess.run(cmd,check=True,capture_output=True,text=True)
                matrix_status="CREATED"
            except Exception as exc:
                matrix_status=f"FALLBACK_CSV: {type(exc).__name__}"
        else:
            matrix_status="FALLBACK_CSV: builder_missing"

    prot=root/"00_Gestao_e_Continuidade/PROTOCOLO.md"
    if not prot.exists():
        prot.write_text(f"""# PROTOCOLO — {a.name}

## Original research input
{a.problem or '[TO DEFINE]'}

## Current research question
[TO REFINE]

## Objective
[TO REFINE]

## Intended contribution
[TO REFINE AFTER NOVELTY AUDIT]

## Article/review design
{a.article_type}

## Scope and exclusions
[TO DEFINE]

## Databases and source roles
[TO DEFINE]

## Date/language/document-type rules
[TO DEFINE]

## Inclusion criteria
[TO DEFINE]

## Exclusion criteria
[TO DEFINE]

## Search families
[TO DEFINE AND VERSION]

## Screening and full-text rules
[TO DEFINE]

## Synthesis/stopping rule
[TO DEFINE]
""",encoding="utf-8")

    print(root)
    print(f"matrix_status={matrix_status}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
