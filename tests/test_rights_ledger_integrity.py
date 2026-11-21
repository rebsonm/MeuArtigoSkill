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
                self.assertEqual(row["rights_review"],"NOT_CHECKED")
                self.assertEqual(row["public_distribution"],"NOT_AUTHORIZED_BY_THIS_LEDGER")
                self.assertEqual(row["publisher_license"],"NOT_CHECKED")
                self.assertNotIn("drive_file_id",row)
                self.assertRegex(row["id"],r"^SRC-[0-9]{4}$")
        self.assertEqual(len(wanted),475)
        self.assertEqual(wanted,actual)
        manifest = json.loads((ROOT / "intake" / "rights-ledger-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(manifest["part_counts"]),475)
        self.assertEqual(manifest["actual_individually_verified_rights_in_this_ledger"],0)
        self.assertFalse(manifest["private_corpus_copied"])
if __name__ == "__main__": unittest.main()
