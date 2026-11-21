"""Prove seventh direct-PDF batch remains bibliographic and rights-scoped."""
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "methodology"
IDS = {"SRC-0018", "SRC-0022", "SRC-0027", "SRC-0028", "SRC-0029",
       "SRC-0030", "SRC-0031", "SRC-0032", "SRC-0033", "SRC-0034"}
PREVIOUSLY_LICENSED = {"SRC-0018"}

class SeventhSourceIdentityBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((BASE / "source_registry_catalog.json").read_text("utf-8"))
        cls.ledger = json.loads((BASE / "intake" / "rights-ledger-part-01.json").read_text("utf-8"))["records"]
        cls.manifest = json.loads((BASE / "intake" / "rights-ledger-manifest.json").read_text("utf-8"))

    def test_identity_without_primary_citation_upgrade(self):
        docs = {r["source_id"]: r for r in self.registry["documents"]}
        ledger = {r["id"]: r for r in self.ledger}
        self.assertTrue(IDS.issubset(docs))
        for sid in IDS:
            with self.subTest(source_id=sid):
                record = docs[sid]
                rights = ledger[sid]
                self.assertTrue(record["source_metadata_only"])
                self.assertEqual(record["bibliography_match_status"], "SOURCE_PDF_WORK_VERIFIED")
                self.assertTrue(record["source_identity_verified_not_citation_grade"])
                self.assertTrue(record["public_work_metadata_screen"]["original_archive_pdf_read"])
                self.assertFalse(record["public_work_metadata_screen"]["scientific_card_review_approved"])
                self.assertEqual(rights["scientific_review"], "PENDING")
                self.assertEqual(record["rights_review"] == "VERIFIED_PUBLISHER_LICENSE",
                                 sid in PREVIOUSLY_LICENSED)
                self.assertEqual(record["has_original_public_pdf"],
                                 sid in PREVIOUSLY_LICENSED)
                self.assertEqual(record["public_work_metadata_screen"]["original_archive_pdf_redistribution_authorized"],
                                 sid in PREVIOUSLY_LICENSED)
                card = (ROOT / record["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(card).hexdigest(), record["sha256"])
                self.assertIn(b"FICHA_DE_PROSPEC", card)
                if sid not in PREVIOUSLY_LICENSED:
                    self.assertEqual(rights["public_distribution"], "NOT_AUTHORIZED_BY_THIS_LEDGER")
                    self.assertEqual(record["source_read_scope"],
                        "SOURCE_PDF_TEXT_INSPECTED_FOR_IDENTITY_AND_METHOD_NOT_INDEPENDENT_SCIENTIFIC_REVIEW")
                    self.assertIsNone(record["public_pdf_path"])

    def test_counts_preserve_prior_rights(self):
        docs = self.registry["documents"]
        self.assertEqual(len(docs), 475)
        self.assertEqual(sum(d["bibliography_match_status"] == "SOURCE_PDF_WORK_VERIFIED"
                             for d in docs), 132)
        self.assertEqual(sum(d["bibliography_match_status"] == "CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED"
                             for d in docs), 343)
        self.assertEqual(sum(d["source_read_scope"] != "NOT_RECORDED_IN_LEDGER"
                             for d in docs), 134)
        self.assertEqual(self.manifest["source_pdf_work_verified_count"], 132)
        self.assertEqual(self.manifest["provisional_matches_remaining"], 343)
        self.assertEqual(self.manifest["original_archive_text_scoped_read_count"], 134)
        self.assertEqual(self.manifest["actual_individually_verified_rights_in_this_ledger"], 17)
        self.assertEqual(self.manifest["source_pdf_count_public_catalogue"], 51)
        self.assertEqual(self.manifest["original_editorial_cards_count"], 174)

    def test_thesis_book_and_translation_not_misrepresented(self):
        docs = {r["source_id"]: r for r in self.registry["documents"]}
        self.assertEqual(docs["SRC-0022"]["topic"], "Ciência Política e Políticas Educacionais")
        self.assertEqual(docs["SRC-0022"]["work_type"], "MASTER_DISSERTATION")
        self.assertEqual(docs["SRC-0029"]["work_type"], "EDITED_BOOK_CHAPTER")
        self.assertEqual(docs["SRC-0032"]["work_type"], "HANDBOOK_CHAPTER")
        self.assertEqual(docs["SRC-0032"]["public_work_metadata_screen"]["year"], "NOT_VERIFIED")
        self.assertEqual(docs["SRC-0030"]["work_type"], "TRANSLATED_ARTICLE")
        self.assertIn("TRANSLATED_ARTICLE", docs["SRC-0030"]["public_work_metadata_screen"]["rights_screen"])
        self.assertEqual(docs["SRC-0018"]["source_read_scope"], "TITLE_ABSTRACT_AND_METHOD_EXPOSITION_CONSULTED")
        self.assertEqual(docs["SRC-0018"]["rights_review"], "VERIFIED_PUBLISHER_LICENSE")

if __name__ == "__main__":
    unittest.main()
