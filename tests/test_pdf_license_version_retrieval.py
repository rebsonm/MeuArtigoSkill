"""Synthetic regression: publisher-declared CC BY PDFs can be accessed.

No third-party PDFs are downloaded; fixture bytes are fictional.
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


def entry(license_label):
    body = b"not a PDF"
    return {
        "path": "knowledge/methodology/pdfs/synthetic-example.pdf",
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
    def test_declared_cc_by_available_without_silent_downgrade(self):
        for module in (installed_reader, experimental_reader):
            for label in ("CC BY", "CC BY 4.0"):
                with self.subTest(module=module.__name__, license=label):
                    item = entry(label)
                    raw = json.dumps({
                        "schema": module.SCHEMA,
                        "documents": [item],
                    }).encode("utf-8")
                    calls = []

                    def fetch(ref, path, limit):
                        calls.append(path)
                        if path == module.CATALOG:
                            return raw
                        self.assertEqual(path, item["path"])
                        return b"not a PDF"

                    self.assertEqual(len(module.metadata(raw)), 1)
                    with self.assertRaisesRegex(ValueError, "NOT_A_PDF"):
                        module.query("synthetic methods", ref=COMMIT, fetch=fetch)
                    self.assertEqual(calls, [module.CATALOG, item["path"]])

    def test_restricted_license_is_not_mislabeled_as_cc_by(self):
        for module in (installed_reader, experimental_reader):
            with self.subTest(module=module.__name__):
                raw = json.dumps({
                    "schema": module.SCHEMA,
                    "documents": [entry("CC BY-NC 4.0")],
                }).encode("utf-8")
                with self.assertRaisesRegex(ValueError, "PUBLIC_PDF_LICENSE_NOT_UNRESTRICTED"):
                    module.metadata(raw)


if __name__ == "__main__":
    unittest.main()
