"""Safe read-only methodological dialogue, across route families."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from adaptive_method_guide import preview, for_project
from method_choice_dialogue import dialogue
from method_routes import ROUTES, new_profile
import native_chat_dashboard as native

class MethodDialogueTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.mgmt=self.root/"00_Gestao_e_Continuidade"
        self.mgmt.mkdir()

    def configure(self,route="QUALITATIVE"):
        (self.mgmt/"PROJECT_CONFIG.json").write_text(json.dumps({
            "method_route":route,"presentation_mode":"MINIMAL",
            "storage_mode":"GOOGLE_DRIVE"}))
        (self.mgmt/"METHOD_PROFILE.json").write_text(json.dumps(new_profile(route)))
        (self.mgmt/"CONTINUIDADE.md").write_text(
            "# Fictional project continuity; no actual scientific approvals\n")

    def test_initial_two_or_three_methods_plus_an_open_path(self):
        for route,dimension in (
            ("QUALITATIVE","analysis"),
            ("QUANTITATIVE","sampling"),
            ("MIXED_METHODS","inference"),
            ("SYSTEMATIC_REVIEW","analysis"),
            ("CONCEPTUAL_THEORY","reporting"),
            ("DESIGN_SCIENCE","analysis")):
            with self.subTest(route=route):
                doc=dialogue(preview(route,dimension=dimension))
                self.assertEqual(doc["action"],"suggest")
                self.assertLessEqual(len(doc["cards"]),4)
                self.assertEqual(doc["cards"][-1]["id"],"OTHER_NOT_LISTED")
                self.assertTrue(doc["shown_as_unranked_catalogue_examples"])
                self.assertFalse(doc["researcher_question_inferred_from_text"])
                self.assertFalse(doc["method_recommended_or_selected"])
                self.assertFalse(doc["canonical_state_modified"])
                self.assertTrue(doc["human_action"]["required_to_commit_scientific_choice"])

    def test_explore_shows_consequences_and_human_responsibility(self):
        source=preview("QUALITATIVE",dimension="sampling")
        res=dialogue(source,action="explore",option_id="PURPOSIVE")
        self.assertEqual(res["selected_for_exploration"],"PURPOSIVE")
        self.assertEqual(len(res["cards"]),1)
        self.assertTrue(res["cards"][0]["potential"])
        self.assertTrue(res["cards"][0]["what_changes_next"])
        self.assertEqual(len(res["cards"][0]["reflective_questions"]),4)
        self.assertTrue(res["cards"][0]["required_human_decision"])
        self.assertFalse(res["gate_approved"])
        self.assertFalse(res["selection_written"])

    def test_compare_reveals_tradeoffs_not_a_winner(self):
        src=preview("QUANTITATIVE",dimension="sampling")
        report=dialogue(src,action="compare",compare_ids=("PROBABILITY","NONPROBABILITY"))
        self.assertEqual(len(report["compared"]),2)
        self.assertEqual([x["id"] for x in report["compared"]],["PROBABILITY","NONPROBABILITY"])
        self.assertNotEqual(report["compared"][0]["limits"],report["compared"][1]["limits"])
        self.assertFalse(report["method_recommended_or_selected"])
        self.assertFalse(report["selection_written"])
        self.assertFalse(report["gate_approved"])
        self.assertIn("request_human_decision",report["next_choices"])

    def test_all_options_and_other_tradition_stay_accessible(self):
        source=preview("QUALITATIVE")
        limited=dialogue(source)
        all_options=dialogue(source,action="all")
        self.assertLess(len(limited["cards"]),len(all_options["cards"]))
        self.assertEqual(len(all_options["cards"]),source["option_count"])
        self.assertEqual(all_options["cards"][-1]["id"],"OTHER_NOT_LISTED")
        other=dialogue(source,action="explore",option_id="OTHER_NOT_LISTED")
        self.assertEqual(other["selected_for_exploration"],"OTHER_NOT_LISTED")
        self.assertTrue(other["cards"][0]["limits"])
        self.assertTrue(other["human_action"]["required_to_commit_scientific_choice"])

    def test_decision_request_is_only_a_question_never_an_approval(self):
        src=preview("MIXED_METHODS",dimension="analysis")
        report=dialogue(src,action="decision")
        self.assertEqual(report["decision_status"],"HUMAN_DECISION_NOT_YET_OBTAINED")
        self.assertIn("actual attributable researcher decision",report["navigation_question"])
        self.assertFalse(report["selection_written"])
        self.assertFalse(report["human_reviewer_authenticated"])
        self.assertFalse(report["gate_approved"])
        self.assertTrue(report["human_action"]["required_to_commit_scientific_choice"])

    def test_methodology_not_applicable_returns_other_without_empirical_invention(self):
        res=dialogue(preview("CONCEPTUAL_THEORY",dimension="sampling"))
        self.assertEqual(res["status"],"NOT_UNIVERSALLY_APPLICABLE")
        self.assertEqual([x["id"] for x in res["cards"]],["OTHER_NOT_LISTED"])
        self.assertFalse(res["gate_approved"])

    def test_invalid_option_ids_and_duplicate_comparison_are_rejected(self):
        src=preview("QUALITATIVE")
        with self.assertRaisesRegex(ValueError,"existing option"):
            dialogue(src,action="explore",option_id="INVENTED_METHOD")
        for ids in (("CASE_STUDY","CASE_STUDY"),("CASE_STUDY","INVENTED_METHOD")):
            with self.assertRaisesRegex(ValueError,"two distinct"):
                dialogue(src,action="compare",compare_ids=ids)
        with self.assertRaisesRegex(ValueError,"only allowed"):
            dialogue(src,action="suggest",option_id="CASE_STUDY")
        with self.assertRaisesRegex(ValueError,"Unknown"):
            dialogue(src,action="submit_review")

    def test_unavailable_project_asks_reconciliation_not_method_approval(self):
        unavailable={"mode":"UNAVAILABLE","status":"NO_SAFE_METHOD_PROFILE",
                     "options":[]}
        report=dialogue(unavailable)
        self.assertEqual(report["status"],"GUIDANCE_UNAVAILABLE_RECONCILIATION_REQUIRED")
        self.assertEqual(report["cards"],[])
        self.assertTrue(report["human_action"]["required_now_to_explore"])
        self.assertFalse(report["gate_approved"])
        with self.assertRaisesRegex(ValueError,"Reconcile"):
            dialogue(unavailable,action="decision")

    def test_no_private_research_text_leaks_from_real_project_or_changes_files(self):
        self.configure("QUALITATIVE")
        path=self.mgmt/"METHOD_PROFILE.json"
        record=json.loads(path.read_text())
        record["research_question"]="CONFIDENTIAL_RESEARCH_QUESTION_7684"
        record["human_route_rationale"]="PRIVATE_HUMAN_RATIONALE_7684"
        path.write_text(json.dumps(record))
        before={p.name:p.read_bytes() for p in self.mgmt.iterdir()}
        guide=for_project(self.root,dimension="analysis")
        res=dialogue(guide,action="compare",
                     compare_ids=("REFLEXIVE_THEMATIC","NARRATIVE_INTERPRETATION"))
        self.assertNotIn("CONFIDENTIAL_RESEARCH_QUESTION_7684",json.dumps(res))
        self.assertNotIn("PRIVATE_HUMAN_RATIONALE_7684",json.dumps(res))
        self.assertFalse(res["source_evidence_verified_by_dialogue"])
        self.assertFalse(res["drive_sync_verified"])
        self.assertFalse(res["canonical_state_modified"])
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.mgmt.iterdir()})

    def test_native_panel_exposes_small_readonly_method_dialogue(self):
        self.configure("QUALITATIVE")
        panel=native.panel(self.root,mode="MINIMAL")
        conv=panel["method_conversation"]
        self.assertEqual(conv["schema"],"MEU_ARTIGO_METHOD_DIALOGUE_V1")
        self.assertEqual(conv["action"],"suggest")
        self.assertEqual(len(conv["cards"]),4)
        self.assertEqual(conv["cards"][-1]["id"],"OTHER_NOT_LISTED")
        self.assertFalse(conv["selection_written"])
        self.assertFalse(conv["gate_approved"])
        self.assertIn("Method dialogue:",native.fallback(panel))

    def test_legacy_panel_stays_safe_without_recorded_route(self):
        self.configure("QUALITATIVE")
        cfg=self.mgmt/"PROJECT_CONFIG.json"
        item=json.loads(cfg.read_text())
        item.pop("method_route")
        cfg.write_text(json.dumps(item))
        report=native.panel(self.root)
        self.assertEqual(report["method_conversation"]["status"],
                         "GUIDANCE_UNAVAILABLE_RECONCILIATION_REQUIRED")
        self.assertEqual(report["method_conversation"]["cards"],[])
        self.assertFalse(report["method_conversation"]["gate_approved"])

    def test_every_route_has_non_scientifically_ranking_navigation(self):
        for route in ROUTES:
            with self.subTest(route=route):
                g=preview(route)
                r=dialogue(g)
                self.assertFalse(r["method_recommended_or_selected"])
                self.assertFalse(r["gate_approved"])
                self.assertFalse(r["selection_written"])
                self.assertTrue(r["human_action"]["required_to_commit_scientific_choice"])

if __name__=="__main__":
    unittest.main()
