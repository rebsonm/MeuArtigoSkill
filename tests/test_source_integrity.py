"""Synthetic source integrity regressions. No participant, corpus or scientific findings."""
import csv
import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import verify_sources as vs
import source_report_integrity as integrity
import visual_dashboard as visual
import governance_events as governance

class SourceIntegrityTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.mgmt = self.root / integrity.MGMT
        self.mgmt.mkdir()
        self.article = self.root / "article.txt"
        self.article.write_text("The conceptual model was tested with two independent samples of respondents.\n", encoding="utf-8")
        self.evidence = {
            "Evidence_ID": "EVID-001", "DOI_or_persistent_ID": "10.1234/abc",
            "Title": "Sample model of organizations", "Year": "2020",
            "Supporting_locator": '"The conceptual model was tested with two independent samples of respondents."',
            "Source_path": "article.txt",
        }
        self.screening = {"Record_ID": "REC-001", "DOI": "10.1234/abc",
                          "Title": "Sample model of organizations", "Year": "2020"}
        self.tracker = {"Record_ID": "REC-001", "Evidence_matrix_id": "EVID-001", "File_or_URL": "article.txt"}
        self.write("05_Evidence_Matrix.csv", [self.evidence])
        self.write("03_Screening.csv", [self.screening])
        self.write("04_FullText_Tracker.csv", [self.tracker])
        (self.mgmt / "PROJECT_CONFIG.json").write_text(json.dumps({
            "project_name": "SYNTHETIC TEST PROJECT",
            "presentation_mode": "FULL", "source_verification_required": True,
            "storage_mode": "WORK_FALLBACK", "storage_state": "WORK_FALLBACK_AUTHORIZED",
        }), encoding="utf-8")

    def write(self, filename, data):
        with (self.mgmt / filename).open("w", encoding="utf-8-sig", newline="") as stream:
            columns = list(dict.fromkeys(key for row in data for key in row))
            writer = csv.DictWriter(stream, fieldnames=columns or ["Record_ID"])
            writer.writeheader()
            writer.writerows(data)

    def fetch(self, provider, doi, mailto=""):
        if provider == "crossref":
            return {"status": "FOUND", "data": {
                "DOI": doi, "title": ["Sample model of organizations"],
                "published": {"date-parts": [[2020]]}, "author": [{"family": "Silva"}],
            }}
        return {"status": "FOUND", "data": {
            "doi": "https://doi.org/" + doi, "display_name": "Sample model of organizations",
            "publication_year": 2020, "is_retracted": False,
        }}

    def generate(self, fetcher=None):
        report = vs.verify_project(self.root, fetcher=fetcher or self.fetch)
        (self.mgmt / "SOURCE_VERIFICATION.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        return report

    def decision(self, report_hash, *, limitations="OpenAlex is unavailable, reducing independent metadata corroboration.",
                 rationale="I inspected the available Crossref metadata and retained uncertainty about this source.",
                 reference="researcher-message-2026-10-10"):
        row = {
            "DEC_ID": "DEC-0001", "Decision_type": "EVIDENCE", "Status": "APPROVED",
            "Gate_ID": "GATE-0006", "Evidence_IDs": "EVID-001",
            "Decided_by": "RESEARCHER", "Rationale": rationale,
            "Affected_artifacts": "SOURCE_VERIFICATION.json#sha256=" + report_hash,
            "Notes": "SOURCE_REVIEW_LIMITATIONS=" + limitations + "\nORIGINAL_RESPONSE_REF=" + reference,
        }
        self.write("17_Decision_Log.csv", [row])

    def test_complete_report_binds_three_files_ids_and_local_text(self):
        report = self.generate()
        m = report["input_manifest"]
        self.assertEqual(report["schema_version"], 2)
        self.assertEqual(set(m["csv_sha256"]), {"evidence", "screening", "fulltext"})
        self.assertEqual(m["bindings"], [{"Evidence_ID": "EVID-001", "Record_ID": "REC-001"}])
        self.assertEqual(len(m["files"]), 1)
        self.assertEqual(m["files"][0]["state"], "PRESENT")
        self.assertEqual(integrity.assess(self.root)["status"], "RECORDED_CLEAR")
        self.assertNotIn("The conceptual model was tested", json.dumps(report))

    def test_change_each_canonical_input_invalidates_report(self):
        for filename in ["05_Evidence_Matrix.csv", "03_Screening.csv", "04_FullText_Tracker.csv"]:
            with self.subTest(filename=filename):
                self.generate()
                path = self.mgmt / filename
                original = path.read_bytes()
                path.write_bytes(original + b"\n")
                self.assertTrue(integrity.assess(self.root)["report_stale"])
                path.write_bytes(original)

    def test_local_file_modified_removed_and_newly_referenced(self):
        self.generate()
        original = self.article.read_bytes()
        self.article.write_bytes(original + b"Changed")
        self.assertEqual(integrity.assess(self.root)["status"], "STALE")
        self.article.write_bytes(original)
        self.article.unlink()
        self.assertEqual(integrity.assess(self.root)["status"], "STALE")
        self.article.write_bytes(original)
        (self.root / "new.txt").write_text("new source", encoding="utf-8")
        self.write("04_FullText_Tracker.csv", [self.tracker, {
            "Record_ID": "REC-002", "Evidence_matrix_id": "", "File_or_URL": "new.txt"
        }])
        self.assertEqual(integrity.assess(self.root)["status"], "STALE")

    def test_duplicate_and_conflicting_identifiers_block(self):
        self.write("05_Evidence_Matrix.csv", [self.evidence, dict(self.evidence)])
        self.generate()
        result = integrity.assess(self.root)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("ambiguous or duplicated Evidence_ID/Record_ID links", result["errors"])

    def test_screening_tracker_conflict_and_duplicate_record_block(self):
        self.write("04_FullText_Tracker.csv", [self.tracker, dict(self.tracker)])
        self.generate()
        self.assertEqual(integrity.assess(self.root)["status"], "BLOCKED")

    def test_report_ids_must_match_exactly_and_unique(self):
        report = self.generate()
        for changed_checks in (
            [{**report["checks"][0], "Evidence_ID": "EVID-FAKE"}],
            [report["checks"][0], dict(report["checks"][0])],
            [{**report["checks"][0], "Record_ID": "REC-WRONG"}],
        ):
            with self.subTest(rows=len(changed_checks)):
                report["checks"] = changed_checks
                (self.mgmt / "SOURCE_VERIFICATION.json").write_text(json.dumps(report), encoding="utf-8")
                self.assertEqual(integrity.assess(self.root)["status"], "BLOCKED")
        self.generate()

    def test_crossref_updated_by_retraction_and_correction_differ(self):
        for kind, retract, corrected in [("retraction", True, False), ("correction", False, True)]:
            with self.subTest(kind=kind):
                def fetch(provider, doi, mailto=""):
                    record = self.fetch(provider, doi, mailto)
                    if provider == "crossref":
                        record["data"]["updated-by"] = [
                            {"DOI": "10.1234/notice", "type": kind, "label": kind.title()}]
                    return record
                row = vs.verify_row(self.evidence, self.root, {}, fetcher=fetch)
                self.assertIs(row["retraction_alert"], retract)
                self.assertIs(row["correction_alert"], corrected)
                self.assertEqual(row["result"], "REVIEW_REQUIRED")
                self.assertEqual(row["editorial_notices"][0]["notice_doi"], "10.1234/notice")
                self.assertEqual(row["editorial_notices"][0]["direction"], "UPDATES_THIS_WORK")

    def test_update_to_is_notice_not_retraction_of_its_own_doi(self):
        def fetch(provider, doi, mailto=""):
            record = self.fetch(provider, doi, mailto)
            if provider == "crossref":
                record["data"]["update-to"] = [{"DOI": "10.1234/original", "type": "retraction"}]
            return record
        row = vs.verify_row(self.evidence, self.root, {}, fetcher=fetch)
        self.assertFalse(row["retraction_alert"])
        self.assertFalse(row["correction_alert"])
        self.assertFalse(row["update_alert"])
        self.assertEqual(row["editorial_notices"][0]["direction"], "THIS_WORK_UPDATES")

    def test_openalex_unavailable_retains_warning(self):
        def fetch(provider, doi, mailto=""):
            return {"status": "ERROR"} if provider == "openalex" else self.fetch(provider, doi, mailto)
        report = self.generate(fetcher=fetch)
        self.assertEqual(report["checks"][0]["provider_warnings"], ["OPENALEX_UNAVAILABLE"])
        self.assertEqual(report["checks"][0]["result"], "REVIEW_REQUIRED")
        self.assertEqual(integrity.assess(self.root)["status"], "REVIEW_REQUIRED")

    def test_page_mismatch_is_objective_blocker(self):
        pdf = self.root / "excerpt.pdf"
        pdf.write_bytes(b"synthetic fake PDF fixture")
        row = dict(self.evidence, Source_path="excerpt.pdf",
                   Supporting_locator='p. 2: "The conceptual model was tested with two independent samples of respondents."')
        with patch.object(vs, "source_pages", return_value=["The conceptual model was tested with two independent samples of respondents.", "Other text"]):
            verification = vs.verify_row(row, self.root, {}, fetcher=self.fetch)
        self.assertEqual(verification["locator_status"], "PAGE_MISMATCH")
        self.assertEqual(verification["result"], "FAIL")

    def test_exception_specific_to_exact_report_no_auto_upgrade(self):
        def fetch(provider, doi, mailto=""):
            return {"status": "ERROR"} if provider == "openalex" else self.fetch(provider, doi, mailto)
        report = self.generate(fetcher=fetch)
        source = self.mgmt / "SOURCE_VERIFICATION.json"
        report_hash = integrity.sha256(source)
        self.decision(report_hash)
        outcome = integrity.assess(self.root)
        self.assertEqual(outcome["status"], "REVIEWED_LIMITATIONS")
        self.assertEqual(outcome["reviewed_limitations"], 1)
        self.assertEqual(report["checks"][0]["result"], "REVIEW_REQUIRED")
        before = (self.mgmt / "17_Decision_Log.csv").read_bytes()
        # Changing the report content invalidates the review binding, not the history.
        report["created_at_utc"] = "2026-10-10T00:00:00Z"
        source.write_text(json.dumps(report), encoding="utf-8")
        self.assertEqual(integrity.assess(self.root)["status"], "REVIEW_REQUIRED")
        self.assertEqual((self.mgmt / "17_Decision_Log.csv").read_bytes(), before)

    def test_insufficient_human_review_cannot_waive_pending(self):
        def fetch(provider, doi, mailto=""):
            return {"status": "ERROR"} if provider == "openalex" else self.fetch(provider, doi, mailto)
        self.generate(fetcher=fetch)
        self.decision(integrity.sha256(self.mgmt / "SOURCE_VERIFICATION.json"),
                      rationale="Okay", reference="short", limitations="Noted")
        self.assertEqual(integrity.assess(self.root)["status"], "REVIEW_REQUIRED")

    def test_gate_six_does_not_mutate_when_objective_issue_exists(self):
        self.write("05_Evidence_Matrix.csv", [dict(self.evidence, Supporting_locator='"This passage does not exist in the document anywhere at all."')])
        self.generate()
        gate = {"GATE_ID": "GATE-0006", "Name": "Scientific claims", "Status": "READY", "Decision": "PENDING"}
        self.write("18_Human_Validation_Gates.csv", [gate])
        before = (self.mgmt / "18_Human_Validation_Gates.csv").read_bytes()
        args = Namespace(project=str(self.root), gate_id="GATE-0006", decision="APPROVED",
                         validated_by="RESEARCHER", method="Critical source review", evidence="original-response-reference",
                         notes="", researcher_rationale="", researcher_limitation="", no_snapshot=True)
        with self.assertRaises(SystemExit) as cm:
            governance.record_gate(args)
        self.assertIn("source verification", str(cm.exception))
        self.assertEqual((self.mgmt / "18_Human_Validation_Gates.csv").read_bytes(), before)

    def test_dashboard_read_only_sanitized_and_conflicting_approval_flagged(self):
        self.generate()
        self.article.write_text("Changed after verification", encoding="utf-8")
        gate = {"GATE_ID": "GATE-0006", "Name": "Claims", "Status": "COMPLETED",
                "Decision": "APPROVED", "Validated_by": "researcher",
                "Validation_evidence": "reference"}
        self.write("18_Human_Validation_Gates.csv", [gate])
        before = {p: p.read_bytes() for p in self.mgmt.iterdir() if p.is_file()}
        dashboard = visual.view(self.root)
        self.assertEqual(dashboard["scientific"]["source_verification"]["status"], "STALE")
        self.assertEqual(dashboard["scientific"]["gates_approved_with_source_conflicts"], 1)
        exposed = json.dumps(dashboard)
        self.assertNotIn("article.txt", exposed)
        self.assertNotIn("The conceptual model was tested", exposed)
        self.assertEqual(before, {p: p.read_bytes() for p in self.mgmt.iterdir() if p.is_file()})

if __name__ == "__main__":
    unittest.main()
