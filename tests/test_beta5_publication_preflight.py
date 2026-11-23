"""Keep historical beta release evidence alongside published plugin RC.4."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from check_release_metadata import audit_published_source_metadata
from version_info import read_version

class Beta5PublicationHistoryTests(unittest.TestCase):
    def setUp(self):
        self.version=read_version(ROOT)
        self.notes=(ROOT/"docs/NOTAS-DA-VERSAO-0.9.0-beta.6.md").read_text(encoding="utf-8")
        self.readme=(ROOT/"README.md").read_text(encoding="utf-8")

    def test_historical_beta_and_current_candidate_distinction(self):
        self.assertEqual(self.version,"1.0.0-rc.4")
        self.assertEqual(audit_published_source_metadata(ROOT),[])
        self.assertIn("experimental",self.readme.lower())
        self.assertIn("pre-release",self.notes.lower())
        self.assertIn("not a stable",self.notes.lower())
        self.assertIn("No independent scientific validation",self.notes)
        self.assertIn("seven researcher decision gates",self.notes)

    def test_history_and_manual_publisher_unchanged(self):
        self.assertEqual((ROOT/"OFFICIAL_SKILL_RELEASE").read_text().strip(),"1.0.0-rc.3")
        guide=(ROOT/"docs/TESTE-BETA-PESQUISADORES.md").read_text(encoding="utf-8")
        issue=(ROOT/".github/ISSUE_TEMPLATE/relato-beta.md").read_text(encoding="utf-8")
        self.assertIn("v1.0.0-rc.1",guide)
        self.assertIn("saved project",guide)
        self.assertIn("SECURITY.md",issue)
        self.assertIn("Expected result",issue)
        self.assertIn("Actual observed result",issue)
        self.assertIn("v0.9.0-beta.6",self.readme)
        workflow=(ROOT/".github/workflows/publish-beta.yml").read_text(encoding="utf-8")
        for fragment in ("workflow_dispatch:","acknowledgement",'"$ACK" != "publish-beta"',
                         "gh release create","--prerelease","--latest=false"):
            self.assertIn(fragment,workflow)
        self.assertNotIn("pull_request:",workflow)

if __name__=="__main__":
    unittest.main()
