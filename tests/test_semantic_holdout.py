"""Untuned developer-labeled synthetic holdout: test execution integrity only."""
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import evaluate_semantic_holdout as h
from evaluation_registry import read_ledger
from evaluation_package import validate as replay_verify
B=ROOT/"benchmarks/claim_support_heldout_v1.json"

class HoldoutTests(unittest.TestCase):
    def test_frozen_cases(self):
        data=h.frozen(B)
        self.assertEqual(len(data["cases"]),24)
        self.assertFalse(data["protocol"]["independent_human_ground_truth"])
        self.assertTrue(data["protocol"]["no_detector_refit_on_holdout"])

    def test_run_and_scores_are_observed_not_assumed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            out=root/"new_results"
            result=h.evaluate(B,out,revision="a"*40)
            self.assertEqual(result["case_count"],24)
            self.assertEqual(result["reg001_recorded"],24)
            self.assertEqual(result["reg001_expected_matches"]+result["reg001_mismatches"],24)
            counts=result["confusion_counts"]
            self.assertEqual(counts["true_positive"]+counts["false_negative"],18)
            self.assertEqual(counts["true_negative"]+counts["false_positive"],6)
            self.assertFalse(result["scientific_quality_validated"])
            self.assertFalse(result["human_review_authenticated"])
            self.assertFalse(result["semantic_entailment_established"])
            self.assertEqual(len(read_ledger(out/"evaluation_runs.jsonl")),1)
            report=replay_verify(out/"evaluation-replay.zip")
            self.assertEqual(report["observed_total"],24)
            self.assertFalse(report["scientific_validity_proven"])
            for row in result["cases"]:
                self.assertTrue((out/"evidence"/(row["case_id"]+".json")).exists())

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td)/"prior"
            folder.mkdir()
            guard=folder/"existing.txt"
            guard.write_text("UNTOUCHED")
            with self.assertRaises(ValueError):
                h.evaluate(B,folder,revision="a"*40)
            self.assertEqual(guard.read_text(),"UNTOUCHED")

if __name__=="__main__":
    unittest.main()
