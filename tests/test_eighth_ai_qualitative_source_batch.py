"""Direct-source identity screening for ten AI-assisted qualitative-method works.

This tests bibliographic identity and licence boundaries, NOT source-claim approval
or permission to reproduce additional original archived PDFs.
"""
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "methodology"
IDS = {"SRC-0071", "SRC-0072", "SRC-0074", "SRC-0075", "SRC-0077",
       "SRC-0078", "SRC-0079", "SRC-0080", "SRC-0081", "SRC-0082"}
NONCOMMERCIAL = {"SRC-0077", "SRC-0080"}
CC_BY_CANDIDATES = {"SRC-0079", "SRC-0081"}

class EighthAIQualitativeIdentitiesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((BASE / "source_registry_catalog.json").read_text("utf-8"))
        cls.ledger = json.loads((BASE / "intake" / "rights-ledger-part-01.json").read_text("utf-8"))["records"]
        cls.manifest = json.loads((BASE / "intake" / "rights-ledger-manifest.json").read_text("utf-8"))

    def test_ten_directly_inspected_sources_cannot_be_promoted_to_evidence(self):
        docs = {r["source_id"]: r for r in self.registry["documents"]}
        ledger = {r["id"]: r for r in self.ledger}
        self.assertTrue(IDS.issubset(docs))
        for source_id in IDS:
            with self.subTest(source_id=source_id):
                d = docs[source_id]
                l = ledger[source_id]
                self.assertTrue(d["source_metadata_only"])
                self.assertEqual(d["bibliography_match_status"], "SOURCE_PDF_WORK_VERIFIED")
                self.assertEqual(d["source_read_scope"],
                    "SOURCE_PDF_TEXT_INSPECTED_FOR_IDENTITY_AND_METHOD_NOT_INDEPENDENT_SCIENTIFIC_REVIEW")
                self.assertTrue(d["source_identity_verified_not_citation_grade"])
                self.assertFalse(d["public_work_metadata_screen"]["scientific_card_review_approved"])
                self.assertTrue(d["public_work_metadata_screen"]["original_archive_pdf_read"])
                self.assertFalse(d["public_work_metadata_screen"]["original_archive_pdf_redistribution_authorized"])
                self.assertEqual(d["rights_review"], "NOT_CHECKED")
                self.assertFalse(d["has_original_public_pdf"])
                self.assertIsNone(d["public_pdf_path"])
                self.assertEqual(l["public_distribution"], "NOT_AUTHORIZED_BY_THIS_LEDGER")
                self.assertEqual(l["scientific_review"], "PENDING")
                raw = (ROOT / d["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), d["sha256"])
                self.assertIn("FICHA_DE_PROSPECÇÃO_NÃO_REVISADA", raw.decode("utf-8"))
                self.assertIn("[L]", raw.decode("utf-8"))

    def test_restricted_licenses_and_cc_by_candidates_not_conflated(self):
        docs = {r["source_id"]: r for r in self.registry["documents"]}
        for source_id in NONCOMMERCIAL:
            self.assertIn("NOT_UNRESTRICTED", docs[source_id]["public_work_metadata_screen"]["rights_screen"])
        self.assertEqual(docs["SRC-0071"]["public_work_metadata_screen"]["rights_screen"],
                         "PREPRINT_ALL_RIGHTS_RESERVED")
        for source_id in CC_BY_CANDIDATES:
            self.assertIn("EXACT_COPY_UNCLEARED",
                docs[source_id]["public_work_metadata_screen"]["rights_screen"])
            self.assertFalse(docs[source_id]["has_original_public_pdf"])
        self.assertEqual(docs["SRC-0082"]["work_type"], "JOURNAL_EDITORIAL")
        self.assertEqual(docs["SRC-0075"]["work_type"],
                         "RESEARCH_SURVEY_PAPER_REVIEW_STATUS_UNVERIFIED")

    def test_totals_preserve_rights_and_card_gate(self):
        docs = self.registry["documents"]
        self.assertEqual(len(docs), 475)
        self.assertEqual(sum(x["bibliography_match_status"] == "SOURCE_PDF_WORK_VERIFIED"
                             for x in docs), 132)
        self.assertEqual(sum(x["bibliography_match_status"] == "CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED"
                             for x in docs), 343)
        self.assertEqual(sum(x["source_read_scope"] != "NOT_RECORDED_IN_LEDGER"
                             for x in docs), 134)
        self.assertEqual(self.manifest["source_pdf_work_verified_count"], 132)
        self.assertEqual(self.manifest["provisional_matches_remaining"], 343)
        self.assertEqual(self.manifest["original_archive_text_scoped_read_count"], 134)
        self.assertEqual(self.manifest["source_pdf_count_public_catalogue"], 51)
        self.assertEqual(self.manifest["actual_individually_verified_rights_in_this_ledger"], 17)
        self.assertEqual(self.manifest["original_editorial_cards_count"], 174)

if __name__ == "__main__":
    unittest.main()
