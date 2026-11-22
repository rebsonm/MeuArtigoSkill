#!/usr/bin/env python3
"""Replace erroneous machine translations with conservative English editorial redrafts.

This is not a translation of protected publications or a scientific appraisal.
Historical Portuguese versions remain available at the immutable public ref.
"""
from __future__ import annotations
import hashlib,json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LIB=ROOT/"knowledge/methodology"
ORIGINAL="9cf5b9ee91c0c0ade6c6d66316b26bde67cbe413"
PENDING="MACHINE_TRANSLATED_REVIEW_PENDING"
DONE="ENGLISH_EDITORIAL_REWRITE_METADATA_GROUNDED_NOT_SOURCE_REVIEW"
LEGACY="REVISÃO_CIENTÍFICA_INDEPENDENTE_PENDENTE"
METHODS=[
("Difference-in-differences",r"difference.in.difference|dif.in.dif|diferen.as em diferen.as|santanna|krueger",
 "Specify treated and comparison units, timing, estimand, and assumptions about counterfactual trends.",
 "Check anticipation, spillovers, changing composition, and rival time trends."),
("Impact evaluation",r"impact eval|avalia..o de impacto|causal|contrafactual|counterfactual",
 "State the intervention, comparison logic, estimand, and identifying assumptions.",
 "Association or temporal coincidence cannot establish a causal effect."),
("Regression discontinuity",r"regression discontinuity|\brdd\b",
 "Explain the running variable, cutoff, manipulation checks, and local estimand.",
 "A local estimate need not generalize to every unit or threshold."),
("Surveys and measurement",r"survey|questionnaire|question.rio|escala|likert",
 "Document the population, sampling, item wording, measurement validity, and nonresponse.",
 "Questionnaire responses alone do not prove population representativeness."),
("Sampling and saturation",r"sampling|amostragem|satura..o|sample size",
 "Explain sample selection, heterogeneity, coverage, and stopping rationale.",
 "Do not treat a predetermined interview count as proof of saturation."),
("Qualitative interviewing",r"interview|entrevista",
 "Record recruitment, interview protocol, consent, participant context, and analytic trail.",
 "Interview accounts are situated testimony rather than complete behavioral records."),
("Focus groups",r"focus group|grupo focal|grupos focais",
 "Justify group composition, moderation, interaction data, and confidentiality.",
 "Group discussion is not a set of independent interviews."),
("Ethnography and observation",r"ethnograph|etnograf|participant observation|observa..o participante|fieldwork",
 "Describe field access, positionality, observation protocols, and interpretation.",
 "The observer's presence and situated access can affect what is recorded."),
("Document analysis",r"document|documental|arquivo|archive",
 "Specify provenance, document selection, genre, missing records, and coding or interpretation.",
 "Official documents must not be equated automatically with lived or organizational practice."),
("Thematic analysis",r"thematic|tem.tic|coding|codifica|code agreement",
 "Align the role of codes and themes with the analytic tradition and research question.",
 "Coding agreement or frequency alone does not demonstrate interpretive validity."),
("Discourse and content analysis",r"discourse|discurso|content analysis|conte.do",
 "Set units of analysis, categories, context, counterexamples, and interpretation rules.",
 "A word or category count is not a causal inference or interpretation by itself."),
("Grounded theory",r"grounded theory|teoria fundamentada",
 "Trace constant comparison, theoretical sampling, memoing, and category development.",
 "Coding software or interview collection alone does not establish grounded theory."),
("Comparative and case-study design",r"case stud|estudo de caso|comparad|comparativ|yin|eisenhardt",
 "Define cases, units, case-selection logic, and rival explanations.",
 "Analytical transfer differs from statistical generalization."),
("Action research",r"action research|pesquisa.a..o|pesquisa a..o",
 "Describe collaboration, intervention cycles, reflection, and documented evaluation.",
 "A successful improvement is not automatically a generalizable scientific finding."),
("Design science research",r"design science|dsrm|artefato|hevner|peffers",
 "Separate artifact design, demonstration, evaluation, and iteration.",
 "Demonstration of use does not by itself establish effectiveness."),
("Reviews and synthesis",r"review|revis.o|prisma|snyder|meta.analysis|scoping|literature|bibliografic",
 "Match the review type to the question; document retrieval, selection, appraisal, and synthesis.",
 "A PRISMA-style flowchart does not replace a defensible review design."),
("Bibliometrics and networks",r"bibliometr|citation|co.cita|network|rede social|redes",
 "Report database coverage, metadata cleanup, thresholds, network assumptions, and interpretation.",
 "Citation counts and network clusters do not establish theory truth or causality."),
("Spatial and ecological methods",r"spatial|espacial|geoprocess|ecologic|ecol.gic",
 "State geographic units, scale, dependence, aggregation, and spatial confounding.",
 "Ecological patterns need not hold at the individual level."),
("Statistical modeling",r"regression|regress.o|logistic|log.stica|fatorial|factor|cluster|correlation|correla|painel|panel|structural equation|equacoes|survival|sobreviv|instrumental|outlier|intera..o|correspondence",
 "Define outcome, predictors, assumptions, preprocessing, uncertainty, and robustness checks.",
 "Model fit or statistical significance alone does not establish a causal mechanism."),
("Computation and digital methods",r"machine learning|text mining|texto como dado|nlp|simula|monte carlo|sociologia digital|digital methods",
 "Document inputs, provenance, preprocessing, computation choices, and reproducibility.",
 "Predictions or simulations are not empirical validation of an explanatory mechanism."),
("AI-assisted research",r"\bai\b|llm|genai|intelig.ncia artificial|chatbot|prompt|artificial intelligence",
 "Record the AI's task, model version, prompts, researcher decisions, and verification steps.",
 "Fluent output, speed, or apparent human agreement does not validate scientific interpretation."),
("Research transparency and writing",r"transparent|transpar|reproduc|replic|publication|escrita cient|scientific writing|manuscript",
 "Explain reporting decisions, deviation logs, claim-to-source traceability, and writing boundaries.",
 "Fluent academic prose is not evidence of primary-source reading."),
("Institutional and policy analysis",r"institutional|instituciona|public polic|pol.ticas p.blicas|jurimet|political|pol.tica",
 "Identify institutional rules, actors, mechanisms, and credible alternative accounts.",
 "Written regulations do not demonstrate observed compliance or impact."),
("Epistemology and qualitative quality",r"epistemolog|feminist|paradigm|reflexiv|quality|qualidade|valid|etic|.tica",
 "State the epistemological position, researcher role, criteria of adequacy, and interpretation limits.",
 "Quality criteria must fit the research tradition rather than be applied mechanically."),
("Visual methods",r"image|imagem|fotograf|photo|visual",
 "Record image provenance, production context, consent, and analytic triangulation.",
 "A photograph is not a self-interpreting explanation of a social phenomenon."),
]
DEFAULT=("Research design and methods","Link the question, constructs, data sources, and inferential strategy.",
         "Limit claims to the evidence and alternatives the design can support.")
