#!/usr/bin/env python3
"""Repeat synthetic fixtures and compare legacy vs contextual risk hints.

The original 24 examples are development-visible to this authoring process.
Do not call them a new blind holdout, independent scientific evaluation,
real-world efficacy, or a source of new training thresholds.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile

from evaluation_registry import canonical, digest, record, validate_catalog
from evaluation_package import build as make_package, validate as verify_package
from evaluate_semantic_holdout import frozen
from evaluate_semantic_challenge import prepare, assessment
from semantic_claim_review import review

def metrics(rows: list[dict], key: str) -> dict:
    pos=[r for r in rows if r["author_label"]!="SUPPORTED"]
    neg=[r for r in rows if r["author_label"]=="SUPPORTED"]
    tp=sum(bool(x[key]) for x in pos)
    fp=sum(bool(x[key]) for x in neg)
    fn=len(pos)-tp
    tn=len(neg)-fp
    return {
        "true_positive":tp,"false_negative":fn,
        "false_positive":fp,"true_negative":tn,
        "author_labeled_negative":len(pos),"author_labeled_positive":len(neg),
        "sensitivity_on_author_labels":round(tp/len(pos),3),
        "specificity_on_author_labels":round(tn/len(neg),3),
    }

def evaluate(benchmark: Path, output: Path, *, revision: str) -> dict:
    if output.exists() or output.is_symlink():
        raise ValueError("A new output directory is required")
    if not isinstance(revision,str) or not re.fullmatch("[a-f0-9]{40}",revision):
        raise ValueError("Exact lowercase 40-digit source commit required")
    source=frozen(benchmark)
    output.mkdir(parents=True,exist_ok=False)
    evid=output/"evidence"
    evid.mkdir()
    results=[]
    for case in source["cases"]:
        with tempfile.TemporaryDirectory(prefix="context-probe-fixture-") as t:
            root=Path(t)
            prepare(root,case)
            reviewed=review(root,assessment(root,case,label_aware=False))
        if (len(reviewed["review_items"])!=1 or
            reviewed["review_items"][0]["status"]!="HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED" or
            reviewed["semantic_support_proven"] is not False or
            reviewed["gate_approval_performed"] is not False or
            reviewed["researcher_authenticated"] is not False):
            raise ValueError("Expected only recorded, unverified synthetic declaration")
        row=reviewed["review_items"][0]
        lex=row["semantic_risk_codes"]
        context=row.get("contextual_signal_codes")
        if row.get("contextual_probe_status")!="SCREENED_EXPERIMENTAL_CONTEXT_ONLY" or not isinstance(context,list):
            raise ValueError("Context probe did not run after a verified quotation")
        if row.get("contextual_signals_block_workflow") is not False or row.get("heuristic_blocks_workflow") is not False:
            raise ValueError("A screening hint was given gate/block authority")
        identifier=case["case_id"]
        proof={"schema_version":1,"case_id":identifier,
               "author_label":case["gold_support"],
               "author_label_independently_approved":False,
               "source_and_claim_sha256":hashlib.sha256(canonical({
                   "claim":case["claim_text"],"excerpt":case["source_passage"]})).hexdigest(),
               "lexical_codes":lex,"contextual_codes":context,
               "status":row["status"],"human_review_authenticated":False,
               "scientific_verdict":None,"no_raw_excerpt_exported":True}
        evidence=evid/(identifier+".json")
        evidence.write_text(json.dumps(proof,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        results.append({"case_id":identifier,"author_label":case["gold_support"],
                        "legacy_flag":bool(lex),"contextual_flag":bool(context),
                        "legacy_codes":lex,"contextual_codes":context,
                        "evidence_sha256":hashlib.sha256(evidence.read_bytes()).hexdigest()})
    catalog={"schema_version":1,"purpose":"SYNTHETIC_ADVERSARIAL_CASES","cases":[
        {"case_id":r["case_id"],"category":"development_exposed_comparison",
         "scenario":"author_labeled_support_challenge",
         "control":"semantic_claim_review",
         "expected_action":"PASS" if r["author_label"]=="SUPPORTED" else "FLAG",
         "synthetic":True} for r in results]}
    validate_catalog(catalog)
    catalog_path=output/"comparison_catalog.json"
    catalog_path.write_text(json.dumps(catalog,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    ledger=output/"evaluation_runs.jsonl"
    run_metrics={}
    for key,name in (("legacy_flag","lexical"),("contextual_flag","contextual")):
        observed_path=output/(name+"_observations.json")
        observed_path.write_text(json.dumps({"schema_version":1,"cases":[
            {"case_id":r["case_id"],"observed_action":"FLAG" if r[key] else "PASS",
             "evidence_reference":"evidence/"+r["case_id"]+".json"} for r in results]},
             indent=2,sort_keys=True)+"\n",encoding="utf-8")
        record(catalog_path,observed_path,ledger,"synthetic-comparison-"+name,revision)
        run_metrics[name]=metrics(results,key)
    pkg=output/"comparison-replay.zip"
    make_package(pkg,catalog_path,ledger=ledger)
    validated=verify_package(pkg)
    if validated["run_count"]!=2 or validated["observed_total"]!=len(results)*2:
        raise ValueError("Failed to validate replayed comparison")
    report={"schema_version":1,"kind":"REG011_EXPERIMENTAL_CONTEXTUAL_COMPARISON",
            "source_commit_declared":revision,"benchmark_sha256":digest(source),
            "label_source":"DEVELOPMENT_ASSISTANT_NOT_INDEPENDENT",
            "fixture_already_seen_by_development_assistant":True,
            "blind_prospective_holdout":False,
            "new_independently_verified_corpus":False,
            "case_count":len(results),"lexical":run_metrics["lexical"],
            "contextual":run_metrics["contextual"],
            "lexical_minus_contextual_false_alarms":(
                run_metrics["lexical"]["false_positive"]-
                run_metrics["contextual"]["false_positive"]),
            "contextual_minus_lexical_true_positives":(
                run_metrics["contextual"]["true_positive"]-
                run_metrics["lexical"]["true_positive"]),
            "comparison_stages":"PARALLEL_SIDECARS_ONLY",
            "detector_thresholds_or_rules_adjusted_in_this_run":False,
            "scientific_validity_established":False,
            "independent_human_review":False,
            "gates_approved":False,"real_sources_verified":False,
            "google_drive_sync":False,
            "cases":results}
    (output/"comparison.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return report

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--benchmark",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    p.add_argument("--skill-commit",required=True)
    args=p.parse_args(argv)
    try:
        data=evaluate(args.benchmark,args.output_dir,revision=args.skill_commit)
        print(json.dumps({k:v for k,v in data.items() if k!="cases"},
                         indent=2,sort_keys=True))
        return 0
    except (ValueError,OSError,TypeError,KeyError,json.JSONDecodeError) as exc:
        print("CONTEXTUAL_COMPARISON_ERROR: "+type(exc).__name__+": "+str(exc),file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
