"""Prevent a source with non-commercial conditions from entering the unrestricted public corpus."""
from pathlib import Path
import json, hashlib, unittest, sys
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"knowledge"/"methodology"
sys.path.insert(0,str(ROOT/"scripts"))
sys.path.insert(0,str(ROOT/"experimental"/"conceptual_rag"))
import public_method_pdf as installed
import github_pdf_reader as experimental
class NonCommercialRightsBoundary(unittest.TestCase):
 def test_archived_restricted_original_is_not_public_binary(self):
  docs=json.loads((BASE/"source_registry_catalog.json").read_text("utf-8"))["documents"]
  one=next(x for x in docs if x["source_id"]=="SRC-0367")
  self.assertTrue(one["source_metadata_only"])
  self.assertFalse(one["has_original_public_pdf"])
  self.assertEqual(one["rights_review"],"NOT_CHECKED")
  self.assertEqual(one["public_work_metadata_screen"]["restricted_license_observed"],"CC BY-NC 4.0")
  self.assertFalse(one["public_work_metadata_screen"]["original_archive_pdf_redistribution_authorized"])
  self.assertEqual(hashlib.sha256((ROOT/one["path"]).read_bytes()).hexdigest(),one["sha256"])
  self.assertFalse((BASE/"pdfs"/"silva-hernandez-2020-analise-conteudo-politica-externa.pdf").exists())
  ledger=json.loads((BASE/"intake"/"rights-ledger-part-03.json").read_text("utf-8"))["records"]
  row=next(x for x in ledger if x["id"]=="SRC-0367")
  self.assertEqual(row["observed_publisher_license"],"CC BY-NC 4.0")
  self.assertEqual(row["license_restriction"],"NONCOMMERCIAL")
  self.assertEqual(row["public_distribution"],"NOT_AUTHORIZED_BY_THIS_LEDGER")
  self.assertTrue(row["restriction_evidence_url"].startswith("https://www.scielo.br/"))
 def test_all_remaining_public_pdfs_have_unrestricted_licenses(self):
  corpus=(BASE/"pdf_catalog.json").read_bytes()
  for module in (installed,experimental):
   items=module.metadata(corpus)
   self.assertEqual(len(items),55)
   self.assertFalse(any("silva-hernandez-2020" in x["path"] for x in items))
   self.assertTrue(all(x["license"] in ("CC BY","CC BY 4.0") for x in items))
 def test_retriever_rejects_noncommercial_metadata_even_with_rights_flag(self):
  base=json.loads((BASE/"pdf_catalog.json").read_text("utf-8"))
  for module in (installed,experimental):
   for license in ("CC BY-NC 4.0","CC BY-ND 4.0","CC BY-SA 4.0","UNVERIFIED"):
    with self.subTest(module=module.__name__,license=license):
     case=json.loads(json.dumps(base))
     case["documents"][0]["license"]=license
     with self.assertRaisesRegex(ValueError,"PUBLIC_PDF_LICENSE_NOT_UNRESTRICTED"):
      module.metadata(json.dumps(case).encode())
 def test_editorial_card_kept_with_honest_license_warning(self):
  allcards=json.loads((BASE/"catalog.json").read_text("utf-8"))["documents"]
  one=next(x for x in allcards if x.get("source_registry_id")=="SRC-0367")
  b=(ROOT/one["path"]).read_bytes()
  self.assertIn(b"BY-NC",b)
  self.assertEqual(hashlib.sha256(b).hexdigest(),one["sha256"])
  self.assertEqual(one["editorial_status"],"DRAFT_NEEDS_INDEPENDENT_REVIEW")
if __name__=="__main__":unittest.main()
