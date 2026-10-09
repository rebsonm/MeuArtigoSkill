"""Deterministic RT-10 disclosure tests; fixtures are not real authors or journals."""
import csv,hashlib,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import editorial_ai_disclosure as ed
class EditorialAITests(unittest.TestCase):
 def setUp(self):
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
  self.root=Path(tmp.name);(self.root/ed.MGMT).mkdir(parents=True)
  (self.root/ed.PROFILE).parent.mkdir(parents=True)
  self.fields=["AI_Use_ID","Platform_or_tool","Model_or_version","Purpose","Materiality",
   "Accepted_modified_or_rejected","Human_review_method","Disclosure_required",
   "Disclosure_category","Human_review_evidence","Confidentiality_review"]
  self.event={"AI_Use_ID":"AIUSE-0001","Platform_or_tool":"Software test model",
   "Model_or_version":"fixture-v1","Purpose":"Assisted classification of an example literature record",
   "Materiality":"SUBSTANTIVE","Accepted_modified_or_rejected":"MODIFIED",
   "Human_review_method":"Researcher compared suggestions against original literature",
   "Disclosure_required":"YES","Disclosure_category":"LITERATURE_SEARCH",
   "Human_review_evidence":"message:test-researcher-reviewed-event",
   "Confidentiality_review":"CLEARED"}
  self.make_log([self.event])
  self.profile={"status":"VERIFIED","official_rules_verified":True,"journal_name":"Fixture Journal",
   "ai_disclosure_policy":{"status":"VERIFIED","source":"https://example.org/journal-ai-policy",
   "verified_at":"2026-10-09","statement_location":"DECLARATIONS",
   "category_rules":{"LITERATURE_SEARCH":"ALLOWED"}}}
  self.confirm();self.save_profile()
 def make_log(self,events):
  with (self.root/ed.AI).open("w",encoding="utf-8-sig",newline="") as f:
   w=csv.DictWriter(f,fieldnames=self.fields);w.writeheader();w.writerows(events)
 def confirm(self):
  self.profile["ai_disclosure_attestation"]={"status":"CONFIRMED",
   "reviewed_by":"Fixture researcher","reviewed_at":"2026-10-09",
   "evidence_ref":"message:test-researcher-confirmed-history",
   "ai_log_sha256":ed.checksum(self.root/ed.AI)}
 def save_profile(self):
  (self.root/ed.PROFILE).write_text(json.dumps(self.profile))
 def command(self,cmd):
  return subprocess.run([sys.executable,str(ROOT/"scripts/editorial_ai_disclosure.py"),
   cmd,str(self.root)],capture_output=True,text=True)
 def test_ready_requires_verified_policy_and_full_log_review(self):
  a=ed.assess(self.root);self.assertFalse(a["errors"]);self.assertEqual(a["status"],"READY_FOR_PLACEMENT_REVIEW")
 def test_draft_is_not_release_certificate(self):
  self.profile["ai_disclosure_policy"]["status"]="PENDING";self.save_profile()
  r=self.command("draft");self.assertEqual(r.returncode,2)
  self.assertTrue((self.root/ed.DRAFT).is_file())
  self.assertFalse((self.root/ed.FINAL).exists())
 def test_missing_journal_specific_category_blocks(self):
  self.profile["ai_disclosure_policy"]["category_rules"]={};self.save_profile()
  self.assertTrue(ed.assess(self.root)["errors"])
 def test_editorial_review_is_not_automatic_permission(self):
  self.profile["ai_disclosure_policy"]["category_rules"]["LITERATURE_SEARCH"]="EDITORIAL_REVIEW";self.save_profile()
  self.assertTrue(ed.assess(self.root)["errors"])
 def test_ai_use_marked_no_cannot_hide_record(self):
  event=dict(self.event);event["Disclosure_required"]="NO";self.make_log([event]);self.confirm();self.save_profile()
  r=ed.assess(self.root);self.assertEqual(r["count"],1)
  self.assertTrue(any("override" in x for x in r["warnings"]))
 def test_substantive_use_requires_real_human_review(self):
  event=dict(self.event);event["Human_review_method"]="";self.make_log([event]);self.confirm();self.save_profile()
  self.assertTrue(any("review evidence" in x for x in ed.assess(self.root)["errors"]))
 def test_sensitive_use_unreviewed_blocks(self):
  event=dict(self.event);event["Confidentiality_review"]="UNKNOWN";self.make_log([event]);self.confirm();self.save_profile()
  self.assertTrue(any("confidentiality" in x for x in ed.assess(self.root)["errors"]))
 def test_no_events_no_automatic_declaration(self):
  self.make_log([]);self.save_profile()
  self.assertTrue(ed.assess(self.root)["errors"])
 def test_final_has_hash_bound_audit(self):
  r=self.command("final");self.assertEqual(r.returncode,0,r.stderr)
  self.assertEqual(ed.verify_final(self.root),[])
  report=json.loads((self.root/ed.AUDIT).read_text())
  self.assertEqual(report["final_sha256"],ed.checksum(self.root/ed.FINAL))
 def test_ai_log_changed_invalidates_final(self):
  self.assertEqual(self.command("final").returncode,0)
  event=dict(self.event);event["Purpose"]="Different research activity was recorded after final approval"
  self.make_log([event])
  self.assertTrue(ed.verify_final(self.root))
 def test_journal_policy_changed_invalidates_final(self):
  self.assertEqual(self.command("final").returncode,0)
  self.profile["ai_disclosure_policy"]["statement_location"]="METHODS";self.save_profile()
  self.assertTrue(ed.verify_final(self.root))
 def test_final_text_changed_invalidates_audit(self):
  self.assertEqual(self.command("final").returncode,0)
  with (self.root/ed.FINAL).open("a") as f:f.write("Changed after review")
  self.assertTrue(ed.verify_final(self.root))
 def test_final_never_invents_undocumented_tools(self):
  self.assertEqual(self.command("final").returncode,0)
  txt=(self.root/ed.FINAL).read_text()
  self.assertIn("Software test model",txt)
  self.assertNotIn("Crossref",txt)
 def test_empty_log_needs_author_attestation(self):
  self.make_log([]);self.confirm();self.save_profile()
  r=ed.assess(self.root);self.assertFalse(r["errors"])
  self.assertIn("nenhum uso foi declarado",ed.render(r))
 def test_journal_can_require_model_version(self):
  event=dict(self.event);event["Model_or_version"]=""
  self.make_log([event]);self.confirm()
  self.profile["ai_disclosure_policy"]["require_model_version"]=True
  self.save_profile();self.assertTrue(ed.assess(self.root)["errors"])
 def test_no_final_if_attestation_is_stale(self):
  event=dict(self.event);event["Purpose"]="Updated purpose requires a fresh confirmation"
  self.make_log([event]);self.save_profile()
  self.assertIn("NOT_READY",ed.assess(self.root)["status"])
 def test_gate7_rejects_missing_disclosure(self):
  import governance_events as gov
  p=self.root/ed.MGMT/"PROJECT_CONFIG.json"
  p.write_text(json.dumps({"editorial_ai_disclosure_required":True}))
  g=self.root/ed.MGMT/"18_Human_Validation_Gates.csv"
  with g.open("w",newline="") as f:
   w=csv.DictWriter(f,fieldnames=gov.GATE_HEADERS);w.writeheader()
   w.writerow({"GATE_ID":"GATE-0007","Status":"READY","Name":"Submission"})
  cmd=[sys.executable,str(ROOT/"scripts/governance_events.py"),"gate",
   str(self.root),"--gate-id","GATE-0007","--decision","APPROVED",
   "--validated-by","Researcher","--evidence","message:researcher-review",
   "--method","Researcher editorial review","--no-snapshot"]
  r=subprocess.run(cmd,capture_output=True,text=True)
  self.assertNotEqual(r.returncode,0)
  self.assertIn("not ready",r.stderr)
if __name__=="__main__": unittest.main()
