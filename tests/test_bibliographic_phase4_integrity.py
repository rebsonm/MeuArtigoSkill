"""Phase 4: mocked provider outage, pagination, staging and source provenance.

Only synthetic bibliographic metadata and temporary workspaces are used.
An engineering receipt is not an external provider attestation or human review.
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
import bibliographic_connectors as bc
import bibliographic_workflow as bw
import init_project


def sample(n=0):
    return {"id": f"https://openalex.org/W{n+1}",
            "display_name": f"Synthetic bibliographic record {n+1}",
            "doi": f"https://doi.org/10.1234/synthetic-{n+1}",
            "publication_year": 2024,
            "authorships": [{"author": {"display_name": "Synthetic Researcher"}}],
            "primary_location": {
                "landing_page_url": "https://example.org/fictional",
                "source": {"display_name": "Synthetic Journal"}}}


class OptionalProviderPhase4Tests(unittest.TestCase):
    def test_second_page_rate_limit_preserves_received_work_and_error(self):
        count = 0
        def fetch(url, headers):
            nonlocal count
            count += 1
            if count == 1:
                return {"meta": {"count": 105}, "results": [sample(i) for i in range(100)]}
            raise bc.ProviderFailure("RATE_LIMITED")
        out = bc.search("openalex", "synthetic query", limit=105, execute=True, fetcher=fetch)
        self.assertEqual(out.status, "PARTIAL")
        self.assertEqual(out.error_code, "RATE_LIMITED")
        self.assertEqual(len(out.rows), 100)
        self.assertEqual(out.pages_received, 1)

    def test_malformed_row_is_not_silently_discarded_as_full_coverage(self):
        out = bc.search("openalex", "synthetic", execute=True,
            fetcher=lambda url, hdr: {"meta": {"count": 2},
                "results": [sample(), "INVALID_OBJECT"]})
        self.assertEqual(out.status, "INVALID_RESPONSE")
        self.assertEqual(out.rows, [])
        self.assertEqual(out.pages_received, 0)

    def test_malformed_nested_metadata_is_sanitized_as_provider_error(self):
        wrong = sample()
        wrong["primary_location"] = ["not-a-dictionary"]
        out = bc.search("openalex", "synthetic", execute=True,
            fetcher=lambda url, hdr: {"meta": {"count": 1}, "results": [wrong]})
        self.assertEqual(out.status, "INVALID_RESPONSE")
        self.assertEqual(out.rows, [])

    def test_malformed_later_page_keeps_prior_pages_without_false_success(self):
        calls = 0
        def fake(url, headers):
            nonlocal calls
            calls += 1
            if calls == 1:
                return {"meta": {"count": 101}, "results": [sample(i) for i in range(100)]}
            return {"meta": {"count": 101}, "results": [{"id": "bad", "primary_location": [1]}]}
        out = bc.search("openalex", "synthetic", limit=101, execute=True, fetcher=fake)
        self.assertEqual(out.status, "PARTIAL")
        self.assertEqual(out.error_code, "INVALID_RESPONSE")
        self.assertEqual(out.pages_received, 1)
        self.assertEqual(len(out.rows), 100)

    def test_missing_crossref_cursor_on_full_page_marks_partial(self):
        def fake(url, headers):
            return {"message": {"total-results": 105,
                                "items": [{"DOI": "10.1234/synthetic",
                                           "title": ["Synthetic"]} for _ in range(100)]}}
        out = bc.search("crossref", "synthetic", limit=105, execute=True, fetcher=fake)
        self.assertEqual(out.status, "PARTIAL")
        self.assertEqual(out.error_code, "PAGINATION_INCOMPLETE")
        self.assertEqual(out.pages_received, 1)

    def test_crossref_unknown_total_and_no_cursor_is_not_complete(self):
        def fake(url, headers):
            return {"message": {"items": [
                {"DOI": "10.1234/synthetic", "title": ["Synthetic"]}
                for _ in range(100)]}}
        out = bc.search("crossref", "synthetic", limit=105, execute=True, fetcher=fake)
        self.assertEqual(out.status, "PARTIAL")
        self.assertEqual(out.error_code, "PAGINATION_INCOMPLETE")

    def test_known_zero_results_remains_valid_nonfabricated_empty_search(self):
        out = bc.search("openalex", "synthetic", limit=25, execute=True,
                        fetcher=lambda url, headers: {"meta": {"count": 0}, "results": []})
        self.assertEqual(out.status, "COMPLETE")
        self.assertEqual(out.rows, [])
        self.assertIsNone(out.error_code)


class AuthorizedBibliographyReceiptTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "research"
        self.mgmt = self.root / bw.MGMT
        self.mgmt.mkdir(parents=True)
        (self.mgmt / "PROJECT_CONFIG.json").write_text(json.dumps({
            "storage_mode": "WORK_FALLBACK",
            "fallback_authorized": True
        }), encoding="utf-8")
        for table in (bw.SEARCH, bw.SCREENING, bw.TRACE):
            bw._atomic_csv(self.root / table, init_project.TABLES[table], [])
        self.before = {name: (self.root / name).read_bytes()
                       for name in (bw.SEARCH, bw.SCREENING, bw.TRACE)}
        self.outcome = bc.search("openalex", "fictional search", limit=5,
                                 fetcher=lambda url, headers: {
                                     "meta": {"count": 1}, "results": [sample()]},
                                 execute=True)
        self.stage = self.root / "STAGING"
        self.receipt = bw.export_staging(self.root, self.stage, self.outcome)
        self.export = self.stage / "openalex_metadata.csv"

    def unchanged(self):
        for name, original in self.before.items():
            self.assertEqual((self.root / name).read_bytes(), original, name)

    def test_complete_staging_can_be_imported_without_scientific_approval(self):
        r = bw.commit_to_authorized_local_project(self.root, self.outcome, self.export)
        self.assertEqual(r["new_records"], 1)
        self.assertFalse(r["drive_synced"])
        self.assertFalse(r["scientific_approval"])
        searches = bw._read_rows(self.root / bw.SEARCH, init_project.TABLES[bw.SEARCH])
        self.assertEqual(len(searches), 1)
        self.assertIn(self.receipt["export_sha256"], searches[0]["Notes"])
        self.assertIn("provider_error=NONE", searches[0]["Notes"])
        trace = bw._read_rows(self.root / bw.TRACE, init_project.TABLES[bw.TRACE])
        self.assertEqual(trace[0]["Status"], "UNVERIFIED")

    def test_mutated_staging_csv_is_rejected_without_touching_canonical_data(self):
        self.export.write_bytes(self.export.read_bytes() + b"\n")
        with self.assertRaisesRegex(ValueError, "STAGED_RECEIPT_OR_EXPORT_CHANGED"):
            bw.commit_to_authorized_local_project(self.root, self.outcome, self.export)
        self.unchanged()

    def test_falsified_receipt_is_rejected_without_write(self):
        path = self.stage / "retrieval_receipt.json"
        altered = json.loads(path.read_text(encoding="utf-8"))
        altered["status"] = "PARTIAL"
        path.write_text(json.dumps(altered), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "STAGED_RECEIPT_OR_EXPORT_CHANGED"):
            bw.commit_to_authorized_local_project(self.root, self.outcome, self.export)
        self.unchanged()

    def test_modified_in_memory_results_are_not_imported_against_old_export(self):
        self.outcome.rows[0]["title"] = "Modified after staging"
        with self.assertRaisesRegex(ValueError, "STAGED_ROWS_DIFFER_FROM_RETRIEVAL"):
            bw.commit_to_authorized_local_project(self.root, self.outcome, self.export)
        self.unchanged()

    def test_forged_export_path_outside_authorized_project_is_denied(self):
        other = self.root.parent / "outside-staging.csv"
        other.write_bytes(self.export.read_bytes())
        with self.assertRaisesRegex(ValueError, "STAGED_EXPORT_MUST_BE_IN_AUTHORIZED_WORKSPACE"):
            bw.commit_to_authorized_local_project(self.root, self.outcome, other)
        self.unchanged()

    def test_repeating_same_stage_does_not_destroy_older_receipt(self):
        original_csv = self.export.read_bytes()
        original_receipt = (self.stage / "retrieval_receipt.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "STAGING_EXPORT_ALREADY_EXISTS"):
            bw.export_staging(self.root, self.stage, self.outcome)
        self.assertEqual(self.export.read_bytes(), original_csv)
        self.assertEqual((self.stage / "retrieval_receipt.json").read_bytes(), original_receipt)

    def test_partial_real_response_preserves_diagnostic_in_search_and_trace(self):
        self.outcome.status = "PARTIAL"
        self.outcome.error_code = "RATE_LIMITED"
        self.stage.joinpath("retrieval_receipt.json").unlink()
        self.export.unlink()
        receipt = bw.export_staging(self.root, self.stage, self.outcome)
        self.assertEqual(receipt["status"], "PARTIAL")
        written = bw.commit_to_authorized_local_project(self.root, self.outcome, self.export)
        self.assertEqual(written["new_records"], 1)
        search_rows = bw._read_rows(self.root / bw.SEARCH, init_project.TABLES[bw.SEARCH])
        trace_rows = bw._read_rows(self.root / bw.TRACE, init_project.TABLES[bw.TRACE])
        self.assertEqual(search_rows[0]["Status"], "PARTIAL")
        self.assertIn("provider_error=RATE_LIMITED", search_rows[0]["Notes"])
        self.assertIn("partial=True", trace_rows[0]["Notes"])
        self.assertEqual(trace_rows[0]["Status"], "UNVERIFIED")

    def test_no_api_manual_project_configuration_is_unaffected(self):
        self.assertFalse(bw.optional_config(bw._read_config(self.root))["enabled"])
        self.assertEqual(bc.search("openalex", "not opted in").status, "NOT_EXECUTED")
        self.unchanged()


if __name__ == "__main__":
    unittest.main()
