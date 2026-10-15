"""REG-017 read-only Evidence-view integration; synthetic research fixtures."""
from __future__ import annotations
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import native_chat_dashboard as native

def csv_table(path,cols,rows):
    with path.open("w",newline="",encoding="utf-8-sig") as h:
        w=csv.DictWriter(h,fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

class UnifiedPanelTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.m=self.root/native.MGMT
        self.m.mkdir()
        (self.m/"PROJECT_CONFIG.json").write_text(json.dumps({
            "presentation_mode":"MINIMAL","storage_mode":"GOOGLE_DRIVE"}),encoding="utf-8")
        (self.m/"CONTINUIDADE.md").write_text("# Fictional project\nNo approved next step",encoding="utf-8")
        csv_table(self.m/"11_CADA_Control.csv",
                  ["CADA_ID","Title","Assigned_to","Deadline","Status"],
                  [{"CADA_ID":"CADA-0001","Title":"A private task",
                    "Assigned_to":"","Deadline":"","Status":"BLOCKED"}])
        csv_table(self.m/"18_Human_Validation_Gates.csv",
                  ["GATE_ID","Status","Decision"],
                  [{"GATE_ID":"GATE-0001","Status":"PENDING","Decision":"PENDING"}])

    def valid_tables(self):
        csv_table(self.m/"05_Evidence_Matrix.csv",
                  ["Evidence_ID","Citation","DOI_or_persistent_ID"],
                  [{"Evidence_ID":"EVID-0001","Citation":"PRIVATE_BIBLIOGRAPHIC_TITLE",
                    "DOI_or_persistent_ID":"10.1234/demo"}])
        csv_table(self.m/"09_Claims_Ledger.csv",
                  ["Claim_ID","Claim_type","Claim_text","Evidence_IDs"],
                  [{"Claim_ID":"CLAIM-0001","Claim_type":"[L]",
                    "Claim_text":"PRIVATE_RESEARCH_CLAIM","Evidence_IDs":"EVID-0001"},
                   {"Claim_ID":"CLAIM-0002","Claim_type":"[L]",
                    "Claim_text":"Another private claim","Evidence_IDs":"EVID-9999"},
                   {"Claim_ID":"CLAIM-0003","Claim_type":"[L]",
                    "Claim_text":"Source-less claim","Evidence_IDs":""}])
        csv_table(self.m/"03_Screening.csv",["Record_ID"],
                  [{"Record_ID":"REC-0001"}])
        csv_table(self.m/"04_FullText_Tracker.csv",
                  ["Record_ID","Evidence_matrix_id","File_or_URL"],
                  [{"Record_ID":"REC-0001","Evidence_matrix_id":"EVID-0001",
                    "File_or_URL":"PRIVATE_FULLTEXT_LOCATION"}])
        csv_table(self.m/"01_Protocolo.csv",
                  ["Item","Decision","Rationale","Status"],
                  [{"Item":"Method","Decision":"Fictional design",
                    "Rationale":"PRIVATE_METHOD_RATIONALE","Status":"PENDING"}])

    def test_incomplete_canonical_inputs_have_unknown_not_zero_counts(self):
        x=native.panel(self.root)["evidence"]["diagnostic"]
        self.assertEqual(x["status"],"NOT_READY")
        self.assertIsNone(x["blocking_occurrences"])
        self.assertIsNone(x["review_occurrences"])
        self.assertFalse(x["scientific_quality_validated"])
        self.assertFalse(x["drive_sync_verified_in_this_session"])

    def test_one_existing_evidence_view_contains_diagnostic(self):
        self.valid_tables()
        p=native.panel(self.root)
        self.assertNotIn("diagnostic",p)
        d=p["evidence"]["diagnostic"]
        self.assertEqual(d["status"],"ASSESSED_LIMITED_SCOPE")
        self.assertEqual(d["source_report_status"],"MISSING")
        self.assertFalse(p["drive_sync_verified_in_this_session"])
        self.assertEqual(p["overview"]["next_task_id"],p["continuation"]["next_task_id"])

    def test_full_and_minimal_preserve_same_classification(self):
        self.valid_tables()
        m=native.panel(self.root,mode="MINIMAL")["evidence"]["diagnostic"]
        f=native.panel(self.root,mode="FULL")["evidence"]["diagnostic"]
        for key in ("blocking_occurrences","review_occurrences",
                    "verdict","source_report_status"):
            self.assertEqual(m[key],f[key])
        self.assertEqual(len(m["findings"]),2)
        self.assertGreater(len(f["findings"]),len(m["findings"]))
        self.assertEqual(len(m["next_actions"]),1)
        self.assertLessEqual(len(f["next_actions"]),4)
        self.assertGreater(m["findings_hidden"],f["findings_hidden"])
        self.assertFalse(m["scientific_quality_validated"])

    def test_private_source_titles_claims_and_methods_are_not_in_payload(self):
        self.valid_tables()
        for mode in ("FULL","MINIMAL"):
            blob=json.dumps(native.panel(self.root,mode=mode))
            for secret in ("PRIVATE_BIBLIOGRAPHIC_TITLE","PRIVATE_RESEARCH_CLAIM",
                           "PRIVATE_FULLTEXT_LOCATION","PRIVATE_METHOD_RATIONALE"):
                self.assertNotIn(secret,blob)

    def test_modes_never_mutate_canonical_inputs(self):
        self.valid_tables()
        before={p.name:p.read_bytes() for p in self.m.iterdir() if p.is_file()}
        native.panel(self.root,mode="MINIMAL")
        native.panel(self.root,mode="FULL")
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.m.iterdir() if p.is_file()})

    def test_bibliography_and_claim_defects_share_same_priority_list(self):
        self.valid_tables()
        x=native.panel(self.root,mode="FULL")["evidence"]["diagnostic"]
        codes={item["code"] for item in x["findings"]}
        self.assertIn("UNKNOWN_REFERENCE",codes)
        self.assertIn("CLAIM_EVIDENCE_MISSING_OR_AMBIGUOUS",codes)
        self.assertGreater(x["blocking_occurrences"],0)
        self.assertEqual(x["verdict"],"CORRECAO_REQUERIDA")

    def test_text_fallback_shows_diagnosis_and_drive_unverified(self):
        self.valid_tables()
        t=native.fallback(native.panel(self.root))
        self.assertIn("Research diagnostic: ASSESSED_LIMITED_SCOPE",t)
        self.assertIn("First diagnostic finding:",t)
        self.assertIn("Google Drive sync verified: NO",t)
        self.assertNotIn("PRIVATE_RESEARCH_CLAIM",t)

    def test_missing_input_fallback_never_presents_zero(self):
        t=native.fallback(native.panel(self.root))
        self.assertIn("Research diagnostic: NOT_READY | blockers: None | review: None",t)
        self.assertIn("Unavailable or none recorded",t)

    def test_malformed_source_report_does_not_approve_evidence(self):
        self.valid_tables()
        (self.m/"SOURCE_VERIFICATION.json").write_text("{ not-json",encoding="utf-8")
        d=native.panel(self.root)["evidence"]["diagnostic"]
        self.assertNotEqual(d["source_report_status"],"RECORDED_CLEAR")
        self.assertFalse(d["scientific_quality_validated"])

if __name__=="__main__":
    unittest.main()
