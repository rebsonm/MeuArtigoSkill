"""Every source-archive PDF has a neutral rights ledger entry; none is pre-cleared."""
from pathlib import Path
import json
import unittest
ROOT = Path(__file__).resolve().parents[1] / "knowledge" / "methodology"
class RightsLedgerTests(unittest.TestCase):
    def test_all_original_inventory_records_have_one_neutral_entry(self):
        wanted = []
        actual = []
        for i in range(1,6):
            src = json.loads((ROOT / "inventory" / f"drive-source-candidates-part-0{i}.json").read_text(encoding="utf-8"))
            for f in src["folders"]:
                for e in f["entries"]:
                    if e["kind"] == "PDF":
                        wanted.append((f["folder"],e["filename"]))
            part = json.loads((ROOT / "intake" / f"rights-ledger-part-0{i}.json").read_text(encoding="utf-8"))
            self.assertEqual(part["status"],"UNREVIEWED_ITEMS_NOT_PUBLICATION_APPROVAL")
            for row in part["records"]:
                actual.append((row["folder"],row["filename"]))
                if row["rights_review"] == "NOT_CHECKED":
                    self.assertEqual(row["public_distribution"], "NOT_AUTHORIZED_BY_THIS_LEDGER")
                    self.assertEqual(row["publisher_license"], "NOT_CHECKED")
                elif row["rights_review"] == "VERIFIED_PUBLISHER_LICENSE":
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
                    self.assertRegex(row["original_pdf_sha256"], r"^[0-9a-f]{64}$")
                else:
                    self.fail("Unexpected unreviewed file promoted to rights approval")
                self.assertNotIn("drive_file_id",row)
                self.assertRegex(row["id"],r"^SRC-[0-9]{4}$")
        self.assertEqual(len(wanted),475)
        self.assertEqual(wanted,actual)
        manifest = json.loads((ROOT / "intake" / "rights-ledger-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(manifest["part_counts"]),475)
        self.assertEqual(manifest["actual_individually_verified_rights_in_this_ledger"],
                         sum(1 for i in range(1,6) for row in
                             json.loads((ROOT / "intake" / f"rights-ledger-part-0{i}.json").read_text(encoding="utf-8"))["records"]
                             if row["rights_review"] == "VERIFIED_PUBLISHER_LICENSE"))
        self.assertFalse(manifest["private_corpus_copied"])
if __name__ == "__main__": unittest.main()
