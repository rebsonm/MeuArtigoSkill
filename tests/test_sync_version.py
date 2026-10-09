"""VERSION is authoritative; sync derived metadata without fabricated contents."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import sync_version


class VersionSyncTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        (self.root/"docs").mkdir()
        (self.root/"VERSION").write_text("0.8.0-beta.9\n",encoding="utf-8")
        (self.root/"README.md").write_text("**Current version:** `0.8.0-beta.8` · downloads\n",encoding="utf-8")
        (self.root/"CITATION.cff").write_text(
            'version: "0.8.0-beta.8"\ndate-released: "2026-10-08"\n',encoding="utf-8"
        )
        (self.root/"CHANGELOG.md").write_text(
            "# Changelog\n\n## Unreleased\n\n- Contributor-approved change.\n\n"
            "## 0.8.0-beta.8 — 2026-10-08\n\n- History preserved.\n",encoding="utf-8"
        )
        (self.root/"docs/NOTAS-DA-VERSAO-0.8.0-beta.9.md").write_text(
            "# Version 0.8.0-beta.9\n\n- Approved release scope.\n",encoding="utf-8"
        )

    def test_syncs_all_public_metadata_and_preserves_history(self):
        changes=sync_version.sync(self.root,"2026-10-09")
        self.assertEqual(changes,["README.md","CITATION.cff","CHANGELOG.md"])
        changelog=(self.root/"CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("Contributor-approved change",changelog)
        self.assertIn("## 0.8.0-beta.9 — 2026-10-09",changelog)
        self.assertIn("History preserved",changelog)
        self.assertIn('version: "0.8.0-beta.9"',
                      (self.root/"CITATION.cff").read_text(encoding="utf-8"))
        self.assertEqual(sync_version.sync(self.root,"2026-10-09"),[])

    def test_missing_real_release_notes_blocks_all_writes(self):
        (self.root/"docs/NOTAS-DA-VERSAO-0.8.0-beta.9.md").unlink()
        before=(self.root/"README.md").read_text(encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"Author real release notes"):
            sync_version.sync(self.root,"2026-10-09")
        self.assertEqual((self.root/"README.md").read_text(encoding="utf-8"),before)

    def test_bad_date_blocks_all_writes(self):
        with self.assertRaises(ValueError):
            sync_version.sync(self.root,"tomorrow")
        self.assertIn("beta.8",(self.root/"CITATION.cff").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
