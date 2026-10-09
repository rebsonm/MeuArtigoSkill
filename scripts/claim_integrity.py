#!/usr/bin/env python3
"""Deterministic claim provenance and novelty-scope checks.

Bibliographic evidence, inference and original propositions have different
burdens of justification. No automated semantic judgment is claimed.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

MGMT="00_Gestao_e_Continuidade"
CLAIMS=f"{MGMT}/09_Claims_Ledger.csv"
EVIDENCE=f"{MGMT}/05_Evidence_Matrix.csv"
SEARCH=f"{MGMT}/02_Search_Log.csv"
EXTRA_COLUMNS=[
    "Inference_warrant","Nearest_prior_Evidence_IDs","Contribution_delta",
    "Novelty_scope","Novelty_search_ref","Researcher_review_evidence",
]
TYPES={
    "L":"L","[L]":"L","LITERATURE":"L","LITERATURE_SUPPORTED":"L",
    "I":"I","[I]":"I","INFERENCE":"I","ANALYTICAL_INFERENCE":"I",
    "P":"P","[P]":"P","PROPOSITION":"P","ORIGINAL_PROPOSITION":"P",
    "EMPIRICAL_RESULT":"E",
}
FINAL={"VERIFIED","FROZEN","FINAL","READY"}
# These phrases claim exhaustive precedence. The system cannot prove their
# truth merely from a search log or a nearby DOI, so final freeze rejects them.
ABSOLUTE_RX=re.compile(
    r"\b(?:primeir[oa]s?\s+(?:estudo|pesquisa|trabalho|artigo|vez|modelo)"
    r"|pela\s+primeira\s+vez|inedit[oa]s?|nunca\s+(?:foi|foram|antes)"
    r"|nao\s+(?:existem|ha|foram\s+encontrados)\s+(?:estudos|pesquisas|trabalhos)"
    r"|unic[oa]s?\s+(?:estudo|pesquisa|trabalho)"
    r"|first[\s-]ever|first\s+(?:study|research|paper|model)"
    r"|unprecedented|never\s+(?:been|previously)\s+studied"
    r"|no\s+prior\s+(?:studies|research)|only\s+(?:study|research))\b", re.I
)
WORD_RX=re.compile(r"\b\w+\b", re.UNICODE)

def clean(value):
    return " ".join(str(value or "").split())

def normalized(value):
    decomposed=unicodedata.normalize("NFKD",clean(value).casefold())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))

def substantive(value):
    v=clean(value)
    return len(v)>=30 and len(WORD_RX.findall(v))>=5

def refs(value):
    return [s for s in re.split(r"[,;\s]+",clean(value)) if s]

def type_of(value):
    return TYPES.get(clean(value).upper(), "")

def contains_unbounded_novelty(value):
    return bool(ABSOLUTE_RX.search(normalized(value)))

def read_table(path):
    if not path.exists():
        return [],[]
    with path.open(encoding="utf-8-sig",newline="") as f:
        rdr=csv.DictReader(f)
        headers=rdr.fieldnames or []
        records=list(rdr)
    if any(None in r for r in records):
        raise ValueError("Malformed CSV input with surplus cells")
    return headers,records

def audit(claim_rows,evidence_rows,search_rows,*,strict=False,freeze=False,headers=None):
    errors,warnings=[],[]
    counts={"claims":0,"literature":0,"inference":0,"proposition":0,
            "empirical_result":0,"unsupported_novelty_phrases":0,"pending":0}
    all_evidence={clean(r.get("Evidence_ID")):r for r in evidence_rows if clean(r.get("Evidence_ID"))}
    search_index={clean(r.get("Search_ID")):r for r in search_rows if clean(r.get("Search_ID"))}
    seen=set()
    if strict and headers is not None and claim_rows:
        absent=[key for key in EXTRA_COLUMNS if key not in headers]
        if absent:
            errors.append("Claims ledger is missing required provenance columns: "+", ".join(absent))
    for i,row in enumerate(claim_rows,2):
        claim_id=clean(row.get("Claim_ID"))
        if not claim_id: continue
        counts["claims"]+=1
        if claim_id in seen:
            errors.append(f"{claim_id}: duplicate claim ID")
        seen.add(claim_id)
        kind=type_of(row.get("Claim_type"))
        if not kind:
            (errors if strict else warnings).append(f"{claim_id}: unknown epistemic type")
            continue
        key={"L":"literature","I":"inference","P":"proposition","E":"empirical_result"}[kind]
        counts[key]+=1
        is_final=clean(row.get("Draft_status")).upper() in FINAL
        mandatory=bool(freeze or (strict and is_final))
        listed=refs(row.get("Evidence_IDs"))
        nearby=refs(row.get("Nearest_prior_Evidence_IDs"))
        counter=refs(row.get("Counter_Evidence_IDs"))
        if len(set(listed))!=len(listed) or len(set(nearby))!=len(nearby):
            errors.append(f"{claim_id}: duplicate evidence identifier")
        for evidence_id in {*listed,*nearby,*counter}:
            if evidence_id not in all_evidence:
                errors.append(f"{claim_id}: unknown Evidence_ID {evidence_id}")
        text=clean(row.get("Claim_text"))
        if not text:
            errors.append(f"{claim_id}: material claim text is absent")
            continue
        if contains_unbounded_novelty(text):
            counts["unsupported_novelty_phrases"]+=1
            msg=f"{claim_id}: categorical priority/novelty language needs narrower wording; search metadata cannot prove universal absence"
            (errors if mandatory else warnings).append(msg)
        if kind=="L":
            if not listed:
                (errors if mandatory else warnings).append(f"{claim_id}: [L] requires a cited Evidence_ID")
            if mandatory:
                if not clean(row.get("Locator_status")):
                    errors.append(f"{claim_id}: [L] locator status missing; metadata presence is not semantic support")
                for evidence_id in listed:
                    src=all_evidence.get(evidence_id)
                    if src is not None and not clean(src.get("Supporting_locator")):
                        errors.append(f"{claim_id}: [L] evidence {evidence_id} lacks a source locator")
        if kind=="I":
            if not listed:
                (errors if mandatory else warnings).append(f"{claim_id}: [I] must identify the source evidence for the inference")
            if not substantive(row.get("Inference_warrant")):
                (errors if mandatory else warnings).append(f"{claim_id}: [I] needs explicit reasoning beyond a source quotation")
            if mandatory and not substantive(row.get("Boundary_conditions")):
                errors.append(f"{claim_id}: [I] requires a defensible boundary/limitation")
        if kind=="P":
            if not nearby:
                (errors if mandatory else warnings).append(f"{claim_id}: [P] requires nearest prior works (identifiable Evidence_IDs) for comparison")
            if not substantive(row.get("Contribution_delta")):
                (errors if mandatory else warnings).append(f"{claim_id}: [P] requires a specific contribution versus prior work")
            if not substantive(row.get("Novelty_scope")):
                (errors if mandatory else warnings).append(f"{claim_id}: [P] requires an explicit, bounded scope of originality")
            search_ref=refs(row.get("Novelty_search_ref"))
            if not search_ref:
                (errors if mandatory else warnings).append(f"{claim_id}: [P] lacks a traceable novelty-search reference")
            for search_id in search_ref:
                entry=search_index.get(search_id)
                if entry is None:
                    errors.append(f"{claim_id}: unknown Search_ID {search_id}")
                elif mandatory and (not clean(entry.get("Literal_query")) or
                      clean(entry.get("Status")).upper() in {"","PLANNED","INVALID","SUPERSEDED"}):
                    errors.append(f"{claim_id}: novelty search {search_id} lacks an executed and reproducible query")
        if kind=="E":
            warnings.append(f"{claim_id}: original empirical findings require separate data/protocol verification")
        if mandatory:
            if clean(row.get("Human_validation")).upper() not in {"VALIDATED","REVISED"}:
                errors.append(f"{claim_id}: final claim needs researcher validation")
            if not substantive(row.get("Researcher_review_evidence")):
                errors.append(f"{claim_id}: final claim needs traceable researcher review evidence")
        if not is_final:
            counts["pending"]+=1
    if freeze and counts["claims"]==0:
        errors.append("cannot freeze an empty scientific claims ledger")
    return {"errors":errors,"warnings":warnings,"counts":counts,
            "semantic_support_proven":False,"novelty_proven":False}

def audit_project(project,*,strict=False,freeze=False):
    root=Path(project).resolve()
    claim_file=root/CLAIMS
    if not claim_file.is_file():
        raise ValueError("Canonical claims ledger missing")
    headers, claims=read_table(claim_file)
    _,evidence=read_table(root/EVIDENCE)
    _,search=read_table(root/SEARCH)
    return audit(claims,evidence,search,strict=strict,freeze=freeze,headers=headers)

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("project")
    p.add_argument("--strict",action="store_true")
    p.add_argument("--freeze",action="store_true")
    args=p.parse_args(argv)
    try:
        result=audit_project(args.project,strict=args.strict,freeze=args.freeze)
    except (ValueError,OSError,csv.Error) as exc:
        print(f"ERROR: {exc}",file=sys.stderr)
        return 1
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if result["errors"] else 0

if __name__=="__main__":
    raise SystemExit(main())
