"""Offline regression for internal Markdown links and heading fragments."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import check_documentation_links as links


class DocumentationLinkTests(unittest.TestCase):
    def test_repo_guidance_links_exist(self):
        report=links.inspect(ROOT)
        self.assertEqual(report["errors"],[], "\n".join(report["errors"]))
        self.assertGreater(report["documents"],20)
        self.assertGreater(report["checked"],25)

    def test_missing_file_is_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/"README.md").write_text("[a](docs/missing.md)",encoding="utf-8")
            report=links.inspect(root)
            self.assertTrue(any("destination missing" in e for e in report["errors"]))

    def test_heading_anchor_is_checked(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/"docs").mkdir()
            (root/"docs"/"guide.md").write_text("# Como começar\n",encoding="utf-8")
            (root/"README.md").write_text("[ok](docs/guide.md#como-começar)\n"
                                         "[bad](docs/guide.md#nao-existe)\n",encoding="utf-8")
            report=links.inspect(root)
            self.assertEqual(len(report["errors"]),1)
            self.assertIn("heading not found",report["errors"][0])

    def test_ignore_external_and_code_fences(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/"README.md").write_text(
                "[official](https://example.org/doc)\n"
                "Inline: "+chr(96)+"[ignored](bad.md)"+chr(96)+"\n"
                "~~~md\n"
                "[example](other.md)\n"
                "~~~\n",encoding="utf-8")
            self.assertEqual(links.inspect(root)["errors"],[])

    def test_relative_parent_and_reference_link(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/"docs").mkdir()
            (root/"README.md").write_text("# README",encoding="utf-8")
            (root/"docs"/"page.md").write_text(
                "[go][root]\n[root]: ../README.md\n",encoding="utf-8")
            self.assertEqual(links.inspect(root)["errors"],[])

    def test_traversal_outside_repo_is_error(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/"README.md").write_text("[bad](../../private.txt)",encoding="utf-8")
            self.assertTrue(any("escapes repository" in e for e in links.inspect(root)["errors"]))


if __name__=="__main__":
    unittest.main()
