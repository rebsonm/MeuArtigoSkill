#!/usr/bin/env python3
"""Type-aware critical appraisal of evidence (not an automatic scientific verdict).

No commercial dependencies, no invented reviewer, no numeric universal
quality scale. A completed checklist attests only to a *recorded* appraisal.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

EVIDENCE="00_Gestao_e_Continuidade/05_Evidence_Matrix.csv"
FIELDS=["Appraisal_family","Appraisal_criteria","Appraisal_judgement",
        "Appraisal_limitations","Appraisal_reviewer","Appraisal_evidence",
        "Appraisal_rationale"]
RATINGS={"YES","NO","UNCLEAR","NOT_APPLICABLE"}
JUDGEMENTS={"USE_WITH_CAVEATS","SUITABLE_FOR_CLAIM","INSUFFICIENT_INFORMATION",
            "DO_NOT_USE_FOR_CLAIM"}
FAMILIES={
    "QUANTITATIVE":{
        "design_fit":"Is the quantitative design suitable to the stated question?",
        "sampling_bias":"Are sampling, selection and possible bias adequately addressed?",
        "measurement":"Are measures, variables and measurement limitations defensible?",
        "analysis":"Are statistical methods and uncertainty reporting appropriate?",
    },
    "QUALITATIVE":{
        "design_fit":"Is the qualitative approach coherent with the question?",
        "sampling_context":"Are sampling and context adequate and transparent?",
        "analysis_trace":"Is interpretation/analysis traceable to empirical material?",
        "reflexivity_limitations":"Are researcher position and relevant limitations addressed?",
    },
    "MIXED_METHODS":{
        "quantitative_rigor":"Are quantitative design and analyses suitable?",
        "qualitative_rigor":"Are qualitative design and analyses suitable?",
        "integration":"Are methods and findings integrated and divergences examined?",
        "limitations":"Are mixed-methods limitations and inferences adequately bounded?",
    },
    "REVIEW":{
        "question_scope":"Are review purpose, eligibility and scope explicit?",
        "search_coverage":"Is retrieval coverage and its limitations reported?",
        "selection_extraction":"Are selection and extraction procedures auditable?",
        "synthesis_appraisal":"Are synthesis method and appraisal of included sources appropriate?",
    },
    "CONCEPTUAL":{
        "construct_precision":"Are concepts and boundaries defined with precision?",
        "argument_consistency":"Are premises, arguments and claimed relationships coherent?",
        "literature_dialogue":"Does the argument engage relevant alternatives and counterpositions?",
        "scope_limits":"Are propositions and transfer limits explicit?",
    },
    "NORMATIVE":{
        "authority_version":"Is the issuing authority, legal status and document version known?",
        "jurisdiction_scope":"Are jurisdiction, temporal validity and binding scope explicit?",
        "interpretation":"Is the interpretation supported by actual provisions and context?",
        "normative_vs_empirical":"Is the document not misrepresented as empirical evidence?",
    },
    "OTHER":{
        "source_nature":"Is the type and purpose of the material explicit?",
        "provenance":"Are origin, authority and access traceable?",
        "claim_fit":"Is use of this source appropriate for the claim at issue?",
        "uncertainty":"Are limitations and uncertainty documented?",
    },
}
EMPTY={"", "ok","sim","yes","aprovado","agree","nenhum","none","n/a","not applicable"}


def normal(v):
    return " ".join(str(v or "").strip().split())


def substantial(v):
    v=normal(v)
    return len(v)>=25 and len(v.split())>=5 and v.casefold() not in EMPTY


def cite_ref(v):
    v=normal(v)
    return len(v)>=12 and v.casefold() not in EMPTY


def checks(family, data):
    """Validate checklist *documentation*, not substantive truth."""
    problems=[]
    if family not in FAMILIES:
        return ["unknown appraisal family"]
    if not isinstance(data,dict) or set(data)!=set(FAMILIES[family]):
        return ["checklist keys do not match the type-specific rubric"]
    for key in FAMILIES[family]:
        item=data[key]
        if not isinstance(item,dict) or item.get("rating") not in RATINGS:
            problems.append(f"{key}: missing or invalid rating")
            continue
        if not substantial(item.get("basis")):
            problems.append(f"{key}: explain the source-based rationale")
        if item.get("rating")=="NOT_APPLICABLE" and not substantial(item.get("basis")):
            problems.append(f"{key}: not applicable requires a reason")
    return problems


def assessment_issues(row,required=False):
    eid=normal(row.get("Evidence_ID"))
    family=normal(row.get("Appraisal_family")).upper()
    judgment=normal(row.get("Appraisal_judgement")).upper()
    if not any(normal(row.get(k)) for k in FIELDS):
        return [f"{eid}: critical appraisal not documented"] if required else []
    problems=[]
    if family not in FAMILIES:problems.append(f"{eid}: unknown appraisal family")
    if judgment not in JUDGEMENTS:problems.append(f"{eid}: missing or invalid appraisal judgement")
    try:
        entries=json.loads(row.get("Appraisal_criteria") or "")
    except (ValueError,TypeError):
        entries=None
    problems.extend(f"{eid}: {v}" for v in checks(family,entries))
    if not substantial(row.get("Appraisal_limitations")):
        problems.append(f"{eid}: appraisal limitations not adequately documented")
    if not substantial(row.get("Appraisal_rationale")):
        problems.append(f"{eid}: appraisal judgement requires substantive reasoning")
    if not normal(row.get("Appraisal_reviewer")) or normal(row.get("Appraisal_reviewer")).casefold() in {"ai","chatgpt","llm","agent","model"}:
        problems.append(f"{eid}: appraisal requires a named human reviewer")
    if not cite_ref(row.get("Appraisal_evidence")):
        problems.append(f"{eid}: appraisal lacks a reference to actual human review")
    if isinstance(entries,dict) and family in FAMILIES and not problems:
        ratings=[entries[k]["rating"] for k in FAMILIES[family]]
        if judgment=="SUITABLE_FOR_CLAIM" and any(x!="YES" for x in ratings):
            problems.append(f"{eid}: unqualified suitability conflicts with flagged or nonapplicable criteria")
        if judgment=="USE_WITH_CAVEATS" and all(x=="YES" for x in ratings):
            # A coherent rationale may still require caveats due to external constraints:
            # do not silently change the researcher's assessment.
            pass
    return problems


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(project):
    file=Path(project).resolve()/EVIDENCE
    if not file.is_file():
        raise ValueError("evidence matrix not found")
    with file.open("r",encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        headers=reader.fieldnames or []
        rows=list(reader)
    if "Evidence_ID" not in headers or len(headers)!=len(set(headers)):
        raise ValueError("evidence table has no unique Evidence_ID")
    if any(None in r for r in rows):
        raise ValueError("malformed CSV row")
    return file,headers,rows


def write(file, headers, rows):
    headers=headers+[x for x in FIELDS if x not in headers]
    fd,name=tempfile.mkstemp(prefix=".appraisal-",suffix=".csv",dir=file.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8-sig",newline="") as out:
            writer=csv.DictWriter(out,fieldnames=headers)
            writer.writeheader()
            writer.writerows([{key:row.get(key) or "" for key in headers} for row in rows])
            out.flush()
            os.fsync(out.fileno())
        os.replace(name,file)
    finally:
        if os.path.exists(name):os.unlink(name)


def record(args):
    file,headers,rows=load(args.project)
    matching=[r for r in rows if normal(r.get("Evidence_ID"))==args.evidence_id]
    if len(matching)!=1:raise ValueError("Evidence_ID missing or ambiguous")
    row=matching[0]
    if any(normal(row.get(field)) for field in FIELDS):
        raise ValueError("existing appraisal cannot be silently overwritten; version the scientific decision")
    path=Path(args.checklist).resolve()
    if not path.is_file() or path.stat().st_size>100_000:
        raise ValueError("checklist file missing or too large")
    try:
        rubric=json.loads(path.read_text(encoding="utf-8"))
    except (ValueError,UnicodeError):
        raise ValueError("invalid JSON checklist")
    selected=args.family.upper()
    new_row=dict(row)
    new_row.update({
        "Appraisal_family":selected,
        "Appraisal_criteria":json.dumps(rubric,ensure_ascii=False,sort_keys=True,separators=(",",":")),
        "Appraisal_judgement":args.judgement.upper(),
        "Appraisal_limitations":normal(args.limitations),
        "Appraisal_reviewer":normal(args.reviewer),
        "Appraisal_evidence":normal(args.review_evidence),
        "Appraisal_rationale":normal(args.rationale),
    })
    problems=assessment_issues(new_row,required=True)
    if problems:raise ValueError("; ".join(problems))
    before=sha(file)
    row.update(new_row)
    write(file,headers,rows)
    print(json.dumps({"evidence_id":args.evidence_id,"outcome":"HUMAN_APPRAISAL_RECORDED",
                      "file_sha256_before":before,"file_sha256_after":sha(file),
                      "scientific_quality_certified":False},ensure_ascii=False))
    return 0


def audit(rows,*,required_ids=None,enforce=False,headers=None):
    required_ids=set(required_ids or [])
    problems=[]
    counts={"evidence_items":0,"assessed":0,"unassessed":0,"with_caveats":0,"insufficient":0,"not_for_claim":0}
    if enforce and headers is not None and required_ids and any(x not in headers for x in FIELDS):
        problems.append("evidence CSV lacks required appraisal fields")
    found=set()
    for row in rows:
        eid=normal(row.get("Evidence_ID"))
        if not eid:continue
        if eid in found:
            problems.append(f"duplicate Evidence_ID: {eid}")
            continue
        found.add(eid)
        counts["evidence_items"]+=1
        is_recorded=any(normal(row.get(k)) for k in FIELDS)
        if is_recorded:
            counts["assessed"]+=1
            judgement=normal(row.get("Appraisal_judgement")).upper()
            if judgement=="USE_WITH_CAVEATS":counts["with_caveats"]+=1
            if judgement=="INSUFFICIENT_INFORMATION":counts["insufficient"]+=1
            if judgement=="DO_NOT_USE_FOR_CLAIM":counts["not_for_claim"]+=1
        else:counts["unassessed"]+=1
        if eid in required_ids or is_recorded:
            problems.extend(assessment_issues(row,required=eid in required_ids))
            if eid in required_ids and normal(row.get("Appraisal_judgement")).upper() in {"INSUFFICIENT_INFORMATION","DO_NOT_USE_FOR_CLAIM"}:
                problems.append(f"{eid}: cannot rely on evidence with this appraisal judgement")
    for missing in sorted(required_ids-found):
        problems.append(f"material claim references unknown evidence: {missing}")
    return {"errors":problems,"counts":counts,
            "limits":"Completed documentation is not independent proof of research quality or reviewer identity."}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="cmd",required=True)
    template=sub.add_parser("template")
    template.add_argument("--family",required=True,choices=sorted(FAMILIES))
    recordp=sub.add_parser("record")
    recordp.add_argument("project")
    recordp.add_argument("--evidence-id",required=True)
    recordp.add_argument("--family",required=True,choices=sorted(FAMILIES))
    recordp.add_argument("--checklist",required=True)
    recordp.add_argument("--judgement",required=True,choices=sorted(JUDGEMENTS))
    recordp.add_argument("--rationale",required=True)
    recordp.add_argument("--limitations",required=True)
    recordp.add_argument("--reviewer",required=True)
    recordp.add_argument("--review-evidence",required=True)
    auditp=sub.add_parser("audit")
    auditp.add_argument("project")
    auditp.add_argument("--require-evidence",action="append",default=[])
    auditp.add_argument("--strict",action="store_true")
    args=parser.parse_args(argv)
    try:
        if args.cmd=="template":
            print(json.dumps({k:{"question":v,"rating":"","basis":""} for k,v in FAMILIES[args.family].items()},ensure_ascii=False,indent=2))
            return 0
        if args.cmd=="record":return record(args)
        _,headers,records=load(args.project)
        report=audit(records,required_ids=args.require_evidence,enforce=args.strict,headers=headers)
        print(json.dumps(report,ensure_ascii=False,indent=2))
        return 1 if report["errors"] else 0
    except (OSError,ValueError,csv.Error) as exc:
        print(f"ERROR: {exc}",file=sys.stderr)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
