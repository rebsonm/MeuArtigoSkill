"""Offline RC.4 one-plugin distribution invariants, not real-host certification."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import build_plugin_bundle as bundle


class RC4PluginOnlyTests(unittest.TestCase):
    def test_manifest_version_and_scientific_entrypoint(self):
        self.assertEqual(bundle.checked_manifest(ROOT)["name"],"meu-artigo")
        self.assertEqual(bundle.checked_manifest(ROOT)["version"],(ROOT/"VERSION").read_text().strip())
        self.assertTrue((ROOT/"SKILL.md").read_text().startswith("---\nname: meu-artigo\n"))
        self.assertEqual(bundle.PLUGIN_NAME,"meu-artigo")

    def test_logo_required_and_preflight_does_not_claim_acceptance(self):
        result=bundle.preflight(ROOT)
        self.assertEqual(result["distribution"],"CHATGPT_PLUGIN_ONLY")
        self.assertFalse(result["host_normal_chat_verified"])
        self.assertFalse(result["host_work_verified"])
        self.assertFalse(result["scientific_quality_validated"])
        if not (ROOT / bundle.LOGO_PATH).exists():
            self.assertFalse(result["logo_ready"])
            with self.assertRaisesRegex(ValueError,"RC4_LOGO_PENDING"):
                bundle.package(ROOT,ROOT/"dist"/"MeuArtigoPlugin-v1.0.0-rc.4.zip")

    def test_no_skill_release_from_rc4_ci(self):
        ci=(ROOT/".github/workflows/release-audit.yml").read_text()
        self.assertIn("steps.rc.outputs.plugin_only != 'true'",ci)
        self.assertIn("build_plugin_bundle.py",ci)
        self.assertIn("MeuArtigoPlugin-rc4-test-only-not-published",ci)
        self.assertNotIn("gh release create",ci)

    def test_citation_and_release_match_verified_zenodo_rc4(self):
        cff=(ROOT/"CITATION.cff").read_text()
        self.assertEqual((ROOT/"OFFICIAL_PLUGIN_RELEASE").read_text().strip(),"1.0.0-rc.5.1")
        if (ROOT/"VERSION").read_text().strip() == "1.0.0-rc.4":
            self.assertIn('doi: "10.5281/zenodo.24453186"',cff)
            self.assertIn('date-released: "2026-11-23"',cff)
        elif (ROOT/"VERSION").read_text().strip() == (ROOT/"OFFICIAL_PLUGIN_RELEASE").read_text().strip():
            self.assertIn('date-released: "2026-11-24"',cff)
            self.assertNotIn('doi: "10.5281/zenodo.24453186"',cff)
        else:
            self.assertNotIn('\ndoi:',cff)
            self.assertNotIn('\ndate-released:',cff)
        obj=json.loads((ROOT/"zenodo/metadata-draft.json").read_text())
        self.assertEqual(obj["version"],"1.0.0-rc.5.1")
        self.assertEqual(obj["historical_zenodo_rc4_version"]["doi"],"10.5281/zenodo.24453186")
        self.assertTrue(obj["github_release_published"])


if __name__=="__main__":
    unittest.main()
