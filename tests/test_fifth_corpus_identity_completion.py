"""Fifth library batch: work identity, legal scope and digest checks, not scientific approval."""
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"knowledge"/"methodology"
NEW={f"SRC-{n}" for n in ("0006","0011","0036","0040","0132","0154","0158","0181","0182","0184","0199","0205","0206","0239","0240","0242","0259","0267","0268","0270","0273","0274","0298","0310","0337","0353","0358","0367","0397","0401","0410")}
LICENSED={f"SRC-{n}" for n in ("0132","0184","0240","0397")}
class AllFormerlyUnresolvedWorkIdentities(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.registry=json.loads((BASE/"source_registry_catalog.json").read_text("utf-8"))
  cls.cards=json.loads((BASE/"catalog.json").read_text("utf-8"))["documents"]
  cls.pdfs=json.loads((BASE/"pdf_catalog.json").read_text("utf-8"))["documents"]
  cls.ledger=sum((json.loads((BASE/"intake"/f"rights-ledger-part-0{i}.json").read_text("utf-8"))["records"] for i in range(1,6)),[])
 def test_unresolved_zero_is_identity_only(self):
  docs=self.registry["documents"]; ids={d["source_id"] for d in docs}
  self.assertEqual(len(docs),475)
  self.assertTrue(NEW.issubset(ids))
  by_id={x["source_id"]:x for x in docs}
  self.assertEqual(by_id["SRC-0367"]["public_work_metadata_screen"]["restricted_license_observed"],"CC BY-NC 4.0")
  self.assertEqual(sum(x["bibliography_match_status"]=="SOURCE_PDF_WORK_VERIFIED" for x in docs),116)
  self.assertEqual(sum(x["bibliography_match_status"]=="IDENTITY_UNRESOLVED" for x in docs),0)
  self.assertEqual(sum(x["bibliography_match_status"]=="CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED" for x in docs),359)
  self.assertEqual(self.registry["source_text_read_in_ledger"],118)
  for row in docs:
   if row["source_id"] not in NEW: continue
   self.assertTrue(row["source_metadata_only"])
   self.assertTrue(row["source_identity_verified_not_citation_grade"])
   self.assertFalse(row["public_work_metadata_screen"]["scientific_card_review_approved"])
   self.assertEqual(row["has_original_public_pdf"],row["source_id"] in LICENSED)
   self.assertEqual(row["rights_review"]=="VERIFIED_PUBLISHER_LICENSE",row["source_id"] in LICENSED)
   body=(ROOT/row["path"]).read_bytes()
   self.assertEqual(hashlib.sha256(body).hexdigest(),row["sha256"])
   self.assertIn("FICHA_DE_PROSPECÇÃO_NÃO_REVISADA",body.decode("utf-8"))
 def test_archived_sources_do_not_inherit_scholarship_approval(self):
  self.assertEqual(len(self.cards),174)
  new=[x for x in self.cards if x.get("source_registry_id") in NEW]
  self.assertEqual(len(new),31)
  for row in new:
   self.assertEqual(row["editorial_status"],"DRAFT_NEEDS_INDEPENDENT_REVIEW")
   raw=(ROOT/row["path"]).read_bytes()
   self.assertEqual(hashlib.sha256(raw).hexdigest(),row["sha256"])
   self.assertIn("REVISÃO_CIENTÍFICA_INDEPENDENTE_PENDENTE",raw.decode("utf-8"))
 def test_five_exact_redistributable_pdfs_and_binary_copyright_isolation(self):
  self.assertEqual(len(self.pdfs),51)
  reg={x["source_id"]:x for x in self.registry["documents"]}
  pub=[x for x in self.pdfs if x["path"] in {reg[s]["public_pdf_path"] for s in LICENSED}]
  self.assertEqual(len(pub),4)
  for x in pub:
   b=(ROOT/x["path"]).read_bytes()
   self.assertTrue(b.startswith(b"%PDF-"))
   self.assertEqual(len(b),x["size"])
   self.assertEqual(hashlib.sha256(b).hexdigest(),x["sha256"])
   self.assertIn(x["license"],("CC BY","CC BY 4.0"))
   self.assertTrue(x["rights_evidence"].startswith("https://"))
  self.assertEqual(len([x for x in self.ledger if x["rights_review"]=="VERIFIED_PUBLISHER_LICENSE"]),17)
  self.assertFalse(any("longino" in p["path"].lower() or "bonate" in p["path"].lower() or "quevedo" in p["path"].lower() for p in self.pdfs))
 def test_edition_corrections_duplicate_and_publisher_source_limit(self):
  reg={x["source_id"]:x for x in self.registry["documents"]}
  self.assertIn("2004",reg["SRC-0242"]["public_work_metadata_screen"]["year"])
  self.assertIn("2001",reg["SRC-0298"]["public_work_metadata_screen"]["year"])
  self.assertEqual(reg["SRC-0337"]["work_duplicate_of"],"SRC-0206")
  self.assertEqual(reg["SRC-0337"]["public_work_metadata_screen"]["doi"],reg["SRC-0206"]["public_work_metadata_screen"]["doi"])
  self.assertFalse(reg["SRC-0154"]["public_work_metadata_screen"]["original_archive_pdf_version_verified"])
  self.assertTrue(reg["SRC-0154"]["public_work_metadata_screen"]["publisher_version_uncertain"])
  self.assertEqual(reg["SRC-0036"]["source_read_scope"],"SOURCE_PDF_TITLE_PAGE_VISUALLY_INSPECTED_NOT_SCIENTIFICALLY_REVIEWED")
if __name__=="__main__":unittest.main()
