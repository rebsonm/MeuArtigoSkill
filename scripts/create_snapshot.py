#!/usr/bin/env python3
"""Create a frozen, hash-verified Meu Artigo project snapshot."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

MGMT="00_Gestao_e_Continuidade"
SNAP_DIR=f"{MGMT}/Snapshots"
SNAP_FILE=f"{MGMT}/19_Snapshots.csv"
GATE_FILE=f"{MGMT}/18_Human_Validation_Gates.csv"
DEC_FILE=f"{MGMT}/17_Decision_Log.csv"
CADA_FILE=f"{MGMT}/11_CADA_Control.csv"

SNAP_HEADERS=[
"SNAP_ID","Timestamp","Milestone","Scientific_stage","Trigger","Gate_ID",
"DEC_IDs","CADA_IDs","Previous_SNAP_ID","Snapshot_path_or_URL","Manifest_path",
"Manifest_SHA256","Canonical_artifacts","Change_summary","Validation_status",
"EXPORT_ID","Notes"
]

def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def slug(v:str)->str:
    v=re.sub(r"[^A-Za-z0-9._-]+","-",v.strip()).strip("-")
    return v or "snapshot"

def rows(path:Path)->list[dict[str,str]]:
    if not path.exists(): return []
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def ensure(path:Path,headers:list[str]):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists() or path.stat().st_size==0:
        with path.open("w",encoding="utf-8-sig",newline="") as f:
            csv.writer(f).writerow(headers)

def next_id(path:Path)->str:
    n=0
    pat=re.compile(r"^SNAP-(\d+)$")
    for r in rows(path):
        m=pat.match((r.get("SNAP_ID") or "").strip())
        if m: n=max(n,int(m.group(1)))
    return f"SNAP-{n+1:04d}"

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def canonical_files(root:Path)->list[Path]:
    keep=[]
    mgmt=root/MGMT
    if mgmt.exists():
        for p in mgmt.rglob("*"):
            if p.is_file() and "Snapshots" not in p.parts:
                keep.append(p)
    for rel in ["05_Manuscrito/Versao_Canonica","06_Submissao/Regras_da_Revista","06_Submissao/Arquivos_Finais"]:
        d=root/rel
        if d.exists():
            for p in d.rglob("*"):
                if p.is_file() and not p.name.startswith("RO_CRATE_"):
                    keep.append(p)
    for rel in ["04_Evidencias_e_Sintese/MAPA_CORPUS.json","04_Evidencias_e_Sintese/MAPA_CORPUS.md"]:
        p=root/rel
        if p.exists() and p.is_file():
            keep.append(p)
    seen=set(); out=[]
    for p in sorted(keep):
        rp=p.resolve()
        if rp in seen: continue
        seen.add(rp); out.append(p)
    return out

def write_manifest(root:Path,payload:Path,manifest:Path)->dict[str,str]:
    entries={}
    for p in sorted(payload.rglob("*")):
        if p.is_file():
            rel=p.relative_to(payload).as_posix()
            entries[rel]=sha256(p)
    manifest.write_text("\n".join(f"{h}  {rel}" for rel,h in entries.items())+"\n",encoding="utf-8")
    return entries

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--milestone",required=True)
    ap.add_argument("--stage",default="")
    ap.add_argument("--trigger",default="MANUAL")
    ap.add_argument("--gate-id",default="")
    ap.add_argument("--dec-ids",default="")
    ap.add_argument("--cada-ids",default="")
    ap.add_argument("--change-summary",default="")
    ap.add_argument("--export-id",default="")
    ap.add_argument("--notes",default="")
    a=ap.parse_args()

    root=Path(a.project).resolve()
    table=root/SNAP_FILE
    ensure(table,SNAP_HEADERS)
    existing=rows(table)
    sid=next_id(table)
    previous=(existing[-1].get("SNAP_ID") or "") if existing else ""

    snap_dir=root/SNAP_DIR/f"{sid}_{slug(a.milestone)}"
    if snap_dir.exists(): shutil.rmtree(snap_dir)
    payload=snap_dir/"payload"
    payload.mkdir(parents=True,exist_ok=True)

    artifacts=[]
    for src in canonical_files(root):
        rel=src.relative_to(root)
        dst=payload/rel
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,dst)
        artifacts.append(rel.as_posix())

    manifest=snap_dir/"manifest-sha256.txt"
    hashes=write_manifest(root,payload,manifest)

    metadata={
        "snapshot_id":sid,
        "timestamp":now_iso(),
        "milestone":a.milestone,
        "scientific_stage":a.stage,
        "trigger":a.trigger,
        "gate_id":a.gate_id,
        "decision_ids":a.dec_ids,
        "cada_ids":a.cada_ids,
        "previous_snapshot_id":previous,
        "change_summary":a.change_summary,
        "canonical_artifacts":artifacts,
        "file_hashes":hashes,
        "manifest_sha256":sha256(manifest),
        "export_id":a.export_id,
        "notes":a.notes,
    }
    (snap_dir/"snapshot.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    validation="VALID" if hashes else "VALID_EMPTY"

    with table.open("a",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=SNAP_HEADERS)
        w.writerow({
            "SNAP_ID":sid,
            "Timestamp":metadata["timestamp"],
            "Milestone":a.milestone,
            "Scientific_stage":a.stage,
            "Trigger":a.trigger,
            "Gate_ID":a.gate_id,
            "DEC_IDs":a.dec_ids,
            "CADA_IDs":a.cada_ids,
            "Previous_SNAP_ID":previous,
            "Snapshot_path_or_URL":snap_dir.as_posix(),
            "Manifest_path":manifest.as_posix(),
            "Manifest_SHA256":metadata["manifest_sha256"],
            "Canonical_artifacts":"; ".join(artifacts),
            "Change_summary":a.change_summary,
            "Validation_status":validation,
            "EXPORT_ID":a.export_id,
            "Notes":a.notes,
        })

    # If linked to a gate, populate Snapshot_after.
    if a.gate_id:
        gate_path=root/GATE_FILE
        gate_rows=rows(gate_path)
        if gate_rows:
            headers=list(gate_rows[0].keys())
            changed=False
            for r in gate_rows:
                if (r.get("GATE_ID") or "").strip()==a.gate_id:
                    r["Snapshot_after"]=sid
                    changed=True
            if changed:
                with gate_path.open("w",encoding="utf-8-sig",newline="") as f:
                    w=csv.DictWriter(f,fieldnames=headers); w.writeheader(); w.writerows(gate_rows)

    print(f"snapshot_id={sid}")
    print(f"snapshot_dir={snap_dir}")
    print(f"manifest_sha256={metadata['manifest_sha256']}")
    print(f"files={len(hashes)}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
