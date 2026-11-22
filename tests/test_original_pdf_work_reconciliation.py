"""Batched reconciliation of twelve directly identified PDF works (no automatic scientific gate)."""
from pathlib import Path
import hashlib,json,unittest
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"knowledge"/"methodology"
IDS={"SRC-0001","SRC-0002","SRC-0016","SRC-0026","SRC-0035","SRC-0041","SRC-0049","SRC-0050","SRC-0054","SRC-0055","SRC-0063","SRC-0069"}
PUBLIC={"SRC-0049","SRC-0069"}
class ReconciledSourceTests(unittest.TestCase):
 def test_source_provenance_and_identity_counts(self):
  o=json.loads((BASE/"source_registry_catalog.json").read_text("utf-8"))
  docs=o["documents"]
  verified=[x for x in docs if x["bibliography_match_status"]=="SOURCE_PDF_WORK_VERIFIED"]
  self.assertTrue(IDS.issubset({x["source_id"] for x in verified}))
  self.assertEqual(len(docs),475)
  self.assertEqual(o["source_text_read_in_ledger"],134)
  self.assertEqual(len([x for x in docs if x["bibliography_match_status"]=="IDENTITY_UNRESOLVED"]),0)
  self.assertEqual(len([x for x in docs if x["bibliography_match_status"]=="CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED"]),343)
  for d in (x for x in verified if x["source_id"] in IDS):
   self.assertTrue(d["source_metadata_only"])
   self.assertFalse(d["public_work_metadata_screen"]["scientific_card_review_approved"])
   self.assertEqual(d["has_original_public_pdf"], d["source_id"] in PUBLIC)
   self.assertEqual(hashlib.sha256((ROOT/d["path"]).read_bytes()).hexdigest(),d["sha256"])
 def test_two_individually_licensed_pdfs_with_exact_bytes(self):
  j=json.loads((BASE/"pdf_catalog.json").read_text("utf-8"))
  self.assertEqual(len(j["documents"]),55)
  added=[d for d in j["documents"] if "schroeder-lequere" in d["path"] or "mayring-2025-chatgpt" in d["path"]]
  self.assertEqual(len(added),2)
  for d in added:
   raw=(ROOT/d["path"]).read_bytes()
   self.assertTrue(raw.startswith(b"%PDF"))
   self.assertEqual(len(raw),d["size"])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),d["sha256"])
   self.assertEqual(d["license"],"CC BY 4.0")
   self.assertTrue(d["rights_evidence"].startswith("https://"))
  self.assertFalse(any("lazar" in d["path"] or "hayes" in d["path"] for d in j["documents"]))
 def test_editorial_cards_remain_unapproved(self):
  j=json.loads((BASE/"catalog.json").read_text("utf-8"))
  cards=[x for x in j["documents"] if x.get("source_registry_id") in IDS]
  self.assertEqual(len(cards),12)
  for c in cards:
   self.assertEqual(c["editorial_status"],"DRAFT_NEEDS_INDEPENDENT_REVIEW")
   self.assertEqual(hashlib.sha256((ROOT/c["path"]).read_bytes()).hexdigest(),c["sha256"])
if __name__=="__main__":unittest.main()
