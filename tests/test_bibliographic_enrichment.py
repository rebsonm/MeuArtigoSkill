"""Offline-only synthetic tests of optional enrichment and user-owned Zotero."""
import json
from pathlib import Path
import sys
import unittest
from urllib.parse import urlparse, parse_qs

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import bibliographic_enrichment as be


class BibliographicEnrichmentTests(unittest.TestCase):
    def test_doi_lookup_default_never_calls_network(self):
        self.assertEqual(be.lookup_doi("unpaywall", "10.1234/example")["status"],
                         "NOT_EXECUTED")
        self.assertEqual(be.lookup_doi("opencitations", "10.1234/example")["status"],
                         "NOT_EXECUTED")

    def test_unpaywall_requires_email(self):
        self.assertEqual(be.lookup_doi("unpaywall", "10.1234/example",
                                       execute=True)["status"], "NOT_CONFIGURED")

    def test_unpaywall_doi_only_and_no_download(self):
        calls = []
        def fake(url, headers):
            calls.append((url, headers))
            return {"is_oa": True, "best_oa_location": {
                "url_for_landing_page": "https://example.org/oa-landing",
                "license": "cc-by"}}
        r = be.lookup_doi("unpaywall", "https://doi.org/10.1234/example",
                          email="support@example.org", execute=True, fetcher=fake)
        self.assertEqual(r["status"], "COMPLETE")
        self.assertTrue(r["is_open_access_reported"])
        self.assertEqual(r["oa_url_reported"], "https://example.org/oa-landing")
        self.assertFalse(r["fulltext_processed"])
        self.assertFalse(r["rights_confirmed"])
        self.assertEqual(parse_qs(urlparse(calls[0][0]).query)["email"],
                         ["support@example.org"])

    def test_opencitations_reports_count_not_article_quality(self):
        r = be.lookup_doi("opencitations", "10.1234/example",
                          execute=True, fetcher=lambda u, h: [{"count": "23"}])
        self.assertEqual(r["incoming_citation_count_reported"], 23)
        self.assertFalse(r["scientific_validated"])

    def test_failed_opencitations_does_not_substitute_zero(self):
        r = be.lookup_doi("opencitations", "10.1234/example",
                          execute=True, fetcher=lambda u, h: [])
        self.assertEqual(r["status"], "INVALID_RESPONSE")
        self.assertNotIn("incoming_citation_count_reported", r)

    def test_zotero_no_credential_no_network(self):
        self.assertEqual(be.list_own_zotero_metadata(
            user_id="2", api_key="", execute=True)["status"], "NOT_CONFIGURED")
        self.assertEqual(be.list_own_zotero_metadata(
            user_id="2", api_key="fake")["status"], "NOT_EXECUTED")

    def test_zotero_user_scoped_header_and_no_private_notes(self):
        calls = []
        def fake(url, headers):
            calls.append((url, headers))
            return [{
                "key": "ITEM001",
                "data": {
                    "itemType": "journalArticle",
                    "title": "Synthetic private bibliography entry",
                    "DOI": "10.1234/test",
                    "date": "2024-04-12",
                    "publicationTitle": "Test Journal",
                    "creators": [{"firstName": "Example", "lastName": "Author"}],
                    "abstractNote": "CONFIDENTIAL_ABSTRACT",
                    "notes": "CONFIDENTIAL_NOTE",
                    "tags": [{"tag": "PRIVATE_TAG"}],
                    "attachments": ["SENSITIVE_ATTACHMENT"],
                }
            }]
        r = be.list_own_zotero_metadata(
            user_id="100", api_key="DO_NOT_LEAK_TOKEN",
            execute=True, fetcher=fake)
        self.assertEqual(r["status"], "COMPLETE")
        self.assertEqual(r["records"][0]["doi"], "10.1234/test")
        self.assertEqual(r["records"][0]["authors"], "Example Author")
        payload = json.dumps(r)
        for secret in ("DO_NOT_LEAK_TOKEN", "CONFIDENTIAL_ABSTRACT",
                       "CONFIDENTIAL_NOTE", "PRIVATE_TAG", "SENSITIVE_ATTACHMENT"):
            self.assertNotIn(secret, payload)
        self.assertEqual(calls[0][1]["Zotero-API-Key"], "DO_NOT_LEAK_TOKEN")
        self.assertTrue(calls[0][0].startswith("https://api.zotero.org/users/100/items"))

    def test_invalid_id_does_not_invoke_authentication(self):
        r = be.list_own_zotero_metadata(
            user_id="../../another_user", api_key="fake", execute=True)
        self.assertEqual(r["status"], "NOT_CONFIGURED")


if __name__ == "__main__":
    unittest.main()
