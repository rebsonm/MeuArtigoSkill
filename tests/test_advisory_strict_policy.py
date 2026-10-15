"""REG-011/013 policy: lexical hints cannot masquerade as objective blockers.

All fixtures are synthetic and do not authenticate a researcher.
"""
from __future__ import annotations
import contextlib
import csv
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import evaluate_semantic_challenge as fixture
import semantic_claim_review as claims
import scientific_diagnostic as diagnostic

EXAMPLES=ROOT/"benchmarks/claim_support_challenge_v1.json"

class AdvisoryVersusBlockingPolicyTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.base=Path(t.name)
        self.cases=fixture.load_frozen(EXAMPLES)["cases"]

    def project(self,case_index=4,*,complete_protocol=False):
        root=self.base/("case-"+str(case_index))
        item=self.cases[case_index]
        fixture.prepare(root,item)
        if complete_protocol:
            with (root/claims.MGMT/"01_Protocolo.csv").open(
                    "w",encoding="utf-8-sig",newline="") as stream:
                writer=csv.DictWriter(
                    stream,fieldnames=["Item","Decision","Rationale","Status"])
                writer.writeheader()
                writer.writerow({
                    "Item":"Synthetic protocol","Decision":"Bounded synthetic review",
                    "Rationale":"This is a simulated protocol for software tests only.",
                    "Status":"RECORDED"})
        annotation=fixture.assessment(root,item,label_aware=False)
        path=root/"synthetic_assessment.json"
        path.write_text(json.dumps(annotation),encoding="utf-8")
        return root,path,item

    def run_claims(self,root,assessment=None):
        argv=[str(root)]
        if assessment is not None: argv.extend(["--assessments",str(assessment)])
        argv.append("--strict")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            status=claims.main(argv)
        return status,json.loads(out.getvalue())

    def run_diagnostic(self,root,assessment=None):
        argv=[str(root),"--format","json","--strict"]
        if assessment is not None: argv.extend(["--assessments",str(assessment)])
        with contextlib.redirect_stdout(io.StringIO()) as out:
            status=diagnostic.main(argv)
        return status,json.loads(out.getvalue())

    def test_heuristic_only_never_blocks_a_formally_complete_review(self):
        root,path,item=self.project(4,complete_protocol=True)
        rc,report=self.run_claims(root,path)
        self.assertEqual(rc,0)
        self.assertEqual(report["formal_review_requirements_pending"],0)
        row=report["review_items"][0]
        self.assertTrue(row["heuristic_review_needed"])
        self.assertTrue(row["semantic_risk_codes"])
        self.assertEqual(row["heuristic_severity"],"ADVISORY")
        self.assertFalse(row["heuristic_blocks_workflow"])
        self.assertEqual(row["status"],
                         "HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED")
        self.assertFalse(report["semantic_support_proven"])
        self.assertFalse(report["gate_approval_performed"])
        self.assertFalse(report["researcher_authenticated"])

    def test_compact_diagnostic_keeps_heuristic_review_without_blocking(self):
        root,path,item=self.project(4,complete_protocol=True)
        rc,report=self.run_diagnostic(root,path)
        self.assertEqual(rc,0)
        self.assertGreater(report["counts"]["heuristic_advisory_occurrences"],0)
        self.assertEqual(report["counts"]["strict_required_occurrences"],0)
        self.assertEqual(report["counts"]["blocking_occurrences"],0)
        self.assertIn("CLAIM_POSSIBLE_SEMANTIC_OVERREACH",
                      {x["code"] for x in report["priority_findings"]})
        self.assertEqual(report["verdict"],"REVISAO_CIENTIFICA_PENDENTE")
        self.assertFalse(report["scientific_quality_validated"])
        self.assertFalse(report["independent_peer_review_performed"])
        self.assertNotIn(item["source_passage"],json.dumps(report))
        self.assertNotIn(item["claim_text"],json.dumps(report))

    def test_missing_required_human_review_still_fails_strict(self):
        root,path,item=self.project(4,complete_protocol=True)
        rc,report=self.run_claims(root)
        self.assertEqual(rc,2)
        self.assertEqual(report["review_items"][0]["status"],"PENDING_HUMAN_REVIEW")
        self.assertEqual(report["formal_review_requirements_pending"],1)
        rc,report=self.run_diagnostic(root)
        self.assertEqual(rc,2)
        self.assertGreater(report["counts"]["strict_required_occurrences"],0)

    def test_invented_literal_passage_still_fails_strict(self):
        root,path,item=self.project(4,complete_protocol=True)
        raw=json.loads(path.read_text())
        raw["reviews"][0]["quoted_passage"]=(
            "A completely made up passage with no resemblance to this source.")
        path.write_text(json.dumps(raw),encoding="utf-8")
        rc,report=self.run_claims(root,path)
        self.assertEqual(rc,2)
        self.assertEqual(report["review_items"][0]["status"],
                         "QUOTED_PASSAGE_NOT_CONFIRMED")
        rc,diag=self.run_diagnostic(root,path)
        self.assertEqual(rc,2)
        self.assertGreater(diag["counts"]["blocking_occurrences"],0)

    def test_stale_local_source_cannot_be_downgraded_to_advisory(self):
        root,path,item=self.project(4,complete_protocol=True)
        (root/"synthetic_source.txt").write_text(
            item["source_passage"]+"\nCHANGED AFTER HASH",encoding="utf-8")
        rc,report=self.run_claims(root,path)
        self.assertEqual(rc,2)
        self.assertEqual(report["review_items"][0]["status"],
                         "SOURCE_REPORT_UNAVAILABLE_OR_STALE")
        rc,diag=self.run_diagnostic(root,path)
        self.assertEqual(rc,2)
        self.assertGreater(diag["counts"]["strict_required_occurrences"],0)

    def test_wrong_reference_cannot_be_downgraded_to_advisory(self):
        root,path,item=self.project(4,complete_protocol=True)
        ledger=root/claims.MGMT/"09_Claims_Ledger.csv"
        original=ledger.read_text(encoding="utf-8-sig")
        ledger.write_text(original.replace("EVID-0001","EVID-9999"),
                          encoding="utf-8-sig")
        rc,report=self.run_claims(root,path)
        self.assertEqual(rc,2)
        self.assertEqual(report["review_items"][0]["status"],
                         "SOURCE_REPORT_UNAVAILABLE_OR_STALE")
        rc,diag=self.run_diagnostic(root,path)
        self.assertEqual(rc,2)
        self.assertGreater(diag["counts"]["strict_required_occurrences"],0)

    def test_formal_support_cannot_autoapprove_without_heuristics(self):
        root,path,item=self.project(0,complete_protocol=True)
        rc,report=self.run_claims(root,path)
        self.assertEqual(rc,0)
        self.assertEqual(report["heuristic_risk_occurrences"],0)
        self.assertFalse(report["semantic_support_proven"])
        self.assertFalse(report["review_declared_is_authenticated"])
        self.assertFalse(report["gate_approval_performed"])

if __name__=="__main__":
    unittest.main()
