"""Candidate source version and independent MCP metadata must agree.

No network, account changes, release or ZIP publication.
"""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "integrations" / "mcp-apps"


class DistributionVersionCoherence(unittest.TestCase):
    def test_source_release_metadata_matches_candidate(self):
        v = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(v, r"^\d+\.\d+\.\d+-beta\.\d+$")
        self.assertIn(f"**Current version:** `{v}`",
                      (ROOT / "README.md").read_text(encoding="utf-8"))
        cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        self.assertIn(f'version: "{v}"', cff)
        if "pending publication" in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"):
            self.assertNotIn("date-released:", cff.split("#", 1)[0])
        self.assertTrue((ROOT / "docs" / f"NOTAS-DA-VERSAO-{v}.md").is_file())
        self.assertIn(f"## {v} — pending publication",
                      (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))

    def test_mcp_package_lock_server_and_bridge_versions_match(self):
        pkg = json.loads((MCP / "package.json").read_text(encoding="utf-8"))
        lock = json.loads((MCP / "package-lock.json").read_text(encoding="utf-8"))
        v = pkg["version"]
        self.assertTrue(pkg["private"])
        self.assertEqual(lock["version"], v)
        self.assertEqual(lock["packages"][""]["version"], v)
        server = (MCP / "server.mjs").read_text(encoding="utf-8")
        bridge = (MCP / "src" / "bridge.ts").read_text(encoding="utf-8")
        self.assertIn(f'name:"Meu Artigo — Host-Side Research",version:"{v}"', server)
        self.assertIn(f'name:"Meu Artigo",version:"{v}"', bridge)

    def test_draft_cannot_claim_installed_or_published(self):
        doc = (MCP / "STAGE17-VERSION-CANDIDATE.md").read_text(encoding="utf-8")
        self.assertIn("**UNCHANGED**", doc)
        self.assertIn("authorizes no merge", doc)
        self.assertIn("source-only decision evidence", doc)


if __name__ == "__main__":
    unittest.main()
