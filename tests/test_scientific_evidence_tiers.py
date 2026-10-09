"""Software-only regression fixtures; no invented scientific evaluation."""
from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from scientific_evidence_tiers import audit


class ScientificEvidenceTiersTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.m=self.root/"00_Gestao_e_Continuidade"
        self.m.mkdir()
        self.write_json("PROJECT_CONFIG.json", {
            "method_route_governance_required": True,
            "method_route": "QUANTITATIVE",
        })
        self.write_json("METHOD_PROFILE.json", {
            "schema_version":1,
            "route":"QUANTITATIVE",
            "evidence_status":"NOT_EXECUTED",
            "material_evidence_ref":"",
            "analysis_evidence_ref":"",
        })

    def write_json(self,name,data):
        (self.m/name).write_text(json.dumps(data),encoding="utf-8")

    def write_csv(self,name,rows):
        if not rows:
            raise AssertionError("Fixture rows required")
        with (self.m/name).open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)

    def test_empty_workspace_never_claims_independent_validation(self):
        r=audit(self.root)
        self.assertFalse(r["empirical_scientific_result_independently_validated"])
        self.assertFalse(r["literal_locator_proves_claim_semantics"])
        self.assertFalse(r["human_review_record_authenticates_reviewer"])
        self.assertEqual(r["layers"]["empirical_result_claims"], 0)

    def test_empirical_result_without_executed_data_cannot_be_frozen(self):
        self.write_csv("09_Claims_Ledger.csv", [
            {"Claim_ID":"claim-placeholder",
             "Claim_type":"EMPIRICAL_RESULT",
             "Trace_IDs":"",
             "Researcher_review_evidence":""}
        ])
        r=audit(self.root,freeze=True)
        self.assertGreaterEqual(len(r["errors"]), 3)
        self.assertTrue(any("no recorded completed analysis" in x for x in r["errors"]))

    def test_preliminary_draft_is_not_presented_as_validated(self):
        self.write_csv("09_Claims_Ledger.csv", [
            {"Claim_ID":"claim-placeholder","Claim_type":"EMPIRICAL_RESULT",
             "Trace_IDs":"","Researcher_review_evidence":""}
        ])
        r=audit(self.root,freeze=False)
        self.assertFalse(r["errors"])
        self.assertEqual(r["layers"]["empirical_result_claims"],1)
        self.assertFalse(r["empirical_scientific_result_independently_validated"])

    def test_bibliographic_lookup_never_proves_semantics(self):
        # Static marker inspection only; not fabricated scholarly metadata.
        r=audit(self.root)
        self.assertIs(r["bibliographic_identity_proves_text_read"],False)
        self.assertIs(r["literal_locator_proves_claim_semantics"],False)


if __name__ == "__main__":
    unittest.main()
