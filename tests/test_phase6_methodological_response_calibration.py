"""Offline structural calibration of research responses; never a human adjudication.

These are synthetic fixture expectations, NOT outputs from a real LLM or a
validation of any actual research argument, publisher or source access.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import quality_benchmark as q


class MethodologicalResponseCalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference_path = q.DEFAULT_METHOD_REFERENCE
        cls.reference = q.methodology_reference_cases(q.read_json(cls.reference_path))
        cls.frozen_sha = q.digest(cls.reference_path)

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def write_candidate(self, cases, name="recorded.json", **extra):
        path = self.root / name
        q.write_json(path, {"schema_version": 1,
                            "reference_sha256": self.frozen_sha,
                            "cases": cases, **extra})
        return path

    def proper_cases(self):
        return [{
            "case": cid,
            "fields": {**source["expected"],
                       **{name: f"Synthetic test-only justification for {name}"
                          for name in source["required_nonempty"]}}
        } for cid, source in self.reference.items()]

    def test_frozen_reference_explicitly_disclaims_scientific_gold(self):
        ref = q.read_json(self.reference_path)
        self.assertEqual(len(self.reference), 8)
        self.assertEqual(ref["source_kind"], "SYNTHETIC_SOFTWARE_REGRESSION_FIXTURE")
        self.assertFalse(ref["independent_scientific_gold"])
        self.assertEqual(
            self.reference["scientific_gate_never_autopasses"]["expected"]["Decision"],
            "PENDING")
        self.assertFalse(
            self.reference["scientific_gate_never_autopasses"]["expected"]["scientific_gate_approved_by_this_command"])

    def test_missing_all_candidates_is_zero_coverage_not_passing(self):
        out = q.evaluate_methodology(self.reference_path, self.write_candidate([]))
        metrics = out["metrics"]
        self.assertEqual(metrics["submitted_cases"], 0)
        self.assertEqual(metrics["case_coverage"], 0)
        self.assertEqual(metrics["criterion_coverage"], 0)
        self.assertEqual(metrics["fixed_rule_conformance_all_criteria"], 0)
        self.assertIsNone(metrics["fixed_rule_conformance_observed_only"])
        self.assertFalse(out["scientific_validity_proven"])
        self.assertEqual(out["human_semantic_review"], "NOT_PERFORMED")
        self.assertTrue(all(c["status"] == "NOT_SUBMITTED" for c in out["cases"]))

    def test_all_synthetic_expected_fields_can_match_without_semantic_claim(self):
        path = self.write_candidate(self.proper_cases())
        out = q.evaluate_methodology(self.reference_path, path)
        totals = out["metrics"]
        self.assertEqual(totals["structurally_matching_cases"], 8)
        self.assertEqual(totals["matched_criteria"], totals["criterion_count"])
        self.assertEqual(totals["fixed_rule_conformance_all_criteria"], 1)
        self.assertFalse(out["scientific_validity_proven"])
        self.assertFalse(out["reviewer_identity_authenticated"])
        self.assertFalse(out["source_access_verified"])
        self.assertEqual(out["reference_sha256"], self.frozen_sha)
        self.assertEqual(out["candidate_sha256"], q.digest(path))
        self.assertFalse(any("independently validated" in x.lower()
                             for x in out["limitations"]))

    def test_literal_locator_match_cannot_claim_semantic_verification(self):
        cases = self.proper_cases()
        target = next(c for c in cases if c["case"] ==
                      "literature_locator_is_not_semantic_support")
        target["fields"]["semantic_support"] = "VERIFIED"
        out = q.evaluate_methodology(self.reference_path, self.write_candidate(cases))
        item = next(c for c in out["cases"] if c["case"] == target["case"])
        self.assertEqual(item["status"], "STRUCTURAL_MISMATCH")
        self.assertIn("semantic_support", item["mismatched_fields"])
        self.assertFalse(out["scientific_validity_proven"])

    def test_missing_evidence_warrant_or_boundaries_are_not_silent_pass(self):
        cases = self.proper_cases()
        target = next(c for c in cases if c["case"] == "inference_has_reasoning_and_boundary")
        target["fields"]["inference_warrant"] = "   "
        del target["fields"]["boundary_conditions"]
        out = q.evaluate_methodology(self.reference_path, self.write_candidate(cases))
        item = next(c for c in out["cases"] if c["case"] == target["case"])
        self.assertIn("inference_warrant", item["mismatched_fields"])
        self.assertIn("boundary_conditions", item["missing_fields"])

    def test_ai_only_screening_must_stay_as_proposal(self):
        cases = self.proper_cases()
        target = next(c for c in cases if c["case"] ==
                      "ai_screening_cannot_impersonate_reviewer")
        target["fields"]["Pass1_decision"] = "INCLUDE"
        target["fields"]["human_decision_recorded"] = True
        out = q.evaluate_methodology(self.reference_path, self.write_candidate(cases))
        item = next(x for x in out["cases"] if x["case"] == target["case"])
        self.assertEqual(set(item["mismatched_fields"]),
                         {"Pass1_decision", "human_decision_recorded"})

    def test_paywall_is_not_a_scientific_exclusion(self):
        cases = self.proper_cases()
        target = next(c for c in cases if c["case"] == "paywall_is_not_scientific_exclusion")
        target["fields"]["scientific_exclusion"] = "EXCLUDED"
        item = next(x for x in q.evaluate_methodology(
            self.reference_path, self.write_candidate(cases))["cases"]
                    if x["case"] == target["case"])
        self.assertIn("scientific_exclusion", item["mismatched_fields"])

    def test_gate_autoapproval_and_unbounded_novelty_are_detected(self):
        cases = self.proper_cases()
        gate = next(c for c in cases if c["case"] == "scientific_gate_never_autopasses")
        gate["fields"]["scientific_gate_approved_by_this_command"] = True
        prop = next(c for c in cases if c["case"] == "proposition_novelty_is_bounded")
        prop["fields"]["absolute_novelty_proven"] = True
        out = q.evaluate_methodology(self.reference_path, self.write_candidate(cases))
        for cid, field in [
            ("scientific_gate_never_autopasses", "scientific_gate_approved_by_this_command"),
            ("proposition_novelty_is_bounded", "absolute_novelty_proven"),
        ]:
            item = next(c for c in out["cases"] if c["case"] == cid)
            self.assertIn(field, item["mismatched_fields"])

    def test_unverified_source_cannot_be_promoted_to_verified(self):
        cases = self.proper_cases()
        target = next(c for c in cases if c["case"] == "unsupported_evidence_remains_pending")
        target["fields"]["treat_as_verified"] = 0  # bool and integer must not compare as equal.
        out = q.evaluate_methodology(self.reference_path, self.write_candidate(cases))
        item = next(c for c in out["cases"] if c["case"] == target["case"])
        self.assertIn("treat_as_verified", item["mismatched_fields"])

    def test_unknown_and_duplicate_case_ids_are_rejected(self):
        case = self.proper_cases()[0]
        with self.assertRaisesRegex(ValueError, "Repeated case"):
            q.evaluate_methodology(self.reference_path, self.write_candidate([case, case]))
        with self.assertRaisesRegex(ValueError, "unknown methodological cases"):
            q.evaluate_methodology(self.reference_path, self.write_candidate([
                {"case": "not_in_reference", "fields": {}}]))

    def test_changed_reference_hash_prevents_cross_rubric_comparison(self):
        path = self.write_candidate(self.proper_cases(), reference_sha256="0"*64)
        with self.assertRaisesRegex(ValueError, "matching frozen reference"):
            q.evaluate_methodology(self.reference_path, path)
        reference = q.read_json(self.reference_path)
        reference["cases"][0]["expected"]["semantic_support"] = "VERIFIED"
        variant = self.root / "fake_ref.json"
        q.write_json(variant, reference)
        with self.assertRaisesRegex(ValueError, "matching frozen reference"):
            q.evaluate_methodology(variant, self.write_candidate(self.proper_cases()))

    def test_claimed_independent_gold_in_reference_is_rejected(self):
        bad = q.read_json(self.reference_path)
        bad["independent_scientific_gold"] = True
        with self.assertRaisesRegex(ValueError, "bounded synthetic"):
            q.methodology_reference_cases(bad)
        bad["independent_scientific_gold"] = False
        bad["cases"][6]["expected"]["scientific_gate_approved_by_this_command"] = True
        with self.assertRaisesRegex(ValueError, "cannot claim AI approved"):
            q.methodology_reference_cases(bad)

    def test_comparison_preserves_coverage_and_counts_not_scientific_metrics(self):
        previous = self.write_candidate([], name="previous.json")
        current = self.write_candidate(self.proper_cases(), name="current.json")
        out = q.evaluate_methodology(self.reference_path, current, baseline=previous)
        compared = out["baseline_comparison"]
        self.assertEqual(compared["change_matched_criteria"],
                         out["metrics"]["criterion_count"])
        self.assertEqual(compared["baseline_case_coverage"], 0)
        self.assertEqual(compared["candidate_case_coverage"], 1)
        self.assertFalse(out["scientific_validity_proven"])

    def test_reports_retain_no_submitted_private_prose(self):
        cases = self.proper_cases()
        cases[0]["fields"]["supporting_locator"] = "PRIVATE_PATIENT_DATA_DO_NOT_DISCLOSE"
        out = q.evaluate_methodology(self.reference_path, self.write_candidate(cases))
        self.assertNotIn("PRIVATE_PATIENT_DATA_DO_NOT_DISCLOSE",
                         json.dumps(out, ensure_ascii=False))
        self.assertFalse(out["source_access_verified"])

    def test_cli_writes_non_approval_report_offline(self):
        candidate = self.write_candidate(self.proper_cases())
        outfile = self.root / "evaluated.json"
        proc = subprocess.run([
            sys.executable, str(ROOT / "scripts/quality_benchmark.py"),
            "evaluate-methodology", "--reference", str(self.reference_path),
            "--candidate", str(candidate), "--output", str(outfile)
        ], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(outfile.read_text(encoding="utf-8"))
        self.assertEqual(data["mode"], "methodological_response_calibration")
        self.assertFalse(data["scientific_validity_proven"])
        self.assertIn("NOT_PERFORMED", proc.stdout)
        self.assertFalse(data["source_access_verified"])
        self.assertFalse(data["reviewer_identity_authenticated"])


if __name__ == "__main__":
    unittest.main()
