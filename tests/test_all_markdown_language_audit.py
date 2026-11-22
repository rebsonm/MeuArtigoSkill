"""Coverage regression for the full Markdown language inventory."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_all_markdown_language import inspect_markdown


class AllMarkdownLanguageTests(unittest.TestCase):
    def test_every_markdown_area_is_scanned(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = [
                "docs/guide.md",
                "knowledge/methodology/cards/c1.md",
                "knowledge/methodology/source_cards/src-0001.md",
                "knowledge/methodology/intake/history.md",
                "wiki/Home.md",
            ]
            for rel in paths:
                p = root / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(
                    ("Scientific inquiry must record sources.\n" if rel.startswith("docs/") else
                     "A pesquisa científica não dispensa revisão e análise das fontes. "
                     "O pesquisador deve verificar a metodologia, os resultados e a evidência.\n"),
                    encoding="utf-8",
                )
            report = inspect_markdown(root)
            self.assertEqual(report["markdown_files_scanned"], 5)
            self.assertEqual(report["files_requiring_editorial_language_review"], 4)
            flagged = {item["path"] for item in report["unresolved"]}
            self.assertNotIn("docs/guide.md", flagged)
            self.assertIn("knowledge/methodology/cards/c1.md", flagged)
            self.assertIn("knowledge/methodology/source_cards/src-0001.md", flagged)
            self.assertIn("knowledge/methodology/intake/history.md", flagged)
            self.assertIn("wiki/Home.md", flagged)
            self.assertFalse(report["english_only_verified"])

    def test_bibliographic_titles_are_not_translation_targets(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            p = root / "knowledge/methodology/source_cards/src-0009.md"
            p.parent.mkdir(parents=True)
            p.write_text(
                "- Bibliographic source: A pesquisa científica exige revisão e "
                "análise das fontes, metodologia e verificação\n"
                "The remaining editorial guidance is written in English.\n",
                encoding="utf-8",
            )
            self.assertEqual(inspect_markdown(root)["unresolved"], [])

    def test_strict_threshold_is_explicit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            p = root / "README.md"
            p.write_text("A pesquisa científica não dispensa revisão, "
                         "análise, verificação, resultados e fontes.\n",
                         encoding="utf-8")
            self.assertEqual(inspect_markdown(root)["files_requiring_editorial_language_review"], 1)
            self.assertEqual(inspect_markdown(root, threshold=30)["unresolved"], [])
            with self.assertRaises(ValueError):
                inspect_markdown(root, threshold=0)


if __name__ == "__main__":
    unittest.main()
