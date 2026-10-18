"""Offline packaging regression for Meu Artigo ChatGPT private/public candidates."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "integrations" / "mcp-apps" / "scripts"))
sys.path.insert(0, str(ROOT / "scripts"))
from build_chatgpt_plugin_candidate import build_candidate, inspect_candidate
from version_info import read_version

TEST_PUBLIC_MCP_URL = 'https://mcp.allflux.com.br/mcp'  # not verified live


class ChatGPTPluginCandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.version = read_version(ROOT)

    def path(self, channel):
        return self.root / ("MeuArtigoChatGPT-" + channel + "-v" + self.version + ".zip")

    def test_public_bundle_contains_remote_mcp_and_not_published(self):
        output = self.path("public")
        result = build_candidate(ROOT, output, "public", mcp_url=TEST_PUBLIC_MCP_URL)
        self.assertEqual(result["status"], "SOURCE_PACKAGE_CHECK_PASS")
        self.assertEqual(result["public_directory_approval"], "NOT_ASSERTED")
        self.assertIs(result["registered_app_live_verified"], False)
        self.assertIs(result["installation_authorized"], False)
        with ZipFile(output) as z:
            names = z.namelist()
            self.assertIn("plugin.json", names)
            self.assertIn("skills/meu-artigo/SKILL.md", names)
            self.assertIn("skills/meu-artigo/BUNDLE_MANIFEST.json", names)
            self.assertNotIn(".app.json", names)
            self.assertIn("mcp.json", names)
            remote = json.loads(z.read("mcp.json"))["mcpServers"]["meu-artigo"]
            self.assertEqual(remote["type"], "streamable-http")
            self.assertEqual(remote["url"], TEST_PUBLIC_MCP_URL)
            self.assertEqual(remote["extensions"]["com.openai"]["auth"],
                             {"type": "oauth", "baseScopes": ["mcp:read"]})
            manifest = json.loads(z.read("plugin.json"))
            self.assertEqual(manifest["version"], self.version)
            ui = manifest["extensions"]["com.openai"]["interface"]
            self.assertLessEqual(len(ui["shortDescription"]), 30)
            self.assertLessEqual(len(ui["defaultPrompt"]), 3)
            self.assertTrue(all(len(prompt) <= 128 for prompt in ui["defaultPrompt"]))
            self.assertNotIn("apps", manifest["extensions"]["com.openai"])
        self.assertEqual(inspect_candidate(output, ROOT, "public")["status"],
                         "SOURCE_PACKAGE_CHECK_PASS")

    def test_public_rejects_unconfigured_or_unsafe_url(self):
        output = self.path("public")
        with self.assertRaisesRegex(ValueError, "PUBLIC_MCP_URL_REQUIRED"):
            build_candidate(ROOT, output, "public")
        for bad in (
            "http://mcp.allflux.com.br/mcp", "https://localhost/mcp",
            "https://synthetic.invalid/mcp", "https://mcp.allflux.com.br/other",
            "https://someone:secret@mcp.allflux.com.br/mcp",
            "https://mcp.allflux.com.br/mcp?secret=x",
        ):
            with self.subTest(url=bad):
                with self.assertRaisesRegex(ValueError, "PUBLIC_MCP_URL_INVALID"):
                    build_candidate(ROOT, output, "public", mcp_url=bad)
        self.assertFalse(output.exists())

    def test_private_rejects_public_mcp_url(self):
        with self.assertRaisesRegex(ValueError, "PRIVATE_MCP_URL_UNEXPECTED"):
            build_candidate(ROOT, self.path("private"), "private",
                            "asdk_app_FICTIONAL_STRUCTURAL_TEST",
                            mcp_url=TEST_PUBLIC_MCP_URL)

    def test_public_duplicate_manifest_is_rejected(self):
        output = self.path("public")
        build_candidate(ROOT, output, "public", mcp_url=TEST_PUBLIC_MCP_URL)
        with ZipFile(output, "a") as z:
            z.writestr("mcp.json", '{"mcpServers": {}}')
        with self.assertRaisesRegex(ValueError, "ZIP_DUPLICATE_OR_OVERSIZED"):
            inspect_candidate(output, ROOT, "public")

    def test_private_requires_explicit_registered_app_id(self):
        with self.assertRaisesRegex(ValueError, "PRIVATE_REQUIRES"):
            build_candidate(ROOT, self.path("private"), "private")
        self.assertFalse(self.path("private").exists())

    def test_synthetic_e05_can_never_be_packaged_as_production(self):
        with self.assertRaisesRegex(ValueError, "PRIVATE_REQUIRES"):
            build_candidate(ROOT, self.path("private"), "private",
                            "asdk_app_6ad412c004808191a27b70a8aceb8ac7")

    def test_mcp_pilot_is_never_a_production_app(self):
        with self.assertRaisesRegex(ValueError, "PRIVATE_REQUIRES"):
            build_candidate(ROOT, self.path("private"), "private",
                            "asdk_app_6ad3cf00e45c81918892e94fdcbf4a2e")
        self.assertFalse(self.path("private").exists())

    def test_no_public_app_reference_even_when_supplied(self):
        with self.assertRaisesRegex(ValueError, "PUBLIC_APP_REFERENCE_FORBIDDEN"):
            build_candidate(ROOT, self.path("public"), "public",
                            "asdk_app_ExampleProductionOnly")

    def test_private_structural_candidate_remains_nonproduction(self):
        # Fake ID verifies the packaging shape only; it is not a real server
        # and must never be installed or represented as a live validation.
        result = build_candidate(ROOT, self.path("private"), "private",
                                 "asdk_app_FICTIONAL_STRUCTURAL_TEST")
        self.assertEqual(result["mcp_live_acceptance"], "NOT_ASSERTED")
        self.assertEqual(result["scientific_validation"], "NOT_ASSERTED")
        self.assertIs(result["registered_app_live_verified"], False)
        self.assertIs(result["installation_authorized"], False)
        with ZipFile(self.path("private")) as z:
            manifest = json.loads(z.read("plugin.json"))
            self.assertEqual(manifest["extensions"]["com.openai"]["apps"],
                             "./.app.json")
            app = json.loads(z.read(".app.json"))
            self.assertEqual(app["apps"]["meu-artigo"]["id"],
                             "asdk_app_FICTIONAL_STRUCTURAL_TEST")

    def test_mismatched_source_version_blocks_release(self):
        output = self.path("public")
        build_candidate(ROOT, output, "public", mcp_url=TEST_PUBLIC_MCP_URL)
        with tempfile.TemporaryDirectory() as temporary:
            other = Path(temporary)
            (other / "VERSION").write_text("0.9.0-beta.999\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "PLUGIN_SKILL_VERSION_DRIFT"):
                inspect_candidate(output, other, "public")

    def test_public_archive_cannot_silently_embed_app(self):
        output = self.path("public")
        build_candidate(ROOT, output, "public", mcp_url=TEST_PUBLIC_MCP_URL)
        with ZipFile(output, "a") as z:
            z.writestr(".app.json", '{"apps":{"unknown":{"id":"asdk_app_fake"}}}')
        with self.assertRaisesRegex(ValueError, "PUBLIC_MCP_APP_REFERENCE_FORBIDDEN"):
            inspect_candidate(output, ROOT, "public")


if __name__ == "__main__":
    unittest.main()
