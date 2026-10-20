"""Source-only guards for the non-public Auth0 multi-user shadow probe."""
from pathlib import Path
import re
import subprocess
import unittest

SOURCE = (Path(__file__).resolve().parents[1] / "scripts"
          / "v1-auth0-shadow-probe.sh")


class V1Auth0ShadowContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SOURCE.read_text(encoding="utf-8")

    def test_shell_syntax(self):
        r = subprocess.run(["bash", "-n", str(SOURCE)], text=True,
                           capture_output=True, timeout=5, check=False)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_exact_prior_accepted_staging_and_auth0_identity(self):
        for phrase in (
            'STAGE="/opt/meu-artigo-v1-acceptance"',
            'STAGE_SHA="07a92e6decc9c79d6a297522079c7389f6762ac2"',
            'ISSUER="https://dev-w6estudk22tzwdil.us.auth0.com/"',
            'RESOURCE="https://mcp.allflux.com.br/mcp"',
            'PORT=18087',
            'MEU_ARTIGO_AUTH_MODE=auth0',
            'MEU_ARTIGO_MCP_MULTIUSER=YES',
            'MEU_ARTIGO_BIND_HOST=127.0.0.1',
            'STAGING_SHA_DRIFT',
            'OLD_SHA_DRIFT',
            'STAGING_AUTH_CODE_MODIFIED',
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_stage_only_and_no_credential_use(self):
        for forbidden in (
            "git pull", "git reset", "systemctl stop", "systemctl start",
            "systemctl restart", "systemctl enable", "nginx -s reload",
            "nginx -t", "rm -rf", "chmod -R", "chown -R",
            "MEU_ARTIGO_MCP_BEARER=", "MEU_ARTIGO_PILOT_SUB=",
            "MEU_ARTIGO_GOOGLE_CLIENT_SECRET",
            "MEU_ARTIGO_GOOGLE_TOKEN_DIR",
            "AUTH0_CLIENT_SECRET",
            "MEU_ARTIGO_E05_SYNTHETIC_ONLY=YES",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, self.text)
        self.assertIn('runuser -u "$STAGE_USER" -- env -i', self.text)
        self.assertIn("trap cleanup EXIT", self.text)
        self.assertIn("trap - EXIT", self.text)
        self.assertIn("TEMPORARY_PORT_NOT_RELEASED", self.text)
        self.assertIn("V1_AUTH0_REAL_PKCE_LOGIN=NOT_TESTED", self.text)
        self.assertIn("V1_AUTH0_SHADOW_PUBLIC_ROUTE=NOT_CHANGED", self.text)

    def test_probes_are_actual_response_checks_not_mocked(self):
        for phrase in (
            "/.well-known/oauth-protected-resource",
            "/.well-known/oauth-protected-resource/mcp",
            '[[ "$denied" == 401 ]]',
            '[[ "$wrong" == 401 ]]',
            '[[ "$external" == 404 ]]',
            "m.authorization_servers",
            'm.scopes_supported?.includes("mcp:read")',
            "V1_AUTH0_SHADOW_COMPLETE=PASS",
        ):
            self.assertIn(phrase, self.text)


if __name__ == "__main__":
    unittest.main()
