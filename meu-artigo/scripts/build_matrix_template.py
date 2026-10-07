#!/usr/bin/env python3
"""Build the canonical Meu Artigo C.A.D.A. + traceability workbook.

Reference implementation for environments with artifact_tool available.
Other platforms should reproduce the same logical structure from
references/spreadsheet-template.md.

Usage:
  python build_matrix_template.py --output /path/MATRIZ_MESTRA_projeto.xlsx \
      --project-name "Projeto" --problem "Problema..." --article-type undecided
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
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
["00","Entrada & Workspace","Problema preservado; workspace e governança inicializados."],
["01","Auditoria de novidade","Literatura mais próxima avaliada; contribuição/pergunta refinada."],
["02","Método / desenho","Tipo de artigo/revisão definido e justificado."],
["03","Protocolo","Escopo, critérios, bases, famílias de busca e regras congelados."],
["04","Execução das buscas","Buscas executadas e registradas."],
["05","Validação de exports","Exports conferidos; rodadas inválidas isoladas."],
["06","Deduplicação","Corpus canônico e auditoria de duplicatas."],
["07","Screening","Decisões e justificativas registradas."],
["08","Full text","Acesso, versão e decisão de textos completos controlados."],
["09","Extração de evidências","Matriz de evidências preenchida."],
["10","Síntese","Categorias, convergências, contradições e limites integrados."],
["11","Diálogo com revista","Aderência e conversa do periódico registradas."],
["12","Manuscrito","Redação ancorada em evidências e proveniência."],
["13","Auditoria final","Método, contagens, claims, IA e referências reconciliados."],
["14","Submissão","Arquivos, checklist, protocolo e comprovante preservados."],
]

def title(sheet, text, subtitle, span):
    sheet.merge_cells(span)
    sheet.get_range(span.split(":")[0]).values=[[text]]
    sheet.get_range(span).format=TITLE
    a,b=span.split(":"); c1=a[0]; c2=b[0]
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

def build(output:Path, project_name:str, problem:str, article_type:str, pm_provider:str="NONE"):
    wb=Workbook.create()

    cfg=wb.worksheets.add("15_CONFIG")
    title(cfg,"CONFIGURAÇÕES E DICIONÁRIOS","Listas controladas, etapas e parâmetros.","A1:H1")
    cfg.get_range("A4:D4").values=[["Lista","Valor","Descrição","Ordem"]]; hdr(cfg,"A4:D4")
    lists={
      "CADA_STATUS":["CAPTURED","ASSIGNED","READY","IN_PROGRESS","WAITING","BLOCKED","DONE","CANCELLED","SUPERSEDED"],
      "PRIORIDADE":["BAIXA","MÉDIA","ALTA","CRÍTICA"],
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
    }
    rows=[]
    for ln,vals in lists.items():
        for i,v in enumerate(vals,1): rows.append([ln,v,"",i])
    cfg.get_range(f"A5:D{4+len(rows)}").values=rows; body(cfg,f"A5:D{4+len(rows)}")
    cfg.get_range("F4:H4").values=[["Etapa","Nome","Resultado esperado"]]; hdr(cfg,"F4:H4")
    cfg.get_range("F5:H19").values=STAGES; body(cfg,"F5:H19")
    widths(cfg,{"A":20,"B":24,"C":48,"D":10,"F":9,"G":24,"H":58}); cfg.freeze_panes.freeze_rows(4)

    proj=wb.worksheets.add("03_PROJETO")
    title(proj,"IDENTIDADE CIENTÍFICA DO PROJETO","Problema, pergunta, objetivo, contribuição, método e escopo.","A1:D1")
    proj.get_range("A4:D4").values=[["Campo","Valor","Status","Última atualização"]]; hdr(proj,"A4:D4")
    vals=[
      ["Título curto do projeto",project_name,"PLANNED",date.today()],
      ["Problema original",problem or "[INSERIR TEXTO ORIGINAL DO PESQUISADOR]","FROZEN",date.today()],
      ["Pergunta atual","[A REFINAR]","IN_PROGRESS",date.today()],
      ["Objetivo","[A REFINAR]","IN_PROGRESS",date.today()],
      ["Contribuição pretendida","[A VALIDAR NA AUDITORIA DE NOVIDADE]","IN_PROGRESS",date.today()],
      ["Desenho metodológico",article_type,"PLANNED",date.today()],
      ["Escopo e exclusões","[A DEFINIR]","PLANNED",date.today()],
      ["Revista-alvo","[NÃO DEFINIDA]","PLANNED",date.today()],
      ["Idiomas","Português; Inglês","PLANNED",date.today()],
      ["Período de busca","[A DEFINIR]","PLANNED",date.today()],
      ["Etapa atual","01 — Auditoria de novidade","IN_PROGRESS",date.today()],
      ["Modo de gestão","MATRIX_PLUS_EXTERNAL" if pm_provider!="NONE" else "MATRIX_ONLY","FROZEN",date.today()],
      ["Gerenciador externo",pm_provider,"NOT APPLICABLE" if pm_provider=="NONE" else "IN_PROGRESS",date.today()],
      ["Rastreabilidade habilitada","SIM","FROZEN",date.today()],
    ]
    proj.get_range("A5:D18").values=vals; body(proj,"A5:D18")
    proj.get_range("D5:D18").format.number_format="yyyy-mm-dd"
    proj.get_range("C5:C18").data_validation={"rule":{"type":"list","values":lists["STATUS_GERAL"]}}
    widths(proj,{"A":28,"B":70,"C":20,"D":18}); proj.freeze_panes.freeze_rows(4)

    cada=wb.worksheets.add("01_CADA")
    title(cada,"GESTÃO C.A.D.A.","Capturar → Atribuir → Definir prazo → Acompanhar.","A1:S1")
    ch=["CADA_ID","Etapa","Tarefa","Responsável","Próxima ação","Prazo","Tipo de prazo","Status","Prioridade","Dependências","Bloqueio","Evidência de avanço","Evidência de conclusão","Artefato relacionado","Última atualização","Trace_IDs","PM Provider","External Item ID","Observações"]
    cada.get_range("A4:S4").values=[ch]; hdr(cada,"A4:S4")
    seed=[
      ["CADA-0001","00 — Entrada & Workspace","Inicializar workspace de pesquisa","AGENT","Confirmar artefatos canônicos e iniciar auditoria de novidade",None,"TO_DEFINE","DONE","ALTA","","","Workspace criado","CONTINUIDADE + protocolo + matriz","00_Gestao_e_Continuidade",date.today(),"TRACE-0001",pm_provider,"",""],
      ["CADA-0002","01 — Auditoria de novidade","Executar auditoria inicial de novidade e terminologia","AGENT","Localizar literatura próxima e testar a contribuição proposta",None,"TO_DEFINE","READY","ALTA","CADA-0001","","","","01_Auditoria_de_Novidade",date.today(),"",pm_provider,"",""],
      ["CADA-0003","02–03 — Método / Protocolo","Definir e congelar desenho metodológico e protocolo v1","AGENT+RESEARCHER","Aguardar auditoria de novidade; depois propor método e protocolo v1",None,"DEPENDENCY","CAPTURED","ALTA","CADA-0002","CADA-0002","","","PROTOCOLO.md",date.today(),"",pm_provider,"",""],
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
    title(tl,"LINHA DO TEMPO E RASTREABILIDADE","Como chegamos até aqui: eventos materiais da construção científica.","A1:T1")
    th=["Trace_ID","Timestamp","Etapa","CADA_ID","Ator","Ferramenta / IA","Modelo / versão","Tipo de ação","Resumo da ação","Entrada / Fonte","Decisão / Saída","Justificativa","Artefato antes","Artefato depois","Método de verificação","Validação humana","IDs relacionados","Materialidade","Status","Observações"]
    tl.get_range("A4:T4").values=[th]; hdr(tl,"A4:T4")
    tl.get_range("A5:T5").values=[["TRACE-0001",datetime.now(),"00","CADA-0001","SCRIPT","build_matrix_template.py","","WORKSPACE_INITIALIZATION","Inicialização da matriz C.A.D.A. e rastreabilidade.","Entrada inicial","Estrutura canônica criada","Iniciar proveniência antes da pesquisa substantiva","","Matriz criada","Conferência dos artefatos","PENDING","CADA-0001","ADMINISTRATIVE","COMPLETE",""]]
    body(tl,"A5:T500"); tl.get_range("B5:B500").format.number_format="yyyy-mm-dd hh:mm"
    tl.get_range("E5:E500").data_validation={"rule":{"type":"list","values":lists["ATOR"]}}
    tl.get_range("R5:R500").data_validation={"rule":{"type":"list","values":lists["MATERIALIDADE_IA"]}}
    widths(tl,{"A":14,"B":20,"C":10,"D":14,"E":16,"F":22,"G":18,"H":24,"I":46,"J":34,"K":40,"L":40,"M":24,"N":24,"O":30,"P":24,"Q":28,"R":18,"S":16,"T":28})
    tl.freeze_panes.freeze_rows(4); tl.freeze_panes.freeze_columns(4)

    definitions=[
      ("04_EVIDENCIAS","MAPA DE EVIDÊNCIAS — VISÃO SINTÉTICA","Uma visão de alto nível das evidências que sustentam a argumentação.",["Evidence_ID","Fonte / Citação","Conceito / Categoria","Achado / contribuição","Papel","Força / relevância","Claim_IDs","Locator / trecho","Status","Observações"],"A1:J1",{"A":14,"B":38,"C":28,"D":48,"E":18,"F":18,"G":18,"H":34,"I":16,"J":30}),
      ("05_PROTOCOLO","PROTOCOLO DO ESTUDO","Decisões metodológicas versionadas e justificadas.",["Item","Decisão","Justificativa","Status","Versão","Atualizado em","Trace_ID"],"A1:G1",{"A":28,"B":44,"C":54,"D":16,"E":10,"F":16,"G":16}),
      ("06_BUSCAS","LOG DE BUSCAS BIBLIOGRÁFICAS","Cada string executada deve permanecer versionada e rastreável.",["Search_ID","Data","Base / Fonte","Blocos conceituais","String literal","Filtros","Encontrados","Exportados","Arquivo / URL","Status","Iteração","Trace_ID","Validação","Observações"],"A1:N1",{"A":14,"B":13,"C":20,"D":38,"E":64,"F":38,"G":12,"H":12,"I":34,"J":16,"K":10,"L":16,"M":16,"N":32}),
      ("07_SCREENING","SCREENING","Decisões de inclusão/exclusão preservadas com justificativa e proveniência.",["Record_ID","Fonte","Search_ID","Título","Autores","Ano","DOI / ID","Resumo","Tipo","Idioma","Pass1","Motivo Pass1","Pass2","Motivo Pass2","Duplicata","Canonical_ID","Trace_ID","Observações"],"A1:R1",{"A":14,"B":16,"C":14,"D":48,"E":30,"F":9,"G":24,"H":60,"I":16,"J":12,"K":16,"L":30,"M":22,"N":30,"O":22,"P":16,"Q":16,"R":26}),
      ("08_FULL_TEXT","CONTROLE DE FULL TEXT","Acesso, versão, decisão e vínculo com a matriz de evidências.",["Record_ID","Prioridade","Status full text","Versão acessada","Fonte de acesso","Data de acesso","Decisão","Motivo exclusão","Evidence_ID","Arquivo / URL","Observações"],"A1:K1",{"A":14,"B":12,"C":18,"D":18,"E":28,"F":14,"G":14,"H":32,"I":14,"J":38,"K":30}),
      ("09_MATRIZ_EVID","MATRIZ DE EVIDÊNCIAS — DETALHADA","Extração estruturada para síntese horizontal e redação ancorada em fontes.",["Evidence_ID","Citação","DOI / ID","Conceito","Definição / claim","Problema / tensão","Mecanismo / achado","Desenho / tipo de fonte","Amostra / dados","Contexto","Processo / etapa","Atores / papéis","Ação / decisão","Evidência observável","Condições de contorno","Limitações","Transferibilidade","Papel / força","Locator","Rótulo epistêmico","Observações"],"A1:U1",{"A":14,"B":36,"C":24,"D":26,"E":42,"F":36,"G":42,"H":24,"I":28,"J":24,"K":22,"L":22,"M":24,"N":34,"O":34,"P":30,"Q":34,"R":20,"S":34,"T":18,"U":28}),
      ("10_SINTESE","SÍNTESE ENTRE FONTES","Convergências, contradições, limites e inferências explicitamente rastreadas.",["Synthesis_ID","Tema / Categoria","Evidence_IDs","Padrão entre fontes","Contradições","Condições de contorno","Inferência","Status epistêmico","Decisão","Claim_IDs","Trace_ID"],"A1:K1",{"A":14,"B":28,"C":28,"D":46,"E":36,"F":36,"G":44,"H":18,"I":30,"J":24,"K":16}),
      ("11_CLAIMS","CLAIMS LEDGER — MANUSCRITO ↔ EVIDÊNCIA","Cada afirmação relevante deve apontar para sua sustentação e proveniência.",["Claim_ID","Seção do manuscrito","Claim / afirmação","Tipo","Evidence_IDs","Locators","Trace_IDs","Força","Verificação","Status de redação","Observações"],"A1:K1",{"A":14,"B":24,"C":56,"D":20,"E":24,"F":34,"G":24,"H":14,"I":26,"J":18,"K":28}),
      ("12_USO_IA","REGISTRO DE USO DE IA","Transparência: onde a IA atuou, para quê e como houve validação humana.",["AI_Use_ID","Data","Etapa","CADA_ID","Trace_ID","Plataforma / ferramenta","Modelo / versão","Finalidade","Categoria de entrada","Categoria de saída","Materialidade","Método de revisão humana","Decisão humana","Aceito / modificado / rejeitado","Artefatos relacionados","Disclosure necessário","Texto / nota de disclosure","Observações"],"A1:R1",{"A":14,"B":13,"C":12,"D":14,"E":14,"F":24,"G":18,"H":36,"I":24,"J":24,"K":18,"L":40,"M":28,"N":22,"O":34,"P":18,"Q":48,"R":28}),
      ("13_SUBMISSAO","CHECKLIST DE SUBMISSÃO","Fechamento: requisitos, arquivos, prazos, comprovantes e rastreabilidade.",["Item","Requisito","Fonte do requisito","Status","Prazo","Evidência / arquivo","Trace_ID","Observações"],"A1:H1",{"A":24,"B":44,"C":30,"D":16,"E":14,"F":38,"G":16,"H":30}),
      ("14_PM_SYNC","SINCRONIZAÇÃO COM GERENCIADOR EXTERNO","Opcional: ClickUp, Jira, Trello ou equivalente. A planilha continua canônica.",["CADA_ID","Provider","Workspace / site","Container ID","External item ID","External URL","Status externo","Responsável externo","Prazo externo","Status canônico","Responsável canônico","Prazo canônico","Último push","Último pull","Sync status","Conflito","Observações"],"A1:Q1",{"A":14,"B":14,"C":24,"D":18,"E":18,"F":38,"G":18,"H":20,"I":14,"J":18,"K":20,"L":14,"M":20,"N":20,"O":16,"P":30,"Q":30}),
    ]
    for name,ttl,subt,heads,span,wmap in definitions:
        sh=wb.worksheets.add(name); title(sh,ttl,subt,span)
        end=chr(64+len(heads)) if len(heads)<=26 else "Z"
        sh.get_range(f"A4:{end}4").values=[heads]; hdr(sh,f"A4:{end}4")
        body(sh,f"A5:{end}500"); widths(sh,wmap); sh.freeze_panes.freeze_rows(4)

    wb.worksheets.get_item("05_PROTOCOLO").get_range("A5:G11").values=[
      ["Tipo de artigo/revisão","[A DEFINIR]","Depende da finalidade e da auditoria de novidade","PLANNED","v0",date.today(),""],
      ["Escopo","[A DEFINIR]","","PLANNED","v0",date.today(),""],
      ["Critérios de inclusão","[A DEFINIR]","","PLANNED","v0",date.today(),""],
      ["Critérios de exclusão","[A DEFINIR]","","PLANNED","v0",date.today(),""],
      ["Bases e papéis","[A DEFINIR]","","PLANNED","v0",date.today(),""],
      ["Regra de full text","[A DEFINIR]","","PLANNED","v0",date.today(),""],
      ["Regra de síntese/parada","[A DEFINIR]","","PLANNED","v0",date.today(),""],
    ]
    wb.worksheets.get_item("07_SCREENING").get_range("K5:K1000").data_validation={"rule":{"type":"list","values":lists["PASS1"]}}
    wb.worksheets.get_item("07_SCREENING").get_range("M5:M1000").data_validation={"rule":{"type":"list","values":lists["PASS2"]}}
    wb.worksheets.get_item("09_MATRIZ_EVID").get_range("T5:T500").data_validation={"rule":{"type":"list","values":lists["EPISTEMICO"]}}
    ai=wb.worksheets.get_item("12_USO_IA")
    ai.get_range("K5:K500").data_validation={"rule":{"type":"list","values":lists["MATERIALIDADE_IA"]}}
    ai.get_range("N5:N500").data_validation={"rule":{"type":"list","values":lists["DECISAO_IA"]}}

    dash=wb.worksheets.add("00_PAINEL")
    title(dash,"MEU ARTIGO — PAINEL DE GOVERNANÇA CIENTÍFICA","Onde estamos? O que falta? Como chegamos aqui? Onde a IA participou?","A1:L1")
    dash.get_range("A4:B4").values=[["Projeto","Valor"]]; hdr(dash,"A4:B4")
    dash.get_range("A5:A9").values=[["Título"],["Etapa atual"],["Modo de gestão"],["Gerenciador externo"],["Última atualização"]]
    dash.get_range("A5:A9").format=LABEL
    dash.get_range("B5").formulas=[["=IFERROR(INDEX('03_PROJETO'!$B$5:$B$30,MATCH(\"Título curto do projeto\",'03_PROJETO'!$A$5:$A$30,0)),\"[DEFINIR]\")"]]
    dash.get_range("B6").formulas=[["=IFERROR(INDEX('03_PROJETO'!$B$5:$B$30,MATCH(\"Etapa atual\",'03_PROJETO'!$A$5:$A$30,0)),\"—\")"]]
    dash.get_range("B7").formulas=[["=IFERROR(INDEX('03_PROJETO'!$B$5:$B$30,MATCH(\"Modo de gestão\",'03_PROJETO'!$A$5:$A$30,0)),\"MATRIX_ONLY\")"]]
    dash.get_range("B8").formulas=[["=IFERROR(INDEX('03_PROJETO'!$B$5:$B$30,MATCH(\"Gerenciador externo\",'03_PROJETO'!$A$5:$A$30,0)),\"NONE\")"]]
    dash.get_range("B9").formulas=[["=TODAY()"]]; dash.get_range("B9").format.number_format="yyyy-mm-dd"; body(dash,"A5:B9")

    cards=[
      ("D4:E4","D5:E6","Avanço C.A.D.A.","=IFERROR(COUNTIF('01_CADA'!$H$5:$H$500,\"DONE\")/COUNTA('01_CADA'!$A$5:$A$500),0)","0%"),
      ("F4:G4","F5:G6","Itens ativos","=COUNTIF('01_CADA'!$H$5:$H$500,\"READY\")+COUNTIF('01_CADA'!$H$5:$H$500,\"IN_PROGRESS\")+COUNTIF('01_CADA'!$H$5:$H$500,\"WAITING\")+COUNTIF('01_CADA'!$H$5:$H$500,\"BLOCKED\")","0"),
      ("H4:I4","H5:I6","Bloqueados","=COUNTIF('01_CADA'!$H$5:$H$500,\"BLOCKED\")","0"),
      ("J4:K4","J5:K6","Vencidos","=COUNTIFS('01_CADA'!$F$5:$F$500,\"<\"&TODAY(),'01_CADA'!$F$5:$F$500,\">0\",'01_CADA'!$H$5:$H$500,\"<>DONE\",'01_CADA'!$H$5:$H$500,\"<>CANCELLED\",'01_CADA'!$H$5:$H$500,\"<>SUPERSEDED\")","0"),
    ]
    for lr,vr,label,formula,nf in cards:
        dash.merge_cells(lr); dash.merge_cells(vr)
        dash.get_range(lr.split(":")[0]).values=[[label]]; dash.get_range(lr).format=KPI_LABEL
        dash.get_range(vr.split(":")[0]).formulas=[[formula]]; dash.get_range(vr).format=KPI_VALUE; dash.get_range(vr).format.number_format=nf

    dash.merge_cells("A12:F12"); dash.get_range("A12").values=[["PRÓXIMA AÇÃO"]]; dash.get_range("A12:F12").format=SECTION
    dash.get_range("A13:A16").values=[["CADA_ID"],["Ação"],["Responsável"],["Prazo"]]; dash.get_range("A13:A16").format=LABEL
    for r in range(13,17): dash.merge_cells(f"B{r}:F{r}")
    dash.get_range("B13").formulas=[["=IFERROR(INDEX('01_CADA'!$A$5:$A$500,MATCH(\"IN_PROGRESS\",'01_CADA'!$H$5:$H$500,0)),IFERROR(INDEX('01_CADA'!$A$5:$A$500,MATCH(\"READY\",'01_CADA'!$H$5:$H$500,0)),\"—\"))"]]
    dash.get_range("B14").formulas=[["=IFERROR(INDEX('01_CADA'!$E$5:$E$500,MATCH(B13,'01_CADA'!$A$5:$A$500,0)),\"—\")"]]
    dash.get_range("B15").formulas=[["=IFERROR(INDEX('01_CADA'!$D$5:$D$500,MATCH(B13,'01_CADA'!$A$5:$A$500,0)),\"—\")"]]
    dash.get_range("B16").formulas=[["=IFERROR(INDEX('01_CADA'!$F$5:$F$500,MATCH(B13,'01_CADA'!$A$5:$A$500,0)),\"—\")"]]
    dash.get_range("B16").format.number_format="yyyy-mm-dd"; body(dash,"A13:F16")

    dash.merge_cells("H12:L12"); dash.get_range("H12").values=[["RASTREABILIDADE & IA"]]; dash.get_range("H12:L12").format=SECTION
    dash.get_range("H13:H16").values=[["Rastreabilidade de DONE"],["TRACE events"],["IA substantiva validada"],["Claims verificados"]]; dash.get_range("H13:H16").format=LABEL
    for r in range(13,17): dash.merge_cells(f"I{r}:L{r}")
    dash.get_range("I13").formulas=[["=IFERROR(COUNTIFS('01_CADA'!$H$5:$H$500,\"DONE\",'01_CADA'!$M$5:$M$500,\"<>\")/COUNTIF('01_CADA'!$H$5:$H$500,\"DONE\"),0)"]]; dash.get_range("I13").format.number_format="0%"
    dash.get_range("I14").formulas=[["=COUNTA('02_LINHA_TEMPO'!$A$5:$A$500)"]]
    dash.get_range("I15").formulas=[["=COUNTIFS('12_USO_IA'!$K$5:$K$500,\"SUBSTANTIVE\",'12_USO_IA'!$N$5:$N$500,\"<>PENDING\")&\"/\"&COUNTIF('12_USO_IA'!$K$5:$K$500,\"SUBSTANTIVE\")"]]
    dash.get_range("I16").formulas=[["=COUNTIF('11_CLAIMS'!$J$5:$J$500,\"VERIFIED\")&\"/\"&COUNTA('11_CLAIMS'!$A$5:$A$500)"]]; body(dash,"H13:L16")

    dash.get_range("A19:B19").values=[["Status C.A.D.A.","Quantidade"]]; hdr(dash,"A19:B19")
    st=["CAPTURED","ASSIGNED","READY","IN_PROGRESS","WAITING","BLOCKED","DONE","CANCELLED","SUPERSEDED"]
    dash.get_range("A20:A28").values=[[x] for x in st]
    dash.get_range("B20:B28").formulas=[[f'=COUNTIF(\'01_CADA\'!$H$5:$H$500,A{r})'] for r in range(20,29)]
    body(dash,"A20:B28")
    try:
        chart=dash.charts.add("bar",dash.get_range("A19:B28")); chart.title_text="Situação dos itens C.A.D.A."; chart.has_legend=False; chart.set_position("A31","F46")
    except Exception:
        pass

    dash.get_range("H31:L31").values=[["Etapa","Nome","Resultado esperado","Itens ativos","Situação"]]; hdr(dash,"H31:L31")
    dash.get_range("H32:J46").values=STAGES
    for r in range(32,47):
        n=r-32
        dash.get_range(f"K{r}").formulas=[[f'=COUNTIF(\'01_CADA\'!$B$5:$B$500,\"{n:02d}*\")-COUNTIFS(\'01_CADA\'!$B$5:$B$500,\"{n:02d}*\",\'01_CADA\'!$H$5:$H$500,\"DONE\")']]
        dash.get_range(f"L{r}").formulas=[[f'=IF(COUNTIF(\'01_CADA\'!$B$5:$B$500,\"{n:02d}*\")=0,\"NÃO INICIADA\",IF(K{r}=0,\"CONCLUÍDA\",\"EM ANDAMENTO\"))']]
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
    ap.add_argument("--pm-provider",default="NONE")
    a=ap.parse_args()
    path=build(Path(a.output),a.project_name,a.problem,a.article_type,(a.pm_provider or "NONE").upper())
    print(path)

if __name__=="__main__":
    main()
