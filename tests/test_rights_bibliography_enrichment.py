"""Check that bibliography enrichment never approves copyright or source claims."""
import json
from pathlib import Path
import unittest
BASE=Path(__file__).resolve().parents[1]/"knowledge"/"methodology"/"intake"
class BibEnrichmentTest(unittest.TestCase):
    def test_source_metadata_is_not_rights_evidence(self):
        all_records=[]
        for i in range(1,6):
            p=json.loads((BASE/f"rights-ledger-part-0{i}.json").read_text(encoding="utf-8"))
            all_records.extend(p["records"])
        m=json.loads((BASE/"rights-ledger-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(all_records),475)
        self.assertEqual(len([r for r in all_records if r.get("bibliographic_title_original")]),m["matched_bibliographic_titles"])
        self.assertGreaterEqual(m["matched_bibliographic_titles"],370)
        self.assertEqual(m["matched_bibliographic_titles"]+m["ambiguous_bibliographic_matches"]+m["source_records_not_in_spreadsheet"],475)
        independently_reviewed = []
        for row in all_records:
            if row["rights_review"] == "NOT_CHECKED":
                self.assertEqual(row["publisher_license"], "NOT_CHECKED")
                self.assertEqual(row["public_distribution"], "NOT_AUTHORIZED_BY_THIS_LEDGER")
            else:
                self.assertEqual(row["rights_review"], "VERIFIED_PUBLISHER_LICENSE")
                if row["id"] == "SRC-0256":
                    self.assertEqual(row["publisher_license"], "CC BY 3.0 IGO")
                    self.assertIn("LINK_ONLY", row["public_distribution"])
                    self.assertIsNone(row.get("public_pdf_path"))
                    self.assertTrue(row["publisher_download_url"].startswith("https://"))
                else:
                    self.assertIn(row["publisher_license"], ("CC BY 4.0", "CC BY"))
                    self.assertEqual(row["public_distribution"], "LICENSED_ORIGINAL_SOURCE_INDEXED")
                    self.assertTrue(row["public_pdf_path"].startswith("knowledge/methodology/pdfs/"))
                self.assertTrue(row["rights_evidence_url"].startswith("https://"))
                self.assertRegex(row["original_pdf_sha256"], r"^[a-f0-9]{64}$")
                independently_reviewed.append(row)
        self.assertEqual(len(independently_reviewed),
                         m["actual_individually_verified_rights_in_this_ledger"])
        self.assertFalse(m["source_title_matching_guarantees_rights"])
if __name__=="__main__":unittest.main()
