#!/usr/bin/env python3
"""Separate AI screening suggestions from researcher's accountable decisions.

Standard library only. No invented second reviewer, final AI exclusion, or
silent promotion of an AI suggestion to an eligibility decision.
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

SCREENING = "00_Gestao_e_Continuidade/03_Screening.csv"
STAGES = {
    "pass1": {"prefix": "Pass1", "options": {"INCLUDE", "BORDERLINE", "EXCLUDE"}},
    "pass2": {"prefix": "Pass2", "options": {"FULL TEXT — CORE", "FULL TEXT — SUPPORT", "EXCLUDE"}},
}
EXTRA_COLUMNS = [
    f"{stage}_{name}"
    for stage in ("Pass1", "Pass2")
    for name in ("AI_proposal", "AI_reason", "AI_source", "reviewed_by",
                 "review_evidence", "disagreement_reason")
]
INVALID_REVIEWERS = {"ai", "agent", "chatgpt", "model", "llm", "gpt", "human ai", "human+ai"}
INVALID_EVIDENCE = {"ok", "yes", "approved", "aprovado", "sim", "concordo", "validated", "reviewed"}


def clean(s):
    return " ".join(str(s or "").split())


def canonical(value):
    value=clean(value).upper().replace(" - ", " — ")
    return value


def real_review_reference(value):
    return len(clean(value)) >= 12 and clean(value).lower() not in INVALID_EVIDENCE


def substantive(value):
    return len(clean(value)) >= 20 and len(clean(value).split()) >= 3


def read_table(project):
    project = Path(project).resolve()
    file = project / SCREENING
    if not file.is_file():
        raise ValueError("Canonical screening CSV is not present")
    with file.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        columns = reader.fieldnames or []
        data = list(reader)
    if "Record_ID" not in columns or len(columns) != len(set(columns)):
        raise ValueError("Screening CSV has no unique Record_ID column")
    if any(None in row for row in data):
        raise ValueError("Malformed CSV rows with unexpected extra columns")
    return file, columns, data


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1024*1024), b""):
            h.update(part)
    return h.hexdigest()


def write_atomic(file, columns, rows):
    columns = [*columns, *(h for h in EXTRA_COLUMNS if h not in columns)]
    fd, temp_name = tempfile.mkstemp(prefix=".screening-", suffix=".csv", dir=str(file.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=columns)
            writer.writeheader()
            writer.writerows([{key: row.get(key) or "" for key in columns} for row in rows])
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, file)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def selected(rows, record_id):
    result=[row for row in rows if clean(row.get("Record_ID")) == record_id]
    if len(result)!=1:
        raise ValueError("Record_ID is missing or duplicated in screening data")
    return result[0]


def eligible_stage(row, stage):
    if stage == "pass2" and canonical(row.get("Pass1_decision")) not in {"INCLUDE", "BORDERLINE"}:
        raise ValueError("Pass2 requires a reviewed retained or borderline Pass1 decision")


def register_proposal(args):
    file, columns, rows = read_table(args.project)
    row = selected(rows, args.record_id)
    stage = STAGES[args.stage]
    prefix = stage["prefix"]
    proposal = canonical(args.proposal)
    if proposal not in stage["options"]:
        raise ValueError("Unsupported AI screening suggestion")
    if not substantive(args.reason) or not real_review_reference(args.source):
        raise ValueError("AI proposal requires substantive reasoning and a traceable source reference")
    eligible_stage(row, args.stage)
    if clean(row.get(f"{prefix}_decision")):
        raise ValueError("Cannot add an AI proposal after a final human decision")
    if clean(row.get(f"{prefix}_AI_proposal")):
        raise ValueError("Existing AI proposal is immutable; document a revision separately")
    before = sha256(file)
    row[f"{prefix}_AI_proposal"] = proposal
    row[f"{prefix}_AI_reason"] = clean(args.reason)
    row[f"{prefix}_AI_source"] = clean(args.source)
    write_atomic(file, columns, rows)
    print(json.dumps({"Record_ID": args.record_id, "stage":args.stage, "outcome":"AI_PROPOSAL_ONLY",
                      "human_decision_recorded":False, "sha256_before":before,
                      "sha256_after":sha256(file)}))
    return 0


def register_human_decision(args):
    file, columns, rows = read_table(args.project)
    row=selected(rows, args.record_id)
    config=STAGES[args.stage]
    prefix=config["prefix"]
    decision=canonical(args.decision)
    if decision not in config["options"]:
        raise ValueError("Unsupported final screening decision")
    eligible_stage(row, args.stage)
    if clean(row.get(f"{prefix}_decision")):
        raise ValueError("Existing final decision is immutable; revise through a documented protocol/decision event")
    if not clean(args.reviewer) or clean(args.reviewer).lower() in INVALID_REVIEWERS:
        raise ValueError("Final decisions require attribution to an actual human reviewer")
    if not real_review_reference(args.evidence):
        raise ValueError("Human review requires an external source reference to the actual response")
    if not substantive(args.reason):
        raise ValueError("Human decision requires a substantive reason, including exclusions")
    proposal=canonical(row.get(f"{prefix}_AI_proposal"))
    if proposal and proposal != decision and not substantive(args.disagreement_reason):
        raise ValueError("AI-human disagreement requires a substantive resolution reason")
    before=sha256(file)
    row[f"{prefix}_decision"]=decision
    row[f"{prefix}_reason"]=clean(args.reason)
    row[f"{prefix}_reviewed_by"]=clean(args.reviewer)
    row[f"{prefix}_review_evidence"]=clean(args.evidence)
    row[f"{prefix}_disagreement_reason"]=clean(args.disagreement_reason) if proposal!=decision else ""
    write_atomic(file,columns,rows)
    print(json.dumps({"Record_ID":args.record_id, "stage":args.stage, "outcome":"HUMAN_DECISION_RECORDED",
                      "disagreement": bool(proposal and proposal != decision),
                      "human_identity_authenticated":False,
                      "sha256_before":before,"sha256_after":sha256(file)}))
    return 0


def audit_rows(rows, *, enforce=False, freeze=False, headers=None):
    """Return deterministic data integrity findings; never infer actual human identity."""
    errors, warnings = [], []
    stats = {"records":0,"ai_suggestions":0,"unreviewed_suggestions":0,
             "recorded_pass1":0,"recorded_pass2":0,"recorded_exclusions":0,
             "disagreements":0,"unresolved_at_freeze":0}
    seen=set()
    if enforce and headers is not None:
        missing=[x for x in EXTRA_COLUMNS if x not in headers]
        if missing and rows:
            errors.append("screening CSV missing provenance columns: " + ", ".join(missing))
    for i,row in enumerate(rows,2):
        rid=clean(row.get("Record_ID"))
        if not rid:
            errors.append(f"screening row {i}: Record_ID is missing")
            continue
        if rid in seen:
            errors.append(f"screening row {i}: duplicate Record_ID {rid}")
            continue
        seen.add(rid)
        stats["records"]+=1
        is_duplicate=canonical(row.get("Duplicate_status")) in {
            "DUPLICATE", "EXACT_DUPLICATE", "NEAR_DUPLICATE_CONFIRMED"}
        p1=canonical(row.get("Pass1_decision"))
        p2=canonical(row.get("Pass2_decision"))
        if p1 and p1 not in STAGES["pass1"]["options"]:
            errors.append(f"{rid}: invalid Pass1 decision")
        if p2 and p2 not in STAGES["pass2"]["options"]:
            errors.append(f"{rid}: invalid Pass2 decision")
        if p2 and p1 not in {"INCLUDE","BORDERLINE"}:
            errors.append(f"{rid}: Pass2 recorded without a retained Pass1")
        if is_duplicate and not clean(row.get("Canonical_record_id")):
            errors.append(f"{rid}: duplicate status lacks canonical record reference")
        for stage,info in STAGES.items():
            prefix=info["prefix"]
            ai=canonical(row.get(f"{prefix}_AI_proposal"))
            final=canonical(row.get(f"{prefix}_decision"))
            reviewer=clean(row.get(f"{prefix}_reviewed_by"))
            evidence=clean(row.get(f"{prefix}_review_evidence"))
            reason=clean(row.get(f"{prefix}_reason"))
            ai_reason=clean(row.get(f"{prefix}_AI_reason"))
            ai_source=clean(row.get(f"{prefix}_AI_source"))
            conflict=clean(row.get(f"{prefix}_disagreement_reason"))
            if ai and stage=="pass2" and p1 not in {"INCLUDE","BORDERLINE"}:
                errors.append(f"{rid} pass2: AI proposal cannot bypass retained Pass1 review")
            if ai:
                stats["ai_suggestions"]+=1
                if ai not in info["options"] or not substantive(ai_reason) or not real_review_reference(ai_source):
                    errors.append(f"{rid} {stage}: AI proposal lacks source/valid reason or has invalid decision")
            elif ai_reason or ai_source:
                errors.append(f"{rid} {stage}: orphan AI explanation or source without proposal")
            if final:
                if stage=="pass1":stats["recorded_pass1"]+=1
                else:stats["recorded_pass2"]+=1
                if final=="EXCLUDE":stats["recorded_exclusions"]+=1
                if enforce and (not reviewer or reviewer.lower() in INVALID_REVIEWERS
                                or not real_review_reference(evidence) or not substantive(reason)):
                    errors.append(f"{rid} {stage}: final decision without human review evidence and substantive reason")
                if ai and ai!=final:
                    stats["disagreements"]+=1
                    if not substantive(conflict):
                        errors.append(f"{rid} {stage}: AI-human disagreement has no documented resolution")
                elif conflict:
                    warnings.append(f"{rid} {stage}: disagreement reason exists without a divergence")
            else:
                if reviewer or evidence or conflict:
                    errors.append(f"{rid} {stage}: review attribution without final decision")
                if ai:
                    stats["unreviewed_suggestions"]+=1
        if freeze and not is_duplicate and (not p1 or (p1 in {"INCLUDE","BORDERLINE"} and not p2)):
            stats["unresolved_at_freeze"]+=1
            errors.append(f"{rid}: corpus freeze requires reviewed decisions across applicable screening passes")
        if p1=="BORDERLINE" and not p2:
            warnings.append(f"{rid}: borderline record pending Pass2 assessment")
    if freeze and (stats["records"] == 0 or all(
        canonical(r.get("Duplicate_status")) in
        {"DUPLICATE","EXACT_DUPLICATE","NEAR_DUPLICATE_CONFIRMED"}
        for r in rows
    )):
        errors.append("corpus freeze requires at least one nonduplicate screening record")
    return {"errors":errors,"warnings":warnings,"counts":stats}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="command",required=True)
    common=argparse.ArgumentParser(add_help=False)
    common.add_argument("project")
    common.add_argument("--stage",required=True,choices=sorted(STAGES))
    common.add_argument("--record-id",required=True)
    propose=sub.add_parser("propose",parents=[common])
    propose.add_argument("--proposal",required=True)
    propose.add_argument("--reason",required=True)
    propose.add_argument("--source",required=True)
    decide=sub.add_parser("decide",parents=[common])
    decide.add_argument("--decision",required=True)
    decide.add_argument("--reason",required=True)
    decide.add_argument("--reviewer",required=True)
    decide.add_argument("--evidence",required=True)
    decide.add_argument("--disagreement-reason",default="")
    audit=sub.add_parser("audit")
    audit.add_argument("project")
    audit.add_argument("--strict",action="store_true")
    audit.add_argument("--freeze",action="store_true")
    args=parser.parse_args(argv)
    try:
        if args.command=="propose":
            return register_proposal(args)
        if args.command=="decide":
            return register_human_decision(args)
        file,headers,rows=read_table(args.project)
        report=audit_rows(rows,enforce=args.strict,freeze=args.freeze,headers=headers)
        print(json.dumps(report,ensure_ascii=False,indent=2))
        return 1 if report["errors"] else 0
    except (ValueError,OSError,csv.Error) as exc:
        print("ERROR: "+str(exc),file=sys.stderr)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
