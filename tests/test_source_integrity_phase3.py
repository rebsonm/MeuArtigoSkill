"""Phase 3 synthetic source-verification integrity and provenance regressions.

No external API or real researcher assertions are used. Metadata identity,
editorial notices and literal source passages are not semantic peer review.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import verify_sources as verify
import source_report_integrity as integrity

MGMT = "00_Gestao_e_Continuidade"
DOI = "10.1234/fictitious-model"


def write_csv(path, headers, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


class SourceIntegrityPhase3Tests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name) / "research"
        self.mgmt = self.root / MGMT
        self.mgmt.mkdir(parents=True)
        (self.root / "source.txt").write_text(
            "The researchers compared two independently collected organizational samples.\n",
            encoding="utf-8")
        write_csv(self.mgmt / "05_Evidence_Matrix.csv",
                  ["Evidence_ID", "DOI_or_persistent_ID", "Title", "Year",
                   "Supporting_locator", "Source_path"],
                  [{"Evidence_ID": "EVID-0001", "DOI_or_persistent_ID": DOI,
                    "Title": "Synthetic model and organizations", "Year": "2022",
                    "Supporting_locator": '"The researchers compared two independently collected organizational samples."',
                    "Source_path": "source.txt"}])
        write_csv(self.mgmt / "03_Screening.csv",
                  ["Record_ID", "Title", "Year", "DOI", "Authors"],
                  [{"Record_ID": "REC-0001",
                    "Title": "Synthetic model and organizations",
                    "Year": "2022", "DOI": DOI, "Authors": "Silva"}])
        write_csv(self.mgmt / "04_FullText_Tracker.csv",
                  ["Record_ID", "Evidence_matrix_id", "File_or_URL"],
                  [{"Record_ID": "REC-0001", "Evidence_matrix_id": "EVID-0001",
                    "File_or_URL": "source.txt"}])
        self.report = self.mgmt / "SOURCE_VERIFICATION.json"

    def provider(self, name, doi, mailto=""):
        self.assertEqual(doi, DOI)
        if name == "crossref":
            return {"status": "FOUND", "data": {
                "DOI": doi, "title": ["Synthetic model and organizations"],
                "published": {"date-parts": [[2022]]},
                "author": [{"family": "Silva"}]}}
        return {"status": "FOUND", "data": {
            "doi": "https://doi.org/" + doi,
            "display_name": "Synthetic model and organizations",
            "publication_year": 2022, "is_retracted": False}}

    def generate(self, provider=None):
        report = verify.verify_project(self.root, fetcher=provider or self.provider)
        self.save(report)
        return report

    def save(self, report):
        self.report.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")

    def test_clean_crossref_openalex_and_local_source_are_recorded_not_semantically_proved(self):
        report = self.generate()
        entry = report["checks"][0]
        self.assertEqual(entry["metadata_status"], "VERIFIED")
        self.assertEqual(entry["locator_status"], "MATCHED")
        self.assertEqual(entry["claim_support_status"], "NOT_SEMANTICALLY_VERIFIED")
        self.assertEqual(len(entry["metadata_checks"]), 2)
        self.assertTrue(all(len(x["response_sha256"]) == 64
                            for x in entry["metadata_checks"]))
        self.assertEqual(integrity.assess(self.root)["status"], "RECORDED_CLEAR")

    def test_online_provider_failure_is_review_required_even_when_other_matches(self):
        def partial(name, doi, mailto=""):
            return ({"status": "ERROR", "reason": "SyntheticProviderOutage"}
                    if name == "crossref" else self.provider(name, doi, mailto))
        report = self.generate(provider=partial)
        entry = report["checks"][0]
        self.assertEqual(entry["metadata_status"], "VERIFIED")
        self.assertIn("CROSSREF_UNAVAILABLE", entry["provider_warnings"])
        self.assertEqual(entry["result"], "REVIEW_REQUIRED")
        self.assertEqual(integrity.assess(self.root)["status"], "REVIEW_REQUIRED")

    def test_false_clear_unverified_offline_metadata_does_not_pass(self):
        report = self.generate()
        report["offline"] = True
        self.save(report)
        self.assertEqual(integrity.assess(self.root)["status"], "BLOCKED")

    def test_false_clear_missing_provider_identity_evidence_does_not_pass(self):
        report = self.generate()
        report["checks"][0]["metadata_checks"] = []
        self.save(report)
        self.assertEqual(integrity.assess(self.root)["status"], "BLOCKED")

    def test_false_clear_wrong_local_source_sha_does_not_pass(self):
        report = self.generate()
        report["checks"][0]["source_sha256"] = "0" * 64
        self.save(report)
        self.assertEqual(integrity.assess(self.root)["status"], "BLOCKED")

    def test_retraction_notice_cannot_be_hidden_behind_clear_outcome(self):
        report = self.generate()
        report["checks"][0]["editorial_notices"] = [
            {"direction": "UPDATES_THIS_WORK", "kind": "retraction",
             "notice_doi": "10.1234/synthetic-notice", "provider": "crossref"}]
        self.save(report)
        self.assertEqual(integrity.assess(self.root)["status"], "BLOCKED")

    def test_an_actual_retraction_is_alerted_without_claiming_semantic_judgment(self):
        def retracted(name, doi, mailto=""):
            item = self.provider(name, doi, mailto)
            if name == "openalex":
                item["data"]["is_retracted"] = True
            return item
        report = self.generate(provider=retracted)
        entry = report["checks"][0]
        self.assertTrue(entry["retraction_alert"])
        self.assertEqual(entry["result"], "REVIEW_REQUIRED")
        self.assertEqual(integrity.assess(self.root)["status"], "REVIEW_REQUIRED")

    def test_concurrent_change_during_provider_lookup_does_not_produce_false_fresh_report(self):
        original = (self.mgmt / "03_Screening.csv").read_bytes()
        changed = False
        def mutate(name, doi, mailto=""):
            nonlocal changed
            if not changed:
                changed = True
                (self.mgmt / "03_Screening.csv").write_bytes(original + b"\n")
            return self.provider(name, doi, mailto)
        with self.assertRaisesRegex(ValueError, "SOURCE_INPUTS_CHANGED"):
            verify.verify_project(self.root, fetcher=mutate)

    def test_atomic_report_write_preserves_previous_report_on_write_failure(self):
        self.report.write_bytes(b"historical-preserve\n")
        with patch.object(verify.os, "replace", side_effect=OSError("disk full")):
            self.assertEqual(verify.main([str(self.root), "--offline"]), 1)
        self.assertEqual(self.report.read_bytes(), b"historical-preserve\n")
        self.assertFalse(list(self.mgmt.glob(".source-verification-*.tmp")))


if __name__ == "__main__":
    unittest.main()
