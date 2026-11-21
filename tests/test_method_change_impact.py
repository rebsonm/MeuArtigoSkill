"""Synthetic-only regressions for all eight Skill method routes.

These tests verify deterministic behavior; they do not validate science.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from method_change_impact import (
    ENUM_FIELDS, ROUTE_REVIEW_HINTS, preview_change,
)
from method_routes import REQUIRED_DESIGN, new_profile
from method_fill_preflight import for_existing_project


class RouteChangePreviewTests(unittest.TestCase):
    def test_every_defined_route_has_curated_example_and_canonical_targets(self):
        self.assertEqual(set(ROUTE_REVIEW_HINTS), set(REQUIRED_DESIGN))
        for route, triggers in ROUTE_REVIEW_HINTS.items():
            self.assertTrue(triggers)
            for field, targets in triggers.items():
                with self.subTest(route=route, field=field):
                    self.assertIn(field, REQUIRED_DESIGN[route])
                    self.assertTrue(targets)
                    self.assertEqual(len(targets), len(set(targets)))
                    self.assertTrue(all(t in REQUIRED_DESIGN[route] for t in targets))
                    old, new = self.samples(route, field)
                    result = preview_change(route, field, old, new)
                    self.assertTrue(result["change_detected"])
                    self.assertEqual(result["review_map_coverage"],
                                     "CURATED_POTENTIAL_TARGETS")
                    self.assertEqual(result["potential_review_targets"][0], field)
                    self.assertFalse(result["affected_decisions_or_claims_identified"])
                    self.assertFalse(result["scientific_gate_approved"])
                    self.assertFalse(result["project_modified"])

    @staticmethod
    def samples(route, field):
        if (route, field) == ("QUANTITATIVE", "inference_aim"):
            return "ASSOCIATIONAL", "CAUSAL"
        if (route, field) == ("MIXED_METHODS", "mixed_design"):
            return "CONVERGENT", "EXPLANATORY_SEQUENTIAL"
        if (route, field) == ("MIXED_METHODS", "integration_type"):
            return "CONNECTING", "MERGING"
        return ("Original defensible researcher-defined method choice",
                "A substantively different researcher-defined method choice")

    def test_every_other_field_has_conservative_unmapped_fallback(self):
        for route, fields in REQUIRED_DESIGN.items():
            for field in fields:
                if field in ROUTE_REVIEW_HINTS[route]:
                    continue
                old, new = self.samples(route, field)
                with self.subTest(route=route, field=field):
                    report = preview_change(route, field, old, new)
                    self.assertEqual(report["review_map_coverage"],
                                     "FIELD_ONLY_UNMAPPED")
                    self.assertEqual(report["potential_review_targets"], [field])
                    self.assertEqual(report["status"],
                                     "TEXT_CHANGED_SEMANTIC_IMPACT_UNKNOWN")

    def test_identical_change_does_not_request_new_review(self):
        r = preview_change("QUALITATIVE", "sampling_logic",
                           "Select diverse documented cases", "Select diverse documented cases")
        self.assertEqual(r["status"], "IDENTICAL_FIELD_NO_NEW_REVIEW")
        self.assertEqual(r["potential_review_targets"], [])
        self.assertFalse(r["human_review_may_be_needed"])

    def test_surrounding_whitespace_and_line_endings_do_not_trigger_review(self):
        a = preview_change("CONCEPTUAL_THEORY", "theoretical_problem",
                           "  Original idea\r\nwith limits \n",
                           "Original idea\nwith limits")
        self.assertEqual(a["status"], "BOUNDARY_FORMATTING_ONLY_NO_NEW_REVIEW")
        self.assertFalse(a["change_detected"])
        self.assertEqual(a["potential_review_targets"], [])

    def test_internal_whitespace_is_not_assumed_editorial(self):
        a = preview_change("QUANTITATIVE", "analysis_plan",
                           "y = a+b", "y = a + b")
        self.assertEqual(a["status"], "TEXT_CHANGED_SEMANTIC_IMPACT_UNKNOWN")
        self.assertTrue(a["human_review_may_be_needed"])

    def test_mixed_design_and_integration_changes_are_not_confused(self):
        a = preview_change("MIXED_METHODS", "mixed_design",
                           "CONVERGENT", "EXPLANATORY_SEQUENTIAL")
        b = preview_change("MIXED_METHODS", "integration_type",
                           "CONNECTING", "MERGING")
        self.assertEqual(a["status"], "CANONICAL_DESIGN_LABEL_CHANGED_REVIEW_REQUIRED")
        self.assertEqual(b["status"], "CANONICAL_DESIGN_LABEL_CHANGED_REVIEW_REQUIRED")
        self.assertIn("quantitative_strand", a["potential_review_targets"])
        self.assertNotIn("quantitative_strand", b["potential_review_targets"])
        self.assertIn("integration_point", b["potential_review_targets"])
        self.assertTrue(a["human_review_may_be_needed"])

    def test_missing_or_invalid_baseline_fails_closed_without_inventing_history(self):
        self.assertEqual(
            preview_change("DESIGN_SCIENCE", "evaluation_plan", "", "New evaluated plan")["status"],
            "NO_RECORDED_BASELINE")
        self.assertEqual(
            preview_change("QUANTITATIVE", "inference_aim",
                           "FICTITIOUS", "CAUSAL")["status"],
            "INVALID_CANONICAL_ENUM_NOT_COMPARED")

    def test_invalid_proposal_never_signals_scientific_change(self):
        r = preview_change("SYSTEMATIC_REVIEW", "eligibility_criteria",
                           "Prior actual criteria", "pending", proposal_eligible=False)
        self.assertEqual(r["status"], "INVALID_OR_BLOCKED_PROPOSAL_NOT_COMPARED")
        self.assertEqual(r["potential_review_targets"], [])
        self.assertFalse(r["change_detected"])

    def test_wrong_route_field_refuses_to_guess(self):
        with self.assertRaises(ValueError):
            preview_change("UNDECIDED", "sampling_logic", "x", "y")
        with self.assertRaises(ValueError):
            preview_change("QUALITATIVE", "inference_aim", "x", "y")

    def test_preview_never_leaks_old_or_new_confidential_text(self):
        old = "PRIVATE RESEARCHER SOURCE 984112"
        new = "PRIVATE UNRELEASED MANUSCRIPT 984113"
        r = preview_change("INTEGRATIVE_REVIEW", "selection_logic", old, new)
        assert old not in json.dumps(r)
        assert new not in json.dumps(r)
        self.assertFalse(r["recorded_value_disclosed"])
        self.assertFalse(r["proposed_value_disclosed"])
        self.assertFalse(r["actual_dependency_edges_verified"])

    def test_no_auto_approval_or_verified_dependencies_for_every_trigger(self):
        for route, fields in ROUTE_REVIEW_HINTS.items():
            for field in fields:
                old, new = self.samples(route, field)
                r = preview_change(route, field, old, new)
                self.assertFalse(r["actual_dependency_edges_verified"])
                self.assertFalse(r["scientific_adequacy_verified"])
                self.assertFalse(r["affected_decisions_or_claims_identified"])
                self.assertFalse(r["scientific_gate_approved"])
                self.assertFalse(r["project_modified"])

    def test_canonical_enum_map_reuses_existing_vocabularies(self):
        for (route, field), allowed in ENUM_FIELDS.items():
            self.assertIn(route, REQUIRED_DESIGN)
            self.assertIn(field, REQUIRED_DESIGN[route])
            self.assertGreaterEqual(len(allowed), 4)

    def test_live_preflight_integration_remains_read_only_for_all_routes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mgmt = root / "00_Gestao_e_Continuidade"
            mgmt.mkdir()
            for route, triggers in ROUTE_REVIEW_HINTS.items():
                field = next(iter(triggers))
                old, new = self.samples(route, field)
                (mgmt / "PROJECT_CONFIG.json").write_text(json.dumps({
                    "method_route": route, "method_route_governance_required": True,
                    "storage_mode": "GOOGLE_DRIVE",
                }), encoding="utf-8")
                doc = new_profile(route)
                doc["route_details"][field] = old
                doc["research_question"] = "PRIVATE QUESTION 7753"
                (mgmt / "METHOD_PROFILE.json").write_text(json.dumps(doc), encoding="utf-8")
                # Existing gate data must never be mutated by a preflight.
                (mgmt / "18_Human_Validation_Gates.csv").write_text(
                    "GATE_ID,Status,Decision\nGATE-0001,PENDING,PENDING\n",
                    encoding="utf-8")
                before = {p.name: p.read_bytes() for p in mgmt.iterdir()}
                result = for_existing_project(root, field=field, proposal=new)
                impact = result["method_change_impact"]
                self.assertTrue(impact["human_review_may_be_needed"])
                self.assertGreater(result["blocking_finding_count"], 0)
                self.assertFalse(result["scientific_gate_approved"])
                self.assertNotIn("PRIVATE QUESTION 7753", json.dumps(result))
                self.assertEqual(
                    before, {p.name: p.read_bytes() for p in mgmt.iterdir()})
                if route == "QUANTITATIVE":
                    self.assertEqual(result["inference_change_impact"]["status"],
                                     "CAUSAL_ESCALATION_REQUIRES_REVIEW")

    def test_preflight_placeholder_does_not_create_change_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            mgmt = Path(directory) / "00_Gestao_e_Continuidade"
            mgmt.mkdir()
            (mgmt / "PROJECT_CONFIG.json").write_text(json.dumps({
                "method_route": "DESIGN_SCIENCE",
                "method_route_governance_required": True,
                "storage_mode": "GOOGLE_DRIVE",
            }))
            doc = new_profile("DESIGN_SCIENCE")
            doc["route_details"]["evaluation_plan"] = "Real original evaluation plan"
            (mgmt / "METHOD_PROFILE.json").write_text(json.dumps(doc))
            res = for_existing_project(Path(directory),
                                       field="evaluation_plan", proposal="pending")
            self.assertEqual(res["method_change_impact"]["status"],
                             "INVALID_OR_BLOCKED_PROPOSAL_NOT_COMPARED")

if __name__ == "__main__":
    unittest.main()
