"""End-to-end controlled execution on synthetic cases, with real code invoked."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import run_critical_cases as run
from evaluation_registry import read_ledger
from evaluation_package import validate as replay_verify


class ExecutedCriticalCaseTests(unittest.TestCase):
    def setUp(self):
        td=tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self.root=Path(td.name)
        self.out=self.root/"results"
        self.catalog=ROOT/"benchmarks/critical_cases_v1.json"
        self.sha="a"*40

    def test_all_twelve_controls_actually_invoked_and_recorded(self):
        result=run.execute(self.catalog,self.out,skill_commit=self.sha)
        self.assertEqual(result["catalog_cases"],12)
        self.assertEqual(len(result["cases"]),12)
        self.assertEqual(result["observed"],12)
        self.assertEqual(result["not_evaluated"],0)
        self.assertEqual(result["matches_expected"],12)
        self.assertEqual(result["mismatches"],0)
        for case in result["cases"]:
            self.assertIs(case["matches_expected"],True,case["case_id"])
            evidence=self.out/"evidence"/(case["case_id"]+".json")
            self.assertTrue(evidence.is_file())
            proof=json.loads(evidence.read_text(encoding="utf-8"))
            self.assertEqual(proof["observed_action"],case["observed"])
            self.assertEqual(run.sha(evidence.read_bytes()),case["proof_sha256"])
            self.assertTrue(proof["actual_control_invoked"])
            self.assertFalse(proof["scientific_validity_established"])
            self.assertFalse(proof["real_research_corpus_used"])
        ledger=read_ledger(self.out/"evaluation_runs.jsonl")
        self.assertEqual(len(ledger),1)
        self.assertEqual(ledger[0]["result"]["observed"],12)
        self.assertEqual(ledger[0]["result"]["matches_expected"],12)
        summary=replay_verify(self.out/"evaluation-replay.zip")
        self.assertEqual(summary["observed_total"],12)
        self.assertFalse(summary["scientific_validity_proven"])

    def test_cases_without_real_providers_do_not_call_network(self):
        import verify_sources
        with patch.object(verify_sources,"provider_query",side_effect=AssertionError("LIVE_NETWORK")):
            for cid in ("DOI-001","DOI-002"):
                result=run.probe(cid,self.root/cid)
                self.assertEqual(result["observed_action"],"FLAG")
                self.assertEqual(result["providers_checked"],2)

    def test_overstated_support_is_only_formally_detected(self):
        result=run.probe("SUP-004",self.root/"support")
        self.assertEqual(result["observed_action"],"FLAG")
        self.assertEqual(result["control_status"],"UNQUALIFIED_SUPPORT_CONTRADICTS_REVIEW")
        self.assertFalse(result["semantic_entailment_verified"])

    def test_gate_approval_is_refused_and_gate_file_is_unchanged(self):
        result=run.probe("GAT-005",self.root/"gates")
        self.assertEqual(result["observed_action"],"BLOCK")
        self.assertTrue(result["gate_file_unchanged"])
        self.assertNotEqual(result["return_code"],0)

    def test_fulltext_without_local_source_denied(self):
        result=run.probe("ACC-009",self.root/"rights")
        self.assertEqual(result["observed_action"],"BLOCK")
        self.assertGreater(result["control_errors_count"],0)

    def test_storage_is_presentation_only_no_remote_receipt(self):
        result=run.probe("STO-006",self.root/"storage")
        self.assertEqual(result["boundary"],"READ_ONLY_PRESENTATION_ONLY")
        self.assertEqual(result["observed_action"],"BLOCK")
        self.assertFalse(result["drive_receipt_present"])

    def test_failed_case_stays_mismatch_and_cannot_be_called_success(self):
        original=run.probe
        def broken(cid,root):
            if cid=="DOI-001":
                root.mkdir()
                return {"observed_action":"PASS","finding":"NO_EXPECTED_FINDING"}
            return original(cid,root)
        with patch.object(run,"probe",side_effect=broken):
            result=run.execute(self.catalog,self.out,skill_commit=self.sha,
                               record_ledger=False)
        self.assertEqual(result["mismatches"],1)
        self.assertEqual(result["matches_expected"],11)
        self.assertEqual(result["observed"],12)
        self.assertFalse((self.out/"evaluation_runs.jsonl").exists())

    def test_exception_is_not_evaluated_and_never_passed(self):
        original=run.probe
        def failing(cid,root):
            if cid=="LOC-003":
                raise RuntimeError("Synthetic failed control execution")
            return original(cid,root)
        with patch.object(run,"probe",side_effect=failing):
            result=run.execute(self.catalog,self.out,skill_commit=self.sha,
                               record_ledger=False)
        item=next(x for x in result["cases"] if x["case_id"]=="LOC-003")
        self.assertEqual(result["not_evaluated"],1)
        self.assertIsNone(item["matches_expected"])
        self.assertEqual(item["observed"],"NOT_EVALUATED")
        proof=json.loads((self.out/"evidence"/"LOC-003.json").read_text())
        self.assertEqual(proof["error_class"],"RuntimeError")
        self.assertFalse(proof["actual_control_invoked"])

    def test_catalog_change_requires_explicit_adapter_review(self):
        changed=json.loads(self.catalog.read_text(encoding="utf-8"))
        changed["cases"][0]["control"]="invented_unused_control"
        filename=self.root/"modified_catalog.json"
        filename.write_text(json.dumps(changed),encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"adapter"):
            run.execute(filename,self.out,skill_commit=self.sha)
        self.assertFalse(self.out.exists())

    def test_output_is_create_only_no_existing_outputs_overwritten(self):
        self.out.mkdir()
        marker=self.out/"research_record.csv"
        marker.write_text("DO_NOT_REPLACE",encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"NEW output directory"):
            run.execute(self.catalog,self.out,skill_commit=self.sha)
        self.assertEqual(marker.read_text(),"DO_NOT_REPLACE")

    def test_invalid_revision_rejected_without_claiming_provenance(self):
        with self.assertRaisesRegex(ValueError,"40-hex"):
            run.execute(self.catalog,self.out,skill_commit="not-a-sha")
        self.assertFalse(self.out.exists())

    def test_sanitized_outputs_no_private_material_or_api_credentials(self):
        result=run.execute(self.catalog,self.out,skill_commit=self.sha)
        text="".join(p.read_text(encoding="utf-8") for p in self.out.rglob("*.json"))
        for secret in ("api.crossref.org","OPENALEX_API_KEY","PRIVATE_RESEARCH_CORPUS",
                       "Human gate approved by ChatGPT","synthetic-real-user@"):
            self.assertNotIn(secret,text)
        self.assertFalse(result["independent_scientific_validation"])
        self.assertEqual(result["real_academic_provider_queries_performed"],0)
        self.assertFalse(result["google_drive_write"])

if __name__=="__main__":
    unittest.main()
