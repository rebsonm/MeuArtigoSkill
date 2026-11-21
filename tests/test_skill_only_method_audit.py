"""Safety contract for the Skill-only methodology route and 12 metadata matches."""
import hashlib,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"knowledge"/"methodology"
class SkillOnlyMethodAuditTests(unittest.TestCase):
 def test_verified_archive_work_identities_do_not_approve_science(self):
  audit=json.loads((BASE/"intake"/"PUBLIC-WORK-BIBLIOGRAPHY-AUDIT-12.json").read_text("utf-8"))
  register=json.loads((BASE/"source_registry_catalog.json").read_text("utf-8"))
  self.assertEqual(audit["count"],12)
  self.assertEqual(register["public_bibliographic_work_checks"],12)
  self.assertEqual(len(register["documents"]),475)
  self.assertEqual(sum(x["bibliography_match_status"]=="IDENTITY_UNRESOLVED" for x in register["documents"]),50)
  for item in audit["rows"]:
   self.assertRegex(item["doi"],r"^10\.[0-9]{4,9}/")
   self.assertTrue(item["public_locator"].startswith("https://"))
   self.assertTrue(item["archive_pdf_identity_confirmed"])
   self.assertTrue(item["archive_pdf_text_read"])
   self.assertEqual(item["rights_to_redistribute_archive_pdf"],item["source_registry_id"] in {"SRC-0049","SRC-0069"})
   self.assertFalse(item["independent_scientific_card_approval"])
   doc=next(x for x in register["documents"] if x["source_id"]==item["source_registry_id"])
   self.assertEqual(doc["public_work_metadata_screen"]["doi"],item["doi"])
   self.assertTrue(doc["source_metadata_only"])
   self.assertTrue(doc["public_work_metadata_screen"]["original_archive_pdf_read"])
   self.assertEqual(doc["public_work_metadata_screen"]["original_archive_pdf_redistribution_authorized"],item["source_registry_id"] in {"SRC-0049","SRC-0069"})
 def test_skill_routing_no_server_or_auto_gate(self):
  skill=(ROOT/"SKILL.md").read_text("utf-8")
  doc=(ROOT/"references"/"METHODOLOGY-CONSULTATION-SKILL-ONLY.md").read_text("utf-8")
  self.assertIn("METHODOLOGY-CONSULTATION-SKILL-ONLY.md",skill)
  self.assertIn("SKILL_ONLY_NO_SERVER_REQUIRED",doc)
  self.assertIn("If Python/HTTPS is unavailable",doc)
  self.assertIn("Do not approve gates",doc)
  self.assertIn("not a remotely hosted service",doc)
 def test_corrected_cards_match_manifest_hashes(self):
  j=json.loads((BASE/"catalog.json").read_text("utf-8"))
  self.assertEqual(len(j["documents"]),114)
  names=("institutional-grammar-2-2021-encoding-design.md","prahl-2025-ai-reflexivity-checklist.md")
  for doc in j["documents"]:
   if Path(doc["path"]).name in names:
    b=(ROOT/doc["path"]).read_bytes()
    self.assertEqual(hashlib.sha256(b).hexdigest(),doc["sha256"])
    self.assertEqual(doc["editorial_status"],"DRAFT_NEEDS_INDEPENDENT_REVIEW")
if __name__=="__main__":unittest.main()
