"""Synthetic Skill conversation-resume checks, not a researcher UX study."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import init_project
from method_routes import MGMT,new_profile
from research_resume_brief import from_panel, text, SCHEMA
from native_chat_dashboard import panel

PRIVATE="SENSITIVE_RESEARCH_RATIONALE_SHOULD_NOT_LEAK_8181"

def projection(*,storage="WORK_FALLBACK",local_allowed=True):
    return {
        "schema":"MEU_ARTIGO_NATIVE_PANEL_V1",
        "project_storage_recorded":storage,
        "local_work_fallback_authorized_in_config":local_allowed,
        "mode":"MINIMAL",
        "continuation":{
            "status":"TECHNICAL_PREPARATION_AVAILABLE",
            "next_task_id":"CADA-0002","next_gate_id":"GATE-0002",
            "technical_preparation_possible":True,"blockers":[],
        },
        "decision_continuity":{
            "status":"READ_ONLY_GUIDANCE",
            "last_recorded_decision":{
                "status":"LATEST_RECORD_PRESENT_NOT_HUMAN_AUTHENTICATED",
                "decision_id":"DEC-0001",
                "trace_link_recorded":True,
                "Rationale":PRIVATE,
            },
            "method_progress":{
                "route":"QUALITATIVE","next_missing_field":"tradition",
                "completed_field_count":1,"required_field_count":4,
            },
            "next_action":{
                "code":"EXECUTE_RECORDED_CADA_TASK",
                "responsible":"TECHNICAL_AGENT",
                "existing_cada_task_id":"CADA-0002",
                "existing_scientific_gate_id":"GATE-0002",
                "technical_preparation_already_authorized_by_router":True,
                "execution_authorized_by_this_view":False,
            },
            "blockers":[],
        },
        "tasks":{"items":[{"id":"CADA-0002","task":PRIVATE,
                           "execution_owner":PRIVATE,"deadline":PRIVATE}]},
        "limitations":[PRIVATE],
    }

def make_csv(path,headers,rows=None):
    with path.open("w",encoding="utf-8-sig",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=headers)
        writer.writeheader()
        writer.writerows([{key:r.get(key,"") for key in headers}
                           for r in (rows or [])])

class ResumeProjectionUnitTests(unittest.TestCase):
    def test_ready_candidate_is_only_guidance_and_private_prose_is_not_returned(self):
        data=from_panel(projection())
        self.assertEqual(data["schema"],SCHEMA)
        self.assertEqual(data["status"],"TECHNICAL_PREPARATION_CANDIDATE")
        self.assertTrue(data["next_step"]["technical_preparation_candidate"])
        self.assertEqual(data["recorded"]["last_decision_id"],"DEC-0001")
        self.assertEqual(data["recorded"]["method_route"],"QUALITATIVE")
        self.assertEqual(data["recorded"]["next_missing_method_field"],"tradition")
        self.assertFalse(data["next_step"]["task_executed_by_this_brief"])
        self.assertFalse(data["next_step"]["gate_approved_by_this_brief"])
        self.assertTrue(data["scientific_decision_requires_researcher"])
        self.assertNotIn(PRIVATE,json.dumps(data,ensure_ascii=False))
        self.assertNotIn(PRIVATE,text(data))
        self.assertFalse(data["storage"]["google_drive_sync_verified_in_this_session"])

    def test_missing_local_authorization_blocks_even_ready_navigation(self):
        data=from_panel(projection(local_allowed=False))
        self.assertEqual(data["status"],"RECONCILIATION_REQUIRED")
        self.assertIn("LOCAL_FALLBACK_AUTHORIZATION_NOT_RECORDED",data["blockers"])
        self.assertFalse(data["next_step"]["technical_preparation_candidate"])

    def test_drive_canonical_mirror_must_not_authorize_local_progress(self):
        data=from_panel(projection(storage="GOOGLE_DRIVE",local_allowed=False))
        self.assertIn("CANONICAL_DRIVE_ACCESS_NOT_VERIFIED_BY_LOCAL_PANEL",
                      data["blockers"])
        self.assertEqual(data["status"],"RECONCILIATION_REQUIRED")
        self.assertFalse(data["next_step"]["technical_preparation_candidate"])

    def test_missing_or_unknown_storage_fails_closed(self):
        for mode in ("UNKNOWN",None,"LOCAL",PRIVATE):
            with self.subTest(mode=mode):
                x=from_panel(projection(storage=mode,local_allowed=True))
                self.assertEqual(x["status"],"RECONCILIATION_REQUIRED")
                self.assertIn("CANONICAL_STORAGE_MODE_UNKNOWN",x["blockers"])
                self.assertNotIn(PRIVATE,json.dumps(x))

    def test_decision_provenance_blocker_wins_over_ready_task(self):
        p=projection()
        p["decision_continuity"]["status"]="RECONCILIATION_REQUIRED"
        p["decision_continuity"]["blockers"]=[
            "DECISION_PROVENANCE_RECONCILIATION_REQUIRED"]
        x=from_panel(p)
        self.assertEqual(x["status"],"RECONCILIATION_REQUIRED")
        self.assertFalse(x["next_step"]["technical_preparation_candidate"])
        self.assertEqual(x["available_followups"],
                         ["REVIEW_BLOCKERS","SHOW_EXISTING_RECORD_IDENTIFIERS"])

    def test_navigation_cannot_disagree_with_scientific_router(self):
        p=projection()
        p["continuation"]["next_task_id"]="CADA-9999"
        x=from_panel(p)
        self.assertIn("NEXT_ACTION_NAVIGATION_MISMATCH",x["blockers"])
        self.assertFalse(x["next_step"]["technical_preparation_candidate"])

    def test_forged_router_permission_is_not_a_technical_candidate(self):
        p=projection()
        p["decision_continuity"]["next_action"][
            "technical_preparation_already_authorized_by_router"]=False
        x=from_panel(p)
        self.assertIn("NEXT_ACTION_AUTHORIZATION_MISMATCH",x["blockers"])
        self.assertFalse(x["next_step"]["technical_preparation_candidate"])

    def test_invalid_identifiers_are_not_echoed_to_the_researcher(self):
        p=projection()
        p["decision_continuity"]["next_action"]["existing_cada_task_id"]=PRIVATE
        p["decision_continuity"]["last_recorded_decision"]["decision_id"]=PRIVATE
        x=from_panel(p)
        self.assertIsNone(x["recorded"]["last_decision_id"])
        self.assertIsNone(x["next_step"]["existing_cada_id"])
        self.assertIn("NEXT_ACTION_IDENTIFIER_REQUIRES_RECONCILIATION",
                      x["blockers"])
        self.assertNotIn(PRIVATE,json.dumps(x))

    def test_nav_blocked_must_not_create_a_technical_candidate(self):
        p=projection()
        p["continuation"]["status"]="BLOCKED"
        x=from_panel(p)
        self.assertEqual(x["status"],"RECONCILIATION_REQUIRED")
        self.assertIn("CANONICAL_NAVIGATION_STATUS_CONFLICT",x["blockers"])
        self.assertFalse(x["next_step"]["technical_preparation_candidate"])

    def test_unlinked_trace_blocks_even_if_upstream_view_was_optimistic(self):
        p=projection()
        p["decision_continuity"]["last_recorded_decision"]["trace_link_recorded"]=False
        x=from_panel(p)
        self.assertIn("RECORDED_DECISION_PROVENANCE_NOT_VERIFIED",x["blockers"])
        self.assertFalse(x["next_step"]["technical_preparation_candidate"])

    def test_unrecognized_router_status_stays_blocked(self):
        p=projection()
        p["continuation"]["status"]="NEW_UNREVIEWED_ROUTER_STATUS"
        p["continuation"]["technical_preparation_possible"]=False
        x=from_panel(p)
        self.assertIn("CANONICAL_NAVIGATION_STATUS_NOT_RECOGNIZED",x["blockers"])
        self.assertFalse(x["next_step"]["technical_preparation_candidate"])

    def test_unrecognized_action_cannot_trigger_execution(self):
        p=projection()
        p["decision_continuity"]["next_action"]["code"]="APPLY_APPROVAL"
        p["decision_continuity"]["next_action"]["responsible"]="UNKNOWN_PERSON"
        x=from_panel(p)
        self.assertIn("NEXT_ACTION_PROJECTION_UNRECOGNIZED",x["blockers"])
        self.assertEqual(x["next_step"]["code"],
                         "REQUEST_RESEARCHER_REVIEW_OF_CONTINUATION")
        self.assertFalse(x["next_step"]["technical_preparation_candidate"])

    def test_no_recorded_decision_is_never_fabricated_as_authenticated(self):
        p=projection()
        p["decision_continuity"]["last_recorded_decision"]={
            "status":"NO_RECORDED_DECISIONS","decision_id":None}
        x=from_panel(p)
        self.assertIsNone(x["recorded"]["last_decision_id"])
        self.assertFalse(x["recorded"]["decision_is_authenticated"])

    def test_malformed_snapshot_is_rejected_instead_of_guessing(self):
        for bad in (None,{},{"schema":"MEU_ARTIGO_NATIVE_PANEL_V1"},
                    {"schema":"INVALID","continuation":{},"decision_continuity":{}}):
            with self.subTest(case=str(bad)), self.assertRaises(ValueError):
                from_panel(bad)

class ResumeLiveReadOnlyFixtureTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.m=self.root/MGMT
        self.m.mkdir()
        (self.m/"PROJECT_CONFIG.json").write_text(json.dumps({
            "presentation_mode":"MINIMAL",
            "storage_mode":"WORK_FALLBACK",
            "fallback_authorized":True,
            "method_route":"UNDECIDED",
            "method_route_governance_required":True,
        }))
        (self.m/"METHOD_PROFILE.json").write_text(
            json.dumps(new_profile("UNDECIDED")))
        (self.m/"CONTINUIDADE.md").write_text(
            "# Fictional project\nNext valid action: CADA-0001\n")
        make_csv(self.m/"11_CADA_Control.csv",
                 init_project.TABLES[f"{MGMT}/11_CADA_Control.csv"],[
            {"CADA_ID":"CADA-0001","Title":PRIVATE,"Status":"READY",
             "Next_action":PRIVATE,"Assigned_to":"AGENT",
             "Execution_mode":"AUTONOMOUS","Scientific_stage":"01"}])
        make_csv(self.m/"18_Human_Validation_Gates.csv",
                 init_project.TABLES[f"{MGMT}/18_Human_Validation_Gates.csv"],[
            {"GATE_ID":f"GATE-{i:04d}","Status":"READY","Decision":"PENDING",
             "Scientific_stage":f"{i:02d}"}
            for i in range(1,8)])
        make_csv(self.m/"17_Decision_Log.csv",
                 ["DEC_ID","Decision_type","Decision_question","Decision",
                  "Status","Decided_by","Trace_ID","Rationale","Notes"],[])
        make_csv(self.m/"13_Traceability_Log.csv",
                 ["Trace_ID","Decision_or_output","Notes"],[])

    def test_real_panel_composition_is_read_only_and_has_no_private_text(self):
        before={p.name:p.read_bytes() for p in self.m.iterdir() if p.is_file()}
        data=from_panel(panel(self.root))
        self.assertEqual(data["schema"],SCHEMA)
        self.assertIsNone(data["recorded"]["last_decision_id"])
        self.assertFalse(data["next_step"]["task_executed_by_this_brief"])
        self.assertFalse(data["next_step"]["gate_approved_by_this_brief"])
        self.assertNotIn(PRIVATE,json.dumps(data))
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.m.iterdir()
                                 if p.is_file()})

    def test_missing_decision_register_blocks_read_only_resume(self):
        (self.m/"17_Decision_Log.csv").unlink()
        data=from_panel(panel(self.root))
        self.assertEqual(data["status"],"RECONCILIATION_REQUIRED")
        self.assertIn("DECISION_PROVENANCE_RECONCILIATION_REQUIRED",
                      data["blockers"])
        self.assertFalse(data["next_step"]["technical_preparation_candidate"])

    def test_revoking_local_fallback_blocks_continuation(self):
        config=self.m/"PROJECT_CONFIG.json"
        obj=json.loads(config.read_text())
        obj["fallback_authorized"]=False
        config.write_text(json.dumps(obj))
        data=from_panel(panel(self.root))
        self.assertIn("LOCAL_FALLBACK_AUTHORIZATION_NOT_RECORDED",data["blockers"])
        self.assertFalse(data["next_step"]["technical_preparation_candidate"])

if __name__=="__main__":
    unittest.main()
