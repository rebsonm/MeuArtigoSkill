"""Stage 15 horizontal integration — synthetic-only canonical read projections.

The four consumers must agree on identifiers, not on scientific certainty.
All tests operate on disposable local files and do not call cloud APIs.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import test_native_chat_dashboard as fixture
import native_chat_dashboard as native
import build_research_workspace as workspace
import build_research_site as site
from fictional_method_projection import fictional_projection
from method_routes import ROUTES
from method_decision_dimensions import DIMENSIONS

class Stage15HorizontalTests(unittest.TestCase):
    def local(self):
        case=fixture.NativeChatDashboardTests(
            "test_minimal_has_five_views_and_no_scientific_percentage")
        case.setUp()
        self.addCleanup(case.doCleanups)
        return case

    def test_cross_projection_full_tasks_gates_next_action(self):
        case=self.local()
        native_data=native.panel(case.root,mode="FULL")
        skill=workspace.model(project=case.root,mode="FULL")
        website=site.project_site_model(skill)
        self.assertEqual(website["kind"],"CANONICAL_LOCAL_SNAPSHOT")
        self.assertEqual(website["tasks"],native_data["tasks"]["items"])
        self.assertEqual([x["id"] for x in website["gates"]],
                         [x["id"] for x in native_data["gates"]["items"]])
        self.assertEqual(website["registered_gate_total"],
                         native_data["gates"]["registered_total"])
        self.assertFalse(website["gate_view_partial"])
        self.assertEqual(website["documented_gate_count"],
                         native_data["overview"]["documented_gate_approvals"])
        self.assertEqual(website["next_action"]["code"],
                         native_data["decision_continuity"]["next_action"]["code"])
        self.assertEqual(skill["decision_continuity"],
                         native_data["decision_continuity"])
        self.assertEqual(skill["scientific_diagnostic"],
                         native_data["scientific_diagnostic"])

    def test_minimal_partial_gates_never_misstate_total(self):
        case=self.local()
        native_data=native.panel(case.root,mode="MINIMAL")
        view=workspace.model(project=case.root,mode="MINIMAL")
        website=site.project_site_model(view)
        self.assertTrue(native_data["gates"]["items_partial"])
        self.assertTrue(view["human_gates"]["items_partial"])
        self.assertTrue(website["gate_view_partial"])
        self.assertEqual(website["registered_gate_total"],4)
        self.assertEqual(len(website["gates"]),3)
        self.assertEqual(website["documented_gate_count"],1)
        self.assertFalse(website["automatic_scientific_approval"])

    def test_minimal_hides_fourth_approval_without_claiming_zero(self):
        case=self.local()
        case.write("18_Human_Validation_Gates.csv",[
            {"GATE_ID":f"GATE-000{i}","Status":"COMPLETED" if i==4 else "READY",
             "Decision":"APPROVED" if i==4 else "PENDING",
             "Validated_by":"RESEARCHER" if i==4 else "",
             "Validation_evidence":"synthetic human record" if i==4 else ""}
            for i in range(1,8)])
        tiny=native.panel(case.root,mode="MINIMAL")
        full=native.panel(case.root,mode="FULL")
        shown=site.project_site_model(workspace.model(project=case.root,mode="MINIMAL"))
        complete=site.project_site_model(workspace.model(project=case.root,mode="FULL"))
        self.assertEqual(tiny["overview"]["documented_gate_approvals"],1)
        self.assertEqual(shown["documented_gate_count"],0)
        self.assertTrue(shown["gate_view_partial"])
        self.assertEqual(shown["registered_gate_total"],7)
        self.assertEqual(complete["documented_gate_count"],1)
        self.assertFalse(complete["gate_view_partial"])
        self.assertFalse(complete["automatic_scientific_approval"])

    def test_site_rejects_impossible_partiality_or_gate_totals(self):
        example=workspace.model(route="QUALITATIVE")
        example["is_project_bound"]=True
        example["human_gates"]={"items":[
            {"id":"GATE-0001","approval_documented":False}],
            "total":0,"items_partial":False}
        with self.assertRaisesRegex(ValueError,"SITE_GATE_TOTAL_BELOW_VISIBLE"):
            site.project_site_model(example)
        example["human_gates"]["total"]=7
        example["human_gates"]["items_partial"]="YES"
        with self.assertRaisesRegex(ValueError,"SITE_GATE_PARTIAL_FLAG_INVALID"):
            site.project_site_model(example)
        example["human_gates"]["items_partial"]=False
        view=site.project_site_model(example)
        self.assertTrue(view["gate_view_partial"])

    def test_full_and_minimal_read_do_not_mutate_project(self):
        case=self.local()
        before={p.name:p.read_bytes() for p in case.mgmt.iterdir() if p.is_file()}
        for mode in ("MINIMAL","FULL"):
            native.panel(case.root,mode=mode)
            ws=workspace.model(project=case.root,mode=mode)
            output=site.render_site(ws)
            self.assertIn('"kind":"CANONICAL_LOCAL_SNAPSHOT"',output)
        self.assertEqual(before,{p.name:p.read_bytes() for p in case.mgmt.iterdir() if p.is_file()})

    def test_forbidden_private_passages_not_across_consumers(self):
        case=self.local()
        prohibited=["SECRET_SOURCE_PATH","COPYRIGHTED_AND_PRIVATE_PASSAGE",
                    "PRIVATE_ORIGINAL_MESSAGE","SECRET_RESPONSE_TEXT",
                    "Sensitive internal action","CONFIDENTIAL"]
        for mode in ("MINIMAL","FULL"):
            native_data=native.panel(case.root,mode=mode)
            skill=workspace.model(project=case.root,mode=mode)
            model=site.project_site_model(skill)
            packed=" ".join(json.dumps(x,ensure_ascii=False) for x in
                            (native_data,skill,model))
            for secret in prohibited:
                self.assertNotIn(secret,packed)
            self.assertFalse(model["canonical_drive_sync_verified"])
            self.assertFalse(model["automatic_scientific_approval"])
            self.assertFalse(model["canonical_writes_allowed"])
            self.assertFalse(skill["preflight_contract"]["automatic_write_possible"])

    def test_missing_drive_sync_and_scientific_evidence_stay_unknown(self):
        case=self.local()
        n=native.panel(case.root)
        site_data=site.project_site_model(workspace.model(project=case.root))
        self.assertFalse(n["drive_sync_verified_in_this_session"])
        self.assertFalse(n["scientific_quality_independently_validated"])
        self.assertIsNone(n["evidence"]["verified_sources"])
        self.assertFalse(site_data["canonical_drive_sync_verified"])
        diag=site_data.get("scientific_diagnostic")
        if diag is not None:
            self.assertFalse(diag["scientific_quality_validated"])
            self.assertFalse(diag["scientific_gate_approved"])
            self.assertFalse(diag["drive_sync_verified"])

    def test_unknown_scientific_diagnostic_never_means_zero(self):
        case=self.local()
        ui=site.project_site_model(workspace.model(project=case.root))
        d=ui["scientific_diagnostic"]
        if d is not None and d["status"]=="INPUTS_UNAVAILABLE":
            self.assertIsNone(d["objective_blockers"])
            self.assertIsNone(d["advisory_occurrences"])

    def test_method_catalogue_all_modes_and_routes_no_writes(self):
        self.assertEqual(len(ROUTES),9)
        self.assertEqual(len(DIMENSIONS),5)
        for route in ROUTES:
            for action in ("suggest","all","decision"):
                model=fictional_projection(route,action=action)
                self.assertFalse(model["is_project_bound"])
                self.assertEqual(model["fictional_method_dialogue"]["action"],action)
                self.assertFalse(model["fictional_method_dialogue"]["selection_written"])
                self.assertFalse(model["fictional_method_dialogue"]["gate_approved"])
                ids=[x["id"] for x in model["fictional_method_dialogue"]["cards"]]
                self.assertIn("OTHER_NOT_LISTED",ids)

    def test_adversarial_route_never_selects_or_persists(self):
        for invalid in ("../../../source","APPLY","SAVE_NOW","Approve gate"):
            with self.assertRaises(ValueError):
                fictional_projection("QUALITATIVE",action=invalid)
        decision=fictional_projection("QUALITATIVE",action="decision")
        self.assertEqual(decision["fictional_method_dialogue"]["decision_status"],
                         "HUMAN_DECISION_NOT_YET_OBTAINED")

    def test_site_no_uncontrolled_script_from_task(self):
        case=self.local()
        case.write("11_CADA_Control.csv",[
           {"CADA_ID":"CADA-0042","Title":"</script><img src=x onerror=alert(1)>",
            "Assigned_to":"RESEARCHER","Status":"READY"}])
        ws=workspace.model(project=case.root,mode="FULL")
        html=site.render_site(ws)
        self.assertNotIn("</script><img src=x onerror=alert(1)>",html)
        self.assertIn("\\u003c/script\\u003e",html)

    def test_source_presence_does_not_claim_verification(self):
        case=self.local()
        (case.mgmt/"SOURCE_VERIFICATION.json").write_text(
           json.dumps({"schema_version":1,"checks":[{"result":"EXISTS_ONLY"}]}))
        n=native.panel(case.root)
        self.assertEqual(n["evidence"]["source_report_presence"],
                         "PRESENT_NOT_AUDITED")
        self.assertIsNone(n["evidence"]["verified_sources"])
        self.assertFalse(site.project_site_model(workspace.model(project=case.root))[
                         "canonical_drive_sync_verified"])

if __name__=="__main__":
    unittest.main()
