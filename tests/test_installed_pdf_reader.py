"""Synthetic local-PDF tests: never fetch an unlisted missing PDF remotely."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import public_method_pdf as reader


class InstalledLocalPDFTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        self.catalog = self.root / "knowledge/methodology/pdf_catalog.json"
        self.catalog.parent.mkdir(parents=True)
        self.pdf = self.root / "knowledge/methodology/pdfs/test-source.pdf"
        self.pdf.parent.mkdir(parents=True)
        self.data = b"%PDF-1.4\nSynthetic licensed fixture\n"
        self.pdf.write_bytes(self.data)
        self.catalog.write_text(json.dumps({"schema": reader.SCHEMA, "documents": []}))
        self.filename = str(self.root / "scripts/public_method_pdf.py")

    def test_local_catalog_and_pdf_used_without_network(self):
        with patch.object(reader, "__file__", self.filename):
            with patch.object(reader, "fetch_github", side_effect=AssertionError("NETWORK_USED")):
                self.assertIn(b"documents", reader.fetch_installed_or_github(
                    "a" * 40, reader.CATALOG, 250_000))
                self.assertEqual(reader.fetch_installed_or_github(
                    "a" * 40,
                    "knowledge/methodology/pdfs/test-source.pdf", 20000), self.data)

    def test_missing_pdf_does_not_trigger_remote_fallback(self):
        self.pdf.unlink()
        with patch.object(reader, "__file__", self.filename):
            with patch.object(reader, "fetch_github", side_effect=AssertionError("NETWORK_USED")):
                with self.assertRaisesRegex(ValueError, "BUNDLED_CATALOG_OR_PDF_MISSING"):
                    reader.fetch_installed_or_github(
                        "a"*40, "knowledge/methodology/pdfs/test-source.pdf", 20_000)

    def test_symlinked_pdf_refused(self):
        self.pdf.unlink()
        self.pdf.symlink_to(self.catalog)
        with patch.object(reader, "__file__", self.filename):
            with self.assertRaisesRegex(ValueError, "BUNDLED_CATALOG_OR_PDF_MISSING"):
                reader.fetch_installed_or_github(
                    "a"*40, "knowledge/methodology/pdfs/test-source.pdf", 20_000)

    def test_local_pdf_size_bound(self):
        with patch.object(reader, "__file__", self.filename):
            with self.assertRaisesRegex(ValueError, "BUNDLED_BYTES_EXCEED_LIMIT"):
                reader.fetch_installed_or_github(
                    "a"*40, "knowledge/methodology/pdfs/test-source.pdf", 8)


if __name__ == "__main__":
    unittest.main()
