#!/usr/bin/env python3
"""Auditable AI-use disclosure based on the canonical log and journal policy."""
import argparse,csv,hashlib,json,sys
from pathlib import Path
from urllib.parse import urlparse
MGMT="00_Gestao_e_Continuidade"
AI=f"{MGMT}/14_AI_Use_Log.csv"
PROFILE="06_Submissao/Regras_da_Revista/JOURNAL_PROFILE.json"
DRAFT="06_Submissao/Regras_da_Revista/AI_DISCLOSURE_DRAFT.md"
FINAL="06_Submissao/Regras_da_Revista/AI_DISCLOSURE_FINAL.md"
AUDIT=f"{MGMT}/AI_DISCLOSURE_AUDIT.json"
CATS=("ADMIN_SUPPORT","LITERATURE_SEARCH","SCREENING","EVIDENCE_EXTRACTION","DATA_ANALYSIS","DRAFTING_EDITING","FIGURES","OTHER")
EXTRA=("Disclosure_category","Human_review_evidence","Confidentiality_review")
def clean(x): return " ".join(str(x or "").split())
def checksum(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fingerprint(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def source(x):
 s=clean(x); p=urlparse(s)
 return len(s)>=14 and ((p.scheme=="https" and bool(p.netloc)) or s.startswith(("message:","document:","journal:")))
def substantive(x): return len(clean(x))>=18 and len(clean(x).split())>=3
def load(root):
 log=root/AI; profile=root/PROFILE
 if not log.is_file() or not profile.is_file(): raise ValueError("AI log or journal profile is missing")
 with log.open(encoding="utf-8-sig",newline="") as f:
  reader=csv.DictReader(f); cols=reader.fieldnames or []; uses=list(reader)
 if any(None in x for x in uses): raise ValueError("Malformed AI-use log")
 obj=json.loads(profile.read_text(encoding="utf-8"))
 if not isinstance(obj,dict): raise ValueError("Invalid journal profile")
 return log,cols,uses,obj
def assess(root):
 root=Path(root).resolve()
 log,columns,rows,profile=load(root)
 errors=[]; warnings=[]; uses=[]; seen=set()
 if rows:
  for name in EXTRA:
   if name not in columns: errors.append("Missing AI-use column "+name)
 for n,row in enumerate(rows,2):
  id=clean(row.get("AI_Use_ID"))
  cat=clean(row.get("Disclosure_category")).upper()
  tool=clean(row.get("Platform_or_tool"))
  purpose=clean(row.get("Purpose"))
  material=clean(row.get("Materiality")).upper()
  disposition=clean(row.get("Accepted_modified_or_rejected")).upper()
  if not id or id in seen: errors.append(f"Row {n}: duplicate/missing AI_Use_ID")
  seen.add(id)
  if cat not in CATS: errors.append(f"{id}: category not classified")
  if not tool or not substantive(purpose): errors.append(f"{id}: tool/purpose incomplete")
  if material not in ("SUBSTANTIVE","ADMINISTRATIVE","ASSISTIVE","NOT_APPLICABLE"):
   errors.append(f"{id}: materiality not classified")
  if disposition not in ("ACCEPTED","MODIFIED","REJECTED"):
   errors.append(f"{id}: final human decision not recorded")
  if material=="SUBSTANTIVE":
   if not substantive(row.get("Human_review_method")) or not source(row.get("Human_review_evidence")):
    errors.append(f"{id}: substantive use lacks review evidence")
  if clean(row.get("Confidentiality_review")).upper()!="CLEARED":
   errors.append(f"{id}: confidentiality review pending")
  if clean(row.get("Disclosure_required")).upper()=="NO":
   warnings.append(f"{id}: NO in the log does not override editorial rules")
  model=clean(row.get("Model_or_version")) or "versão não informada"
  uses.append({"id":id,"category":cat,"tool":tool,"model":model,"purpose":purpose,
               "review":clean(row.get("Human_review_method")),"decision":disposition})
 policy=profile.get("ai_disclosure_policy") or {}
 if policy.get("require_model_version") is True and any(u["model"]=="versão não informada" for u in uses):
  errors.append("journal requires exact model/version identification")
 att=profile.get("ai_disclosure_attestation") or {}
 if not (profile.get("status")=="VERIFIED" and
         profile.get("official_rules_verified") is True and
         policy.get("status")=="VERIFIED"):
  errors.append("official journal AI policy is not verified")
 if not clean(profile.get("journal_name")): errors.append("journal not defined")
 if not source(policy.get("source")): errors.append("journal AI policy source missing")
 if not clean(policy.get("verified_at")): errors.append("journal policy date missing")
 if policy.get("statement_location") not in (
  "METHODS","ACKNOWLEDGMENTS","DECLARATIONS","COVER_LETTER",
  "MANUSCRIPT_AND_COVER_LETTER","OTHER_OFFICIAL"):
  errors.append("journal disclosure placement not verified")
 rules=policy.get("category_rules") or {}
 for cat in {u["category"] for u in uses if u["category"] in CATS}:
  if rules.get(cat)!="ALLOWED":
   errors.append(f"{cat}: journal permission missing, prohibited or pending editor review")
 att=profile.get("ai_disclosure_attestation") or {}
 if att.get("status")!="CONFIRMED": errors.append("AI log completeness not confirmed")
 if att.get("ai_log_sha256")!=checksum(log): errors.append("AI log changed since attestation")
 if not source(att.get("evidence_ref")): errors.append("AI log attestation source missing")
 if not clean(att.get("reviewed_by")) or not clean(att.get("reviewed_at")):
  errors.append("AI log attestation reviewer/date missing")
 if not rows and att.get("status")!="CONFIRMED":
  errors.append("empty log cannot establish absence of AI use")
 return {
  "schema_version":1,
  "status":"READY_FOR_PLACEMENT_REVIEW" if not errors else "NOT_READY",
  "errors":errors,"warnings":warnings,
  "journal":clean(profile.get("journal_name")),
  "location":clean(policy.get("statement_location")),
  "uses":uses,"count":len(rows),
  "ai_log_sha256":checksum(log),
  "policy_sha256":fingerprint([profile.get("status"),policy,profile.get("journal_name"),att]),
  "editorial_acceptance_guaranteed":False,
  "researcher_placement_verified":False
 }
def render(result):
 lines=["# Declaração editorial de IA — minuta",
        "","Revista: "+result["journal"],
        "Local previsto: "+(result["location"] or "A CONFIRMAR"),
        "Situação: "+result["status"],""]
 if result["uses"]:
  lines+=["## Declaração proposta","",
          "Ferramentas de IA foram utilizadas nas atividades registradas a seguir.",
          "Os autores permanecem responsáveis pelas fontes, interpretações e pelo conteúdo final.",""]
  for event in result["uses"]:
   def safe(x): return clean(x).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
   lines.append("- "+safe(event["category"])+": "+safe(event["tool"])+" ("+
                safe(event["model"])+"); finalidade: "+safe(event["purpose"])+
                "; revisão: "+safe(event["review"] or "não descrita")+
                "; decisão: "+safe(event["decision"])+".")
 else:
  lines+=["Segundo a revisão documentada do pesquisador, nenhum uso foi declarado no registro.",
           "A conclusão depende da veracidade dessa manifestação humana.",""]
 if result["errors"]:
  lines+=["## Pendências",*("- "+x for x in result["errors"])]
 return "\n".join(lines)+"\n"
def render_compact(result):
 """Brief declaration for editorial use; never silently omit recorded activities.

 This is a text-length target, not a claim of a physically printed A4 page.
 """
 def safe(x):
  return clean(x).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
 if result["errors"]:
  # Draft can exist but must expose its non-final status.
  status="MINUTA COM PENDÊNCIAS"
 else:
  status="PRONTO PARA REVISÃO FINAL DO AUTOR"
 groups={}
 for u in result["uses"]:
  k=(u["category"],u["tool"],u["model"])
  groups.setdefault(k,[]).append(u["purpose"])
 lines=["# Transparência sobre uso de IA — versão breve","",
        "Periódico: "+safe(result["journal"] or "A CONFIRMAR"),
        "Local exigido: "+safe(result["location"] or "A CONFIRMAR"),
        "Situação: "+status,""]
 if not groups:
  lines.append("Segundo manifestação documentada do pesquisador, não houve uso de IA declarado no registro examinado. Um log vazio não comprova, por si, ausência de uso.")
 else:
  lines.append("Ferramentas e finalidades declaradas (conforme registros efetivos):")
  for (category,tool,model),purposes in sorted(groups.items()):
   unique=list(dict.fromkeys(clean(p) for p in purposes))
   category_label={
   "ADMIN_SUPPORT":"apoio administrativo","LITERATURE_SEARCH":"apoio à busca bibliográfica",
   "SCREENING":"apoio à triagem","EVIDENCE_EXTRACTION":"organização de evidências",
   "DATA_ANALYSIS":"apoio à análise de dados","DRAFTING_EDITING":"apoio à redação/edição",
   "FIGURES":"apoio à preparação de figuras","OTHER":"outra atividade descrita"
  }.get(category,category)
  lines.append("- "+safe(category_label)+": "+safe(tool)+" ("+safe(model)+") — "+safe("; ".join(unique))+".")
  lines.append("")
  lines.append("O pesquisador permanece responsável pela revisão dos resultados, precisão das fontes, interpretação e conteúdo final.")
 lines+=["","Texto sujeito às instruções vigentes do periódico e à verificação humana de posicionamento. A emissão não atesta aceite editorial."]
 if result["errors"]:
  lines.append("Pendências: "+str(len(result["errors"]))+"; consultar a auditoria completa antes de enviar.")
 output="\n".join(lines)+"\n"
 if len(output)>3000 or len(lines)>32:
  raise ValueError("Recorded AI usage exceeds one-page text budget; retain the full report and ask the researcher to revise a faithful brief statement.")
 return output

def verify_final(root):
 root=Path(root).resolve(); current=assess(root)
 errors=list(current["errors"])
 report=root/AUDIT; statement=root/FINAL
 if not report.is_file() or not statement.is_file():
  errors.append("final AI statement or audit missing")
 else:
  try:
   previous=json.loads(report.read_text(encoding="utf-8"))
   if previous.get("status")!="READY_FOR_PLACEMENT_REVIEW":
    errors.append("disclosure not ready when issued")
   for k in ("ai_log_sha256","policy_sha256","count"):
    if previous.get(k)!=current.get(k): errors.append(k+" changed after disclosure")
   if previous.get("final_sha256")!=checksum(statement):
    errors.append("final AI statement changed after audit")
   if previous.get("compact_final_sha256"):
    compact_path=root/"06_Submissao/Regras_da_Revista/AI_DISCLOSURE_COMPACT_FINAL.md"
    if not compact_path.is_file() or previous["compact_final_sha256"]!=checksum(compact_path):
     errors.append("compact editorial AI statement changed since audit")
  except (ValueError,OSError):
   errors.append("final AI audit unreadable")
 return errors
def main(argv=None):
 p=argparse.ArgumentParser(description=__doc__)
 sub=p.add_subparsers(dest="cmd",required=True)
 for operation in ("audit","draft","final","compact","compact-final","verify-final"):
  sp=sub.add_parser(operation);sp.add_argument("project")
 args=p.parse_args(argv)
 try:
  root=Path(args.project).resolve()
  if args.cmd=="verify-final":
   problems=verify_final(root)
   print(json.dumps({"ready":not problems,"errors":problems},ensure_ascii=False))
   return 1 if problems else 0
  result=assess(root)
  if args.cmd=="audit":
   print(json.dumps(result,ensure_ascii=False,indent=2))
   return 1 if result["errors"] else 0
  if args.cmd in ("final","compact-final") and result["errors"]:
   print(json.dumps({"status":"BLOCKED","errors":result["errors"]},ensure_ascii=False))
   return 1
  compact=args.cmd in ("compact","compact-final")
  destination=root/(
   "06_Submissao/Regras_da_Revista/AI_DISCLOSURE_COMPACT_FINAL.md" if args.cmd=="compact-final" else
   "06_Submissao/Regras_da_Revista/AI_DISCLOSURE_COMPACT_DRAFT.md" if args.cmd=="compact" else
   FINAL if args.cmd=="final" else DRAFT)
  destination.parent.mkdir(parents=True,exist_ok=True)
  destination.write_text(render_compact(result) if compact else render(result),encoding="utf-8")
  if args.cmd in ("final","compact-final"):
   if args.cmd=="compact-final":
    # A brief statement never replaces the complete policy-bound full declaration.
    issues=verify_final(root)
    if issues:
     destination.unlink(missing_ok=True)
     raise ValueError("Full editorial AI disclosure needs verification before compact final: "+"; ".join(issues[:3]))
    old=json.loads((root/AUDIT).read_text(encoding="utf-8"))
    old["compact_final_sha256"]=checksum(destination)
    (root/AUDIT).write_text(json.dumps(old,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"file":str(destination)},ensure_ascii=False))
    return 0
   result["final_sha256"]=checksum(destination)
   path=root/AUDIT;path.parent.mkdir(parents=True,exist_ok=True)
   path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print(json.dumps({"status":result["status"],"file":str(destination)},ensure_ascii=False))
  return 0 if not result["errors"] else 2
 except (OSError,ValueError,json.JSONDecodeError,csv.Error) as exc:
  print("ERROR: "+str(exc),file=sys.stderr)
  return 1

if __name__=="__main__":
 raise SystemExit(main())
