"""Offline regression coverage for the adversarial-case observation ledger."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
import evaluation_registry as er

CATALOG = ROOT/"benchmarks/critical_cases_v1.json"

class EvaluationRegistryTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.temp = Path(tmp.name)
        self.ledger = self.temp/"results.jsonl"
        self.data = er.load(CATALOG)
        self.cases = er.validate_catalog(self.data)
        self.assertEqual(len(self.cases), 12)

    def observations(self, rowlist, suffix):
        path = self.temp/(suffix+".json")
        path.write_text(json.dumps({"schema_version":1,"cases":rowlist}),encoding="utf-8")
        return path

    def test_empty_observations_are_not_fake_success(self):
        stats = er.summarize(self.cases, {})
        self.assertIsNone(stats["match_rate_on_observed"])
        self.assertEqual(stats["observed"],0)
        self.assertEqual(stats["not_evaluated"],12)
        self.assertFalse(stats["scientific_validity_established"])

    def test_record_verify_and_reject_duplicate_run(self):
        obs = self.observations([], "empty")
        one = er.record(CATALOG,obs,self.ledger,"run-001","a"*40)
        self.assertEqual(len(er.read_ledger(self.ledger)),1)
        with self.assertRaisesRegex(ValueError,"Duplicate"):
            er.record(CATALOG,obs,self.ledger,"run-001","a"*40)
        two = er.record(CATALOG,obs,self.ledger,"run-002","b"*40)
        self.assertEqual(two["previous_entry_sha256"],one["entry_sha256"])

    def test_observations_require_evidence_and_known_cases(self):
        one = next(iter(self.cases))
        with self.assertRaisesRegex(ValueError,"evidence"):
            er.validate_observations({"schema_version":1,"cases":[
                {"case_id":one,"observed_action":"BLOCK"}]},self.cases)
        with self.assertRaisesRegex(ValueError,"Unknown"):
            er.validate_observations({"schema_version":1,"cases":[
                {"case_id":"FAKE-999","observed_action":"FLAG","evidence_reference":"x"}]},self.cases)

    def test_missed_control_and_comparison(self):
        one = next(iter(self.cases))
        obs1 = self.observations([], "baseline")
        obs2 = self.observations([{"case_id":one,"observed_action":"PASS",
                                   "evidence_reference":"observed-fixture-output.txt"}],"new")
        er.record(CATALOG,obs1,self.ledger,"baseline","a"*40)
        second = er.record(CATALOG,obs2,self.ledger,"candidate","b"*40)
        self.assertEqual(second["result"]["mismatches"],1)
        self.assertEqual(second["result"]["matches_expected"],0)
        self.assertFalse(second["result"]["independent_reviewer_authenticated"])
        self.assertEqual(len(er.compare(self.ledger,"baseline","candidate")["changes"]),1)

    def test_altered_ledger_is_rejected(self):
        obs = self.observations([], "empty")
        er.record(CATALOG,obs,self.ledger,"run-001","a"*40)
        self.ledger.write_text(self.ledger.read_text(encoding="utf-8").replace("run-001","run-999"),encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"integrity"):
            er.read_ledger(self.ledger)

    def test_changed_catalog_is_not_comparable(self):
        obs = self.observations([], "empty")
        er.record(CATALOG,obs,self.ledger,"baseline","a"*40)
        newcat = json.loads(CATALOG.read_text(encoding="utf-8"))
        newcat["cases"][0]["scenario"] += " revised"
        altered = self.temp/"new_catalog.json"
        altered.write_text(json.dumps(newcat),encoding="utf-8")
        er.record(altered,obs,self.ledger,"candidate","b"*40)
        with self.assertRaisesRegex(ValueError,"changed case catalogs"):
            er.compare(self.ledger,"baseline","candidate")

if __name__ == "__main__":
    unittest.main()
