#!/usr/bin/env python3
"""Offline interactive research workspace: one safe, read-only HTML snapshot.

Generated from the same canonical dashboard, method guides and continuity
router as the Skill. A visual draft check is only an ephemeral CLIENT-SIDE
screen; an actual decision MUST be made by the researcher, rechecked by
method_fill_preflight and written separately by commit_method_field after
human authorization and current source/Drive verification.

No network, persistence, live host bridge, real researcher approval,
source-content disclosure, or hidden implicit scientific gate.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

from adaptive_method_guide import for_project, preview
from method_decision_dimensions import DIMENSIONS
from method_fill_preflight import ENUM_FIELDS, PLACEHOLDER_NORMALIZED, LIMIT_BYTES
from method_routes import ROUTES
from native_chat_dashboard import panel

ROOT=Path(__file__).resolve().parents[1]
TEMPLATE=ROOT/"assets"/"research_workspace.html"
SCHEMA="MEU_ARTIGO_OFFLINE_RESEARCH_WORKSPACE_V1"

def model(*, project: Path|None=None, route: str="QUALITATIVE", mode: str="MINIMAL") -> dict:
    """Build a stable interaction model. Never read or export private prose."""
    if project is not None:
        data=panel(project,mode=mode)
        guides={"overview":for_project(project)}
        method_route=data["method_guidance"].get("route_recorded")
        if method_route is None:
            method_route=data["method_guidance"].get("preview_route")
        if method_route not in ROUTES:
            method_route="UNDECIDED"
        if method_route!="UNDECIDED":
            guides["dimensions"]={
                d:for_project(project,dimension=d) for d in DIMENSIONS
            }
        else:
            guides["dimensions"]={}
        mode_type="EXISTING_PROJECT_LOCAL_SNAPSHOT"
        # Snapshot may contain private task titles: create in a controlled
        # local directory and never commit/upload this HTML to a public repo.
        task_rows=data["tasks"]["items"]
        decision=data["decision_continuity"]
        gates=data["gates"]
        summary=data["overview"]
        continuation=data["continuation"]
        source=data["evidence"]
    else:
        if route not in ROUTES:
            raise ValueError("Unknown illustrative method route")
        mode_type="FICTIONAL_PREVIEW_NOT_A_REAL_PROJECT"
        method_route=route
        guides={"overview":preview(route),"dimensions":{
            d:preview(route,dimension=d) for d in DIMENSIONS
        } if route!="UNDECIDED" else {}}
        task_rows=[]
        decision={
            "last_recorded_decision":{"status":"NO_RECORDED_DECISIONS",
                                      "decision_id":None,"recorded_status":None},
            "method_progress":{"status":"ILLUSTRATIVE_ONLY",
                               "next_missing_field":None,
                               "completed_field_count":0,"required_field_count":0},
            "route_implications":{"summary":None},
            "next_action":{
                "code":"RESEARCHER_EXPLORE_METHOD_OPTIONS",
                "explanation":"Explore alternatives; the actual researcher must decide, justify and record the method in an authorized project.",
                "responsible":"HUMAN_RESEARCHER",
                "existing_cada_task_id":None,"existing_scientific_gate_id":None,
                "technical_preparation_already_authorized_by_router":False,
            },
            "blockers":[],"drive_sync_verified":False,
        }
        gates={"items":[],"registered_total":None}
        summary={"documented_gate_approvals":None}
        continuation={"status":"FICTIONAL_PREVIEW","blockers":[]}
        source={"verified_sources":None}
    # The source objects are *projections*, not raw canonical files.
    # Research content, names, evidence excerpts and rationale never enter.
    enums={r+"::"+f:sorted(values) for (r,f),values in ENUM_FIELDS.items()}
    return {
        "schema":SCHEMA,"snapshot_kind":mode_type,"active_route":method_route,
        "is_project_bound":project is not None,"presentation_mode":mode,
        "overview":{"human_gate_approvals_recorded":summary["documented_gate_approvals"],
                    "scientific_progress_percent":None,
                    "independent_scientific_validation":False,
                    "canonical_drive_sync_verified":False},
        "method_guides":guides,
        "decision_continuity":decision,
        "continuation":{"status":continuation["status"],
                        "blockers":continuation["blockers"]},
        "tasks":{"columns":["ID Tarefa","Tarefa","Responsável execução","Prazo"],
                 "items":[{"id":row.get("id"),"task":row.get("task"),
                           "execution_owner":row.get("execution_owner"),
                           "deadline":row.get("deadline")} for row in task_rows]},
        "human_gates":{"total":gates["registered_total"],
                       "items":[{"id":g.get("id"),"status":g.get("status"),
                                 "approval_documented":g.get("approval_documented",False)}
                                for g in gates["items"]]},
        "preflight_contract":{
            "placeholder_values":sorted(PLACEHOLDER_NORMALIZED),
            "controlled_enums":enums,"max_utf8_bytes":LIMIT_BYTES,
            "local_screen_is_not_authoritative":True,
            "server_validation_required_before_human_authorized_write":True,
            "automatic_write_possible":False,
        },
        "permissions":{"view_and_compare":"READ_ONLY_BROWSER",
                       "draft_review":"LOCAL_EPHEMERAL_CLIENT_HINTS",
                       "canonical_write":"NOT_AVAILABLE_IN_THIS_UI",
                       "human_scientific_approval":"NOT_AVAILABLE_IN_THIS_UI",
                       "chat_host_action":"NOT_CONNECTED"},
        "limitations":[
            "Static catalogue options are not personalized semantic recommendations.",
            "The displayed local project snapshot is not independently authenticated.",
            "No artifact/source passage or private researcher rationale is exported.",
            "The preview and browser draft checker cannot record or approve any choice.",
            "Real canonical writes require new validated human authorization and storage checks.",
        ],
    }

def render(model_data: dict, *, live: bool=False) -> str:
    """Escape inert JSON. Permit loopback-only requests only in opt-in live mode."""
    if model_data.get("schema")!=SCHEMA:
        raise ValueError("Invalid research-workspace schema")
    enabled=bool((model_data.get("local_bridge") or {}).get("enabled"))
    if enabled != live:
        raise ValueError("Live credentials must never be saved in offline HTML")
    if TEMPLATE.is_symlink() or not TEMPLATE.is_file():
        raise ValueError("Missing safe HTML template")
    template=TEMPLATE.read_text(encoding="utf-8")
    # Only the local HTTP session can opt into same-origin requests. Saved
    # offline HTML keeps a stricter 'connect-src none' CSP.
    if live:
        csp="connect-src 'none'"
        if template.count(csp)!=1:
            raise ValueError("Missing strict baseline CSP")
        template=template.replace(csp,"connect-src 'self'")
    slot="__RESEARCH_WORKSPACE_MODEL_JSON__"
    if template.count(slot)!=1:
        raise ValueError("HTML template must have exactly one data slot")
    safe=(json.dumps(model_data,ensure_ascii=False,separators=(",",":"),sort_keys=True)
          .replace("<",r"\u003c").replace("> ",r"\u003e ")
          .replace(">",r"\u003e").replace("&",r"\u0026")
          .replace("\u2028",r"\u2028").replace("\u2029",r"\u2029"))
    return template.replace(slot,safe)

def save(path: Path, html: str) -> None:
    """Create only, 0600. Never overwrite an existing private snapshot."""
    if not path.parent.is_dir() or path.is_symlink() or path.exists():
        raise ValueError("HTML output requires new name in an existing directory")
    with open(path,"x",encoding="utf-8",opener=lambda name,flags:
              os.open(name,flags,0o600)) as stream:
        stream.write(html)

def main(argv=None) -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project",nargs="?",type=Path)
    ap.add_argument("--preview-route",choices=ROUTES)
    ap.add_argument("--mode",choices=("MINIMAL","FULL"),default="MINIMAL")
    ap.add_argument("--output",required=True,type=Path,
                    help="New local-only HTML filename (never an existing file)")
    args=ap.parse_args(argv)
    if args.project and args.preview_route:
        ap.error("An actual project and an illustrative preview are mutually exclusive")
    try:
        data=model(project=args.project,route=args.preview_route or "QUALITATIVE",
                   mode=args.mode)
        save(args.output,render(data))
        print(json.dumps({
            "status":"LOCAL_INTERACTIVE_PREVIEW_CREATED",
            "snapshot_kind":data["snapshot_kind"],
            "output_name":args.output.name,
            "canonical_writes":False,"scientific_approvals":False,
            "drive_sync_verified":False,"installed_chatgpt_extension":False,
        },sort_keys=True))
        return 0
    except (OSError,ValueError,UnicodeError,TypeError,json.JSONDecodeError) as exc:
        print("RESEARCH_WORKSPACE_ERROR: "+type(exc).__name__,file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
