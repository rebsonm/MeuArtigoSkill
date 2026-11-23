"""RC.4 is an unpublished plugin candidate; historical RC.3 remains cited."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_release_metadata import audit_candidate_metadata
from check_github_zenodo_parity import preflight

CANDIDATE = "1.0.0-rc.4"
PUBLISHED = "1.0.0-rc.3"
RELEASE_URL = "https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v" + PUBLISHED


class PluginCandidateAndPublishedHistoryTests(unittest.TestCase):
    def test_candidate_separate_from_published_history(self):
        self.assertEqual((ROOT / "VERSION").read_text().strip(), CANDIDATE)
        self.assertEqual((ROOT / "OFFICIAL_SKILL_RELEASE").read_text().strip(), PUBLISHED)
        self.assertEqual(audit_candidate_metadata(ROOT), [])
        self.assertEqual(preflight(ROOT, "v" + CANDIDATE), [])
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        self.assertIn('version: "1.0.0-rc.4"', citation)
        self.assertNotRegex(citation, r"(?m)^date-released:")
        self.assertNotRegex(citation, r"(?m)^doi:")
        self.assertIn("## 1.0.0-rc.4 —", (ROOT / "CHANGELOG.md").read_text())
        self.assertIn("NOT PUBLISHED", (ROOT / "docs/NOTAS-DA-VERSAO-1.0.0-rc.4.md").read_text())

    def test_plugin_only_public_guides_and_historical_release(self):
        for path in ("README.md","docs/INSTALLATION.md","docs/CHATGPT.md",
                     "docs/COMECE-AQUI.md","docs/COMPATIBILIDADE-PLATAFORMAS.md"):
            text=(ROOT / path).read_text(encoding="utf-8")
            self.assertIn("plugin", text.lower())
            self.assertIn(RELEASE_URL, text)
            self.assertNotIn("MeuArtigoSkill-v1.0.0-rc.4.zip", text)
            self.assertIn("rc.4", text.lower())
        self.assertFalse((ROOT / "assets/rc4-logo.png").exists() and
                         (ROOT / "VERSION").read_text().strip() != CANDIDATE)

    def test_historical_history_and_rights_are_retained(self):
        historic = (ROOT / "docs/CURRENT-RELEASE.md").read_text(encoding="utf-8")
        for term in ("51","475","174","XLSX","PENDING","v0.9.0-beta.6","1.0.0-rc.3"):
            self.assertIn(term, historic)
        self.assertTrue((ROOT / "knowledge/methodology/PDF-ATTRIBUTIONS.md").exists())


if __name__ == "__main__":
    unittest.main()
