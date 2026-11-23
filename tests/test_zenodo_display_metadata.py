"""Protect Zenodo title presentation for future GitHub-archived releases.

Source metadata and unit fixtures cannot certify remote Zenodo UI or DOI.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_TITLE = "Meu Artigo — AI-Assisted Scientific Research Workflow and Governance Tool"


class ZenodoDisplayMetadataTests(unittest.TestCase):
    def test_citation_name_used_by_github_zenodo_matches_official_title(self):
        cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        names = re.findall(r'^title:\s*"([^"]+)"\s*$', cff, flags=re.M)
        self.assertEqual(names, [OFFICIAL_TITLE])
        self.assertIn('version: "' + (ROOT / "VERSION").read_text().strip() + '"', cff)
        self.assertIn('doi: "10.5281/zenodo.24452285"', cff)

    def test_canonical_author_is_mendes_rebson_de_morais(self):
        cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        match = re.search(
            r'(?m)^authors:\\s*\\n\\s+- family-names:\\s*"([^"]+)"'
            r'\\s*\\n\\s+given-names:\\s*"([^"]+)"',
            cff,
        )
        self.assertIsNotNone(match, "Software author missing or malformed")
        family, given = match.groups()
        self.assertEqual((family, given), ("Mendes", "Rebson de Morais"))
        self.assertEqual(f"{family}, {given}", "Mendes, Rebson de Morais")

    def test_zenodo_draft_matches_title_type_and_access(self):
        obj = json.loads((ROOT / "zenodo/metadata-draft.json").read_text(encoding="utf-8"))
        self.assertEqual(obj["title"], OFFICIAL_TITLE)
        self.assertEqual(obj["creators"], [{"name": "Mendes, Rebson de Morais"}])
        self.assertEqual(obj["upload_type"], "software")
        self.assertEqual(obj["access_right"], "open")

    def test_any_future_zenodo_override_must_keep_same_title(self):
        # Zenodo prioritizes .zenodo.json over CITATION.cff if both exist.
        override = ROOT / ".zenodo.json"
        if override.exists():
            metadata = json.loads(override.read_text(encoding="utf-8"))
            self.assertEqual(metadata["title"], OFFICIAL_TITLE)


if __name__ == "__main__":
    unittest.main()
