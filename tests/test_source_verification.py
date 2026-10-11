"""Offline behavioral checks for independent source verification."""
import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/verify_sources.py"
spec = importlib.util.spec_from_file_location("verify_sources", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SourceCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.mgmt = self.root / module.MGMT
        self.mgmt.mkdir()
        self.source = self.root / "readable.txt"
        self.source.write_text("The conceptual model was tested with two independent samples of respondents.\n", encoding="utf-8")
        self.row = {"Evidence_ID": "EVID-001", "DOI_or_persistent_ID": "10.1234/abc",
                    "Title": "Sample model of organizations", "Year": "2020",
                    "Supporting_locator": '"The conceptual model was tested with two independent samples of respondents."',
                    "Source_path": "readable.txt"}

    def fetcher(self, provider, doi, mailto=""):
        self.assertEqual(doi, "10.1234/abc")
        if provider == "crossref":
            return {"status": "FOUND", "data": {"DOI": doi, "title": ["Sample model of organizations"],
                    "published": {"date-parts": [[2020]]}, "author": [{"family": "Silva"}]}}
        return {"status": "FOUND", "data": {"doi": "https://doi.org/" + doi,
                "display_name": "Sample model of organizations", "publication_year": 2020,
                "is_retracted": False}}

    def check(self, row=None, fetcher=None, offline=False):
        return module.verify_row(row or self.row, self.root, {}, fetcher or self.fetcher, offline)

    def test_metadata_and_locator_are_independently_checkable(self):
        report = self.check()
        self.assertEqual(report["metadata_status"], "VERIFIED")
        self.assertEqual(report["locator_status"], "MATCHED")
        self.assertEqual(report["result"], "METADATA_AND_LOCATOR_CHECKED")
        self.assertEqual(report["claim_support_status"], "NOT_SEMANTICALLY_VERIFIED")

    def test_unknown_doi_does_not_pass(self):
        result = self.check(fetcher=lambda *args: {"status": "NOT_FOUND"})
        self.assertEqual(result["metadata_status"], "NOT_FOUND")
        self.assertEqual(result["result"], "FAIL")

    def test_wrong_title_is_not_metadata_verified(self):
        other = dict(self.row, Title="Unrelated evidence and field research")
        report = self.check(other)
        self.assertEqual(report["metadata_status"], "MISMATCH")

    def test_wrong_doi_does_not_pass_even_with_correct_title(self):
        def unexpected_doi(provider, doi, mailto=""):
            payload = self.fetcher(provider, doi, mailto)
            payload["data"]["DOI" if provider == "crossref" else "doi"] = "10.3333/other"
            return payload
        self.assertEqual(self.check(fetcher=unexpected_doi)["metadata_status"], "MISMATCH")

    def test_non_doi_is_not_fabricated(self):
        other = dict(self.row, DOI_or_persistent_ID="ISBN 978-0-1234")
        self.assertEqual(self.check(other)["metadata_status"], "NO_DOI")

    def test_offline_cannot_be_declared_verified(self):
        self.assertEqual(self.check(offline=True)["metadata_status"], "UNVERIFIED")

    def test_missing_locator_and_page_only_are_not_verified(self):
        self.assertEqual(self.check(dict(self.row, Supporting_locator="p. 32"))["locator_status"], "LOCATOR_NOT_CHECKABLE")

    def test_nonexistent_passage_fails(self):
        other = dict(self.row, Supporting_locator='"This totally invented passage cannot be found in the actual local source."')
        self.assertEqual(self.check(other)["locator_status"], "PASSAGE_NOT_FOUND")

    def test_external_document_is_never_downloaded(self):
        other = dict(self.row, Source_path="https://invalid.example/readable.pdf")
        self.assertEqual(self.check(other)["locator_status"], "REMOTE_NOT_DOWNLOADED")

    def test_outside_root_is_rejected(self):
        other = dict(self.row, Source_path="../../private.pdf")
        self.assertEqual(self.check(other)["locator_status"], "OUTSIDE_WORKSPACE")

    def test_retraction_flag_is_not_hidden(self):
        def retracted(provider, doi, mailto=""):
            payload = self.fetcher(provider, doi, mailto)
            if provider == "openalex":
                payload["data"]["is_retracted"] = True
            return payload
        result = self.check(fetcher=retracted)
        self.assertTrue(result["retraction_alert"])
        self.assertEqual(result["result"], "REVIEW_REQUIRED")

    def test_service_outage_is_not_absence(self):
        status = self.check(fetcher=lambda *args: {"status": "ERROR"})
        self.assertEqual(status["metadata_status"], "UNVERIFIED")
        self.assertEqual(status["result"], "REVIEW_REQUIRED")

    def test_report_binds_input_hash_and_does_not_copy_copyrighted_passage(self):
        matrix = self.mgmt / "05_Evidence_Matrix.csv"
        with matrix.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(self.row))
            writer.writeheader()
            writer.writerow(self.row)
        report = module.verify_project(self.root, fetcher=self.fetcher)
        self.assertEqual(report["summary"]["checked"], 1)
        self.assertEqual(report["input_sha256"], module.digest(matrix))
        self.assertNotIn("The conceptual model was tested", json.dumps(report))


if __name__ == "__main__":
    unittest.main()
