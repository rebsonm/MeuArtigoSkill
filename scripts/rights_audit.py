#!/usr/bin/env python3
"""Conservative, offline document access and redistribution provenance guard.

No rights are inferred from a DOI, open URL, availability, deposited PDF, or a
researcher's access. A project record is an attestation, not legal verification.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

MGMT = "00_Gestao_e_Continuidade"
TRACKER = f"{MGMT}/04_FullText_Tracker.csv"
CORPUS = "03_Screening_e_FullText/FullText_Corpus"
COLUMNS = [
    "Access_basis", "Rights_basis", "License_URI", "Rights_evidence",
    "Permission_scope", "Attribution_text", "Source_sha256",
    "Rights_reviewed_by", "Rights_review_evidence",
]
ACCESS = {"OPEN_ACCESS","INSTITUTIONAL_ACCESS","PERSONAL_AUTHORIZED","DIRECT_PERMISSION","UNKNOWN"}
RIGHTS = {
    "UNKNOWN", "ALL_RIGHTS_RESERVED", "CC0_1_0", "CC_BY_4_0",
    "CC_BY_SA_4_0", "PUBLIC_DOMAIN", "DIRECT_PERMISSION",
    "INSTITUTIONAL_ACCESS", "PERSONAL_ACCESS",
}
OPEN_LICENSES = {
    "CC0_1_0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "CC_BY_4_0": "https://creativecommons.org/licenses/by/4.0/",
    "CC_BY_SA_4_0": "https://creativecommons.org/licenses/by-sa/4.0/",
}
RESTRICTED = {"UNKNOWN","ALL_RIGHTS_RESERVED","INSTITUTIONAL_ACCESS","PERSONAL_ACCESS"}
EXCLUDED_REVIEWERS = {"AI","LLM","CHATGPT","GPT","MODEL","AGENT"}
SAFE_EXT = {".pdf",".txt",".md",".html",".htm",".epub",".docx"}
MAX_BYTES = 150*1024*1024

def val(x): return " ".join(str(x or "").split())

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def tracker(root):
    file=Path(root)/TRACKER
    if not file.is_file():
        return [],[]
    with file.open("r",encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        columns=reader.fieldnames or []
        records=list(reader)
    if any(None in r for r in records):
        raise ValueError("Malformed full-text tracker rows")
    return columns,records

def local_file(root,value,*,require_corpus=True):
    root=Path(root).resolve()
    if not value or "://" in value or Path(value).is_absolute():
        raise ValueError("Source path must be project-relative, not an external URL")
    path=(root/value).resolve()
    corpus=(root/CORPUS).resolve()
    if not path.is_relative_to(root) or (require_corpus and not path.is_relative_to(corpus)):
        raise ValueError("Source path is outside the authorized full-text corpus")
    if not path.is_file() or path.is_symlink() or path.suffix.lower() not in SAFE_EXT:
        raise ValueError("Source is missing, symlinked or has an unsupported file type")
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("Source exceeds conservative size limit")
    return path

def source_inventory(root):
    dir=(Path(root).resolve()/CORPUS).resolve()
    if not dir.is_dir(): return []
    entries=[]
    for path in sorted(dir.rglob("*")):
        if path.is_symlink():
            raise ValueError("Symlink in full-text corpus is not eligible for external export")
        if path.is_file():
            if path.suffix.lower() not in SAFE_EXT:
                raise ValueError(f"Unrecognized full-text corpus artifact: {path.name}")
            if not path.resolve().is_relative_to(dir):
                raise ValueError("Full-text path escapes corpus")
            entries.append(path)
    return entries

def evidence_reference(text):
    s=val(text)
    # A meaningful source-specific publisher/repository page or project permission
    # record, not just the generic Creative Commons license description.
    if len(s)<16 or any(x in s.lower() for x in ["placeholder","to define","pending permission"]):
        return False
    if s.lower().startswith((
        "https://creativecommons.org/licenses/",
        "https://creativecommons.org/publicdomain/",
        "https://br.creativecommons.net/licencas",
    )):
        # A generic license deed does not prove that this particular article
        # or exact manuscript version is available under that license.
        return False
    return (s.startswith("https://") or s.startswith("permission:") or
            s.startswith("repository:") or s.startswith("document:"))

def evaluated_rights(row,root,*,for_export=False):
    rid=val(row.get("Record_ID")) or "UNKNOWN_RECORD"
    problems=[]
    basis=val(row.get("Rights_basis")).upper()
    access=val(row.get("Access_basis")).upper()
    source=val(row.get("File_or_URL"))
    if access not in ACCESS:
        problems.append("access basis is missing or unsupported")
    if basis not in RIGHTS:
        problems.append("rights basis is missing or unsupported")
    if not source or "://" in source:
        problems.append("no local source file associated with the record")
        return {"record_id":rid,"errors":problems,"eligible":False}
    try:
        path=local_file(root,source)
        actual=digest(path)
        sha=val(row.get("Source_sha256")).lower()
        if not re.fullmatch(r"[a-f0-9]{64}",sha) or sha!=actual:
            problems.append("source digest missing or inconsistent with local file")
    except (OSError,ValueError) as exc:
        problems.append(f"unsafe or inaccessible source ({type(exc).__name__})")
        path=None
        actual=None

    if for_export:
        if basis in RESTRICTED:
            problems.append("access alone does not authorize redistribution")
        if basis in OPEN_LICENSES and val(row.get("License_URI"))!=OPEN_LICENSES[basis]:
            problems.append("exact license URI required")
        if basis=="DIRECT_PERMISSION" and "PUBLIC_REDISTRIBUTION" not in {
            x.strip() for x in val(row.get("Permission_scope")).upper().split(";") if x.strip()
        }:
            problems.append("specific permission for public redistribution is not documented")
        if not evidence_reference(row.get("Rights_evidence")):
            problems.append("missing source-specific license or permission evidence")
        if basis not in {"CC0_1_0","PUBLIC_DOMAIN"} and not val(row.get("Attribution_text")):
            problems.append("source attribution or required notice is missing")
        reviewer=val(row.get("Rights_reviewed_by"))
        if not reviewer or reviewer.upper() in EXCLUDED_REVIEWERS:
            problems.append("no accountable human rights review attestation")
        if not evidence_reference(row.get("Rights_review_evidence")):
            problems.append("no source reference for rights review")
        if basis=="PUBLIC_DOMAIN" and not evidence_reference(row.get("Rights_evidence")):
            problems.append("public-domain assertion has no specific evidence")
    return {
        "record_id":rid,"path":source,"sha256":actual,
        "rights_basis":basis,"access_basis":access,
        "license_uri":val(row.get("License_URI")),
        "attribution":val(row.get("Attribution_text")),
        "rights_reference":val(row.get("Rights_evidence")),
        "errors":problems,"eligible":not problems,
    }

def authorize_external_fulltext(root):
    root=Path(root).resolve()
    files=source_inventory(root)
    if not files:
        raise ValueError("Cannot export a full-text corpus with no local documents")
    _,records=tracker(root)
    match={}
    for row in records:
        name=val(row.get("File_or_URL"))
        if not name or "://" in name:
            continue
        try: path=local_file(root,name)
        except (ValueError,OSError): continue
        match.setdefault(path,[]).append(row)
    decisions=[]
    errors=[]
    for path in files:
        rel=path.relative_to(root).as_posix()
        candidates=match.get(path,[])
        if len(candidates)!=1:
            errors.append(f"{rel}: needs exactly one Record_ID rights entry")
            continue
        assessment=evaluated_rights(candidates[0],root,for_export=True)
        if assessment["errors"]:
            errors.extend(f"{rel}: {issue}" for issue in assessment["errors"])
        else:
            decisions.append(assessment)
    if errors:
        raise ValueError("Full-text redistribution NOT authorized: "+"; ".join(errors[:10]))
    return decisions

def audit_project(root,strict=False):
    root=Path(root).resolve()
    _,records=tracker(root)
    errors,warnings=[],[]
    counts={"records":len(records),"local_files":0,"unknown_rights":0,
            "open_or_authorized_claims":0,"exportable_documents":0}
    seen=set()
    for row in records:
        name=val(row.get("File_or_URL"))
        if not name or "://" in name:
            continue
        try: path=local_file(root,name)
        except (OSError,ValueError) as exc:
            (errors if strict else warnings).append(
                f"{val(row.get('Record_ID')) or '?'}: local source unresolved ({type(exc).__name__})")
            continue
        counts["local_files"]+=1
        if path in seen:
            errors.append(f"{path.name}: multiple tracker rows for one local document")
        seen.add(path)
        basis=val(row.get("Rights_basis")).upper()
        if basis not in RIGHTS or basis in RESTRICTED:
            counts["unknown_rights"]+=1
            warnings.append(f"{val(row.get('Record_ID')) or '?'}: access does not imply redistribution")
        else:
            counts["open_or_authorized_claims"]+=1
            check=evaluated_rights(row,root,for_export=True)
            if check["eligible"]:
                counts["exportable_documents"]+=1
            else:
                errors.extend(f"{check['record_id']}: {s}" for s in check["errors"])
    # Source files can be used locally but cannot slip into an export as untracked.
    try:
        orphan=source_inventory(root)
        for path in orphan:
            if path not in seen:
                warnings.append(f"{path.name}: full-text file without a matching rights registry record")
    except ValueError as exc:
        errors.append(str(exc))
    return {"errors":errors,"warnings":warnings,"counts":counts,
            "rights_legally_verified":False,"local_access_proves_redistribution":False}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("project")
    p.add_argument("--strict",action="store_true")
    p.add_argument("--check-export",action="store_true")
    args=p.parse_args(argv)
    try:
        if args.check_export:
            outcome={"eligible":authorize_external_fulltext(args.project),
                     "automatic_legal_certification":False}
        else:
            outcome=audit_project(args.project,strict=args.strict)
        print(json.dumps(outcome,ensure_ascii=False,indent=2))
        return 1 if outcome.get("errors") else 0
    except (ValueError,OSError) as exc:
        print("ERROR: "+str(exc),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
