"""Ensure provenance of 31 remaining unverified *prospecting-only* source cards.

This test never treats a filename title as proof of source identity or reading.
"""
import json,hashlib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"knowledge"/"methodology"
class ProvisionalTitleTests(unittest.TestCase):
 def test_source_candidates_remain_unverified(self):
  j=json.loads((BASE/"source_registry_catalog.json").read_text(encoding="utf-8"))
  a=[x for x in j["documents"] if x["bibliography_match_status"]=="IDENTITY_UNRESOLVED"]
  self.assertEqual(len(a),31)
  for x in a:
   with self.subTest(x=x["source_id"]):
    self.assertTrue(x["source_metadata_only"])
    self.assertTrue(x["title_candidate_only"])
    raw=(ROOT/x["path"]).read_bytes()
    self.assertEqual(hashlib.sha256(raw).hexdigest(),x["sha256"])
    txt=raw.decode("utf-8")
    self.assertIn("Documento original consultado para esta ficha: NÃO",txt)
    self.assertIn("Não atribuir as propostas acima ao autor",txt)
    self.assertIn("IDENTITY_UNRESOLVED",txt)
 def test_new_editorial_cards_do_not_claim_private_pdf_read(self):
  c=json.loads((BASE/"catalog.json").read_text(encoding="utf-8"))
  self.assertEqual(len(c["documents"]),133)
  matched=[x for x in c["documents"] if x.get("source_registry_id")]
  self.assertEqual(len(matched),45)
  for x in matched:
   raw=(ROOT/x["path"]).read_bytes()
   self.assertEqual(hashlib.sha256(raw).hexdigest(),x["sha256"])
   txt=raw.decode("utf-8")
   self.assertIn("REVISÃO_CIENTÍFICA_INDEPENDENTE_PENDENTE",txt)
   self.assertIn("NÃO",txt)
   self.assertEqual(x["editorial_status"],"DRAFT_NEEDS_INDEPENDENT_REVIEW")
if __name__=="__main__":unittest.main()
