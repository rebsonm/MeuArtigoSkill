#!/usr/bin/env python3
"""Opt-in bibliographic retrieval/export for authorized local Meu Artigo projects.

This is a CLI adapter, not an installed ChatGPT HTTP tool or cloud connector.
Never call this automatically during onboarding. Project registry updates are
allowed only for a locally authorized WORK_FALLBACK. Google Drive projects
receive explicit staging exports; actual sync must be confirmed separately.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from uuid import uuid4

from bibliographic_connectors import FIELDS, LOCKED, SUPPORTED, capabilities, search
from init_project import TABLES

MGMT = "00_Gestao_e_Continuidade"
SEARCH = f"{MGMT}/02_Search_Log.csv"
SCREENING = f"{MGMT}/03_Screening.csv"
TRACE = f"{MGMT}/13_Traceability_Log.csv"
MANUAL_MESSAGE = (
    "Bibliographic APIs are optional. Continue normally with manual searches "
    "and CSV/RIS/BibTeX exports when you do not want or cannot authorize them."
)

GUIDES = {
    "openalex": (
        "OpenAlex: https://help.openalex.org/api/ . Search works are available "
        "without an API key where the current service allows; for higher limits "
        "register personally and store OPENALEX_API_KEY only in the secure runtime."
    ),
    "crossref": (
        "Crossref: https://www.crossref.org/documentation/retrieve-metadata/"
        "rest-api/ . Public metadata endpoint normally requires no key. "
        "For polite access set MEU_ARTIGO_CONTACT_EMAIL in your own runtime."
    ),
    "semantic_scholar": (
        "Semantic Scholar: https://api.semanticscholar.org/api-docs/ . "
        "Search public metadata within the provider's rate limits. "
        "When authorized, store SEMANTIC_SCHOLAR_API_KEY only in your protected runtime."
    ),
    "scopus": (
        "Scopus: https://dev.elsevier.com/ . Obtain your personal developer "
        "API key and confirm actual institutional API entitlement and permitted "
        "AI processing with Elsevier. CAFe login alone does not grant API rights. "
        "No authenticated Scopus execution is provided by this pilot."
    ),
    "wos_starter": (
        "Web of Science Starter: https://developer.clarivate.com/apis/wos-starter . "
        "Apply for a personal key; check the plan and licence, then use an "
        "approved secure executor. No live authenticated integration in pilot."
    ),
    "wos_expanded": (
        "Web of Science Expanded: https://developer.clarivate.com/apis/wos . "
        "Requires API licence and institution authorization; not enabled."
    ),
}


def optional_config(config: dict) -> dict:
    """Missing settings must never turn an API into a required dependency."""
    value = config.get("bibliographic_connectors")
    if not isinstance(value, dict):
        return {"enabled": False, "providers": {}}
    enabled = value.get("enabled") is True
    providers = value.get("providers")
    return {"enabled": enabled, "providers": providers if isinstance(providers, dict) else {}}


def _read_config(root: Path) -> dict:
    file = root / MGMT / "PROJECT_CONFIG.json"
    if not file.is_file():
        raise ValueError("No real authorized project configuration found")
    data = json.loads(file.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Invalid project configuration")
    return data


def set_provider_preference(root: Path, provider: str, enabled: bool) -> dict:
    """Local opt-in preference only, never provider credential authorization.

    Remote Drive-canonical project changes require a separate actual Drive
    connector write and cannot be asserted from this local utility.
    """
    if provider not in SUPPORTED + LOCKED:
        raise ValueError("Unsupported provider")
    config = _read_config(root)
    if config.get("storage_mode") != "WORK_FALLBACK" or config.get("fallback_authorized") is not True:
        raise ValueError("Local preferences require authorized WORK_FALLBACK")
    state = optional_config(config)
    state["providers"][provider] = {"enabled": enabled,
                                     "credential_verified": False,
                                     "provider_licence_verified": False}
    state["enabled"] = any(
        isinstance(v, dict) and v.get("enabled") is True
        for v in state["providers"].values())
    config["bibliographic_connectors"] = state
    path = root / MGMT / "PROJECT_CONFIG.json"
    temp = path.with_name("." + path.name + "." + uuid4().hex + ".tmp")
    try:
        temp.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)
    return {"provider": provider, "enabled": enabled,
            "is_authorized_provider_credential": False,
            "drive_sync_verified": False}


def _read_rows(path: Path, expected: list[str]) -> list[dict[str, str]]:
    if not path.is_file():
        raise ValueError("Canonical register missing; stop rather than fabricate one")
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != expected:
            raise ValueError("Canonical register headings diverged; migration required")
        return list(reader)


def _next_id(rows: list[dict[str, str]], key: str, prefix: str) -> str:
    used = {row.get(key) for row in rows}
    number = 1
    while f"{prefix}-{number:06d}" in used:
        number += 1
    return f"{prefix}-{number:06d}"


def _atomic_csv(path: Path, headers: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name("." + path.name + "." + uuid4().hex + ".tmp")
    try:
        with temp.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows([{h: row.get(h, "") for h in headers} for row in rows])
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def _csv_safe(v: str) -> str:
    """Guard spreadsheet formula injection without changing the in-memory record."""
    value = str(v or "")
    if value.lstrip()[:1] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + value
    return value


def export_staging(root: Path | None, out_dir: Path, outcome) -> dict:
    """Export only metadata, never tokens or licensed fulltext."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{outcome.provider}_metadata.csv"
    records = [{key: _csv_safe(row.get(key, "")) for key in FIELDS}
               for row in outcome.rows]
    _atomic_csv(path, list(FIELDS), records)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    outcome.export_sha256 = digest
    receipt = {
        "kind": "LOCAL_EXECUTION_RECORD_NOT_INDEPENDENT_PROVIDER_RECEIPT",
        "provider": outcome.provider, "literal_query": outcome.query,
        "status": outcome.status, "error_code": outcome.error_code,
        "executed_at": outcome.executed_at,
        "reported_total": outcome.reported_total,
        "records_received": len(outcome.rows),
        "pages_received": outcome.pages_received,
        "export_file": path.name, "export_sha256": digest,
        "drive_sync_verified": False,
        "scopus_wos_licence_verified": False,
        "scientific_validation": False,
        "note": "Metadata only; abstracts and full texts were not read or validated.",
    }
    (out_dir / "retrieval_receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt


def commit_to_authorized_local_project(root: Path, outcome, export_path: Path) -> dict:
    """Append real retrieved rows to canonical registers without replacing files.

    Google Drive canonical projects remain staging only; this routine cannot
    independently prove an external Drive write. It is not a science approval.
    """
    config = _read_config(root)
    if config.get("storage_mode") != "WORK_FALLBACK" or config.get("fallback_authorized") is not True:
        raise ValueError("Canonical write requires explicitly authorized WORK_FALLBACK")
    if not outcome.executed_at or outcome.status not in {"COMPLETE", "PARTIAL"}:
        raise ValueError("No executed bibliographic result to register")
    search_headers = TABLES[SEARCH]
    screening_headers = TABLES[SCREENING]
    trace_headers = TABLES[TRACE]
    srows = _read_rows(root / SEARCH, search_headers)
    rrows = _read_rows(root / SCREENING, screening_headers)
    trows = _read_rows(root / TRACE, trace_headers)
    search_id = _next_id(srows, "Search_ID", "SEARCH-API")
    trace_id = _next_id(trows, "Trace_ID", "TRACE-API")
    srow = {x: "" for x in search_headers}
    srow.update({
        "Search_ID": search_id, "Date": outcome.executed_at,
        "Database_or_source": outcome.provider,
        "Conceptual_blocks": "REQUIRES_RESEARCHER_REVIEW",
        "Literal_query": outcome.query,
        "Filters": "provider-default; bounded retrieval, not cross-base equivalent",
        "Records_found": str(outcome.reported_total) if outcome.reported_total is not None else "",
        "Records_exported": str(len(outcome.rows)),
        "Export_file_or_URL": str(export_path.resolve().relative_to(root.resolve()))
        if export_path.resolve().is_relative_to(root.resolve()) else export_path.name,
        "Status": outcome.status, "Iteration": "1",
        "Notes": "API metadata-only, researcher screening still pending. "
                 "Local record; no remote Drive sync asserted.",
    })
    # Canonical records retain individual source IDs, with no invented abstract.
    for row in outcome.rows:
        rid = _next_id(rrows, "Record_ID", "REC-API")
        new = {x: "" for x in screening_headers}
        new.update({
            "Record_ID": rid, "Source_database": outcome.provider,
            "Search_ID": search_id, "Title": row["title"],
            "Authors": row["authors"], "Year": row["year"],
            "DOI": row["doi"], "Other_identifier": row["source_id"],
            "Document_type": row["document_type"],
            "Language": row["language"],
            "Notes": "API metadata only; no full text reviewed; source ID recorded.",
        })
        rrows.append(new)
    trow = {x: "" for x in trace_headers}
    trow.update({
        "Trace_ID": trace_id, "Timestamp": outcome.executed_at,
        "Scientific_stage": "04", "Actor": "SCRIPT",
        "AI_platform_or_tool": "bibliographic_workflow.py",
        "Action_type": "BIBLIOGRAPHIC_METADATA_RETRIEVAL",
        "Action_summary": "Recorded opted-in metadata search",
        "Source_or_artifact_IDs": search_id,
        "Input_or_source": outcome.provider,
        "Decision_or_output": outcome.status,
        "Verification_method": "Local export SHA-256; remote validation not inferred",
        "Related_Search_IDs": search_id,
        "Status": "UNVERIFIED",
    })
    # Write staging files first and add a durable idempotency guard: a run's
    # export hash must not be recorded twice with the same Search_ID.
    if any(row.get("Export_file_or_URL") == srow["Export_file_or_URL"] for row in srows):
        raise ValueError("This export appears already registered")
    srows.append(srow); trows.append(trow)
    # All three canonical files have been checked before any write.
    _atomic_csv(root / SCREENING, screening_headers, rrows)
    _atomic_csv(root / SEARCH, search_headers, srows)
    _atomic_csv(root / TRACE, trace_headers, trows)
    return {"Search_ID": search_id, "Trace_ID": trace_id,
            "new_records": len(outcome.rows),
            "scientific_approval": False, "drive_synced": False}


def print_guidance(provider: str | None = None, lang: str = "pt") -> None:
    if lang == "pt":
        print("As APIs bibliográficas são OPCIONAIS; o modo padrão sem API permanece disponível.")
        print("Você pode usar buscas e arquivos CSV/RIS/BibTeX manuais sem conectar credenciais.")
        print("Não cole senhas, chaves, tokens nem cookies neste chat ou no Google Drive.")
    else:
        print(MANUAL_MESSAGE)
        print("Never paste API keys, CAFe passwords, OAuth tokens or cookies into chat.")
    for key in ([provider] if provider else GUIDES):
        if key not in GUIDES:
            raise ValueError("Unknown provider")
        print(key + ": " + GUIDES[key])


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    cmd = parser.add_subparsers(dest="command", required=True)
    guide = cmd.add_parser("guide", help="Explain optional BYOC connections")
    guide.add_argument("--provider", choices=list(GUIDES))
    guide.add_argument("--lang", choices=["pt", "en"], default="pt")
    status = cmd.add_parser("status", help="Inspect optional configuration only; no HTTP")
    status.add_argument("--project", required=True)
    configure = cmd.add_parser("configure", help="Set optional local preference (NOT API login)")
    configure.add_argument("--project", required=True)
    configure.add_argument("--provider", required=True, choices=list(SUPPORTED) + list(LOCKED))
    choice = configure.add_mutually_exclusive_group(required=True)
    choice.add_argument("--enable", action="store_true")
    choice.add_argument("--disable", action="store_true")
    retrieve = cmd.add_parser("search", help="Explicit opt-in bounded metadata search")
    retrieve.add_argument("--provider", required=True, choices=list(SUPPORTED) + list(LOCKED))
    retrieve.add_argument("--query", required=True, help="Literal query for THIS provider")
    retrieve.add_argument("--limit", type=int, default=50)
    retrieve.add_argument("--project", help="Existing authorized project, optional for export")
    retrieve.add_argument("--out-dir", required=True, help="Private staging directory")
    retrieve.add_argument("--allow-network", action="store_true", help="Explicitly opt in to provider HTTP")
    retrieve.add_argument("--commit-local", action="store_true",
                          help="Append to registers only in explicitly authorized WORK_FALLBACK")
    dedupe = cmd.add_parser("dedupe", help="Use existing dedupe_records.py on hybrid imports")
    dedupe.add_argument("inputs", nargs="+")
    dedupe.add_argument("--out-dir", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "guide":
            print_guidance(args.provider, args.lang)
            return 0
        if args.command == "status":
            c = _read_config(Path(args.project))
            print(json.dumps({"bibliographic_connectors": optional_config(c),
                              "manual_mode_available": True, "network_called": False}))
            return 0
        if args.command == "configure":
            updated = set_provider_preference(Path(args.project), args.provider,
                                              enabled=bool(args.enable))
            print(json.dumps(updated))
            return 0
        if args.command == "dedupe":
            result = subprocess.run(
                [sys.executable, str(Path(__file__).with_name("dedupe_records.py")),
                 *args.inputs, "--out-dir", args.out_dir],
                check=False)
            return result.returncode
        root = Path(args.project).resolve() if args.project else None
        if args.commit_local and root is None:
            raise ValueError("--commit-local requires --project")
        if root is not None:
            config = _read_config(root)
            if args.commit_local and not (config.get("storage_mode") == "WORK_FALLBACK"
                                          and config.get("fallback_authorized") is True):
                raise ValueError("Use staging for Google Drive projects; no automatic sync")
        else:
            config = {}
        # A CLI search is an explicit opt-in, never a setup prerequisite.
        key = (os.environ.get("OPENALEX_API_KEY", "") if args.provider == "openalex"
               else os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "")
               if args.provider == "semantic_scholar" else "")
        email = os.environ.get("MEU_ARTIGO_CONTACT_EMAIL", "")
        result = search(args.provider, args.query, limit=args.limit,
                        execute=args.allow_network, email=email, api_key=key)
        if result.status == "NOT_EXECUTED":
            print(json.dumps({"status": result.status,
                              "manual_mode_available": True,
                              "hint": "Add --allow-network to expressly run the optional search."}))
            return 0
        if result.status not in ("COMPLETE", "PARTIAL") or (
                result.status == "PARTIAL" and not result.rows):
            print(json.dumps({"status": result.status, "error_code": result.error_code,
                              "records_received": len(result.rows),
                              "manual_mode_available": True}))
            return 2
        output = Path(args.out_dir).resolve() / (result.provider + "-" + uuid4().hex[:10])
        receipt = export_staging(root, output, result)
        payload = {"status": result.status, "provider": result.provider,
                   "records_received": len(result.rows),
                   "reported_total": result.reported_total,
                   "receipt": str(output / "retrieval_receipt.json"),
                   "project_registry_updated": False, "drive_synced": False}
        if args.commit_local:
            payload.update(commit_to_authorized_local_project(
                root, result, output / f"{result.provider}_metadata.csv"))
            payload["project_registry_updated"] = True
        print(json.dumps(payload, ensure_ascii=False))
        return 0 if result.status == "COMPLETE" else 3
    except (OSError, ValueError, json.JSONDecodeError, csv.Error):
        # Fixed sanitised error; no raw URLs, keys, source text or server payload.
        print("ERROR: INVALID_OR_UNAUTHORIZED_LOCAL_OPERATION", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
