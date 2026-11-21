"""REG-018: deterministic adversarial tests of read-only citation reconciliation.

All records, DOIs and file passages are synthetic fixtures. No provider calls.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import reference_audit as audit
from source_report_integrity import manifest, sha256


def write_csv(path, headers, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)


class ReferenceAuditTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.mgmt = self.root / audit.MGMT
        self.mgmt.mkdir()
        (self.root / "paper.txt").write_text(
            "This hypothetical study used two samples for a descriptive comparison.",
            encoding="utf-8")
        self.evidence = [{
            "Evidence_ID": "EVID-0001", "Citation": "Synthetic Doe (2022)",
            "DOI_or_persistent_ID": "10.1234/synthetic-case",
        }]
        self.claims = [{
            "Claim_ID": "CLAIM-0001", "Claim_type": "[L]",
            "Evidence_IDs": "EVID-0001",
        }]
        self.save_inputs()

    def save_inputs(self):
        write_csv(self.mgmt / audit.EVIDENCE,
                  ["Evidence_ID", "Citation", "DOI_or_persistent_ID"], self.evidence)
        write_csv(self.mgmt / audit.CLAIMS,
                  ["Claim_ID", "Claim_type", "Evidence_IDs"], self.claims)
        write_csv(self.mgmt / "03_Screening.csv",
                  ["Record_ID"], [{"Record_ID": "REC-0001"}])
        write_csv(self.mgmt / "04_FullText_Tracker.csv",
                  ["Record_ID", "Evidence_matrix_id", "File_or_URL"],
                  [{"Record_ID": "REC-0001", "Evidence_matrix_id": "EVID-0001",
                    "File_or_URL": "paper.txt"}])

    def save_report(self, *, metadata="VERIFIED", retracted=False,
                    corrected=False, warnings=None, locator="MATCHED"):
        files = manifest(self.root)
        row = {
            "Evidence_ID": "EVID-0001", "Record_ID": "REC-0001",
            "doi": "10.1234/synthetic-case",
            "metadata_status": metadata,
            "metadata_checks": [{"provider": "crossref", "status":
                                 "VERIFIED" if metadata == "VERIFIED" else "TITLE_MISMATCH"}]
                                 if metadata in {"VERIFIED", "MISMATCH"} else [],
            "locator_status": locator, "source_path": "paper.txt",
            "source_sha256": sha256(self.root / "paper.txt"), "retraction_alert": retracted,
            "correction_alert": corrected, "update_alert": False,
            "provider_warnings": warnings or [], "editorial_notices": [],
            "result": "FAIL" if metadata in {"MISMATCH", "INVALID_DOI", "NOT_FOUND"} or locator in {
                "PASSAGE_NOT_FOUND", "PAGE_MISMATCH"} else (
                "REVIEW_REQUIRED" if metadata != "VERIFIED" or retracted or corrected or warnings or locator != "MATCHED"
                else "METADATA_AND_LOCATOR_CHECKED"
            )
        }
        self.report = self.mgmt / audit.SOURCE_REPORT
        self.report.write_text(json.dumps({
            "schema_version": 2, "offline": False, "input_manifest": files,
            "checks": [row]}, ensure_ascii=False), encoding="utf-8")

    def codes(self, result=None):
        return [x["code"] for x in (result or audit.audit(self.root))["findings"]]

    def test_absent_source_report_is_unverified_and_no_semantic_conclusion(self):
        result = audit.audit(self.root)
        self.assertIn("SOURCE_REPORT_MISSING", self.codes(result))
        self.assertFalse(result["semantic_support_proven"])
        self.assertFalse(result["full_manuscript_citations_audited"])
        self.assertFalse(result["google_drive_sync_verified"])

    def test_clean_report_only_confirms_bibliographic_coverage(self):
        self.save_report()
        result = audit.audit(self.root)
        self.assertEqual(result["source_report_status"], "RECORDED_CLEAR")
        self.assertEqual(result["finding_counts"], {})
        self.assertEqual(result["referenced_evidence_count"], 1)
        self.assertFalse(result["semantic_support_proven"])

    def test_nonexistent_evidence_id_and_missing_literature_link(self):
        self.claims = [
            {"Claim_ID": "CLAIM-0001", "Claim_type": "[L]",
             "Evidence_IDs": "EVID-9099"},
            {"Claim_ID": "CLAIM-0002", "Claim_type": "L", "Evidence_IDs": ""}
        ]
        self.save_inputs()
        result = audit.audit(self.root)
        self.assertIn("UNKNOWN_REFERENCE", self.codes(result))
        self.assertIn("LITERATURE_CLAIM_WITHOUT_REFERENCE", self.codes(result))

    def test_duplicate_doi_requires_review_not_automatic_deletion(self):
        self.evidence.append({
            "Evidence_ID": "EVID-0002", "Citation": "Doe (2022), alternative source",
            "DOI_or_persistent_ID": "https://doi.org/10.1234/synthetic-case"})
        self.save_inputs()
        self.assertIn("DUPLICATE_DOI", self.codes())

    def test_duplicate_evidence_id_is_blocked(self):
        self.evidence.append(dict(self.evidence[0]))
        self.save_inputs()
        self.assertIn("DUPLICATE_REFERENCE_ID", self.codes())
        self.assertIn("AMBIGUOUS_REFERENCE", self.codes())

    def test_malformed_doi_not_flagged_as_not_found_in_providers(self):
        self.evidence[0]["DOI_or_persistent_ID"] = "doi: not-valid"
        self.save_inputs()
        codes = self.codes()
        self.assertIn("INVALID_DOI", codes)
        self.assertNotIn("SOURCE_DOI_NOT_FOUND", codes)

    def test_book_without_doi_is_not_called_fraud(self):
        self.evidence[0]["DOI_or_persistent_ID"] = "ISBN 978-1-234"
        self.save_inputs()
        codes = self.codes()
        self.assertIn("REFERENCE_WITHOUT_DOI", codes)
        self.assertNotIn("INVALID_DOI", codes)

    def test_source_metadata_mismatch_blocks_without_semantic_claim(self):
        self.save_report(metadata="MISMATCH")
        result = audit.audit(self.root)
        self.assertIn("SOURCE_METADATA_MISMATCH", self.codes(result))
        self.assertEqual(result["source_report_status"], "BLOCKED")
        self.assertFalse(result["semantic_support_proven"])

    def test_retraction_is_review_not_automatic_exclusion(self):
        self.save_report(retracted=True)
        result = audit.audit(self.root)
        self.assertIn("SOURCE_RETRACTION_ALERT", self.codes(result))
        self.assertEqual(result["finding_counts"].get("BLOCK",0), 0)

    def test_partial_provider_success_is_review(self):
        self.save_report(warnings=["OPENALEX_UNAVAILABLE"])
        self.assertIn("SOURCE_PROVIDER_PARTIAL", self.codes())

    def test_stale_source_report_cannot_certify_identity(self):
        self.save_report()
        self.evidence[0]["Citation"] = "Changed source citation"
        self.save_inputs()
        result = audit.audit(self.root)
        self.assertIn("SOURCE_REPORT_STALE", self.codes(result))
        self.assertNotEqual(result["source_report_status"], "RECORDED_CLEAR")

    def test_objective_locator_conflict_is_reported(self):
        self.save_report(locator="PASSAGE_NOT_FOUND")
        self.assertIn("SOURCE_LOCATOR_CONFLICT", self.codes())

    def test_no_private_titles_or_fulltext_are_exported(self):
        self.evidence[0]["Citation"] = "Secret synthetic long title for privacy check"
        self.save_inputs()
        result = audit.audit(self.root)
        raw = json.dumps(result)
        self.assertNotIn("Secret synthetic", raw)
        self.assertNotIn("This hypothetical study", raw)
        self.assertNotIn(str(self.root), raw)

    def test_explicit_local_report_never_overwrites_canonical_data(self):
        before = (self.mgmt / audit.EVIDENCE).read_bytes()
        result = audit.audit(self.root)
        target = self.root / "98_Technical_Reports" / "reference_audit.json"
        audit._write_output(self.root, target, result)
        self.assertTrue(target.is_file())
        self.assertEqual((self.mgmt / audit.EVIDENCE).read_bytes(), before)
        with self.assertRaisesRegex(ValueError, "98_Technical_Reports"):
            audit._write_output(self.root, self.mgmt/audit.EVIDENCE, result)

    def test_output_must_stay_in_project(self):
        with self.assertRaisesRegex(ValueError, "within"):
            audit._write_output(self.root, self.root.parent/"outside.json", audit.audit(self.root))

if __name__ == "__main__":
    unittest.main()
