#!/usr/bin/env python3
"""Validate a Meu Artigo W3C PROV / RO-Crate package."""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

RO_CRATE_CONFORMS = "https://w3id.org/ro/crate/1.3"

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def validate_dir(root: Path) -> tuple[list[str], list[str]]:
    errors=[]; warnings=[]
    meta=root/"ro-crate-metadata.json"
    prov=root/"provenance/prov.jsonld"
    manifest=root/"manifest-sha256.txt"

    if not meta.exists(): errors.append("missing ro-crate-metadata.json")
    if not prov.exists(): errors.append("missing provenance/prov.jsonld")
    if not manifest.exists(): errors.append("missing manifest-sha256.txt")
    if errors: return errors,warnings

    try:
        doc=json.loads(meta.read_text(encoding="utf-8"))
        graph=doc.get("@graph")
        if not isinstance(graph,list): errors.append("RO-Crate @graph missing/not a list"); graph=[]
        descriptor=next((x for x in graph if x.get("@id")=="ro-crate-metadata.json"),None)
        crate=next((x for x in graph if x.get("@id")=="./"),None)
        if not descriptor: errors.append("RO-Crate metadata descriptor missing")
        else:
            if descriptor.get("@type")!="CreativeWork": errors.append("metadata descriptor @type must be CreativeWork")
            if (descriptor.get("about") or {}).get("@id")!="./": errors.append("metadata descriptor about must reference ./")
            if (descriptor.get("conformsTo") or {}).get("@id")!=RO_CRATE_CONFORMS:
                errors.append("metadata descriptor conformsTo must be RO-Crate 1.3")
        if not crate: errors.append("Root Data Entity ./ missing")
        else:
            if crate.get("@type")!="Dataset": errors.append("Root Data Entity @type must be Dataset")
            for part in crate.get("hasPart",[]):
                rid=(part or {}).get("@id")
                if rid and not (root/rid).exists():
                    errors.append(f"RO-Crate hasPart missing on disk: {rid}")
    except Exception as exc:
        errors.append(f"invalid ro-crate-metadata.json: {exc}")

    try:
        pdoc=json.loads(prov.read_text(encoding="utf-8"))
        graph=pdoc.get("@graph")
        if not isinstance(graph,list): errors.append("PROV @graph missing/not a list"); graph=[]
        types=[n.get("@type") for n in graph if isinstance(n,dict)]
        if "prov:Activity" not in types: warnings.append("PROV graph contains no prov:Activity")
        if "prov:Entity" not in types and "prov:Plan" not in types: warnings.append("PROV graph contains no prov:Entity/prov:Plan")
        if "prov:Agent" not in types and "prov:SoftwareAgent" not in types: warnings.append("PROV graph contains no prov:Agent")
    except Exception as exc:
        errors.append(f"invalid provenance/prov.jsonld: {exc}")

    try:
        for line_no,line in enumerate(manifest.read_text(encoding="utf-8").splitlines(),1):
            if not line.strip(): continue
            parts=line.split("  ",1)
            if len(parts)!=2:
                errors.append(f"manifest line {line_no}: invalid format")
                continue
            expected,rel=parts
            p=root/rel
            if not p.exists():
                errors.append(f"manifest file missing: {rel}")
                continue
            actual=sha256(p)
            if actual!=expected:
                errors.append(f"checksum mismatch: {rel}")
    except Exception as exc:
        errors.append(f"invalid manifest-sha256.txt: {exc}")

    return errors,warnings

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("package")
    a=ap.parse_args()
    p=Path(a.package).resolve()

    if p.is_dir():
        root=p
        errors,warnings=validate_dir(root)
    elif p.suffix.lower()==".zip":
        with tempfile.TemporaryDirectory() as td:
            with zipfile.ZipFile(p) as z:
                z.extractall(td)
            base=Path(td)
            dirs=[x for x in base.iterdir() if x.is_dir()]
            root=dirs[0] if len(dirs)==1 else base
            errors,warnings=validate_dir(root)
    else:
        print("ERROR: package must be a directory or .zip")
        return 2

    for w in warnings: print("WARNING:",w)
    for e in errors: print("ERROR:",e)
    print(f"validation_errors={len(errors)}")
    print(f"validation_warnings={len(warnings)}")
    return 1 if errors else 0

if __name__=="__main__":
    raise SystemExit(main())
