"""Synthetic validation of optional multi-disciplinary research decision guidance."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import adaptive_method_guide as guide
from method_decision_dimensions import (
 DIMENSIONS, ROUTE_FIELDS, CATALOG, candidates, eligible, existing_field)
from method_routes import ROUTES, REQUIRED_DESIGN, new_profile

class DimensionGuidanceTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.m=self.root/"00_Gestao_e_Continuidade"
        self.m.mkdir()

    def setup_route(self,route):
        (self.m/"PROJECT_CONFIG.json").write_text(json.dumps({"method_route":route}))
        (self.m/"METHOD_PROFILE.json").write_text(json.dumps(new_profile(route)))

    def test_five_dimensions_for_every_route_without_new_schema_fields(self):
        self.assertEqual(set(DIMENSIONS),{"sampling","sources","analysis","inference","reporting"})
        self.assertEqual(set(CATALOG),set(ROUTE_FIELDS))
        for route in set(ROUTES)-{"UNDECIDED"}:
            self.assertEqual(set(ROUTE_FIELDS[route]),set(DIMENSIONS))
            for dimension in DIMENSIONS:
                field=existing_field(route,dimension)
                if field is not None:
                    self.assertIn(field,REQUIRED_DESIGN[route])
                if eligible(route,dimension):
                    self.assertGreaterEqual(len(candidates(route,dimension)),2)

    def test_many_traditions_have_distinct_relevant_choices(self):
        samples=[
          ("SYSTEMATIC_REVIEW","sampling","DOCUMENT_ELIGIBILITY"),
          ("SYSTEMATIC_REVIEW","analysis","QUANTITATIVE_SYNTHESIS"),
          ("QUALITATIVE","sampling","PURPOSIVE"),
          ("QUALITATIVE","sources","DOCUMENTS"),
          ("QUANTITATIVE","analysis","REGRESSION_OR_MODELLING"),
          ("QUANTITATIVE","inference","CAUSAL"),
          ("MIXED_METHODS","inference","DISCORDANCE_PLAN"),
          ("DESIGN_SCIENCE","analysis","CONTROLLED_ARTIFACT_TEST"),
          ("CONCEPTUAL_THEORY","reporting","ARGUMENT_MAP"),
          ("PROBLEMATIZING_REVIEW","sources","CROSS_TRADITION_COMPARISON"),
        ]
        for route,dimension,choice in samples:
            with self.subTest(route=route,dimension=dimension):
                result=guide.preview(route,dimension=dimension)
                self.assertEqual(result["mode"],"EXPLORE_DECISION_DIMENSION")
                self.assertIn(choice,{x["id"] for x in result["options"]})
                self.assertEqual(result["options"][-1]["id"],"OTHER_NOT_LISTED")
                self.assertFalse(result["human_scientific_gate_approved"])
                self.assertTrue(result["human_action"]["needed_to_confirm_scientific_choice"])
                for card in result["options"]:
                    self.assertTrue(all(card[k] for k in
                        ("when_to_consider","potential","limits","what_changes_next")))
                    self.assertIsNone(card["recommendation_rank"])

    def test_reporting_advisory_no_shadow_canonical_file(self):
        self.setup_route("QUANTITATIVE")
        p=self.m/"METHOD_PROFILE.json"
        before=p.read_bytes()
        result=guide.for_project(self.root,dimension="reporting")
        self.assertEqual(result["status"],"ADVISORY_DIMENSION_NOT_CANONICAL_FIELD")
        self.assertFalse(result["dimension_is_canonical_field"])
        self.assertIsNone(result["target_field"])
        self.assertFalse(result["selection_persists_to_project"])
        self.assertEqual(before,p.read_bytes())

    def test_mixed_sampling_is_exploratory_not_one_generic_field(self):
        self.setup_route("MIXED_METHODS")
        result=guide.for_project(self.root,dimension="sampling")
        self.assertEqual(result["status"],"ADVISORY_DIMENSION_NOT_CANONICAL_FIELD")
        self.assertIsNone(result["target_field"])
        self.assertIn("CONNECTED_SAMPLING",{x["id"] for x in result["options"]})

    def test_theoretical_studies_are_not_forced_into_participant_sampling(self):
        self.setup_route("CONCEPTUAL_THEORY")
        result=guide.for_project(self.root,dimension="sampling")
        self.assertEqual(result["status"],"NOT_UNIVERSALLY_APPLICABLE")
        self.assertFalse(result["decision_dimension_applies"])
        self.assertEqual([x["id"] for x in result["options"]],["OTHER_NOT_LISTED"])

    def test_existing_field_benefits_from_same_curated_alternatives(self):
        self.setup_route("QUANTITATIVE")
        result=guide.for_project(self.root,field="sampling_logic")
        self.assertIn("PROBABILITY",{x["id"] for x in result["options"]})
        self.assertEqual(result["mode"],"EXPLORE_METHOD_FIELD")
        self.assertIsNone(result["decision_dimension"])

    def test_recorded_private_project_decision_never_leaks_or_changes(self):
        self.setup_route("QUALITATIVE")
        path=self.m/"METHOD_PROFILE.json"
        data=json.loads(path.read_text())
        data["research_question"]="CONFIDENTIAL_PROJECT_QUESTION"
        data["route_details"]["analysis_logic"]="PRIVATE_ANALYSIS_TEXT"
        data["human_route_rationale"]="SECRET_RATIONALE"
        path.write_text(json.dumps(data))
        before=path.read_bytes()
        result=guide.for_project(self.root,dimension="analysis")
        self.assertEqual(result["status"],"FIELD_ALREADY_RECORDED_REVIEW_BEFORE_CHANGE")
        self.assertFalse(result["researcher_selection_recorded"])
        self.assertFalse(result["methodological_option_recommendation_independently_validated"])
        self.assertFalse(result["human_scientific_gate_approved"])
        for secret in ("CONFIDENTIAL_PROJECT_QUESTION","PRIVATE_ANALYSIS_TEXT","SECRET_RATIONALE"):
            self.assertNotIn(secret,json.dumps(result))
        self.assertEqual(path.read_bytes(),before)

    def test_invalid_combinations_refuse_to_autoselect(self):
        with self.assertRaisesRegex(ValueError,"route"):
            guide.preview("UNDECIDED",dimension="analysis")
        with self.assertRaisesRegex(ValueError,"either"):
            guide.preview("QUANTITATIVE",field="analysis_plan",dimension="analysis")
        with self.assertRaisesRegex(ValueError,"Unknown"):
            guide.preview("QUALITATIVE",dimension="invented")
        self.setup_route("UNDECIDED")
        with self.assertRaisesRegex(ValueError,"route"):
            guide.for_project(self.root,dimension="reporting")

if __name__=="__main__":
    unittest.main()
