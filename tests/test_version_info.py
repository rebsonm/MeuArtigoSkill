"""Repository version contract regression; no scientific-data fixtures."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import version_info


class VersionContractTests(unittest.TestCase):
    def test_repository_version_has_matching_release_notes(self):
        version = version_info.read_version(ROOT)
        self.assertTrue(version_info.release_notes_path(ROOT).is_file())
        self.assertEqual(version_info.release_zip_name(ROOT),
                         f"MeuArtigoSkill-v{version}.zip")

    def test_version_can_advance_without_changing_python_source(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "VERSION").write_text("4.2.0-beta.93\n", encoding="utf-8")
            self.assertEqual(version_info.read_version(root), "4.2.0-beta.93")
            self.assertEqual(version_info.release_notes_path(root).name,
                             "NOTAS-DA-VERSAO-4.2.0-beta.93.md")

    def test_invalid_version_fails_closed(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for bad in ("", "latest", "v4.2.0", "0.8.0-beta.8; rm -rf /",
                        "../secret", "0.8.0-beta."):
                (root / "VERSION").write_text(bad, encoding="utf-8")
                with self.subTest(bad=bad), self.assertRaises(ValueError):
                    version_info.read_version(root)


if __name__ == "__main__":
    unittest.main()
