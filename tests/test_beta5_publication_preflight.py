"""Preserve historical beta.5 notes; verify beta.6 release-preparation safeguards."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from check_release_metadata import audit_release_metadata
from version_info import read_version

class Beta5PublicationTests(unittest.TestCase):
    def setUp(self):
        self.version=read_version(ROOT)
        self.notes=(ROOT/"docs"/"NOTAS-DA-VERSAO-0.9.0-beta.6.md").read_text(encoding="utf-8")
        self.readme=(ROOT/"README.md").read_text(encoding="utf-8")

    def test_consistent_release_metadata(self):
        self.assertEqual(self.version,"0.9.0-beta.6")
        self.assertEqual(audit_release_metadata(ROOT,expected_date="2026-10-15"),[])
        self.assertIn("confirmed published",self.readme.lower())
        self.assertIn("pre-release",self.notes.lower())
        self.assertIn("not a stable",self.notes.lower())

    def test_release_is_experimental(self):
        self.assertIn("Every 0.9.0-beta release is experimental",self.readme)
        self.assertIn("No independent scientific validation",self.notes)
        self.assertIn("seven researcher decision gates",self.notes)
        self.assertNotIn("v1.0.0 has been published",self.readme)

    def test_user_guides_and_recommendation(self):
        self.assertEqual((ROOT/"OFFICIAL_SKILL_RELEASE").read_text(encoding="utf-8").strip(),"0.9.0-beta.6")
        guide=(ROOT/"docs/TESTE-BETA-PESQUISADORES.md").read_text(encoding="utf-8")
        issue=(ROOT/".github/ISSUE_TEMPLATE/relato-beta.md").read_text(encoding="utf-8")
        self.assertIn("v0.9.0-beta.6",guide)
        self.assertIn("saved project",guide)
        self.assertIn("SECURITY.md",issue)
        self.assertIn("Expected result",issue)
        self.assertIn("Actual observed result",issue)
        self.assertIn("beta.1 and beta.2",self.readme)

    def test_manual_publishing_enforces_explicit_confirmation(self):
        workflow=(ROOT/".github/workflows/publish-beta.yml").read_text(encoding="utf-8")
        for fragment in ("workflow_dispatch:","acknowledgement",'"$ACK" != "publish-beta"', "gh release create","--prerelease","--latest=false"):
            self.assertIn(fragment,workflow)
        self.assertNotIn("pull_request:",workflow)

if __name__=="__main__":
    unittest.main()
