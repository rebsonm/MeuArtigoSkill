"""REG-011 offline adversarial controls. All articles/people are synthetic."""
from __future__ import annotations
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
import semantic_claim_review as scr
from source_report_integrity import manifest
from verify_sources import digest

def save_csv(path, headers, data):
    with path.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=headers)
        w.writeheader();w.writerows(data)

class SemanticClaimReviewTests(unittest.TestCase):
    def setUp(self):
        td=tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self.root=Path(td.name)
        self.m=self.root/scr.MGMT
        self.m.mkdir()
        self.quote="The researchers compared two independently collected organizational samples to estimate descriptive differences."
        self.source=self.root/"paper.txt"
        self.source.write_text(self.quote+"\n",encoding="utf-8")
        self.claim={"Claim_ID":"CLAIM-0001","Claim_type":"[L]",
                    "Claim_text":"Organizational samples exhibited descriptively different properties.",
                    "Evidence_IDs":"EVID-0001"}
        self.evidence={"Evidence_ID":"EVID-0001","Citation":"Hypothetical Doe (2022)",
                       "DOI_or_persistent_ID":"10.1234/synthetic-article",
                       "Supporting_locator":self.quote}
        self.write_inputs()
        self.write_report()

    def write_inputs(self):
        save_csv(self.m/scr.CLAIMS,list(self.claim),[self.claim])
        save_csv(self.m/scr.EVIDENCE,list(self.evidence),[self.evidence])
        save_csv(self.m/"03_Screening.csv",["Record_ID"],[{"Record_ID":"REC-0001"}])
        save_csv(self.m/"04_FullText_Tracker.csv",
                 ["Record_ID","Evidence_matrix_id","File_or_URL"],
                 [{"Record_ID":"REC-0001","Evidence_matrix_id":"EVID-0001","File_or_URL":"paper.txt"}])

    def write_report(self, *, met="VERIFIED",locator="MATCHED",retraction=False):
        row={"Evidence_ID":"EVID-0001","Record_ID":"REC-0001",
             "doi":"10.1234/synthetic-article","metadata_status":met,
             "metadata_checks":[{"provider":"crossref","status":"VERIFIED" if met=="VERIFIED" else "NOT_FOUND"}],
             "locator_status":locator,"source_path":"paper.txt",
             "source_sha256":digest(self.source),"retraction_alert":retraction,
             "correction_alert":False,"update_alert":False,"provider_warnings":[],
             "editorial_notices":[],
             "result":"FAIL" if met=="NOT_FOUND" or locator=="PASSAGE_NOT_FOUND" else
                      "REVIEW_REQUIRED" if retraction or met!="VERIFIED" or locator!="MATCHED" else
                      "METADATA_AND_LOCATOR_CHECKED"}
        (self.m/scr.SOURCE_REPORT).write_text(json.dumps({
            "schema_version":2,"input_manifest":manifest(self.root),
            "offline":False,"checks":[row]}),encoding="utf-8")

    def annotation(self,**overrides):
        source=scr.snapshot(self.root)
        a={"claim_id":"CLAIM-0001","evidence_id":"EVID-0001",
           "claim_sha256":scr.sha(scr.clean(self.claim["Claim_text"]).encode("utf-8")),
           "source_sha256":digest(self.source),
           "source_report_sha256":source[scr.SOURCE_REPORT],
           "reviewer_kind":"HUMAN_DECLARED","reviewer":"Hypothetical reviewer",
           "response_reference":"synthetic-conversation-response-001",
           "judgment":"SUPPORTED",
           "scope_alignment":"ALIGNED","method_alignment":"ALIGNED","context_alignment":"ALIGNED",
           "counterevidence_considered":True,
           "rationale":"The precise quoted sentence is consistent with the narrowly bounded descriptive statement.",
           "limitations":"Only the stated descriptive comparison is considered.",
           "quoted_passage":self.quote}
        a.update(overrides)
        return {"schema_version":1,"reviews":[a]}

    def item(self, assessments=None):
        return scr.review(self.root,assessments)["review_items"][0]

    def test_unannotated_claim_remains_pending_and_not_semantically_proven(self):
        result=scr.review(self.root)
        self.assertEqual(self.item()["status"],"PENDING_HUMAN_REVIEW")
        self.assertFalse(result["semantic_support_proven"])
        self.assertFalse(result["gate_approval_performed"])
        self.assertFalse(result["researcher_authenticated"])

    def test_declared_supported_is_never_automatic_scientific_validation(self):
        result=scr.review(self.root,self.annotation())
        row=result["review_items"][0]
        self.assertEqual(row["status"],"HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED")
        self.assertEqual(row["declared_judgment"],"SUPPORTED")
        self.assertFalse(result["semantic_support_proven"])
        self.assertFalse(result["claim_summaries"][0]["scientific_claim_approved"])
        raw=json.dumps(result)
        self.assertNotIn(self.quote,raw)
        self.assertNotIn("Hypothetical reviewer",raw)
        self.assertNotIn("The precise quoted",raw)
        self.assertNotIn("paper.txt",raw)

    def test_claim_overreach_cannot_be_marked_supported_without_alignment(self):
        annotation=self.annotation(scope_alignment="OVERGENERALIZED")
        self.assertEqual(self.item(annotation)["status"],"UNQUALIFIED_SUPPORT_CONTRADICTS_REVIEW")

    def test_missing_counterevidence_check_blocks_unqualified_support(self):
        self.assertEqual(self.item(self.annotation(counterevidence_considered=False))["status"],
                         "UNQUALIFIED_SUPPORT_CONTRADICTS_REVIEW")

    def test_invented_passage_is_not_accepted(self):
        self.assertEqual(self.item(self.annotation(
            quoted_passage="The study established universal causality with no limitations in all settings."))["status"],
                         "QUOTED_PASSAGE_NOT_CONFIRMED")

    def test_ai_claiming_reviewer_role_is_rejected(self):
        self.assertEqual(self.item(self.annotation(reviewer_kind="AI"))["status"],
                         "HUMAN_REVIEW_NOT_DECLARED")

    def test_bibliographic_not_found_is_not_upgraded_by_human_claim(self):
        self.write_report(met="NOT_FOUND")
        self.assertEqual(self.item(self.annotation())["status"],"SOURCE_REQUIRES_REVIEW")

    def test_retraction_requires_review_not_silent_supported_status(self):
        self.write_report(retraction=True)
        self.assertEqual(self.item(self.annotation())["status"],"SOURCE_REQUIRES_REVIEW")

    def test_stale_source_report_blocks_any_review(self):
        self.evidence["Citation"]="Changed title"
        self.write_inputs()
        self.assertEqual(self.item(self.annotation())["status"],"SOURCE_REPORT_UNAVAILABLE_OR_STALE")

    def test_source_hash_change_invalidates_annotation(self):
        annotation=self.annotation()
        self.source.write_text(self.quote+"\nchanged",encoding="utf-8")
        self.assertEqual(self.item(annotation)["status"],"SOURCE_REPORT_UNAVAILABLE_OR_STALE")

    def test_annotation_bound_to_old_claim_hash_is_rejected(self):
        self.assertEqual(self.item(self.annotation(claim_sha256="0"*64))["status"],
                         "REVIEW_BOUND_TO_STALE_OR_DIFFERENT_INPUT")

    def test_partial_support_is_recorded_without_pretending_full_support(self):
        result=scr.review(self.root,self.annotation(judgment="PARTIALLY_SUPPORTED",
                                                    scope_alignment="OVERGENERALIZED"))
        self.assertEqual(result["review_items"][0]["status"],
                         "HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED")
        self.assertTrue(result["claim_summaries"][0]["one_or_more_partially_supported"])
        self.assertFalse(result["semantic_support_proven"])

    def test_non_literature_claims_are_not_relabelled_literature(self):
        self.claim["Claim_type"]="[I]"
        self.write_inputs()
        result=scr.review(self.root)
        self.assertEqual(result["review_items"],[])
        with self.assertRaisesRegex(ValueError,"absent"):
            scr.review(self.root,self.annotation())

    def test_duplicate_annotations_rejected(self):
        a=self.annotation()
        a["reviews"].append(dict(a["reviews"][0]))
        with self.assertRaisesRegex(ValueError,"Duplicate"):
            scr.review(self.root,a)

    def test_output_stays_local_never_overwrites_source_or_annotations(self):
        output=self.root/"tmp"/"review.json"
        scr.save_local(self.root,output,scr.review(self.root),None)
        self.assertTrue(output.is_file())
        with self.assertRaisesRegex(ValueError,"canonical"):
            scr.save_local(self.root,self.m/scr.CLAIMS,{},None)
        with self.assertRaisesRegex(ValueError,"within"):
            scr.save_local(self.root,self.root.parent/"outside.json",{},None)

    def test_input_assessments_path_confined_to_project(self):
        with self.assertRaisesRegex(ValueError,"authorized"):
            scr.local_json(self.root,self.root.parent/"file.json")

if __name__=="__main__":
    unittest.main()
