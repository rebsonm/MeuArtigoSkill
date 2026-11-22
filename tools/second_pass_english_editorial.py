#!/usr/bin/env python3
"""Final source-aware editorial quality pass, preserving original English cards."""
from __future__ import annotations
import hashlib,json,re,subprocess,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"knowledge/methodology"
ORIGINAL="9cf5b9ee91c0c0ade6c6d66316b26bde67cbe413"
NEW="ENGLISH_EDITORIAL_REWRITE_METADATA_GROUNDED_NOT_SOURCE_REVIEW"
RESTORED="RESTORED_PREEXISTING_ENGLISH_EDITORIAL_NOT_SCIENTIFIC_APPROVAL"
PT=re.compile(r"\b(?:não|pesquisa|revisão|análise|metodologia|científico|científica|fontes|dados|questão|limitações|avaliação|apenas|também|considerar|verificar|contribuição|entrevista|qualitativa|qualitativo|conclusão|evidência|proposta|quais|pesquisador|realizada|objetivo|perguntas|direitos|para|como|antes|uma|com|sem|quando|dessa|aquilo|ainda)\b",re.I)
# Each item is original independently written methodological caution, NOT an
# assertion that the linked article empirically demonstrated any finding.
OVERRIDES=[
("collaborative-autoethnography|al-fattal-singh","Comparative autoethnography and AI-assisted interpretation",
 "Compare analytic speed with situated interpretive depth and researcher reflexivity using distinct criteria.",
 "Two researchers' reflexive accounts do not establish population-level agreement or a randomized performance comparison."),
("reflexive-thematic|braun-clarke|kiger-varpio|dias-mishima|thematic-practice",
 "Reflexive thematic analysis",
 "Make epistemological position, researcher role, interpretive themes, analytic memos and reflexivity explicit.",
 "Intercoder agreement and counts are not automatic quality criteria for reflexive thematic analysis."),
("intercoder|content-analysis-reliability","Qualitative coding agreement and reliability",
 "Specify the analytic tradition and whether multiple coders, training, disagreement resolution and statistics are meaningful.",
 "Intercoder agreement cannot replace validity of categories or reflexive interpretation."),
("rijnsoever|sampling-saturation|thematic-saturation|sim-etal|campos-saidel",
 "Qualitative sampling and stopping decisions",
 "Justify the sample through heterogeneity, study purpose, analytic depth and explicit stopping rationale.",
 "Do not claim saturation solely from a convenient predetermined sample size."),
("focus-group|group-design","Focus groups",
 "Analyze group interaction and moderation, not merely independent answers from co-present participants.",
 "Power imbalances, social desirability and confidentiality may limit inference."),
("mixed-methods-integration|creswell-creswell","Mixed-methods inference",
 "Specify when quantitative and qualitative strands connect and how their integration changes the interpretation.",
 "Simply collecting two types of data is not a mixed-methods integration."),
("qualitative-metaanalysis","Qualitative evidence synthesis",
 "Specify the interpretive synthesis logic, primary-study contexts and conceptual translation across findings.",
 "Qualitative meta-synthesis should not be treated as numerical effect-size meta-analysis."),
("prisma-s-2021","Search-strategy reporting",
 "Record databases, search dates, exact strings, field tags, limits and reproducible retrieval decisions.",
 "Search reporting standards do not by themselves establish critical appraisal or synthesis validity."),
("prisma-scr-2018","Scoping-review reporting",
 "Specify the mapping purpose, inclusion logic, charting of evidence and relevant reporting decisions.",
 "Mapping a field is not necessarily a systematic review of intervention effectiveness."),
("prisma-p-2015","Systematic-review protocols",
 "Distinguish planned eligibility, selection, analysis and deviations before and after the study.",
 "A protocol is not proof that procedures were executed as planned."),
("prisma-2020|prisma-roses","Transparent review reporting",
 "Trace eligibility, screened records, exclusions and synthesis decisions against the appropriate checklist.",
 "A flowchart and checklist cannot compensate for omitted full-text assessment."),
("snyder-2019|elsbach-van-knippenberg|reviews.md|literature-review-writing|salvador-1986",
 "Literature-review strategy",
 "Distinguish systematic, semi-systematic, narrative and integrative objectives, retrieval and synthesis requirements.",
 "A database query or PRISMA figure alone cannot establish the chosen review type."),
("alvesson-sandberg","Problematisation and research questions",
 "Identify assumptions taken for granted by a literature and formulate a meaningful theoretical tension.",
 "A simple claim that few papers exist is not necessarily a defensible theoretical gap."),
("research-practice-protocol|saunders-lewis|design.md","Vertical research-design coherence",
 "Link problem, question, constructs, philosophy, observations, analysis and bounded contribution.",
 "A chosen method or research-onion label does not justify the inference without appropriate data."),
("manuscript-argument|scientific-writing|writing-productivity","Scientific writing and claim discipline",
 "Give each section a clear argumentative role and trace every substantive claim to its actual evidence.",
 "Writing fluency or outline completeness is not a methodological or empirical validation."),
("eisenhardt-1989","Building theory from cases",
 "Justify purposive case sampling, within-case evidence, cross-case comparisons and rival mechanisms.",
 "Multiple cases alone do not yield theory without defensible theoretical iteration."),
("hevner-2004|peffers-2008|design-science","Design science research",
 "Separate problem relevance, artifact construction, demonstration, evaluation and iterative refinement.",
 "An artifact demonstration cannot be relabeled independent effectiveness evaluation."),
("sampaio-sabbatini-limongi|responsible-ai","Responsible AI research assistance",
 "Record AI tasks, prompt/model versions, human decisions, claim provenance and disclosure.",
 "Generated output is not primary scientific evidence without independent examination."),
("ibrahim-voyer","Technological reflexivity",
 "Record how LLM framing, interface and researcher interpretations may shape qualitative reading.",
 "A conversational tool is not a neutral observer or epistemological substitute."),
("misra-et-al|jiang-et-al|castellanos-et-al",
 "Comparing human and LLM qualitative coding",
 "Specify unit of comparison, coding framework, adjudication and interpretation of observed agreement.",
 "Agreement proportions do not establish equivalent meaning, causal validity or universal quality."),
("nguyen-welch-2025-epistemic|messner-smith-richards",
 "Epistemic compatibility of GenAI and qualitative inquiry",
 "Examine how language-model outputs differ from situated meaning-making and researcher experience.",
 "Textual plausibility cannot stand in for contextual human understanding."),
("vikan-et-al|wise-gresalfi-spencer",
 "Human interpretation with local or assisted AI",
 "Distinguish technical deployment constraints from analytic judgement and researcher accountability.",
 "Offline inference does not automatically resolve interpretive bias or ethical limitations."),
("costa-et-al-2025-abductivai|nguyen-trung-2025-gaita",
 "Abductive and guided AI-assisted analysis",
 "Log surprising observations, proposed explanations, AI alternatives and human adjudication.",
 "Automatically suggested themes or hypotheses need corroboration and competing explanations."),
("dellafiore-et-al|paulus-lester-davis",
 "Claims about AI roles in qualitative research",
 "Separate expert perceptions, documented use, and experimentally demonstrated capabilities.",
 "Reported enthusiasm or task descriptions are not causal performance estimates."),
("jones-2025-genai-disclosure",
 "Transparent disclosure of GenAI use",
 "State each AI contribution, model/tool, human review, and effect on research outputs.",
 "Disclosure alone does not certify rigorous collection, analysis or source verification."),
("dahal-et-al","Representational and legitimacy risks in GenAI research",
 "Examine who is represented, whose interpretation is authorized, and which practices are affected.",
 "Procedural convenience should not displace reflexivity and research ethics."),
("jarrahi-2025-interviewing-ai",
 "AI-system behavior as a research object",
 "Specify whether prompts are probes of system responses rather than interviews with human participants.",
 "Model behavior cannot be interpreted as human subjective experience."),
("duarte-et-al|nguyen-welch-2025-engaged|friedman-owen",
 "Critical alternatives to automated qualitative interpretation",
 "Compare AI and non-AI research paths against epistemological commitments and participant obligations.",
 "Using GenAI is not inevitable and declining it is a legitimate methodological choice."),
("macgeorge-2025",
 "Futures research and generative AI",
 "Separate rapid scenario generation from contextual interpretation and stakeholder validation.",
 "A plausible generated future is not a forecast supported by empirical evidence."),
("kon-et-al","Small-sample AI summarization",
 "Disclose number and type of transcripts, sampling variation and adjudicated omissions.",
 "A very small clinical transcript sample cannot establish broadly generalizable validity."),
("davison-et-al","Secondary use and sharing of qualitative data",
 "State consent, purpose limitation, confidentiality and risks of model training on research records.",
 "Analytical access is not automatically consent for secondary exploitation or redistribution."),
("paulus-marone","Commercial claims about AI analysis",
 "Separate vendor performance promises from independent comparative evidence and actual analytic requirements.",
 "Marketing demonstrations cannot validate scientific quality."),
("eschrich-sterman","Counterexamples in AI-assisted interpretation",
 "Use generated interpretations as hypotheses to challenge against source passages and alternative readings.",
 "A confident model-generated interpretation is not a verified participant perspective."),
("de-paoli-2026","Philosophical debate about GenAI",
 "Distinguish a conceptual rejoinder to AI scepticism from empirical evaluation of tools.",
 "Philosophical argument and experimental validation answer different questions."),
("teixeira-tschopp-jobin","Status of a position paper on AI coding",
 "Identify the exact manuscript version and distinguish conference acceptance from proceedings publication.",
 "Do not attribute the evidentiary status of a published empirical study to an unpublished position paper."),
("barros-et-al","Mapping LLM uses in qualitative studies",
 "Separate counts of reported applications from measurements of their analytical validity.",
 "Publication frequency is not a performance metric."),
("santanna-2025|card-krueger|gertler-et-al",
 "Quasi-experimental impact identification",
 "Define comparison groups, treatment timing, identifying assumptions and robust counterfactual checks.",
 "A before/after comparison or study-label alone is not a causal design."),
("conceicao-et-al","Spatial ecological regression",
 "Inspect spatial dependence, unit aggregation, confounding and the ecological level of inference.",
 "Area-level coefficients are not individual-level treatment effects."),
("carlomagno-rocha","Content-category construction",
 "Define mutually intelligible category rules, empirical examples, ambiguity handling and coding decisions.",
 "Mechanical assignment does not substitute interpretive category validity."),
("siddiki-basurto-weible","Institutional grammar and compliance",
 "Distinguish encoded rules from actors' observed behavior and explain the coding grammar.",
 "Institutional rules cannot establish compliance without observational evidence."),
("source-review-0239|source-review-0240|source-review-0242",
 "Correspondence analysis",
 "Justify categorical data structure, weighting, dimensional interpretation and stability.",
 "A visual map of associations should not be interpreted as a causal model."),
("source-review-0401","Robust cluster analysis",
 "State clustering objective, outlier treatment, tuning parameters and robustness.",
 "Cluster membership is not an externally validated natural kind."),
("source-review-0410","Exploratory factor analysis",
 "Check dimensionality assumptions, sampling adequacy, loadings, rotations and interpretation.",
 "Factor labels are theoretically interpreted, not identified by software automatically."),
("source-review-0273|source-review-0274",
 "Spatial data methods",
 "Document geolocation, scale, spatial autocorrelation and uncertainty in map-based inference.",
 "Aggregated spatial relations are not individual causal evidence."),
("source-review-0205|source-review-0206|source-review-0337",
 "Visual evidence in social research",
 "Record image provenance, framing, consent and the role of visual interpretation.",
 "An image recommendation or duplicate bibliography is not an independent empirical study."),
("source-review-0181|source-review-0182|source-review-0184",
 "Transparency and reproducibility",
 "Specify what data, scripts, protocols and corrections are available for reproduction.",
 "Availability of files does not guarantee independent scientific replication."),
("source-checked-0008|source-checked-0009|source-checked-0010|source-checked-0012|source-checked-0013|source-checked-0015|source-review-0011",
 "Documentary methodology",
 "Differentiate document analysis, content interpretation and evidence of observed organizational behavior.",
 "Archival selection, document genre and missing records can bias conclusions."),
]
def hash_bytes(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()
def old_file(path):
    return subprocess.check_output(["git","show",ORIGINAL+":"+path]).decode("utf-8")
def portable_english(s):
    body="\n".join(line for line in s.splitlines()
                    if not re.search(r"^(?:[-*]\s*)?(?:Original published title|Source title|Título original|Referência bibliográfica):",line,re.I))
    tokens=PT.findall(body)
    return len(s)>=550 and len(tokens)<=4 and len(re.findall(r"[A-Za-z]{3,}",body))>=65
def main():
    cp=BASE/"catalog.json";lp=BASE/"intake/operational-validation.json"
    cat=json.loads(cp.read_text(encoding="utf-8"));ledger=json.loads(lp.read_text(encoding="utf-8"))
    lookup={x["path"]:x for x in ledger["cards"]}
    preserved=0
    enriched=0
    for row in cat["documents"]:
        if row.get("translation_fidelity_status")!="ENGLISH_EDITORIAL_REWRITE_METADATA_GROUNDED_NOT_SOURCE_REVIEW":
            continue
        path=row["path"]
        previous=old_file(path)
        file=ROOT/path
        if portable_english(previous):
            revised=previous
            row["translation_fidelity_status"]=RESTORED
            preserved+=1
        else:
            revised=file.read_text(encoding="utf-8")
            subject=path.split("/")[-1]
            matched=None
            for pattern,family,guide,caveat in OVERRIDES:
                if re.search(pattern,subject,re.I):
                    matched=(family,guide,caveat)
                    break
            if matched:
                family,guide,caveat=matched
                revised=re.sub(r"^# Methodological decision card — .*? — ",
                               "# Methodological decision card — "+family+" — ",
                               revised,count=1,flags=re.M)
                a=r"(?s)(## Original English methodological guidance \[I\]\n).*?(\n\n## Limits and alternative interpretations \[I\]\n).*?(\nSource-specific conclusions require)"
                def f(m):
                    return m.group(1)+guide+m.group(2)+caveat+m.group(3)
                revised,num=re.subn(a,f,revised,count=1)
                if num!=1:raise ValueError("UNEXPECTED_FORMAT: "+path)
                enriched+=1
        if not revised:
            raise ValueError("EMPTY_EDITORIAL_CARD "+path)
        if not portable_english(previous) and "[L]" not in revised:
            raise ValueError("GRADE_LOST_IN_NEW_CARD "+path)
        file.write_text(revised,encoding="utf-8")
        row["sha256"]=lookup[path]["sha256"]=hash_bytes(revised)
    assert preserved+enriched>=40,(preserved,enriched)
    cp.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    doc=ROOT/"docs/ALL-MARKDOWN-LANGUAGE-STATUS.md"
    s=doc.read_text(encoding="utf-8")
    marker="## Second-round editorial quality verification — 22 November 2026\n"
    s=s.replace("## Current English-language remediation — 22 November 2026",
                marker+"\nPre-existing high-quality English editorial cards were restored from the immutable baseline where their text was already English. Other cards received specific methodological cautions when the title and source scope allowed a conservative editorial decision. Neither action changes independent scientific-review status or copyright.\n\n## Current English-language remediation — 22 November 2026",1)
    doc.write_text(s,encoding="utf-8")
    report={"previous_english_cards_restored":preserved,
            "english_editorial_cards_enriched":enriched,
            "remaining_subject_cards":110-preserved-enriched,
            "scientific_approvals":0,
            "source_rights_changed":False,
            "fidelity_verified_for_every_card":False}
    Path("/tmp/english-quality-pass.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report))
if __name__=="__main__":
    main()
