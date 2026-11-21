#!/usr/bin/env python3
"""Prelabeled synthetic semantic-support challenge for existing REG-011.

No external articles, research subjects, actual peer reviewers, web requests
or model-based semantic judgments are used. A fake human declaration is
ADVERSARIAL INPUT, never authenticated human participation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile

from evaluation_package import build as replay_build, validate as replay_verify
from evaluation_registry import digest, record, validate_catalog, read_ledger
from semantic_claim_review import MGMT, CLAIMS, EVIDENCE, SOURCE_REPORT, review, sha, clean
from source_report_integrity import manifest
from verify_sources import digest as source_digest

LABELS = ("SUPPORTED","PARTIALLY_SUPPORTED","NOT_SUPPORTED","INCONCLUSIVE")
SUPPORTING = "SUPPORTED"
UNAUTHENTICATED = "HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED"

def load_frozen(path: Path) -> dict:
    if path.is_symlink() or not path.is_file() or path.stat().st_size>1_000_000:
        raise ValueError("Authorized bounded frozen synthetic benchmark unavailable")
    data=json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version")!=1 or data.get("kind")!="REG011_AUTHOR_LABELED_SYNTHETIC_SUPPORT_CHALLENGE":
        raise ValueError("Unexpected challenge benchmark schema")
    p=data.get("protocol")
    items=data.get("cases")
    if not isinstance(p,dict) or not isinstance(items,list) or len(items)!=16:
        raise ValueError("Frozen benchmark must have exactly sixteen cases")
    if p.get("frozen_case_count")!=16 or p.get("gold_created_by")!="DEVELOPMENT_ASSISTANT_NOT_INDEPENDENT_ADJUDICATOR" or \
       p.get("semantic_ground_truth_independently_established") is not False or p.get("no_external_sources") is not True:
        raise ValueError("Challenge protocol is not explicitly synthetic and non-independent")
    ids=set()
    counts={key:0 for key in LABELS}
    for item in items:
        if not isinstance(item,dict) or item.get("synthetic") is not True:
            raise ValueError("Only author-labeled synthetic cases are permitted")
        cid=item.get("case_id")
        if not isinstance(cid,str) or not re.fullmatch(r"SYN-\d{3}",cid) or cid in ids:
            raise ValueError("Invalid or duplicate case ID")
        ids.add(cid)
        label=item.get("gold_support")
        if label not in counts:
            raise ValueError("Unrecognized reference classification")
        counts[label]+=1
        if any(not isinstance(item.get(k),str) or len(item[k].strip())<40
               for k in ("source_passage","claim_text","gold_rationale")):
            raise ValueError("Challenge lacks substantive source, claim or rationale")
    if set(ids)!={"SYN-"+str(n).zfill(3) for n in range(1,17)} or any(n!=4 for n in counts.values()):
        raise ValueError("Challenge changed from the balanced frozen sixteen-case design")
    return data

def csv_file(path: Path, rows: list[dict]):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def prepare(root: Path, item: dict):
    mgmt=root/MGMT
    mgmt.mkdir(parents=True)
    source=root/"synthetic_source.txt"
    source.write_text(item["source_passage"]+"\n",encoding="utf-8")
    csv_file(mgmt/CLAIMS,[{
        "Claim_ID":"CLAIM-0001","Claim_type":"[L]",
        "Claim_text":item["claim_text"],"Evidence_IDs":"EVID-0001",
    }])
    csv_file(mgmt/EVIDENCE,[{
        "Evidence_ID":"EVID-0001","Record_ID":"REC-0001",
        "Citation":"FICTIONAL SOURCE — NOT A REAL PUBLICATION",
        "DOI_or_persistent_ID":"10.9999/synthetic-fixture",
        "Supporting_locator":item["source_passage"],
    }])
    csv_file(mgmt/"03_Screening.csv",[{"Record_ID":"REC-0001"}])
    csv_file(mgmt/"04_FullText_Tracker.csv",[{
        "Record_ID":"REC-0001","Evidence_matrix_id":"EVID-0001",
        "File_or_URL":"synthetic_source.txt",
    }])
    # A controlled negative test can present an internally coherent provider
    # assertion that is fully MOCKED. This is NOT an independent metadata check.
    source_report={
        "schema_version":2,"input_manifest":manifest(root),"offline":False,
        "synthetic_mocked_metadata":True,"external_provider_queries":0,
        "checks":[{
            "Evidence_ID":"EVID-0001","Record_ID":"REC-0001",
            "doi":"10.9999/synthetic-fixture",
            "metadata_status":"VERIFIED",
            "metadata_checks":[{"provider":"synthetic-fixture","status":"VERIFIED"}],
            "locator_status":"MATCHED",
            "source_path":"synthetic_source.txt",
            "source_sha256":source_digest(source),
            "retraction_alert":False,"correction_alert":False,
            "update_alert":False,"provider_warnings":[],
            "editorial_notices":[],"result":"METADATA_AND_LOCATOR_CHECKED",
        }],
    }
    (mgmt/SOURCE_REPORT).write_text(json.dumps(source_report,sort_keys=True),encoding="utf-8")
    return source,source_report

def assessment(root: Path, item: dict, *, label_aware: bool):
    label=item["gold_support"] if label_aware else "SUPPORTED"
    alignment=({"SUPPORTED":"ALIGNED",
                "PARTIALLY_SUPPORTED":"OVERGENERALIZED",
                "NOT_SUPPORTED":"MISREPRESENTED",
                "INCONCLUSIVE":"UNKNOWN"}[label]
               if label_aware else "ALIGNED")
    source=root/"synthetic_source.txt"
    entry={
        "claim_id":"CLAIM-0001","evidence_id":"EVID-0001",
        "claim_sha256":sha(clean(item["claim_text"]).encode("utf-8")),
        "source_sha256":source_digest(source),
        "source_report_sha256":sha((root/MGMT/SOURCE_REPORT).read_bytes()),
        "reviewer_kind":"HUMAN_DECLARED",
        "reviewer":"SYNTHETIC_NOT_AN_ACTUAL_HUMAN_REVIEWER",
        "response_reference":"SYNTHETIC_ADVERSARIAL_FIXTURE_ONLY",
        "judgment":label,
        "scope_alignment":alignment,
        "method_alignment":"ALIGNED" if label_aware and label=="SUPPORTED" else alignment,
        "context_alignment":"ALIGNED" if label_aware and label=="SUPPORTED" else alignment,
        "counterevidence_considered":True,
        "rationale":"Synthetic input supplied by the evaluation script; "
                    + (item["gold_rationale"] if label_aware else
                       "the declaration falsely claims full support regardless of source."),
        "limitations":"This is a fictional fixture, NOT an authenticated researcher judgment.",
        "quoted_passage":item["source_passage"],
    }
    return {"schema_version":1,"reviews":[entry]}

def take(root: Path, reviews=None) -> dict:
    result=review(root,reviews)
    if len(result["review_items"])!=1:
        raise ValueError("Expected one literature claim and one evidence pair")
    item=result["review_items"][0]
    if result["semantic_support_proven"] is not False or \
       result["researcher_authenticated"] is not False or \
       result["gate_approval_performed"] is not False:
        raise ValueError("Synthetic fixture was misrepresented as scientific proof")
    return {"status":item["status"],
            "declared_judgment":item["declared_judgment"],
            "semantic_support_proven":False,
            "researcher_authenticated":False,
            "semantic_probe_status":item.get("semantic_probe_status", "NOT_EVALUATED"),
            "semantic_risk_codes":item.get("semantic_risk_codes", []),
            "heuristic_review_needed":bool(item.get("semantic_risk_codes", []))}

def evaluate(benchmark_path: Path, out: Path, *, source_commit: str) -> dict:
    if out.exists() or out.is_symlink():
        raise ValueError("Use a new result directory; never overwrite earlier evaluations")
    if not isinstance(source_commit,str) or not re.fullmatch("[0-9a-f]{40}",source_commit):
        raise ValueError("Exact source commit (40 lowercase hexadecimal characters) required")
    benchmark=load_frozen(benchmark_path)
    target_cases=[]
    results=[]
    observations=[]
    out.mkdir(parents=True)
    proof_dir=out/"evidence"
    proof_dir.mkdir()
    for item in benchmark["cases"]:
        cid=item["case_id"]
        with tempfile.TemporaryDirectory(prefix="semantic-synthetic-") as td:
            root=Path(td)
            prepare(root,item)
            without=take(root)
            blanket=take(root,assessment(root,item,label_aware=False))
            declared=take(root,assessment(root,item,label_aware=True))
        if without["status"]!="PENDING_HUMAN_REVIEW":
            raise ValueError("An unevaluated source was silently treated as reviewed")
        if blanket["status"]!=UNAUTHENTICATED or declared["status"]!=UNAUTHENTICATED:
            raise ValueError("Unexpected declaration path; inspect the REG-011 output")
        # A reported formal-consistency PASS never signifies scientific
        # support. The author's gold labels are an EXTERNAL challenge oracle.
        observed_action="FLAG" if blanket["heuristic_review_needed"] else "PASS"
        expected_action="PASS" if item["gold_support"]==SUPPORTING else "FLAG"
        target_cases.append({
            "case_id":cid,"category":"declared_semantic_support_challenge",
            "scenario":item["error_type"],"control":"semantic_claim_review",
            "expected_action":expected_action,"synthetic":True,
        })
        proof={
            "schema_version":1,"case_id":cid,
            "gold_support":item["gold_support"],
            "gold_label_source":"AUTHOR_LABELED_NOT_INDEPENDENT",
            "without_assessment":without,
            "blind_to_reference_label":False,
            "blanket_supported_declaration":blanket,
            "reference_label_supplied_declaration":declared,
            "observed_action":observed_action,
            "expected_semantic_challenge_action":expected_action,
            "mocked_source_verification":True,
            "heuristic_source_comparison":True,
            "not_an_independent_scientific_review":True,
        }
        path=proof_dir/(cid+".json")
        path.write_text(json.dumps(proof,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        observations.append({"case_id":cid,"observed_action":observed_action,
                             "evidence_reference":"evidence/"+cid+".json"})
        results.append({
            "case_id":cid,"gold_support":item["gold_support"],
            "expected_action":expected_action,"observed_action":observed_action,
            "semantic_discrepancy_flagged":observed_action=="FLAG",
            "risk_codes":blanket["semantic_risk_codes"],
            "recorded_without_authentication":blanket["status"]==UNAUTHENTICATED,
            "pending_without_review":without["status"]=="PENDING_HUMAN_REVIEW",
            "source_evidence_sha256":sha(path.read_bytes()),
        })
    catalog={"schema_version":1,"purpose":"SYNTHETIC_ADVERSARIAL_CASES",
             "note":"PASS means no formal contradiction in a fictional declared review, not scientific approval",
             "cases":target_cases}
    validate_catalog(catalog)
    (out/"semantic_case_catalog.json").write_text(json.dumps(catalog,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    (out/"observations.json").write_text(json.dumps({
        "schema_version":1,"cases":observations,
    },indent=2,sort_keys=True)+"\n",encoding="utf-8")
    ledger=out/"evaluation_runs.jsonl"
    recorded=record(out/"semantic_case_catalog.json",out/"observations.json",
                    ledger,"synthetic-semantic-declaration-001",source_commit)
    checks=recorded["result"]
    replay_build(out/"evaluation-replay.zip",out/"semantic_case_catalog.json",ledger=ledger)
    replay_verify(out/"evaluation-replay.zip")
    gold_negative=[x for x in results if x["gold_support"]!=SUPPORTING]
    gold_positive=[x for x in results if x["gold_support"]==SUPPORTING]
    tp=sum(x["semantic_discrepancy_flagged"] for x in gold_negative)
    fn=len(gold_negative)-tp
    fp=sum(x["semantic_discrepancy_flagged"] for x in gold_positive)
    tn=len(gold_positive)-fp
    outcome={
        "schema_version":1,"kind":"REG011_PRELIMINARY_SYNTHETIC_SUPPORT_STRESS",
        "benchmark_sha256":digest(benchmark),
        "source_commit_declared":source_commit,
        "case_count":len(results),
        "gold_author_label_distribution":{key:sum(x["gold_support"]==key for x in results) for key in LABELS},
        "without_review_pending_count":sum(x["pending_without_review"] for x in results),
        "blanket_declared_as_supported_count":sum(x["recorded_without_authentication"] for x in results),
        "declared_judgment_internally_checked_count":len(results),
        "semantic_discrepancy_confusion_author_labels":{
            "true_positive":tp,"false_negative":fn,"false_positive":fp,"true_negative":tn,
            "negative_cases":len(gold_negative),"positive_cases":len(gold_positive),
            "sensitivity_on_this_author_labeled_challenge":round(tp/len(gold_negative),3),
            "specificity_on_this_author_labeled_challenge":round(tn/len(gold_positive),3),
        },
        "reg001_recorded":checks["observed"],
        "reg001_expected_matches":checks["matches_expected"],
        "reg001_challenge_mismatches":checks["mismatches"],
        "counterexamples": [x["case_id"] for x in gold_negative if not x["semantic_discrepancy_flagged"]],
        "results":results,
        "benchmark_labels_not_independently_adjudicated":True,
        "human_participants":False,"real_academic_provider_queries":0,
        "semantic_entailment_automated":False,
        "lexical_signal_screening_only":True,
        "labels_seen_during_detector_development":True,
        "external_blinded_generalization_not_tested":True,
        "researcher_authenticated":False,
        "scientific_quality_established":False,"drive_sync_verified":False,
        "interpretation":"In-sample exploratory lexical risk screening against developer-labeled fictional examples; not blind validation, semantic entailment or scientific approval.",
    }
    (out/"preliminary_assessment.json").write_text(json.dumps(outcome,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return outcome

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--benchmark",type=Path,required=True)
    p.add_argument("--out-dir",type=Path,required=True)
    p.add_argument("--skill-commit",required=True)
    a=p.parse_args(argv)
    try:
        result=evaluate(a.benchmark,a.out_dir,source_commit=a.skill_commit)
        print(json.dumps({k:v for k,v in result.items() if k not in {"results"}},
                         indent=2,sort_keys=True))
        return 0
    except (ValueError,OSError,TypeError,KeyError,json.JSONDecodeError) as exc:
        print("SEMANTIC_CHALLENGE_ERROR: "+type(exc).__name__+": "+str(exc),file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
