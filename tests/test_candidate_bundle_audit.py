"""Unpublished candidate checksum, icon and tamper regressions (synthetic only)."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from version_info import read_version
from build_skill_bundle import package as skill_package
from build_plugin_bundle import build as plugin_build
from audit_candidate_bundles import validate_candidates, validate_zip


class CandidateAuditingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dist = Path(self.temp.name)
        self.v = read_version(ROOT)
        self.skill = self.dist / f"MeuArtigoSkill-v{self.v}.zip"
        self.plugin = self.dist / f"MeuArtigoPlugin-v{self.v}-candidate.zip"

    def candidates(self):
        skill_package(ROOT, self.skill)
        plugin_build(ROOT, self.plugin)
        return validate_candidates(ROOT, self.dist)

    def test_verified_candidate_does_not_claim_release_or_deployment(self):
        r = self.candidates()
        self.assertTrue(r["candidate_only"])
        self.assertFalse(r["public_release_created"])
        self.assertFalse(r["plugin_installed_or_updated"])
        self.assertFalse(r["mcp_app_deployed"])
        self.assertFalse(r["drive_sync_verified"])
        self.assertEqual(r["version"], self.v)
        self.assertEqual(r["skill"]["filename"], self.skill.name)
        self.assertEqual(r["plugin"]["filename"], self.plugin.name)

    def test_corrupted_candidate_is_rejected(self):
        self.candidates()
        b = bytearray(self.plugin.read_bytes())
        b[-23] ^= 0x11
        self.plugin.write_bytes(bytes(b))
        with self.assertRaises((ValueError, RuntimeError, __import__("zipfile").BadZipFile)):
            validate_candidates(ROOT, self.dist)

    def test_prohibited_private_member_is_rejected(self):
        test = self.dist / "unsafe.zip"
        with ZipFile(test, "w", compression=ZIP_DEFLATED) as z:
            z.writestr("skills/meu-artigo/secret/private/patient.pdf", b"fake")
        with self.assertRaisesRegex(ValueError, "prohibited path"):
            validate_zip(test)

    def test_plugin_identity_icon_and_absent_mcp_endpoint(self):
        self.candidates()
        with ZipFile(self.plugin) as z:
            m = json.loads(z.read("plugin.json"))
            o = json.loads(z.read(".codex-plugin/plugin.json"))
            self.assertEqual(m["version"], self.v)
            self.assertEqual(o["interface"]["logo"], "./assets/icon.svg")
            self.assertEqual(m["extensions"]["com.openai"]["interface"]["logo"], "./assets/icon.svg")
            self.assertNotIn("mcp.json", z.namelist())
            self.assertEqual(z.read("assets/icon.svg"), (ROOT/"assets/icon.svg").read_bytes())


if __name__ == "__main__":
    unittest.main()
