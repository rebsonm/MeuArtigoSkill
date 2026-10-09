"""Offline unit and integration safeguards for the C.A.D.A. / science boundary.

All test task rows are temporary software fixtures, not empirical outcomes.
"""
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import audit_governance_boundary as boundary
import governance_events as governance

PLAN=ROOT/"benchmarks/cada_comparison_protocol_v1.json"


class GovernanceBoundaryTests(unittest.TestCase):
    def setUp(self):
        ctx=tempfile.TemporaryDirectory()
        self.addCleanup(ctx.cleanup)
        self.root=Path(ctx.name)
        self.mgmt=self.root/boundary.MGMT
        self.mgmt.mkdir()
        self._write("11_CADA_Control.csv",
                    ["CADA_ID","Status","Completion_evidence"],
                    [{"CADA_ID":"CADA-0001","Status":"DONE",
                      "Completion_evidence":"Signed file in project workspace"}])
        self._write("18_Human_Validation_Gates.csv",
                    ["GATE_ID","Status","Decision","Validation_method","Validation_evidence"],
                    [{"GATE_ID":"GATE-0001","Status":"COMPLETED","Decision":"APPROVED",
                      "Validation_method":"Researcher review of protocol",
                      "Validation_evidence":"Dated direct researcher response retained in project"}])
        self._write("05_Evidence_Matrix.csv",["Evidence_ID"],
                    [{"Evidence_ID":"EVID-0001"}])
        self._write("09_Claims_Ledger.csv",["Claim_ID"],
                    [{"Claim_ID":"CLAIM-0001"}])
        self._write("17_Decision_Log.csv",["DEC_ID"],
                    [{"DEC_ID":"DEC-0001"}])
        self._write("13_Traceability_Log.csv",["Trace_ID","Status"],
                    [{"Trace_ID":"TRACE-0001","Status":"UNVERIFIED"}])

    def _write(self,name,headers,items):
        with (self.mgmt/name).open("w",encoding="utf-8-sig",newline="") as f:
            wr=csv.DictWriter(f,fieldnames=headers)
            wr.writeheader()
            wr.writerows(items)

    def _run(self,*args):
        return subprocess.run([sys.executable,str(ROOT/"scripts/audit_governance_boundary.py"),
                               *map(str,args)],text=True,capture_output=True)

    def test_independent_categories_never_reduce_to_one_score(self):
        r=boundary.audit(self.root,strict=True)
        self.assertEqual(r["integrity"]["errors"],[])
        self.assertEqual(r["management_activity"]["tasks_marked_done"],1)
        self.assertEqual(r["scientific_registers"]["gate_approvals_recorded"],1)
        self.assertEqual(r["execution_provenance"]["unverified"],1)
        self.assertFalse(r["scientific_quality_validated"])
        self.assertFalse(r["causal_CADA_effect_established"])
        self.assertNotIn("scientific_quality_score",r)

    def test_done_task_without_evidence_is_not_proven(self):
        self._write("11_CADA_Control.csv",["CADA_ID","Status","Completion_evidence"],
                    [{"CADA_ID":"CADA-0001","Status":"DONE","Completion_evidence":""}])
        r=boundary.audit(self.root,strict=True)
        self.assertTrue(any("completion evidence" in x for x in r["integrity"]["errors"]))

    def test_task_id_is_not_adequate_completion_proof(self):
        self._write("11_CADA_Control.csv",["CADA_ID","Status","Completion_evidence"],
                    [{"CADA_ID":"CADA-0001","Status":"DONE",
                      "Completion_evidence":"CADA-0002"}])
        self.assertEqual(boundary.audit(self.root)["management_activity"]["done_without_meaningful_completion_evidence"],1)

    def test_scientific_gate_cannot_rely_only_on_cada_done(self):
        self._write("18_Human_Validation_Gates.csv",
                    ["GATE_ID","Status","Decision","Validation_method","Validation_evidence"],
                    [{"GATE_ID":"GATE-0001","Status":"COMPLETED","Decision":"APPROVED",
                      "Validation_method":"CADA DONE","Validation_evidence":"CADA-0001"}])
        report=boundary.audit(self.root,strict=True)
        self.assertTrue(any("scientific approval" in msg for msg in report["integrity"]["errors"]))

    def test_gate_not_completed_is_not_scientifically_approved(self):
        self._write("18_Human_Validation_Gates.csv",
                    ["GATE_ID","Status","Decision"],
                    [{"GATE_ID":"GATE-0001","Status":"READY","Decision":"PENDING"}])
        self.assertEqual(boundary.audit(self.root)["scientific_registers"]["gate_approvals_recorded"],0)

    def test_trace_legacy_complete_not_confirmed(self):
        self._write("13_Traceability_Log.csv",["Trace_ID","Status"],
                    [{"Trace_ID":"TRACE-0001","Status":"COMPLETE"}])
        self.assertEqual(boundary.audit(self.root)["execution_provenance"]["locally_confirmed"],0)

    def test_report_written_only_inside_workspace(self):
        result=self._run("audit",self.root,"--strict","--output",
                         "00_Gestao_e_Continuidade/GOVERNANCE_BOUNDARY_REPORT.json")
        self.assertEqual(result.returncode,0,result.stderr)
        path=self.mgmt/"GOVERNANCE_BOUNDARY_REPORT.json"
        obj=json.loads(path.read_text(encoding="utf-8"))
        self.assertFalse(obj["scientific_quality_validated"])
        self.assertFalse(obj["causal_CADA_effect_established"])

    def test_prevent_audit_file_write_outside_project(self):
        result=self._run("audit",self.root,"--output","../uncontrolled.json")
        self.assertNotEqual(result.returncode,0)

    def test_existing_report_separates_management_from_scientific_status(self):
        from generate_transparency_report import report_data
        x=report_data(self.root)
        self.assertEqual(x["governance_boundary"]["management_activity"]["recorded_tasks"],1)
        self.assertEqual(x["governance_boundary"]["scientific_registers"]["evidence_records"],1)

    def test_research_gate_denies_cada_only_validation(self):
        cfg=self.mgmt/"PROJECT_CONFIG.json"
        cfg.write_text(json.dumps({"cada_science_boundary_required":True}),encoding="utf-8")
        self._write("18_Human_Validation_Gates.csv",governance.GATE_HEADERS,
                    [{"GATE_ID":"GATE-0001","Status":"READY","Name":"Research question"}])
        command=[sys.executable,str(ROOT/"scripts/governance_events.py"),"gate",
                 str(self.root),"--gate-id","GATE-0001","--decision","APPROVED",
                 "--validated-by","Researcher","--method","CADA",
                 "--evidence","CADA-0001","--no-snapshot"]
        result=subprocess.run(command,capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn("C.A.D.A. task status",result.stderr)
        # The pre-existing TRACE row must remain unchanged on rejected approval.
        with (self.mgmt/"13_Traceability_Log.csv").open(encoding="utf-8-sig",newline="") as stream:
            self.assertEqual(len(list(csv.DictReader(stream))),1)

    def test_comparison_protocol_structure_only_is_valid(self):
        report=boundary.protocol_check(PLAN)
        self.assertEqual(report["status"],"PROTOCOL_STRUCTURE_VALID")
        self.assertFalse(report["comparison_executed"])
        self.assertFalse(report["scientific_effect_established"])

    def test_comparison_protocol_preserves_scientific_gates_in_both_arms(self):
        plan=json.loads(PLAN.read_text(encoding="utf-8"))
        self.assertEqual({a["scientific_gates"] for a in plan["arms"]},{"SAME_REQUIRED_GATES"})
        self.assertEqual({a["scientific_protocol"] for a in plan["arms"]},{"SAME_FROZEN_RESEARCH_PROTOCOL"})

    def test_plan_rejects_fake_results(self):
        plan=json.loads(PLAN.read_text(encoding="utf-8"))
        plan["results"]={"time_saved_hours":200}
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"protocol.json"
            path.write_text(json.dumps(plan),encoding="utf-8")
            self.assertTrue(boundary.protocol_check(path)["errors"])

    def test_plan_rejects_identical_management_arms(self):
        plan=json.loads(PLAN.read_text(encoding="utf-8"))
        plan["arms"][1]["management_layer_enabled"]=True
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"protocol.json"
            path.write_text(json.dumps(plan),encoding="utf-8")
            self.assertTrue(boundary.protocol_check(path)["errors"])

    def test_project_config_enables_boundary_for_new_projects(self):
        src=(ROOT/"scripts/init_project.py").read_text(encoding="utf-8")
        self.assertIn('"cada_science_boundary_required":True',src)

    def test_read_only_empty_project_never_looks_like_effect_measurement(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)
            (p/boundary.MGMT).mkdir()
            r=boundary.audit(p,strict=False)
            self.assertEqual(r["management_activity"]["recorded_tasks"],0)
            self.assertEqual(r["scientific_registers"]["claims_registered"],0)
            self.assertFalse(r["causal_CADA_effect_established"])


if __name__=="__main__":
    unittest.main()
