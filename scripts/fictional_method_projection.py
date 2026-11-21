#!/usr/bin/env python3
"""Fictional, local-only methodological projection. No project access or writes."""
from __future__ import annotations
import argparse
import json
import sys
from build_research_workspace import model
from adaptive_method_guide import preview
from method_choice_dialogue import ACTIONS, dialogue
from method_decision_dimensions import DIMENSIONS
from method_routes import ROUTES

def fictional_projection(route: str, mode: str = "MINIMAL", *,
                       action: str = "suggest", dimension: str | None = None,
                       option_id: str | None = None,
                       compare_ids: tuple[str, str] | None = None) -> dict:
    if route not in ROUTES or mode not in ("MINIMAL", "FULL") or action not in ACTIONS or (
            dimension is not None and dimension not in DIMENSIONS):
        raise ValueError("Unsupported fictional methodology parameters")
    snapshot = model(route=route, mode=mode)
    if (snapshot.get("is_project_bound") is not False
            or snapshot.get("snapshot_kind") != "FICTIONAL_PREVIEW_NOT_A_REAL_PROJECT"
            or snapshot.get("permissions", {}).get("canonical_write") != "NOT_AVAILABLE_IN_THIS_UI"):
        raise ValueError("Fictional-only invariant failed")
    response = dialogue(preview(route, dimension=dimension), action=action,
                        option_id=option_id, compare_ids=compare_ids)
    if (response.get("gate_approved") is not False or
            response.get("selection_written") is not False or
            response.get("canonical_state_modified") is not False or
            response.get("method_recommended_or_selected") is not False):
        raise ValueError("Untrusted methodological authorization")
    snapshot["fictional_method_dialogue"] = response
    snapshot["preview_contract"] = {
        "schema": "MEU_ARTIGO_FICTIONAL_METHOD_PROJECTION_V1",
        "fictional_only": True, "real_project_access": False,
        "researcher_authenticated": False, "write_tools_available": False,
        "scientific_gate_approval_available": False,
        "canonical_drive_sync_verified": False,
        "server_tool_registered": False, "standalone_server_created": False,
    }
    return snapshot

def public_cli_contract() -> dict:
    """Constant nonapproval envelope; never logs option text or dynamic cards."""
    return {
        "snapshot_kind": "FICTIONAL_PREVIEW_NOT_A_REAL_PROJECT",
        "is_project_bound": False,
        "tasks": {"items": []},
        "human_gates": {"items": []},
        "overview": {"independent_scientific_validation": False},
        "permissions": {"canonical_write": "NOT_AVAILABLE_IN_THIS_UI"},
        "preview_contract": {
            "fictional_only": True, "real_project_access": False,
            "researcher_authenticated": False, "write_tools_available": False,
            "scientific_gate_approval_available": False,
            "canonical_drive_sync_verified": False,
            "server_tool_registered": False, "standalone_server_created": False,
        },
        "fictional_method_dialogue": {
            "selection_written": False, "gate_approved": False,
            "canonical_state_modified": False,
            "method_recommended_or_selected": False,
            "drive_sync_verified": False, "human_reviewer_authenticated": False,
            "human_action": {"required_to_commit_scientific_choice": True},
        },
        "full_catalogue_available_only_via_read_only_python_api": True,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--route", choices=ROUTES, default="QUALITATIVE")
    parser.add_argument("--mode", choices=("MINIMAL", "FULL"), default="MINIMAL")
    parser.add_argument("--dimension", choices=DIMENSIONS)
    parser.add_argument("--action", choices=ACTIONS, default="suggest")
    parser.add_argument("--option-id")
    parser.add_argument("--compare", nargs=2, metavar=("A", "B"))
    args = parser.parse_args(argv)
    try:
        x=fictional_projection(args.route,args.mode,action=args.action,
                              dimension=args.dimension,option_id=args.option_id,
                              compare_ids=tuple(args.compare) if args.compare else None)
        # Dynamic cards and arbitrary option identifiers are not terminal-safe.
        print(json.dumps(public_cli_contract(),sort_keys=True,
                         separators=(",",":"),allow_nan=False))
        return 0
    except (ValueError,OSError,TypeError,KeyError):
        print("FICTIONAL_METHOD_PROJECTION_UNAVAILABLE",file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
