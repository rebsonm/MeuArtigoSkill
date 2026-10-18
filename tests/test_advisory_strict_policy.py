"""REG-011/013 policy: lexical hints cannot masquerade as objective blockers.

Adapted from PR #65 for the current sanitized diagnostic CLI; detailed
scientific findings are inspected in process, not printed to a terminal.

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
        # Current privacy contract: detailed findings stay IN PROCESS.
        # scientific_diagnostic.main() prints only a bounded safe summary.
        reviews=claims.local_json(root,assessment) if assessment is not None else None
        result=diagnostic.compose(root,assessments=reviews)
        strict_pending=result["counts"]["strict_required_occurrences"]
        return (2 if strict_pending else 0),result

    def test_diagnostic_cli_stdout_is_bounded_and_science_unapproved(self):
        root,path,item=self.project(4,complete_protocol=True)
        with contextlib.redirect_stdout(io.StringIO()) as out:
            rc=diagnostic.main([str(root),"--assessments",str(path),
                                "--format","json","--strict"])
        safe=json.loads(out.getvalue())
        self.assertEqual(safe["status"],"SCIENTIFIC_DIAGNOSTIC_REVIEW_REQUIRED")
        self.assertFalse(safe["scientific_quality_validated"])
        self.assertFalse(safe["source_details_disclosed"])
        self.assertTrue(safe["human_review_required"])
        self.assertNotIn("priority_findings",safe)
        self.assertNotIn("review_items",safe)
        self.assertNotIn(item["source_passage"],out.getvalue())
        self.assertNotIn(item["claim_text"],out.getvalue())

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
        # The annotation references a pair now absent from the ledger;
        # fail closed on malformed input rather than emit a fabricated report.
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                rc=claims.main([str(root),"--assessments",str(path),"--strict"])
        self.assertEqual(rc,1)
        self.assertEqual(stdout.getvalue(),"")
        self.assertIn("absent from the canonical literature ledger",stderr.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                rc=diagnostic.main([str(root),"--assessments",str(path),
                                    "--format","json","--strict"])
        self.assertEqual(rc,1)
        self.assertEqual(stdout.getvalue(),"")
        self.assertIn("DIAGNOSTIC_ERROR: INPUT_OR_OUTPUT_BLOCKED",stderr.getvalue())

    def test_adverse_declared_outcomes_hold_strict_even_without_lexical_flags(self):
        for index,expected in ((4,"PARTIALLY_SUPPORTED"),
                               (8,"NOT_SUPPORTED"),(12,"INCONCLUSIVE")):
            with self.subTest(verdict=expected):
                root,path,item=self.project(index,complete_protocol=True)
                path.write_text(json.dumps(fixture.assessment(
                    root,item,label_aware=True)),encoding="utf-8")
                rc,record=self.run_claims(root,path)
                self.assertEqual(rc,2)
                self.assertEqual(record["review_items"][0]["status"],
                                 "HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED")
                self.assertEqual(record["review_items"][0]["declared_judgment"],
                                 expected)
                self.assertEqual(record["formal_review_requirements_pending"],1)
                self.assertFalse(record["semantic_support_proven"])
                rc,diag=self.run_diagnostic(root,path)
                self.assertEqual(rc,2)
                self.assertGreater(diag["counts"]["strict_required_occurrences"],0)
                self.assertFalse(diag["scientific_quality_validated"])

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
