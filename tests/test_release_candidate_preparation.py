"""Unpublished RC preparation must be honest, reversible and read-only to study data.

Fixtures exercise only source release metadata, never connected providers.
"""
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_release_metadata import audit_candidate_metadata, audit_release_metadata
from sync_version import prepare_candidate
from version_info import read_version, release_channel


class CandidatePreparationTests(unittest.TestCase):
    def setUp(self):
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        self.root = Path(holder.name)
        (self.root / "docs").mkdir()
        (self.root / "VERSION").write_text("1.0.0-rc.1\n", encoding="utf-8")
        (self.root / "OFFICIAL_SKILL_RELEASE").write_text("0.9.0-beta.6\n", encoding="utf-8")
        (self.root / "README.md").write_text(
            "**Current version:** `0.9.0-beta.6` — unpublished release candidate "
            "source for a controlled test, not a published installer.\n",
            encoding="utf-8")
        (self.root / "CITATION.cff").write_text(
            'version: "0.9.0-beta.6"\ndate-released: "2026-10-15"\n',
            encoding="utf-8")
        (self.root / "CHANGELOG.md").write_text(
            "## Unreleased\n\n## 1.0.0-rc.1 — UNRELEASED\n\n"
            "Experimental source candidate for practical acceptance.\n"
            "## 0.9.0-beta.6 — 2026-10-15\n",
            encoding="utf-8")
        (self.root / "docs/NOTAS-DA-VERSAO-1.0.0-rc.1.md").write_text(
            "# Meu Artigo v1.0.0-rc.1\n"
            "RELEASE CANDIDATE ONLY — NOT PUBLISHED. NOT A STABLE RELEASE.\n",
            encoding="utf-8")

    def test_candidate_synchronizer_preserves_published_recommendation(self):
        official = (self.root / "OFFICIAL_SKILL_RELEASE").read_bytes()
        self.assertEqual(prepare_candidate(self.root),
                         ["README.md", "CITATION.cff"])
        self.assertEqual(prepare_candidate(self.root), [])
        self.assertEqual((self.root / "OFFICIAL_SKILL_RELEASE").read_bytes(), official)
        self.assertEqual(release_channel(read_version(self.root)), "release-candidate")
        self.assertIn("**Current version:** `1.0.0-rc.1`",
                      (self.root / "README.md").read_text())
        citation = (self.root / "CITATION.cff").read_text()
        self.assertIn('version: "1.0.0-rc.1"', citation)
        self.assertNotIn("date-released:", citation)
        self.assertEqual(audit_candidate_metadata(self.root), [])

    def test_candidate_without_publication_date_cannot_pass_beta_release_gate(self):
        prepare_candidate(self.root)
        self.assertIn("CITATION_DATE_MISSING_OR_AMBIGUOUS",
                      audit_release_metadata(self.root))

    def test_fake_candidate_publication_date_is_blocked(self):
        prepare_candidate(self.root)
        cff = self.root / "CITATION.cff"
        cff.write_text(cff.read_text() + 'date-released: "2026-11-20"\n')
        self.assertIn("UNPUBLISHED_CANDIDATE_MUST_NOT_CLAIM_RELEASE_DATE",
                      audit_candidate_metadata(self.root))

    def test_public_recommendation_must_not_silently_change_to_rc(self):
        prepare_candidate(self.root)
        (self.root / "OFFICIAL_SKILL_RELEASE").write_text("1.0.0-rc.1\n")
        self.assertIn("PUBLISHED_RECOMMENDATION_MUST_STAY_BETA6",
                      audit_candidate_metadata(self.root))

    def test_bogus_published_rc_link_is_not_accepted(self):
        prepare_candidate(self.root)
        f = self.root / "README.md"
        f.write_text(f.read_text() +
                     "https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v1.0.0-rc.1\n")
        self.assertIn("UNPUBLISHED_RC_MUST_NOT_HAVE_RELEASE_LINK",
                      audit_candidate_metadata(self.root))

    def test_missing_author_notes_blocks_candidate_synchronizer(self):
        (self.root / "docs/NOTAS-DA-VERSAO-1.0.0-rc.1.md").unlink()
        before = (self.root / "CITATION.cff").read_bytes()
        with self.assertRaisesRegex(ValueError, "candidate notes"):
            prepare_candidate(self.root)
        self.assertEqual(before, (self.root / "CITATION.cff").read_bytes())

    def test_not_rc_cannot_inherit_candidate_metadata(self):
        (self.root / "VERSION").write_text("1.0.0\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "release-candidate"):
            prepare_candidate(self.root)


if __name__ == "__main__":
    unittest.main()
