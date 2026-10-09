"""Offline adversarial regression for claim types and novelty boundaries.

Any invented claim/source text in these tests is a disposable software fixture,
not a benchmark of real scientific literature or a research output.
"""
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import claim_integrity as ci


class ClaimIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.evidence=[
            {"Evidence_ID":"EVID-0001","Supporting_locator":"p. 4: methodological limitations and institutional context."},
            {"Evidence_ID":"EVID-0002","Supporting_locator":"p. 12: comparative evidence and conditional applicability."},
        ]
        self.search=[{"Search_ID":"SEARCH-0001","Literal_query":"governance AND models",
                      "Status":"COMPLETE","Records_exported":"12"}]
        self.claim={
            "Claim_ID":"CLAIM-0001","Claim_type":"LITERATURE",
            "Claim_text":"The cited study discusses the organizational processes involved in evaluation.",
            "Evidence_IDs":"EVID-0001","Locator_status":"MATCHED",
            "Robustness_status":"ROBUST","Human_validation":"VALIDATED","Draft_status":"READY",
            "Researcher_review_evidence":"Researcher review logged in an actual dated research note.",
        }

    def check(self,change=None,freeze=True):
        claim={**self.claim,**(change or {})}
        return ci.audit([claim],self.evidence,self.search,strict=True,freeze=freeze,
                        headers=[*self.claim,*ci.EXTRA_COLUMNS])

    def test_literature_claim_has_grounding_and_human_reference(self):
        self.assertEqual(self.check()["errors"],[])

    def test_literature_claim_without_evidence_is_blocked(self):
        self.assertTrue(any("[L] requires" in x for x in self.check({"Evidence_IDs":""})["errors"]))

    def test_literal_source_has_to_contain_locator(self):
        self.evidence[0]["Supporting_locator"]=""
        self.assertTrue(any("lacks a source locator" in x for x in self.check()["errors"]))

    def test_unknown_evidence_id_cannot_be_invented(self):
        self.assertTrue(any("unknown Evidence_ID" in x for x in self.check({"Evidence_IDs":"EVID-9999"})["errors"]))

    def test_inference_requires_warrant_and_limits(self):
        change={"Claim_type":"INFERENCE","Inference_warrant":"",
                "Boundary_conditions":"Some contextual boundaries apply to the cited processes."}
        self.assertTrue(any("reasoning" in x for x in self.check(change)["errors"]))
        change["Inference_warrant"]="By comparing distinct mechanisms the analysis infers a plausible conditional relationship."
        self.assertEqual(self.check(change)["errors"],[])

    def test_inference_without_boundary_is_blocked(self):
        report=self.check({"Claim_type":"[I]","Inference_warrant":
            "A contextual interpretation follows from the documented relationship between the two constructs.",
            "Boundary_conditions":""})
        self.assertTrue(any("boundary" in x for x in report["errors"]))

    def test_proposition_must_address_closest_literature_and_contribution(self):
        change={"Claim_type":"PROPOSITION","Evidence_IDs":"","Nearest_prior_Evidence_IDs":"",
                "Contribution_delta":"","Novelty_scope":"","Novelty_search_ref":""}
        report=self.check(change)
        self.assertGreaterEqual(len(report["errors"]),4)

    def test_proposition_with_bounded_scope_does_not_pretend_absolute_novelty(self):
        change={"Claim_type":"PROPOSITION","Nearest_prior_Evidence_IDs":"EVID-0002",
            "Contribution_delta":"This proposal connects previously distinct responsibilities into a testable administrative model.",
            "Novelty_scope":"Within the selected literature on administrative coordination, this is a proposed conceptual extension.",
            "Novelty_search_ref":"SEARCH-0001"}
        self.assertEqual(self.check(change)["errors"],[])

    def test_novelty_string_cannot_prove_absolute_precedence(self):
        for language in [
            "Este é o primeiro estudo de rastreabilidade científica sobre essa abordagem.",
            "O modelo é inédito para qualquer organização.",
            "This is the first-ever model applied in research.",
            "No prior studies have explored this organizational mechanism.",
        ]:
            with self.subTest(language=language):
                result=self.check({"Claim_type":"PROPOSITION","Claim_text":language})
                self.assertTrue(any("categorical priority" in x for x in result["errors"]))

    def test_categorical_wording_is_warning_while_drafting(self):
        report=self.check({"Draft_status":"DRAFT",
            "Claim_text":"O modelo é inédito para todas as organizações."},freeze=False)
        self.assertFalse(any("categorical priority" in x for x in report["errors"]))
        self.assertTrue(any("categorical priority" in x for x in report["warnings"]))

    def test_search_reference_must_exist(self):
        change={"Claim_type":"PROPOSITION","Nearest_prior_Evidence_IDs":"EVID-0002",
            "Contribution_delta":"This study proposes a contextual extension to existing conceptual approaches.",
            "Novelty_scope":"Only for the defined sampled publications within this specified literature corpus.",
            "Novelty_search_ref":"SEARCH-9090"}
        self.assertTrue(any("unknown Search_ID" in x for x in self.check(change)["errors"]))

    def test_planned_search_cannot_prove_novelty_audit(self):
        self.search[0]["Status"]="PLANNED"
        change={"Claim_type":"PROPOSITION","Nearest_prior_Evidence_IDs":"EVID-0002",
            "Contribution_delta":"This study proposes a contextual extension to existing conceptual approaches.",
            "Novelty_scope":"Only for the defined sampled publications within this specified literature corpus.",
            "Novelty_search_ref":"SEARCH-0001"}
        self.assertTrue(any("executed and reproducible" in x for x in self.check(change)["errors"]))

    def test_researcher_review_is_not_silently_assumed(self):
        result=self.check({"Researcher_review_evidence":"", "Human_validation":"PENDING"})
        self.assertTrue(any("researcher" in x for x in result["errors"]))

    def test_source_metadata_is_not_semantic_verification(self):
        report=self.check()
        self.assertIs(report["semantic_support_proven"],False)
        self.assertIs(report["novelty_proven"],False)

    def test_legacy_draft_has_no_automatic_full_freeze(self):
        claim={"Claim_ID":"CLAIM-0001","Claim_type":"INFERENCE",
               "Claim_text":"This proposed relationship may be limited to the studied setting."}
        check=ci.audit([claim],self.evidence,self.search,strict=False,freeze=False)
        self.assertFalse(check["errors"])
        self.assertTrue(check["warnings"])

    def test_cli_rejects_frozen_claim_without_prior_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/ci.MGMT
            folder.mkdir()
            def write(name,cols,items):
                with (folder/name).open("w",encoding="utf-8",newline="") as f:
                    writer=csv.DictWriter(f,fieldnames=cols)
                    writer.writeheader();writer.writerows(items)
            one={**self.claim,"Claim_type":"PROPOSITION"}
            write("09_Claims_Ledger.csv",list(one)+[x for x in ci.EXTRA_COLUMNS if x not in one],[one])
            write("05_Evidence_Matrix.csv",list(self.evidence[0]),self.evidence)
            write("02_Search_Log.csv",list(self.search[0]),self.search)
            result=subprocess.run([sys.executable,str(ROOT/"scripts/claim_integrity.py"),tmp,"--strict","--freeze"],
                                  capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn("nearest",result.stdout.lower())


if __name__=="__main__":
    unittest.main()
