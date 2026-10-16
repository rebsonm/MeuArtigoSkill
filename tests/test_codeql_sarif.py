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