def n(s):
    s=unicodedata.normalize("NFKD",str(s or "")).casefold()
    return "".join(c for c in s if not unicodedata.combining(c))
def topic(row):
    text=n(" ".join([str(row.get("topic","")),str(row.get("title","")),row["path"]]+
                    [str(x) for x in row.get("keywords",[])]))
    for family,pattern,plan,limit in METHODS:
        if re.search(pattern,text):return family,plan,limit
    return DEFAULT
def safe(x):
    return re.sub(r"\s+"," ",str(x or "")).strip().replace("|"," / ").replace("<","&lt;").replace(">","&gt;")[:1200]
def hashstr(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()
def original(path):
    return "https://github.com/rebsonm/MeuArtigoSkill/blob/"+ORIGINAL+"/"+path
def source_card(row):
    family,plan,limit=topic(row)
    meta=row.get("public_work_metadata_screen") or {}
    authors=meta.get("authors") or meta.get("author") or ""
    if isinstance(authors,list):authors="; ".join(str(x) for x in authors)
    year=meta.get("year") or meta.get("publication_year") or ""
    doi=meta.get("doi") or meta.get("DOI") or ""
    lines=["UNREVIEWED_PROSPECTING_CARD — [P] bibliography for consultation, NOT evidence [L].","",
           "# Bibliographic lead — "+row["source_id"],"",
           "## Source identification",
           "- Original published title: "+safe(row["title"]),
           "- Record: "+row["source_id"],
           "- Methodological field: "+family]
    if authors:lines.append("- Authors as catalogued: "+safe(authors))
    if year and str(year) not in ("UNKNOWN","NOT_VERIFIED"):lines.append("- Year as catalogued: "+safe(year))
    if doi:lines.append("- DOI recorded in public catalogue: "+safe(doi))
    lines.extend([
      "- Source identity check: "+str(row["bibliography_match_status"]),
      "- Scope of source consultation: "+str(row["source_read_scope"]),
      "",
      "## Original methodological consultation questions [P]",
      "- "+plan,
      "- "+limit,
      "- What source pages, empirical setting, sampling and rival findings would be required to support a specific claim?",
      "",
      "## Evidence and copyright boundaries",
      "- Rights review status for the underlying work: "+str(row["rights_review"]),
      "- Exact public-source PDF recorded in this catalogue: "+str(bool(row["has_original_public_pdf"])).lower(),
      "- Identifying a work does not grant a right to reproduce it or establish the validity of its findings.",
      "- The source has NOT been independently scientifically reviewed for this card. [P] proposals and [I] interpretations are not primary source support [L].",
      "- No scientific gate is approved.",
      "",
      "## Provenance and editorial status",
      "This is a **new English editorial rewrite** based on public catalogue metadata, not a literal or certified translation of the source publication or of the previous card.",
      "The questions are independent guidance, not claims about what the source authors established.",
      "- Original earlier editorial record: "+original(row["path"]),
      "- English rewrite classification: "+DONE,
      ""])
    return "\n".join(lines)
def editorial_card(row):
    family,plan,limit=topic(row)
    slug=Path(row["path"]).stem
    lines=["# Methodological decision card — "+family+" — "+slug,"",
           "Card ID: "+slug,
           "Editorial status: DRAFT_NEEDS_INDEPENDENT_REVIEW",
           "Evidence grade: [I] bounded editorial perspective; [P] research prompts; NOT primary evidence [L].",
           "Independent scientific review: NOT APPROVED."]
    if row.get("source_registry_id"):lines.append("Related bibliographic record: "+str(row["source_registry_id"]))
    if row.get("source_doi"):lines.append("DOI lead for source verification: "+safe(row["source_doi"]))
    if str(row.get("source_url","")).startswith("https://"):
        lines.append("Source locator for independent verification: "+safe(row["source_url"]))
    lines+=["",
            "## Original topic and research use",
            "- Original catalogued topic label (preserved as metadata): "+safe(row["title"]),
            "## Original English methodological guidance [I]",
            plan,
            "",
            "## Limits and alternative interpretations [I]",
            limit,
            "Source-specific conclusions require consultation of the relevant original publication, edition and exact supporting passages.",
            "",
            "## Researcher prompts [P]",
            "- Which research question, theory, unit of analysis and data make this method defensible?",
            "- Which competing design or interpretation could explain the observations?",
            "- What contrary evidence or primary-source passage must be checked before asserting [L] support?",
            "- Which decisions, omissions and sensitivity checks should be reported?",
            "",
            "## Scientific governance and rights",
            "Editorial rights scope: "+str(row.get("rights_scope","ORIGINAL_EDITORIAL_TEXT_ONLY")),
            "Underlying publication rights: "+str(row.get("underlying_source_rights_status","NOT_ESTABLISHED_BY_CARD_CATALOG")),
            "The article/book/PDF is not reproduced or authorized for redistribution by this card.",
            "No source-specific result, independent review, or scientific gate is approved.",
            "Historic pending-review identifier (technical metadata only): "+LEGACY,
            "",
            "## Provenance",
            "This is newly written conservative English guidance based on the existing public catalogue topic, NOT a faithful line-by-line translation or a primary-source appraisal.",
            "Original Portuguese editorial notes and source-specific detail: "+original(row["path"]),
            "Editorial rewrite classification: "+DONE,
            ""]
    return "\n".join(lines)
def main():
    sc=LIB/"source_registry_catalog.json";ec=LIB/"catalog.json";lc=LIB/"intake/operational-validation.json"
    sources=json.loads(sc.read_text(encoding="utf-8"))
    editorials=json.loads(ec.read_text(encoding="utf-8"))
    ledger=json.loads(lc.read_text(encoding="utf-8"))
    by={x["path"]:x for x in ledger["cards"]}
    assert len(sources["documents"])==475 and len(editorials["documents"])==174 and len(by)==649
    done_s=done_e=0
    for row in sources["documents"]:
        if row.get("translation_fidelity_status")!=PENDING:continue
        content=source_card(row);path=row["path"]
        assert row["source_id"] in content and "[L]" in content and "[P]" in content
        assert len(content.encode("utf-8"))<14000
        (ROOT/path).write_text(content,encoding="utf-8")
        row["sha256"]=by[path]["sha256"]=hashstr(content)
        row["translation_fidelity_status"]=DONE;done_s+=1
    for row in editorials["documents"]:
        if row.get("translation_fidelity_status")!=PENDING:continue
        content=editorial_card(row);path=row["path"]
        assert "DRAFT_NEEDS_INDEPENDENT_REVIEW" in content
        assert len(content.encode("utf-8"))<14000
        (ROOT/path).write_text(content,encoding="utf-8")
        row["sha256"]=by[path]["sha256"]=hashstr(content)
        row["translation_fidelity_status"]=DONE;done_e+=1
    assert (done_s,done_e)==(472,110),(done_s,done_e)
    for path,data in [(sc,sources),(ec,editorials),(lc,ledger)]:
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    assert not any(x.get("translation_fidelity_status")==PENDING for x in sources["documents"]+editorials["documents"])
    doc=ROOT/"docs/ALL-MARKDOWN-LANGUAGE-STATUS.md"
    prior=doc.read_text(encoding="utf-8")
    msg=(
       "## Current English-language remediation — 22 November 2026\n\n"
       "**582 unreliable machine-translated Markdown cards have been replaced** by conservative English editorial redrafts: 472 bibliographic prospecting cards and 110 methodological decision cards.\n\n"
       "This is NOT a certification of literal translation fidelity. The redrafts use the existing public bibliographic metadata and method-specific decision prompts, without attributing unverified claims to source authors. Each card links to its immutable prior Portuguese editorial record so that valuable original detail remains accessible. The 649-entry ledger and all source-rights and scientific-review states are unchanged. The seven scientific gates remain unapproved and no restricted PDF is republished.\n\n"
       "Historical intake notes remain archival evidence in their original language; they were not silently rewritten. Original published titles and technical identifiers also retain their source language. This is an editorial quality repair, not a peer review of 582 underlying works.\n\n"
    )
    doc.write_text(prior.split("\n",1)[0]+"\n\n"+msg+prior.split("\n",1)[1],encoding="utf-8")
    result={"source_cards":done_s,"editorial_cards":done_e,"total":done_s+done_e,
            "registry":475,"catalogue":174,"ledger":649,"scientific_approvals":0,
            "rights_changed":False,"pdf_uploads":0,"translation_fidelity_certified":False,
            "classification":DONE}
    Path("/tmp/english-remediation-receipt.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result))
if __name__=="__main__":
    main()
