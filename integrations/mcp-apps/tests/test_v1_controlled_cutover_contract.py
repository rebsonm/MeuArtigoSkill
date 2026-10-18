"""Offline safety contract for maintainer-authorized, deny-all v1 cutover."""
from pathlib import Path
import subprocess
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "v1-controlled-cutover.sh"


class CutoverContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text("utf-8")

    def test_shell_compiles(self):
        result = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True,
                                text=True, check=False, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_only_explicit_operator_and_pinned_source(self):
        for token in (
            "EXPLICIT_ROOT_APPLY_REQUIRED", 'SOURCE_SHA',
            'SHA="02e03674e8e897d7f5e3f6769f7902062695b8dc"',
            "V1_ALREADY_EXISTS", "V1_USER_ALREADY_EXISTS", "LEGACY_SHA_CHANGED",
            'runuser -u "$USER_NAME" -- env -i', "GIT_TERMINAL_PROMPT=0",
            "npm ci --ignore-scripts", "npm run test:private-pilot",
            "V1_PRIVATE_CUTOVER=PASS", "V1_PLUGIN_AND_MAIN=UNCHANGED",
        ):
            if token == "SOURCE_SHA":  # The fixed field is called SHA.
                continue
            with self.subTest(token=token):
                self.assertIn(token, self.script)

    def test_pilot_restriction_and_no_public_auth_bypass(self):
        for token in (
            "MEU_ARTIGO_AUTH_MODE=auth0",
            "MEU_ARTIGO_MCP_MULTIUSER=YES",
            "MEU_ARTIGO_MCP_PRIVATE_PILOT=YES",
            "MEU_ARTIGO_MCP_PILOT_SUBS=DENY_ALL",
            "LOCAL_ANONYMOUS_ALLOWED",
            "PUBLIC_ACCEPTANCE_FAILED",
            "V1_PUBLIC_UNAUTH_MCP=401",
            "V1_PUBLIC_READYZ=404",
            "V1_REAL_LOGIN=NOT_TESTED",
        ):
            self.assertIn(token, self.script)
        for forbidden in (
            "MEU_ARTIGO_PILOT_SUB=", "MEU_ARTIGO_GOOGLE_TOKEN_DIR",
            "MEU_ARTIGO_GOOGLE_CLIENT_SECRET", "Auth0ClientSecret",
            "git reset --hard", "git pull", "rm -rf", "chmod -R",
            "systemctl restart nginx", "do-release-upgrade", "curl -k",
            "mcp.allflux.com.br/mcp?token",
        ):
            self.assertNotIn(forbidden, self.script)

    def test_existing_nginx_and_old_e05_preserved_with_rollback(self):
        for token in (
            'SITE_LINK="/etc/nginx/sites-enabled/meu-artigo-mcp.conf"',
            "ACME_NOT_PRESENT", "DEFAULT_DENY_MISSING",
            "proxy_pass http://127.0.0.1:18086;",
            "proxy_pass http://127.0.0.1:18087;",
            'cp -a "$SITE" "$BACKUP"',
            'cp -a "$BACKUP" "$SITE"',
            "trap rollback EXIT",
            "systemctl reload nginx", "nginx -t",
            "meu-artigo-e05-tunnel.service", "meu-artigo-mcp.service",
            "V1_AUTOMATIC_ROLLBACK_END",
        ):
            self.assertIn(token, self.script)


if __name__ == "__main__":
    unittest.main()
