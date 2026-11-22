"""Original-document identity and copyright boundaries for the ninth 16-work batch.

Source PDF bodies are deliberately not imported into a public distribution. The
checks certify only observed metadata and registry integrity, not scientific claims.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "methodology"
IDS = {f"SRC-{i:04d}" for i in range(83, 99)}
CLEARLY_RESERVED = {"SRC-0088", "SRC-0094"}
PENDING_CC_BY_EXACT_COPY = {"SRC-0084", "SRC-0087", "SRC-0092"}
SPECIAL = {"SRC-0088": "COPYRIGHT_RESTRICTED_MONOGRAPH",
           "SRC-0094": "COPYRIGHT_RESTRICTED_EDITED_BOOK",
           "SRC-0097": "EDITED_BOOK_CHAPTER_RIGHTS_CONFLICT",
           "SRC-0098": "TRANSLATED_BOOK_CHAPTER_IN_JOURNAL"}

class NinthDigitalMethodsSourceWorkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((BASE / "source_registry_catalog.json").read_text("utf-8"))
        cls.ledger = json.loads((BASE / "intake" / "rights-ledger-part-01.json").read_text("utf-8"))["records"]
        cls.manifest = json.loads((BASE / "intake" / "rights-ledger-manifest.json").read_text("utf-8"))

    def test_originals_identified_but_no_public_rights_or_citation_promotion(self):
        docs = {r["source_id"]: r for r in self.registry["documents"]}
        ledger = {r["id"]: r for r in self.ledger}
        self.assertTrue(IDS.issubset(docs))
        for sid in IDS:
            with self.subTest(sid=sid):
                d=docs[sid]
                l=ledger[sid]
                self.assertEqual(d["bibliography_match_status"], "SOURCE_PDF_WORK_VERIFIED")
                self.assertEqual(d["source_read_scope"],
                    "SOURCE_PDF_TEXT_INSPECTED_FOR_IDENTITY_AND_METHOD_NOT_INDEPENDENT_SCIENTIFIC_REVIEW")
                self.assertTrue(d["source_metadata_only"])
                self.assertTrue(d["source_identity_verified_not_citation_grade"])
                self.assertEqual(d["rights_review"], "NOT_CHECKED")
                self.assertFalse(d["has_original_public_pdf"])
                self.assertIsNone(d["public_pdf_path"])
                self.assertFalse(d["public_work_metadata_screen"]["scientific_card_review_approved"])
                self.assertFalse(d["public_work_metadata_screen"]["original_archive_pdf_redistribution_authorized"])
                self.assertTrue(d["public_work_metadata_screen"]["original_archive_pdf_read"])
                self.assertEqual(l["public_distribution"], "NOT_AUTHORIZED_BY_THIS_LEDGER")
                self.assertEqual(l["scientific_review"], "PENDING")
                raw=(ROOT / d["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(),d["sha256"])
                self.assertTrue("FICHA_DE_PROSPECÇÃO_NÃO_REVISADA" in raw.decode("utf-8") or
                                "UNREVIEWED_PROSPECTING_CARD" in raw.decode("utf-8"))
                self.assertIn("[L]",raw.decode("utf-8"))
                self.assertNotIn("drive.google.com/drive/",raw.decode("utf-8").lower())

    def test_reserved_books_conflicting_notices_and_translations(self):
        docs={r["source_id"]:r for r in self.registry["documents"]}
        for sid,kind in SPECIAL.items():
            self.assertEqual(docs[sid]["work_type"],kind)
        for sid in CLEARLY_RESERVED:
            self.assertIn("ALL_RIGHTS_RESERVED",
                docs[sid]["public_work_metadata_screen"]["rights_screen"])
        for sid in PENDING_CC_BY_EXACT_COPY:
            self.assertTrue("EXACT_COPY_NEEDS" in
                docs[sid]["public_work_metadata_screen"]["rights_screen"])
            self.assertFalse(docs[sid]["has_original_public_pdf"])
        self.assertIn("CONFLICTS_WITH_NC_ND",
            docs["SRC-0097"]["public_work_metadata_screen"]["rights_screen"])
        self.assertFalse(docs["SRC-0097"]["has_original_public_pdf"])

    def test_aggregate_inventory_still_excludes_unlicensed_binary(self):
        docs=self.registry["documents"]
        self.assertEqual(len(docs),475)
        self.assertEqual(sum(x["bibliography_match_status"]=="SOURCE_PDF_WORK_VERIFIED"
                             for x in docs),132)
        self.assertEqual(sum(x["bibliography_match_status"]=="CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED"
                             for x in docs),343)
        self.assertEqual(sum(x["source_read_scope"]!="NOT_RECORDED_IN_LEDGER"
                             for x in docs),134)
        self.assertEqual(self.manifest["source_pdf_work_verified_count"],132)
        self.assertEqual(self.manifest["provisional_matches_remaining"],343)
        self.assertEqual(self.manifest["original_archive_text_scoped_read_count"],134)
        self.assertEqual(self.manifest["actual_individually_verified_rights_in_this_ledger"],17)
        self.assertEqual(self.manifest["source_pdf_count_public_catalogue"],51)
        self.assertEqual(self.manifest["original_editorial_cards_count"],174)

if __name__ == "__main__":
    unittest.main()
