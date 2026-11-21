"""Offline tests of local CodeQL SARIF screening (synthetic only)."""
import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from audit_codeql_sarif import inspect


class SARIFContractTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def store(self,results,score="9.0"):
        obj={"version":"2.1.0","runs":[{"tool":{"driver":{"name":"CodeQL",
             "rules":[{"id":"js/security","properties":{"security-severity":score}}]}},
             "results":results}]}
        (self.root/"javascript.sarif").write_text(json.dumps(obj),encoding="utf-8")

    def test_fails_when_missing_sarif(self):
        with self.assertRaisesRegex(ValueError,"MISSING"):
            inspect(self.root)

    def test_empty_valid_codeql_is_allowed(self):
        self.store([])
        self.assertEqual(inspect(self.root)["results"],0)

    def test_high_security_alert_blocks(self):
        self.store([{"ruleId":"js/security","level":"warning"}])
        self.assertEqual(inspect(self.root)["high"],1)

    def test_lower_severity_requires_review_without_block(self):
        self.store([{"ruleId":"js/security","level":"warning"}],score="6.9")
        p=inspect(self.root)
        self.assertEqual(p["high"],0)
        self.assertEqual(p["other_requires_manual_review"],1)

    def test_extension_rule_high_is_not_silently_discarded(self):
        """Actual CodeQL action SARIF has driver.rules=[] and extension rules."""
        alert = {"ruleId": "py/overly-permissive-file", "level": "warning",
                 "rule": {"id": "py/overly-permissive-file", "index": 0,
                          "toolComponent": {"index": 1}},
                 "locations": [{"physicalLocation": {
                     "artifactLocation": {"uri": "tests/test_drive_f7_anchor.py"},
                     "region": {"startLine": 203}}}]}
        obj = {"version": "2.1.0", "runs": [{"tool": {
            "driver": {"name": "CodeQL", "rules": []},
            "extensions": [
                {"name": "codeql-action/pr-diff-range", "rules": []},
                {"name": "codeql/python-queries", "rules": [
                    {"id": "py/overly-permissive-file",
                     "properties": {"security-severity": "7.8"}}]}]},
            "results": [alert]}]}
        (self.root / "python.sarif").write_text(json.dumps(obj), encoding="utf-8")
        actual = inspect(self.root)
        self.assertEqual(actual["high"], 1)
        self.assertEqual(actual["blocking_high"], 1)
        acknowledged = inspect(
            self.root, acknowledge_synthetic_drive_f7_fixtures=True)
        self.assertEqual(acknowledged["high"], 1)
        self.assertEqual(acknowledged["acknowledged_synthetic_test_high"], 1)
        self.assertEqual(acknowledged["blocking_high"], 0)

        alert["locations"][0]["physicalLocation"]["region"]["startLine"] = 204
        (self.root / "python.sarif").write_text(json.dumps(obj), encoding="utf-8")
        moved = inspect(self.root, acknowledge_synthetic_drive_f7_fixtures=True)
        self.assertEqual(moved["blocking_high"], 1)
        self.assertEqual(moved["acknowledged_synthetic_test_high"], 0)

    def test_missing_rule_metadata_fails_closed(self):
        self.store([{"ruleId": "js/new-unknown-rule", "level": "warning"}])
        with self.assertRaisesRegex(ValueError, "METADATA_MISSING"):
            inspect(self.root)

    def test_other_sarif_tool_rejected(self):
        self.store([])
        p=self.root/"javascript.sarif"
        obj=json.loads(p.read_text())
        obj["runs"][0]["tool"]["driver"]["name"]="UntrustedTool"
        p.write_text(json.dumps(obj))
        with self.assertRaisesRegex(ValueError,"UNEXPECTED_TOOL"):
            inspect(self.root)


if __name__ == "__main__":
    unittest.main()
