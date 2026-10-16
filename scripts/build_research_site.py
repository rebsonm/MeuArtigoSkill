#!/usr/bin/env python3
"""Build the approved Meu Artigo blue website from an authorized read-only projection.

Preview mode shows fictional example numbers. Project mode uses existing local
canonical read-only model and NEVER treats the offline snapshot as Drive sync.
This file intentionally does not expose private project titles, documents,
source passages, method rationales, tokens or Drive folder names.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import build_research_workspace as workspace

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "research_site.html"
SLOT = "__MEU_ARTIGO_SITE_MODEL_JSON__"
SCHEMA = "MEU_ARTIGO_SITE_V1"
MAX_TASKS = 10000
MAX_GATES = 7


def project_site_model(snapshot: dict) -> dict:
    """Whitelist display fields from the established canonical projection."""
    if not isinstance(snapshot, dict) or snapshot.get("schema") != workspace.SCHEMA:
        raise ValueError("SITE_SNAPSHOT_SCHEMA_INVALID")
    if snapshot.get("local_bridge", {}).get("enabled"):
        # The website has NO local bridge transport or session key support.
        raise ValueError("SITE_LOCAL_BRIDGE_NOT_SUPPORTED")
    if snapshot.get("is_project_bound") is not True:
        return {"schema": SCHEMA, "kind": "ILLUSTRATIVE_PREVIEW"}
    tasks = snapshot.get("tasks", {}).get("items")
    gates = snapshot.get("human_gates", {}).get("items")
    next_action = snapshot.get("decision_continuity", {}).get("next_action")
    if (not isinstance(tasks, list) or len(tasks) > MAX_TASKS or
            not isinstance(gates, list) or len(gates) > MAX_GATES or
            not isinstance(next_action, dict)):
        raise ValueError("SITE_CANONICAL_PROJECTION_INCOMPLETE")
    # Only data already admitted to the authenticated read-only projection.
    return {
        "schema": SCHEMA, "kind": "CANONICAL_LOCAL_SNAPSHOT",
        "active_route": snapshot.get("active_route"),
        "documented_gate_count": snapshot.get("overview", {}).get(
            "human_gate_approvals_recorded"),
        "tasks": [
            {"id": row.get("id"), "task": row.get("task"),
             "execution_owner": row.get("execution_owner"),
             "deadline": row.get("deadline")} for row in tasks
        ],
        "gates": [
            {"id": row.get("id"),
             "approval_documented": row.get("approval_documented") is True}
            for row in gates
        ],
        "next_action": {
            "code": next_action.get("code"),
            "explanation": next_action.get("explanation"),
            "responsible": next_action.get("responsible"),
        },
        "canonical_drive_sync_verified": False,
        "automatic_scientific_approval": False,
        "canonical_writes_allowed": False,
    }


def render_site(snapshot: dict) -> str:
    data = project_site_model(snapshot)
    data["locale"] = snapshot.get("site_locale", "auto")
    if TEMPLATE.is_symlink() or not TEMPLATE.is_file():
        raise ValueError("SITE_TEMPLATE_NOT_SAFE")
    source = TEMPLATE.read_text(encoding="utf-8")
    if source.count(SLOT) != 1:
        raise ValueError("SITE_TEMPLATE_SLOT_INVALID")
    # The inert JSON script tag can contain quoted and untrusted text.
    # Escape HTML-significant chars to block closing script injection.
    encoded = (json.dumps(data, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False)
               .replace("&", r"\u0026")
               .replace("<", r"\u003c")
               .replace(">", r"\u003e")
               .replace("\u2028", r"\u2028")
               .replace("\u2029", r"\u2029"))
    return source.replace(SLOT, encoded)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group()
    group.add_argument("--project", type=Path,
                       help="Authorized existing local project, never Drive proof")
    group.add_argument("--preview-route", choices=workspace.ROUTES,
                       default=None, help="Illustrative route; no real data")
    p.add_argument("--output", type=Path,
                   help="Create new private HTML; cannot overwrite an existing file")
    p.add_argument("--mode", choices=("MINIMAL", "FULL"), default="MINIMAL",
                   help="Read-only presentation depth; does not authorize writes")
    p.add_argument("--json-only", action="store_true",
                   help="Emit only whitelisted read-only snapshot JSON for MCP Apps")
    p.add_argument("--language", default="auto",
                   help="BCP-47 user interface locale; unrelated to manuscript")
    args = p.parse_args(argv)
    try:
        projection = workspace.model(
            project=args.project,
            route=args.preview_route or "QUALITATIVE",
            mode="MINIMAL")
        if args.json_only:
            if args.project is None:
                raise ValueError("SITE_MCP_DATA_REQUIRES_AUTHORIZED_PROJECT")
            result = project_site_model(projection)
            if result["kind"] != "CANONICAL_LOCAL_SNAPSHOT":
                raise ValueError("SITE_MCP_NO_CANONICAL_PROJECT")
            result["locale"] = args.language
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        if args.output is None:
            raise ValueError("SITE_OUTPUT_REQUIRED")
        projection["site_locale"] = args.language
        html = render_site(projection)
        workspace.save(args.output, html)
    except (OSError, ValueError, TypeError, KeyError, UnicodeError) as exc:
        # Do not echo protected project paths or content.
        print("SITE_GENERATION_BLOCKED: " + type(exc).__name__, file=sys.stderr)
        return 2
    print(json.dumps({
        "status": "READ_ONLY_SITE_CREATED",
        "kind": "CANONICAL_LOCAL_SNAPSHOT" if args.project else "ILLUSTRATIVE_PREVIEW",
        "output_name": args.output.name,
        "canonical_writes": False, "drive_sync_verified": False,
        "scientific_approvals": False, "installed_chatgpt_ui": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
