#!/usr/bin/env python3
"""Build the canonical Meu Artigo C.A.D.A. + traceability workbook.

Reference implementation for environments with artifact_tool available.
Other platforms should reproduce the same logical structure from
references/spreadsheet-template.md.

Usage:
  python build_matrix_template.py --output /path/MATRIZ_MESTRA_projeto.xlsx \
      --project-name "Project" --problem "Research problem..." --article-type undecided
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
import re
from pathlib import Path

from artifact_tool import Workbook, SpreadsheetFile


NAVY="#17324D"; TEAL="#1F6E6A"; BLUE="#2D6CDF"; LIGHT_BLUE="#EAF2FF"
LIGHT_GRAY="#F4F6F8"; MID_GRAY="#D9E0E7"; DARK="#1F2933"; WHITE="#FFFFFF"
GREEN="#2E7D32"; LIGHT_GREEN="#EAF5EA"; AMBER="#B7791F"; LIGHT_AMBER="#FFF5D9"
RED="#B42318"; LIGHT_RED="#FDECEC"; PURPLE="#6B4FA1"; LIGHT_PURPLE="#F2ECFA"

HEADER={"fill":NAVY,"font":{"bold":True,"color":WHITE},"horizontal_alignment":"center","vertical_alignment":"center","wrap_text":True}
TITLE={"fill":NAVY,"font":{"bold":True,"color":WHITE,"size":16},"vertical_alignment":"center"}
SECTION={"fill":TEAL,"font":{"bold":True,"color":WHITE},"vertical_alignment":"center"}
LABEL={"fill":LIGHT_GRAY,"font":{"bold":True,"color":DARK},"vertical_alignment":"center"}
KPI_LABEL={"fill":LIGHT_GRAY,"font":{"bold":True,"color":NAVY},"horizontal_alignment":"center","vertical_alignment":"center"}
KPI_VALUE={"fill":WHITE,"font":{"bold":True,"color":DARK,"size":14},"horizontal_alignment":"center","vertical_alignment":"center"}
BORDER={"top":{"style":"continuous","color":MID_GRAY},"bottom":{"style":"continuous","color":MID_GRAY},"left":{"style":"continuous","color":MID_GRAY},"right":{"style":"continuous","color":MID_GRAY}}

STAGES=[
["00","Entrada & Workspace",'Problem preserved; initialized workspace and governance.'],
["01","Auditoria de novidade","Literatura mais próxima avaliada; contribuição/pergunta refinada."],
["02",'Method/design','Type of article/review defined and justified.'],
["03","Protocolo",'Frozen scope, criteria, bases, search families and rules.'],
["04","Search execution","Searches performed and documented."],
["05","Validation de exports","Exports conferidos; rodadas inválidas isoladas."],
["06","Deduplicação","Corpus canônico e auditoria de duplicatas."],
["07","Screening","Decisões e justificativas registradas."],
["08","Full text","Acesso, versão e decisão de textos completos controlados."],
["09",'Evidence extraction','Completed evidence matrix.'],
["10","Síntese","Categorias, convergências, contradições e limites integrados."],
["11",'Dialogue with magazine','Journal adherence and conversation recorded.'],
["12","Manuscrito",'Writing anchored in evidence and provenance.'],
["13","Auditoria final",'Method, counts, claims, AI and references reconciled.'],
["14","Submissão","Files, checklist, protocol and receipts preserved."],
]

def excel_column(index:int)->str:
    result=""
    while index:
        index, remainder=divmod(index-1,26)
        result=chr(65+remainder)+result
    return result


def title(sheet, text, subtitle, span):
    sheet.merge_cells(span)
    sheet.get_range(span.split(":")[0]).values=[[text]]
    sheet.get_range(span).format=TITLE
    a,b=span.split(":"); c1=re.match(r"[A-Z]+",a).group(); c2=re.match(r"[A-Z]+",b).group()
    sheet.merge_cells(f"{c1}2:{c2}2")
    sheet.get_range(f"{c1}2").values=[[subtitle]]
    sheet.get_range(f"{c1}2:{c2}2").format={"fill":LIGHT_BLUE,"font":{"italic":True,"color":NAVY},"vertical_alignment":"center","wrap_text":True}

def hdr(sheet, rng):
    sheet.get_range(rng).format=HEADER
    sheet.get_range(rng).format.borders=BORDER

def body(sheet, rng):
    sheet.get_range(rng).format.borders=BORDER
    sheet.get_range(rng).format.vertical_alignment="top"
    sheet.get_range(rng).format.wrap_text=True

def widths(sheet, mapping):
    for col,w in mapping.items(): sheet.get_range(f"{col}:{col}").format.column_width=w

def build(output:Path, project_name:str, problem:str, article_type:str, pm_provider:str="NONE", target_journal:str="", journal_mode:str="JOURNAL_NEUTRAL", journal_profile_status:str="TO_DEFINE"):
    wb=Workbook.create()

    cfg=wb.worksheets.add("15_CONFIG")
    title(cfg,"CONFIGURATION AND VOCABULARIES","Controlled lists, stages and settings.","A1:H1")
    cfg.get_range("A4:D4").values=[["Lista","Value","Descrição","Ordem"]]; hdr(cfg,"A4:D4")
    lists={
      "CADA_STATUS":["CAPTURED","ASSIGNED","READY","IN_PROGRESS","WAITING","BLOCKED","DONE","CANCELLED","SUPERSEDED"],
      "PRIORIDADE":["BAIXA","MÉDIA","HIGH","CRÍTICA"],
      "TIPO_PRAZO":["EXTERNAL","USER_SET","INTERNAL_TARGET","DEPENDENCY","TO_DEFINE"],
      "ATOR":["HUMAN","AI","HUMAN+AI","DATABASE","SCRIPT","EXTERNAL_REVIEWER","EDITOR","OTHER"],
      "MATERIALIDADE_IA":["ASSISTIVE","SUBSTANTIVE","ADMINISTRATIVE","NOT_APPLICABLE"],
      "DECISAO_IA":["ACCEPTED","MODIFIED","REJECTED","PENDING"],
      "PASS1":["INCLUDE","BORDERLINE","EXCLUDE"],
      "PASS2":["FULL TEXT — CORE","FULL TEXT — SUPPORT","EXCLUDE"],
      "EPISTEMICO":["[L]","[I]","[P]"],
      "STATUS_GERAL":["PLANNED","IN_PROGRESS","COMPLETE","VALID","INVALID","SUPERSEDED","PENDING ACCESS","FROZEN","NOT APPLICABLE"],
      "MODO_GESTAO":["MATRIX_ONLY","MATRIX_PLUS_EXTERNAL"],
      "PROVIDER_PM":["NONE","CLICKUP","JIRA","TRELLO","OTHER"],
      "DECISION_TYPE":["QUESTION_CONTRIBUTION","METHOD","SCOPE","SEARCH","SCREENING","FULL_TEXT","EVIDENCE","SYNTHESIS","CLAIM","MANUSCRIPT","JOURNAL","SUBMISSION","OTHER"],
      "DECISION_STATUS":["PROPOSED","APPROVED","REJECTED","FROZEN","SUPERSEDED"],
      "GATE_DECISION":["PENDING","APPROVED","APPROVED_WITH_CHANGES","REJECTED","NOT_APPLICABLE"],
      "GATE_STATUS":["PENDING","READY","COMPLETED","NOT_APPLICABLE"],
      "SNAPSHOT_STATUS":["VALID","INVALID","PENDING"],
      "JOURNAL_MODE":["JOURNAL_NEUTRAL","JOURNAL_AWARE_PENDING_PROFILE","JOURNAL_AWARE"],
      "JOURNAL_PROFILE_STATUS":["TO_DEFINE","PENDING_RULES","LOADED","VERIFIED","SUPERSEDED"],
      "CLAIM_ROBUSTNESS":["NOT_AUDITED","ROBUST","QUALIFIED","REVISE","REJECT","NOT_APPLICABLE"],
      "HUMAN_VALIDATION":["PENDING","VALIDATED","REVISED","REJECTED","NOT_APPLICABLE"],
      "ANONYMIZATION_STATUS":["TO_CONFIGURE","CONFIGURED","VERIFIED","NOT_REQUIRED"],
      "EXTERNAL_ARTIFACT_MODE":["EXTERNAL_ANONYMIZED","EXTERNAL_IDENTIFIED","INTERNAL_IDENTIFIED"],
      "LITERATURE_ROLE":["FOUNDATIONAL","CANONICAL","CLASSIC_CRITIQUE","METHOD_FOUNDATIONAL","CONTEMPORARY_UPDATE","EMPIRICAL_SUPPORT","CONTRARY_EVIDENCE","CONTEXT","OTHER"],
      "PRIMARY_SOURCE_STATUS":["PRIMARY_VERIFIED","SECONDARY_ONLY","NOT_VERIFIED","NOT_APPLICABLE"],
    }
    rows=[]
    for ln,vals in lists.items():
        for i,v in enumerate(vals,1): rows.append([ln,v,"",i])
    cfg.get_range(f"A5:D{4+len(rows)}").values=rows; body(cfg,f"A5:D{4+len(rows)}")
    cfg.get_range("F4:H4").values=[["Stage","Name","Expected result"]]; hdr(cfg,"F4:H4")
    cfg.get_range("F5:H19").values=STAGES; body(cfg,"F5:H19")
    widths(cfg,{"A":20,"B":24,"C":48,"D":10,"F":9,"G":24,"H":58}); cfg.freeze_panes.freeze_rows(4)

    proj=wb.worksheets.add("03_PROJETO")
    title(proj,'PROJECT’S SCIENTIFIC IDENTITY','Problem, question, objective, contribution, method and scope.',"A1:D1")
    proj.get_range("A4:D4").values=[["Field","Value","Status","Last updated"]]; hdr(proj,"A4:D4")
    vals=[
      ['Short project title',project_name,"PLANNED",date.today()],
      ['Original problem',problem or "[INSERT THE RESEARCHER'S ORIGINAL TEXT]","FROZEN",date.today()],
      ["Current research question","[TO REFINE]","IN_PROGRESS",date.today()],
      ["Objective","[TO REFINE]","IN_PROGRESS",date.today()],
      ["Intended contribution","[TO VERIFY IN THE NOVELTY AUDIT]","IN_PROGRESS",date.today()],
      ['Methodological design',article_type,"PLANNED",date.today()],
      ["Scope and exclusions","[TO DEFINE]","PLANNED",date.today()],
      ["Target journal",target_journal or '[NOT DEFINED]',"PLANNED" if not target_journal else "IN_PROGRESS",date.today()],
      ["Editorial construction mode",journal_mode,"FROZEN" if journal_mode=="JOURNAL_NEUTRAL" else "IN_PROGRESS",date.today()],
      ['Journal profile',journal_profile_status,"PLANNED" if journal_profile_status in {"TO_DEFINE","PENDING_RULES"} else "IN_PROGRESS",date.today()],
      ["Languages","Interaction: AUTO; manuscript: UNDECIDED","PLANNED",date.today()],
      ["Search period","[TO DEFINE]","PLANNED",date.today()],
      ['Current stage',"01 — Novelty audit","IN_PROGRESS",date.today()],
      ["Management mode","MATRIX_PLUS_EXTERNAL" if pm_provider!="NONE" else "MATRIX_ONLY","FROZEN",date.today()],
      ["External work manager",pm_provider,"NOT APPLICABLE" if pm_provider=="NONE" else "IN_PROGRESS",date.today()],
      ["Traceability enabled","YES","FROZEN",date.today()],
      ["Default external-file mode","EXTERNAL_ANONYMIZED","FROZEN",date.today()],
      ["Anonymization profile","TO_CONFIGURE","PLANNED",date.today()],
    ]
    proj.get_range("A5:D22").values=vals; body(proj,"A5:D22")
    proj.get_range("D5:D22").format.number_format="yyyy-mm-dd"
    proj.get_range("C5:C22").data_validation={"rule":{"type":"list","values":lists["STATUS_GERAL"]}}
    widths(proj,{"A":28,"B":70,"C":20,"D":18}); proj.freeze_panes.freeze_rows(4)

    cada=wb.worksheets.add("01_CADA")
    title(cada,"GESTÃO C.A.D.A.",'Capture → Assign → Set deadline → Track.',"A1:S1")
    ch=["CADA_ID","Stage","Task","Owner","Next action","Deadline",'Type of deadline',"Status","Priority","Dependencies","Blocker",'Evidence of advancement','Evidence of Conclusion',"Related artifact","Last updated","Trace_IDs","PM Provider","External Item ID",'Observations']
    cada.get_range("A4:S4").values=[ch]; hdr(cada,"A4:S4")
    seed=[
      ["CADA-0001","00 — Intake & workspace",'Initialize research workspace',"AGENT","Verify canonical artifacts and start a novelty audit",None,"TO_DEFINE","DONE","HIGH","","","Workspace created","CONTINUIDADE + protocolo + matriz","00_Gestao_e_Continuidade",date.today(),"TRACE-0001",pm_provider,"",""],
      ["CADA-0002","01 — Novelty audit","Carry out the initial novelty and terminology audit","AGENT","Locate the nearest literature and critically check the proposed contribution",None,"TO_DEFINE","READY","HIGH","CADA-0001","","","","01_Auditoria_de_Novidade",date.today(),"",pm_provider,"",""],
      ["CADA-0003",'02–03 — Method / Protocol','Define and freeze methodological design and protocol v1',"AGENT+RESEARCHER",'Wait for new audit; then propose method and protocol v1',None,"DEPENDENCY","CAPTURED","HIGH","CADA-0002","CADA-0002","","","PROTOCOLO.md",date.today(),"",pm_provider,"",""],
    ]
    cada.get_range("A5:S7").values=seed; body(cada,"A5:S500")
    cada.get_range("F5:F500").format.number_format="yyyy-mm-dd"; cada.get_range("O5:O500").format.number_format="yyyy-mm-dd"
    cada.get_range("G5:G500").data_validation={"rule":{"type":"list","values":lists["TIPO_PRAZO"]}}
    cada.get_range("H5:H500").data_validation={"rule":{"type":"list","values":lists["CADA_STATUS"]}}
    cada.get_range("I5:I500").data_validation={"rule":{"type":"list","values":lists["PRIORIDADE"]}}
    cada.get_range("Q5:Q500").data_validation={"rule":{"type":"list","values":lists["PROVIDER_PM"]}}
    cada.get_range("H5:H500").conditional_formats.add_custom('=H5="DONE"',{"fill":LIGHT_GREEN,"font":{"color":GREEN,"bold":True}})
    cada.get_range("H5:H500").conditional_formats.add_custom('=H5="BLOCKED"',{"fill":LIGHT_RED,"font":{"color":RED,"bold":True}})
    cada.get_range("H5:H500").conditional_formats.add_custom('=H5="IN_PROGRESS"',{"fill":LIGHT_BLUE,"font":{"color":BLUE,"bold":True}})
    cada.get_range("H5:H500").conditional_formats.add_custom('=H5="READY"',{"fill":LIGHT_AMBER,"font":{"color":AMBER,"bold":True}})
    cada.get_range("F5:F500").conditional_formats.add_custom('=AND(F5<TODAY(),F5<>"",H5<>"DONE",H5<>"CANCELLED",H5<>"SUPERSEDED")',{"fill":LIGHT_RED,"font":{"color":RED}})
    widths(cada,{"A":14,"B":23,"C":34,"D":18,"E":42,"F":13,"G":18,"H":18,"I":12,"J":16,"K":20,"L":30,"M":32,"N":28,"O":16,"P":18,"Q":14,"R":18,"S":30})
    cada.freeze_panes.freeze_rows(4); cada.freeze_panes.freeze_columns(3)

    tl=wb.worksheets.add("02_LINHA_TEMPO")
    title(tl,"TIMELINE AND TRACEABILITY","How we arrived here: material events in the scientific development process.","A1:T1")
    th=["Trace_ID","Timestamp","Stage","CADA_ID","Actor","Tool / AI","Model / version","Action type",'Action summary','Input/Source',"Decision / output","Rationale","Artifact before","Artifact after",'Verification method','Human validation',"Related IDs","Materiality","Status",'Observations']
    tl.get_range("A4:T4").values=[th]; hdr(tl,"A4:T4")
    tl.get_range("A5:T5").values=[["TRACE-0001",datetime.now(),"00","CADA-0001","SCRIPT","build_matrix_template.py","","WORKSPACE_INITIALIZATION","Inicialização da matriz C.A.D.A. e rastreabilidade.","Entrada inicial","Estrutura canônica criada",'Start provenance before substantive search',"","Matrix created","Conferência dos artefatos","PENDING","CADA-0001","ADMINISTRATIVE","COMPLETE",""]]
    body(tl,"A5:T500"); tl.get_range("B5:B500").format.number_format="yyyy-mm-dd hh:mm"
    tl.get_range("E5:E500").data_validation={"rule":{"type":"list","values":lists["ATOR"]}}
    tl.get_range("R5:R500").data_validation={"rule":{"type":"list","values":lists["MATERIALIDADE_IA"]}}
    widths(tl,{"A":14,"B":20,"C":10,"D":14,"E":16,"F":22,"G":18,"H":24,"I":46,"J":34,"K":40,"L":40,"M":24,"N":24,"O":30,"P":24,"Q":28,"R":18,"S":16,"T":28})
    tl.freeze_panes.freeze_rows(4); tl.freeze_panes.freeze_columns(4)

    definitions=[
      ("04_EVIDENCIAS",'EVIDENCE MAP — SYNTHETIC VIEW','A high-level view of the evidence supporting the argument.',["Evidence_ID",'Source/Quote',"Concept / category","Finding / contribution","Role","Strength / relevance","Claim_IDs","Locator / passage","Status",'Observations'],"A1:J1",{"A":14,"B":38,"C":28,"D":48,"E":18,"F":18,"G":18,"H":34,"I":16,"J":30}),
      ("05_PROTOCOLO","STUDY PROTOCOL","Versioned and justified methodological decisions.",["Item","Decision","Rationale","Status","Version","Updated at","Trace_ID"],"A1:G1",{"A":28,"B":44,"C":54,"D":16,"E":10,"F":16,"G":16}),
      ("06_BUSCAS","BIBLIOGRAPHIC SEARCH LOG","Every executed search query must remain versioned and traceable.",["Search_ID","Date",'Base/Source',"Conceptual blocks","Literal query","Filters","Found","Exported","File / URL","Status","Iteration","Trace_ID","Validation",'Observations'],"A1:N1",{"A":14,"B":13,"C":20,"D":38,"E":64,"F":38,"G":12,"H":12,"I":34,"J":16,"K":10,"L":16,"M":16,"N":32}),
      ("07_SCREENING","SCREENING","Separate AI recommendations from decisions actually reviewed by the researcher.",["Record_ID","Source","Search_ID",'Title',"Authors","Year","DOI / ID","Abstract","Type","Language","Pass1",'Reason Pass1',"Pass2",'Pass2 reason',"Duplicate","Canonical_ID","Trace_ID",'Observations',"Pass1 AI proposal",'Pass1 reason AI','Pass1 AI source',"Pass1 reviewed by",'Pass1 review evidence',"Pass1 disagreement resolution","Pass2 AI proposal",'Pass2 reason AI','Pass2 AI source',"Pass2 reviewed by",'Pass2 review evidence',"Pass2 disagreement resolution"],"A1:AD1",{"A":14,"B":16,"C":14,"D":48,"E":30,"F":9,"G":24,"H":60,"I":16,"J":12,"K":16,"L":30,"M":22,"N":30,"O":22,"P":16,"Q":16,"R":26,"S":20,"T":38,"U":32,"V":24,"W":40,"X":40,"Y":22,"Z":38,"AA":32,"AB":24,"AC":40,"AD":40}),
      ("08_FULL_TEXT","FULL-TEXT CONTROL",'Access and analysis do not imply authorization to redistribute PDFs.',["Record_ID","Priority","Status full text","Accessed version",'Access source',"Access date","Decision",'Reason for exclusion',"Evidence_ID","File / URL",'Observations',"Access basis","Rights basis","License URI",'Evidence of rights',"Permission scope","Required attribution",'SHA-256 source',"Rights reviewer",'Review evidence'],"A1:T1",{"A":14,"B":12,"C":18,"D":18,"E":28,"F":14,"G":14,"H":32,"I":14,"J":38,"K":30,"L":22,"M":22,"N":44,"O":40,"P":30,"Q":54,"R":68,"S":25,"T":44}),
      ("09_MATRIZ_EVID",'EVIDENCE MATRIX — DETAILED',"Structured extraction for cross-source synthesis, conceptual lineage and evidence-grounded writing.",["Evidence_ID",'Quote',"DOI / ID","Concept",'Definition/claim',"Role in literature","Basis of classification",'Primary source',"Conceptual lineage / relation",'Problem/tension',"Mechanism / finding",'Source design/type','Sample/data',"Context",'Process/step',"Actors / roles","Action / decision",'Observable evidence',"Boundary conditions",'Limitations',"Transferability","Role / strength","Locator","Epistemic label",'Observations','Appraisal family','Criteria/answers',"Critical appraisal judgment",'Assessment limitations','Human reviewer','Evidence review','Justification of use'],"A1:AF1",{"A":14,"B":36,"C":24,"D":26,"E":42,"F":24,"G":38,"H":22,"I":42,"J":36,"K":42,"L":24,"M":28,"N":24,"O":22,"P":22,"Q":24,"R":34,"S":34,"T":30,"U":34,"V":20,"W":34,"X":18,"Y":28,"Z":20,"AA":60,"AB":24,"AC":42,"AD":24,"AE":36,"AF":42}),
      ("10_SINTESE","CROSS-SOURCE SYNTHESIS","Traceable convergences, contradictions, limitations and inferences.",["Synthesis_ID","Theme / category","Evidence_IDs","Cross-source pattern","Contradictions","Boundary conditions","Inference","Epistemic status","Decision","Claim_IDs","Trace_ID"],"A1:K1",{"A":14,"B":28,"C":28,"D":46,"E":36,"F":36,"G":44,"H":18,"I":30,"J":24,"K":16}),
      ("11_CLAIMS",'CLAIMS LEDGER — EVIDENCE, CONTESTING AND ROBUSTNESS','Each material claim must show support, contrary evidence, limits and robustness audit results.',["Claim_ID","Manuscript section","Claim / assertion","Type","Evidence_IDs","Counter_Evidence_IDs","Locators","Alternative explanations","Boundary conditions",'Single source dependency',"Strength","Robustness","Robustness notes","Trace_IDs","Gate_ID",'Human validation',"Draft status",'Observations',"Inferential warrant","Nearest literature Evidence_IDs","Contribution delta","Novelty scope","Novelty audit Search_IDs",'Researcher review evidence'],"A1:X1",{"A":14,"B":24,"C":56,"D":20,"E":24,"F":26,"G":34,"H":42,"I":34,"J":24,"K":14,"L":18,"M":42,"N":24,"O":14,"P":20,"Q":18,"R":28,"S":48,"T":28,"U":48,"V":42,"W":30,"X":42}),
      ("12_USO_IA",'AI USE LOG','Transparency: where the AI \u200b\u200bacted, for what purpose and how there was human validation.',["AI_Use_ID","Date","Stage","CADA_ID","Trace_ID","Platform / tool","Model / version","Purpose","Input category","Output category","Materiality",'Human review method','Human decision',"Accepted / modified / rejected","Related artifacts","Disclosure required","Disclosure text / note",'Observations',"Disclosure category",'Human review evidence','Confidentiality review'],"A1:U1",{"A":14,"B":13,"C":12,"D":14,"E":14,"F":24,"G":18,"H":36,"I":24,"J":24,"K":18,"L":40,"M":28,"N":22,"O":34,"P":18,"Q":48,"R":28,"S":24,"T":42,"U":30}),
      ("13_SUBMISSAO","SUBMISSION CHECKLIST","Submission closure: rules, artifacts, deadlines, receipts and traceability.",["Item","Requirement",'Source of requirement',"Status","Deadline",'Evidence/archive',"Trace_ID",'Observations'],"A1:H1",{"A":24,"B":44,"C":30,"D":16,"E":14,"F":38,"G":16,"H":30}),
      ("14_PM_SYNC","EXTERNAL WORK MANAGER SYNC","Optional: ClickUp, Jira, Trello or equivalent; the canonical matrix remains authoritative.",["CADA_ID","Provider","Workspace / site","Container ID","External item ID","External URL","External status","External owner",'External deadline',"Canonical status","Canonical owner",'Canonical deadline',"Last push","Last pull","Sync status","Conflict",'Observations'],"A1:Q1",{"A":14,"B":14,"C":24,"D":18,"E":18,"F":38,"G":18,"H":20,"I":14,"J":18,"K":20,"L":14,"M":20,"N":20,"O":16,"P":30,"Q":30}),
    ]
    for name,ttl,subt,heads,span,wmap in definitions:
        sh=wb.worksheets.add(name); title(sh,ttl,subt,span)
        end=excel_column(len(heads))
        sh.get_range(f"A4:{end}4").values=[heads]; hdr(sh,f"A4:{end}4")
        body(sh,f"A5:{end}500"); widths(sh,wmap); sh.freeze_panes.freeze_rows(4)
        if name=="09_MATRIZ_EVID":
            sh.get_range("F5:F500").data_validation={"rule":{"type":"list","values":lists["LITERATURE_ROLE"]}}
            sh.get_range("H5:H500").data_validation={"rule":{"type":"list","values":lists["PRIMARY_SOURCE_STATUS"]}}
            sh.get_range("X5:X500").data_validation={"rule":{"type":"list","values":lists["EPISTEMICO"]}}
            sh.get_range("Z5:Z500").data_validation={"rule":{"type":"list","values":["QUANTITATIVE","QUALITATIVE","MIXED_METHODS","REVIEW","CONCEPTUAL","NORMATIVE","OTHER"]}}
            sh.get_range("AB5:AB500").data_validation={"rule":{"type":"list","values":["SUITABLE_FOR_CLAIM","USE_WITH_CAVEATS","INSUFFICIENT_INFORMATION","DO_NOT_USE_FOR_CLAIM"]}}
        if name=="13_SUBMISSAO":
            sh.get_range("A5:H9").values=[
              ["Anonymization: visible content",'Authors, affiliations, contacts, acknowledgments and identifiers consistent with the review modality.','Meu Artigo policy + journal',"PENDING",None,"","",""],
              ["Anonymization: hidden metadata","ZERO_NONESSENTIAL_METADATA: remove unnecessary Author/Creator/Producer/Generator/Application, dates, OOXML properties, XMP/EXIF/IPTC, comments/revisions, package timestamps and generator labels (Python/pypdf/ReportLab/Matplotlib/LibreOffice etc.).",'Meu Artigo policy + journal',"PENDING",None,"","",""],
              ["Anonymization: filenames, paths and links",'File names, local paths, private links, and accounts must not unduly reveal authorship.','Meu Artigo policy',"PENDING",None,"","",""],
              ["Anonymization: participants/cases","Participant, organization and location identifiers must respect confidentiality and the research protocol.",'Meu Artigo policy + protocol',"PENDING",None,"","",""],
              ["Anonymization: final audit","The exact output files must have ANONYMIZATION_AUDIT PASS or PASS_WITH_HUMAN_REVIEW.",'Meu Artigo policy',"PENDING",None,"","",""],
            ]

    interop=wb.worksheets.add("16_INTEROPERABILIDADE")
    title(interop,"INTEROPERABILIDADE E PACOTES DE PROVENIÊNCIA","Histórico de exports W3C PROV / RO-Crate, fixidade e validação.","A1:M1")
    ih=["Export_ID","Timestamp","Padrões","Pacote / URL","SHA-256 do pacote","Validation","TRACE events","PROV entities","PROV activities","PROV agents","RO-Crate files","Warnings",'Observations']
    interop.get_range("A4:M4").values=[ih]; hdr(interop,"A4:M4")
    body(interop,"A5:M200")
    interop.get_range("B5:B200").format.number_format="yyyy-mm-dd hh:mm"
    interop.get_range("F5:F200").data_validation={"rule":{"type":"list","values":["VALID","INVALID","PENDING"]}}
    interop.get_range("F5:F200").conditional_formats.add_custom('=F5="VALID"',{"fill":LIGHT_GREEN,"font":{"color":GREEN,"bold":True}})
    interop.get_range("F5:F200").conditional_formats.add_custom('=F5="INVALID"',{"fill":LIGHT_RED,"font":{"color":RED,"bold":True}})
    widths(interop,{"A":14,"B":20,"C":30,"D":48,"E":68,"F":16,"G":13,"H":14,"I":14,"J":12,"K":14,"L":48,"M":30})
    interop.freeze_panes.freeze_rows(4)

    dec=wb.worksheets.add("17_DECISOES")
    title(dec,"DECISÕES CIENTÍFICAS","O que decidimos, por quê, com base em quê e qual foi o impacto.","A1:T1")
    dh=["DEC_ID","Timestamp","Stage","Type","Pergunta decisória","Decision","Alternativas consideradas","Rationale","Evidence_IDs","Record_IDs","CADA_ID","Trace_ID","Gate_ID","Status","Decidido por","Impacto","Artefatos afetados","Versão resultante","Supersede DEC_ID",'Observations']
    dec.get_range("A4:T4").values=[dh]; hdr(dec,"A4:T4"); body(dec,"A5:T300")
    dec.get_range("B5:B300").format.number_format="yyyy-mm-dd hh:mm"
    dec.get_range("D5:D300").data_validation={"rule":{"type":"list","values":lists["DECISION_TYPE"]}}
    dec.get_range("N5:N300").data_validation={"rule":{"type":"list","values":lists["DECISION_STATUS"]}}
    dec.get_range("N5:N300").conditional_formats.add_custom('=N5="FROZEN"',{"fill":LIGHT_GREEN,"font":{"color":GREEN,"bold":True}})
    dec.get_range("N5:N300").conditional_formats.add_custom('=N5="REJECTED"',{"fill":LIGHT_RED,"font":{"color":RED,"bold":True}})
    widths(dec,{"A":14,"B":20,"C":12,"D":22,"E":42,"F":44,"G":40,"H":52,"I":24,"J":24,"K":14,"L":14,"M":14,"N":16,"O":18,"P":42,"Q":36,"R":18,"S":18,"T":30})
    dec.freeze_panes.freeze_rows(4); dec.freeze_panes.freeze_columns(5)

    gates=wb.worksheets.add("18_VALIDACOES")
    title(gates,'CRITICAL HUMAN VALIDATIONS','Few gates, only at points where advancement requires human scientific responsibility.',"A1:T1")
    gh=["GATE_ID","Type","Stage","Name","Condição de entrada","Itens a validar","DEC_IDs","CADA_IDs","Evidence_IDs","Snapshot antes","Decision","Validado por","Date",'Validation method','Evidence of validation',"Trace_ID","Snapshot depois","Status","Transição bloqueada",'Observations']
    gates.get_range("A4:T4").values=[gh]; hdr(gates,"A4:T4"); body(gates,"A5:T100")
    gate_seed=[
      ["GATE-0001","QUESTION_CONTRIBUTION","01","Question and contribution","Initial novelty examination completed.","Proposed question, aim, contribution and limits.","","CADA-0002","","","PENDING","","","","","","","PENDING",'Definition of the methodological design',""],
      ["GATE-0002","METHOD_PROTOCOL","02-03",'Method and protocol','Methodological design and protocol v1 prepared.','Method, criteria, scope, roles of the bases and screening rules.',"","CADA-0003","","","PENDING","","","","","","","PENDING","Busca em escala",""],
      ["GATE-0003","SEARCH_STRATEGY","03-04","Search strategy","Search queries and filters prepared and checked.","Conceptual blocks, strings literais, filtros e bases.","","","","","PENDING","","","","","","","PENDING","Execução das buscas canônicas",""],
      ["GATE-0004","CORPUS_FREEZE","08-09","Corpus freeze","Screening and full-text review closed with reconciled counts.","Eligible corpus, exclusions, duplicates and final counts.","","","","","PENDING","","","","","","","PENDING","Extração/síntese final do corpus",""],
      ["GATE-0005","SYNTHESIS","10","Synthesis and theoretical product","Cross-source synthesis stabilized.","Categories, contradictions, inferences and propositions/models.","","","","","PENDING","","","","","","","PENDING","Substantive manuscript drafting",""],
      ["GATE-0006","CLAIMS_AUDIT","12-13","Claims and scientific audit",'Main claims linked to evidence; contrary evidence, alternative explanations, source dependence and audited limits.','Claims, Evidence_IDs, Counter_Evidence_IDs, locators, alternative explanations, boundary conditions, source dependency, robustness, use of AI, and applicable editorial adherence.',"","","","","PENDING","","","","","","","PENDING","Final version release",""],
      ["GATE-0007","SUBMISSION_RELEASE","14","Submission readiness approval",'Canonical version, checklist, magazine profile, anonymization and transparency reconciled.',"Final manuscript, JOURNAL_PROFILE, anonymization profile, ANONYMIZATION_AUDIT, hidden metadata, verified official rules, AI-use disclosures and exact submission artifacts.","","","","","PENDING","","","","","","","PENDING","External submission",""],
    ]
    gates.get_range("A5:T11").values=gate_seed
    gates.get_range("K5:K100").data_validation={"rule":{"type":"list","values":lists["GATE_DECISION"]}}
    gates.get_range("R5:R100").data_validation={"rule":{"type":"list","values":lists["GATE_STATUS"]}}
    gates.get_range("M5:M100").format.number_format="yyyy-mm-dd hh:mm"
    gates.get_range("R5:R100").conditional_formats.add_custom('=R5="READY"',{"fill":LIGHT_AMBER,"font":{"color":AMBER,"bold":True}})
    gates.get_range("R5:R100").conditional_formats.add_custom('=R5="COMPLETED"',{"fill":LIGHT_GREEN,"font":{"color":GREEN,"bold":True}})
    widths(gates,{"A":14,"B":24,"C":12,"D":30,"E":44,"F":52,"G":22,"H":22,"I":24,"J":16,"K":24,"L":20,"M":20,"N":42,"O":40,"P":16,"Q":16,"R":18,"S":34,"T":30})
    gates.freeze_panes.freeze_rows(4); gates.freeze_panes.freeze_columns(4)

    snaps=wb.worksheets.add("19_SNAPSHOTS")
    title(snaps,"SCIENTIFIC SNAPSHOTS",'Frozen, verifiable, and comparable project states.',"A1:Q1")
    sh=["SNAP_ID","Timestamp","Marco","Stage","Trigger","Gate_ID","DEC_IDs","CADA_IDs","SNAP anterior","Caminho / URL","Manifest","SHA-256 do manifest","Artefatos canônicos",'Change summary',"Validation","EXPORT_ID",'Observations']
    snaps.get_range("A4:Q4").values=[sh]; hdr(snaps,"A4:Q4"); body(snaps,"A5:Q200")
    snaps.get_range("B5:B200").format.number_format="yyyy-mm-dd hh:mm"
    snaps.get_range("O5:O200").data_validation={"rule":{"type":"list","values":lists["SNAPSHOT_STATUS"]}}
    snaps.get_range("O5:O200").conditional_formats.add_custom('=O5="VALID"',{"fill":LIGHT_GREEN,"font":{"color":GREEN,"bold":True}})
    snaps.get_range("O5:O200").conditional_formats.add_custom('=O5="INVALID"',{"fill":LIGHT_RED,"font":{"color":RED,"bold":True}})
    widths(snaps,{"A":14,"B":20,"C":30,"D":12,"E":18,"F":14,"G":22,"H":22,"I":16,"J":46,"K":46,"L":68,"M":54,"N":48,"O":16,"P":14,"Q":30})
    snaps.freeze_panes.freeze_rows(4); snaps.freeze_panes.freeze_columns(3)

    cmap=wb.worksheets.add("20_MAPA_CORPUS")
    title(cmap,"MAPA DO CORPUS","Visão exploratória da estrutura do corpus validado. Nenhum dado é inventado; campos permanecem vazios até haver metadados reais.","A1:O1")
    cmap.get_range("A4:D4").values=[["Visão geral","Value",'Source/rule',"Updated at"]]; hdr(cmap,"A4:D4")
    cmap.get_range("A5:A9").values=[["Registros retidos"],["FULL TEXT — CORE"],["FULL TEXT — SUPPORT"],["Evidence_IDs"],["Claim_IDs"]]
    cmap.get_range("A5:A9").format=LABEL
    cmap.get_range("B5").formulas=[["=COUNTIF('07_SCREENING'!$M$5:$M$1000,\"FULL TEXT — CORE\")+COUNTIF('07_SCREENING'!$M$5:$M$1000,\"FULL TEXT — SUPPORT\")"]]
    cmap.get_range("B6").formulas=[["=COUNTIF('07_SCREENING'!$M$5:$M$1000,\"FULL TEXT — CORE\")"]]
    cmap.get_range("B7").formulas=[["=COUNTIF('07_SCREENING'!$M$5:$M$1000,\"FULL TEXT — SUPPORT\")"]]
    cmap.get_range("B8").formulas=[["=COUNTA('09_MATRIZ_EVID'!$A$5:$A$500)"]]
    cmap.get_range("B9").formulas=[["=COUNTA('11_CLAIMS'!$A$5:$A$500)"]]
    cmap.get_range("C5:C9").values=[["Pass2 decision"],["Pass2 decision"],["Pass2 decision"],['Evidence matrix'],["Claims ledger"]]
    body(cmap,"A5:D9")

    cmap.get_range("A12:B12").values=[["Publicações por ano","Count"]]; hdr(cmap,"A12:B12")
    cmap.get_range("D12:E12").values=[['Most recurring authors',"Count"]]; hdr(cmap,"D12:E12")
    cmap.get_range("G12:H12").values=[["Journals / sources","Count"]]; hdr(cmap,"G12:H12")
    cmap.get_range("J12:K12").values=[["Keywords / conceitos","Count"]]; hdr(cmap,"J12:K12")
    cmap.get_range("M12:O12").values=[["Estrutura de rede","Value","Regra / observação"]]; hdr(cmap,"M12:O12")
    body(cmap,"A13:B40"); body(cmap,"D13:E40"); body(cmap,"G13:H40"); body(cmap,"J13:K40"); body(cmap,"M13:O40")
    cmap.get_range("M13:M17").values=[['edge method'],["Clusters"],["Artigos-ponte"],["Cobertura de enriquecimento"],["Warnings"]]
    cmap.get_range("M13:M17").format=LABEL
    cmap.get_range("N13:O17").values=[
      ["","Populate only if there is a real, documented network model."],
      ["",'Do not generate bibliometric clusters based on semantic similarity alone.'],
      ["",'Require operational basis: citation, co-authorship, coupling, co-citation or co-occurrence.'],
      ["",'Register OpenAlex/Crossref or other source when actually used.'],
      ["","Metadados ausentes devem permanecer explicitamente ausentes."],
    ]
    body(cmap,"M13:O17")
    cmap.merge_cells("A43:O43")
    cmap.get_range("A43").values=[['The tab is a view of the validated corpus. Use scripts/build_corpus_map.py or equivalent tool to fill in real metadata only. An exploratory map does not transform the drawing into bibliometrics.']]
    cmap.get_range("A43:O43").format={"fill":LIGHT_BLUE,"font":{"italic":True,"color":NAVY},"wrap_text":True}
    widths(cmap,{"A":24,"B":14,"C":28,"D":18,"E":14,"F":4,"G":30,"H":14,"I":4,"J":30,"K":14,"L":4,"M":24,"N":24,"O":48})
    cmap.freeze_panes.freeze_rows(4)

    wb.worksheets.get_item("05_PROTOCOLO").get_range("A5:G12").values=[
      ['Type of article/review',"[TO DEFINE]","Depends on the purpose and real novelty audit.","PLANNED","v0",date.today(),""],
      ['Target magazine/editorial agreement',target_journal or "TO_DEFINE",f"Mode: {journal_mode}; profile: {journal_profile_status}. Editorial rules guide presentation, not results or evidence.","PLANNED" if not target_journal else "IN_PROGRESS","v0",date.today(),""],
      ["Scope","[TO DEFINE]","","PLANNED","v0",date.today(),""],
      ['Inclusion criteria',"[TO DEFINE]","","PLANNED","v0",date.today(),""],
      ['Exclusion criteria',"[TO DEFINE]","","PLANNED","v0",date.today(),""],
      ["Databases and roles","[TO DEFINE]","","PLANNED","v0",date.today(),""],
      ["Full-text rule","[TO DEFINE]","","PLANNED","v0",date.today(),""],
      ["Synthesis/stopping rule","[TO DEFINE]","","PLANNED","v0",date.today(),""],
    ]
    wb.worksheets.get_item("07_SCREENING").get_range("K5:K1000").data_validation={"rule":{"type":"list","values":lists["PASS1"]}}
    wb.worksheets.get_item("07_SCREENING").get_range("M5:M1000").data_validation={"rule":{"type":"list","values":lists["PASS2"]}}
    wb.worksheets.get_item("07_SCREENING").get_range("S5:S1000").data_validation={"rule":{"type":"list","values":lists["PASS1"]}}
    wb.worksheets.get_item("07_SCREENING").get_range("Y5:Y1000").data_validation={"rule":{"type":"list","values":lists["PASS2"]}}
    wb.worksheets.get_item("09_MATRIZ_EVID").get_range("T5:T500").data_validation={"rule":{"type":"list","values":lists["EPISTEMICO"]}}
    ai=wb.worksheets.get_item("12_USO_IA")
    ai.get_range("K5:K500").data_validation={"rule":{"type":"list","values":lists["MATERIALIDADE_IA"]}}
    ai.get_range("N5:N500").data_validation={"rule":{"type":"list","values":lists["DECISAO_IA"]}}
    claims=wb.worksheets.get_item("11_CLAIMS")
    claims.get_range("L5:L500").data_validation={"rule":{"type":"list","values":lists["CLAIM_ROBUSTNESS"]}}
    claims.get_range("P5:P500").data_validation={"rule":{"type":"list","values":lists["HUMAN_VALIDATION"]}}
    claims.get_range("L5:L500").conditional_formats.add_custom('=L5="ROBUST"',{"fill":LIGHT_GREEN,"font":{"color":GREEN,"bold":True}})
    claims.get_range("L5:L500").conditional_formats.add_custom('=L5="QUALIFIED"',{"fill":LIGHT_AMBER,"font":{"color":AMBER,"bold":True}})
    claims.get_range("L5:L500").conditional_formats.add_custom('=OR(L5="REVISE",L5="REJECT")',{"fill":LIGHT_RED,"font":{"color":RED,"bold":True}})


    dash=wb.worksheets.add("00_PAINEL")
    title(dash,'MEU ARTIGO — SCIENTIFIC GOVERNANCE PANEL',"Where are we? What remains? How did we get here? Where was AI used?","A1:L1")
    dash.get_range("A4:B4").values=[["Project","Value"]]; hdr(dash,"A4:B4")
    dash.get_range("A5:A11").values=[['Title'],['Current stage'],["Management mode"],["External work manager"],["Last updated"],["Target journal"],["Modo editorial"]]
    dash.get_range("A5:A11").format=LABEL
    dash.get_range("B5").formulas=[["=IFERROR(INDEX('03_PROJETO'!$B$5:$B$30,MATCH(\"Short project title\",'03_PROJETO'!$A$5:$A$30,0)),\"[TO DEFINE]\")"]]
    dash.get_range("B6").formulas=[["=IFERROR(INDEX('03_PROJETO'!$B$5:$B$30,MATCH(\"Current stage\",'03_PROJETO'!$A$5:$A$30,0)),\"—\")"]]
    dash.get_range("B7").formulas=[["=IFERROR(INDEX('03_PROJETO'!$B$5:$B$30,MATCH(\"Management mode\",'03_PROJETO'!$A$5:$A$30,0)),\"MATRIX_ONLY\")"]]
    dash.get_range("B8").formulas=[["=IFERROR(INDEX('03_PROJETO'!$B$5:$B$30,MATCH(\"External work manager\",'03_PROJETO'!$A$5:$A$30,0)),\"NONE\")"]]
    dash.get_range("B9").formulas=[["=TODAY()"]]; dash.get_range("B9").format.number_format="yyyy-mm-dd"
    dash.get_range("B10").formulas=[["=IFERROR(INDEX('03_PROJETO'!$B$5:$B$30,MATCH(\"Target journal\",'03_PROJETO'!$A$5:$A$30,0)),\"[UNDEFINED]\")"]]
    dash.get_range("B11").formulas=[["=IFERROR(INDEX('03_PROJETO'!$B$5:$B$30,MATCH(\"Editorial construction mode\",'03_PROJETO'!$A$5:$A$30,0)),\"JOURNAL_NEUTRAL\")"]]
    body(dash,"A5:B11")

    cards=[
      ("D4:E4","D5:E6","Avanço C.A.D.A.","=IFERROR(COUNTIF('01_CADA'!$H$5:$H$500,\"DONE\")/COUNTA('01_CADA'!$A$5:$A$500),0)","0%"),
      ("F4:G4","F5:G6","Active items","=COUNTIF('01_CADA'!$H$5:$H$500,\"READY\")+COUNTIF('01_CADA'!$H$5:$H$500,\"IN_PROGRESS\")+COUNTIF('01_CADA'!$H$5:$H$500,\"WAITING\")+COUNTIF('01_CADA'!$H$5:$H$500,\"BLOCKED\")","0"),
      ("H4:I4","H5:I6","Bloqueados","=COUNTIF('01_CADA'!$H$5:$H$500,\"BLOCKED\")","0"),
      ("J4:K4","J5:K6","Vencidos","=COUNTIFS('01_CADA'!$F$5:$F$500,\"<\"&TODAY(),'01_CADA'!$F$5:$F$500,\">0\",'01_CADA'!$H$5:$H$500,\"<>DONE\",'01_CADA'!$H$5:$H$500,\"<>CANCELLED\",'01_CADA'!$H$5:$H$500,\"<>SUPERSEDED\")","0"),
    ]
    for lr,vr,label,formula,nf in cards:
        dash.merge_cells(lr); dash.merge_cells(vr)
        dash.get_range(lr.split(":")[0]).values=[[label]]; dash.get_range(lr).format=KPI_LABEL
        dash.get_range(vr.split(":")[0]).formulas=[[formula]]; dash.get_range(vr).format=KPI_VALUE; dash.get_range(vr).format.number_format=nf

    dash.merge_cells("A12:F12"); dash.get_range("A12").values=[["PRÓXIMA AÇÃO"]]; dash.get_range("A12:F12").format=SECTION
    dash.get_range("A13:A16").values=[["CADA_ID"],["Ação"],["Owner"],["Deadline"]]; dash.get_range("A13:A16").format=LABEL
    for r in range(13,17): dash.merge_cells(f"B{r}:F{r}")
    dash.get_range("B13").formulas=[["=IFERROR(INDEX('01_CADA'!$A$5:$A$500,MATCH(\"IN_PROGRESS\",'01_CADA'!$H$5:$H$500,0)),IFERROR(INDEX('01_CADA'!$A$5:$A$500,MATCH(\"READY\",'01_CADA'!$H$5:$H$500,0)),\"—\"))"]]
    dash.get_range("B14").formulas=[["=IFERROR(INDEX('01_CADA'!$E$5:$E$500,MATCH(B13,'01_CADA'!$A$5:$A$500,0)),\"—\")"]]
    dash.get_range("B15").formulas=[["=IFERROR(INDEX('01_CADA'!$D$5:$D$500,MATCH(B13,'01_CADA'!$A$5:$A$500,0)),\"—\")"]]
    dash.get_range("B16").formulas=[["=IFERROR(INDEX('01_CADA'!$F$5:$F$500,MATCH(B13,'01_CADA'!$A$5:$A$500,0)),\"—\")"]]
    dash.get_range("B16").format.number_format="yyyy-mm-dd"; body(dash,"A13:F16")

    dash.merge_cells("H12:L12"); dash.get_range("H12").values=[["TRACEABILITY & AI"]]; dash.get_range("H12:L12").format=SECTION
    dash.get_range("H13:H16").values=[["Evidence-backed DONE tasks"],["TRACE events"],["Human-reviewed substantive AI"],["Verified claims"]]; dash.get_range("H13:H16").format=LABEL
    for r in range(13,17): dash.merge_cells(f"I{r}:L{r}")
    dash.get_range("I13").formulas=[["=IFERROR(COUNTIFS('01_CADA'!$H$5:$H$500,\"DONE\",'01_CADA'!$M$5:$M$500,\"<>\")/COUNTIF('01_CADA'!$H$5:$H$500,\"DONE\"),0)"]]; dash.get_range("I13").format.number_format="0%"
    dash.get_range("I14").formulas=[["=COUNTA('02_LINHA_TEMPO'!$A$5:$A$500)"]]
    dash.get_range("I15").formulas=[["=COUNTIFS('12_USO_IA'!$K$5:$K$500,\"SUBSTANTIVE\",'12_USO_IA'!$N$5:$N$500,\"<>PENDING\")&\"/\"&COUNTIF('12_USO_IA'!$K$5:$K$500,\"SUBSTANTIVE\")"]]
    dash.get_range("I16").formulas=[["=COUNTIF('11_CLAIMS'!$J$5:$J$500,\"VERIFIED\")&\"/\"&COUNTA('11_CLAIMS'!$A$5:$A$500)"]]; body(dash,"H13:L16")

    dash.get_range("A19:B19").values=[["C.A.D.A. status","Count"]]; hdr(dash,"A19:B19")
    st=["CAPTURED","ASSIGNED","READY","IN_PROGRESS","WAITING","BLOCKED","DONE","CANCELLED","SUPERSEDED"]
    dash.get_range("A20:A28").values=[[x] for x in st]
    dash.get_range("B20:B28").formulas=[[f'=COUNTIF(\'01_CADA\'!$H$5:$H$500,A{r})'] for r in range(20,29)]
    body(dash,"A20:B28")
    try:
        chart=dash.charts.add("bar",dash.get_range("A19:B28")); chart.title_text="C.A.D.A. item status"; chart.has_legend=False; chart.set_position("A31","F46")
    except Exception:
        pass

    dash.merge_cells("H19:L19"); dash.get_range("H19").values=[["SCIENTIFIC GOVERNANCE"]]; dash.get_range("H19:L19").format=SECTION
    dash.get_range("H20:H23").values=[["Next gate"],["Recorded decisions"],["Snapshots"],["Gate status"]]; dash.get_range("H20:H23").format=LABEL
    for rr in range(20,24): dash.merge_cells(f"I{rr}:L{rr}")
    dash.get_range("I20").formulas=[["=IFERROR(INDEX('18_VALIDACOES'!$A$5:$A$100,MATCH(\"READY\",'18_VALIDACOES'!$R$5:$R$100,0)),IFERROR(INDEX('18_VALIDACOES'!$A$5:$A$100,MATCH(\"PENDING\",'18_VALIDACOES'!$R$5:$R$100,0)),\"—\"))"]]
    dash.get_range("I21").formulas=[["=COUNTA('17_DECISOES'!$A$5:$A$300)"]]
    dash.get_range("I22").formulas=[["=COUNTA('19_SNAPSHOTS'!$A$5:$A$200)"]]
    dash.get_range("I23").formulas=[["=IF(I20=\"—\",\"—\",IFERROR(INDEX('18_VALIDACOES'!$R$5:$R$100,MATCH(I20,'18_VALIDACOES'!$A$5:$A$100,0)),\"—\"))"]]
    body(dash,"H20:L23")

    dash.get_range("H31:L31").values=[["Stage","Name","Expected result","Active items","Status"]]; hdr(dash,"H31:L31")
    dash.get_range("H32:J46").values=STAGES
    for r in range(32,47):
        n=r-32
        dash.get_range(f"K{r}").formulas=[[f'=COUNTIF(\'01_CADA\'!$B$5:$B$500,\"{n:02d}*\")-COUNTIFS(\'01_CADA\'!$B$5:$B$500,\"{n:02d}*\",\'01_CADA\'!$H$5:$H$500,\"DONE\")']]
        dash.get_range(f"L{r}").formulas=[[f'=IF(COUNTIF(\'01_CADA\'!$B$5:$B$500,\"{n:02d}*\")=0,\"NOT STARTED\",IF(K{r}=0,\"COMPLETED\",\"IN PROGRESS\"))']]
    body(dash,"H32:L46"); widths(dash,{"A":18,"B":24,"C":3,"D":16,"E":16,"F":16,"G":3,"H":22,"I":26,"J":44,"K":12,"L":18})
    dash.freeze_panes.freeze_rows(2)

    # Put dashboard first in final order when supported by generation environment.
    output.parent.mkdir(parents=True,exist_ok=True)
    SpreadsheetFile.export_xlsx(wb).save(str(output))
    return output

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",required=True)
    ap.add_argument("--project-name",required=True)
    ap.add_argument("--problem",default="")
    ap.add_argument("--article-type",default="undecided")
    ap.add_argument("--target-journal",default="")
    ap.add_argument("--journal-mode",default="JOURNAL_NEUTRAL")
    ap.add_argument("--journal-profile-status",default="TO_DEFINE")
    ap.add_argument("--pm-provider",default="NONE")
    a=ap.parse_args()
    path=build(Path(a.output),a.project_name,a.problem,a.article_type,(a.pm_provider or "NONE").upper(),a.target_journal,a.journal_mode,a.journal_profile_status)
    print(path)

if __name__=="__main__":
    main()
