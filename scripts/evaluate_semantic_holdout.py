#!/usr/bin/env python3
"""One-pass post-freeze synthetic holdout check against unchanged REG-011.

Developer-labeled fictional cases are new to the detector's development
examples; this is NOT independently adjudicated, blinded, or population-
representative scientific validation. No thresholds are fitted here.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile

from evaluation_registry import canonical, digest, record, validate_catalog
from evaluation_package import build as replay_build, validate as replay_verify
from evaluate_semantic_challenge import prepare, assessment, take, UNAUTHENTICATED
from claim_overreach_signals import VERSION as RISK_VERSION

LABELS=("SUPPORTED","PARTIALLY_SUPPORTED","NOT_SUPPORTED","INCONCLUSIVE")
EXPECTED_IDS={f"HLD-{i:03d}" for i in range(1,25)}
SEPARATE_FROM_DEVELOPMENT_CASES=True

def frozen(path: Path) -> dict:
    if path.is_symlink() or not path.is_file() or path.stat().st_size>1_000_000:
        raise ValueError("Held-out fixture unavailable or above size limit")
    data=json.loads(path.read_text(encoding="utf-8"))
    meta=data.get("protocol")
    cases=data.get("cases")
    if (data.get("schema_version")!=1 or
        data.get("kind")!="REG011_HELDOUT_V1_AUTHOR_LABELED_SYNTHETIC" or
        not isinstance(meta,dict) or
        meta.get("frozen_case_count")!=24 or
        meta.get("no_detector_refit_on_holdout") is not True or
        meta.get("preregistered_before_execution") is not True or
        meta.get("independent_human_ground_truth") is not False or
        meta.get("labels_development_assistant_authored") is not True or
        not isinstance(cases,list) or len(cases)!=24):
        raise ValueError("Invalid frozen held-out case protocol")
    ids=[]
    for row in cases:
        if not isinstance(row,dict) or row.get("synthetic") is not True:
            raise ValueError("Only fictional synthetic inputs allowed")
        cid=row.get("case_id")
        if not isinstance(cid,str) or not re.fullmatch(r"HLD-[0-9]{3}",cid):
            raise ValueError("Invalid holdout case ID")
        ids.append(cid)
        if row.get("gold_support") not in LABELS:
            raise ValueError("Unsupported provisional gold class")
        if any(not isinstance(row.get(k),str) or len(row[k].strip())<40
               for k in ("claim_text","source_passage","gold_rationale")):
            raise ValueError("Held-out case has missing content")
    if len(set(ids))!=24 or set(ids)!=EXPECTED_IDS:
        raise ValueError("Held-out identifiers are not frozen unique series")
    if {x:sum(r["gold_support"]==x for r in cases) for x in LABELS}!={x:6 for x in LABELS}:
        raise ValueError("Held-out label distribution changed")
    return data

def evaluate(fixture: Path, output: Path, *, revision: str) -> dict:
    if output.exists() or output.is_symlink():
        raise ValueError("Evaluation results must use a new output directory")
    if not isinstance(revision,str) or not re.fullmatch(r"[0-9a-f]{40}",revision):
        raise ValueError("Exact checked-out source revision is required")
    data=frozen(fixture)
    output.mkdir(parents=True,exist_ok=False)
    evidence_dir=output/"evidence"
    evidence_dir.mkdir()
    catalog_rows=[]
    obs=[]
    cases=[]
    for example in data["cases"]:
        cid=example["case_id"]
        with tempfile.TemporaryDirectory(prefix="holdout-fictional-") as temp:
            project=Path(temp)
            prepare(project,example)
            missing=take(project)
            blanket=take(project,assessment(project,example,label_aware=False))
        if missing["status"]!="PENDING_HUMAN_REVIEW":
            raise ValueError("Unauthenticated no-judgment state was lost")
        if blanket["status"]!=UNAUTHENTICATED or blanket["semantic_support_proven"]:
            raise ValueError("Claim was incorrectly approved or review state changed")
        if blanket["researcher_authenticated"]:
            raise ValueError("Simulated reviewer was authenticated")
        codes=blanket["semantic_risk_codes"]
        if not isinstance(codes,list) or any(not isinstance(x,str) for x in codes):
            raise ValueError("Malformed risk signal codes")
        expected="PASS" if example["gold_support"]=="SUPPORTED" else "FLAG"
        actual="FLAG" if codes else "PASS"
        catalog_rows.append({
            "case_id":cid,"category":"synthetic_semantic_holdout",
            "scenario":example["error_type"],
            "control":"semantic_claim_review",
            "expected_action":expected,"synthetic":True,
        })
        # Only coded observations and generic hashes; raw text is excluded.
        proof={
            "schema_version":1,"case_id":cid,
            "gold_support_author_labeled":example["gold_support"],
            "gold_independently_verified":False,
            "source_claim_fixture_sha256":hashlib.sha256(canonical({
                "source_passage":example["source_passage"],
                "claim_text":example["claim_text"]})).hexdigest(),
            "no_declaration_status":missing["status"],
            "blanket_declaration_status":blanket["status"],
            "lexical_probe_status":blanket["semantic_probe_status"],
            "lexical_risk_codes":codes,
            "expected_action":expected,"observed_action":actual,
            "matched_author_label":actual==expected,
            "real_provider_query":False,"scientific_support_proven":False,
            "human_reviewer_authenticated":False,
        }
        ev=evidence_dir/(cid+".json")
        ev.write_text(json.dumps(proof,sort_keys=True,indent=2)+"\n",encoding="utf-8")
        obs.append({"case_id":cid,"observed_action":actual,
                    "evidence_reference":"evidence/"+ev.name})
        cases.append({"case_id":cid,"author_label":example["gold_support"],
                      "expected_action":expected,"observed_action":actual,
                      "possible_overreach_codes":codes,
                      "matched_author_label":actual==expected,
                      "proof_sha256":hashlib.sha256(ev.read_bytes()).hexdigest()})
    catalog={"schema_version":1,"purpose":"SYNTHETIC_ADVERSARIAL_CASES",
             "notes":"Author labels, distinct from real scientific truth; PASS never certifies support",
             "cases":catalog_rows}
    validate_catalog(catalog)
    (output/"observation_catalog.json").write_text(json.dumps(catalog,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    (output/"observations.json").write_text(json.dumps({
        "schema_version":1,"cases":obs},sort_keys=True,indent=2)+"\n",encoding="utf-8")
    recorded=record(output/"observation_catalog.json",output/"observations.json",
                    output/"evaluation_runs.jsonl","synthetic-holdout-001",revision)
    replay_build(output/"evaluation-replay.zip",output/"observation_catalog.json",
                 ledger=output/"evaluation_runs.jsonl")
    replay_verify(output/"evaluation-replay.zip")
    positives=[x for x in cases if x["author_label"]!="SUPPORTED"]
    negatives=[x for x in cases if x["author_label"]=="SUPPORTED"]
    tp=sum(x["observed_action"]=="FLAG" for x in positives)
    fn=len(positives)-tp
    fp=sum(x["observed_action"]=="FLAG" for x in negatives)
    tn=len(negatives)-fp
    result={
        "schema_version":1,
        "kind":"REG011_UNTUNED_DEVELOPER_LABELED_SYNTHETIC_HOLDOUT",
        "case_count":len(cases),
        "benchmark_sha256":digest(data),
        "source_commit_declared":revision,
        "frozen_detector_commit_declared":data["protocol"]["evaluated_against_frozen_detector_commit"],
        "lexical_rule_set":RISK_VERSION,
        "label_source":"DEVELOPMENT_ASSISTANT_NOT_INDEPENDENT",
        "reference_labels_independently_verified":False,
        "no_detector_refit_to_holdout":True,
        "reported_without_human_review":len(cases),
        "scored_against_author_labels_only":True,
        "confusion_counts":{
            "true_positive":tp,"false_negative":fn,"false_positive":fp,"true_negative":tn,
            "n_author_labeled_problematic":len(positives),
            "n_author_labeled_supported":len(negatives),
            "sensitivity_this_synthetic_sample_only":round(tp/len(positives),3),
            "specificity_this_synthetic_sample_only":round(tn/len(negatives),3)},
        "reg001_recorded":recorded["result"]["observed"],
        "reg001_expected_matches":recorded["result"]["matches_expected"],
        "reg001_mismatches":recorded["result"]["mismatches"],
        "error_cases":[x["case_id"] for x in cases if not x["matched_author_label"]],
        "cases":cases,
        "semantic_entailment_established":False,
        "human_review_authenticated":False,
        "scientific_quality_validated":False,
        "real_academic_documents_used":False,
        "provider_queries_performed":0,
        "gate_approved":False,
        "drive_synchronized":False,
        "interpretation":"Fixed development-independent-case software probe only, with developer-authored labels. Results are NOT independently assessed scientific performance.",
    }
    (output/"holdout_assessment.json").write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--benchmark",type=Path,required=True)
    p.add_argument("--out-dir",type=Path,required=True)
    p.add_argument("--skill-commit",required=True)
    args=p.parse_args(argv)
    try:
        result=evaluate(args.benchmark,args.out_dir,revision=args.skill_commit)
        print(json.dumps({k:v for k,v in result.items() if k!="cases"},sort_keys=True,indent=2))
        return 0
    except (ValueError,OSError,TypeError,KeyError,json.JSONDecodeError) as exc:
        print("HELDOUT_EVALUATION_ERROR: "+type(exc).__name__+": "+str(exc),file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
