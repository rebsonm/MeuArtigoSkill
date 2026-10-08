#!/usr/bin/env python3
"""Audit outgoing artifacts for anonymization and metadata leakage.

For EXTERNAL_ANONYMIZED artifacts, release requires both:
1. no configured identity/sensitive-content leak; and
2. no nonessential descriptive/provenance metadata such as author, creator,
   producer, generator, application, dates, comments, revision authorship,
   embedded paths, XMP/EXIF/IPTC or similar file properties.

The audit does not silently clean files. Use sanitize_metadata.py first, then
run this audit on the exact outgoing files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

MGMT="00_Gestao_e_Continuidade"
PROFILE_REL=Path(MGMT)/"ANONYMIZATION_PROFILE.json"
DEFAULT_OUT_REL=Path("06_Submissao")/"Anonimizacao"

TEXT_EXTS={".md",".txt",".csv",".json",".yaml",".yml",".xml",".html",".htm",".tex",".rst"}
OOXML_EXTS={".docx",".xlsx",".pptx",".docm",".xlsm",".pptm"}
VISUAL_EXTS={".pdf",".png",".jpg",".jpeg",".webp",".tif",".tiff",".svg"}
PNG_META={b"tEXt",b"zTXt",b"iTXt",b"eXIf",b"tIME"}
JPEG_META_MARKERS={0xE1:"APP1_EXIF_XMP",0xED:"APP13_IPTC",0xFE:"COMMENT"}
META_ATTRS={"author","initials","date","dateutc","lastmodifiedby","userid","authorid","creator"}
GENERATOR_COMMENT=re.compile(r"(?:generated|generator|created with|produced by|python|matplotlib|reportlab|pypdf|libreoffice|openoffice)",re.I)

GENERIC_PATTERNS=[
    ("EMAIL",re.compile(r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])",re.I),"HIGH"),
    ("ORCID",re.compile(r"\b\d{4}-\d{4}-\d{4}-\d{3}[\dX]\b",re.I),"HIGH"),
    ("CPF_LIKE",re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),"HIGH"),
    ("PHONE_BR",re.compile(r"(?<!\d)(?:\+?55\s*)?(?:\(?\d{2}\)?\s*)?9?\d{4}[-\s]?\d{4}(?!\d)"),"MEDIUM"),
    ("LOCAL_PATH_WINDOWS",re.compile(r"\b[A-Z]:\\(?:Users|Documents and Settings)\\[^\s<>\"']+",re.I),"HIGH"),
    ("LOCAL_PATH_MAC",re.compile(r"/Users/[^/\s]+/"),"HIGH"),
    ("LOCAL_PATH_LINUX",re.compile(r"/home/[^/\s]+/"),"HIGH"),
    ("PRIVATE_CLOUD_LINK",re.compile(r"https?://(?:drive|docs)\.google\.com/[^\s)\]>]+",re.I),"MEDIUM"),
]

PROFILE_SEVERITY={
    "author_names":"MEDIUM","name_variants":"MEDIUM","emails":"HIGH","orcids":"HIGH",
    "affiliations":"HIGH","departments_units":"HIGH","institutional_identifiers":"HIGH",
    "case_site_names":"MEDIUM","participant_identifiers":"HIGH","account_usernames":"HIGH",
    "local_path_tokens":"HIGH","custom_terms":"MEDIUM",
}

def load_profile(root:Path)->dict:
    path=root/PROFILE_REL
    if not path.exists(): raise SystemExit(f"missing anonymization profile: {path}")
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: raise SystemExit(f"invalid anonymization profile: {exc}")

def configured_terms(profile:dict):
    out=[]; groups=profile.get("sensitive_terms") or {}
    if not isinstance(groups,dict): return out
    for category,values in groups.items():
        if not isinstance(values,list): continue
        sev=PROFILE_SEVERITY.get(category,"MEDIUM")
        for idx,value in enumerate(values,1):
            value=str(value or "").strip()
            if len(value)>=3: out.append((category,idx,value,sev))
    return out

def add_finding(findings,*,file:Path,kind:str,severity:str,location:str,token_label:str=""):
    findings.append({"file":file.as_posix(),"kind":kind,"severity":severity,
                     "location":location,"token_label":token_label})

def scan_text(text:str,file:Path,findings,terms,location="content"):
    for kind,pattern,severity in GENERIC_PATTERNS:
        for _ in pattern.finditer(text):
            add_finding(findings,file=file,kind=kind,severity=severity,location=location)
    lowered=text.casefold()
    for category,idx,value,severity in terms:
        if value.casefold() in lowered:
            add_finding(findings,file=file,kind="PROFILE_TERM",severity=severity,
                        location=location,token_label=f"{category}[{idx}]")

def scan_filename(file,findings,terms):
    scan_text(file.name,file,findings,terms,location="filename")

def lname(name:str)->str:
    return name.rsplit("}",1)[-1].rsplit(":",1)[-1].lower()

def scan_ooxml(file:Path,findings,terms,manual,blocking_errors):
    try:
        with zipfile.ZipFile(file) as z:
            for info in z.infolist():
                name=info.filename; low=name.lower()
                if low.startswith("docprops/"):
                    add_finding(findings,file=file,kind="OOXML_DOCUMENT_PROPERTIES_PRESENT",
                                severity="HIGH",location=f"package:{name}")
                if info.comment or info.extra:
                    add_finding(findings,file=file,kind="ZIP_ENTRY_METADATA_PRESENT",
                                severity="HIGH",location=f"package:{name}")
                # Non-normalized timestamps can disclose generation/edit time.
                if tuple(info.date_time)!=(1980,1,1,0,0,0):
                    add_finding(findings,file=file,kind="ZIP_TIMESTAMP_METADATA_PRESENT",
                                severity="HIGH",location=f"package:{name}")
                if not (low.endswith(".xml") or low.endswith(".rels")):
                    continue
                raw=z.read(name); text=raw.decode("utf-8",errors="replace")
                scan_text(text,file,findings,terms,location=f"package:{name}")
                if "comments" in low or "commentauthors" in low:
                    add_finding(findings,file=file,kind="COMMENTS_OR_COMMENT_METADATA_PRESENT",
                                severity="HIGH",location=f"package:{name}")
                if low.endswith(".xml"):
                    try:
                        root=ET.fromstring(raw)
                        for elem in root.iter():
                            for key in elem.attrib:
                                if lname(key) in META_ATTRS and str(elem.attrib.get(key) or "").strip():
                                    add_finding(findings,file=file,kind="REVISION_OR_AUTHOR_METADATA_PRESENT",
                                                severity="HIGH",location=f"package:{name}",
                                                token_label=lname(key))
                    except Exception:
                        pass
                if re.search(r"file://|target=\"(?:[A-Z]:\\|/Users/|/home/)",text,re.I):
                    add_finding(findings,file=file,kind="EMBEDDED_LOCAL_PATH",
                                severity="HIGH",location=f"package:{name}")
            if z.comment:
                add_finding(findings,file=file,kind="ZIP_ARCHIVE_COMMENT_PRESENT",
                            severity="HIGH",location="zip_comment")
    except Exception as exc:
        blocking_errors.append(f"{file.name}: OOXML package could not be deterministically inspected: {exc}")

def scan_pdf(file:Path,findings,terms,manual,blocking_errors):
    try:
        from pypdf import PdfReader
    except Exception:
        blocking_errors.append(f"{file.name}: pypdf unavailable; PDF metadata cannot be deterministically verified")
        manual.append({"file":file.as_posix(),"reason":"PDF still requires human visual review for visible/rasterized identifiers."})
        return
    try:
        reader=PdfReader(str(file))
        metadata=reader.metadata or {}
        for key,value in metadata.items():
            if str(value or "").strip():
                add_finding(findings,file=file,kind="PDF_DOCUMENT_METADATA_PRESENT",
                            severity="HIGH",location="pdf_info",token_label=str(key))
        root=reader.trailer.get("/Root")
        try:
            root_obj=root.get_object() if root is not None else {}
        except Exception:
            root_obj={}
        for key in ("/Metadata","/PieceInfo","/SpiderInfo"):
            try:
                if root_obj and root_obj.get(key) is not None:
                    add_finding(findings,file=file,kind="PDF_EMBEDDED_METADATA_PRESENT",
                                severity="HIGH",location="pdf_catalog",token_label=key)
            except Exception:
                pass
        if reader.trailer.get("/ID") is not None:
            add_finding(findings,file=file,kind="PDF_DOCUMENT_ID_PRESENT",
                        severity="HIGH",location="pdf_trailer")
        for i,page in enumerate(reader.pages,1):
            text=page.extract_text() or ""
            scan_text(text,file,findings,terms,location=f"pdf_page:{i}")
            try:
                if page.get("/Metadata") is not None:
                    add_finding(findings,file=file,kind="PDF_PAGE_METADATA_PRESENT",
                                severity="HIGH",location=f"pdf_page:{i}")
            except Exception:
                pass
    except Exception as exc:
        blocking_errors.append(f"{file.name}: PDF parsing failed; metadata status is unverified: {exc}")
    manual.append({"file":file.as_posix(),"reason":"PDF requires human visual review for visible/rasterized identifiers even after deterministic metadata inspection."})

def png_chunks(data:bytes):
    if not data.startswith(b"\x89PNG\r\n\x1a\n"): raise ValueError("not a PNG")
    pos=8
    while pos+12<=len(data):
        ln=struct.unpack(">I",data[pos:pos+4])[0]; typ=data[pos+4:pos+8]; end=pos+12+ln
        if end>len(data): raise ValueError("truncated PNG")
        yield typ,data[pos+8:pos+8+ln]
        pos=end
        if typ==b"IEND": break

def scan_png(file,findings,blocking_errors):
    try:
        for typ,_ in png_chunks(file.read_bytes()):
            if typ in PNG_META:
                add_finding(findings,file=file,kind="IMAGE_METADATA_PRESENT",
                            severity="HIGH",location="png_chunk",token_label=typ.decode("ascii"))
    except Exception as exc:
        blocking_errors.append(f"{file.name}: PNG metadata inspection failed: {exc}")

def scan_jpeg(file,findings,blocking_errors):
    try:
        data=file.read_bytes()
        if not data.startswith(b"\xff\xd8"): raise ValueError("not a JPEG")
        pos=2
        while pos<len(data):
            if data[pos]!=0xFF: break
            while pos<len(data) and data[pos]==0xFF: pos+=1
            if pos>=len(data): break
            marker=data[pos]; pos+=1
            if marker in {0xD8,0xD9} or 0xD0<=marker<=0xD7 or marker==0x01:
                if marker==0xD9: break
                continue
            if pos+2>len(data): raise ValueError("truncated JPEG marker")
            seglen=struct.unpack(">H",data[pos:pos+2])[0]; end=pos+seglen
            if end>len(data): raise ValueError("truncated JPEG segment")
            if marker in JPEG_META_MARKERS:
                add_finding(findings,file=file,kind="IMAGE_METADATA_PRESENT",
                            severity="HIGH",location="jpeg_segment",
                            token_label=JPEG_META_MARKERS[marker])
            pos=end
            if marker==0xDA: break
    except Exception as exc:
        blocking_errors.append(f"{file.name}: JPEG metadata inspection failed: {exc}")

def scan_svg(file,findings,terms,manual):
    text=file.read_text(encoding="utf-8",errors="replace")
    scan_text(text,file,findings,terms,location="svg_source")
    if re.search(r"<metadata\b",text,re.I):
        add_finding(findings,file=file,kind="SVG_METADATA_PRESENT",severity="HIGH",location="svg_metadata")
    for m in re.finditer(r"<!--(.*?)-->",text,re.S):
        if GENERATOR_COMMENT.search(m.group(1)):
            add_finding(findings,file=file,kind="GENERATOR_METADATA_PRESENT",
                        severity="HIGH",location="svg_comment")
    manual.append({"file":file.as_posix(),"reason":"SVG requires human visual review for visible identifiers."})

def scan_other_image(file,findings,manual,blocking_errors):
    try:
        from PIL import Image
    except Exception:
        blocking_errors.append(f"{file.name}: image metadata parser unavailable; metadata status is unverified")
        manual.append({"file":file.as_posix(),"reason":"Image requires human visual review for visible identifiers."})
        return
    try:
        with Image.open(file) as im:
            try:
                if im.getexif() and len(im.getexif())>0:
                    add_finding(findings,file=file,kind="IMAGE_EXIF_METADATA_PRESENT",
                                severity="HIGH",location="image_exif")
            except Exception:
                pass
            suspect={"exif","xmp","xml","comment","description","software","author","artist","title",
                     "datetime","date_time","creation_time","photoshop","iptc"}
            for key,value in (im.info or {}).items():
                if str(key).lower() in suspect and value not in (None,"",b""):
                    add_finding(findings,file=file,kind="IMAGE_METADATA_PRESENT",
                                severity="HIGH",location="image_info",token_label=str(key))
    except Exception as exc:
        blocking_errors.append(f"{file.name}: image metadata inspection failed: {exc}")
    manual.append({"file":file.as_posix(),"reason":"Image requires human visual review for visible identifiers."})

def collect_targets(targets):
    out=[]
    for raw in targets:
        p=Path(raw).resolve()
        if p.is_file(): out.append(p)
        elif p.is_dir(): out.extend(x for x in p.rglob("*") if x.is_file())
    return sorted(dict.fromkeys(out))

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("project",help="Canonical project root")
    ap.add_argument("targets",nargs="*",help="Files/directories to audit; defaults to 06_Submissao/Arquivos_Finais")
    ap.add_argument("--output-dir",default="",help="Audit report directory")
    ap.add_argument("--acknowledge-human-review",action="store_true",
                    help="Record that required visual/medium-risk review was completed by a human")
    args=ap.parse_args()

    root=Path(args.project).resolve()
    profile=load_profile(root); terms=configured_terms(profile)
    targets=args.targets or [str(root/"06_Submissao"/"Arquivos_Finais")]
    files=collect_targets(targets)
    findings=[]; manual=[]; blocking_errors=[]

    status=profile.get("status")
    if status not in {"VERIFIED","NOT_REQUIRED"}:
        blocking_errors.append("Anonymization profile must be VERIFIED or NOT_REQUIRED.")
    if status=="NOT_REQUIRED" and not str(profile.get("notes") or "").strip():
        blocking_errors.append("NOT_REQUIRED requires a rationale.")
    if not files:
        blocking_errors.append("No outgoing files found.")
        manual.append({"file":"","reason":"No outgoing files found in the requested audit scope."})

    fingerprints=[]
    for file in files:
        try:
            relative=file.relative_to(root).as_posix()
            fingerprints.append({"path":relative,"sha256":hashlib.sha256(file.read_bytes()).hexdigest()})
        except (ValueError,OSError):
            blocking_errors.append("Audit files must be readable and inside the project.")
        scan_filename(file,findings,terms)
        ext=file.suffix.lower()
        if ext in TEXT_EXTS:
            try: scan_text(file.read_text(encoding="utf-8",errors="replace"),file,findings,terms)
            except Exception as exc: blocking_errors.append(f"{file.name}: text file could not be read: {exc}")
        elif ext in OOXML_EXTS:
            scan_ooxml(file,findings,terms,manual,blocking_errors)
        elif ext==".pdf":
            scan_pdf(file,findings,terms,manual,blocking_errors)
        elif ext==".png":
            scan_png(file,findings,blocking_errors)
            manual.append({"file":file.as_posix(),"reason":"PNG requires human visual review for visible identifiers."})
        elif ext in {".jpg",".jpeg"}:
            scan_jpeg(file,findings,blocking_errors)
            manual.append({"file":file.as_posix(),"reason":"JPEG requires human visual review for visible identifiers."})
        elif ext==".svg":
            scan_svg(file,findings,terms,manual)
        elif ext in VISUAL_EXTS:
            scan_other_image(file,findings,manual,blocking_errors)
        else:
            blocking_errors.append(f"{file.name}: unsupported/binary format cannot be deterministically metadata-audited")

    high=[f for f in findings if f["severity"]=="HIGH"]
    medium=[f for f in findings if f["severity"]=="MEDIUM"]
    if high or blocking_errors:
        result="FAIL"
    elif (medium or manual) and not args.acknowledge_human_review:
        result="REVIEW_REQUIRED"
    elif medium or manual:
        result="PASS_WITH_HUMAN_REVIEW"
    else:
        result="PASS"

    report={
        "schema_version":"3.0",
        "metadata_policy":"ZERO_NONESSENTIAL_METADATA",
        "blocking_errors":blocking_errors,
        "file_manifest":fingerprints,
        "profile_sha256":hashlib.sha256((root/PROFILE_REL).read_bytes()).hexdigest(),
        "generated_at":datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "project":root.name,
        "profile_status":profile.get("status","TO_CONFIGURE"),
        "default_external_artifact_mode":profile.get("default_external_artifact_mode","ANONYMIZED"),
        "audit_scope":[str(Path(t)) for t in targets],
        "files_scanned":len(files),
        "high_risk_findings":len(high),
        "medium_risk_findings":len(medium),
        "manual_review_items":len(manual),
        "human_review_acknowledged":bool(args.acknowledge_human_review),
        "result":result,
        "findings":findings,
        "manual_review":manual,
        "note":"Sensitive literal values and metadata values are intentionally omitted from this report.",
    }

    outdir=Path(args.output_dir).resolve() if args.output_dir else root/DEFAULT_OUT_REL
    outdir.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    out=outdir/f"ANONYMIZATION_AUDIT_{stamp}.json"
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    print(f"anonymization_result={result}")
    print(f"metadata_policy={report['metadata_policy']}")
    print(f"files_scanned={len(files)}")
    print(f"high_risk_findings={len(high)}")
    print(f"medium_risk_findings={len(medium)}")
    print(f"manual_review_items={len(manual)}")
    print(f"report={out}")
    return 0 if result in {"PASS","PASS_WITH_HUMAN_REVIEW"} else 1

if __name__=="__main__":
    raise SystemExit(main())
