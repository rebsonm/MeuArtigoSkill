"""Synthetic tests for full-repository credential scanner, never real secrets."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_repository_secrets import scan_entry


class SecretAuditTests(unittest.TestCase):
    def test_repository_patterns_detect_synthetic_github_credential(self):
        fixture = "ghp_" + "F" * 36
        self.assertIn("GitHub credential", scan_entry("app.js", fixture.encode()))

    def test_repository_patterns_detect_synthetic_google_oauth_secret(self):
        fixture = "GOCSPX-" + "F" * 25
        self.assertIn("Google OAuth client secret", scan_entry("config.py", fixture.encode()))

    def test_repo_blocks_local_env_and_private_key_names(self):
        for path in ["integrations/mcp-apps/.env", ".env.production", "x/id_rsa", "x/private.pem"]:
            self.assertIn("credential-like filename", scan_entry(path, b"secret"))

    def test_safe_examples_and_public_identifiers_are_not_secrets(self):
        example = b"MEU_ARTIGO_AUTH_ISSUER=https://sample.us.auth0.com/\n"
        self.assertEqual(scan_entry(".env.example", example), [])
        self.assertEqual(scan_entry("auth0.mjs", b"https://mcp.allflux.com.br/mcp"), [])

    def test_no_secret_material_is_returned(self):
        fixture = "sk-" + "F" * 40
        findings = scan_entry("config.txt", fixture.encode())
        self.assertTrue(findings)
        self.assertNotIn(fixture, str(findings))


if __name__ == "__main__":
    unittest.main()
