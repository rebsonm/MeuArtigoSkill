"""Release metadata checks are about publication honesty, not article quality."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_release_metadata import audit_release_metadata


class ReleaseMetadataTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        (self.root / "VERSION").write_text("0.9.0-beta.2\n", encoding="utf-8")
        (self.root / "docs").mkdir()
        (self.root / "CITATION.cff").write_text(
            'version: "0.9.0-beta.2"\n', encoding="utf-8")
        (self.root / "CHANGELOG.md").write_text(
            "## 0.9.0-beta.2 — 2026-10-10\n", encoding="utf-8")
        (self.root / "docs/NOTAS-DA-VERSAO-0.9.0-beta.2.md").write_text(
            "# Meu Artigo — 0.9.0-beta.2\nRELEASE CANDIDATE ONLY — NOT PUBLISHED\n",
            encoding="utf-8")
        (self.root / "README.md").write_text(
            "# Meu Artigo\nCurrent version 0.9.0-beta.2, unpublished.\n",
            encoding="utf-8")

    def _prepare(self):
        (self.root / "CITATION.cff").write_text(
            'version: "0.9.0-beta.2"\ndate-released: "2026-10-10"\n',
            encoding="utf-8")
        (self.root / "README.md").write_text(
            "Published v0.9.0-beta.2\n"
            "https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.2\n",
            encoding="utf-8")
        (self.root / "docs/NOTAS-DA-VERSAO-0.9.0-beta.2.md").write_text(
            "# Meu Artigo — 0.9.0-beta.2\nExperimental beta; independent"
            " scientific validation pending.\n", encoding="utf-8")

    def test_current_source_candidate_is_not_publishable(self):
        problems = audit_release_metadata(self.root, expected_date="2026-10-10")
        self.assertIn("CITATION_DATE_MISSING_OR_AMBIGUOUS", problems)
        self.assertIn("README_HAS_NO_EXACT_NEW_RELEASE_LINK", problems)
        self.assertIn("RELEASE_NOTES_STILL_DESCRIBE_UNPUBLISHED_CANDIDATE",
                      problems)

    def test_corrected_release_metadata_passes_documentary_gate_only(self):
        self._prepare()
        self.assertEqual(audit_release_metadata(self.root, expected_date="2026-10-10"), [])

    def test_wrong_publication_date_is_blocked(self):
        self._prepare()
        self.assertIn("CITATION_DATE_DOES_NOT_MATCH_PUBLICATION_DATE",
                      audit_release_metadata(self.root, expected_date="2026-10-11"))

    def test_duplicate_citation_date_is_blocked(self):
        self._prepare()
        file = self.root / "CITATION.cff"
        file.write_text(file.read_text(encoding="utf-8") +
                        'date-released: "2026-10-10"\n', encoding="utf-8")
        self.assertIn("CITATION_DATE_MISSING_OR_AMBIGUOUS",
                      audit_release_metadata(self.root))

    def test_changelog_mismatch_is_blocked(self):
        self._prepare()
        (self.root / "CHANGELOG.md").write_text(
            "## 0.9.0-beta.2 — 2026-10-09\n", encoding="utf-8")
        self.assertIn("CHANGELOG_PUBLICATION_DATE_INCONSISTENT",
                      audit_release_metadata(self.root))


if __name__ == "__main__":
    unittest.main()
