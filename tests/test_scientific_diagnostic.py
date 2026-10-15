"""REG-013 offline one-page report tests using synthetic source/protocol fixtures."""
from __future__ import annotations
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import scientific_diagnostic as d
from source_report_integrity import manifest
from verify_sources import digest

def csvwrite(path,rows,fields):
    with path.open("w",encoding="utf-8-sig",newline="") as stream:
        w=csv.DictWriter(stream,fieldnames=fields);w.writeheader();w.writerows(rows)

class DiagnosticTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.mgmt=self.root/d.MGMT;self.mgmt.mkdir()
        self.article=self.root/"source.txt"
        self.article.write_text("The two organizational samples showed descriptive differences and limited generality.",encoding="utf-8")
        self.evidence=[{"Evidence_ID":"EVID-0001","Citation":"Fictional Doe 2022",
                        "DOI_or_persistent_ID":"10.1234/demo"}]
        self.claims=[{"Claim_ID":"CLAIM-0001","Claim_type":"[L]",
                      "Claim_text":"The samples showed descriptive differences.",
                      "Evidence_IDs":"EVID-0001"}]
        self.protocol=[{"Item":"Design","Decision":"Qualitative document study",
                        "Rationale":"A suitable bounded design for a synthetic example.","Status":"FROZEN"}]
        self.write_inputs()
        self.save_report()

    def write_inputs(self):
        csvwrite(self.mgmt/"05_Evidence_Matrix.csv",self.evidence,
                 ["Evidence_ID","Citation","DOI_or_persistent_ID"])
        csvwrite(self.mgmt/"09_Claims_Ledger.csv",self.claims,
                 ["Claim_ID","Claim_type","Claim_text","Evidence_IDs"])
        csvwrite(self.mgmt/"01_Protocolo.csv",self.protocol,
                 ["Item","Decision","Rationale","Status"])
        csvwrite(self.mgmt/"03_Screening.csv",[{"Record_ID":"REC-0001"}],["Record_ID"])
        csvwrite(self.mgmt/"04_FullText_Tracker.csv",
                 [{"Record_ID":"REC-0001","Evidence_matrix_id":"EVID-0001",
                   "File_or_URL":"source.txt"}],
                 ["Record_ID","Evidence_matrix_id","File_or_URL"])

    def save_report(self, *, meta="VERIFIED", locator="MATCHED",retracted=False):
        check={"Evidence_ID":"EVID-0001","Record_ID":"REC-0001",
               "doi":"10.1234/demo","metadata_status":meta,
               "metadata_checks":[{"provider":"crossref","status":"VERIFIED" if meta=="VERIFIED" else "TITLE_MISMATCH"}],
               "locator_status":locator,"source_path":"source.txt","source_sha256":digest(self.article),
               "retraction_alert":retracted,"correction_alert":False,"update_alert":False,
               "provider_warnings":[],"editorial_notices":[],
               "result":("FAIL" if meta=="MISMATCH" or locator=="PASSAGE_NOT_FOUND" else
                         "REVIEW_REQUIRED" if meta!="VERIFIED" or locator!="MATCHED" or retracted else
                         "METADATA_AND_LOCATOR_CHECKED")}
        (self.mgmt/"SOURCE_VERIFICATION.json").write_text(
            json.dumps({"schema_version":2,"offline":False,
                        "input_manifest":manifest(self.root),"checks":[check]}),
            encoding="utf-8")

    def test_even_clear_checks_do_not_make_scientific_approval(self):
        result=d.compose(self.root)
        self.assertEqual(result["counts"]["references"],1)
        self.assertEqual(result["counts"]["claims"],1)
        self.assertEqual(result["verdict"],"REVISAO_CIENTIFICA_PENDENTE")
        self.assertEqual(result["priority_findings"][0]["code"],"CLAIM_PENDING_HUMAN_REVIEW")
        self.assertFalse(result["scientific_quality_validated"])
        self.assertFalse(result["semantic_entailment_automated"])
        self.assertFalse(result["independent_peer_review_performed"])

    def test_bad_reference_and_claim_are_prioritized_as_blocking(self):
        self.claims[0]["Evidence_IDs"]="EVID-9999"
        self.write_inputs()
        result=d.compose(self.root)
        self.assertEqual(result["verdict"],"CORRECAO_REQUERIDA")
        self.assertGreater(result["counts"]["blocking_occurrences"],0)
        self.assertIn("UNKNOWN_REFERENCE",[x["code"] for x in result["priority_findings"]])

    def test_incomplete_protocol_is_counted_not_validated(self):
        self.protocol[0]["Status"]="PLANNED"
        self.write_inputs()
        r=d.compose(self.root)
        self.assertEqual(r["protocol"]["pending"],1)
        self.assertFalse(r["protocol"]["methodological_validity_proven"])
        self.assertIn("METHODOLOGY_RECORDS_PENDING",[x["code"] for x in r["priority_findings"]])

    def test_missing_protocol_does_not_get_marked_as_complete(self):
        (self.mgmt/"01_Protocolo.csv").unlink()
        r=d.compose(self.root)
        self.assertEqual(r["protocol"]["status"],"NOT_AVAILABLE")
        self.assertIn("METHODOLOGY_PROTOCOL_MISSING",[x["code"] for x in r["priority_findings"]])

    def test_source_report_missing_or_stale_blocks_fabricated_success(self):
        (self.mgmt/"SOURCE_VERIFICATION.json").unlink()
        r=d.compose(self.root)
        self.assertEqual(r["source_verification"],"MISSING")
        self.assertGreater(r["counts"]["findings_total"],0)

    def test_retraction_notice_is_visible_and_not_auto_exclusion(self):
        self.save_report(retracted=True)
        r=d.compose(self.root)
        self.assertIn("SOURCE_RETRACTION_ALERT",[x["code"] for x in r["priority_findings"]])
        self.assertFalse(r["scientific_quality_validated"])

    def test_markdown_is_compact_and_contains_no_private_text(self):
        text=d.markdown(d.compose(self.root))
        self.assertIn("Diagnóstico científico",text)
        self.assertLessEqual(len(text.splitlines()),28)
        self.assertLessEqual(len(text),3300)
        self.assertNotIn("Fictional Doe",text)
        self.assertNotIn("The two organizational",text)
        self.assertNotIn("Qualitative document",text)
        self.assertNotIn(str(self.root),text)

    def test_print_html_is_a4_and_does_not_leak_source(self):
        html=d.html_page(d.compose(self.root))
        self.assertIn("@page{size:A4",html)
        self.assertNotIn("Fictional Doe",html)
        self.assertNotIn("The two organizational",html)
        self.assertIn("Triagem técnica",html)

    def test_overflow_of_many_findings_is_fully_counted_and_truncated(self):
        self.evidence.extend({"Evidence_ID":f"EVID-{n:04d}","Citation":f"Fictional {n}",
                              "DOI_or_persistent_ID":"invalid"} for n in range(2,30))
        self.write_inputs()
        report=d.compose(self.root)
        self.assertLessEqual(len(report["priority_findings"]),6)
        self.assertGreater(report["omitted_finding_categories"],0)
        md=d.markdown(report)
        self.assertLessEqual(len(md),3300)
        self.assertIn("não exibidas",md)

    def test_invalid_review_cannot_escalate_to_science(self):
        a={"schema_version":1,"reviews":[{
            "claim_id":"CLAIM-0001","evidence_id":"EVID-0001",
            "claim_sha256":"0"*64,"judgment":"SUPPORTED",
            "reviewer_kind":"AI"}]}
        r=d.compose(self.root,assessments=a)
        self.assertFalse(r["scientific_quality_validated"])
        self.assertIn("CLAIM_HUMAN_REVIEW_NOT_DECLARED",[x["code"] for x in r["priority_findings"]])

    def test_reproducible_output_when_inputs_unchanged(self):
        self.assertEqual(d.markdown(d.compose(self.root)),d.markdown(d.compose(self.root)))

    def test_optional_output_never_mutates_canonical_csv(self):
        before=(self.mgmt/"09_Claims_Ledger.csv").read_bytes()
        output=self.root/"reports"/"diagnostic.md"
        d.output_file(self.root,output,d.markdown(d.compose(self.root)),None)
        self.assertEqual((self.mgmt/"09_Claims_Ledger.csv").read_bytes(),before)
        self.assertTrue(output.is_file())
        with self.assertRaisesRegex(ValueError,"canonical"):
            d.output_file(self.root,self.mgmt/"09_Claims_Ledger.csv","x",None)
        with self.assertRaisesRegex(ValueError,"inside"):
            d.output_file(self.root,self.root.parent/"outside.md","x",None)

    def test_sanitize_ids_for_markdown_and_html(self):
        self.assertEqual(d.safe_id("<script>alert(1)</script>"),"-")
        self.assertEqual(d.safe_id("CLAIM-0001"),"CLAIM-0001")
        self.assertNotIn("<script>",d.html_page(d.compose(self.root)))

if __name__=="__main__":
    unittest.main()
