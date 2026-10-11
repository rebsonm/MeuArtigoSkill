"""Public release recommendation is distinct from the main development version."""
from pathlib import Path
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]
OFFICIAL = "0.9.0-beta.1"
ZIP = "https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.1/MeuArtigoSkill-v0.9.0-beta.1.zip"
GUIDES = ("README.md", "docs/INSTALLATION.md", "docs/COMECE-AQUI.md", "docs/CHATGPT.md", "docs/IMPLANTACAO-BETA.md")

class OfficialRecommendationTests(unittest.TestCase):
    def test_explicit_official_release_and_all_installation_guides(self):
        self.assertEqual((ROOT / "OFFICIAL_SKILL_RELEASE").read_text().strip(), OFFICIAL)
        for filename in GUIDES:
            guide = (ROOT / filename).read_text(encoding="utf-8")
            self.assertIn(ZIP, guide, filename)
            self.assertNotIn("MeuArtigoSkill-v0.9.0-beta.2.zip", guide, filename)
            self.assertNotRegex(guide, re.compile(r"\b(?:mcp|plugin|visual-app)\b",re.I), filename)

    def test_unreleased_main_source_not_misrepresented_as_official(self):
        dev_version = (ROOT / "VERSION").read_text().strip()
        self.assertEqual(dev_version, "0.9.0-beta.4")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"**Current version:** `{dev_version}`", readme)
        self.assertIn("Official recommended public Skill", readme)
        self.assertIn("not the recommended public Skill", readme)

    def test_historical_notes_kept_for_provenance(self):
        for v in ("0.9.0-beta.1", "0.9.0-beta.2", "0.9.0-beta.4"):
            self.assertTrue((ROOT / "docs" / f"NOTAS-DA-VERSAO-{v}.md").exists())

if __name__ == '__main__':
    unittest.main()
