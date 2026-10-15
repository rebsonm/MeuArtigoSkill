"""Synthetic, read-only checks for conversational blocker explanations."""
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
from native_chat_dashboard import panel
from research_resume_brief import from_panel, SCHEMA as RESUME_SCHEMA
from research_blocker_guide import explain,text,SCHEMA,CATALOG,RECORDS

PRIVATE="CONFIDENTIAL_RESEARCH_TEXT_DONT_EXPORT_8027"

def sample(*,codes=None,status="RECONCILIATION_REQUIRED"):
    return {
        "schema":RESUME_SCHEMA,"status":status,
        "blockers":list(codes or []),
        "recorded":{"last_decision_id":None},
        "next_step":{"code":"RECONCILE_PROJECT_RECORDS"},
        "private_task_text":PRIVATE,
    }

def write_csv(path,headers,rows=None):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=headers)
        w.writeheader()
        w.writerows([{h:r.get(h,"") for h in headers} for r in (rows or [])])

class BlockerGuideUnitTests(unittest.TestCase):
    def test_storage_and_provenance_have_explained_read_only_plan(self):
        p=explain(sample(codes=[
            "DECISION_PROVENANCE_RECONCILIATION_REQUIRED",
            "CANONICAL_DRIVE_ACCESS_NOT_VERIFIED_BY_LOCAL_PANEL"]))
        self.assertEqual(p["schema"],SCHEMA)
        self.assertEqual(p["status"],"BLOCKED_REVIEW_ONLY")
        self.assertEqual(p["primary"]["code"],"CANONICAL_DRIVE_ACCESS_NOT_VERIFIED_BY_LOCAL_PANEL")
        self.assertEqual(p["primary"]["responsible"],"AUTHORIZED_OPERATOR")
        self.assertIn(RECORDS["CONFIG"],p["primary"]["canonical_records_to_review"])
        self.assertEqual(p["issues_total"],2)
        self.assertFalse(p["primary"]["automatic_repair_authorized"])
        self.assertFalse(p["no_canonical_write"] is False)
        self.assertNotIn(PRIVATE,json.dumps(p))
        self.assertNotIn(PRIVATE,text(p))

    def test_unknown_codes_are_not_echoed_or_treated_as_instructions(self):
        unknown="ATTACKER_INVENTED_AUTOMATIC_APPROVAL"
        p=explain(sample(codes=[unknown,"UNKNOWN_STRING_LOOKS_LIKE_VALID_CODE"]))
        self.assertEqual(p["issues_total"],1)
        self.assertEqual(p["primary"]["code"],"UNCLASSIFIED_RECONCILIATION_CAUSE")
        self.assertIn("cannot classify",p["primary"]["reason"])
        self.assertNotIn(unknown,json.dumps(p))
        self.assertFalse(p["primary"]["automatic_repair_authorized"])

    def test_empty_reconciliation_state_requires_inspection(self):
        x=explain(sample(codes=[]))
        self.assertEqual(x["status"],"BLOCKED_REVIEW_ONLY")
        self.assertEqual(x["primary"]["code"],"UNCLASSIFIED_RECONCILIATION_CAUSE")
        self.assertFalse(x["no_automatic_repair"] is False)

    def test_no_blocker_is_not_execution_or_scientific_approval(self):
        p=explain(sample(codes=[],status="TECHNICAL_PREPARATION_CANDIDATE"))
        self.assertEqual(p["status"],"NO_RECORDED_BLOCKER_NOT_AN_EXECUTION_APPROVAL")
        self.assertIsNone(p["primary"])
        for key in ("no_task_executed","no_gate_approved","no_canonical_write",
                    "no_automatic_repair","project_changed","drive_sync_verified"):
            self.assertEqual(p[key],key not in {"project_changed","drive_sync_verified"})
        self.assertIn("current permission checks",text(p))

    def test_missing_auth_and_transaction_recovery_have_different_owners(self):
        a=explain(sample(codes=["LOCAL_FALLBACK_AUTHORIZATION_NOT_RECORDED"]))
        self.assertEqual(a["primary"]["responsible"],"HUMAN_RESEARCHER")
        self.assertIn("only the researcher",a["primary"]["safe_read_only_next_step"])
        b=explain(sample(codes=["PENDING_RESEARCH_TRANSACTION_RECOVERY"]))
        self.assertEqual(b["primary"]["responsible"],"AUTHORIZED_OPERATOR")
        self.assertIn("do not delete",b["primary"]["safe_read_only_next_step"])

    def test_cada_and_scientific_gate_blocker_explanations(self):
        for code,owner,record in (
            ("UNFINISHED_TASK_DEPENDENCY","AUTHORIZED_OPERATOR","CADA"),
            ("UNVERIFIED_TASK_DEPENDENCY_COMPLETION","AUTHORIZED_OPERATOR","TRACE"),
            ("PRIOR_HUMAN_GATE_NOT_DOCUMENTED","HUMAN_RESEARCHER","GATES"),
            ("METHOD_PROFILE_REQUIRES_RECONCILIATION","HUMAN_RESEARCHER","METHOD"),
        ):
            with self.subTest(code=code):
                p=explain(sample(codes=[code]))
                self.assertEqual(p["primary"]["code"],code)
                self.assertEqual(p["primary"]["responsible"],owner)
                self.assertIn(RECORDS[record],
                              p["primary"]["canonical_records_to_review"])
                self.assertFalse(p["primary"]["scientific_gate_approved"])

    def test_duplicate_codes_and_presentation_limit_are_safe(self):
        p=explain(sample(codes=[
            "TASK_NOT_READY","TASK_NOT_READY","METHOD_PROFILE_REQUIRES_RECONCILIATION",
            "CANONICAL_STORAGE_NOT_VERIFIED","UNFINISHED_TASK_DEPENDENCY"]),
            limit=2)
        self.assertEqual(p["issues_total"],4)
        self.assertEqual(len(p["issues"]),2)
        self.assertEqual(p["issues_not_shown"],2)
        self.assertEqual(p["primary"]["code"],"CANONICAL_STORAGE_NOT_VERIFIED")
        self.assertIn("Additional issues not shown: 2",text(p))

    def test_static_catalog_only_uses_preapproved_filenames(self):
        self.assertTrue(CATALOG)
        for code,entry in CATALOG.items():
            with self.subTest(code=code):
                self.assertRegex(code,r"^[A-Z][A-Z0-9_]+$")
                self.assertEqual(len(entry),6)
                self.assertTrue(entry[4])
                for item in entry[4]:
                    self.assertIn(item,RECORDS)
                self.assertNotIn(PRIVATE,json.dumps(entry))
        self.assertEqual(len(CATALOG),len(set(CATALOG)))

    def test_malformed_input_is_not_repaired_or_trusted(self):
        for v in (None,{},sample(status="UNSUPPORTED"),
                  {**sample(), "schema":"INVALID"},
                  {**sample(), "blockers":PRIVATE},
                  {**sample(), "blockers":[7]}):
            with self.subTest(v=str(v)[:70]),self.assertRaises(ValueError):
                explain(v)
        for n in (0,9,True,1.5):
            with self.subTest(n=n),self.assertRaises(ValueError):
                explain(sample(),limit=n)

class BlockerGuideCanonicalProjectTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)/"fictional-project"
        self.m=self.root/MGMT
        self.m.mkdir(parents=True)
        self.config=self.m/"PROJECT_CONFIG.json"
        self.config.write_text(json.dumps({
            "storage_mode":"WORK_FALLBACK","fallback_authorized":True,
            "presentation_mode":"MINIMAL","method_route":"UNDECIDED",
            "method_route_governance_required":True,
        }))
        (self.m/"METHOD_PROFILE.json").write_text(json.dumps(new_profile("UNDECIDED")))
        (self.m/"CONTINUIDADE.md").write_text(
            "# Fictional case\nNext valid action: CADA-0001\n")
        write_csv(self.m/"11_CADA_Control.csv",
                  init_project.TABLES[f"{MGMT}/11_CADA_Control.csv"],[
            {"CADA_ID":"CADA-0001","Title":PRIVATE,"Next_action":PRIVATE,
             "Status":"READY","Execution_mode":"AUTONOMOUS",
             "Assigned_to":"AGENT","Scientific_stage":"01"}])
        write_csv(self.m/"18_Human_Validation_Gates.csv",
                  init_project.TABLES[f"{MGMT}/18_Human_Validation_Gates.csv"],[
            {"GATE_ID":f"GATE-{i:04d}","Status":"READY",
             "Decision":"PENDING","Scientific_stage":f"{i:02d}"}
            for i in range(1,8)])
        write_csv(self.m/"17_Decision_Log.csv",
                  ["DEC_ID","Decision_type","Decision_question","Decision",
                   "Status","Decided_by","Trace_ID","Rationale"],[])
        write_csv(self.m/"13_Traceability_Log.csv",
                  ["Trace_ID","Notes"],[])

    def observe(self):
        return explain(from_panel(panel(self.root)))

    def test_complete_read_only_project_flow_and_no_private_prose(self):
        before={x.name:x.read_bytes() for x in self.m.iterdir() if x.is_file()}
        result=self.observe()
        self.assertEqual(result["schema"],SCHEMA)
        self.assertTrue(result["no_task_executed"])
        self.assertFalse(result["drive_sync_verified"])
        self.assertNotIn(PRIVATE,json.dumps(result))
        self.assertEqual(before,{x.name:x.read_bytes() for x in self.m.iterdir()
                                 if x.is_file()})

    def test_missing_decision_register_causes_specific_guidance(self):
        (self.m/"17_Decision_Log.csv").unlink()
        result=self.observe()
        self.assertEqual(result["status"],"BLOCKED_REVIEW_ONLY")
        self.assertTrue(any(x["code"]=="DECISION_PROVENANCE_RECONCILIATION_REQUIRED"
                            for x in result["issues"]))
        self.assertTrue(result["no_canonical_write"])

    def test_drive_mirror_prevents_automatic_progress(self):
        cfg=json.loads(self.config.read_text())
        cfg["storage_mode"]="GOOGLE_DRIVE"
        cfg["fallback_authorized"]=False
        self.config.write_text(json.dumps(cfg))
        result=self.observe()
        self.assertEqual(result["primary"]["code"],
                         "CANONICAL_DRIVE_ACCESS_NOT_VERIFIED_BY_LOCAL_PANEL")
        self.assertTrue(result["no_task_executed"])
        self.assertTrue(result["no_gate_approved"])

    def test_method_profile_missing_cannot_be_auto_reconstructed(self):
        (self.m/"METHOD_PROFILE.json").unlink()
        result=self.observe()
        self.assertTrue(any(x["code"]=="METHOD_PROFILE_REQUIRES_RECONCILIATION"
                            for x in result["issues"]))
        self.assertFalse(result["project_changed"])

if __name__=="__main__":
    unittest.main()
