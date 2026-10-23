"""Stage 12: isolated advisory-only science screening; fictional inputs only.

These tests do not certify sources, authors, semantic entailment, or gates.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from claim_overreach_signals import signals
from contextual_support_probe import examine
from semantic_claim_review import review, local_json, valid_annotation
from reference_audit import _issue, BLOCKERS
from report_output_guard import write_report
import claim_integrity


class Stage12ScientificAdvisoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_contextual_causality_is_advisory(self):
        report = examine(
            "The user interface redesign caused the decrease in administrative delay.",
            "The study was observational; groups differed in staffing and tasks.")
        self.assertIn("CONTEXT_CAUSAL_ATTRIBUTION",
                      [x["code"] for x in report["signals"]])
        self.assertTrue(all(x["severity"] == "ADVISORY"
                            for x in report["signals"]))
        self.assertEqual(report["severity"], "ADVISORY")
        self.assertFalse(report["can_block_scientific_workflow"])
        self.assertFalse(report["entailment_proven"])

    def test_contextual_qualified_denial_not_positive_proof(self):
        result = examine(
            "The study did not establish that a checklist caused the outcome.",
            "The observational groups were not randomized.")
        self.assertNotIn("CONTEXT_CAUSAL_ATTRIBUTION",
                         [x["code"] for x in result["signals"]])
        self.assertFalse(result["entailment_proven"])
        self.assertTrue(result["human_review_required"])

    def test_contextual_population_extrapolation_advisory(self):
        result = examine(
            "There is a widespread pattern throughout public administration.",
            "The small exploratory study interviewed six clerks at a single archive.")
        self.assertIn("CONTEXT_POPULATION_SCOPE",
                      [x["code"] for x in result["signals"]])
        self.assertFalse(result["independent_scientific_validation"])

    def test_contextual_unobserved_outcomes_advisory(self):
        result = examine("The project proved effective at eliminating delays.",
                         "Data collection had not started. No results were reported.")
        self.assertIn("CONTEXT_UNOBSERVED_OUTCOME",
                      [x["code"] for x in result["signals"]])
        self.assertTrue(result["human_review_required"])

    def test_contextual_manual_method_contradiction_advisory(self):
        result = examine("The study used an automated classifier.",
                         "Requests were manually sorted; no machine-learning was used.")
        self.assertIn("CONTEXT_MANUAL_AUTOMATED_METHOD",
                      [x["code"] for x in result["signals"]])
        self.assertEqual(result["severity"], "ADVISORY")

    def test_contextual_not_evaluated_requires_human_review(self):
        for claim, excerpt in [("", "source text"), ("x" * 13000, "source text")]:
            result = examine(claim, excerpt)
            self.assertEqual(result["status"], "NOT_EVALUATED")
            self.assertEqual(result["severity"], "ADVISORY")
            self.assertFalse(result["can_block_scientific_workflow"])
            self.assertFalse(result["entailment_proven"])

    def test_lexical_no_flags_is_not_evidence_of_support(self):
        result = signals("The paper concerns records.",
                         "Some records were organized.")
        self.assertEqual(result["codes"], [])
        self.assertEqual(result["severity"], "ADVISORY")
        self.assertFalse(result["can_block_scientific_workflow"])
        self.assertFalse(result["semantic_entailment_proven"])
        self.assertFalse(result["is_scientific_verification"])

    def test_lexical_not_evaluated_is_advisory(self):
        for claim in ("", "z" * 13000):
            result = signals(claim, "fictional passage")
            self.assertEqual(result["status"], "NOT_EVALUATED")
            self.assertEqual(result["severity"], "ADVISORY")
            self.assertTrue(result["human_review_required"])
            self.assertFalse(result["semantic_entailment_proven"])

    def test_both_sidecars_never_export_source_passages(self):
        claim = "The process caused improvements in all public organizations."
        passage = "Observational association only, without causal inference."
        for result in [signals(claim, passage), examine(claim, passage)]:
            raw = json.dumps(result)
            self.assertNotIn(claim, raw)
            self.assertNotIn(passage, raw)
            self.assertEqual(result["severity"], "ADVISORY")

    def test_deterministic_screening_and_bounded_outputs(self):
        a = "The redesign caused effects in all public institutions."
        b = "Only two departments had observational associations; not randomized."
        for detector in [signals, examine]:
            first = detector(a, b)
            self.assertEqual(first, detector(a, b))
            self.assertLess(len(json.dumps(first)), 15000)

    def test_announced_human_reviewer_is_not_authenticated(self):
        valid = {"reviewer_kind": "AI_GENERATED", "reviewer": "assistant",
                 "rationale": "x" * 90, "limitations": "x" * 35,
                 "response_reference": "synthetic-only",
                 "claim_sha256": "a" * 64, "source_sha256": "b" * 64,
                 "source_report_sha256": "c" * 64,
                 "judgment": "SUPPORTED", "scope_alignment": "ALIGNED",
                 "method_alignment": "ALIGNED", "context_alignment": "ALIGNED",
                 "counterevidence_considered": True}
        self.assertEqual(valid_annotation(valid, "a" * 64, "b" * 64, "c" * 64),
                         "HUMAN_REVIEW_NOT_DECLARED")
        valid["reviewer_kind"] = "HUMAN_DECLARED"
        self.assertIsNone(valid_annotation(valid, "a" * 64, "b" * 64, "c" * 64))
        # A syntactically valid declaration alone is not identity verification.

    def test_reference_blocker_is_objective_not_semantic_verdict(self):
        self.assertIn("UNKNOWN_REFERENCE", BLOCKERS)
        result = _issue("UNKNOWN_REFERENCE", evidence_id="EVID-0001")
        self.assertEqual(result["severity"], "BLOCK")
        # Only structural/bibliographic integrity, never semantic support.
        self.assertEqual(set(result), {"code", "severity", "evidence_id", "claim_id"})
        self.assertNotIn("scientific_validated", result)

    def test_report_writer_never_replaces_existing_file(self):
        folder = self.root / "98_Technical_Reports"
        folder.mkdir()
        target = folder / "advisory.json"
        target.write_text("ORIGINAL", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            write_report(self.root, Path("98_Technical_Reports/advisory.json"),
                         "CHANGED", allowed_extensions=frozenset({".json"}))
        self.assertEqual(target.read_text(encoding="utf-8"), "ORIGINAL")

    def test_report_writer_refuses_symlink_escape(self):
        outside = self.root.parent / (self.root.name + "-outside")
        outside.mkdir()
        self.addCleanup(lambda: outside.rmdir())
        link = self.root / "98_Technical_Reports"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("platform cannot make directory symlinks")
        with self.assertRaises(ValueError):
            write_report(self.root, Path("98_Technical_Reports/report.json"),
                         "UNSAFE", allowed_extensions=frozenset({".json"}))
        self.assertEqual(list(outside.iterdir()), [])

    def test_reports_are_created_only_under_technical_reports(self):
        with self.assertRaises(ValueError):
            write_report(self.root, Path("00_Gestao_e_Continuidade/09_Claims_Ledger.csv"),
                         "WRONG", allowed_extensions=frozenset({".csv"}))
        self.assertFalse((self.root / "00_Gestao_e_Continuidade").exists())

    def test_claim_integrity_authority_stays_independent(self):
        self.assertTrue(callable(claim_integrity.audit))
        self.assertTrue(callable(claim_integrity.normative_observation_risk))
        result = claim_integrity.audit([], [], [], strict=True)
        self.assertIs(result["semantic_support_proven"], False)
        self.assertIs(result["novelty_proven"], False)


if __name__ == "__main__":
    unittest.main()
