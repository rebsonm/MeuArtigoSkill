"""Behavioral controls for event evidence, without paid services or live APIs."""
from pathlib import Path
import csv
import importlib.util
import json
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "scripts"))
import trace_execution as te
import governance_events as gov

class TraceExecutionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.management = self.root / te.MGMT
        self.management.mkdir()
        with (self.management / "05_Evidence_Matrix.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Evidence_ID", "DOI_or_persistent_ID", "Supporting_locator"])
            writer.writeheader()
            writer.writerow({"Evidence_ID": "EVID-001", "DOI_or_persistent_ID": "",
                             "Supporting_locator": "No accessible quotation"})
        self.output = f"{te.MGMT}/SOURCE_VERIFICATION.json"

    def options(self, *, outputs=None, inputs=None, extra=None):
        import argparse
        return argparse.Namespace(
            project=str(self.root), stage="08", cada_id="",
            action="SOURCE_CHECK", summary="Run local source verification",
            materiality="SUBSTANTIVE", script="verify_sources.py",
            outputs=outputs if outputs is not None else [self.output],
            inputs=inputs if inputs is not None else [f"{te.MGMT}/05_Evidence_Matrix.csv"],
            script_args=extra if extra is not None else ["--offline"]
        )

    def read_trace(self):
        return te.trace_rows(self.root)

    def run_confirmed(self):
        result = te.run_script(self.options())
        self.assertEqual(result, 0)
        self.assertEqual(self.read_trace()[-1]["Status"], "CONFIRMED")
        return self.read_trace()[-1]

    def test_script_execution_creates_hashed_receipt(self):
        trace = self.run_confirmed()
        audit = te.audit_receipts(self.root, strict=True)
        self.assertEqual(audit["counts"]["confirmed"], 1)
        self.assertEqual(audit["errors"], [])
        proof = dict(p.split("=",1) for p in trace["Reproducibility_information"].split(";"))
        receipt = json.loads((self.root / proof["receipt"]).read_text())
        self.assertEqual(receipt["exit_code"], 0)
        self.assertEqual(receipt["status"], "CONFIRMED")
        self.assertEqual(trace["Action_type"], "LOCAL_SOURCE_VERIFICATION")
        self.assertEqual(receipt["outputs_after"][0]["sha256"], te.sha256(self.root / self.output))

    def test_no_receipt_cannot_confirm_external_claim(self):
        from argparse import Namespace
        args = Namespace(project=str(self.root), stage="04", cada_id="",
                         action="SEARCH_EXECUTED", summary="Provider reported 200 records",
                         materiality="SUBSTANTIVE")
        self.assertEqual(te.declare(args), 0)
        self.assertEqual(self.read_trace()[-1]["Status"], "UNVERIFIED")
        self.assertEqual(te.audit_receipts(self.root, strict=True)["counts"]["confirmed"], 0)

    def test_missing_expected_output_is_partial(self):
        args = self.options(outputs=[f"{te.MGMT}/absent.csv"])
        self.assertEqual(te.run_script(args), 2)
        self.assertEqual(self.read_trace()[-1]["Status"], "PARTIAL")
        self.assertEqual(te.audit_receipts(self.root, strict=True)["counts"]["partial"], 1)

    def test_second_identical_output_is_not_new_proof(self):
        self.run_confirmed()
        self.assertEqual(te.run_script(self.options(outputs=[f"{te.MGMT}/05_Evidence_Matrix.csv"])), 2)
        self.assertEqual(self.read_trace()[-1]["Status"], "PARTIAL")

    def test_arbitrary_external_action_cannot_be_attested_by_local_script(self):
        args = self.options()
        args.action = "SEARCH_EXECUTED_ON_SCOPUS"
        self.assertEqual(te.run_script(args), 0)
        self.assertEqual(self.read_trace()[-1]["Action_type"], "LOCAL_SOURCE_VERIFICATION")

    def test_failed_execution_is_not_confirmed(self):
        (self.management / "05_Evidence_Matrix.csv").unlink()
        self.assertEqual(te.run_script(self.options(inputs=[])), 1)
        self.assertEqual(self.read_trace()[-1]["Status"], "FAILED")

    def test_changed_output_invalidates_receipt_binding(self):
        self.run_confirmed()
        with (self.root / self.output).open("a", encoding="utf-8") as f:
            f.write("altered")
        self.assertTrue(any("no longer matches" in e for e in te.audit_receipts(self.root, strict=True)["errors"]))

    def test_modified_receipt_is_rejected(self):
        trace = self.run_confirmed()
        proof = dict(p.split("=",1) for p in trace["Reproducibility_information"].split(";"))
        with (self.root / proof["receipt"]).open("a", encoding="utf-8") as f:
            f.write("forged")
        self.assertTrue(any("receipt missing or modified" in e for e in te.audit_receipts(self.root)["errors"]))

    def test_fake_confirmed_csv_row_is_rejected(self):
        gov.append(self.management / "13_Traceability_Log.csv", gov.TRACE_HEADERS, {
            "Trace_ID":"TRACE-0012", "Status":"CONFIRMED", "Action_summary":"Claim of completion"})
        self.assertTrue(te.audit_receipts(self.root, strict=True)["errors"])

    def test_legacy_complete_requires_migration_in_strict_mode(self):
        gov.append(self.management / "13_Traceability_Log.csv", gov.TRACE_HEADERS, {
            "Trace_ID":"TRACE-0001", "Status":"COMPLETE", "Action_summary":"Old log"})
        self.assertTrue(te.audit_receipts(self.root, strict=True)["errors"])
        self.assertEqual(te.audit_receipts(self.root, strict=False)["errors"], [])

    def test_source_outside_project_is_rejected(self):
        with self.assertRaises(ValueError):
            te.run_script(self.options(outputs=["../outside.csv"]))

    def test_governance_does_not_mislabel_approval_as_machine_proof(self):
        tid = gov.record_trace(self.root, stage="02", cada_id="", action_type="SCIENTIFIC_DECISION",
                               summary="Design selected", decision_output="Integrative", rationale="Appropriate",
                               human_validation="Researcher")
        rows = self.read_trace()
        self.assertEqual(rows[-1]["Trace_ID"], tid)
        self.assertEqual(rows[-1]["Status"], "UNVERIFIED")

    def test_cli_run_and_audit_without_paid_services(self):
        result = te.main(["run", "--action", "SOURCE_CHECK", "--summary", "Local verification",
                          "--script", "verify_sources.py", "--output", self.output,
                          str(self.root), "--", "--offline"])
        self.assertEqual(result, 0)
        self.assertEqual(te.main(["audit", str(self.root), "--strict"]), 0)


if __name__ == "__main__":
    unittest.main()
