"""Offline checks that user-facing documents reference the *published* RC.1.

Historical beta release notes are intentionally not rewritten or removed.
These checks do not authenticate the live GitHub release or installed Skill.
"""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_release_metadata import audit_published_source_metadata

VERSION = "1.0.0-rc.1"
RELEASE_URL = "https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v" + VERSION
ZIP_URL = ("https://github.com/rebsonm/MeuArtigoSkill/releases/download/"
           "v" + VERSION + "/MeuArtigoSkill-v" + VERSION + ".zip")
ACTIVE = (
    "README.md", "SECURITY.md", "docs/INSTALLATION.md", "docs/CHATGPT.md",
    "docs/COMECE-AQUI.md", "docs/IMPLANTACAO-BETA.md",
    "docs/TESTE-BETA-PESQUISADORES.md", "docs/COMPATIBILIDADE-PLATAFORMAS.md",
    "wiki/Home.md", "wiki/FAQ.md", "wiki/Installation.md",
    "wiki/Status-and-Limitations.md", "docs/CURRENT-RELEASE.md",
)


class CurrentPublishedDocsTests(unittest.TestCase):
    def test_current_recommendation_and_date(self):
        self.assertEqual((ROOT / "VERSION").read_text().strip(), VERSION)
        self.assertEqual((ROOT / "OFFICIAL_SKILL_RELEASE").read_text().strip(), VERSION)
        self.assertEqual(audit_published_source_metadata(ROOT), [])
        citation = (ROOT / "CITATION.cff").read_text()
        self.assertIn('date-released: "2026-11-22"', citation)
        self.assertIn("## " + VERSION + " — 2026-11-22",
                      (ROOT / "CHANGELOG.md").read_text())

    def test_current_links_are_consistent_across_active_guides(self):
        for path in ACTIVE:
            with self.subTest(path=path):
                content = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn(RELEASE_URL, content)
                self.assertNotIn("latest verified published experimental package", content.lower())
                self.assertNotIn("source v1.0.0-rc.1 is an unpublished", content.lower())
        for path in ("README.md", "docs/INSTALLATION.md", "docs/CHATGPT.md",
                     "docs/COMECE-AQUI.md", "wiki/Installation.md"):
            with self.subTest(installer=path):
                self.assertIn(ZIP_URL, (ROOT / path).read_text(encoding="utf-8"))

    def test_release_cards_pdfs_and_limits_not_conflated(self):
        landing = (ROOT / "docs/CURRENT-RELEASE.md").read_text(encoding="utf-8")
        for expected in ("51", "475", "174", "XLSX", "PENDING",
                         "experimental", "v0.9.0-beta.6"):
            self.assertIn(expected, landing)
        self.assertTrue((ROOT / "knowledge/methodology/PDF-ATTRIBUTIONS.md").exists())
        self.assertTrue((ROOT / "docs/NOTAS-DA-VERSAO-0.9.0-beta.6.md").exists())


if __name__ == "__main__":
    unittest.main()
