"""Synthetic, offline regression tests for read-only inference-change previews.

A passing result verifies software behavior, never scientific adequacy.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import method_fill_preflight as preflight
import method_routes


class InferenceAimChangeImpactTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.mgmt = self.root / "00_Gestao_e_Continuidade"
        self.mgmt.mkdir()
        self.config = self.mgmt / "PROJECT_CONFIG.json"
        self.profile = self.mgmt / "METHOD_PROFILE.json"
        self.configure("QUANTITATIVE", "ASSOCIATIONAL")

    def configure(self, route, inference=""):
        self.config.write_text(json.dumps({
            "method_route": route, "method_route_governance_required": True,
            "storage_mode": "GOOGLE_DRIVE",
        }), encoding="utf-8")
        doc = method_routes.new_profile(route)
        if route == "QUANTITATIVE":
            doc["route_details"]["inference_aim"] = inference
        doc["research_question"] = "PRIVATE RESEARCH QUESTION 98471"
        doc["human_route_rationale"] = "PRIVATE RESEARCH RATIONALE 98472"
        self.profile.write_text(json.dumps(doc), encoding="utf-8")

    def preview(self, proposed, field="inference_aim"):
        return preflight.for_existing_project(
            self.root, field=field, proposal=proposed)

    def test_causal_escalation_reports_potential_dependencies_without_mutation(self):
        before = {p.name: p.read_bytes() for p in self.mgmt.iterdir()}
        result = self.preview("CAUSAL")
        impact = result["inference_change_impact"]
        self.assertEqual(impact["status"], "CAUSAL_ESCALATION_REQUIRES_REVIEW")
        self.assertEqual(impact["previous_aim"], "ASSOCIATIONAL")
        self.assertEqual(impact["proposed_aim"], "CAUSAL")
        self.assertTrue(impact["inference_aim_changed"])
        self.assertTrue(impact["human_researcher_review_required_for_change"])
        self.assertIn("causal_identification_assumptions", impact["review_targets"])
        self.assertIn("analysis_plan", impact["review_targets"])
        self.assertIn("claims_and_conclusions_if_any", impact["review_targets"])
        self.assertFalse(impact["affected_records_identified_or_invalidated"])
        self.assertFalse(impact["scientific_gate_approved"])
        self.assertFalse(impact["canonical_project_modified"])
        self.assertGreater(result["blocking_finding_count"], 0)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.mgmt.iterdir()})

    def test_same_label_does_not_require_revalidation(self):
        impact = self.preview("ASSOCIATIONAL")["inference_change_impact"]
        self.assertEqual(impact["status"], "NO_INFERENCE_AIM_CHANGE")
        self.assertEqual(impact["review_targets"], [])
        self.assertFalse(impact["human_researcher_review_required_for_change"])
        # Existing preflight writer policy is not bypassed by a no-op.
        self.assertFalse(impact["scientific_gate_approved"])

    def test_noncausal_change_keeps_scope_bounded(self):
        impact = self.preview("PREDICTIVE")["inference_change_impact"]
        self.assertEqual(impact["status"], "INFERENCE_AIM_CHANGE_REQUIRES_REVIEW")
        self.assertNotIn("causal_identification_assumptions", impact["review_targets"])
        self.assertIn("intended_inference", impact["review_targets"])

    def test_retreat_from_causal_review_old_claims(self):
        self.configure("QUANTITATIVE", "CAUSAL")
        impact = self.preview("DESCRIPTIVE")["inference_change_impact"]
        self.assertEqual(impact["status"], "CAUSAL_DEESCALATION_REQUIRES_REVIEW")
        self.assertIn("claims_and_conclusions_if_any", impact["review_targets"])

    def test_invalid_label_does_not_fabricate_impact(self):
        impact = self.preview("CAUSALISH")["inference_change_impact"]
        self.assertEqual(impact["status"], "INVALID_PROPOSAL_NOT_COMPARED")
        self.assertIsNone(impact["proposed_aim"])
        self.assertFalse(impact["inference_aim_changed"])
        self.assertEqual(impact["review_targets"], [])
        self.assertGreater(self.preview("CAUSALISH")["blocking_finding_count"], 0)

    def test_unrecorded_baseline_does_not_invent_historical_decision(self):
        self.configure("QUANTITATIVE", "")
        impact = self.preview("CAUSAL")["inference_change_impact"]
        self.assertEqual(impact["status"], "NO_CANONICAL_BASELINE")
        self.assertIsNone(impact["previous_aim"])
        self.assertFalse(impact["inference_aim_changed"])
        self.assertFalse(impact["human_researcher_review_required_for_change"])

    def test_other_routes_do_not_assume_quantitative_inference_model(self):
        self.configure("QUALITATIVE")
        result = self.preview("Grounded observations across actual cases", field="analysis_logic")
        self.assertNotIn("inference_change_impact", result)

    def test_mismatched_canonical_profile_does_not_compare(self):
        self.configure("QUANTITATIVE", "ASSOCIATIONAL")
        doc = json.loads(self.profile.read_text(encoding="utf-8"))
        doc["route"] = "QUALITATIVE"
        self.profile.write_text(json.dumps(doc), encoding="utf-8")
        result = self.preview("CAUSAL")
        self.assertNotIn("inference_change_impact", result)
        self.assertEqual(result["status"], "BLOCKED_BEFORE_WRITING")

    def test_output_has_no_private_project_text(self):
        impact_report = json.dumps(self.preview("CAUSAL"))
        self.assertNotIn("PRIVATE RESEARCH QUESTION 98471", impact_report)
        self.assertNotIn("PRIVATE RESEARCH RATIONALE 98472", impact_report)

    def test_rejects_symlinked_profile_without_following_it(self):
        target = self.root / "profile-original.json"
        target.write_bytes(self.profile.read_bytes())
        self.profile.unlink()
        self.profile.symlink_to(target)
        result = self.preview("CAUSAL")
        self.assertNotIn("inference_change_impact", result)
        self.assertEqual(result["status"], "BLOCKED_BEFORE_WRITING")

    def test_function_does_not_echo_untrusted_old_value(self):
        impact = preflight.inference_aim_change_impact(
            "PRIVATE USER DATA", "CAUSAL")
        self.assertIsNone(impact["previous_aim"])
        self.assertEqual(impact["status"], "NO_CANONICAL_BASELINE")
        self.assertNotIn("PRIVATE USER DATA", json.dumps(impact))


if __name__ == "__main__":
    unittest.main()
