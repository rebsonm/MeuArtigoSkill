"""Integrated Gate-6 synthetic tests: source -> evidence -> claim -> gate.

Fixtures are fabricated deliberately for software quality only. No real
researcher approval, peer review, external DOI lookup or Drive sync occurs.
"""
from __future__ import annotations

from argparse import Namespace
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import claim_source_integrity as linked
import claim_integrity
import governance_events as gov
import source_report_integrity as integrity
import verify_sources as source

MGMT = "00_Gestao_e_Continuidade"
DOI = "10.1234/imaginary-gate6"


def save_csv(path, headers, data):
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


class IntegratedGate6Tests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "project"
        self.mgmt = self.root / MGMT
        self.mgmt.mkdir(parents=True)
        (self.mgmt / "PROJECT_CONFIG.json").write_text(json.dumps({
            "claim_integrity_required": True,
            "source_verification_required": True,
            "method_route_governance_required": False,
            "formative_gates_required": False,
        }), encoding="utf-8")
        (self.root / "synthetic.txt").write_text(
            "Synthetic researchers examined an invented organizational relationship "
            "within a clearly restricted project context.\n", encoding="utf-8")
        self.claim = {
            "Claim_ID": "CLAIM-0001", "Claim_type": "[L]",
            "Claim_text": "The synthetic study reports a relationship in a restricted hypothetical context.",
            "Evidence_IDs": "EVID-0001", "Locator_status": "MATCHED",
            "Human_validation": "VALIDATED", "Draft_status": "READY",
            "Researcher_review_evidence": "Synthetic researcher note: examined source limitations in this fixture.",
            "Robustness_status": "ROBUST",
        }
        self.evidence = {
            "Evidence_ID": "EVID-0001", "Record_ID": "REC-0001",
            "DOI_or_persistent_ID": DOI, "Citation": "Hypothetical Study, 2022",
            "Title": "Invented organizational relationships",
            "Year": "2022",
            "Supporting_locator": '"Synthetic researchers examined an invented organizational relationship within a clearly restricted project context."',
            "Source_path": "synthetic.txt",
        }
        self.claim_headers = list(self.claim) + [
            x for x in claim_integrity.EXTRA_COLUMNS if x not in self.claim
        ]
        save_csv(self.mgmt / "09_Claims_Ledger.csv", self.claim_headers, [self.claim])
        save_csv(self.mgmt / "05_Evidence_Matrix.csv", list(self.evidence), [self.evidence])
        save_csv(self.mgmt / "03_Screening.csv",
                 ["Record_ID", "Title", "Year", "DOI", "Authors"],
                 [{"Record_ID": "REC-0001", "Title": self.evidence["Title"],
                   "Year": "2022", "DOI": DOI, "Authors": "Silva"}])
        save_csv(self.mgmt / "04_FullText_Tracker.csv",
                 ["Record_ID", "Evidence_matrix_id", "File_or_URL"],
                 [{"Record_ID": "REC-0001", "Evidence_matrix_id": "EVID-0001",
                   "File_or_URL": "synthetic.txt"}])
        save_csv(self.mgmt / "02_Search_Log.csv", ["Search_ID", "Literal_query", "Status"],
                 [{"Search_ID": "SEARCH-0001", "Literal_query": "invented AND study",
                   "Status": "COMPLETE"}])
        save_csv(self.mgmt / "18_Human_Validation_Gates.csv", gov.GATE_HEADERS, [
            {"GATE_ID": "GATE-0006", "Name": "Scientific claim audit",
             "Status": "READY", "Scientific_stage": "10"}])
        save_csv(self.mgmt / "13_Traceability_Log.csv", gov.TRACE_HEADERS, [])
        save_csv(self.mgmt / "17_Decision_Log.csv", gov.DEC_HEADERS, [])
        self.create_report()

    def fetcher(self, provider, doi, mailto=""):
        if provider == "crossref":
            return {"status": "FOUND", "data": {
                "DOI": doi, "title": [self.evidence["Title"]],
                "published": {"date-parts": [[2022]]},
                "author": [{"family": "Silva"}]}}
        return {"status": "FOUND", "data": {
            "doi": "https://doi.org/" + doi,
            "display_name": self.evidence["Title"],
            "publication_year": 2022, "is_retracted": False}}

    def create_report(self):
        content = source.verify_project(self.root, fetcher=self.fetcher)
        (self.mgmt / "SOURCE_VERIFICATION.json").write_text(
            json.dumps(content, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        return content

    def set_claim(self, **updates):
        self.claim.update(updates)
        save_csv(self.mgmt / "09_Claims_Ledger.csv", self.claim_headers, [self.claim])

    def set_evidence(self, **updates):
        self.evidence.update(updates)
        save_csv(self.mgmt / "05_Evidence_Matrix.csv", list(self.evidence), [self.evidence])

    def approve(self, snapshot=False):
        return gov.record_gate(Namespace(
            project=self.root, gate_id="GATE-0006", decision="APPROVED",
            validated_by="Synthetic fixture researcher", method="Synthetic document review",
            evidence="Synthetic review reference: fixture-only",
            notes="Synthetic approval for regression testing; not a real human decision",
            researcher_rationale="", researcher_limitation="", no_snapshot=not snapshot))

    def assert_gate_not_changed(self):
        with (self.mgmt / "18_Human_Validation_Gates.csv").open(
                encoding="utf-8-sig", newline="") as stream:
            row = next(csv.DictReader(stream))
        self.assertEqual(row["Status"], "READY")
        with (self.mgmt / "13_Traceability_Log.csv").open(
                encoding="utf-8-sig", newline="") as stream:
            self.assertEqual(len(list(csv.DictReader(stream))), 0)

    def validator(self):
        return subprocess.run([sys.executable, str(ROOT / "scripts/validate_project.py"),
                               str(self.root)], capture_output=True, text=True)

    def test_end_to_end_clean_gate_6_creates_linked_snapshot(self):
        self.assertEqual(integrity.assess(self.root)["status"], "RECORDED_CLEAR")
        self.assertEqual(linked.audit(self.root, freeze=True)["errors"], [])
        self.assertEqual(self.approve(snapshot=True), 0)
        with (self.mgmt / "18_Human_Validation_Gates.csv").open(
                encoding="utf-8-sig", newline="") as stream:
            gate = next(csv.DictReader(stream))
        with (self.mgmt / "19_Snapshots.csv").open(
                encoding="utf-8-sig", newline="") as stream:
            snap = next(csv.DictReader(stream))
        self.assertEqual(gate["Snapshot_after"], snap["SNAP_ID"])
        self.assertEqual(snap["Gate_ID"], "GATE-0006")
        self.assertEqual(gate["Status"], "COMPLETED")
        self.assertEqual(linked.audit(self.root, freeze=True)["errors"], [])
        self.assertFalse((self.mgmt / ".pending_gate_snapshot").exists())

    def test_final_claim_falsely_says_matched_with_reviewed_uncheckable_locator(self):
        self.set_evidence(Supporting_locator="p. 1")
        report = self.create_report()
        self.assertEqual(report["checks"][0]["locator_status"], "LOCATOR_NOT_CHECKABLE")
        sha = hashlib.sha256((self.mgmt / "SOURCE_VERIFICATION.json").read_bytes()).hexdigest()
        record = {
            "DEC_ID": "DEC-0001", "Decision_type": "EVIDENCE", "Status": "APPROVED",
            "Gate_ID": "GATE-0006", "Evidence_IDs": "EVID-0001",
            "Decided_by": "Synthetic researcher",
            "Rationale": "Synthetic decision documents limitations rather than verifying a nonexistent direct passage.",
            "Affected_artifacts": f"SOURCE_VERIFICATION.json#sha256={sha}",
            "Notes": "SOURCE_REVIEW_LIMITATIONS=The literal source quotation is not available in this synthetic test.\n"
                     "ORIGINAL_RESPONSE_REF=synthetic-review-fixture-001",
        }
        save_csv(self.mgmt / "17_Decision_Log.csv", gov.DEC_HEADERS, [record])
        self.assertEqual(integrity.assess(self.root)["status"], "REVIEWED_LIMITATIONS")
        audit = linked.audit(self.root, freeze=True)
        self.assertTrue(any("claims MATCHED" in e for e in audit["errors"]))
        with self.assertRaisesRegex(SystemExit, "claim-source consistency"):
            self.approve()
        self.assert_gate_not_changed()
        self.set_claim(Locator_status="LOCATOR_NOT_CHECKABLE")
        self.assertEqual(linked.audit(self.root, freeze=True)["errors"], [])
        self.assertEqual(self.approve(), 0)

    def test_stale_evidence_matrix_blocks_gate_after_verified_report(self):
        self.set_evidence(Year="2023")
        with self.assertRaisesRegex(SystemExit, "source verification"):
            self.approve()
        self.assert_gate_not_changed()

    def test_missing_source_report_blocks_gate_without_register_mutation(self):
        (self.mgmt / "SOURCE_VERIFICATION.json").unlink()
        with self.assertRaisesRegex(SystemExit, "source verification"):
            self.approve()
        self.assert_gate_not_changed()

    def test_objectively_false_claim_locator_blocks_approval_before_snapshot(self):
        self.set_claim(Locator_status="PASSAGE_NOT_FOUND")
        with self.assertRaisesRegex(SystemExit, "claim freeze"):
            self.approve(snapshot=True)
        self.assert_gate_not_changed()
        self.assertFalse((self.mgmt / "19_Snapshots.csv").exists())

    def test_verified_source_cannot_justify_vague_final_claim_locator_status(self):
        self.set_claim(Locator_status="VERIFIED")
        self.assertEqual(integrity.assess(self.root)["status"], "RECORDED_CLEAR")
        with self.assertRaisesRegex(SystemExit, "claim-source consistency"):
            self.approve()
        self.assert_gate_not_changed()

    def test_completed_gate_is_rechecked_when_literature_claim_is_tampered(self):
        self.assertEqual(self.approve(), 0)
        self.set_claim(Locator_status="VERIFIED")
        inspection = self.validator()
        self.assertNotEqual(inspection.returncode, 0)
        self.assertIn("GATE-0006 claim-source integrity:", inspection.stdout)

    def test_missing_citation_evidence_is_rejected_before_scientific_gate(self):
        self.set_claim(Evidence_IDs="EVID-9999")
        with self.assertRaisesRegex(SystemExit, "claim freeze"):
            self.approve()
        self.assert_gate_not_changed()


if __name__ == "__main__":
    unittest.main()
