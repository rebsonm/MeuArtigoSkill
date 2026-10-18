"""Read-only, source-only assertions for the isolated v1 candidate VPS bootstrap."""
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = (ROOT / "integrations" / "mcp-apps" / "scripts"
          / "stage-v1-isolated.sh")


class StageV1IsolatedContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.code = SCRIPT.read_text(encoding="utf-8")

    def test_bash_syntax(self):
        result = subprocess.run(["bash", "-n", str(SCRIPT)], check=False,
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, "Staging shell syntax invalid")

    def test_dry_run_preflight_and_explicit_apply(self):
        for required in (
            '"--check"', '"--apply"', 'SHA_REQUIRED',
            'EXPECTED_OLD="cdd3affb902028753b9c66b83c2ef5e37f9e1700"',
            'BRANCH="release/prepare-public-mcp-20261018"',
            'STAGE="/opt/meu-artigo-v1-acceptance"',
            'PORT=18087',
            'OLD_SHA_DRIFT', 'STAGE_ALREADY_EXISTS', 'STAGING_PORT_BUSY',
            'E05_NOT_ACTIVE', 'OLD_SERVICE_NOT_ACTIVE',
            'BRANCH_MOVED_STOP', 'GIT_ANONYMOUS_FETCH_FAILED',
            'V1_STAGE_READONLY_PASS', 'V1_STAGE_ISOLATED_COMPLETE=YES',
        ):
            with self.subTest(required=required):
                self.assertIn(required, self.code)

    def test_no_production_mutations_or_auto_exposure(self):
        for bad in (
            "git reset", "git pull", "rm -rf", "chmod -R", "chown -R",
            "systemctl stop", "systemctl restart", "systemctl enable",
            "nginx -s reload", "nginx -t", "ufw allow", "iptables",
            "MEU_ARTIGO_MCP_MULTIUSER=YES", "proxy_pass",
            "MEU_ARTIGO_AUTH_MODE=auth0", "CONTROL_PLANE_API_KEY",
            "MEU_ARTIGO_GOOGLE_CLIENT_SECRET",
        ):
            with self.subTest(bad=bad):
                self.assertNotIn(bad, self.code)
        self.assertNotRegex(self.code, r"\b(curl|wget)\b[^\n]*\|\s*(bash|sh)")
        self.assertIn("runuser -u", self.code)
        self.assertIn("GIT_TERMINAL_PROMPT=0", self.code)
        self.assertIn("npm ci --ignore-scripts", self.code)
        self.assertIn("npm audit --omit=dev --audit-level=high", self.code)

    def test_probe_denies_unauthorized_and_cleans_up(self):
        for item in (
            "MEU_ARTIGO_BIND_HOST=127.0.0.1",
            "MEU_ARTIGO_MCP_PORT=",
            "MEU_ARTIGO_AUTH_MODE=bearer",
            "openssl rand -hex 32",
            "V1_TEMPORARY_LOCAL_READINESS=200",
            "V1_TEMPORARY_LOCAL_MCP_NO_TOKEN=401",
            "V1_AUTH0_REAL_LOGIN=NOT_TESTED",
            "V1_EXTERNAL_MCP=NOT_ACTIVATED",
            "trap cleanup EXIT",
            "trap - EXIT",
            "PROBE_PORT_NOT_RELEASED",
        ):
            self.assertIn(item, self.code)
        self.assertNotRegex(self.code, r"(?m)^\s*echo\s+.*token")
        self.assertNotRegex(self.code, r"(?m)^\s*printf\s+.*token")


if __name__ == "__main__":
    unittest.main()
