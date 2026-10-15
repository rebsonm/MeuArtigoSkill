"""Method-choice orientation: methodological pluralism, safety and continuity.

Synthetic engineering tests only. They do not scientifically validate a
methodological recommendation or claim authenticated researcher approval.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import adaptive_method_guide as guide
import method_routes
import native_chat_dashboard as native

class AdaptiveMethodGuideTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.mgmt=self.root/"00_Gestao_e_Continuidade"
        self.mgmt.mkdir()
        (self.mgmt/"CONTINUIDADE.md").write_text(
            "# Synthetic project continuity\nNo certified human approval.\n",
            encoding="utf-8")
        self.configure("QUALITATIVE")

    def configure(self,route):
        cfg={"method_route":route,"method_route_governance_required":True,
             "presentation_mode":"MINIMAL","storage_mode":"GOOGLE_DRIVE"}
        (self.mgmt/"PROJECT_CONFIG.json").write_text(json.dumps(cfg),encoding="utf-8")
        doc=method_routes.new_profile(route)
        (self.mgmt/"METHOD_PROFILE.json").write_text(json.dumps(doc),encoding="utf-8")
        return doc

    def test_unranked_all_method_families_and_explicit_other(self):
        p=guide.preview()
        self.assertEqual(p["mode"],"DISCOVER_METHOD_FAMILY")
        self.assertEqual(p["status"],"ILLUSTRATIVE_PREVIEW")
        ids={x["id"] for x in p["options"]}
        self.assertEqual(ids,set(method_routes.ROUTES)-{"UNDECIDED"} | {"OTHER_NOT_LISTED"})
        self.assertEqual(p["option_count"],9)
        self.assertTrue(p["all_options_unranked"])
        self.assertTrue(p["other_method_allowed"])
        self.assertFalse(p["researcher_selection_recorded"])
        self.assertFalse(p["researcher_goal_inferred_from_prose"])
        self.assertFalse(p["human_scientific_gate_approved"])
        self.assertFalse(p["selection_persists_to_project"])
        self.assertFalse(p["route_previously_human_confirmed"])
        self.assertTrue(all(x["recommendation_rank"] is None for x in p["options"]))

    def test_qualitative_traditions_are_distinct_not_a_fixed_generic_method(self):
        p=guide.for_project(self.root)
        self.assertEqual(p["route_recorded"],"QUALITATIVE")
        self.assertEqual(p["target_field"],"tradition")
        self.assertEqual(p["status"],"OPTIONS_FOR_HUMAN_EXPLORATION")
        ids={x["id"] for x in p["options"]}
        for key in ("PHENOMENOLOGY","CASE_STUDY","ETHNOGRAPHY",
                    "GROUNDED_THEORY","NARRATIVE","OTHER_NOT_LISTED"):
            self.assertIn(key,ids)
        self.assertTrue(all(x["when_to_consider"] and x["limits"]
                            and x["what_changes_next"] for x in p["options"]))
        self.assertFalse(p["human_action"]["needed_now_to_browse"])
        self.assertTrue(p["human_action"]["needed_to_confirm_scientific_choice"])

    def test_all_current_method_routes_have_advisory_field_options(self):
        for route in method_routes.ROUTES:
            with self.subTest(route=route):
                self.configure(route)
                actual=guide.for_project(self.root)
                self.assertTrue(actual["option_count"]>=3)
                self.assertIn("OTHER_NOT_LISTED",{x["id"] for x in actual["options"]})
                self.assertEqual(actual["route_recorded"],route)
                self.assertFalse(actual["human_scientific_gate_approved"])
                self.assertTrue(actual["technical_preparation_possible"])
                self.assertTrue(actual["human_action"]["needed_to_confirm_scientific_choice"])

    def test_prototype_not_restricted_to_qualitative_or_empirical_methods(self):
        for route,choice in (
            ("SYSTEMATIC_REVIEW","PHENOMENON_OR_EXPERIENCE"),
            ("PROBLEMATIZING_REVIEW","DOMINANT_ASSUMPTION"),
            ("CONCEPTUAL_THEORY","CONCEPTUAL_INCONSISTENCY"),
            ("QUANTITATIVE","PREDICTIVE"),
            ("MIXED_METHODS","CONVERGENT"),
            ("DESIGN_SCIENCE","DEFINED_USE_CASE"),
        ):
            with self.subTest(route=route):
                self.configure(route)
                p=guide.for_project(self.root)
                self.assertIn(choice,{x["id"] for x in p["options"]})

    def test_field_specific_options_and_generic_fallback_without_autoselection(self):
        self.configure("QUALITATIVE")
        result=guide.for_project(self.root,field="material_sources")
        self.assertIn("DOCUMENTS",{x["id"] for x in result["options"]})
        self.assertIn("OBSERVATION",{x["id"] for x in result["options"]})
        result=guide.for_project(self.root,field="reflexivity_or_positioning")
        self.assertIn("COMPARE_FRAMEWORKS",{x["id"] for x in result["options"]})
        self.assertFalse(result["researcher_selection_recorded"])
        with self.assertRaises(ValueError):
            guide.for_project(self.root,field="randomized_trial")
        with self.assertRaises(ValueError):
            guide.preview("UNDECIDED",field="research_strategy")

    def test_completed_fields_are_not_taken_as_scientifically_approved(self):
        doc=self.configure("QUANTITATIVE")
        doc["route_details"]["inference_aim"]="ASSOCIATIONAL"
        doc["route_confirmation"]="HUMAN_CONFIRMED"
        doc["research_question"]="A PRIVATE RESEARCH QUESTION"
        doc["human_route_rationale"]="PRIVATE DECISION EXPLANATION"
        (self.mgmt/"METHOD_PROFILE.json").write_text(json.dumps(doc),encoding="utf-8")
        p=guide.for_project(self.root,field="inference_aim")
        self.assertEqual(p["status"],"FIELD_ALREADY_RECORDED_REVIEW_BEFORE_CHANGE")
        self.assertTrue(p["target_field_already_recorded"])
        self.assertTrue(p["route_previously_human_confirmed"])
        self.assertFalse(p["human_scientific_gate_approved"])
        self.assertFalse(p["researcher_selection_recorded"])
        self.assertFalse(p["selection_persists_to_project"])
        self.assertEqual(p["route_detail_progress"]["fields_completed_structurally"],1)
        self.assertNotIn(doc["research_question"],json.dumps(p))
        self.assertNotIn(doc["human_route_rationale"],json.dumps(p))

    def test_profile_route_mismatch_refuses_to_guess(self):
        self.configure("QUALITATIVE")
        cfg=json.loads((self.mgmt/"PROJECT_CONFIG.json").read_text())
        cfg["method_route"]="SYSTEMATIC_REVIEW"
        (self.mgmt/"PROJECT_CONFIG.json").write_text(json.dumps(cfg))
        res=guide.for_project(self.root)
        self.assertEqual(res["status"],"METHOD_PROFILE_RECONCILIATION_REQUIRED")
        self.assertEqual(res["options"],[])
        self.assertFalse(res["technical_preparation_possible"])

    def test_missing_and_symlinked_profiles_fail_closed(self):
        profile=self.mgmt/"METHOD_PROFILE.json"
        profile.unlink()
        actual=guide.for_project(self.root)
        self.assertEqual(actual["status"],"NO_SAFE_METHOD_PROFILE")
        self.assertFalse(actual["technical_preparation_possible"])
        target=self.root/"replacement.json"
        target.write_text(json.dumps(method_routes.new_profile("QUALITATIVE")))
        profile.symlink_to(target)
        actual=guide.for_project(self.root)
        self.assertEqual(actual["status"],"NO_SAFE_METHOD_PROFILE")

    def test_nonmutating_map_in_native_panel_and_minimal_expansion(self):
        self.configure("QUALITATIVE")
        before={p.name:p.read_bytes() for p in self.mgmt.iterdir() if p.is_file()}
        p=native.panel(self.root,mode="MINIMAL")
        choices=p["method_guidance"]
        self.assertEqual(choices["route_recorded"],"QUALITATIVE")
        self.assertTrue(choices["options_partial"])
        self.assertEqual(choices["option_count"],6)
        self.assertEqual(len(choices["options"]),4)
        self.assertEqual(choices["options"][-1]["id"],"OTHER_NOT_LISTED")
        self.assertFalse(p["drive_sync_verified_in_this_session"])
        self.assertFalse(p["scientific_quality_independently_validated"])
        full=native.panel(self.root,mode="FULL")["method_guidance"]
        self.assertEqual(len(full["options"]),6)
        self.assertFalse(full["options_partial"])
        self.assertEqual({name:p.read_bytes() for name,p in
                          ((p.name,p) for p in self.mgmt.iterdir() if p.is_file())},
                         before)
        self.assertIn("Method choices:",native.fallback(p))

    def test_legacy_project_remains_compatible(self):
        cfg=json.loads((self.mgmt/"PROJECT_CONFIG.json").read_text())
        cfg.pop("method_route")
        (self.mgmt/"PROJECT_CONFIG.json").write_text(json.dumps(cfg))
        p=native.panel(self.root)
        self.assertEqual(p["method_guidance"]["status"],"NO_RECORDED_METHOD_ROUTE")
        self.assertEqual(p["method_guidance"]["options"],[])

    def test_competing_area_custom_traditions_remain_allowed(self):
        for term in ("historical","mathematical","normative","philosophical"):
            self.assertIn(term," ".join(str(v) for v in guide.preview()["options"][-1].values()).lower())
        p=guide.preview("CONCEPTUAL_THEORY")
        self.assertIn("OTHER_NOT_LISTED",{x["id"] for x in p["options"]})

if __name__=="__main__":
    unittest.main()
