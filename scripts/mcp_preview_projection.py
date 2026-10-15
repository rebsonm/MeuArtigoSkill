#!/usr/bin/env python3
"""Strictly fictional MCP Apps preview projection backed by the existing Skill.

Never accepts paths, users, project IDs, credentials or write instructions.
Private-project continuity must remain disabled until separate OAuth,
per-project authorization and canonical-storage verification exist.
"""
from __future__ import annotations

import argparse
import json
import sys

from build_research_workspace import model
from method_routes import ROUTES

def fictional_projection(route: str, mode: str = "MINIMAL") -> dict:
    if route not in ROUTES or mode not in ("MINIMAL", "FULL"):
        raise ValueError("Invalid fictional research preview parameters")
    snapshot = model(route=route, mode=mode)
    if (snapshot.get("is_project_bound") is not False
            or snapshot.get("snapshot_kind") != "FICTIONAL_PREVIEW_NOT_A_REAL_PROJECT"
            or snapshot.get("permissions", {}).get("canonical_write") != "NOT_AVAILABLE_IN_THIS_UI"):
        raise ValueError("Preview-only security invariant failed")
    snapshot["mcp_app"] = {
        "schema": "MEU_ARTIGO_MCP_FICTIONAL_PREVIEW_V1",
        "fictional_only": True,
        "real_project_access": False,
        "researcher_authenticated": False,
        "write_tools_available": False,
        "scientific_gate_approval_available": False,
        "canonical_drive_sync_verified": False,
    }
    return snapshot

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--route", choices=ROUTES, default="QUALITATIVE")
    parser.add_argument("--mode", choices=("MINIMAL", "FULL"), default="MINIMAL")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(fictional_projection(args.route, args.mode),
                         ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    except (ValueError, OSError, TypeError, KeyError):
        print("MCP_PREVIEW_UNAVAILABLE", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
