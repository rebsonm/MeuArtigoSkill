"""Fail-closed retrieval for PDFs whose exact CC BY license version is unknown.

Synthetic metadata and dummy bytes only. No published PDF is downloaded.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "experimental" / "conceptual_rag"))

import public_method_pdf as installed_reader
import github_pdf_reader as experimental_reader

COMMIT = "a" * 40


def entry(slug, license_label):
    body = b"not a PDF"
    return {
        "path": f"knowledge/methodology/pdfs/{slug}.pdf",
        "title": "Synthetic research methods",
        "authors": "Fixture Author",
        "year": 2026,
        "rights": "PUBLIC_REDISTRIBUTION_REVIEWED",
        "license": license_label,
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "rights_evidence": "https://example.org/fictional",
        "source_url": "https://example.org/fictional",
        "sha256": hashlib.sha256(body).hexdigest(),
        "size": len(body),
        "keywords": ["synthetic", "methods"],
    }


class LicenseVersionRetrievalTests(unittest.TestCase):
    def test_unversioned_entry_remains_metadata_only(self):
        for module in (installed_reader, experimental_reader):
            with self.subTest(module=module.__name__):
                raw = json.dumps({
                    "schema": module.SCHEMA,
                    "documents": [entry("unversioned", "CC BY")],
                }).encode("utf-8")
                calls = []

                def fetch(ref, path, limit):
                    calls.append(path)
                    if path != module.CATALOG:
                        self.fail("Unversioned PDF was downloaded")
                    return raw

                result = module.query("synthetic methods", ref=COMMIT, fetch=fetch)
                self.assertEqual(result["status"], "NO_MATCH_IN_PUBLIC_PDF_CATALOG")
                self.assertFalse(result["pdf_fetched"])
                self.assertEqual(calls, [module.CATALOG])
                self.assertEqual(len(module.metadata(raw)), 1)

    def test_versioned_document_selected_before_ambiguous_one(self):
        for module in (installed_reader, experimental_reader):
            with self.subTest(module=module.__name__):
                approved = entry("versioned", "CC BY 4.0")
                raw = json.dumps({
                    "schema": module.SCHEMA,
                    "documents": [entry("unversioned", "CC BY"), approved],
                }).encode("utf-8")
                calls = []

                def fetch(ref, path, limit):
                    calls.append(path)
                    if path == module.CATALOG:
                        return raw
                    self.assertEqual(path, approved["path"])
                    return b"not a PDF"

                with self.assertRaisesRegex(ValueError, "NOT_A_PDF"):
                    module.query("synthetic methods", ref=COMMIT, fetch=fetch)
                self.assertEqual(calls, [module.CATALOG, approved["path"]])


if __name__ == "__main__":
    unittest.main()
