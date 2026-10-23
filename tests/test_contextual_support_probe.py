"""Experimental contextual REG-011 sidecar; no automated scientific judgments."""
from __future__ import annotations
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from contextual_support_probe import examine
import semantic_claim_review as reg011
import scientific_diagnostic as reg013
import evaluate_semantic_challenge as fixture
import compare_contextual_probes as compare
from evaluation_registry import read_ledger
from evaluation_package import validate as replay_verify

BENCH=ROOT/"benchmarks/claim_support_heldout_v1.json"

class ContextualProbeTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)

    def test_observational_attribution_is_advisory(self):
        r=examine(
            "The interface redesign was responsible for faster case handling.",
            "This is an observational comparison. Groups differed in workload and staff.")
        self.assertIn("CONTEXT_CAUSAL_ATTRIBUTION", [x["code"] for x in r["signals"]])
        self.assertEqual(r["status"],"SCREENED_EXPERIMENTAL_CONTEXT_ONLY")
        self.assertFalse(r["can_block_scientific_workflow"])
        self.assertFalse(r["entailment_proven"])
        self.assertTrue(r["human_review_required"])

    def test_qualified_causal_denial_is_not_automatically_suspicious(self):
        r=examine(
            "The pilot did not establish that the checklist caused an improvement.",
            "The pilot was observational and assignment was not randomized.")
        self.assertNotIn("CONTEXT_CAUSAL_ATTRIBUTION",[x["code"] for x in r["signals"]])
        self.assertFalse(r["entailment_proven"])

    def test_population_scope_and_its_qualification(self):
        p="The small exploratory study interviewed six clerks at a single archive."
        bad=examine("There was a widespread pattern throughout public administration.",p)
        self.assertIn("CONTEXT_POPULATION_SCOPE",[x["code"] for x in bad["signals"]])
        qualified=examine(
            "Within the sample, six clerks described indexing delays.",p)
        self.assertNotIn("CONTEXT_POPULATION_SCOPE",[x["code"] for x in qualified["signals"]])

    def test_unmeasured_outcomes_are_not_fabricated(self):
        excerpt="The data collection had not started. No results were reported."
        r=examine("The new procedure proved effective at avoiding delays.",excerpt)
        self.assertIn("CONTEXT_UNOBSERVED_OUTCOME",[x["code"] for x in r["signals"]])
        qualified=examine("No improvement can be assessed yet.",excerpt)
        self.assertNotIn("CONTEXT_UNOBSERVED_OUTCOME",[x["code"] for x in qualified["signals"]])

    def test_metadata_status_and_research_design_cautions(self):
        p="The proposal required substantial revision and should not proceed to recruitment."
        r=examine("The review board cleared the proposal to begin recruitment.",p)
        self.assertIn("CONTEXT_STATUS_CONTRADICTION",[x["code"] for x in r["signals"]])
        r=examine("The experiment used an automated classifier.",
                  "The requests were manually sorted; no machine-learning system was used.")
        self.assertIn("CONTEXT_MANUAL_AUTOMATED_METHOD",[x["code"] for x in r["signals"]])

    def test_bounded_inputs_privacy_and_deterministic_output(self):
        c="The intervention proved effective for all users."
        s="Data collection had not started and no results were reported."
        r=examine(c,s)
        self.assertEqual(r,examine(c,s))
        self.assertNotIn(c,json.dumps(r))
        self.assertNotIn(s,json.dumps(r))
        self.assertFalse(r["independent_scientific_validation"])
        self.assertEqual(examine("",s)["status"],"NOT_EVALUATED")
        self.assertEqual(examine("x"*13000,s)["status"],"NOT_EVALUATED")

    def test_real_reg011_integrates_both_probes_and_preserves_gates(self):
        item=fixture.load_frozen(
            ROOT/"benchmarks/claim_support_challenge_v1.json")["cases"][4]
        project=self.root/"project"
        fixture.prepare(project,item)
        a=fixture.assessment(project,item,label_aware=False)
        result=reg011.review(project,a)
        row=result["review_items"][0]
        self.assertEqual(row["status"],"HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED")
        self.assertEqual(row["contextual_probe_status"],
                         "SCREENED_EXPERIMENTAL_CONTEXT_ONLY")
        self.assertEqual(row["heuristic_severity"],"ADVISORY")
        self.assertFalse(row["contextual_signals_block_workflow"])
        self.assertFalse(row["heuristic_blocks_workflow"])
        self.assertFalse(result["contextual_signals_can_block_workflow"])
        self.assertFalse(result["contextual_signal_absence_proves_support"])
        self.assertFalse(result["semantic_support_proven"])
        self.assertFalse(result["gate_approval_performed"])
        self.assertNotIn(item["source_passage"],json.dumps(result))
        self.assertNotIn(item["claim_text"],json.dumps(result))

    def test_reg013_exposes_independent_review_only_context_code(self):
        item=fixture.load_frozen(
            ROOT/"benchmarks/claim_support_challenge_v1.json")["cases"][4]
        root=self.root/"diag"
        fixture.prepare(root,item)
        with (root/reg011.MGMT/"01_Protocolo.csv").open(
                "w",encoding="utf-8-sig",newline="") as stream:
            writer=csv.DictWriter(stream,fieldnames=["Item","Decision","Rationale","Status"])
            writer.writeheader()
            writer.writerow({
                "Item":"Synthetic","Decision":"Bounded only",
                "Rationale":"A fictional exercise testing only the screening software.",
                "Status":"RECORDED"})
        review=fixture.assessment(root,item,label_aware=False)
        result=reg013.compose(root,assessments=review)
        item_codes={x["code"]:x["severity"] for x in result["priority_findings"]}
        self.assertEqual(item_codes.get("CLAIM_POSSIBLE_CONTEXTUAL_MISMATCH"),"REVIEW")
        self.assertGreater(result["counts"]["contextual_advisory_occurrences"],0)
        self.assertEqual(result["counts"]["blocking_occurrences"],0)
        self.assertEqual(result["counts"]["strict_required_occurrences"],0)
        self.assertFalse(result["scientific_quality_validated"])
        self.assertNotIn(item["source_passage"],json.dumps(result))

    def test_source_without_authenticated_quote_skips_context_probe(self):
        item=fixture.load_frozen(
            ROOT/"benchmarks/claim_support_challenge_v1.json")["cases"][4]
        root=self.root/"pending"
        fixture.prepare(root,item)
        data=reg011.review(root)
        row=data["review_items"][0]
        self.assertEqual(row["contextual_probe_status"],"NOT_EVALUATED")
        self.assertEqual(row["contextual_signal_codes"],[])
        self.assertEqual(row["status"],"PENDING_HUMAN_REVIEW")

    def test_reproducible_development_exposed_parallel_comparison(self):
        out=self.root/"comparison"
        result=compare.evaluate(BENCH,out,revision="a"*40)
        self.assertEqual(result["case_count"],24)
        self.assertEqual(result["lexical"]["true_positive"]+result["lexical"]["false_negative"],18)
        self.assertEqual(result["lexical"]["false_positive"]+result["lexical"]["true_negative"],6)
        self.assertEqual(result["contextual"]["true_positive"]+result["contextual"]["false_negative"],18)
        self.assertEqual(result["contextual"]["false_positive"]+result["contextual"]["true_negative"],6)
        self.assertEqual(len(read_ledger(out/"evaluation_runs.jsonl")),2)
        score=replay_verify(out/"comparison-replay.zip")
        self.assertEqual(score["observed_total"],48)
        self.assertFalse(score["scientific_validity_proven"])
        self.assertFalse(result["blind_prospective_holdout"])
        self.assertFalse(result["scientific_validity_established"])
        self.assertFalse(result["independent_human_review"])
        for case in result["cases"]:
            ev=(out/"evidence"/(case["case_id"]+".json"))
            self.assertTrue(ev.is_file())
            report=json.loads(ev.read_text(encoding="utf-8"))
            self.assertEqual(report["human_review_authenticated"],False)
        body=" ".join(p.read_text(encoding="utf-8") for p in out.rglob("*.json"))
        frozen=compare.frozen(BENCH)
        for case in frozen["cases"]:
            self.assertNotIn(case["source_passage"],body)
            self.assertNotIn(case["claim_text"],body)

    def test_comparison_output_is_create_only(self):
        out=self.root/"before"
        out.mkdir()
        marker=out/"valuable-record.txt"
        marker.write_text("PRESERVED")
        with self.assertRaises(ValueError):
            compare.evaluate(BENCH,out,revision="a"*40)
        self.assertEqual(marker.read_text(),"PRESERVED")

if __name__=="__main__":
    unittest.main()
