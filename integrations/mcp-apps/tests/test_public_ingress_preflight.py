"""Synthetic, offline tests for the read-only production proxy preflight."""
from __future__ import annotations

import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "integrations" / "mcp-apps" / "scripts"))
from public_ingress_preflight import inspect  # noqa: E402

TEMPLATE_PATH = ROOT / "integrations" / "mcp-apps" / "deploy" / "nginx-auth0-production.conf.template"


class IngressSourceGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = TEMPLATE_PATH.read_text(encoding="utf-8")

    def test_safe_source_template_is_not_production_acceptance(self):
        result = inspect(self.template)
        self.assertEqual(result["status"], "SOURCE_TEMPLATE_PASS")
        self.assertEqual(result["live_tls"], "NOT_TESTED")
        self.assertEqual(result["oauth_pkce"], "NOT_TESTED")
        self.assertEqual(result["host_csp"], "NOT_OBSERVED")

    def rendered(self, cert: str, key: str):
        return (self.template
                .replace("YOUR_MCP_HOST.example", "mcp.allflux.com.br")
                .replace("/REPLACE_WITH_CERTIFICATE_CHAIN.pem", cert)
                .replace("/REPLACE_WITH_PRIVATE_KEY.pem", key))

    def test_operator_rendered_config_needs_key_permissions(self):
        with tempfile.TemporaryDirectory() as tmp:
            cert, key = Path(tmp) / "fullchain.pem", Path(tmp) / "privkey.pem"
            cert.write_text("synthetic cert path fixture", encoding="utf-8")
            key.write_text("synthetic key path fixture", encoding="utf-8")
            key.chmod(0o600)
            rendered = self.rendered(str(cert), str(key))
            result = inspect(rendered, host="mcp.allflux.com.br",
                             require_cert_files=True)
            self.assertEqual(result["status"], "RENDERED_SOURCE_CHECK_PASS")
            self.assertEqual(result["live_tls"], "NOT_TESTED")
            key.chmod(0o644)
            with self.assertRaisesRegex(ValueError, "PROXY_TLS_KEY_TOO_PERMISSIVE"):
                inspect(rendered, host="mcp.allflux.com.br",
                        require_cert_files=True)
            # Keep the synthetic private-key marker out of artifacts.
            key.chmod(0o600)

    def test_malformed_or_unscoped_proxy_fails_closed(self):
        base = self.template
        broken = (
            (base.replace("location / { return 404; }",
                          "location / { proxy_pass http://127.0.0.1:8085; }"),
             "PROXY_UNEXPECTED_UPSTREAM"),
            (base.replace("location = /mcp", "location /mcp"),
             "PROXY_LOCATION_MATCH_NOT_EXACT"),
            (base.replace("proxy_pass http://127.0.0.1:8085;",
                          "proxy_pass http://0.0.0.0:8085;", 1),
             "PROXY_TARGET_INVALID"),
            (base.replace("location = /.well-known/oauth-protected-resource/mcp",
                          "location = /healthz"),
             "PROXY_LOCATION_ALLOWLIST_INVALID"),
            (base.replace("ssl_protocols TLSv1.2 TLSv1.3;",
                          "ssl_protocols TLSv1.0 TLSv1.1;"),
             "PROXY_SECURITY_BOUNDARY_MISSING"),
            (base.replace("access_log off;", "access_log on;"),
             "PROXY_SECURITY_BOUNDARY_MISSING"),
            (base.replace("server_name YOUR_MCP_HOST.example;",
                          "server_name some-other.example;"),
             "PROXY_TEMPLATE_PLACEHOLDER_DRIFT"),
        )
        for sample, expected in broken:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(ValueError, expected):
                    inspect(sample)

    def test_missing_certificate_or_unapproved_host_denied(self):
        sample = self.rendered("/tmp/nonexistent-cert.pem", "/tmp/nonexistent-key.pem")
        with self.assertRaisesRegex(ValueError, "PROXY_TLS_FILE_MISSING"):
            inspect(sample, host="mcp.allflux.com.br", require_cert_files=True)
        with self.assertRaisesRegex(ValueError, "PROXY_RENDERED_TLS_INCOMPLETE"):
            inspect(self.template, host="mcp.allflux.com.br")
        with self.assertRaisesRegex(ValueError, "PROXY_EXPECTED_HOST_INVALID"):
            inspect(sample, host="synthetic.example")


if __name__ == "__main__":
    unittest.main()
