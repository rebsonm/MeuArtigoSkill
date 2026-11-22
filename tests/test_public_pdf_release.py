"""Synthetic regression for a public-PDF release technical preflight.

No research PDFs or live publisher permissions are used in these tests.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_public_pdf_release import audit, attribution_register


class PublicPDFReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root / "knowledge/methodology/pdfs"
        self.directory.mkdir(parents=True)
        self.catalog = self.root / "knowledge/methodology/pdf_catalog.json"

    def add(self, name: str, license: str = "CC BY 4.0"):
        path = self.directory / name
        body = b"%PDF-1.4\nSynthetic test fixture - no article content.\n"
        path.write_bytes(body)
        return {
            "path": "knowledge/methodology/pdfs/" + name,
            "title": "Fictional research methods article",
            "authors": "Synthetic Author",
            "year": 2026, "doi": "10.0000/fictional",
            "rights": "PUBLIC_REDISTRIBUTION_REVIEWED",
            "license": license, "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "rights_evidence": "https://publisher.invalid/article/fictional",
            "source_url": "https://publisher.invalid/article/fictional",
            "sha256": hashlib.sha256(body).hexdigest(),
            "size": len(body)
        }

    def save(self, rows):
        self.catalog.write_text(json.dumps({
            "schema": "MEU_ARTIGO_PUBLIC_PDF_CATALOG_V1",
            "documents": rows}, ensure_ascii=False), encoding="utf-8")

    def test_exact_bytes_are_technical_candidates_not_legal_permission(self):
        self.save([self.add("synthetic-source.pdf")])
        result = audit(self.root)
        self.assertEqual(result["integrity_status"], "PASS")
        self.assertEqual(result["technical_candidates"], 1)
        self.assertEqual(result["pending_reconciliation"], 0)
        self.assertEqual(result["release_clearance"],
                         "BLOCKED_PENDING_INDEPENDENT_RIGHTS_REVIEW")
        self.assertIn("NOT an authorization", attribution_register(result))

    def test_license_version_unknown_cannot_be_auto_approved(self):
        self.save([self.add("synthetic-source.pdf", "CC BY")])
        result = audit(self.root)
        self.assertEqual(result["integrity_status"], "PASS")
        self.assertEqual(result["technical_candidates"], 0)
        self.assertEqual(result["pending_reconciliation"], 1)
        self.assertIn("PUBLISHER_LICENSE_VERSION_REQUIRES_REVIEW",
                      [e["issue"] for e in result["issues"]])

    def test_modified_pdf_fails_even_with_unmodified_catalog_claim(self):
        row = self.add("synthetic-source.pdf")
        self.save([row])
        (self.directory / "synthetic-source.pdf").write_bytes(b"%PDF-1.4 altered")
        result = audit(self.root)
        self.assertEqual(result["integrity_status"], "FAIL")
        self.assertIn("PDF_SHA256_MISMATCH",
                      [e["issue"] for e in result["issues"]])

    def test_unlisted_pdf_is_fatal(self):
        self.save([self.add("synthetic-source.pdf")])
        (self.directory / "unlisted-source.pdf").write_bytes(b"%PDF-1.4")
        result = audit(self.root)
        self.assertEqual(result["integrity_status"], "FAIL")
        self.assertIn("UNLISTED_PDF_BINARY",
                      [e["issue"] for e in result["issues"]])

    def test_duplicate_catalog_path_is_not_safe(self):
        source = self.add("synthetic-source.pdf")
        self.save([source, dict(source)])
        result = audit(self.root)
        self.assertEqual(result["integrity_status"], "FAIL")
        self.assertIn("UNSAFE_OR_DUPLICATE_FILE_PATH",
                      [e["issue"] for e in result["issues"]])

    def test_unknown_rights_remain_pending(self):
        row = self.add("synthetic-source.pdf")
        row["rights"] = "UNKNOWN"
        self.save([row])
        result = audit(self.root)
        self.assertEqual(result["integrity_status"], "PASS")
        self.assertIn("RIGHTS_CLAIM_NOT_REVIEWED",
                      [e["issue"] for e in result["issues"]])


if __name__ == "__main__":
    unittest.main()
