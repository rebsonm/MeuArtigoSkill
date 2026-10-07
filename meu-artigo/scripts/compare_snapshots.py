#!/usr/bin/env python3
"""Compare two Meu Artigo snapshots using their stored SHA-256 file hashes."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def load_snapshot(path:Path)->dict:
    if path.is_dir():
        p=path/"snapshot.json"
    else:
        p=path
    if not p.exists():
        raise SystemExit(f"snapshot.json not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("snapshot_a")
    ap.add_argument("snapshot_b")
    ap.add_argument("--output",default="")
    a=ap.parse_args()

    sa=load_snapshot(Path(a.snapshot_a).resolve())
    sb=load_snapshot(Path(a.snapshot_b).resolve())
    ha=sa.get("file_hashes",{}) or {}
    hb=sb.get("file_hashes",{}) or {}

    ka=set(ha); kb=set(hb)
    added=sorted(kb-ka)
    removed=sorted(ka-kb)
    changed=sorted(k for k in ka&kb if ha[k]!=hb[k])
    unchanged=sorted(k for k in ka&kb if ha[k]==hb[k])

    report={
        "snapshot_a":sa.get("snapshot_id"),
        "snapshot_b":sb.get("snapshot_id"),
        "milestone_a":sa.get("milestone"),
        "milestone_b":sb.get("milestone"),
        "added":added,
        "removed":removed,
        "changed":changed,
        "unchanged_count":len(unchanged),
        "decision_ids_a":sa.get("decision_ids",""),
        "decision_ids_b":sb.get("decision_ids",""),
        "gate_a":sa.get("gate_id",""),
        "gate_b":sb.get("gate_id",""),
        "change_summary_a":sa.get("change_summary",""),
        "change_summary_b":sb.get("change_summary",""),
    }

    md=[
        f"# Snapshot comparison — {report['snapshot_a']} → {report['snapshot_b']}",
        "",
        f"- Milestone A: {report['milestone_a']}",
        f"- Milestone B: {report['milestone_b']}",
        f"- Added files: {len(added)}",
        f"- Removed files: {len(removed)}",
        f"- Changed files: {len(changed)}",
        f"- Unchanged files: {len(unchanged)}",
        "",
        "## Added",
    ]
    md += [f"- {x}" for x in added] or ["- None"]
    md += ["","## Removed"]
    md += [f"- {x}" for x in removed] or ["- None"]
    md += ["","## Changed"]
    md += [f"- {x}" for x in changed] or ["- None"]
    md += [
        "",
        "## Governance context",
        f"- DEC_IDs A: {report['decision_ids_a'] or '—'}",
        f"- DEC_IDs B: {report['decision_ids_b'] or '—'}",
        f"- Gate A: {report['gate_a'] or '—'}",
        f"- Gate B: {report['gate_b'] or '—'}",
        f"- Change summary A: {report['change_summary_a'] or '—'}",
        f"- Change summary B: {report['change_summary_b'] or '—'}",
    ]

    text="\n".join(md)+"\n"
    if a.output:
        out=Path(a.output).resolve()
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(text,encoding="utf-8")
        out.with_suffix(".json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(out)
    else:
        print(text)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
