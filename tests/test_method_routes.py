"""Offline controls of conditional scientific method routes (not empirical trials)."""
from __future__ import annotations

import csv
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import method_routes as methods
import init_project


class MethodRoutesTests(unittest.TestCase):
    def test_all_route_names_have_a_configured_scientific_design(self):
        self.assertEqual(len(methods.ROUTES), 9)  # undecided plus eight routes
        for route in methods.ROUTES:
            p = methods.new_profile(route)
            self.assertEqual(p["route"], route)
            self.assertEqual(p["route_confirmation"], "PENDING_HUMAN_DECISION")
            self.assertEqual(p["evidence_status"], "NOT_EXECUTED")

    def test_ambiguous_or_generic_empirical_type_never_selects_a_method(self):
        for article_type in ("empirical", "artigo", "qualquer trabalho", ""):
            self.assertEqual(methods.infer_route(article_type), "UNDECIDED")

    def test_recognizes_theoretical_qualitative_quantitative_and_mixed(self):
        samples = {
            "revisão sistemática": "SYSTEMATIC_REVIEW",
            "integrative review": "INTEGRATIVE_REVIEW",
            "problematização": "PROBLEMATIZING_REVIEW",
            "artigo conceitual": "CONCEPTUAL_THEORY",
            "fenomenologia qualitativa": "QUALITATIVE",
            "survey quantitativo": "QUANTITATIVE",
            "métodos mistos": "MIXED_METHODS",
            "design science research": "DESIGN_SCIENCE",
        }
        for label, expected in samples.items():
            with self.subTest(label=label):
                self.assertEqual(methods.infer_route(label), expected)

    def test_review_corpus_and_quant_data_have_distinct_gate_types(self):
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder) / "18_Gates.csv"
            init_project.seed_gates(dest, "QUANTITATIVE")
            with dest.open("r", encoding="utf-8-sig", newline="") as f:
                gates = list(csv.DictReader(f))
            self.assertEqual(len(gates), 7)
            by_id = {r["GATE_ID"]: r for r in gates}
            self.assertEqual(by_id["GATE-0004"]["Gate_type"], "EMPIRICAL_MATERIALS")
            self.assertEqual(by_id["GATE-0005"]["Gate_type"], "QUANTITATIVE_ANALYSIS")
            self.assertEqual(by_id["GATE-0006"]["Gate_type"], "CLAIMS_AUDIT")

    def test_missing_confirmed_human_decision_blocks_method_gate(self):
        p = methods.new_profile("QUANTITATIVE")
        self.assertIn("researcher has not confirmed route classification",
                      methods.profile_issues(p, "QUANTITATIVE", gate="GATE-0002"))

    def test_quantitative_inference_aim_cannot_be_an_undefined_label(self):
        p = methods.new_profile("QUANTITATIVE")
        p["route_details"] = {field: "planned" for field in methods.REQUIRED_DESIGN["QUANTITATIVE"]}
        p["route_details"]["inference_aim"] = "MAGICAL_CAUSALITY"
        self.assertTrue(any("quantitative inference aim" in x for x in
                            methods.profile_issues(p, "QUANTITATIVE", gate="GATE-0002")))

    def test_mixed_requires_an_actual_integration_decision(self):
        p = methods.new_profile("MIXED_METHODS")
        p["route_details"] = {field: "planned" for field in methods.REQUIRED_DESIGN["MIXED_METHODS"]}
        self.assertTrue(any("mixed design" in x or "integration" in x for x in
                            methods.profile_issues(p, "MIXED_METHODS", gate="GATE-0002")))

    def test_empirical_stage_cannot_be_approved_from_only_a_plan(self):
        p = methods.new_profile("DESIGN_SCIENCE")
        for gid in ("GATE-0004", "GATE-0005"):
            self.assertTrue(methods.profile_issues(p, "DESIGN_SCIENCE", gate=gid))

    def test_legacy_profile_not_required_to_pass_old_gate(self):
        self.assertEqual(methods.approval_issues(Path("/not/a/project"),
                         {"method_route_governance_required": False}, "GATE-0006"), [])


if __name__ == "__main__":
    unittest.main()
