"""Fail-closed GitHub source-tree audit for PDF-only, license-reviewed public corpus.

This is a structural consistency gate; it cannot authenticate a publisher's
license. Repository maintainers must verify redistribution evidence manually.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experimental" / "conceptual_rag"))
import github_pdf_reader as pdf_reader


class PublicPDFCorpusSafetyTests(unittest.TestCase):
    def test_no_unindexed_or_unlicensed_public_pdf(self):
        root = ROOT / "knowledge" / "methodology"
        catalog = root / "pdf_catalog.json"
        self.assertTrue(catalog.is_file())
        docs = pdf_reader.metadata(catalog.read_bytes())
        listed = set()
        for entry in docs:
            path = ROOT / entry["path"]
            self.assertFalse(path.is_symlink(), msg=entry["path"])
            self.assertTrue(path.is_file(), msg=entry["path"])
            blob = path.read_bytes()
            self.assertTrue(blob.startswith(b"%PDF-"), msg=entry["path"])
            self.assertEqual(len(blob), entry["size"], msg=entry["path"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"], msg=entry["path"])
            listed.add(entry["path"])
        actual = set()
        for path in (ROOT / "knowledge").rglob("*.pdf"):
            self.assertFalse(path.is_symlink())
            actual.add(path.relative_to(ROOT).as_posix())
        self.assertEqual(actual, listed, msg="Unreviewed PDF present in the public knowledge tree")

    def test_public_catalog_does_not_claim_independent_scientific_review(self):
        catalog = json.loads((ROOT / "knowledge" / "methodology" / "pdf_catalog.json").read_text())
        self.assertFalse(catalog.get("installer_includes_pdfs"))
        self.assertEqual(catalog.get("rights_policy"), "PUBLIC_REDISTRIBUTION_REVIEWED_ONLY")


if __name__ == "__main__":
    unittest.main()
