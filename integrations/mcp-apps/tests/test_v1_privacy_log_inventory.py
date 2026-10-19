"""Read-only runtime privacy inventory must never ingest sensitive logs or write state."""
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "v1-privacy-log-inventory.sh"

class PrivacyLogInventoryContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SCRIPT.read_text(encoding="utf-8")

    def test_bash_syntax_and_explicit_audit_mode(self):
        result = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"--audit"', self.source)
        self.assertIn("ROOT_REQUIRED_FOR_COMPLETE_READ", self.source)

    def test_no_log_events_secrets_or_runtime_changes(self):
        s = self.source
        for forbidden in (
            "journalctl -u", "journalctl --unit", "/proc/", "printenv",
            "systemctl cat", "systemctl restart", "systemctl reload",
            "systemctl daemon-reload", "truncate -s", "sed -i", "tee ",
            "curl ", "wget ", "git push", "rm -", "auth0.com/api",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, s)
        for required in (
            "V1_JOURNALD_MaxRetentionSec", "V1_NGINX_SITE_ACCESS_LOG",
            "V1_AUTH0_LOG_RETENTION=NOT_VERIFIED_CHECK_TENANT_PLAN",
            "V1_AUTH0_LOG_STREAMS=NOT_VERIFIED_CHECK_AUTH0_DASHBOARD",
            "V1_PRIVACY_INVENTORY_END=PASS_READ_ONLY",
        ):
            if required == "V1_JOURNALD_MaxRetentionSec":
                self.assertRegex(s, r"for key in Storage MaxRetentionSec")
            else:
                self.assertIn(required, s)

    def test_output_exposes_only_allowlisted_fields(self):
        s = self.source
        self.assertIn("value=REDACTED", s)
        self.assertIn("REQUIRES_FULL_CONFIG_REVIEW", s)
        self.assertNotIn("Environment --value", s)
        self.assertNotIn("journalctl --since", s)

if __name__ == "__main__":
    unittest.main()
