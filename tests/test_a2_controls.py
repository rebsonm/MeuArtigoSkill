"""RT closure checks. All projects, claims and people here are test fixtures."""
import csv,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import presentation_mode as pm
import claim_integrity as ci
import editorial_ai_disclosure as ed

class PresentationModeTests(unittest.TestCase):
 def setUp(self):
  obj=tempfile.TemporaryDirectory();self.addCleanup(obj.cleanup)
  self.root=Path(obj.name);(self.root/pm.MGMT).mkdir()
  (self.root/pm.CONFIG).write_text(json.dumps({"source_verification_required":True,
   "formative_gates_required":True,"presentation_mode":"MINIMAL"}),encoding="utf-8")
  self.write(pm.STAGES,["GATE_ID","Name","Status","Decision"],
             [{"GATE_ID":"GATE-0006","Name":"Claims","Status":"PENDING","Decision":""}])
  self.write(pm.TASKS,["CADA_ID","Next_action","Status"],
             [{"CADA_ID":"CADA-0001","Next_action":"Review actual source","Status":"PENDING"}])
  self.write(pm.CLAIMS,["Claim_ID","Claim_text"],[])
 def write(self,path,headers,rows):
  with (self.root/path).open("w",newline="",encoding="utf-8") as f:
   writer=csv.DictWriter(f,fieldnames=headers);writer.writeheader();writer.writerows(rows)
 def test_minimal_presentation_preserves_pending_science(self):
  r=pm.view(self.root)
  self.assertEqual(r["mode"],"MINIMAL")
  self.assertEqual(r["scientific_gates_pending"],1)
  self.assertEqual(r["next_scientific_decision"]["gate_id"],"GATE-0006")
  self.assertFalse(r["empirical_effect_proven"])
 def test_toggle_changes_only_config_and_not_scientific_logs(self):
  files=[pm.STAGES,pm.TASKS,pm.CLAIMS]
  old={n:(self.root/n).read_bytes() for n in files}
  r=pm.set_mode(self.root,"FULL","message:fixture-reviewer-decision")
  self.assertEqual(r["mode"],"FULL")
  self.assertEqual(r["scientific_gates_pending"],1)
  self.assertEqual({n:(self.root/n).read_bytes() for n in files},old)
  config=json.loads((self.root/pm.CONFIG).read_text())
  self.assertTrue(config["source_verification_required"])
  self.assertTrue(config["formative_gates_required"])
 def test_does_not_allow_unattributed_switch(self):
  with self.assertRaises(ValueError):pm.set_mode(self.root,"FULL","")
 def test_missing_config_is_not_fabricated(self):
  (self.root/pm.CONFIG).unlink()
  with self.assertRaises(ValueError):pm.view(self.root)

class NoveltyTests(unittest.TestCase):
 def setUp(self):
  self.evidence=[{"Evidence_ID":"EVID-1","Supporting_locator":"Source passage present"}]
  self.search=[{"Search_ID":"SEARCH-1","Literal_query":"government AND models","Status":"EXECUTED"}]
  self.claim={"Claim_ID":"CL-1","Claim_text":"A novidade sobreviveu no corpus selecionado.",
    "Claim_type":"I","Evidence_IDs":"EVID-1","Inference_warrant":"The retrieved nearest studies cover different governance roles and leave this local interpretation provisional.",
    "Boundary_conditions":"Limited to the search strategy and recorded sources with access constraints.",
    "Novelty_scope":"Only the retrieved studies available in the bounded temporal and indexed sources.",
    "Novelty_search_ref":"SEARCH-1",
    "Human_validation":"VALIDATED","Researcher_review_evidence":"Researcher directly inspected the closest published studies and confirmed limits.",
    "Draft_status":"FROZEN"}
 def run_audit(self,change=None):
  row={**self.claim,**(change or {})}
  return ci.audit([row],self.evidence,self.search,freeze=True,strict=True,
                  headers=[*row,*ci.EXTRA_COLUMNS])
 def test_bounded_novelty_inference_can_be_structurally_reviewed(self):
  self.assertTrue(ci.is_novelty_conclusion(self.claim["Claim_text"]))
  self.assertFalse(self.run_audit()["errors"])
 def test_novelty_survival_cannot_be_literature_or_original_proposition(self):
  for kind in ["L","P"]:
   self.assertTrue(any("must be a bounded [I]" in e for e in
                       self.run_audit({"Claim_type":kind})["errors"]))
 def test_missing_executed_search_fails(self):
  self.assertTrue(any("unexecuted" in e or "unknown novelty" in e or "needs actual Search_ID" in e
     for e in self.run_audit({"Novelty_search_ref":"SEARCH-MISSING"})["errors"]))
 def test_unbounded_priority_still_blocks(self):
  r=self.run_audit({"Claim_text":"Este é o primeiro estudo sobre o fenômeno."})
  self.assertTrue(r["errors"])

class ProtocolTests(unittest.TestCase):
 def test_integrative_reference_has_no_observed_results(self):
  data=json.loads((ROOT/"benchmarks/integrative_replication_protocol_v1.json").read_text())
  self.assertEqual(data["status"],"PLANNED_NOT_EXECUTED")
  self.assertIsNone(data["reproduction_results"])
  self.assertIsNone(data["independent_review"])
  self.assertFalse(data["scientific_quality_validated"])
  self.assertEqual(data["reference"]["doi"],"10.1016/j.giq.2023.101881")
 def test_modes_study_has_no_fabricated_participants(self):
  data=json.loads((ROOT/"benchmarks/minimal_full_comparison_protocol_v1.json").read_text())
  self.assertFalse(data["causal_effect_established"])
  self.assertEqual(data["sample_size_observed"],0)
  self.assertEqual(data["participant_results"],[])
  self.assertEqual(data["arms"]["MINIMAL"]["scientific_controls"],"UNCHANGED")
  self.assertEqual(data["arms"]["FULL"]["scientific_controls"],"UNCHANGED")

class CompactAIDisclosureTests(unittest.TestCase):
 def sample(self):
  return {"journal":"Fixture Journal","location":"DECLARATIONS","status":"READY_FOR_PLACEMENT_REVIEW",
          "errors":[],"uses":[{"category":"LITERATURE_SEARCH","tool":"Fixture Tool",
          "model":"0-test","purpose":"Organize researcher-provided query","review":"Reviewed","decision":"MODIFIED"}]}
 def test_compact_within_target_length(self):
  output=ed.render_compact(self.sample())
  self.assertLessEqual(len(output),3000)
  self.assertLessEqual(len(output.splitlines()),32)
  self.assertIn("Fixture Tool",output)
  self.assertIn("final author review",output.lower())
 def test_pending_is_never_disguised_as_final(self):
  x=self.sample();x["errors"]=["official journal rules not verified"]
  self.assertIn("DRAFT WITH OUTSTANDING REQUIREMENTS",ed.render_compact(x))
 def test_length_limit_rejects_omission(self):
  x=self.sample()
  x["uses"][0]["purpose"]="Content requiring faithful disclosure. "*300
  with self.assertRaises(ValueError):ed.render_compact(x)

if __name__=="__main__":
 unittest.main()
