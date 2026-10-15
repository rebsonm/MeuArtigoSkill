#!/usr/bin/env python3
"""REG-013: compact, read-only scientific *diagnostic*, not a peer review.

Composes existing REG-018 and REG-011 results plus a limited protocol inventory.
No free-text research inputs, author identities or copyrighted passages appear
in the generated report. No scientific gate or Drive record is changed.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
from html import escape
import json
import os
from pathlib import Path
import re
import sys
import tempfile

from report_output_guard import write_report
from reference_audit import audit as audit_references
from semantic_claim_review import review as review_claims, local_json
from source_report_integrity import MGMT

LIMIT_FINDINGS = 6
LIMIT_ACTIONS = 4
MAX_LINE = 104
SAFE_ID = re.compile(r"(?:CLAIM|EVID|GATE|DEC|SEARCH|REC)-[0-9]{3,8}\Z")
PRIORITY = {
    "SOURCE_REPORT_STALE": 1, "UNTRUSTWORTHY_SOURCE_REPORT": 1,
    "SOURCE_METADATA_MISMATCH": 2, "SOURCE_LOCATOR_CONFLICT": 2,
    "UNKNOWN_REFERENCE": 2, "LITERATURE_CLAIM_WITHOUT_REFERENCE": 2,
    "CLAIM_MISSING_EVIDENCE_LINK": 2, "CLAIM_EVIDENCE_MISSING_OR_AMBIGUOUS": 2,
    "CLAIM_SOURCE_REPORT_UNAVAILABLE_OR_STALE": 2,
    "CLAIM_SOURCE_CHECK_MISSING_OR_AMBIGUOUS": 2,
    "CLAIM_QUOTED_PASSAGE_NOT_CONFIRMED": 2,
    "CLAIM_HUMAN_REVIEW_NOT_DECLARED": 3,
    "SOURCE_RETRACTION_ALERT": 3, "CLAIM_REVIEW_DECLARED_NOT_SUPPORTED": 3,
    "CLAIM_UNQUALIFIED_SUPPORT_CONTRADICTS_REVIEW": 3,
    "CLAIM_PENDING_HUMAN_REVIEW": 4, "SOURCE_REPORT_MISSING": 4,
    "CLAIM_POSSIBLE_SEMANTIC_OVERREACH": 3,
    "CLAIM_POSSIBLE_CONTEXTUAL_MISMATCH": 3,
    "METHODOLOGY_PROTOCOL_MISSING": 5,
}
HARD_CLAIM = {
    "MISSING_EVIDENCE_LINK", "EVIDENCE_MISSING_OR_AMBIGUOUS",
    "SOURCE_REPORT_UNAVAILABLE_OR_STALE", "SOURCE_CHECK_MISSING_OR_AMBIGUOUS",
    "QUOTED_PASSAGE_NOT_CONFIRMED", "REVIEW_BOUND_TO_STALE_OR_DIFFERENT_INPUT",
    "UNQUALIFIED_SUPPORT_CONTRADICTS_REVIEW",
}
HARD_DECLARED = {"NOT_SUPPORTED"}
# A lexical hint and a recorded but unauthenticated full-support
# declaration are non-blocking for *technical CLI execution* only.
# This does not certify semantics, a reviewer, or any scientific gate.
STRICT_ADVISORY_ONLY = {
    "CLAIM_POSSIBLE_SEMANTIC_OVERREACH",
    "CLAIM_POSSIBLE_CONTEXTUAL_MISMATCH",
    "CLAIM_REVIEW_DECLARED_SUPPORTED",
}
PROTOCOL = "01_Protocolo.csv"
SOURCE_INPUTS = ("05_Evidence_Matrix.csv", "09_Claims_Ledger.csv", "SOURCE_VERIFICATION.json", PROTOCOL)


def file_hash(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def fingerprints(root: Path) -> dict:
    return {name: file_hash(root / MGMT / name) for name in SOURCE_INPUTS}


def safe_id(value: str | None) -> str:
    return value if isinstance(value, str) and SAFE_ID.fullmatch(value) else "-"


def protocol_inventory(root: Path) -> dict:
    path = root / MGMT / PROTOCOL
    if not path.is_file() or path.is_symlink():
        return {"status": "NOT_AVAILABLE", "items": None, "pending": None,
                "methodological_validity_proven": False}
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not {"Item", "Decision", "Rationale", "Status"}.issubset(reader.fieldnames or []):
            raise ValueError("Canonical protocol has unexpected headers")
        rows = list(reader)
    if any(None in row for row in rows):
        raise ValueError("Malformed canonical protocol")
    pending = 0
    for row in rows:
        missing = any(not str(row.get(k) or "").strip()
                      for k in ("Item", "Decision", "Rationale", "Status"))
        state = str(row.get("Status") or "").upper().strip()
        if missing or state in {"", "PLANNED", "PENDING", "TO_DEFINE",
                               "DRAFT", "IN_PROGRESS", "INVALID", "SUPERSEDED"}:
            pending += 1
    return {"status": "EMPTY" if not rows else "RECORDED_UNASSESSED",
            "items": len(rows), "pending": pending,
            "methodological_validity_proven": False}


def _issue_bucket(bucket: dict, *, kind: str, code: str, severity: str,
                  identifier: str | None = None):
    key = (kind, code, severity)
    if key not in bucket:
        bucket[key] = {"kind": kind, "code": code, "severity": severity,
                       "count": 0, "sample_id": "-"}
    bucket[key]["count"] += 1
    candidate = safe_id(identifier)
    if candidate != "-" and (bucket[key]["sample_id"] == "-" or candidate < bucket[key]["sample_id"]):
        bucket[key]["sample_id"] = candidate


def compose(root: Path, *, assessments: dict | None = None) -> dict:
    root = Path(root).resolve()
    start = fingerprints(root)
    ref = audit_references(root)
    claim = review_claims(root, assessments)
    protocol = protocol_inventory(root)
    if fingerprints(root) != start:
        raise ValueError("Canonical inputs changed during diagnosis")
    if ref.get("semantic_support_proven") is not False or claim.get("semantic_support_proven") is not False:
        raise ValueError("Diagnostic received an invalid scientific-approval assertion")
    issues = {}
    for item in ref["findings"]:
        _issue_bucket(issues, kind="REFERENCE", code=str(item["code"]),
                      severity="BLOCK" if item["severity"] == "BLOCK" else "REVIEW",
                      identifier=item.get("claim_id") or item.get("evidence_id"))
    for item in claim["review_items"]:
        status = str(item.get("status") or "")
        declared = item.get("declared_judgment")
        if status == "HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED":
            code = ("CLAIM_REVIEW_DECLARED_" + declared) if declared in {
                "SUPPORTED", "PARTIALLY_SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE"
            } else "CLAIM_REVIEW_UNAUTHENTICATED"
            severity = "BLOCK" if declared in HARD_DECLARED else "REVIEW"
        else:
            code = "CLAIM_" + status
            severity = "BLOCK" if status in HARD_CLAIM else "REVIEW"
        _issue_bucket(issues, kind="CLAIM", code=code, severity=severity,
                      identifier=item.get("claim_id"))
        if item.get("semantic_risk_codes"):
            _issue_bucket(issues,kind="CLAIM",code="CLAIM_POSSIBLE_SEMANTIC_OVERREACH",
                          severity="REVIEW",identifier=item.get("claim_id"))
        if item.get("contextual_signal_codes"):
            _issue_bucket(issues,kind="CLAIM",code="CLAIM_POSSIBLE_CONTEXTUAL_MISMATCH",
                          severity="REVIEW",identifier=item.get("claim_id"))
    if protocol["status"] != "RECORDED_UNASSESSED":
        _issue_bucket(issues,kind="METHODOLOGY",
                      code="METHODOLOGY_PROTOCOL_MISSING" if protocol["status"] == "NOT_AVAILABLE"
                           else "METHODOLOGY_PROTOCOL_EMPTY",
                      severity="REVIEW")
    elif protocol["pending"]:
        _issue_bucket(issues,kind="METHODOLOGY",code="METHODOLOGY_RECORDS_PENDING",
                      severity="REVIEW")
        issues[("METHODOLOGY", "METHODOLOGY_RECORDS_PENDING", "REVIEW")]["count"] = protocol["pending"]
    full = sorted(issues.values(),
                  key=lambda x: (0 if x["severity"] == "BLOCK" else 1,
                                 PRIORITY.get(x["code"], 10),x["kind"],x["code"]))
    totals = Counter()
    for item in full:
        totals[item["severity"]] += item["count"]
    strict_required = sum(
        item["count"] for item in full
        if item["severity"] == "BLOCK" or item["code"] not in STRICT_ADVISORY_ONLY
    )
    # Provide actions grounded in actual recorded deficiencies, not findings
    # invented from research prose. The prose is constant, no AI generation.
    actions = []
    ref_block = any(x["severity"] == "BLOCK" and x["kind"] == "REFERENCE" for x in full)
    claim_block = any(x["severity"] == "BLOCK" and x["kind"] == "CLAIM" for x in full)
    if ref_block:
        actions.append("Resolve inconsistent identifiers, DOIs and source links.")
    if claim_block:
        actions.append("Reassess claims with missing or conflicting source passages.")
    if ref["source_report_status"] in {"MISSING","STALE","BLOCKED","REVIEW_REQUIRED"}:
        actions.append("Recheck source verification results and documented limitations.")
    if any(x["code"] == "CLAIM_POSSIBLE_CONTEXTUAL_MISMATCH" for x in full):
        actions.append("Compare contextual mismatch hints to the original source; record a human interpretation.")
    if any(x["code"] == "CLAIM_POSSIBLE_SEMANTIC_OVERREACH" for x in full):
        actions.append("Review possible claim overreach against the source and document a human judgment.")
    if any(x["kind"] == "CLAIM" for x in full):
        actions.append("Obtain documented human review, including counterevidence.")
    if protocol["status"] != "RECORDED_UNASSESSED" or protocol["pending"]:
        actions.append("Complete the protocol record and review methodological fit.")
    if not actions:
        actions.append("Seek substantive human scientific review; no alerts does not prove validity.")
    actions = actions[:LIMIT_ACTIONS]
    return {
        "schema_version": 1, "kind": "REG-013_TECHNICAL_SCIENTIFIC_DIAGNOSTIC",
        "verdict": "CORRECAO_REQUERIDA" if totals["BLOCK"] else "REVISAO_CIENTIFICA_PENDENTE",
        "counts": {"references": ref["evidence_count"], "claims": ref["claim_count"],
                   "claim_evidence_pairs": len(claim["review_items"]),
                   "blocking_occurrences": totals["BLOCK"],
                   "review_occurrences": totals["REVIEW"],
                   "strict_required_occurrences": strict_required,
                   "heuristic_advisory_occurrences": sum(
                       x["count"] for x in full
                       if x["code"] == "CLAIM_POSSIBLE_SEMANTIC_OVERREACH"),
                   "contextual_advisory_occurrences": sum(
                       x["count"] for x in full
                       if x["code"] == "CLAIM_POSSIBLE_CONTEXTUAL_MISMATCH"),
                   "findings_total": sum(x["count"] for x in full)},
        "source_verification": ref["source_report_status"],
        "protocol": protocol,
        "input_sha256": start,
        "source_report_sha256": ref.get("source_report_sha256"),
        "priority_findings": full[:LIMIT_FINDINGS],
        "omitted_finding_categories": max(len(full)-LIMIT_FINDINGS,0),
        "all_finding_categories": len(full),
        "actions": actions,
        "coverage": "CANONICAL_TABLES_ONLY; NO_MANUSCRIPT_TEXT_AUDIT",
        "scientific_quality_validated": False,
        "independent_peer_review_performed": False,
        "researcher_identity_authenticated": False,
        "semantic_entailment_automated": False,
        "drive_sync_verified": False,
    }


def _cells(data: dict) -> tuple[list[str],list[tuple[str,str,str]]]:
    lines = []
    for x in data["priority_findings"]:
        code = str(x["code"])[:48]
        lines.append((x["severity"], code+" ("+str(x["count"])+")",x["sample_id"]))
    if data["omitted_finding_categories"]:
        lines.append(("INFO","+"+str(data["omitted_finding_categories"])+" categories not shown","-"))
    return [],lines


def markdown(data: dict) -> str:
    c=data["counts"]; p=data["protocol"]
    _,rows = _cells(data)
    summary = ("**Status:** "+data["verdict"]+" | **Evidence:** "+
               str(c["references"])+" | **Claims:** "+str(c["claims"])+
               " | **Blocking occurrences:** "+str(c["blocking_occurrences"])+
               " | **Review items:** "+str(c["review_occurrences"]))
    proto = ("unavailable" if p["status"] == "NOT_AVAILABLE" else
             str(p["items"])+" items, "+str(p["pending"])+" pending")
    lines=[
        "# Meu Artigo — Scientific diagnostic (technical triage)",
        summary,
        "**Source report:** "+data["source_verification"]+
        " | **Protocol:** "+proto,
        "",
        "## Priority findings",
        "| Level | Finding (count) | Record |",
        "|---|---|---|",
    ]
    lines.extend("| "+str(a)+" | "+str(b)+" | "+str(v)+" |" for a,b,v in rows)
    if not rows:
        lines.append("| INFO | No structural findings recorded | - |")
    lines.extend(["", "## Next actions"])
    lines.extend(str(i+1)+". "+v for i,v in enumerate(data["actions"]))
    lines += ["","**Limits:** canonical-register triage only; full manuscript citations are not inspected,",
              "semantic support is not automated; method adequacy and human review are not authenticated.",
              "**Input hashes:** evidence "+str(data["input_sha256"]["05_Evidence_Matrix.csv"] or "-")[:12]+
              " | claims "+str(data["input_sha256"]["09_Claims_Ledger.csv"] or "-")[:12]+
              " | source "+str(data["source_report_sha256"] or "-")[:12]+
              " | protocol "+str(data["input_sha256"][PROTOCOL] or "-")[:12]+".",
              "**Purpose:** research-support diagnostic; not peer review, a gate approval, or scientific validation."]
    result="\n".join(lines)+"\n"
    # Hard cap both lines and characters: the compact representation is
    # designed to fit a typical single A4 page, but printing depends on fonts.
    if len(result.splitlines()) > 28 or len(result) > 3300:
        raise ValueError("Diagnostic exceeds compact one-page layout budget")
    return result


def html_page(data: dict) -> str:
    c=data["counts"];p=data["protocol"];_, rows=_cells(data)
    safe=lambda s: escape(str(s),quote=True)
    body="".join("<tr><td>"+safe(a)+"</td><td>"+safe(b)+"</td><td>"+safe(v)+"</td></tr>" for a,b,v in rows)
    if not body:
        body="<tr><td>INFO</td><td>No structural findings recorded</td><td>-</td></tr>"
    actions="".join("<li>"+safe(x)+"</li>" for x in data["actions"])
    protocol=("unavailable" if p["status"] == "NOT_AVAILABLE" else
              str(p["items"])+" items; "+str(p["pending"])+" pending")
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<title>Meu Artigo - Technical diagnostic</title><style>'
        '@page{size:A4;margin:13mm}*{box-sizing:border-box}'
        'body{font-family:Arial,Helvetica,sans-serif;font-size:10pt;line-height:1.3;'
        'color:#1a2733;max-width:184mm;margin:auto}h1{font-size:16pt;margin:0 0 7mm}'
        'h2{font-size:11pt;margin:5mm 0 2mm}p{margin:2mm 0}'
        'table{border-collapse:collapse;width:100%;table-layout:fixed}'
        'td,th{border-bottom:1px solid #ced6db;padding:2mm;text-align:left;'
        'overflow-wrap:anywhere;font-size:9pt}th:first-child,td:first-child{width:17%}'
        'th:last-child,td:last-child{width:19%}li{margin:1mm 0}'
        '.small{font-size:8pt;color:#354957}.meta{background:#f3f6f7;padding:3mm}'
        'section{break-inside:avoid}</style></head><body>'
        '<h1>Meu Artigo — Scientific diagnostic</h1>'
        '<p class="small">Technical register triage, not independent scientific or editorial review.</p>'
        '<section class="meta"><b>Status:</b> '+safe(data["verdict"])+
        '<br><b>Evidence:</b> '+str(c["references"])+
        ' &nbsp; <b>Claims:</b> '+str(c["claims"])+
        ' &nbsp; <b>Blockers:</b> '+str(c["blocking_occurrences"])+
        ' &nbsp; <b>Review items:</b> '+str(c["review_occurrences"])+
        '<br><b>Sources:</b> '+safe(data["source_verification"])+
        ' &nbsp; <b>Protocol:</b> '+safe(protocol)+'</section>'
        '<section><h2>Priority findings</h2><table><thead><tr>'
        '<th>Level</th><th>Finding (count)</th><th>Record</th></tr></thead><tbody>'
        +body+'</tbody></table></section><section><h2>Next actions</h2><ol>'+
        actions+'</ol></section><section class="small"><p>'
        '<b>Limits:</b> no complete-manuscript citation audit, '
        'automated semantic support checking, or methodological validation.'
        '</p><p><b>Source SHA:</b> '+safe(str(data["source_report_sha256"] or "-")[:12])+
        ' &nbsp; <b>Evidence SHA:</b> '+
        safe(str(data["input_sha256"]["05_Evidence_Matrix.csv"] or "-")[:12])+
        ' &nbsp; <b>Claim SHA:</b> '+
        safe(str(data["input_sha256"]["09_Claims_Ledger.csv"] or "-")[:12])+
        '</p><p>Scientific decisions and gates remain under human control.</p>'
        '</section></body></html>\n'
    )


def output_file(root: Path, target: Path, result: str, assessment_path: Path | None):
    write_report(root, target, result,
                 allowed_extensions=frozenset({".json", ".md", ".html"}))


def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_path")
    parser.add_argument("--assessments",type=Path,help="Optional explicitly declared human review JSON")
    parser.add_argument("--format",choices=("markdown","html","json"),default="markdown")
    parser.add_argument("--output",type=Path,help="Local optional output; never an implied Drive write")
    parser.add_argument("--strict",action="store_true",help="2 if required technical checks/reviews remain unresolved; advisory-only findings do not fail")
    args=parser.parse_args(argv)
    try:
        root=Path(args.project_path).resolve()
        reviews=local_json(root,args.assessments) if args.assessments else None
        result=compose(root,assessments=reviews)
        content=markdown(result) if args.format=="markdown" else html_page(result) if args.format=="html" else json.dumps(result,ensure_ascii=False,indent=2)+"\n"
        if args.output:
            output_file(root,args.output,content,(root/args.assessments) if args.assessments else None)
        else:
            print(content,end="")
        if args.strict and result["counts"]["strict_required_occurrences"]:
            return 2
        # Lack of flagged issues still cannot establish scientific quality.
        return 0
    except (ValueError,OSError,csv.Error,json.JSONDecodeError) as exc:
        print("DIAGNOSTIC_ERROR: "+str(exc),file=sys.stderr)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
