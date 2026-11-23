"""Offline checks for unpublished RC.3 source and published historical RC.1.

Read-only file assertions; cannot verify real GitHub/Zenodo releases.
"""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_release_metadata import audit_candidate_metadata
from check_github_zenodo_parity import preflight

CANDIDATE = "1.0.0-rc.3"
PUBLISHED = "1.0.0-rc.1"
RELEASE_URL = "https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v" + PUBLISHED
ZIP_URL = ("https://github.com/rebsonm/MeuArtigoSkill/releases/download/"
           "v" + PUBLISHED + "/MeuArtigoSkill-v" + PUBLISHED + ".zip")
ACTIVE = (
    "README.md", "SECURITY.md", "docs/INSTALLATION.md", "docs/CHATGPT.md",
    "docs/COMECE-AQUI.md", "docs/IMPLANTACAO-BETA.md",
    "docs/TESTE-BETA-PESQUISADORES.md", "docs/COMPATIBILIDADE-PLATAFORMAS.md",
    "wiki/Home.md", "wiki/FAQ.md", "wiki/Installation.md",
    "wiki/Status-and-Limitations.md", "docs/CURRENT-RELEASE.md",
)


class CandidateAndPublishedDocsTests(unittest.TestCase):
    def test_unpublished_candidate_and_published_pointer_are_separate(self):
        self.assertEqual((ROOT / "VERSION").read_text().strip(), CANDIDATE)
        self.assertEqual((ROOT / "OFFICIAL_SKILL_RELEASE").read_text().strip(),
                         PUBLISHED)
        self.assertEqual(audit_candidate_metadata(ROOT), [])
        self.assertEqual(preflight(ROOT, "v" + CANDIDATE), [])
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        self.assertIn('version: "' + CANDIDATE + '"', citation)
        self.assertNotIn("date-released:", citation)
        self.assertNotIn('doi: "10.5281/zenodo.', citation)
        self.assertIn("## " + CANDIDATE + " — UNRELEASED",
                      (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertIn("NOT PUBLISHED",
                      (ROOT / "docs" / f"NOTAS-DA-VERSAO-{CANDIDATE}.md")
                      .read_text(encoding="utf-8"))

    def test_historical_published_links_remain_valid_in_guides(self):
        for path in ACTIVE:
            with self.subTest(path=path):
                content = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn(RELEASE_URL, content)
                self.assertNotIn("latest verified published experimental package",
                                 content.lower())
        for path in ("README.md", "docs/INSTALLATION.md", "docs/CHATGPT.md",
                     "docs/COMECE-AQUI.md", "wiki/Installation.md"):
            with self.subTest(installer=path):
                self.assertIn(ZIP_URL, (ROOT / path).read_text(encoding="utf-8"))
        self.assertNotIn(f"/releases/tag/v{CANDIDATE}",
                         (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_rights_scope_and_host_limitations_remain_documented(self):
        landing = (ROOT / "docs/CURRENT-RELEASE.md").read_text(encoding="utf-8")
        for expected in ("51", "475", "174", "XLSX", "PENDING",
                         "experimental", "v0.9.0-beta.6",
                         "1.0.0-rc.3", "1.0.0-rc.2", "1.0.0-rc.1"):
            self.assertIn(expected, landing)
        self.assertTrue((ROOT / "knowledge/methodology/PDF-ATTRIBUTIONS.md").exists())
        self.assertTrue((ROOT / "docs/NOTAS-DA-VERSAO-0.9.0-beta.6.md").exists())


if __name__ == "__main__":
    unittest.main()
