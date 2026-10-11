"""Offline regressions for published v0.9.0-beta.4 documentation.

GitHub's real published release/assets were confirmed externally before
this documentation update. Offline tests check consistent local claims only,
not real-time availability, scientific quality or installed account state.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_release_metadata import audit_release_metadata
from version_info import read_version


class Beta4PublicPreparationTests(unittest.TestCase):
    def setUp(self):
        self.version = read_version(ROOT)
        self.notes = (ROOT / "docs" / f"NOTAS-DA-VERSAO-{self.version}.md").read_text(encoding="utf-8")
        self.readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_publication_metadata_and_local_release_docs_agree(self):
        self.assertEqual(self.version, "0.9.0-beta.4")
        self.assertEqual(audit_release_metadata(ROOT, expected_date="2026-10-11"), [])
        self.assertIn("publication workflow", self.readme.lower())
        self.assertIn("pre-release is published", self.readme.lower())
        self.assertIn("pre-release", self.notes.lower())
        self.assertRegex(self.notes.lower(), r"not a\s+stable")

    def test_stable_release_is_not_misrepresented(self):
        self.assertIn("Every 0.9.0-beta release is experimental", self.readme)
        self.assertNotIn("independently validated", self.notes.split("## What changed")[0].lower().replace("not a",""))
        self.assertIn("seven researcher decision gates", self.notes)
        self.assertIn("No independent scientific validation", self.notes)

    def test_beta_test_guide_and_issue_template_exist_and_protect_private_data(self):
        guide = (ROOT / "docs/TESTE-BETA-PESQUISADORES.md").read_text(encoding="utf-8")
        issue = (ROOT / ".github/ISSUE_TEMPLATE/relato-beta.md").read_text(encoding="utf-8")
        for phrase in ["source", "research", "privacy", "GitHub"]:
            self.assertIn(phrase.lower(), (guide + issue).lower())
        self.assertIn("SECURITY.md", issue)
        self.assertIn("Expected result", issue)
        self.assertIn("Actual observed result", issue)
        self.assertIn("v0.9.0-beta.4", guide)

    def test_beta4_is_recommended_only_as_experimental_prerelease(self):
        self.assertEqual(
            (ROOT / "OFFICIAL_SKILL_RELEASE").read_text(encoding="utf-8").strip(),
            "0.9.0-beta.4")
        self.assertIn("beta.1 and beta.2", self.readme)
        self.assertIn("recommended experimental", self.readme.lower())
        self.assertIn("v0.9.0-beta.4", self.notes)
        self.assertNotIn("v1.0.0 has been published", self.readme)

    def test_publishing_remains_manual_and_rejects_duplicate_tag(self):
        work = (ROOT / ".github/workflows/publish-beta.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", work)
        self.assertIn("acknowledgement", work)
        self.assertIn('"$ACK" != "publish-beta"', work)
        self.assertIn("Tag $TAG exists; refusing to move or overwrite it.", work)
        self.assertIn("gh release create", work)
        self.assertIn("--prerelease", work)
        self.assertIn("--latest=false", work)
        self.assertNotIn("pull_request:", work)


if __name__ == "__main__":
    unittest.main()
