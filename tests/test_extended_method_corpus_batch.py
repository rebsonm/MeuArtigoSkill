"""Verify 19 additional source-specific cards, two binary licenses, and book link-only rule."""
from pathlib import Path
import json,hashlib,unittest
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"knowledge"/"methodology"
IDS={f"SRC-{i}" for i in ("0044","0046","0047","0051","0053","0056","0057","0065","0066","0067","0068","0070","0073","0076","0255","0256","0258","0269","0373")}
PUBLIC={"SRC-0051","SRC-0073"}
LINK_ONLY="SRC-0256"
class ExtendedMethodsRegression(unittest.TestCase):
 def test_direct_source_identity_and_unresolved_caution(self):
  reg=json.loads((BASE/"source_registry_catalog.json").read_text("utf-8"))
  docs=reg["documents"]
  self.assertEqual(len(docs),475)
  self.assertEqual(len([x for x in docs if x["bibliography_match_status"]=="SOURCE_PDF_WORK_VERIFIED"]),132)
  self.assertEqual(len([x for x in docs if x["bibliography_match_status"]=="IDENTITY_UNRESOLVED"]),0)
  self.assertEqual(reg["source_text_read_in_ledger"],134)
  self.assertEqual(len([x for x in docs if x["bibliography_match_status"]=="CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED"]),343)
  observed=[x for x in docs if x["source_id"] in IDS]
  self.assertEqual(len(observed),19)
  for doc in observed:
   self.assertTrue(doc["source_metadata_only"])
   self.assertFalse(doc["public_work_metadata_screen"]["scientific_card_review_approved"])
   self.assertEqual(doc["rights_review"]=="VERIFIED_PUBLISHER_LICENSE",doc["source_id"] in PUBLIC|{LINK_ONLY})
   self.assertEqual(doc["has_original_public_pdf"],doc["source_id"] in PUBLIC)
   self.assertEqual(hashlib.sha256((ROOT/doc["path"]).read_bytes()).hexdigest(),doc["sha256"])
  closa=next(x for x in docs if x["source_id"]=="SRC-0154")
  self.assertEqual(closa["bibliography_match_status"],"SOURCE_PDF_WORK_VERIFIED")
  self.assertIn("Carlos Closa",closa["public_work_metadata_screen"]["authors"])
 def test_exact_open_pdf_copies_are_indexed_not_other_licenses(self):
  c=json.loads((BASE/"pdf_catalog.json").read_text("utf-8"))["documents"]
  self.assertEqual(len(c),55)
  paths={"knowledge/methodology/pdfs/messner-smith-richards-2025-epistemological-incongruences.pdf","knowledge/methodology/pdfs/eschrich-sterman-2024-llm-qualitative-framework-arxiv-v1.pdf"}
  for row in (x for x in c if x["path"] in paths):
   data=(ROOT/row["path"]).read_bytes()
   self.assertTrue(data.startswith(b"%PDF"))
   self.assertEqual(row["license"],"CC BY 4.0")
   self.assertEqual(len(data),row["size"])
   self.assertEqual(hashlib.sha256(data).hexdigest(),row["sha256"])
   paths.remove(row["path"])
  self.assertFalse(paths)
  self.assertFalse(any("gertler" in x["path"].lower() or "card-krueger" in x["path"] or "wiley" in x["path"] for x in c))
 def test_book_license_verified_but_pdf_not_uploaded(self):
  m=json.loads((BASE/"intake"/"rights-ledger-manifest.json").read_text("utf-8"))
  self.assertEqual(m["actual_individually_verified_rights_in_this_ledger"],17)
  self.assertEqual(m["source_pdf_count_public_catalogue"],55)
  self.assertEqual(m["original_editorial_cards_count"],174)
  ledger=[]
  for i in range(1,6):
   ledger.extend(json.loads((BASE/"intake"/f"rights-ledger-part-0{i}.json").read_text("utf-8"))["records"])
  book=next(x for x in ledger if x["id"]=="SRC-0256")
  self.assertEqual(book["publisher_license"],"CC BY 3.0 IGO")
  self.assertIn("LINK_ONLY",book["public_distribution"])
  self.assertTrue(book["publisher_download_url"].startswith("https://"))
  self.assertEqual(len([x for x in ledger if x["rights_review"]=="VERIFIED_PUBLISHER_LICENSE"]),17)
 def test_method_cards_are_original_and_science_unapproved(self):
  cat=json.loads((BASE/"catalog.json").read_text("utf-8"))["documents"]
  sub=[x for x in cat if x.get("source_registry_id") in IDS]
  self.assertEqual(len(cat),174)
  self.assertEqual(len(sub),19)
  for x in sub:
   b=(ROOT/x["path"]).read_bytes()
   self.assertEqual(hashlib.sha256(b).hexdigest(),x["sha256"])
   self.assertEqual(x["editorial_status"],"DRAFT_NEEDS_INDEPENDENT_REVIEW")
   self.assertIn(b"REVIS",b)
if __name__=="__main__":unittest.main()
