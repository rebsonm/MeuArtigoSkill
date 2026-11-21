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
        for row in all_records:
            self.assertEqual(row["rights_review"],"NOT_CHECKED")
            self.assertEqual(row["publisher_license"],"NOT_CHECKED")
            self.assertEqual(row["public_distribution"],"NOT_AUTHORIZED_BY_THIS_LEDGER")
        self.assertFalse(m["source_title_matching_guarantees_rights"])
if __name__=="__main__":unittest.main()
