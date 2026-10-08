#!/usr/bin/env python3
"""Remove nonessential/descriptive metadata from external anonymized artifacts.

The sanitizer is intentionally conservative: it removes provenance/application
metadata without rewriting scientific content. When a format cannot be cleaned
safely, it fails instead of claiming that the file is metadata-free.

Supported:
- OOXML: DOCX/XLSX/PPTX and macro-enabled variants (document properties removed;
  package timestamps normalized; author/date attributes scrubbed where safe).
- PDF: Info dictionary, XMP metadata and document ID removed when pypdf is
  available. If pypdf is unavailable, sanitization fails.
- PNG/JPEG: descriptive metadata chunks/segments removed losslessly.
- SVG: metadata elements and generator comments removed.
- Plain text/CSV/JSON/YAML/HTML/TeX/RST: copied as-is because they have no
  embedded container metadata; visible content is still audited separately.

This script does not accept/reject tracked changes or silently delete comments
because those operations can change scientific content. The anonymization audit
will keep such files blocked until they are deliberately cleaned.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import struct
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

OOXML_EXTS={".docx",".xlsx",".pptx",".docm",".xlsm",".pptm"}
TEXT_EXTS={".md",".txt",".csv",".json",".yaml",".yml",".html",".htm",".tex",".rst"}
PNG_META={b"tEXt",b"zTXt",b"iTXt",b"eXIf",b"tIME"}
JPEG_META_MARKERS={0xE1,0xED,0xFE}  # APP1 (Exif/XMP), APP13 (IPTC), COM
META_REL_TOKENS=("core-properties","extended-properties","custom-properties")
META_ATTRS={"author","initials","date","dateutc","lastmodifiedby","userid","authorid","creator"}
REVISION_OR_COMMENT_TOKENS=("comments","commentauthors","persons","people")
XML_NS_REL="http://schemas.openxmlformats.org/package/2006/relationships"

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def local_name(name:str)->str:
    return name.rsplit("}",1)[-1].rsplit(":",1)[-1].lower()

def clean_xml_identity_attrs(data:bytes, part_name:str)->tuple[bytes,int]:
    if not part_name.lower().endswith(".xml"):
        return data,0
    try:
        root=ET.fromstring(data)
    except Exception:
        return data,0
    changed=0
    relevant=(
        part_name.startswith("word/") or
        part_name.startswith("ppt/") or
        part_name.startswith("xl/")
    )
    if not relevant:
        return data,0
    for elem in root.iter():
        for key in list(elem.attrib):
            if local_name(key) in META_ATTRS:
                del elem.attrib[key]
                changed+=1
    if not changed:
        return data,0
    return ET.tostring(root,encoding="utf-8",xml_declaration=True),changed

def clean_rels(data:bytes)->tuple[bytes,int]:
    try:
        root=ET.fromstring(data)
    except Exception:
        return data,0
    removed=0
    for child in list(root):
        target=(child.attrib.get("Target") or "").lower()
        typ=(child.attrib.get("Type") or "").lower()
        if target.startswith("docprops/") or any(t in typ for t in META_REL_TOKENS):
            root.remove(child); removed+=1
    if not removed:
        return data,0
    ET.register_namespace("",XML_NS_REL)
    return ET.tostring(root,encoding="utf-8",xml_declaration=True),removed

def clean_content_types(data:bytes)->tuple[bytes,int]:
    try:
        root=ET.fromstring(data)
    except Exception:
        return data,0
    removed=0
    for child in list(root):
        part=(child.attrib.get("PartName") or "").lower()
        if part.startswith("/docprops/"):
            root.remove(child); removed+=1
    if not removed:
        return data,0
    return ET.tostring(root,encoding="utf-8",xml_declaration=True),removed

def sanitize_ooxml(src:Path,dst:Path)->dict:
    actions=[]
    with zipfile.ZipFile(src,"r") as zin, zipfile.ZipFile(dst,"w",compression=zipfile.ZIP_DEFLATED) as zout:
        zout.comment=b""
        for info in zin.infolist():
            name=info.filename
            low=name.lower()
            if low.startswith("docprops/"):
                actions.append(f"removed:{name}")
                continue
            data=zin.read(name)
            if name=="_rels/.rels":
                data,n=clean_rels(data)
                if n: actions.append(f"removed_metadata_relationships:{n}")
            elif name=="[Content_Types].xml":
                data,n=clean_content_types(data)
                if n: actions.append(f"removed_metadata_content_types:{n}")
            elif low.endswith(".xml"):
                data,n=clean_xml_identity_attrs(data,name)
                if n: actions.append(f"scrubbed_identity_attributes:{name}:{n}")
            # ZIP timestamps/comments/extra fields can disclose tool/time provenance.
            zi=zipfile.ZipInfo(filename=name,date_time=(1980,1,1,0,0,0))
            zi.compress_type=zipfile.ZIP_DEFLATED
            zi.external_attr=info.external_attr
            zi.internal_attr=info.internal_attr
            zi.create_system=0
            zi.comment=b""
            zi.extra=b""
            zout.writestr(zi,data)
    return {"actions":actions or ["normalized_package_metadata"]}

def sanitize_pdf(src:Path,dst:Path)->dict:
    try:
        from pypdf import PdfReader,PdfWriter
    except Exception as exc:
        raise RuntimeError("PDF metadata sanitization requires pypdf; release must remain blocked without it") from exc
    reader=PdfReader(str(src))
    writer=PdfWriter()
    if hasattr(writer,"clone_document_from_reader"):
        writer.clone_document_from_reader(reader)
    else:
        for page in reader.pages:
            writer.add_page(page)
    root=getattr(writer,"_root_object",None)
    removed=[]
    if root is not None:
        for key in ("/Metadata","/PieceInfo","/SpiderInfo"):
            if key in root:
                root.pop(key,None); removed.append(key)
    for obj in list(getattr(writer,"_objects",[]) or []):
        try:
            for key in ("/Metadata","/PieceInfo","/SpiderInfo"):
                if key in obj:
                    obj.pop(key,None); removed.append(key)
        except Exception:
            pass
    # pypdf creates /Producer by default; remove the entire Info dictionary
    # instead of replacing values with another generator name.
    try:
        writer._info=None
    except Exception:
        pass
    try:
        writer._ID=None
    except Exception:
        pass
    with dst.open("wb") as f:
        writer.write(f)
    return {"actions":["removed_pdf_info_dictionary","removed_pdf_xmp_metadata","removed_pdf_document_id",*sorted(set(removed))]}

def png_chunks(data:bytes):
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("not a PNG")
    pos=8
    while pos+12<=len(data):
        length=struct.unpack(">I",data[pos:pos+4])[0]
        typ=data[pos+4:pos+8]
        end=pos+12+length
        if end>len(data):
            raise ValueError("truncated PNG")
        yield typ,data[pos:end]
        pos=end
        if typ==b"IEND":
            break

def sanitize_png(src:Path,dst:Path)->dict:
    data=src.read_bytes()
    kept=[b"\x89PNG\r\n\x1a\n"]
    removed=[]
    for typ,raw in png_chunks(data):
        if typ in PNG_META:
            removed.append(typ.decode("ascii"))
            continue
        kept.append(raw)
    dst.write_bytes(b"".join(kept))
    return {"actions":[f"removed_png_chunk:{x}" for x in removed] or ["no_descriptive_png_metadata_found"]}

def sanitize_jpeg(src:Path,dst:Path)->dict:
    data=src.read_bytes()
    if not data.startswith(b"\xff\xd8"):
        raise ValueError("not a JPEG")
    out=bytearray(data[:2]); pos=2; removed=[]
    while pos<len(data):
        if data[pos]!=0xFF:
            # Start of entropy-coded scan data; preserve remainder byte-for-byte.
            out.extend(data[pos:]); break
        start=pos
        while pos<len(data) and data[pos]==0xFF:
            pos+=1
        if pos>=len(data): break
        marker=data[pos]; pos+=1
        if marker in {0xD8,0xD9} or 0xD0<=marker<=0xD7 or marker==0x01:
            out.extend(data[start:pos])
            if marker==0xD9: break
            continue
        if pos+2>len(data):
            raise ValueError("truncated JPEG marker")
        seglen=struct.unpack(">H",data[pos:pos+2])[0]
        end=pos+seglen
        if end>len(data):
            raise ValueError("truncated JPEG segment")
        segment=data[start:end]
        if marker in JPEG_META_MARKERS:
            removed.append(f"0x{marker:02X}")
        else:
            out.extend(segment)
        pos=end
        if marker==0xDA:  # SOS: remainder includes entropy data and EOI.
            out.extend(data[pos:]); break
    dst.write_bytes(bytes(out))
    return {"actions":[f"removed_jpeg_metadata_segment:{x}" for x in removed] or ["no_descriptive_jpeg_metadata_found"]}

def sanitize_svg(src:Path,dst:Path)->dict:
    text=src.read_text(encoding="utf-8",errors="replace")
    before=text
    text=re.sub(r"<metadata\b[^>]*>.*?</metadata\s*>","",text,flags=re.I|re.S)
    text=re.sub(r"<!--.*?(?:generated|generator|created with|python|matplotlib|inkscape|libreoffice).*?-->","",text,flags=re.I|re.S)
    dst.write_text(text,encoding="utf-8")
    return {"actions":["removed_svg_metadata_or_generator_comments"] if text!=before else ["no_descriptive_svg_metadata_found"]}

def sanitize_one(src:Path,dst:Path)->dict:
    ext=src.suffix.lower()
    dst.parent.mkdir(parents=True,exist_ok=True)
    if ext in OOXML_EXTS:
        return sanitize_ooxml(src,dst)
    if ext==".pdf":
        return sanitize_pdf(src,dst)
    if ext==".png":
        return sanitize_png(src,dst)
    if ext in {".jpg",".jpeg"}:
        return sanitize_jpeg(src,dst)
    if ext==".svg":
        return sanitize_svg(src,dst)
    if ext in TEXT_EXTS:
        shutil.copyfile(src,dst)
        return {"actions":["plain_text_no_embedded_container_metadata"]}
    raise RuntimeError(f"unsupported format for deterministic metadata sanitization: {ext or '<none>'}")

def collect(targets:list[str])->list[Path]:
    out=[]
    for raw in targets:
        p=Path(raw).resolve()
        if p.is_file(): out.append(p)
        elif p.is_dir(): out.extend(x for x in p.rglob("*") if x.is_file())
    return sorted(dict.fromkeys(out))

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("targets",nargs="+",help="Files/directories to sanitize")
    ap.add_argument("--in-place",action="store_true",help="Replace each file atomically after successful sanitization")
    ap.add_argument("--output-dir",default="",help="Destination directory when not using --in-place")
    ap.add_argument("--report",default="",help="Optional JSON report path")
    args=ap.parse_args()
    files=collect(args.targets)
    if not files:
        print("metadata_sanitization=FAIL\nerror=no files found")
        return 1
    if not args.in_place and not args.output_dir:
        print("metadata_sanitization=FAIL\nerror=use --in-place or --output-dir")
        return 1

    report={"schema_version":"1.0","generated_at":datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "files":[],"errors":[]}
    outdir=Path(args.output_dir).resolve() if args.output_dir else None
    for src in files:
        before=sha256(src)
        try:
            if args.in_place:
                fd,tmp=tempfile.mkstemp(prefix=src.name+".sanitize-",suffix=src.suffix,dir=str(src.parent))
                os.close(fd); dst=Path(tmp)
            else:
                dst=outdir/src.name
            detail=sanitize_one(src,dst)
            after=sha256(dst)
            if args.in_place:
                os.replace(dst,src); final=src
            else:
                final=dst
            report["files"].append({"path":src.as_posix(),"output":final.as_posix(),
                                    "sha256_before":before,"sha256_after":after,
                                    "actions":detail.get("actions",[])})
        except Exception as exc:
            try:
                if "dst" in locals() and Path(dst).exists() and Path(dst)!=src:
                    Path(dst).unlink()
            except Exception:
                pass
            report["errors"].append({"path":src.as_posix(),"error":str(exc)})

    result="PASS" if not report["errors"] else "FAIL"
    report["result"]=result
    if args.report:
        rp=Path(args.report).resolve(); rp.parent.mkdir(parents=True,exist_ok=True)
        rp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"metadata_sanitization={result}")
    print(f"files_processed={len(report['files'])}")
    print(f"errors={len(report['errors'])}")
    if args.report: print(f"report={Path(args.report).resolve()}")
    return 0 if result=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())
