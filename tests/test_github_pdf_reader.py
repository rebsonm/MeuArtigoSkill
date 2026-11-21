"""No-network PDF-first retrieval regression checks. Synthetic content only."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experimental" / "conceptual_rag"))
import github_pdf_reader as reader

REF = "a" * 40


class PublicPDFGuardTests(unittest.TestCase):
    def catalog(self, entries):
        return json.dumps({"schema": reader.SCHEMA, "documents": entries}).encode()

    def entry(self, data=b"%PDF-1.6\nsynthetic", **overrides):
        item = {
            "path": "knowledge/methodology/pdfs/synthetic-example.pdf",
            "title": "Synthetic Example",
            "sha256": hashlib.sha256(data).hexdigest(),
            "size": len(data),
            "rights": "PUBLIC_REDISTRIBUTION_REVIEWED",
            "rights_evidence": "https://example.org/test-license",
            "keywords": ["synthetic", "methods"],
        }
        item.update(overrides)
        return item

    def fake(self, catalog, pdf=b""):
        calls = []
        def get(ref, path, limit):
            self.assertEqual(ref, REF)
            calls.append(path)
            return catalog if path == reader.CATALOG else pdf
        return get, calls

    def test_empty_catalogue_never_downloads_pdf(self):
        get, calls = self.fake(self.catalog([]))
        result = reader.query("systematic review", ref=REF, fetch=get)
        self.assertEqual(result["status"], "NO_MATCH_IN_PUBLIC_PDF_CATALOG")
        self.assertFalse(result["pdf_fetched"])
        self.assertEqual(calls, [reader.CATALOG])

    def test_unrelated_query_never_downloads_pdf(self):
        pdf = b"%PDF-1.6\nsynthetic"
        get, calls = self.fake(self.catalog([self.entry(pdf)]), pdf)
        result = reader.query("volcano earthquake", ref=REF, fetch=get)
        self.assertEqual(result["status"], "NO_MATCH_IN_PUBLIC_PDF_CATALOG")
        self.assertEqual(calls, [reader.CATALOG])

    def test_unverified_rights_or_evidence_are_blocked(self):
        with self.assertRaisesRegex(ValueError, "RIGHTS_NOT_REVIEWED"):
            reader.metadata(self.catalog([self.entry(rights="PRIVATE_AUTHORIZED")]))
        with self.assertRaisesRegex(ValueError, "RIGHTS_EVIDENCE_REQUIRED"):
            reader.metadata(self.catalog([self.entry(rights_evidence="")]))

    def test_unsafe_or_duplicate_paths_blocked(self):
        for path in ("../../private.pdf", "https://example.com/private.pdf",
                     "knowledge/methodology/pdfs/../../private.pdf"):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "PDF_PATH_UNSAFE"):
                reader.metadata(self.catalog([self.entry(path=path)]))
        entry = self.entry()
        with self.assertRaisesRegex(ValueError, "PDF_PATH_UNSAFE"):
            reader.metadata(self.catalog([entry, entry]))

    def test_branch_refs_fail_before_network(self):
        get, calls = self.fake(self.catalog([]))
        with self.assertRaisesRegex(ValueError, "IMMUTABLE_GITHUB_COMMIT_REQUIRED"):
            reader.query("systematic review", ref="main", fetch=get)
        self.assertEqual(calls, [])

    def test_tampered_pdf_fails_before_parsing(self):
        pdf = b"%PDF-1.6\nsynthetic"
        get, calls = self.fake(self.catalog([self.entry(pdf)]), pdf + b"ADDED")
        with self.assertRaisesRegex(ValueError, "PDF_SIZE_OR_HASH_MISMATCH"):
            reader.query("synthetic methods", ref=REF, fetch=get)
        self.assertEqual(len(calls), 2)

    def test_budgets_and_bad_pdf_header_are_rejected(self):
        pdf = b"not a PDF"
        get, calls = self.fake(self.catalog([self.entry(pdf)]), pdf)
        with self.assertRaisesRegex(ValueError, "NOT_A_PDF"):
            reader.query("synthetic methods", ref=REF, fetch=get)
        with self.assertRaisesRegex(ValueError, "RETRIEVAL_BUDGET_INVALID"):
            reader.query("synthetic methods", ref=REF, fetch=get, max_chars=99999)

    def test_real_pdf_pages_and_context_limit_when_parser_available(self):
        try:
            import fitz
        except ImportError:
            self.skipTest("PyMuPDF is optional on CI")
        pdf = fitz.open()
        page_a = pdf.new_page()
        page_a.insert_text((72, 72), "surveys surveys synthetic research")
        page_b = pdf.new_page()
        page_b.insert_text((72, 72), "interviews interviews synthetic analysis")
        data = pdf.tobytes()
        pdf.close()
        get, calls = self.fake(
            self.catalog([self.entry(data, keywords=["synthetic", "interviews"])]), data)
        result = reader.query("interviews synthetic", ref=REF, fetch=get,
                              max_chars=500, max_pages=1)
        self.assertEqual(result["status"], "RETRIEVED_PDF_PAGES")
        self.assertLessEqual(result["returned_context_chars"], 500)
        self.assertEqual(len(result["hits"]), 1)
        self.assertEqual(result["hits"][0]["pdf_page"], 2)
        self.assertFalse(result["hits"][0]["page_label_verified"])
        self.assertFalse(result["scientific_quality_validated"])
        self.assertEqual(calls, [reader.CATALOG, self.entry(data)["path"]])


if __name__ == "__main__":
    unittest.main()
