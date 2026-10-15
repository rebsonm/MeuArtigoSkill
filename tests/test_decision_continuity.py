"""Synthetic decision continuity tests: no human subjects or science approvals.

Records are developer-authored fixtures, never a genuine human declaration.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from decision_continuity import compose, project_method_progress
from method_routes import MGMT,new_profile
import native_chat_dashboard as native
import init_project

REVIEW_ONLY_NAV={
    "status":"TECHNICAL_PREPARATION_AVAILABLE",
    "next_task_id":"CADA-0002","next_gate_id":"GATE-0002",
    "blockers":[],"technical_preparation_possible":True,
    "requires_human_decision":False,
}

def table(path,headers,rows):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=headers)
        writer.writeheader()
        writer.writerows([{key:row.get(key,"") for key in headers} for row in rows])

class IntelligentContinuityTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.m=self.root/MGMT
        self.m.mkdir()
        self.config=self.m/"PROJECT_CONFIG.json"
        self.config.write_text(json.dumps({
            "presentation_mode":"MINIMAL",
            "storage_mode":"WORK_FALLBACK",
            "fallback_authorized":True,
            "method_route":"QUALITATIVE",
            "method_route_governance_required":True,
        }))
        self.profile=self.m/"METHOD_PROFILE.json"
        self.make_profile("QUALITATIVE",confirmed=True)
        self.decisions=[]
        self.traces=[]
        self.save_tables()
        self.cont=self.m/"CONTINUIDADE.md"
        self.cont.write_text("# Fictional research continuation\nNext valid action: CADA-0002\n")
        self.tasks=self.m/"11_CADA_Control.csv"
        table(self.tasks,init_project.TABLES[f"{MGMT}/11_CADA_Control.csv"],[
            {"CADA_ID":"CADA-0001","Status":"DONE","Title":"Initialize",
             "Completion_evidence":"Synthetic receipt","Scientific_stage":"00"},
            {"CADA_ID":"CADA-0002","Status":"READY","Title":"Prepare source verification",
             "Assigned_to":"AGENT","Execution_mode":"AUTONOMOUS",
             "Next_action":"PRIVATE_NEXT_ACTION_TO_NOT_EXPORT","Scientific_stage":"01"}])
        self.gates=self.m/"18_Human_Validation_Gates.csv"
        table(self.gates,init_project.TABLES[f"{MGMT}/18_Human_Validation_Gates.csv"],[
            {"GATE_ID":f"GATE-{i:04d}","Status":"COMPLETED" if i==1 else "READY",
             "Decision":"APPROVED" if i==1 else "PENDING",
             "Validated_by":"synthetic actor" if i==1 else "",
             "Validation_evidence":"synthetic ref" if i==1 else "",
             "Scientific_stage":f"{i:02d}"}
            for i in range(1,8)])

    def make_profile(self,route,confirmed=False):
        doc=new_profile(route)
        if confirmed:
            doc["route_confirmation"]="HUMAN_CONFIRMED"
            doc["route_decision_id"]="DEC-0001"
            doc["human_route_reviewer"]="FICTIONAL_NOT_AUTHENTICATED"
            doc["human_route_decision_evidence"]="fictional original reference"
        self.profile.write_text(json.dumps(doc))
        return doc

    def save_tables(self):
        table(self.m/"17_Decision_Log.csv",
              ["DEC_ID","Decision_type","Decision_question","Decision",
               "Status","Decided_by","Trace_ID","Rationale","Notes"],self.decisions)
        table(self.m/"13_Traceability_Log.csv",["Trace_ID","Decision_or_output","Notes"],self.traces)

    def add_decision(self,*,field=None,text=None,status="APPROVED",dtype="METHOD",
                     decision=None):
        index=len(self.decisions)+1
        did=f"DEC-{index:04d}"
        tid=f"TRACE-{index:04d}"
        if field is not None:
            assert text is not None
            profile=json.loads(self.profile.read_text())
            profile["route_details"][field]=text
            self.profile.write_text(json.dumps(profile))
            question="Researcher methodological detail: "+field
            value=field+" formally recorded; declared value checksum "+hashlib.sha256(text.encode()).hexdigest()
        else:
            question="Fictional method route question PRIVATE_NOT_EXPORTED"
            value=decision or "QUALITATIVE"
        self.decisions.append({
            "DEC_ID":did,"Decision_type":dtype,"Decision_question":question,
            "Decision":value,"Status":status,"Decided_by":"FICTIONAL_ACTOR",
            "Trace_ID":tid,"Rationale":"PRIVATE_HUMAN_RATIONALE_4257",
            "Notes":"PRIVATE_ORIGINAL_RESPONSE_4257"})
        self.traces.append({"Trace_ID":tid,"Decision_or_output":value,
                            "Notes":"SENSITIVE_TRACE_DETAIL_4257"})
        self.save_tables()
        return did

    def test_no_decisions_means_no_invented_human_approval(self):
        res=compose(self.root,navigation=REVIEW_ONLY_NAV)
        self.assertEqual(res["last_recorded_decision"]["status"],"NO_RECORDED_DECISIONS")
        self.assertIsNone(res["last_recorded_decision"]["decision_id"])
        self.assertFalse(res["human_identity_authenticated"])
        self.assertFalse(res["scientific_gate_approved"])
        self.assertTrue(res["next_action"]["technical_preparation_already_authorized_by_router"])

    def test_latest_field_is_checksum_reconciled_and_followup_is_concrete(self):
        self.add_decision()
        did=self.add_decision(field="tradition",text="An interpretive case-study design with bounded fictional records")
        res=compose(self.root,navigation=REVIEW_ONLY_NAV)
        last=res["last_recorded_decision"]
        self.assertEqual(last["decision_id"],did)
        self.assertEqual(last["detail_field"],"tradition")
        self.assertTrue(last["field_checksum_matches_canonical"])
        self.assertTrue(last["trace_link_recorded"])
        progress=res["method_progress"]
        self.assertEqual(progress["completed_field_count"],1)
        self.assertEqual(progress["next_missing_field"],"context_or_case")
        self.assertIn("sampling_logic",progress["remaining_fields"])
        self.assertEqual(res["next_action"]["code"],"EXECUTE_RECORDED_CADA_TASK")
        self.assertEqual(res["next_action"]["existing_cada_task_id"],"CADA-0002")
        self.assertEqual(res["next_action"]["responsible"],"TECHNICAL_AGENT")
        self.assertFalse(res["next_action"]["execution_authorized_by_this_view"])
        rendered=json.dumps(res)
        for forbidden in ("PRIVATE_HUMAN_RATIONALE_4257",
                          "PRIVATE_ORIGINAL_RESPONSE_4257",
                          "SENSITIVE_TRACE_DETAIL_4257",
                          "PRIVATE_NEXT_ACTION_TO_NOT_EXPORT"):
            self.assertNotIn(forbidden,rendered)

    def test_modified_method_field_blocks_overconfident_next_action(self):
        self.add_decision()
        self.add_decision(field="tradition",text="Original recorded fictional methodological text")
        doc=json.loads(self.profile.read_text())
        doc["route_details"]["tradition"]="Changed secretly outside DEC/TRACE"
        self.profile.write_text(json.dumps(doc))
        res=compose(self.root,navigation=REVIEW_ONLY_NAV)
        self.assertEqual(res["last_recorded_decision"]["status"],
                         "METHOD_FIELD_DECISION_INCONSISTENT")
        self.assertIn("DECISION_PROVENANCE_RECONCILIATION_REQUIRED",res["blockers"])
        self.assertEqual(res["next_action"]["code"],
                         "REVIEW_CONFLICTING_METHOD_DECISION_EVIDENCE")
        self.assertFalse(res["next_action"]["technical_preparation_already_authorized_by_router"])

    def test_nonmethod_latest_decision_is_reported_without_content(self):
        self.add_decision()
        self.add_decision(status="PROPOSED",dtype="SCOPE",decision="SECRET_NONMETHOD_DECISION")
        r=compose(self.root,navigation=REVIEW_ONLY_NAV)
        self.assertEqual(r["last_recorded_decision"]["decision_id"],"DEC-0002")
        self.assertEqual(r["last_recorded_decision"]["recorded_status"],"PROPOSED")
        self.assertEqual(r["last_recorded_decision"]["decision_type"],"SCOPE")
        self.assertNotIn("SECRET_NONMETHOD_DECISION",json.dumps(r))

    def test_unverified_drive_takes_priority_over_method_or_agent(self):
        self.add_decision()
        self.config.write_text(json.dumps({
            "presentation_mode":"MINIMAL",
            "storage_mode":"GOOGLE_DRIVE",
            "method_route":"QUALITATIVE",
            "method_route_governance_required":True,
        }))
        res=compose(self.root)
        self.assertEqual(res["next_action"]["code"],
                         "VERIFY_AUTHORIZED_CANONICAL_STORAGE")
        self.assertFalse(res["next_action"]["technical_preparation_already_authorized_by_router"])
        self.assertTrue(res["next_action"]["blocks_substantive_progress_until_resolved"])
        self.assertIn("CANONICAL_STORAGE_NOT_VERIFIED",res["blockers"])

    def test_human_gate_is_never_automatically_approved(self):
        self.add_decision()
        nav={**REVIEW_ONLY_NAV,"status":"HUMAN_GATE_DECISION_REQUIRED",
             "technical_preparation_possible":False,"next_task_id":None}
        res=compose(self.root,navigation=nav)
        self.assertEqual(res["next_action"]["code"],
                         "RESEARCHER_REVIEW_PENDING_SCIENTIFIC_GATE")
        self.assertTrue(res["next_action"]["human_action_required_for_scientific_decision"])
        self.assertFalse(res["scientific_gate_approved"])

    def test_incomplete_route_indicates_human_method_decision(self):
        self.make_profile("UNDECIDED")
        cfg=json.loads(self.config.read_text())
        cfg["method_route"]="UNDECIDED"
        self.config.write_text(json.dumps(cfg))
        nav={**REVIEW_ONLY_NAV,"status":"HUMAN_GATE_DECISION_REQUIRED",
             "technical_preparation_possible":False,"next_task_id":None}
        r=compose(self.root,navigation=nav)
        self.assertEqual(r["next_action"]["code"],
                         "RESEARCHER_CHOOSE_AND_JUSTIFY_METHOD_ROUTE")
        self.assertEqual(r["method_progress"]["status"],
                         "RESEARCHER_ROUTE_DECISION_REQUIRED")

    def test_missing_last_decision_register_not_fabricated(self):
        (self.m/"17_Decision_Log.csv").unlink()
        res=compose(self.root,navigation=REVIEW_ONLY_NAV)
        self.assertEqual(res["last_recorded_decision"]["status"],
                         "DECISION_REGISTER_UNAVAILABLE")
        self.assertIsNone(res["last_recorded_decision"]["decision_id"])

    def test_duplicate_decisions_do_not_claim_reliable_last(self):
        self.add_decision()
        self.decisions.append(dict(self.decisions[-1]))
        self.save_tables()
        res=compose(self.root,navigation=REVIEW_ONLY_NAV)
        self.assertEqual(res["last_recorded_decision"]["status"],
                         "DECISION_REGISTER_UNAVAILABLE")
        self.assertIn("DUPLICATE_OR_MISSING_RECORD_IDENTIFIER",
                      res["last_recorded_decision"]["warnings"])

    def test_next_step_integrity_conflict_takes_priority(self):
        nav={**REVIEW_ONLY_NAV,"status":"CADA_CONTINUITY_INTEGRITY_REVIEW",
             "blockers":["CADA_CONTINUITY_INTEGRITY_REVIEW"],"technical_preparation_possible":False,
             "next_task_id":None}
        res=compose(self.root,navigation=nav)
        self.assertEqual(res["next_action"]["code"],"RECONCILE_CADA_AND_CONTINUITY")
        self.assertFalse(res["next_action"]["technical_preparation_already_authorized_by_router"])

    def test_native_panel_reads_both_views_without_changing_project(self):
        self.add_decision()
        self.add_decision(field="tradition",text="A bounded fictional case methodology")
        before={p.name:p.read_bytes() for p in self.m.iterdir() if p.is_file()}
        panel=native.panel(self.root)
        view=panel["decision_continuity"]
        self.assertEqual(view["last_recorded_decision"]["decision_id"],"DEC-0002")
        self.assertEqual(view["method_progress"]["next_missing_field"],"context_or_case")
        self.assertEqual(view["next_action"]["existing_cada_task_id"],"CADA-0002")
        self.assertIn("Last recorded decision:",native.fallback(panel))
        self.assertIn("Next responsible action:",native.fallback(panel))
        self.assertFalse(view["project_changed"])
        self.assertFalse(view["drive_sync_verified"])
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.m.iterdir() if p.is_file()})

    def test_placeholder_field_never_counts_as_completed(self):
        p=json.loads(self.profile.read_text())
        p["route_details"]["tradition"]="PENDING"
        p["route_details"]["context_or_case"]="Some fictional bounded archive"
        self.profile.write_text(json.dumps(p))
        progress=project_method_progress("QUALITATIVE",p)
        self.assertEqual(progress["completed_field_count"],1)
        self.assertEqual(progress["next_missing_field"],"tradition")
        self.assertFalse(progress["completion_is_scientific_validation"])

if __name__=="__main__":
    unittest.main()
