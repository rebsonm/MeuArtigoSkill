"""The new 14-publication batch is source-specific and does not claim independent review."""
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"knowledge"/"methodology"
IDS={f"SRC-{i}" for i in ("0037","0038","0039","0042","0043","0045","0048","0052","0058","0059","0060","0061","0062","0064")}
ALLOW={f"SRC-{i}" for i in ("0045","0048","0060","0061","0062")}
class NewOriginalBatchTests(unittest.TestCase):
 def test_document_verified_does_not_mean_claim_supported(self):
  reg=json.loads((BASE/"source_registry_catalog.json").read_text("utf-8"))
  docs=[x for x in reg["documents"] if x["source_id"] in IDS]
  self.assertEqual(len(docs),14)
  self.assertEqual(sum(x["bibliography_match_status"]=="SOURCE_PDF_WORK_VERIFIED" for x in reg["documents"]),96)
  self.assertEqual(sum(x["bibliography_match_status"]=="IDENTITY_UNRESOLVED" for x in reg["documents"]),0)
  self.assertEqual(reg["source_text_read_in_ledger"],99)
  for x in docs:
   self.assertTrue(x["source_metadata_only"])
   self.assertTrue(x["source_identity_verified_not_citation_grade"])
   self.assertFalse(x["public_work_metadata_screen"]["scientific_card_review_approved"])
   self.assertEqual(x["rights_review"]=="VERIFIED_PUBLISHER_LICENSE",x["source_id"] in ALLOW)
   self.assertEqual(hashlib.sha256((ROOT/x["path"]).read_bytes()).hexdigest(),x["sha256"])
 def test_public_license_and_byte_hash_of_five_originals(self):
  cat=json.loads((BASE/"pdf_catalog.json").read_text("utf-8"))["documents"]
  self.assertEqual(len(cat),51)
  target={"10.1177/16094069251383739","10.1007/s11135-025-02165-z","10.3389/frma.2025.1685968","10.1371/journal.pone.0330217","10.2196/64447"}
  got=[x for x in cat if x.get("doi") in target]
  self.assertEqual(len(got),5)
  for x in got:
   b=(ROOT/x["path"]).read_bytes()
   self.assertEqual(x["license"],"CC BY 4.0")
   self.assertTrue(b.startswith(b"%PDF"))
   self.assertEqual(len(b),x["size"])
   self.assertEqual(hashlib.sha256(b).hexdigest(),x["sha256"])
   self.assertTrue(x["rights_evidence"].startswith("https://"))
  excluded={"10.1177/16094069261426100","10.1177/16094069251337870","10.1177/16094069251404329","10.1177/20539517251381697"}
  self.assertFalse(excluded.intersection(x.get("doi") for x in cat))
 def test_all_fourteen_original_method_cards_remain_unapproved(self):
  a=json.loads((BASE/"catalog.json").read_text("utf-8"))["documents"]
  self.assertEqual(len(a),174)
  sub=[x for x in a if x.get("source_registry_id") in IDS]
  self.assertEqual(len(sub),14)
  for x in sub:
   body=(ROOT/x["path"]).read_bytes()
   self.assertEqual(hashlib.sha256(body).hexdigest(),x["sha256"])
   self.assertIn("REVISÃO_CIENTÍFICA_INDEPENDENTE_PENDENTE",body.decode("utf-8"))
   self.assertEqual(x["editorial_status"],"DRAFT_NEEDS_INDEPENDENT_REVIEW")
if __name__=="__main__":unittest.main()
