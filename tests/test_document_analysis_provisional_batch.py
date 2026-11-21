"""Verify the ten document-specific prospecting records and editorial guidance cards."""
from pathlib import Path
import hashlib,json,unittest
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"knowledge"/"methodology"
IDS={f"SRC-{i}" for i in ("0007","0008","0009","0010","0012","0013","0014","0015","0146","0149")}
class TenDocumentProspects(unittest.TestCase):
 def test_original_exemplar_identity_instead_of_filename_guess(self):
  idx=json.loads((BASE/"source_registry_catalog.json").read_text("utf-8"));ds=idx["documents"]
  self.assertEqual(len(ds),475)
  self.assertEqual(sum(x["bibliography_match_status"]=="SOURCE_PDF_WORK_VERIFIED" for x in ds),96)
  self.assertEqual(sum(x["bibliography_match_status"]=="CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED" for x in ds),379)
  self.assertEqual(idx["source_text_read_in_ledger"],99)
  picked=[x for x in ds if x["source_id"] in IDS]
  self.assertEqual(len(picked),10)
  for x in picked:
   self.assertTrue(x["source_metadata_only"])
   self.assertFalse(x["public_work_metadata_screen"]["scientific_card_review_approved"])
   self.assertFalse(x["has_original_public_pdf"])
   self.assertEqual(x["rights_review"],"NOT_CHECKED")
   self.assertEqual(hashlib.sha256((ROOT/x["path"]).read_bytes()).hexdigest(),x["sha256"])
  alt=next(x for x in picked if x["source_id"]=="SRC-0007")
  self.assertFalse(alt["public_work_metadata_screen"]["original_archive_pdf_version_verified"])
 def test_editorial_notes_are_original_not_scientific_approved(self):
  c=json.loads((BASE/"catalog.json").read_text("utf-8"))["documents"]
  self.assertEqual(len(c),174)
  selected=[x for x in c if x.get("source_registry_id") in IDS]
  self.assertEqual(len(selected),10)
  for x in selected:
   s=(ROOT/x["path"]).read_bytes()
   self.assertIn("REVISÃO_CIENTÍFICA_INDEPENDENTE_PENDENTE",s.decode("utf-8"))
   self.assertEqual(hashlib.sha256(s).hexdigest(),x["sha256"])
   self.assertEqual(x["editorial_status"],"DRAFT_NEEDS_INDEPENDENT_REVIEW")
 def test_noncommercial_sources_and_scielo_book_not_uploaded(self):
  pdf=json.loads((BASE/"pdf_catalog.json").read_text("utf-8"))["documents"]
  self.assertEqual(len(pdf),51)
  self.assertFalse(any("fujita" in x["path"] or "morgan-2022" in x["path"] or "oconnor" in x["path"] for x in pdf))
  l=json.loads((BASE/"intake"/"rights-ledger-part-01.json").read_text("utf-8"))["records"]
  for sid,notice in (("SRC-0009","CC_BY_NC_SA_4"),("SRC-0146","CC_BY_NC_4")):
   row=next(x for x in l if x["id"]==sid)
   self.assertEqual(row["observed_license_conditions"],notice)
   self.assertEqual(row["rights_review"],"NOT_CHECKED")
if __name__=="__main__":unittest.main()
