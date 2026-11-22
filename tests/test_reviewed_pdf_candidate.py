"""Synthetic-only negative/positive tests for opt-in PDF packaging."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_reviewed_pdf_candidate import select, notices


class SelectedPDFTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.pdf = self.root / "knowledge/methodology/pdfs/fictional.pdf"
        self.pdf.parent.mkdir(parents=True)
        self.data = b"%PDF-1.4\nFictional test fixture, no copyrighted research article.\n"
        self.pdf.write_bytes(self.data)
        self.scope_path = (self.root / "knowledge/methodology/intake/"
                           "PUBLIC-PDF-TEST-APPROVALS-2026-11-22.json")
        self.scope_path.parent.mkdir(parents=True)
        self.catalogue = self.root / "knowledge/methodology/pdf_catalog.json"
        self.source = {
            "path": "knowledge/methodology/pdfs/fictional.pdf",
            "title": "Fictional methodology",
            "authors": "Fictional Author",
            "year": 2026, "doi": "10.1371/journal.pone.1234567",
            "size": len(self.data), "sha256": hashlib.sha256(self.data).hexdigest(),
            "license": "CC BY 4.0", "rights": "PUBLIC_REDISTRIBUTION_REVIEWED",
            "source_url": "https://journals.plos.org/plosone/",
        }
        self.item = {
            "path": self.source["path"], "doi": self.source["doi"],
            "sha256": self.source["sha256"], "size": self.source["size"],
            "license": "CC BY 4.0", "scope": "CC_BY_4_0_ATTRIBUTION_REQUIRED",
            "review_actor": "AI_ASSISTANT_DOCUMENTARY_CHECK",
            "exact_pdf_licence_certified_by_human": False,
            "review_basis": "PLOS_APPLIES_CC_BY4_UNLESS_EXCEPTION_AND_ARTICLE_METADATA_REVIEWED",
            "rights_evidence_url": "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.1234567",
            "publisher_policy_url": "https://journals.plos.org/plosone/s/licenses-and-copyright"
        }
        self.scope = {
            "schema": "MEU_ARTIGO_REVIEWED_PDF_PACKAGE_SCOPE_V1",
            "candidate_use": "TEST_ONLY_NOT_PUBLIC_RELEASE",
            "source_catalogue_path": "knowledge/methodology/pdf_catalog.json",
            "documents": [self.item],
        }
        self._save()

    def _save(self):
        self.catalogue.write_text(json.dumps({
            "schema": "MEU_ARTIGO_PUBLIC_PDF_CATALOG_V1",
            "documents": [self.source]}), encoding="utf-8")
        self.scope_path.write_text(json.dumps(self.scope), encoding="utf-8")

    def test_one_reviewed_original_pdf_accepted_as_test_candidate(self):
        selected, review = select(self.root)
        self.assertEqual(len(selected), 1)
        self.assertIn("Fictional Author", notices(selected).decode())
        self.assertEqual(review["candidate_use"], "TEST_ONLY_NOT_PUBLIC_RELEASE")

    def test_modified_pdf_is_rejected(self):
        self.pdf.write_bytes(b"%PDF-1.4\nmodified")
        with self.assertRaisesRegex(ValueError, "PDF_BYTES_NOT_ORIGINAL"):
            select(self.root)

    def test_non_cc_by4_rejected(self):
        self.item["license"] = "CC BY-NC 4.0"
        self.source["license"] = "CC BY-NC 4.0"
        self._save()
        with self.assertRaisesRegex(ValueError, "PDF_SCOPE_SOURCE_RIGHTS_MISMATCH"):
            select(self.root)

    def test_private_unlisted_source_rejected(self):
        self.item["path"] = "knowledge/methodology/pdfs/other.pdf"
        self._save()
        with self.assertRaisesRegex(ValueError, "UNREVIEWED_OR_DUPLICATE_PDF_PATH"):
            select(self.root)

    def test_claimed_human_review_rejected_in_ai_only_scope(self):
        self.item["exact_pdf_licence_certified_by_human"] = True
        self._save()
        with self.assertRaisesRegex(ValueError, "PDF_SCOPE_SOURCE_RIGHTS_MISMATCH"):
            select(self.root)

    def test_duplicate_review_entries_rejected(self):
        self.scope["documents"].append(dict(self.item))
        self._save()
        with self.assertRaisesRegex(ValueError, "UNREVIEWED_OR_DUPLICATE_PDF_PATH"):
            select(self.root)


if __name__ == "__main__":
    unittest.main()
