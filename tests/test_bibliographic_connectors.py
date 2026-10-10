"""Deterministic engineering tests only, never a live literature search."""
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import bibliographic_connectors as bc
import bibliographic_workflow as bw
import init_project


def oa(title="Synthetic journal work", doi="https://doi.org/10.1234/example"):
    return {
        "id": "https://openalex.org/W123", "display_name": title,
        "doi": doi, "publication_year": 2024,
        "authorships": [{"author": {"display_name": "Example Researcher"}}],
        "primary_location": {"landing_page_url": "https://example.org/work",
                             "source": {"display_name": "Test Journal"}},
    }


def cr(title="Synthetic journal work"):
    return {
        "DOI": "10.1234/example", "title": [title], "type": "journal-article",
        "published": {"date-parts": [[2024, 1, 1]]},
        "author": [{"given": "Example", "family": "Researcher"}],
        "container-title": ["Test Journal"], "URL": "https://doi.org/10.1234/example",
    }


class OptionalConnectorTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.mgmt = self.root / bw.MGMT
        self.mgmt.mkdir()
        (self.mgmt / "PROJECT_CONFIG.json").write_text(json.dumps({
            "storage_policy": "GOOGLE_DRIVE_FIRST",
            "storage_mode": "WORK_FALLBACK", "fallback_authorized": True,
        }), encoding="utf-8")
        for name in (bw.SEARCH, bw.SCREENING, bw.TRACE):
            bw._atomic_csv(self.root / name, init_project.TABLES[name], [])

    def test_absent_config_api_disabled(self):
        self.assertEqual(bw.optional_config({}), {"enabled": False, "providers": {}})
        self.assertEqual(bw.optional_config({"bibliographic_connectors": None}),
                         {"enabled": False, "providers": {}})

    def test_capabilities_licensed_are_not_claimed_available(self):
        for name in bc.LOCKED:
            d = bc.capabilities(name)
            self.assertFalse(d["metadata_search"])
            self.assertEqual(d["availability"], "LICENCE_AND_EXECUTOR_REVIEW_REQUIRED")

    def test_no_request_without_opt_in(self):
        def unexpected(*_args):
            raise AssertionError("A network call would violate default mode")
        result = bc.search("openalex", "scientific literacy", fetcher=unexpected)
        self.assertEqual(result.status, "NOT_EXECUTED")
        self.assertIsNone(result.executed_at)

    def test_openalex_normalizes_metadata_without_abstract(self):
        urls = []
        def fake(url, headers):
            urls.append(url)
            return {"meta": {"count": 1}, "results": [oa()]}
        result = bc.search("openalex", "scientific literacy", limit=5, fetcher=fake,
                           execute=True)
        self.assertEqual(result.status, "COMPLETE")
        self.assertEqual(result.reported_total, 1)
        self.assertEqual(result.rows[0]["doi"], "10.1234/example")
        self.assertEqual(result.rows[0]["authors"], "Example Researcher")
        self.assertNotIn("abstract", result.rows[0])
        self.assertEqual(parse_qs(urlsplit(urls[0]).query)["search"], ["scientific literacy"])

    def test_crossref_page_cursor_not_offset(self):
        urls = []
        def fake(url, headers):
            urls.append(url)
            if len(urls) == 1:
                return {"message": {"total-results": 150,
                                    "next-cursor": "paging-2",
                                    "items": [cr() for _ in range(100)]}}
            return {"message": {"total-results": 150,
                                "next-cursor": "paging-3",
                                "items": [cr() for _ in range(15)]}}
        outcome = bc.search("crossref", "evidence governance", limit=125,
                            fetcher=fake, execute=True)
        self.assertEqual(outcome.status, "PARTIAL")
        self.assertEqual(len(outcome.rows), 115)
        self.assertEqual(outcome.pages_received, 2)
        self.assertEqual(parse_qs(urlsplit(urls[0]).query)["cursor"], ["*"])
        self.assertEqual(parse_qs(urlsplit(urls[1]).query)["cursor"], ["paging-2"])

    def test_semantic_scholar_uses_own_search_semantics_and_redacts_api_key(self):
        calls = []
        def fake(url, headers):
            calls.append((url, headers))
            return {"total": 1, "data": [{
                "paperId": "PAPER01", "title": "Governance of evidence",
                "year": 2025, "venue": "Test Venue",
                "authors": [{"name": "Example Author"}],
                "externalIds": {"DOI": "10.1234/sample"},
                "url": "https://www.semanticscholar.org/paper/PAPER01",
                "abstract": "CONFIDENTIAL_NOT_FOR_EXPORT",
            }]}
        result = bc.search("semantic_scholar", "governance evidence",
                           api_key="DO_NOT_LOG_SEMANTIC_KEY",
                           execute=True, fetcher=fake)
        self.assertEqual(result.status, "COMPLETE")
        self.assertEqual(result.rows[0]["doi"], "10.1234/sample")
        self.assertEqual(result.rows[0]["authors"], "Example Author")
        self.assertNotIn("CONFIDENTIAL_NOT_FOR_EXPORT", json.dumps(result.rows))
        self.assertEqual(calls[0][1]["x-api-key"], "DO_NOT_LOG_SEMANTIC_KEY")
        self.assertNotIn("DO_NOT_LOG_SEMANTIC_KEY", calls[0][0])
        self.assertEqual(parse_qs(urlsplit(calls[0][0]).query)["query"],
                         ["governance evidence"])

    def test_throttling_avoids_invented_success(self):
        def rate_limited(url, headers):
            raise bc.ProviderFailure("RATE_LIMITED")
        result = bc.search("crossref", "topic", fetcher=rate_limited, execute=True)
        self.assertEqual(result.status, "RATE_LIMITED")
        self.assertEqual(result.rows, [])

    def test_locked_connector_never_calls_api(self):
        self.assertEqual(bc.search("scopus", "topic", execute=True).status,
                         "LICENSE_BLOCKED")

    def test_export_omits_secrets_and_covers_csv_formula_injection(self):
        result = bc.search("openalex", "topic", execute=True, api_key="TOP_SECRET_TEST_KEY",
                           fetcher=lambda url, headers: {
                               "meta": {"count": 1},
                               "results": [oa(title="=HYPERLINK(\"evil\")")]})
        out = self.root / "staging"
        receipt = bw.export_staging(self.root, out, result)
        data = (out / "openalex_metadata.csv").read_text(encoding="utf-8-sig")
        report = (out / "retrieval_receipt.json").read_text(encoding="utf-8")
        self.assertIn("'=HYPERLINK", data)
        self.assertNotIn("TOP_SECRET_TEST_KEY", data + report)
        self.assertEqual(receipt["kind"],
                         "LOCAL_EXECUTION_RECORD_NOT_INDEPENDENT_PROVIDER_RECEIPT")
        self.assertFalse(receipt["drive_sync_verified"])

    def test_local_commit_preserves_scientific_gates_and_ids(self):
        result = bc.search("openalex", "synthetic search", execute=True,
                           fetcher=lambda url, h: {
                               "meta": {"count": 1}, "results": [oa()]})
        out = self.root / "stage"
        bw.export_staging(self.root, out, result)
        p = out / "openalex_metadata.csv"
        receipt = bw.commit_to_authorized_local_project(self.root, result, p)
        self.assertEqual(receipt["new_records"], 1)
        rows = bw._read_rows(self.root / bw.SCREENING,
                             init_project.TABLES[bw.SCREENING])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Title"], "Synthetic journal work")
        self.assertEqual(rows[0]["Pass1_decision"], "")
        self.assertEqual(rows[0]["Abstract"], "")
        self.assertFalse(receipt["scientific_approval"])
        self.assertEqual(receipt["Search_ID"], rows[0]["Search_ID"])
        with self.assertRaises(ValueError):
            bw.commit_to_authorized_local_project(self.root, result, p)

    def test_drive_storage_cannot_claim_automatic_sync(self):
        cfg = self.mgmt / "PROJECT_CONFIG.json"
        cfg.write_text(json.dumps({"storage_mode": "GOOGLE_DRIVE_STAGING",
                                   "storage_policy": "GOOGLE_DRIVE_FIRST"}),
                       encoding="utf-8")
        result = bc.search("openalex", "test", execute=True,
                           fetcher=lambda url, h: {
                               "meta": {"count": 1}, "results": [oa()]})
        out = self.root / "staging"
        bw.export_staging(self.root, out, result)
        with self.assertRaises(ValueError):
            bw.commit_to_authorized_local_project(self.root, result,
                                                    out / "openalex_metadata.csv")

    def test_opt_in_can_be_reversed_without_keys_or_network(self):
        self.assertEqual(bw.optional_config(bw._read_config(self.root))["enabled"], False)
        state = bw.set_provider_preference(self.root, "openalex", True)
        self.assertTrue(state["enabled"])
        self.assertFalse(state["is_authorized_provider_credential"])
        self.assertFalse(state["drive_sync_verified"])
        cfg = bw._read_config(self.root)
        self.assertTrue(cfg["bibliographic_connectors"]["enabled"])
        self.assertEqual(cfg["bibliographic_connectors"]["providers"]["openalex"], {
            "enabled": True,
            "credential_verified": False,
            "provider_licence_verified": False})
        state = bw.set_provider_preference(self.root, "openalex", False)
        self.assertFalse(state["enabled"])
        self.assertFalse(bw.optional_config(bw._read_config(self.root))["enabled"])

    def test_local_preference_cannot_change_drive_canonical_project(self):
        path = self.mgmt / "PROJECT_CONFIG.json"
        path.write_text(json.dumps({"storage_mode": "GOOGLE_DRIVE_STAGING"}),
                        encoding="utf-8")
        before = path.read_bytes()
        with self.assertRaises(ValueError):
            bw.set_provider_preference(self.root, "openalex", True)
        self.assertEqual(path.read_bytes(), before)

    def test_manual_mode_help_does_not_require_provider(self):
        self.assertEqual(bw.run(["status", "--project", str(self.root)]), 0)
        self.assertEqual(bw.run(["guide", "--lang", "pt"]), 0)

    def test_cli_search_without_network_not_executed(self):
        out = self.root / "empty"
        self.assertEqual(bw.run(["search", "--provider", "openalex",
                                 "--query", "sample", "--out-dir", str(out)]), 0)
        self.assertFalse(out.exists())

    def test_reused_existing_hybrid_dedup(self):
        a = self.root / "manual_scopus.csv"
        b = self.root / "openalex_metadata.csv"
        bw._atomic_csv(a, ["title", "doi", "authors", "year"], [
            {"title": "Original", "doi": "10.1234/example",
             "authors": "Example Researcher", "year": "2024"}])
        bw._atomic_csv(b, ["title", "doi", "authors", "year"], [
            {"title": "Alternate title", "doi": "https://doi.org/10.1234/example",
             "authors": "Example Researcher", "year": "2024"}])
        out = self.root / "hybrid"
        code = bw.run(["dedupe", str(a), str(b), "--out-dir", str(out)])
        self.assertEqual(code, 0)
        with (out / "consolidated_exact_dedup.csv").open(encoding="utf-8-sig") as f:
            self.assertEqual(len(list(csv.DictReader(f))), 1)
        with (out / "exact_duplicate_audit.csv").open(encoding="utf-8-sig") as f:
            audits = list(csv.DictReader(f))
        self.assertEqual(len(audits), 1)
        self.assertEqual(audits[0]["reason"], "exact_doi")


if __name__ == "__main__":
    unittest.main()
