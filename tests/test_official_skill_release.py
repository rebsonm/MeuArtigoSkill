"""Historical standalone Skill assets must remain unchanged during RC.4 plugin migration."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
BASE="https://github.com/rebsonm/MeuArtigoSkill"
PUBLISHED="1.0.0-rc.3"

class HistoricalSkillReleaseTests(unittest.TestCase):
    def test_published_rc3_pointer_remains_historical(self):
        self.assertEqual((ROOT/"OFFICIAL_SKILL_RELEASE").read_text().strip(),PUBLISHED)
        self.assertEqual((ROOT/"VERSION").read_text().strip(),"1.0.0-rc.4")
        old_url=f"{BASE}/releases/download/v{PUBLISHED}/MeuArtigoSkill-v{PUBLISHED}.zip"
        for path in ("docs/INSTALLATION.md","docs/CURRENT-RELEASE.md"):
            self.assertIn(old_url,(ROOT/path).read_text(encoding="utf-8"))
        self.assertIn(f"{BASE}/releases/tag/v{PUBLISHED}",
                      (ROOT/"README.md").read_text(encoding="utf-8"))
        self.assertNotIn("MeuArtigoSkill-v1.0.0-rc.4.zip",
                         (ROOT/"README.md").read_text(encoding="utf-8"))

    def test_candidate_not_mislabeled_published(self):
        text=(ROOT/"README.md").read_text(encoding="utf-8").lower()
        self.assertIn("published experimental prerelease (plugin-only)",text)
        self.assertIn("not a stable release",text)
        self.assertIn("plugin",text)
        self.assertIn("v0.9.0-beta.6",text)

    def test_historical_release_notes_survive(self):
        for version in ("0.9.0-beta.1","0.9.0-beta.2","0.9.0-beta.4",
                        "0.9.0-beta.5","0.9.0-beta.6","1.0.0-rc.1","1.0.0-rc.3"):
            self.assertTrue((ROOT/"docs"/f"NOTAS-DA-VERSAO-{version}.md").is_file())

if __name__=="__main__":
    unittest.main()
