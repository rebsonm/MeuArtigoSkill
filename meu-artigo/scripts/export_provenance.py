#!/usr/bin/env python3
"""Export a Meu Artigo project as W3C PROV JSON-LD + RO-Crate 1.3.

No third-party Python dependencies are required.

Default package excludes full-text PDFs. The canonical spreadsheet, project
logs, protocol, traceability, evidence/claims tables, manuscript/submission
files, and provenance metadata are included when present.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import mimetypes
import re
import shutil
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

RO_CRATE_VERSION = "1.3"
RO_CRATE_CONTEXT = "https://w3id.org/ro/crate/1.3/context"
RO_CRATE_CONFORMS = "https://w3id.org/ro/crate/1.3"
PROV_NS = "http://www.w3.org/ns/prov#"
MEUARTIGO_NS = "https://github.com/rebsonm/MeuArtigoSkill/ns#"

MGMT = "00_Gestao_e_Continuidade"
TRACE_FILE = f"{MGMT}/13_Traceability_Log.csv"
AI_FILE = f"{MGMT}/14_AI_Use_Log.csv"
CADA_FILE = f"{MGMT}/11_CADA_Control.csv"
SEARCH_FILE = f"{MGMT}/02_Search_Log.csv"
SCREEN_FILE = f"{MGMT}/03_Screening.csv"
EVIDENCE_FILE = f"{MGMT}/05_Evidence_Matrix.csv"
CLAIMS_FILE = f"{MGMT}/09_Claims_Ledger.csv"
EXPORT_LOG = f"{MGMT}/16_Interoperabilidade.csv"

EXPORT_HEADERS = [
    "Export_ID","Timestamp","Standards","Package_path_or_URL","Package_SHA256",
    "Validation_status","Trace_events","Prov_entities","Prov_activities",
    "Prov_agents","RO_Crate_files","Warnings","Notes"
]

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", (value or "").strip()).strip("-")
    return value or "project"

def urn(kind: str, value: str) -> str:
    return f"urn:meuartigo:{kind}:{quote(str(value), safe='-._~')}"

def refs(value: str) -> list[str]:
    if not value:
        return []
    return [x.strip() for x in re.split(r"[;,|]+", value) if x.strip()]

def read_csv(root: Path, rel: str) -> list[dict[str, str]]:
    path = root / rel
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv_row(path: Path, headers: list[str], row: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        if not exists:
            w.writeheader()
        w.writerow({h: row.get(h, "") for h in headers})

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def next_id(rows: list[dict[str, str]], field: str, prefix: str) -> str:
    n = 0
    pat = re.compile(rf"^{re.escape(prefix)}-(\d+)$")
    for row in rows:
        m = pat.match((row.get(field) or "").strip())
        if m:
            n = max(n, int(m.group(1)))
    return f"{prefix}-{n+1:04d}"

def append_export_trace(root: Path, cada_id: str = "") -> str:
    path = root / TRACE_FILE
    rows = read_csv(root, TRACE_FILE)
    trace_id = next_id(rows, "Trace_ID", "TRACE")
    headers = [
        "Trace_ID","Timestamp","Scientific_stage","CADA_ID","Actor",
        "AI_platform_or_tool","Model_or_version","Action_type","Action_summary",
        "Input_or_source","Source_or_artifact_IDs","Decision_or_output","Rationale",
        "Artifact_before","Artifact_after","Verification_method","Human_validation",
        "Related_Search_IDs","Related_Record_IDs","Related_Evidence_IDs",
        "Related_Claim_IDs","Prompt_or_instruction_summary",
        "Reproducibility_information","Materiality","Status","Notes"
    ]
    row = {
        "Trace_ID": trace_id,
        "Timestamp": now_iso(),
        "Scientific_stage": "13-14",
        "CADA_ID": cada_id,
        "Actor": "SCRIPT",
        "AI_platform_or_tool": "export_provenance.py",
        "Model_or_version": "",
        "Action_type": "PROVENANCE_EXPORT",
        "Action_summary": "Generated interoperable W3C PROV / RO-Crate provenance package.",
        "Input_or_source": "Canonical Meu Artigo workspace",
        "Source_or_artifact_IDs": "C.A.D.A.; traceability; searches; records; evidence; claims; AI use",
        "Decision_or_output": "RO-Crate package and PROV JSON-LD",
        "Rationale": "Preserve machine-readable provenance and project fixity.",
        "Artifact_before": "",
        "Artifact_after": "06_Submissao/Arquivos_Finais/RO_CRATE_*",
        "Verification_method": "validate_provenance_package.py + SHA-256 manifest",
        "Human_validation": "PENDING",
        "Related_Search_IDs": "",
        "Related_Record_IDs": "",
        "Related_Evidence_IDs": "",
        "Related_Claim_IDs": "",
        "Prompt_or_instruction_summary": "Export a standardized audit/provenance package.",
        "Reproducibility_information": "Run export_provenance.py on the canonical project root.",
        "Materiality": "ADMINISTRATIVE",
        "Status": "COMPLETE",
        "Notes": "",
    }
    write_csv_row(path, headers, row)
    return trace_id

def agent_for_trace(row: dict[str, str]) -> list[dict[str, str]]:
    actor = (row.get("Actor") or "OTHER").strip().upper()
    tool = (row.get("AI_platform_or_tool") or "").strip()
    agents = []
    if actor in {"HUMAN", "HUMAN+AI"}:
        agents.append({"id": urn("agent", "human-researcher"), "label": "Human researcher", "type": "prov:Agent"})
    if actor in {"AI", "HUMAN+AI"}:
        name = tool or "AI system"
        agents.append({"id": urn("agent", f"ai-{name}"), "label": name, "type": "prov:SoftwareAgent"})
    elif actor == "SCRIPT":
        name = tool or "script"
        agents.append({"id": urn("agent", f"script-{name}"), "label": name, "type": "prov:SoftwareAgent"})
    elif actor == "DATABASE":
        name = tool or "database/service"
        agents.append({"id": urn("agent", f"database-{name}"), "label": name, "type": "prov:Agent"})
    elif actor not in {"HUMAN", "HUMAN+AI"}:
        agents.append({"id": urn("agent", actor.lower()), "label": actor, "type": "prov:Agent"})
    return agents

def build_prov(root: Path) -> tuple[dict, dict]:
    trace_rows = read_csv(root, TRACE_FILE)
    search_rows = read_csv(root, SEARCH_FILE)
    screen_rows = read_csv(root, SCREEN_FILE)
    evidence_rows = read_csv(root, EVIDENCE_FILE)
    claim_rows = read_csv(root, CLAIMS_FILE)
    cada_rows = read_csv(root, CADA_FILE)

    graph: dict[str, dict] = {}

    def add(node: dict) -> None:
        nid = node["@id"]
        if nid in graph:
            existing = graph[nid]
            for k, v in node.items():
                if k == "@id":
                    continue
                if k not in existing:
                    existing[k] = v
        else:
            graph[nid] = node

    # C.A.D.A. plans
    for r in cada_rows:
        cid = (r.get("CADA_ID") or "").strip()
        if not cid:
            continue
        add({
            "@id": urn("cada", cid),
            "@type": "prov:Plan",
            "rdfs:label": r.get("Title") or cid,
            "meuartigo:cadaId": cid,
            "meuartigo:status": r.get("Status") or "",
            "meuartigo:scientificStage": r.get("Scientific_stage") or "",
            "meuartigo:nextAction": r.get("Next_action") or "",
        })

    # Search activities
    for r in search_rows:
        sid = (r.get("Search_ID") or "").strip()
        if not sid:
            continue
        node = {
            "@id": urn("search", sid),
            "@type": "prov:Activity",
            "rdfs:label": f"Search {sid}",
            "meuartigo:searchId": sid,
            "meuartigo:databaseOrSource": r.get("Database_or_source") or "",
            "meuartigo:literalQuery": r.get("Literal_query") or "",
            "meuartigo:filters": r.get("Filters") or "",
            "meuartigo:recordsFound": r.get("Records_found") or "",
            "meuartigo:recordsExported": r.get("Records_exported") or "",
            "meuartigo:status": r.get("Status") or "",
        }
        if r.get("Date"):
            node["prov:startedAtTime"] = r["Date"]
        add(node)

    # Bibliographic records
    for r in screen_rows:
        rid = (r.get("Record_ID") or "").strip()
        if not rid:
            continue
        node = {
            "@id": urn("record", rid),
            "@type": "prov:Entity",
            "rdfs:label": r.get("Title") or rid,
            "meuartigo:recordId": rid,
            "meuartigo:doi": r.get("DOI") or r.get("Other_identifier") or "",
        }
        sid = (r.get("Search_ID") or "").strip()
        if sid:
            node["prov:wasGeneratedBy"] = {"@id": urn("search", sid)}
        add(node)

    # Evidence
    for r in evidence_rows:
        eid = (r.get("Evidence_ID") or "").strip()
        if not eid:
            continue
        add({
            "@id": urn("evidence", eid),
            "@type": "prov:Entity",
            "rdfs:label": r.get("Citation") or eid,
            "meuartigo:evidenceId": eid,
            "meuartigo:epistemicLabel": r.get("Epistemic_label") or "",
            "meuartigo:locator": r.get("Supporting_locator") or "",
            "meuartigo:construct": r.get("Construct_or_concept") or "",
        })

    # Claims and evidence lineage
    for r in claim_rows:
        cid = (r.get("Claim_ID") or "").strip()
        if not cid:
            continue
        evid = refs(r.get("Evidence_IDs") or "")
        node = {
            "@id": urn("claim", cid),
            "@type": "prov:Entity",
            "rdfs:label": r.get("Claim_text") or cid,
            "meuartigo:claimId": cid,
            "meuartigo:claimType": r.get("Claim_type") or "",
        }
        if evid:
            node["prov:wasDerivedFrom"] = [{"@id": urn("evidence", e)} for e in evid]
        add(node)

    # Trace activities + agents + links
    agent_nodes: dict[str, dict] = {}
    for r in trace_rows:
        tid = (r.get("Trace_ID") or "").strip()
        if not tid:
            continue
        activity_id = urn("trace", tid)
        activity = {
            "@id": activity_id,
            "@type": "prov:Activity",
            "rdfs:label": r.get("Action_summary") or tid,
            "meuartigo:traceId": tid,
            "meuartigo:scientificStage": r.get("Scientific_stage") or "",
            "meuartigo:actionType": r.get("Action_type") or "",
            "meuartigo:materiality": r.get("Materiality") or "",
            "meuartigo:status": r.get("Status") or "",
            "meuartigo:verificationMethod": r.get("Verification_method") or "",
            "meuartigo:humanValidation": r.get("Human_validation") or "",
        }
        if r.get("Timestamp"):
            activity["prov:startedAtTime"] = r["Timestamp"]
        cid = (r.get("CADA_ID") or "").strip()
        if cid:
            activity["meuartigo:managedByCada"] = {"@id": urn("cada", cid)}

        ags = agent_for_trace(r)
        if ags:
            activity["prov:wasAssociatedWith"] = [{"@id": a["id"]} for a in ags]
            for a in ags:
                agent_nodes[a["id"]] = {"@id": a["id"], "@type": a["type"], "rdfs:label": a["label"]}

        used_ids = []
        for field in ("Artifact_before", "Input_or_source", "Source_or_artifact_IDs"):
            for value in refs(r.get(field) or ""):
                eid = urn("artifact", value)
                used_ids.append({"@id": eid})
                add({"@id": eid, "@type": "prov:Entity", "rdfs:label": value})
        for eid0 in refs(r.get("Related_Evidence_IDs") or ""):
            used_ids.append({"@id": urn("evidence", eid0)})
        for rid0 in refs(r.get("Related_Record_IDs") or ""):
            used_ids.append({"@id": urn("record", rid0)})
        if used_ids:
            activity["prov:used"] = used_ids

        output = (r.get("Artifact_after") or "").strip()
        if output:
            oid = urn("artifact", output)
            add({
                "@id": oid,
                "@type": "prov:Entity",
                "rdfs:label": output,
                "prov:wasGeneratedBy": {"@id": activity_id},
            })
        add(activity)

        # Add claim derivation links from the trace when explicit IDs are present.
        evs = refs(r.get("Related_Evidence_IDs") or "")
        for claim_id in refs(r.get("Related_Claim_IDs") or ""):
            node_id = urn("claim", claim_id)
            if node_id not in graph:
                add({"@id": node_id, "@type": "prov:Entity", "rdfs:label": claim_id, "meuartigo:claimId": claim_id})
            if evs:
                graph[node_id]["prov:wasDerivedFrom"] = [{"@id": urn("evidence", e)} for e in evs]

    for node in agent_nodes.values():
        add(node)

    context = {
        "prov": PROV_NS,
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "meuartigo": MEUARTIGO_NS,
        "prov:startedAtTime": {"@type": "xsd:dateTime"},
    }
    doc = {"@context": context, "@graph": list(graph.values())}
    stats = {
        "trace_events": len(trace_rows),
        "entities": sum(1 for n in graph.values() if n.get("@type") in {"prov:Entity", "prov:Plan"}),
        "activities": sum(1 for n in graph.values() if n.get("@type") == "prov:Activity"),
        "agents": sum(1 for n in graph.values() if n.get("@type") in {"prov:Agent", "prov:SoftwareAgent"}),
    }
    return doc, stats

def provenance_warnings(root: Path) -> list[str]:
    warnings = []
    for r in read_csv(root, CADA_FILE):
        if (r.get("Status") or "").upper() == "DONE" and not (r.get("Completion_evidence") or "").strip():
            warnings.append(f"{r.get('CADA_ID','?')}: DONE without Completion_evidence")
    for r in read_csv(root, AI_FILE):
        if (r.get("Materiality") or "").upper() == "SUBSTANTIVE":
            if not (r.get("Human_review_method") or "").strip():
                warnings.append(f"{r.get('AI_Use_ID','?')}: substantive AI use without Human_review_method")
            if (r.get("Accepted_modified_or_rejected") or "").upper() in {"", "PENDING"}:
                warnings.append(f"{r.get('AI_Use_ID','?')}: substantive AI use pending final human decision")
    for r in read_csv(root, CLAIMS_FILE):
        if (r.get("Claim_ID") or "").strip() and not (r.get("Evidence_IDs") or "").strip():
            warnings.append(f"{r.get('Claim_ID','?')}: claim without Evidence_IDs")
    for r in read_csv(root, SEARCH_FILE):
        status = (r.get("Status") or "").upper()
        if status and status not in {"PLANNED", "INVALID", "SUPERSEDED"} and not (r.get("Literal_query") or "").strip():
            warnings.append(f"{r.get('Search_ID','?')}: executed search without Literal_query")
    return warnings

def canonical_files(root: Path, include_fulltext: bool) -> list[Path]:
    candidates = []
    mgmt = root / MGMT
    if mgmt.exists():
        for p in mgmt.rglob("*"):
            if p.is_file():
                candidates.append(p)
    for rel in ["05_Manuscrito/Versao_Canonica", "06_Submissao/Regras_da_Revista", "06_Submissao/Arquivos_Finais", "06_Submissao/Comprovantes"]:
        d = root / rel
        if d.exists():
            for p in d.rglob("*"):
                if not p.is_file():
                    continue
                rel_parts = p.relative_to(d).parts
                if "RO_CRATE_" in p.name or any(part.startswith("RO_CRATE_") for part in rel_parts):
                    continue
                candidates.append(p)
    if include_fulltext:
        d = root / "03_Screening_e_FullText/FullText_Corpus"
        if d.exists():
            candidates.extend([p for p in d.rglob("*") if p.is_file()])
    # Deduplicate by resolved path.
    seen = set()
    out = []
    for p in candidates:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            out.append(p)
    return sorted(out)

def build_ro_crate(root: Path, crate_dir: Path, project_name: str, prov_stats: dict, warnings: list[str], include_fulltext: bool) -> tuple[dict, list[Path]]:
    payload = crate_dir / "payload"
    payload.mkdir(parents=True, exist_ok=True)
    packaged: list[Path] = []

    for src in canonical_files(root, include_fulltext):
        rel = src.relative_to(root)
        dst = payload / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        packaged.append(dst)

    prov_dir = crate_dir / "provenance"
    prov_dir.mkdir(parents=True, exist_ok=True)

    graph = [
        {
            "@id": "ro-crate-metadata.json",
            "@type": "CreativeWork",
            "conformsTo": {"@id": RO_CRATE_CONFORMS},
            "about": {"@id": "./"},
        }
    ]

    has_part = []
    for p in packaged:
        rel = p.relative_to(crate_dir).as_posix()
        has_part.append({"@id": rel})
        mime, _ = mimetypes.guess_type(p.name)
        graph.append({
            "@id": rel,
            "@type": "File",
            "name": p.name,
            "encodingFormat": mime or "application/octet-stream",
            "contentSize": str(p.stat().st_size),
        })

    # Provenance files are added after they are written, but reserve IDs here.
    for rel, name, mime in [
        ("provenance/prov.jsonld", "W3C PROV provenance graph", "application/ld+json"),
        ("provenance/provenance-report.json", "Provenance export report", "application/json"),
        ("provenance/PROVENANCE_REPORT.md", "Human-readable provenance export report", "text/markdown"),
        ("manifest-sha256.txt", "SHA-256 fixity manifest", "text/plain"),
    ]:
        has_part.append({"@id": rel})
        graph.append({"@id": rel, "@type": "File", "name": name, "encodingFormat": mime})

    # Tools from AI log as contextual SoftwareApplication entities.
    seen_tools = set()
    for r in read_csv(root, AI_FILE):
        tool = (r.get("Platform_or_tool") or "").strip()
        if not tool:
            continue
        version = (r.get("Model_or_version") or "").strip()
        key = (tool, version)
        if key in seen_tools:
            continue
        seen_tools.add(key)
        ent = {
            "@id": f"#software-{slug(tool)}-{slug(version) if version else 'unknown'}",
            "@type": "SoftwareApplication",
            "name": tool,
        }
        if version:
            ent["softwareVersion"] = version
        graph.append(ent)

    root_entity = {
        "@id": "./",
        "@type": "Dataset",
        "name": f"Meu Artigo provenance package — {project_name}",
        "description": "Audit/provenance package generated by MeuArtigoSkill with W3C PROV JSON-LD, RO-Crate 1.3 metadata and SHA-256 fixity manifest.",
        "datePublished": datetime.now(timezone.utc).date().isoformat(),
        "hasPart": has_part,
        "mentions": [{"@id": "provenance/prov.jsonld"}],
    }
    graph.append(root_entity)
    return {"@context": RO_CRATE_CONTEXT, "@graph": graph}, packaged

def validate_structure(crate_dir: Path) -> list[str]:
    errors = []
    meta = crate_dir / "ro-crate-metadata.json"
    prov = crate_dir / "provenance/prov.jsonld"
    if not meta.exists():
        return ["missing ro-crate-metadata.json"]
    if not prov.exists():
        errors.append("missing provenance/prov.jsonld")
    try:
        doc = json.loads(meta.read_text(encoding="utf-8"))
        graph = doc.get("@graph", [])
        descriptor = next((x for x in graph if x.get("@id") == "ro-crate-metadata.json"), None)
        root = next((x for x in graph if x.get("@id") == "./"), None)
        if not descriptor or descriptor.get("@type") != "CreativeWork":
            errors.append("invalid RO-Crate metadata descriptor")
        if not descriptor or (descriptor.get("conformsTo") or {}).get("@id") != RO_CRATE_CONFORMS:
            errors.append("metadata descriptor does not conformTo RO-Crate 1.3")
        if not descriptor or (descriptor.get("about") or {}).get("@id") != "./":
            errors.append("metadata descriptor about != ./")
        if not root or root.get("@type") != "Dataset":
            errors.append("missing/invalid Root Data Entity")
        if root:
            for part in root.get("hasPart", []):
                rid = part.get("@id")
                if rid and not (crate_dir / rid).exists():
                    errors.append(f"hasPart file missing: {rid}")
    except Exception as exc:
        errors.append(f"invalid ro-crate-metadata.json: {exc}")
    try:
        pdoc = json.loads(prov.read_text(encoding="utf-8"))
        if "@graph" not in pdoc:
            errors.append("PROV JSON-LD lacks @graph")
    except Exception as exc:
        errors.append(f"invalid prov.jsonld: {exc}")
    return errors

def write_manifest(crate_dir: Path) -> Path:
    manifest = crate_dir / "manifest-sha256.txt"
    files = [p for p in crate_dir.rglob("*") if p.is_file() and p != manifest]
    lines = [f"{file_sha256(p)}  {p.relative_to(crate_dir).as_posix()}" for p in sorted(files)]
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest

def zip_dir(crate_dir: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(crate_dir.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(crate_dir.parent))

def append_traceability_export(root: Path, export_id: str, zip_path: Path, zip_hash: str, validation: str) -> None:
    rast = root / MGMT / "RASTREABILIDADE.md"
    if not rast.exists():
        return
    text = rast.read_text(encoding="utf-8", errors="replace")
    heading = "## Interoperability exports"
    if heading not in text:
        text = text.rstrip() + f"\n\n{heading}\n"
    text += (
        f"\n- {export_id} — {now_iso()} — W3C PROV + RO-Crate {RO_CRATE_VERSION}"
        f" — validation: {validation} — SHA-256: {zip_hash}"
        f" — package: {zip_path.as_posix()}\n"
    )
    rast.write_text(text, encoding="utf-8")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_path")
    ap.add_argument("--output-dir", default="")
    ap.add_argument("--include-fulltext", action="store_true")
    ap.add_argument("--cada-id", default="")
    ap.add_argument("--no-record-export-event", action="store_true")
    args = ap.parse_args()

    root = Path(args.project_path).resolve()
    cfg_path = root / MGMT / "PROJECT_CONFIG.json"
    cfg = {}
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        except Exception:
            cfg = {}
    project_name = cfg.get("project_name") or root.name

    if not args.no_record_export_event:
        append_export_trace(root, args.cada_id)

    prov_doc, prov_stats = build_prov(root)
    warnings = provenance_warnings(root)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    export_rows = read_csv(root, EXPORT_LOG)
    export_id = next_id(export_rows, "Export_ID", "EXPORT")
    base_out = Path(args.output_dir).resolve() if args.output_dir else root / "06_Submissao/Arquivos_Finais"
    crate_name = f"RO_CRATE_{slug(project_name)}_{stamp}"
    crate_dir = base_out / crate_name
    if crate_dir.exists():
        shutil.rmtree(crate_dir)
    crate_dir.mkdir(parents=True, exist_ok=True)

    ro_doc, packaged = build_ro_crate(root, crate_dir, project_name, prov_stats, warnings, args.include_fulltext)

    prov_dir = crate_dir / "provenance"
    (prov_dir / "prov.jsonld").write_text(json.dumps(prov_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = {
        "export_id": export_id,
        "timestamp": now_iso(),
        "standards": ["W3C PROV-O", f"RO-Crate {RO_CRATE_VERSION}", "SHA-256"],
        "project": project_name,
        "trace_events": prov_stats["trace_events"],
        "prov_entities": prov_stats["entities"],
        "prov_activities": prov_stats["activities"],
        "prov_agents": prov_stats["agents"],
        "ro_crate_payload_files": len(packaged),
        "fulltext_included": bool(args.include_fulltext),
        "warnings": warnings,
    }
    (prov_dir / "provenance-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = [
        f"# Provenance export report — {export_id}",
        "",
        f"- Project: {project_name}",
        f"- Timestamp: {report['timestamp']}",
        f"- Standards: W3C PROV-O; RO-Crate {RO_CRATE_VERSION}; SHA-256",
        f"- TRACE events: {prov_stats['trace_events']}",
        f"- PROV entities/plans: {prov_stats['entities']}",
        f"- PROV activities: {prov_stats['activities']}",
        f"- PROV agents: {prov_stats['agents']}",
        f"- Payload files: {len(packaged)}",
        f"- Full-text corpus included: {'yes' if args.include_fulltext else 'no'}",
        "",
        "## Provenance warnings",
    ]
    md += [f"- {w}" for w in warnings] if warnings else ["- None detected by the exporter."]
    md += [
        "",
        "## Interpretation",
        "",
        "This package documents provenance and fixity. It does not by itself establish scientific validity.",
    ]
    (prov_dir / "PROVENANCE_REPORT.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    (crate_dir / "ro-crate-metadata.json").write_text(json.dumps(ro_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    write_manifest(crate_dir)
    errors = validate_structure(crate_dir)
    validation = "VALID" if not errors else "INVALID: " + "; ".join(errors)

    zip_path = base_out / f"{crate_name}.zip"
    zip_dir(crate_dir, zip_path)
    zip_hash = file_sha256(zip_path)

    write_csv_row(root / EXPORT_LOG, EXPORT_HEADERS, {
        "Export_ID": export_id,
        "Timestamp": now_iso(),
        "Standards": f"W3C PROV-O; RO-Crate {RO_CRATE_VERSION}; SHA-256",
        "Package_path_or_URL": zip_path.as_posix(),
        "Package_SHA256": zip_hash,
        "Validation_status": validation,
        "Trace_events": prov_stats["trace_events"],
        "Prov_entities": prov_stats["entities"],
        "Prov_activities": prov_stats["activities"],
        "Prov_agents": prov_stats["agents"],
        "RO_Crate_files": len(packaged) + 5,
        "Warnings": " | ".join(warnings),
        "Notes": "Full text included" if args.include_fulltext else "Full text excluded by default",
    })
    append_traceability_export(root, export_id, zip_path, zip_hash, validation)

    print(f"export_id={export_id}")
    print(f"crate_dir={crate_dir}")
    print(f"zip={zip_path}")
    print(f"sha256={zip_hash}")
    print(f"validation={validation}")
    print(f"warnings={len(warnings)}")
    return 0 if not errors else 2

if __name__ == "__main__":
    raise SystemExit(main())
