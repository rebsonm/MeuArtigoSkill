#!/usr/bin/env python3
"""Integrated, synthetic-only Skill acceptance; no live MCP or researcher data.

Executes the real canonical next-step router, DEC/TRACE continuity, the
conversation resume, and safe blocker guidance against disposable fixtures.
Never reads an actual user's project or performs a canonical write.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import tempfile

import init_project
from method_routes import MGMT, new_profile
from native_chat_dashboard import panel
from research_resume_brief import from_panel
from research_blocker_guide import explain

PRIVATE="SYNTHETIC_PRIVATE_RESEARCH_CONTENT_NEVER_EXPOSE_9861"
NAMES=(
    "authorized_local_ready","missing_decision_register","orphan_decision_trace",
    "route_profile_mismatch","drive_canonical_local_mirror",
    "local_fallback_revoked","stale_continuity_reference",
    "unfinished_method_transaction","missing_scientific_gate",
    "missing_task_dependency","missing_recorded_next_action",
)
EXPECTED={
    "authorized_local_ready":None,
    "missing_decision_register":"DECISION_PROVENANCE_RECONCILIATION_REQUIRED",
    "orphan_decision_trace":"DECISION_PROVENANCE_RECONCILIATION_REQUIRED",
    "route_profile_mismatch":"METHOD_PROFILE_REQUIRES_RECONCILIATION",
    "drive_canonical_local_mirror":"CANONICAL_DRIVE_ACCESS_NOT_VERIFIED_BY_LOCAL_PANEL",
    "local_fallback_revoked":"LOCAL_FALLBACK_AUTHORIZATION_NOT_RECORDED",
    "stale_continuity_reference":"CONTINUITY_NEXT_ACTION_MISMATCH",
    "unfinished_method_transaction":"PENDING_RESEARCH_TRANSACTION_RECOVERY",
    "missing_scientific_gate":"SEVEN_GATES_NOT_PRESENT_OR_UNEXPECTED",
    "missing_task_dependency":"UNKNOWN_TASK_DEPENDENCY",
    "missing_recorded_next_action":"MISSING_RECORDED_NEXT_ACTION",
}
EXPECTED_TEMPLATES=frozenset(EXPECTED)

def _table(path: Path, headers: list[str], rows: list[dict]) -> None:
    with path.open("w",encoding="utf-8-sig",newline="") as out:
        writer=csv.DictWriter(out,fieldnames=headers)
        writer.writeheader()
        writer.writerows([{k:row.get(k,"") for k in headers} for row in rows])

def _init(folder: Path) -> Path:
    root=folder/"fictional-research-project"
    m=root/MGMT
    m.mkdir(parents=True)
    (m/"PROJECT_CONFIG.json").write_text(json.dumps({
        "storage_mode":"WORK_FALLBACK","fallback_authorized":True,
        "presentation_mode":"MINIMAL","method_route":"UNDECIDED",
        "method_route_governance_required":True,
    }),encoding="utf-8")
    (m/"METHOD_PROFILE.json").write_text(
        json.dumps(new_profile("UNDECIDED")),encoding="utf-8")
    (m/"CONTINUIDADE.md").write_text(
        "# Synthetic-only continuation\nNext valid action: CADA-0001\n",
        encoding="utf-8")
    _table(m/"11_CADA_Control.csv",init_project.TABLES[f"{MGMT}/11_CADA_Control.csv"],[
        {"CADA_ID":"CADA-0001","Status":"READY","Title":PRIVATE,
         "Next_action":PRIVATE,"Assigned_to":"AGENT","Execution_mode":"AUTONOMOUS",
         "Scientific_stage":"01"}])
    _table(m/"18_Human_Validation_Gates.csv",init_project.TABLES[f"{MGMT}/18_Human_Validation_Gates.csv"],[
        {"GATE_ID":f"GATE-{i:04d}","Status":"READY",
         "Decision":"PENDING","Scientific_stage":f"{i:02d}"}
        for i in range(1,8)])
    _table(m/"17_Decision_Log.csv",init_project.TABLES[f"{MGMT}/17_Decision_Log.csv"],[])
    _table(m/"13_Traceability_Log.csv",init_project.TABLES[f"{MGMT}/13_Traceability_Log.csv"],[])
    return root

def _replace_csv(path: Path, modifier) -> None:
    with path.open(encoding="utf-8-sig",newline="") as stream:
        reader=csv.DictReader(stream)
        headers=list(reader.fieldnames or [])
        rows=list(reader)
    modifier(rows)
    _table(path,headers,rows)

def _mutate(name: str, root: Path) -> None:
    m=root/MGMT
    if name=="authorized_local_ready":
        return
    if name=="missing_decision_register":
        (m/"17_Decision_Log.csv").unlink()
    elif name=="orphan_decision_trace":
        p=m/"17_Decision_Log.csv"
        _table(p,init_project.TABLES[f"{MGMT}/17_Decision_Log.csv"],[{
            "DEC_ID":"DEC-0001","Decision_type":"SCOPE",
            "Decision_question":PRIVATE,"Decision":"SYNTHETIC_ONLY",
            "Status":"APPROVED","Decided_by":"FICTIONAL_ACTOR",
            "Trace_ID":"TRACE-9999","Rationale":PRIVATE}])
    elif name=="route_profile_mismatch":
        cfg=m/"PROJECT_CONFIG.json"
        obj=json.loads(cfg.read_text())
        obj["method_route"]="QUALITATIVE"
        cfg.write_text(json.dumps(obj))
    elif name in ("drive_canonical_local_mirror","local_fallback_revoked"):
        cfg=m/"PROJECT_CONFIG.json"
        obj=json.loads(cfg.read_text())
        if name=="drive_canonical_local_mirror":
            obj["storage_mode"]="GOOGLE_DRIVE"
        obj["fallback_authorized"]=False
        cfg.write_text(json.dumps(obj))
    elif name=="stale_continuity_reference":
        (m/"CONTINUIDADE.md").write_text(
            "# Synthetic-only continuity\nNext valid action: CADA-9999\n")
    elif name=="unfinished_method_transaction":
        (m/".pending_method_route_change").mkdir()
    elif name=="missing_scientific_gate":
        _replace_csv(m/"18_Human_Validation_Gates.csv",
                     lambda rows: rows.pop())
    elif name in ("missing_task_dependency","missing_recorded_next_action"):
        def edit(rows):
            if name=="missing_task_dependency":
                rows[0]["Dependency_IDs"]="CADA-9999"
            else:
                rows[0]["Next_action"]=""
        _replace_csv(m/"11_CADA_Control.csv",edit)
    else:
        raise ValueError("Unknown synthetic acceptance case")

def _state(root: Path) -> dict[str,bytes]:
    # Compare actual synthetic file bytes, not only the reported flags.
    return {p.relative_to(root).as_posix():p.read_bytes()
            for p in root.rglob("*") if p.is_file()}

def _case(name: str) -> dict:
    with tempfile.TemporaryDirectory(prefix="meu-artigo-integrated-synthetic-") as t:
        root=_init(Path(t))
        _mutate(name,root)
        initial=_state(root)
        p=panel(root,mode="MINIMAL")
        resume=from_panel(p)
        guidance=explain(resume)
        final=_state(root)
        assert initial==final, "Read-only acceptance altered synthetic records"
        assert resume["canonical_files_modified"] is False
        assert resume["next_step"]["task_executed_by_this_brief"] is False
        assert resume["next_step"]["gate_approved_by_this_brief"] is False
        assert guidance["no_task_executed"] and guidance["no_gate_approved"]
        assert guidance["no_canonical_write"] and guidance["no_automatic_repair"]
        assert guidance["drive_sync_verified"] is False
        assert resume["storage"]["google_drive_sync_verified_in_this_session"] is False
        blob=json.dumps({"resume":resume,"guidance":guidance},sort_keys=True)
        assert PRIVATE not in blob, "Private fixture content leaked"
        expected=EXPECTED[name]
        if expected is None:
            assert resume["status"]=="TECHNICAL_PREPARATION_CANDIDATE",resume
            assert resume["next_step"]["technical_preparation_candidate"] is True
            assert guidance["primary"] is None
        else:
            assert expected in resume["blockers"],(name,resume["blockers"])
            assert resume["status"]=="RECONCILIATION_REQUIRED",name
            assert resume["next_step"]["technical_preparation_candidate"] is False
            assert guidance["primary"] is not None
        return {
            "case":name,
            "result":"PASS",
            "expected_blocker":expected,
            "resume_status":resume["status"],
            "blockers_reported":len(resume["blockers"]),
            "blocker_guidance_status":guidance["status"],
            "read_only_project_unchanged":True,
            "private_prose_exported":False,
            "scientific_approval":False,
            "cloud_sync_verified":False,
        }

def run() -> dict:
    records=[_case(name) for name in NAMES]
    assert {r["case"] for r in records}==EXPECTED_TEMPLATES
    root=Path(__file__).resolve().parents[1]
    instructions=(root/"references/mcp-tool-use.md").read_text(encoding="utf-8")
    agent=(root/"agents/openai.yaml").read_text(encoding="utf-8")
    assert "already-connected" in instructions and "MCP_NOT_CONNECTED" in instructions
    assert "does **not** activate MCP Apps UI" in instructions
    assert "Graceful fallback" in instructions and "seven human gates" in instructions
    assert "dependencies:" not in agent
    # These are static contract checks. No attempt to invent a connected tool
    # or attest any production MCP server, OAuth, UI or Drive access.
    return {
        "schema":"MEU_ARTIGO_INTEGRATED_SKILL_ACCEPTANCE_V1",
        "acceptance_kind":"SYNTHETIC_LOCAL_INTEGRATION_ONLY",
        "case_count":len(records),
        "all_scenarios_passed":True,
        "source_of_truth":"DISPOSABLE_SYNTHETIC_LOCAL_RECORDS_ONLY",
        "original_user_projects_accessed":False,
        "original_user_projects_modified":False,
        "all_cases_without_scientific_approval":True,
        "all_cases_without_canonical_writes":True,
        "all_cases_without_private_prose_export":True,
        "optional_mcp_instruction_contract_checked":True,
        "host_mcp_connection_exercised":False,
        "project_owned_mcp_server_connected":False,
        "mcp_apps_ui_verified":False,
        "updated_skill_installed_in_chatgpt":False,
        "real_drive_access_or_sync_verified":False,
        "independent_scientific_validation":False,
        "results":records,
    }

def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,help="New or replaceable synthetic-only JSON report")
    args=parser.parse_args(argv)
    report=run()
    encoded=json.dumps(report,sort_keys=True,indent=2)+"\n"
    if args.output:
        if not args.output.parent.is_dir():
            parser.error("Output parent must already exist")
        args.output.write_text(encoded,encoding="utf-8")
    else:
        print(encoded,end="")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
