#!/usr/bin/env python3
"""REG-019: verifiable, privacy-reduced software-evaluation replay package.

This is NOT a confidential-corpus exporter or a claim of independent
scientific validation. Existing RO-Crate/PROV distribution rules remain
authoritative for any separately authorized scientific-data exchange.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED, BadZipFile

from evaluation_registry import canonical, read_ledger, validate_catalog

FIXED_DATE=(2026,10,14,0,0,0)
FILES=("CASE_CATALOG.json","PROTOCOL.json","OBSERVATIONS.json","README.md")
ALL=set(FILES)|{"MANIFEST.json"}
ACTIONS={"BLOCK","FLAG","PASS","NOT_EVALUATED"}
MAX_BYTES=4_000_000
MAX_RUNS=200
SHA40=re.compile(r"[a-f0-9]{40}\Z")
SHA64=re.compile(r"[a-f0-9]{64}\Z")

def hashed(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()

def json_bytes(data) -> bytes:
    return json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False).encode("utf-8")+b"\n"

def catalog_from(path: Path):
    if path.is_symlink() or not path.is_file() or path.stat().st_size>MAX_BYTES:
        raise ValueError("Authorized frozen case catalog unavailable or oversized")
    catalog=json.loads(path.read_text(encoding="utf-8"))
    cases=validate_catalog(catalog)
    # A caller can set synthetic=true on real content. The export must
    # enforce an explicit metadata-only schema, not trust that assertion.
    top={"schema_version","purpose","description","cases"}
    fields={"case_id","category","scenario","control","expected_action","synthetic"}
    if set(catalog)-top or any(set(row)-fields for row in cases.values()):
        raise ValueError("Evaluation ZIP catalog has undeclared content fields")
    # Prevent a hostile free-text scenario from containing a literal source
    # passage: this bounded exporter is exclusively for case descriptions,
    # not unreviewed research text or manuscript excerpts.
    if any(len(row["scenario"])>280 or len(row["category"])>80 or
           len(row["control"])>80 for row in cases.values()):
        raise ValueError("Evaluation ZIP requires brief synthetic metadata")
    return catalog,cases

def redact_ledger(ledger: Path | None, catalog: dict, cases: dict):
    if ledger is None:
        return []
    if ledger.is_symlink() or not ledger.is_file() or ledger.stat().st_size>MAX_BYTES:
        raise ValueError("Evaluation ledger unavailable, symlinked or oversized")
    rows=read_ledger(ledger)
    if len(rows)>MAX_RUNS:
        raise ValueError("Too many recorded runs for compact evaluation package")
    out=[]
    for record in rows:
        if record.get("schema_version")!=1 or record.get("case_set_sha256")!=hashed(canonical(catalog)):
            raise ValueError("Ledger contains a run against a different frozen case catalog")
        commit=record.get("skill_commit")
        if not isinstance(commit,str) or not SHA40.fullmatch(commit):
            raise ValueError("Ledger run has no valid exact source commit")
        details=record.get("result",{}).get("details")
        if not isinstance(details,list) or len(details)!=len(cases):
            raise ValueError("Ledger run has incomplete case observations")
        shown={}
        for item in details:
            cid=item.get("case_id") if isinstance(item,dict) else None
            if cid not in cases or cid in shown or item.get("expected_action")!=cases[cid]["expected_action"]:
                raise ValueError("Ledger details conflict with frozen expected actions")
            action=item.get("observed_action")
            ref=item.get("evidence_reference")
            if action not in ACTIONS or not isinstance(ref,str):
                raise ValueError("Ledger contains invalid observation")
            if action!="NOT_EVALUATED" and not ref.strip():
                raise ValueError("Observed case without recorded evidence reference")
            shown[cid]={"case_id":cid,"observed_action":action,
                         "evidence_reference_sha256":hashed(ref.encode("utf-8")) if ref else None}
        expected=score_one(cases, list(shown.values()))
        r=record["result"]
        for key in ("case_count","observed","not_evaluated","matches_expected","mismatches"):
            if type(r.get(key)) is not int or r.get(key)!=expected[key]:
                raise ValueError("Ledger summary disagrees with detailed observations")
        if r.get("match_rate_on_observed")!=expected["match_rate_on_observed"]:
            raise ValueError("Ledger recorded rate differs from recomputed rate")
        if r.get("scientific_validity_established") is not False:
            raise ValueError("Scientific approval in evaluation ledger is forbidden")
        out.append({"run_id":record["run_id"],"skill_commit":commit,
                    "case_set_sha256":record["case_set_sha256"],
                    "original_ledger_entry_sha256":record["entry_sha256"],
                    "previous_entry_sha256":record["previous_entry_sha256"],
                    "original_observations_sha256":record["observations_sha256"],
                    "cases":[shown[cid] for cid in cases],
                    "score":expected})
    return out

def score_one(cases: dict, observed: list[dict]) -> dict:
    actions={}
    for item in observed:
        if not isinstance(item,dict):
            raise ValueError("Invalid observation object")
        cid=item.get("case_id")
        action=item.get("observed_action")
        if cid not in cases or cid in actions or action not in ACTIONS:
            raise ValueError("Unknown, duplicate or invalid observation")
        checksum=item.get("evidence_reference_sha256")
        if action!="NOT_EVALUATED":
            if not isinstance(checksum,str) or not SHA64.fullmatch(checksum):
                raise ValueError("Observed action missing evidence reference digest")
        elif checksum is not None and (
                not isinstance(checksum, str) or not SHA64.fullmatch(checksum)):
            raise ValueError("Unobserved action has invalid optional evidence digest")
        actions[cid]=action
    if set(actions)!=set(cases):
        raise ValueError("Each frozen case must have an explicit observation state")
    n=sum(v!="NOT_EVALUATED" for v in actions.values())
    matched=sum(a!="NOT_EVALUATED" and a==cases[cid]["expected_action"]
                for cid,a in actions.items())
    return {"case_count":len(cases),"observed":n,
            "not_evaluated":len(cases)-n,"matches_expected":matched,
            "mismatches":n-matched,
            "match_rate_on_observed":round(matched/n,6) if n else None,
            "scientific_validity_established":False}

def project_protocol_hash(project: Path | None):
    if project is None:
        return None
    root=project.resolve()
    p=root/"00_Gestao_e_Continuidade"/"01_Protocolo.csv"
    if p.is_symlink() or not p.is_file():
        raise ValueError("Canonical project protocol is unavailable")
    if p.stat().st_size>MAX_BYTES:
        raise ValueError("Project protocol oversized")
    return hashed(p.read_bytes())

def make_payload(catalog: dict, cases: dict, runs: list, protocol_sha: str | None):
    actions={
        "freeze_case_catalog":"Use the case IDs, expected classifications and case catalog hash as fixed test conditions.",
        "execute_controlled_tests":"Execute tests externally; observations must come from actual outputs and remain separately verifiable.",
        "register_results":"Append externally observed outcomes to REG-001 ledger; do not invent successful cases.",
        "replay_metrics":"Validate package hashes then recompute matches/mismatches over the fixed catalog.",
        "review_limits":"Independently assess source access, false positives, missed detections and evaluator conflicts of interest.",
    }
    protocol={
        "schema_version":1,"kind":"REG-019_EVALUATION_REPLAY_PROTOCOL",
        "case_catalog_sha256":hashed(canonical(catalog)),
        "case_count":len(cases),"review_design":"CONTROLLED_SYNTHETIC_ADVERSARIAL_SCENARIOS",
        "steps":actions,"outcome_states":sorted(ACTIONS),
        "canonical_project_protocol_sha256":protocol_sha,
        "canonical_project_protocol_contents_included":False,
        "source_code_bundled":False,
        "independent_reviewer_authenticated":False,
        "scientific_validity_proven":False,
        "original_evidence_included":False,
    }
    observations={
        "schema_version":1,"status":"USER_SUPPLIED_RUNS" if runs else "NO_OBSERVED_RUNS",
        "case_catalog_sha256":hashed(canonical(catalog)),
        "run_count":len(runs),"runs":runs,
        "original_ledger_chain_reverifiable_from_this_redacted_package":False,
        "evidence_references_included":False,
        "evidence_reference_sha256_is_not_source_proof":True,
        "original_research_corpus_included":False,
        "independent_scientific_validation":False,
    }
    readme=(
        "# Meu Artigo — REG-019 controlled evaluation replay\n\n"
        "This archive contains a frozen, explicitly SYNTHETIC negative-case catalog, "
        "an execution protocol and redacted outcomes supplied from an existing "
        "tamper-evident local REG-001 ledger. No real tests are run by this exporter.\n\n"
        "Verify this archive with: python scripts/evaluation_package.py verify PACKAGE.zip\n"
        "The verifier rechecks hashes and recalculates outcome counts from the included "
        "declared actions. The exporter never certifies the truth of a supplied observation.\n\n"
        "No raw human assessment, DOI list, passage, copyrighted full text, local "
        "project path, personal name, source-corpus document or Drive receipt is included. "
        "The raw evaluation ledger is excluded because evidence references can be private. "
        "Its full external hash chain CANNOT be independently checked from this "
        "privacy-reduced artifact alone. Use an authorized PRIVATE evidence review "
        "and the existing RO-Crate exporter for real source-level reproducibility.\n\n"
        "Passing this technical audit does NOT validate scientific support, "
        "independent peer review, software effectiveness or a human gate decision.\n"
    ).encode("utf-8")
    return {"CASE_CATALOG.json":json_bytes(catalog),
            "PROTOCOL.json":json_bytes(protocol),
            "OBSERVATIONS.json":json_bytes(observations),"README.md":readme}

def package_data(payload: dict):
    manifest={"schema_version":1,"kind":"REG-019_REPLAY_ARCHIVE",
              "files":{name:hashed(payload[name]) for name in FILES},
              "scientific_validity_proven":False,
              "external_fulltext_included":False,
              "replay_scoped_to_recorded_software_observations":True}
    return {**payload,"MANIFEST.json":json_bytes(manifest)}

def build(target: Path, catalog_file: Path, ledger: Path | None = None,
          project: Path | None = None) -> dict:
    if target.suffix.lower()!=".zip" or target.is_symlink() or target.exists():
        raise ValueError("Use a new non-existing .zip output path")
    catalog,cases=catalog_from(catalog_file)
    rows=redact_ledger(ledger,catalog,cases)
    files=package_data(make_payload(catalog,cases,rows,project_protocol_hash(project)))
    target.parent.mkdir(parents=True,exist_ok=True)
    tmp=None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent,prefix=".reg019-",suffix=".zip",delete=False) as fh:
            tmp=Path(fh.name)
        with ZipFile(tmp,"w",compression=ZIP_DEFLATED,compresslevel=9) as arc:
            for name in sorted(files):
                info=ZipInfo(name,FIXED_DATE)
                info.compress_type=ZIP_DEFLATED
                info.external_attr=0o100644<<16
                arc.writestr(info,files[name])
        validate(tmp)
        # Publish by a same-filesystem exclusive hard-link operation.
        # A check-then-os.replace() can overwrite a concurrently created
        # output even when an earlier existence check appeared clear.
        try:
            os.link(tmp,target,follow_symlinks=False)
        except FileExistsError as exc:
            raise ValueError("Output already exists; refusing overwrite") from exc
        tmp.unlink()
        tmp=None
    finally:
        if tmp is not None:
            tmp.unlink(missing_ok=True)
    return {"archive_sha256":hashed(target.read_bytes()),"run_count":len(rows),
            "case_count":len(cases),"source_proof_included":False,
            "scientific_quality_validated":False}

def validate(path: Path) -> dict:
    if path.is_symlink() or not path.is_file() or path.stat().st_size>MAX_BYTES:
        raise ValueError("Archive missing, symlinked or oversized")
    with ZipFile(path,"r") as z:
        infos=z.infolist()
        names=[i.filename for i in infos]
        if len(names)!=len(set(names)) or set(names)!=ALL:
            raise ValueError("Unexpected or duplicate archive members")
        if any(i.file_size>MAX_BYTES or i.file_size<0 or i.is_dir() or
               (i.external_attr>>16)&0o170000==0o120000 for i in infos):
            raise ValueError("Unsupported archive members")
        data={name:z.read(name) for name in names}
    manifest=json.loads(data["MANIFEST.json"])
    if manifest.get("schema_version")!=1 or manifest.get("kind")!="REG-019_REPLAY_ARCHIVE" \
            or manifest.get("scientific_validity_proven") is not False \
            or manifest.get("external_fulltext_included") is not False \
            or set(manifest.get("files",{}))!=set(FILES):
        raise ValueError("Invalid archive manifest")
    if any(manifest["files"][f]!=hashed(data[f]) for f in FILES):
        raise ValueError("Archive member SHA-256 mismatch")
    catalog=json.loads(data["CASE_CATALOG.json"])
    cases=validate_catalog(catalog)
    protocol=json.loads(data["PROTOCOL.json"])
    obs=json.loads(data["OBSERVATIONS.json"])
    catalog_hash=hashed(canonical(catalog))
    if protocol.get("case_catalog_sha256")!=catalog_hash or \
       obs.get("case_catalog_sha256")!=catalog_hash or \
       protocol.get("case_count")!=len(cases):
        raise ValueError("Frozen case catalog and protocol are inconsistent")
    if protocol.get("independent_reviewer_authenticated") is not False or \
       protocol.get("scientific_validity_proven") is not False or \
       protocol.get("original_evidence_included") is not False or \
       obs.get("independent_scientific_validation") is not False or \
       obs.get("evidence_references_included") is not False or \
       obs.get("original_ledger_chain_reverifiable_from_this_redacted_package") is not False:
        raise ValueError("Unsupported scientific or provenance attestation")
    runs=obs.get("runs")
    if not isinstance(runs,list) or len(runs)>MAX_RUNS or obs.get("run_count")!=len(runs) \
            or obs.get("status")!=("USER_SUPPLIED_RUNS" if runs else "NO_OBSERVED_RUNS"):
        raise ValueError("Invalid observation run inventory")
    previous=None
    run_ids=set()
    for entry in runs:
        if not isinstance(entry,dict) or entry.get("run_id") in run_ids:
            raise ValueError("Invalid or duplicated run")
        run_ids.add(entry["run_id"])
        if not isinstance(entry.get("skill_commit"),str) or not SHA40.fullmatch(entry["skill_commit"]):
            raise ValueError("Run lacks an exact source revision")
        if entry.get("case_set_sha256")!=catalog_hash:
            raise ValueError("Run catalog hash differs")
        if (entry.get("previous_entry_sha256")!=previous or
            not isinstance(entry.get("original_ledger_entry_sha256"),str) or
            not SHA64.fullmatch(entry["original_ledger_entry_sha256"])):
            raise ValueError("Original ledger hash pointers are inconsistent")
        previous=entry["original_ledger_entry_sha256"]
        computed=score_one(cases,entry.get("cases"))
        if entry.get("score")!=computed:
            raise ValueError("Evaluation replay metrics disagree with observations")
    return {"archive_sha256":hashed(path.read_bytes()),"case_count":len(cases),
            "run_count":len(runs),"observed_total":sum(x["score"]["observed"] for x in runs),
            "replay_verified":True,"external_evidence_verified":False,
            "scientific_validity_proven":False}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="command",required=True)
    b=sub.add_parser("build")
    b.add_argument("--catalog",type=Path,required=True)
    b.add_argument("--ledger",type=Path)
    b.add_argument("--project",type=Path,help="Optional canonical protocol checksum only")
    b.add_argument("--output",type=Path,required=True)
    v=sub.add_parser("verify")
    v.add_argument("archive",type=Path)
    a=p.parse_args(argv)
    try:
        report=build(a.output,a.catalog,a.ledger,a.project) if a.command=="build" else validate(a.archive)
        print(json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False))
        return 0
    except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError,BadZipFile) as exc:
        print("EVALUATION_PACKAGE_ERROR: "+str(exc),file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
