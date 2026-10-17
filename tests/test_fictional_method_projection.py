"""Stage 14: isolated read-only method projections over existing catalogues.

No real project files, private sources, human decisions or writes are used.
"""
from __future__ import annotations
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from fictional_method_projection import fictional_projection
from method_routes import ROUTES
from method_decision_dimensions import DIMENSIONS
from adaptive_method_guide import preview

class FictionalMethodProjectionTests(unittest.TestCase):
    def assert_read_only(self,projection):
        contract=projection["preview_contract"]
        self.assertTrue(contract["fictional_only"])
        for f in ("real_project_access","researcher_authenticated",
                  "write_tools_available","scientific_gate_approval_available",
                  "canonical_drive_sync_verified","server_tool_registered",
                  "standalone_server_created"):
            self.assertIs(contract[f],False)
        self.assertIs(projection["is_project_bound"],False)
        self.assertEqual(projection["snapshot_kind"],"FICTIONAL_PREVIEW_NOT_A_REAL_PROJECT")
        self.assertEqual(projection["tasks"]["items"],[])
        self.assertEqual(projection["human_gates"]["items"],[])
        self.assertIs(projection["overview"]["independent_scientific_validation"],False)
        decision=projection["fictional_method_dialogue"]
        for f in ("selection_written","gate_approved","canonical_state_modified",
                  "method_recommended_or_selected","drive_sync_verified",
                  "human_reviewer_authenticated"):
            self.assertIs(decision[f],False)
        self.assertIs(decision["human_action"]["required_to_commit_scientific_choice"],True)

    def test_all_eight_families_and_undecided_remain_fictional(self):
        self.assertEqual(len(ROUTES),9)
        self.assertIn("UNDECIDED",ROUTES)
        for route in ROUTES:
            for mode in ("MINIMAL","FULL"):
                with self.subTest(route=route,mode=mode):
                    p=fictional_projection(route,mode)
                    self.assertEqual(p["active_route"],route)
                    self.assert_read_only(p)
                    ids=[c["id"] for c in p["fictional_method_dialogue"]["cards"]]
                    self.assertIn("OTHER_NOT_LISTED",ids)
                    self.assertTrue(p["fictional_method_dialogue"]["shown_as_unranked_catalogue_examples"])

    def test_all_five_dimensions_keep_unlisted_option(self):
        self.assertEqual(len(DIMENSIONS),5)
        for route in ROUTES:
            if route=="UNDECIDED":continue
            for dimension in DIMENSIONS:
                with self.subTest(route=route,dimension=dimension):
                    p=fictional_projection(route,"MINIMAL",dimension=dimension)
                    self.assert_read_only(p)
                    self.assertEqual(p["fictional_method_dialogue"]["decision_dimension"],dimension)
                    ids=[c["id"] for c in p["fictional_method_dialogue"]["cards"]]
                    self.assertIn("OTHER_NOT_LISTED",ids)
        with self.assertRaises(ValueError):
            fictional_projection("UNDECIDED",dimension="sampling")

    def test_suggest_is_unranked_and_is_not_advice_from_private_question(self):
        p=fictional_projection("QUALITATIVE",action="suggest",dimension="sampling")
        d=p["fictional_method_dialogue"]
        self.assertEqual(d["action"],"suggest")
        self.assertLessEqual(len(d["cards"]),4)
        self.assertFalse(d["researcher_question_inferred_from_text"])
        self.assert_read_only(p)

    def test_explore_explains_limits_without_selecting_method(self):
        p=fictional_projection("QUALITATIVE",action="explore",
                               dimension="sampling",option_id="PURPOSIVE")
        d=p["fictional_method_dialogue"]
        self.assertEqual(d["selected_for_exploration"],"PURPOSIVE")
        self.assertEqual(len(d["cards"]),1)
        self.assertTrue(d["cards"][0]["limits"])
        self.assertTrue(d["cards"][0]["required_human_decision"])
        self.assert_read_only(p)

    def test_compare_explains_two_options_without_winner(self):
        p=fictional_projection("QUANTITATIVE",action="compare",dimension="sampling",
                               compare_ids=("PROBABILITY","NONPROBABILITY"))
        d=p["fictional_method_dialogue"]
        self.assertEqual([x["id"] for x in d["compared"]],
                         ["PROBABILITY","NONPROBABILITY"])
        self.assertNotEqual(d["compared"][0]["limits"],d["compared"][1]["limits"])
        self.assert_read_only(p)

    def test_all_preserves_all_catalogue_members_and_other(self):
        p=fictional_projection("QUALITATIVE",action="all")
        d=p["fictional_method_dialogue"]
        self.assertEqual(len(d["cards"]),d["option_count"])
        self.assertEqual(d["cards"][-1]["id"],"OTHER_NOT_LISTED")
        self.assert_read_only(p)

    def test_decision_prompts_human_with_no_commit(self):
        p=fictional_projection("MIXED_METHODS",action="decision")
        d=p["fictional_method_dialogue"]
        self.assertEqual(d["decision_status"],"HUMAN_DECISION_NOT_YET_OBTAINED")
        self.assertIn("researcher decision",d["navigation_question"])
        self.assert_read_only(p)

    def test_invalid_actions_options_compare_and_route_fail_closed(self):
        bad=[
            dict(route="../../private"),dict(route="",mode="MINIMAL"),
            dict(route="QUALITATIVE",mode="WRITE"),
            dict(route="QUALITATIVE",action="commit"),
            dict(route="QUALITATIVE",dimension="personal_file"),
            dict(route="QUALITATIVE",action="explore",option_id="../private"),
            dict(route="QUALITATIVE",action="compare",compare_ids=("CASE_STUDY","CASE_STUDY")),
            dict(route="QUALITATIVE",action="compare",compare_ids=("CASE_STUDY","INVENTED")),
            dict(route="QUALITATIVE",action="suggest",option_id="CASE_STUDY"),
        ]
        for item in bad:
            with self.subTest(item=item),self.assertRaises(ValueError):
                fictional_projection(**item)

    def test_cli_never_accepts_project_path_or_writes_files(self):
        with tempfile.TemporaryDirectory() as td:
            home=Path(td)
            path=ROOT/"scripts/fictional_method_projection.py"
            cmd=[sys.executable,"-E","-s",str(path),"--route","QUALITATIVE",
                 "--dimension","sampling","--action","decision"]
            good=subprocess.run(cmd,cwd=home,capture_output=True,text=True,check=True)
            result=json.loads(good.stdout)
            self.assert_read_only(result)
            denied=subprocess.run(cmd+["/unauthorized/project"],cwd=home,
                                  capture_output=True,text=True)
            self.assertNotEqual(denied.returncode,0)
            self.assertEqual(list(home.iterdir()),[])

    def test_deterministic_model_and_no_private_data_exports(self):
        a=fictional_projection("CONCEPTUAL_THEORY",action="all",dimension="reporting")
        b=fictional_projection("CONCEPTUAL_THEORY",action="all",dimension="reporting")
        self.assertEqual(a,b)
        packed=json.dumps(a,sort_keys=True)
        self.assertNotIn("SECRET_PRIVATE_SOURCE_774",packed)
        self.assertFalse(a["permissions"]["canonical_write"]!="NOT_AVAILABLE_IN_THIS_UI")

    def test_single_existing_server_not_replaced(self):
        old_server=ROOT/("m"+"cp-preview")
        official=ROOT/"integrations"/("m"+"cp-apps")/"server.mjs"
        self.assertFalse(old_server.exists())
        self.assertTrue(official.is_file())
        source=official.read_text(encoding="utf-8")
        self.assertEqual(source.count("registerAppTool("),1)
        self.assertNotIn("fictional_method_projection",source)

if __name__=="__main__":
    unittest.main()
