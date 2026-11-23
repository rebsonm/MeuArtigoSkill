"""Keep immutable published RC.1 downloads separate from RC.3 source.

These offline checks cannot prove an external release or active installation.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://github.com/rebsonm/MeuArtigoSkill/releases/download"
GUIDES = ("README.md", "docs/INSTALLATION.md", "docs/COMECE-AQUI.md",
          "docs/CHATGPT.md", "docs/IMPLANTACAO-BETA.md")


class OfficialRecommendationTests(unittest.TestCase):
    def test_published_rc1_pointer_and_download_links(self):
        recommended = (ROOT / "OFFICIAL_SKILL_RELEASE").read_text().strip()
        self.assertEqual(recommended, "1.0.0-rc.1")
        self.assertEqual((ROOT / "VERSION").read_text().strip(), "1.0.0-rc.3")
        url = f"{BASE_URL}/v{recommended}/MeuArtigoSkill-v{recommended}.zip"
        for filename in GUIDES:
            with self.subTest(filename=filename):
                self.assertIn(url, (ROOT / filename).read_text(encoding="utf-8"))
        self.assertIn("Recommended published experimental prerelease",
                      (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_source_is_candidate_not_released_or_host_certified(self):
        version = (ROOT / "VERSION").read_text().strip()
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"**Current version:** `{version}`", readme)
        self.assertIn("unpublished release candidate source", readme)
        self.assertIn("published GitHub experimental prerelease", readme)
        self.assertIn("no stable v1.0.0", readme)
        self.assertIn("optional XLSX", readme)
        self.assertIn("v0.9.0-beta.6", readme)
        self.assertNotIn("/releases/tag/v" + version, readme)

    def test_historical_releases_remain_available_as_history(self):
        for version in ("0.9.0-beta.1", "0.9.0-beta.2", "0.9.0-beta.4",
                        "0.9.0-beta.5", "0.9.0-beta.6", "1.0.0-rc.1"):
            self.assertTrue((ROOT / "docs" / f"NOTAS-DA-VERSAO-{version}.md").exists())


if __name__ == "__main__":
    unittest.main()
