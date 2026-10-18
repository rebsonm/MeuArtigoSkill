"""Published beta recommendation is distinct from source VERSION and stable status."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://github.com/rebsonm/MeuArtigoSkill/releases/download"
GUIDES = ("README.md", "docs/INSTALLATION.md", "docs/COMECE-AQUI.md",
          "docs/CHATGPT.md", "docs/IMPLANTACAO-BETA.md")

class OfficialRecommendationTests(unittest.TestCase):
    def test_recommendation_points_to_a_real_existing_beta_and_guides_link_it(self):
        recommended = (ROOT / "OFFICIAL_SKILL_RELEASE").read_text().strip()
        self.assertRegex(recommended, r"^0\.9\.0-beta\.\d+$")
        url = f"{BASE_URL}/v{recommended}/MeuArtigoSkill-v{recommended}.zip"
        for filename in GUIDES:
            guide = (ROOT / filename).read_text(encoding="utf-8")
            self.assertIn(url, guide, filename)
        # A recommendation is version selection, not stable/scientific status.
        # GitHub's actual tag and assets were checked outside the offline CI.
        self.assertEqual(recommended, "0.9.0-beta.6")
        self.assertIn("Recommended published experimental beta", (ROOT / "README.md").read_text())

    def test_current_source_is_not_equated_with_a_published_tag(self):
        dev_version = (ROOT / "VERSION").read_text().strip()
        published=(ROOT/"OFFICIAL_SKILL_RELEASE").read_text().strip()
        self.assertEqual(published,"0.9.0-beta.6")
        self.assertGreaterEqual(int(dev_version.rsplit(".",1)[1]),
                                int(published.rsplit(".",1)[1]))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"**Current version:** `{dev_version}`", readme)
        self.assertIn("experimental", readme.lower())
        if dev_version!=published:
            self.assertIn("source candidate",readme.lower())
            self.assertIn("not published or installed",readme.lower())
            self.assertIn(f'version: "{dev_version}"',
                          (ROOT/"CITATION.cff").read_text(encoding="utf-8"))
            self.assertNotIn("date-released:",
                             (ROOT/"CITATION.cff").read_text(encoding="utf-8"))
        else:
            self.assertIn("published **experimental GitHub Pre-release**",readme)
        self.assertIn("confirmed published", readme)
        self.assertIn("GitHub's", readme)
        self.assertIn("stable v1.0.0", readme)

    def test_historical_releases_not_discarded(self):
        for version in ("0.9.0-beta.1", "0.9.0-beta.2", "0.9.0-beta.4", "0.9.0-beta.5", "0.9.0-beta.6"):
            self.assertTrue((ROOT / "docs" / f"NOTAS-DA-VERSAO-{version}.md").exists())


if __name__ == '__main__':
    unittest.main()
