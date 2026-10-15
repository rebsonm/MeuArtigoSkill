"""End-to-end author-labeled synthetic semantic-support evaluation."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import evaluate_semantic_challenge as exercise
from evaluation_registry import read_ledger, validate_catalog
from evaluation_package import validate as verify_replay
from semantic_claim_review import review

BENCH=ROOT/"benchmarks/claim_support_challenge_v1.json"
COMMIT="a"*40

class SemanticChallengeEvaluationTests(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)
        self.out=self.root/"challenge_results"

    def test_preregistered_balance_and_development_label_limit(self):
        data=exercise.load_frozen(BENCH)
        self.assertEqual(len(data["cases"]),16)
        labels=[c["gold_support"] for c in data["cases"]]
        self.assertEqual({k:labels.count(k) for k in exercise.LABELS},{
            "SUPPORTED":4,"PARTIALLY_SUPPORTED":4,
            "NOT_SUPPORTED":4,"INCONCLUSIVE":4})
        self.assertFalse(data["protocol"]["semantic_ground_truth_independently_established"])
        self.assertTrue(data["protocol"]["no_external_sources"])

    def test_real_reg011_and_reg001_reg019_integration(self):
        res=exercise.evaluate(BENCH,self.out,source_commit=COMMIT)
        self.assertEqual(res["case_count"],16)
        self.assertEqual(res["without_review_pending_count"],16)
        self.assertEqual(res["blanket_declared_as_supported_count"],16)
        self.assertEqual(res["reg001_recorded"],16)
        self.assertEqual(res["reg001_expected_matches"] + res["reg001_challenge_mismatches"],16)
        self.assertTrue(res["labels_seen_during_detector_development"])
        self.assertFalse(res["external_blinded_generalization_not_tested"] is False)
        m=res["semantic_discrepancy_confusion_author_labels"]
        self.assertEqual(m["true_positive"]+m["false_negative"],12)
        self.assertEqual(m["true_negative"]+m["false_positive"],4)
        self.assertEqual(m["true_positive"],sum(x["semantic_discrepancy_flagged"]
                                                 for x in res["results"] if x["gold_support"]!="SUPPORTED"))
        self.assertEqual(m["false_positive"],sum(x["semantic_discrepancy_flagged"]
                                                  for x in res["results"] if x["gold_support"]=="SUPPORTED"))
        self.assertFalse(res["scientific_quality_established"])
        self.assertFalse(res["researcher_authenticated"])
        self.assertFalse(res["semantic_entailment_automated"])
        for row in res["results"]:
            evidence=json.loads((self.out/"evidence"/(row["case_id"]+".json")).read_text())
            self.assertEqual(evidence["without_assessment"]["status"],"PENDING_HUMAN_REVIEW")
            self.assertEqual(evidence["blanket_supported_declaration"]["status"],
                             "HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED")
            self.assertEqual(evidence["reference_label_supplied_declaration"]["status"],
                             "HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED")
            self.assertFalse(evidence["reference_label_supplied_declaration"]["semantic_support_proven"])
            self.assertEqual(evidence["blanket_supported_declaration"]["semantic_probe_status"],
                             "SCREENED_HEURISTIC_ONLY")
            self.assertEqual(evidence["blanket_supported_declaration"]["semantic_risk_codes"],
                             row["risk_codes"])
        ledger=read_ledger(self.out/"evaluation_runs.jsonl")
        self.assertEqual(len(ledger),1)
        self.assertEqual(ledger[0]["result"]["matches_expected"],res["reg001_expected_matches"])
        replay=verify_replay(self.out/"evaluation-replay.zip")
        self.assertEqual(replay["run_count"],1)
        self.assertEqual(replay["observed_total"],16)
        self.assertFalse(replay["scientific_validity_proven"])
        catalog=json.loads((self.out/"semantic_case_catalog.json").read_text())
        self.assertEqual(len(validate_catalog(catalog)),16)

    def test_fabricated_quote_is_blocked_by_actual_locator(self):
        case=exercise.load_frozen(BENCH)["cases"][0]
        p=self.root/"fictional"
        exercise.prepare(p,case)
        a=exercise.assessment(p,case,label_aware=False)
        a["reviews"][0]["quoted_passage"]="This is a passage that does not exist in the synthetic source and has been fabricated."
        x=review(p,a)["review_items"][0]
        self.assertEqual(x["status"],"QUOTED_PASSAGE_NOT_CONFIRMED")

    def test_self_reported_alignment_conflict_is_flagged(self):
        case=exercise.load_frozen(BENCH)["cases"][4]
        p=self.root/"overclaim"
        exercise.prepare(p,case)
        a=exercise.assessment(p,case,label_aware=False)
        a["reviews"][0]["scope_alignment"]="OVERGENERALIZED"
        self.assertEqual(review(p,a)["review_items"][0]["status"],
                         "UNQUALIFIED_SUPPORT_CONTRADICTS_REVIEW")

    def test_rejects_unfrozen_labels_and_duplicate_ids(self):
        d=exercise.load_frozen(BENCH)
        d["cases"][0]["gold_support"]="NOT_SUPPORTED"
        bad=self.root/"changed.json"
        bad.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError,"balanced frozen"):
            exercise.load_frozen(bad)
        d=exercise.load_frozen(BENCH)
        d["cases"][1]["case_id"]=d["cases"][0]["case_id"]
        bad.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError,"duplicate"):
            exercise.load_frozen(bad)

    def test_compact_diagnostic_surfaces_review_risk_without_scientific_approval(self):
        from scientific_diagnostic import compose
        case=exercise.load_frozen(BENCH)["cases"][4]
        root=self.root/"synthetic_diagnostic"
        exercise.prepare(root,case)
        assessment=exercise.assessment(root,case,label_aware=False)
        report=compose(root,assessments=assessment)
        self.assertFalse(report["scientific_quality_validated"])
        self.assertFalse(report["independent_peer_review_performed"])
        self.assertFalse(report["drive_sync_verified"])
        findings=report["priority_findings"]
        self.assertIn("CLAIM_POSSIBLE_SEMANTIC_OVERREACH",
                      {r["code"] for r in findings})
        self.assertTrue(any("possible claim overreach" in action.lower()
                            for action in report["actions"]))
        self.assertNotIn(case["source_passage"],json.dumps(report))
        self.assertNotIn(case["claim_text"],json.dumps(report))

    def test_strict_cli_returns_pending_review_for_heuristic_risk(self):
        import contextlib
        import io
        from semantic_claim_review import main as review_main
        case=exercise.load_frozen(BENCH)["cases"][4]
        root=self.root/"strict_review"
        exercise.prepare(root,case)
        assessments=root/"synthetic_declaration.json"
        assessments.write_text(json.dumps(exercise.assessment(root,case,label_aware=False)),
                               encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()) as output:
            exit_code=review_main([str(root),"--assessments",str(assessments),"--strict"])
        self.assertEqual(exit_code,2)
        report=json.loads(output.getvalue())
        self.assertGreater(report["heuristic_risk_occurrences"],0)
        self.assertFalse(report["gate_approval_performed"])
        self.assertFalse(report["semantic_support_proven"])

    def test_strict_cli_no_heuristic_flag_does_not_prove_validity(self):
        import contextlib
        import io
        from semantic_claim_review import main as review_main
        case=exercise.load_frozen(BENCH)["cases"][0]
        root=self.root/"narrow_supported"
        exercise.prepare(root,case)
        a=root/"synthetic_declaration.json"
        a.write_text(json.dumps(exercise.assessment(root,case,label_aware=False)),
                     encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()) as output:
            exit_code=review_main([str(root),"--assessments",str(a),"--strict"])
        self.assertEqual(exit_code,0)
        record=json.loads(output.getvalue())
        self.assertEqual(record["heuristic_risk_occurrences"],0)
        self.assertFalse(record["semantic_support_proven"])
        self.assertFalse(record["researcher_authenticated"])

    def test_existing_output_is_not_replaced(self):
        self.out.mkdir()
        before=self.out/"original.csv"
        before.write_text("PRIVATE_DATA_DO_NOT_MODIFY")
        with self.assertRaisesRegex(ValueError,"new result directory"):
            exercise.evaluate(BENCH,self.out,source_commit=COMMIT)
        self.assertEqual(before.read_text(),"PRIVATE_DATA_DO_NOT_MODIFY")

    def test_nonrevision_rejected_before_mutation(self):
        with self.assertRaisesRegex(ValueError,"Exact source commit"):
            exercise.evaluate(BENCH,self.out,source_commit="not-a-sha")
        self.assertFalse(self.out.exists())

    def test_exported_evidence_omits_full_source_and_does_not_claim_people(self):
        res=exercise.evaluate(BENCH,self.out,source_commit=COMMIT)
        content=" ".join(p.read_text() for p in self.out.rglob("*.json") if p.is_file())
        for item in exercise.load_frozen(BENCH)["cases"]:
            self.assertNotIn(item["source_passage"],content)
            self.assertNotIn(item["claim_text"],content)
        self.assertNotIn("SYNTHETIC_NOT_AN_ACTUAL_HUMAN_REVIEWER",content)
        self.assertEqual(res["human_participants"],False)
        self.assertEqual(res["real_academic_provider_queries"],0)
        self.assertEqual(res["counterexamples"],[
            item["case_id"] for item in res["results"]
            if item["gold_support"]!="SUPPORTED" and not item["semantic_discrepancy_flagged"]])

if __name__=="__main__":
    unittest.main()
