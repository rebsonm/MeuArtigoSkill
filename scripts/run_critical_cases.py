#!/usr/bin/env python3
"""Execute twelve fixed adversarial scenarios against actual offline controls.

Fixtures and academic-provider replies are SYNTHETIC. The real installed
local functions are invoked; no live Crossref, Drive, researcher or scholarly
evaluation is performed. A NOT_EVALUATED result is never counted as success.
Only neutral codes and source checksums are exported to evaluation files.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from audit_anonymization import scan_text
from claim_integrity import audit as claim_audit
from dedupe_records import run_import
from evaluation_registry import canonical, digest, load, record, validate_catalog
from evaluation_package import build as replay_build, validate as replay_verify
from formative_gates import gate_issues
from governance_events import GATE_HEADERS
from native_chat_dashboard import panel as project_panel
from rights_audit import evaluated_rights
from semantic_claim_review import valid_annotation
from verify_sources import match_metadata

EXPECTED_CONTROLS = {
    "DOI-001":"verify_sources",
    "DOI-002":"verify_sources",
    "LOC-003":"claim_integrity",
    "SUP-004":"human_semantic_review",
    "GAT-005":"governance_events",
    "STO-006":"preflight",
    "TRC-007":"claim_integrity",
    "ANON-008":"audit_anonymization",
    "ACC-009":"rights_audit",
    "DUP-010":"dedupe_records",
    "INF-011":"claim_integrity",
    "PRO-012":"claim_integrity",
}
FIXTURE_KIND = {
    "DOI-001":"MOCKED_PROVIDER_REPLY",
    "DOI-002":"MOCKED_PROVIDER_REPLY",
    "GAT-005":"ISOLATED_LOCAL_PROCESS",
    "DUP-010":"ISOLATED_LOCAL_IMPORT",
}
_ACTIONS = {"BLOCK","FLAG","PASS","NOT_EVALUATED"}

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def _claim(kind: str, *, text: str = "A synthetic assertion about a bounded scholarly example.",
           evidence: str = "EVID-0001", **values) -> dict:
    return {
        "Claim_ID":"CLAIM-0001","Claim_type":kind,"Claim_text":text,
        "Evidence_IDs":evidence,"Draft_status":"DRAFT","Locator_status":"MATCHED",
        **values,
    }

def _audit_claims(claims, evidence=None, *, freeze=False):
    return claim_audit(
        claims, evidence if evidence is not None else [
            {"Evidence_ID":"EVID-0001","Citation":"Synthetic scholarly record",
             "Supporting_locator":"p. 3"}],
        [], freeze=freeze,
    )

def _csv(path: Path, headers: list[str], rows: list[dict]):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def probe(case_id: str, root: Path) -> dict:
    """Map real control output to the catalog's abstract BLOCK/FLAG actions.

    This is rule-based classification of observed code/status, not an
    assertion that a mocked source is genuinely retracted or fictitious.
    """
    root.mkdir()
    if case_id=="DOI-001":
        status, checks, *_ = match_metadata(
            "10.9999/synthetic-unavailable",
            "Bounded synthetic title", "2024", "",
            {"crossref":{"status":"NOT_FOUND"},
             "openalex":{"status":"NOT_FOUND"}})
        return {"observed_action":"FLAG" if status=="NOT_FOUND" else "PASS",
                "finding":"PROVIDER_NOT_FOUND" if status=="NOT_FOUND" else "NO_EXPECTED_FINDING",
                "observed_status":status,"providers_checked":len(checks)}
    if case_id=="DOI-002":
        doi="10.1234/synthetic-other-work"
        status,checks,*_ = match_metadata(
            doi, "Claimed synthetic paper", "2024","",
            {"crossref":{"status":"FOUND","data":{
                "DOI":doi,"title":["Entirely different synthetic paper"],
                "published":{"date-parts":[[2024]]}}},
             "openalex":{"status":"FOUND","data":{
                "doi":"https://doi.org/"+doi,
                "display_name":"Another unrelated synthetic publication",
                "publication_year":2024}}})
        mismatch=any(c["status"] in {"TITLE_MISMATCH","DOI_MISMATCH"} for c in checks)
        return {"observed_action":"FLAG" if mismatch else "PASS",
                "finding":"CITATION_METADATA_MISMATCH" if mismatch else "NO_EXPECTED_FINDING",
                "observed_status":status,"providers_checked":len(checks)}
    if case_id=="LOC-003":
        result=_audit_claims(
            [_claim("[L]",Human_validation="VALIDATED",
                    Researcher_review_evidence="Synthetic decision; no actual researcher claim")],
            [{"Evidence_ID":"EVID-0001","Citation":"Synthetic scholarly work",
              "Supporting_locator":""}],freeze=True)
        issue=any("lacks a source locator" in e for e in result["errors"])
        return {"observed_action":"BLOCK" if issue else "PASS",
                "finding":"MISSING_SOURCE_LOCATOR" if issue else "NO_EXPECTED_FINDING",
                "control_errors_count":len(result["errors"])}
    if case_id=="SUP-004":
        annotation={
            "reviewer_kind":"HUMAN_DECLARED","reviewer":"Synthetic reviewer",
            "response_reference":"Synthetic assessment fixture only",
            "rationale":"The cited study covers a narrow setting and cannot justify broad generality.",
            "limitations":"The contextual limitations restrict any generalization.",
            "claim_sha256":"a"*64,"source_sha256":"b"*64,
            "source_report_sha256":"c"*64,
            "scope_alignment":"OVERGENERALIZED","method_alignment":"ALIGNED",
            "context_alignment":"ALIGNED","counterevidence_considered":True,
            "judgment":"SUPPORTED",
        }
        actual=valid_annotation(annotation,"a"*64,"b"*64,"c"*64)
        detected=actual=="UNQUALIFIED_SUPPORT_CONTRADICTS_REVIEW"
        return {"observed_action":"FLAG" if detected else "PASS",
                "finding":"SELF_REPORTED_SUPPORT_INCONSISTENT" if detected else "NO_EXPECTED_FINDING",
                "control_status":actual or "NO_FORMAL_INCONSISTENCY",
                "semantic_entailment_verified":False}
    if case_id=="GAT-005":
        mgmt=root/"00_Gestao_e_Continuidade"
        mgmt.mkdir()
        gates=mgmt/"18_Human_Validation_Gates.csv"
        _csv(gates,GATE_HEADERS,[{"GATE_ID":"GATE-0002",
                                 "Gate_type":"METHOD_PROTOCOL","Status":"READY"}])
        (mgmt/"PROJECT_CONFIG.json").write_text(
            json.dumps({"formative_gates_required":True}),encoding="utf-8")
        before=gates.read_bytes()
        process=subprocess.run([
            sys.executable,str(Path(__file__).with_name("governance_events.py")),
            "gate",str(root),"--gate-id","GATE-0002",
            "--decision","APPROVED","--validated-by","Synthetic person",
            "--method","Synthetic protocol review","--evidence",
            "Synthetic source reference","--no-snapshot",
        ],capture_output=True,text=True,timeout=20,check=False)
        blocked=(process.returncode!=0 and before==gates.read_bytes())
        return {"observed_action":"BLOCK" if blocked else "PASS",
                "finding":"UNATTESTED_GATE_APPROVAL_DENIED" if blocked else "GATE_APPROVAL_NOT_DENIED",
                "return_code":process.returncode,
                "gate_file_unchanged":before==gates.read_bytes()}
    if case_id=="STO-006":
        mgmt=root/"00_Gestao_e_Continuidade"
        mgmt.mkdir()
        (mgmt/"PROJECT_CONFIG.json").write_text(
            json.dumps({"storage_mode":"GOOGLE_DRIVE","presentation_mode":"MINIMAL"}),
            encoding="utf-8")
        state=project_panel(root)
        not_verified=(state.get("drive_sync_verified_in_this_session") is False and
                      state.get("history_sync",{}).get("drive_sync_verified_in_this_session") is False)
        return {"observed_action":"BLOCK" if not_verified else "PASS",
                "finding":"UNVERIFIED_SYNC_NOT_CERTIFIED" if not_verified else "SYNC_FALSE_ASSERTION",
                "storage_presented":"GOOGLE_DRIVE",
                "drive_receipt_present":False,
                "boundary":"READ_ONLY_PRESENTATION_ONLY"}
    if case_id=="TRC-007":
        result=_audit_claims([_claim("[L]", evidence="EVID-9999")])
        missing=any("unknown Evidence_ID EVID-9999" in e for e in result["errors"])
        return {"observed_action":"BLOCK" if missing else "PASS",
                "finding":"UNKNOWN_EVIDENCE_LINK" if missing else "NO_EXPECTED_FINDING",
                "control_errors_count":len(result["errors"])}
    if case_id=="ANON-008":
        flagged=[]
        scan_text("Contact the identifying author at author@example.invalid",
                  root/"blind_manuscript.md",flagged,[],location="content")
        found=any(x["kind"]=="EMAIL" for x in flagged)
        return {"observed_action":"FLAG" if found else "PASS",
                "finding":"IDENTITY_EMAIL_DETECTED" if found else "NO_EXPECTED_FINDING",
                "highest_severity":"HIGH" if found else "NONE",
                "release_authorized":False}
    if case_id=="ACC-009":
        result=evaluated_rights({
            "Record_ID":"REC-0001","Access_basis":"OPEN_ACCESS",
            "Rights_basis":"CC_BY_4_0","File_or_URL":"https://doi.org/10.1234/fictitious",
            "License_URI":"https://creativecommons.org/licenses/by/4.0/",
        },root,for_export=True)
        refused=(result["eligible"] is False and any(
            "no local source file" in e for e in result["errors"]))
        return {"observed_action":"BLOCK" if refused else "PASS",
                "finding":"METADATA_ONLY_NO_FULLTEXT_RIGHTS" if refused else "UNEXPECTED_RIGHTS_APPROVAL",
                "control_errors_count":len(result["errors"])}
    if case_id=="DUP-010":
        path=root/"two_records.csv"
        _csv(path,["Title","DOI","Authors","Year"],[
            {"Title":"First fictional citation","DOI":"10.1234/synthetic-dupe",
             "Authors":"Example A","Year":"2025"},
            {"Title":"Alternate fictional citation","DOI":"https://doi.org/10.1234/synthetic-dupe",
             "Authors":"Example B","Year":"2025"},
        ])
        out=root/"dedupe_results"
        from argparse import Namespace
        import contextlib
        import io
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            code=run_import(out,Namespace(inputs=[str(path)],fuzzy_threshold=0.94))
        result=json.loads((out/"import_diagnostics.json").read_text(encoding="utf-8")) if code==0 else {}
        flagged=(code==0 and result.get("exact_duplicates")==1 and
                 result.get("canonical_after_exact_dedup")==1)
        return {"observed_action":"FLAG" if flagged else "PASS",
                "finding":"DUPLICATE_CONSOLIDATION_RECORDED" if flagged else "DUPLICATE_NOT_IDENTIFIED",
                "input_records":result.get("input_records",0),
                "canonical_after_exact_dedup":result.get("canonical_after_exact_dedup"),
                "exact_duplicates":result.get("exact_duplicates",0)}
    if case_id=="INF-011":
        result=_audit_claims([_claim("[I]",Inference_warrant="",
                                     Boundary_conditions="")],freeze=True)
        issue=(any("explicit reasoning" in e for e in result["errors"]) and
               any("defensible boundary" in e for e in result["errors"]))
        return {"observed_action":"BLOCK" if issue else "PASS",
                "finding":"INFERENCE_WARRANT_AND_BOUNDARY_MISSING" if issue else "NO_EXPECTED_FINDING",
                "control_errors_count":len(result["errors"])}
    if case_id=="PRO-012":
        result=_audit_claims([_claim("[P]",
            text="This is the first-ever research model and unprecedented solution.",
            Nearest_prior_Evidence_IDs="EVID-0001",
            Contribution_delta="Our synthetic approach adds an explicit contrast to a bounded prior model.",
            Novelty_scope="This claim applies only to the hypothetical reviewed scholarly corpus.",
            Novelty_search_ref="SEARCH-0001")],
            freeze=False)
        flagged=any("categorical priority/novelty language" in x for x in result["warnings"])
        return {"observed_action":"FLAG" if flagged else "PASS",
                "finding":"UNBOUNDED_NOVELTY_CLAIM" if flagged else "NO_EXPECTED_FINDING",
                "control_warnings_count":len(result["warnings"]),
                "scientific_novelty_proven":False}
    raise ValueError("Unsupported case ID: "+case_id)


def execute(catalog_path: Path, output_dir: Path, *, skill_commit: str,
            record_ledger: bool = True) -> dict:
    if output_dir.exists() or output_dir.is_symlink():
        raise ValueError("Use a NEW output directory; prior observations must be preserved")
    catalog=load(catalog_path)
    items=validate_catalog(catalog)
    if set(items)!=set(EXPECTED_CONTROLS):
        raise ValueError("Case catalog changed: explicit executable adapter review required")
    for cid,item in items.items():
        if item["control"]!=EXPECTED_CONTROLS[cid]:
            raise ValueError("Declared case control no longer matches adapter: "+cid)
    if not __import__("re").fullmatch(r"[a-f0-9]{40}",skill_commit):
        raise ValueError("Exact lower-case 40-hex checked-out source revision required")

    output_dir.mkdir(parents=True,exist_ok=False)
    proofs=output_dir/"evidence"
    proofs.mkdir()
    observations=[]
    results=[]
    for cid,item in items.items():
        with tempfile.TemporaryDirectory(prefix="critical-case-") as directory:
            try:
                actual=probe(cid,Path(directory)/"scenario")
                if actual.get("observed_action") not in _ACTIONS:
                    raise ValueError("Adapter returned unsupported action")
                observed=actual["observed_action"]
                why=actual.get("finding") or "NO_CODE"
                proof={
                    "schema_version":1,"case_id":cid,"catalog_control":item["control"],
                    "fixture_type":FIXTURE_KIND.get(cid,"SYNTHETIC_LOCAL_FIXTURE"),
                    "actual_control_invoked":True,
                    "observed_action":observed,"finding_code":why,
                    "control_observation":actual,
                    "source_commit_declared":skill_commit,
                    "independent_human_review_authenticated":False,
                    "scientific_validity_established":False,
                    "real_research_corpus_used":False,
                }
            except (ValueError,OSError,TypeError,KeyError,RuntimeError,
                    subprocess.TimeoutExpired,ImportError) as exc:
                observed="NOT_EVALUATED"
                proof={
                    "schema_version":1,"case_id":cid,"catalog_control":item["control"],
                    "fixture_type":FIXTURE_KIND.get(cid,"SYNTHETIC_LOCAL_FIXTURE"),
                    "actual_control_invoked":False,"observed_action":observed,
                    "finding_code":"CONTROL_EXECUTION_ERROR",
                    "error_class":type(exc).__name__,
                    "source_commit_declared":skill_commit,
                    "scientific_validity_established":False,
                    "real_research_corpus_used":False,
                }
        path=proofs/(cid+".json")
        path.write_bytes(json.dumps(proof,sort_keys=True,indent=2,ensure_ascii=False).encode("utf-8")+b"\n")
        reference="evidence/"+path.name if observed!="NOT_EVALUATED" else ""
        observations.append({"case_id":cid,"observed_action":observed,"evidence_reference":reference})
        results.append({"case_id":cid,"expected":item["expected_action"],
                        "observed":observed,"matches_expected": observed==item["expected_action"]
                         if observed!="NOT_EVALUATED" else None,
                        "finding_code":proof["finding_code"],
                        "proof_sha256":sha(path.read_bytes()),
                        "adapter_type":proof["fixture_type"]})
    (output_dir/"observations.json").write_bytes(json.dumps(
        {"schema_version":1,"cases":observations},sort_keys=True,indent=2).encode("utf-8")+b"\n")
    full={"schema_version":1,"kind":"SYNTHETIC_EXECUTED_SOFTWARE_CHECKS",
          "source_revision_declared":skill_commit,
          "catalog_sha256":digest(catalog),"catalog_cases":len(items),
          "observed":sum(x["observed"]!="NOT_EVALUATED" for x in results),
          "not_evaluated":sum(x["observed"]=="NOT_EVALUATED" for x in results),
          "matches_expected":sum(x["matches_expected"] is True for x in results),
          "mismatches":sum(x["matches_expected"] is False for x in results),
          "cases":results,"mocked_provider_cases":2,
          "real_academic_provider_queries_performed":0,
          "real_research_subjects_or_material":False,
          "independent_scientific_validation":False,
          "google_drive_write":False,
          "claim_semantic_entailment_validated":False}
    (output_dir/"summary.json").write_bytes(json.dumps(
        full,sort_keys=True,indent=2).encode("utf-8")+b"\n")
    if record_ledger:
        ledger=output_dir/"evaluation_runs.jsonl"
        record(catalog_path,output_dir/"observations.json",ledger,
               "synthetic-controls-001",skill_commit)
        replay_build(output_dir/"evaluation-replay.zip",catalog_path,ledger=ledger)
        replay_verify(output_dir/"evaluation-replay.zip")
    return full


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--catalog",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    p.add_argument("--skill-commit",required=True)
    p.add_argument("--no-ledger",action="store_true")
    p.add_argument("--strict",action="store_true")
    a=p.parse_args(argv)
    try:
        summary=execute(a.catalog,a.output_dir,skill_commit=a.skill_commit,
                        record_ledger=not a.no_ledger)
        for case in summary["cases"]:
            print(case["case_id"]+": "+case["observed"]+" (expected "+case["expected"]+
                  ") ["+case["finding_code"]+"]")
        print("observed="+str(summary["observed"])+
              " not_evaluated="+str(summary["not_evaluated"])+
              " matched="+str(summary["matches_expected"])+
              " mismatches="+str(summary["mismatches"]))
        print("SCIENTIFIC_VALIDITY_NOT_ESTABLISHED")
        if a.strict and (summary["not_evaluated"] or summary["mismatches"]):
            return 2
        return 0
    except (ValueError,OSError,TypeError,KeyError,json.JSONDecodeError) as exc:
        print("CRITICAL_CASE_EXECUTION_ERROR: "+type(exc).__name__,file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
