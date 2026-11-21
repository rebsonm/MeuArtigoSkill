"""Ten original archived works inspected only for identity and methods scope.

This test deliberately does not certify rights, complete reading, or academic validity.
"""
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "methodology"
IDS = {"SRC-0003", "SRC-0004", "SRC-0005", "SRC-0017", "SRC-0019",
       "SRC-0020", "SRC-0021", "SRC-0023", "SRC-0024", "SRC-0025"}

class TenWorkIdentityEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((BASE / "source_registry_catalog.json").read_text("utf-8"))
        cls.manifest = json.loads((BASE / "intake" / "rights-ledger-manifest.json").read_text("utf-8"))
        cls.ledger = json.loads((BASE / "intake" / "rights-ledger-part-01.json").read_text("utf-8"))["records"]

    def test_identities_are_directly_inspected_but_not_scientifically_accepted(self):
        rows = {x["source_id"]: x for x in self.registry["documents"]}
        rights = {x["id"]: x for x in self.ledger}
        self.assertTrue(IDS.issubset(rows))
        for key in IDS:
            source = rows[key]
            record = rights[key]
            self.assertTrue(source["source_metadata_only"])
            self.assertEqual(source["bibliography_match_status"], "SOURCE_PDF_WORK_VERIFIED")
            self.assertEqual(source["source_read_scope"],
                             "SOURCE_PDF_TEXT_INSPECTED_FOR_IDENTITY_AND_METHOD_NOT_INDEPENDENT_SCIENTIFIC_REVIEW")
            self.assertTrue(source["source_identity_verified_not_citation_grade"])
            self.assertFalse(source["has_original_public_pdf"])
            self.assertEqual(source["rights_review"], "NOT_CHECKED")
            self.assertEqual(record["rights_review"], "NOT_CHECKED")
            self.assertEqual(record["public_distribution"], "NOT_AUTHORIZED_BY_THIS_LEDGER")
            self.assertEqual(record["original_reading"],
                             "SOURCE_PDF_TEXT_INSPECTED_FOR_IDENTITY_AND_METHOD_NOT_SCIENTIFICALLY_REVIEWED")
            self.assertEqual(record["scientific_review"], "PENDING")
            self.assertFalse(source["public_work_metadata_screen"]["scientific_card_review_approved"])
            self.assertFalse(source["public_work_metadata_screen"]["original_archive_pdf_redistribution_authorized"])
            body = (ROOT / source["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(body).hexdigest(), source["sha256"])
            self.assertIn(b"FICHA_DE_PROSPEC", body)

    def test_aggregate_count_and_rights_separation(self):
        docs = self.registry["documents"]
        self.assertEqual(len(docs), 475)
        self.assertEqual(sum(x["bibliography_match_status"] == "SOURCE_PDF_WORK_VERIFIED"
                             for x in docs), 132)
        self.assertEqual(sum(x["bibliography_match_status"] == "CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED"
                             for x in docs), 343)
        self.assertEqual(self.registry["source_text_read_in_ledger"], 134)
        self.assertEqual(self.manifest["source_pdf_work_verified_count"], 132)
        self.assertEqual(self.manifest["provisional_matches_remaining"], 343)
        self.assertEqual(self.manifest["original_archive_text_scoped_read_count"], 134)
        self.assertEqual(self.manifest["actual_individually_verified_rights_in_this_ledger"], 17)
        self.assertEqual(self.manifest["source_pdf_count_public_catalogue"], 51)
        self.assertEqual(self.manifest["original_editorial_cards_count"], 174)

    def test_caution_for_special_editions_and_rights(self):
        docs = {d["source_id"]: d for d in self.registry["documents"]}
        self.assertIn("HEADER_CONFLICT", docs["SRC-0005"]["public_work_metadata_screen"]["rights_screen"])
        self.assertEqual(docs["SRC-0023"]["public_work_metadata_screen"]["year"], "NOT_VERIFIED")
        self.assertEqual(docs["SRC-0025"]["public_work_metadata_screen"]["rights_screen"],
                         "CC_BY_NC_ND_3_0_NOT_UNRESTRICTED")
        self.assertEqual(docs["SRC-0024"]["public_work_metadata_screen"]["rights_screen"],
                         "TEXT_ONLY_CC_BY_4_THIRD_PARTY_ELEMENTS_RESTRICTED")

if __name__ == "__main__":
    unittest.main()
