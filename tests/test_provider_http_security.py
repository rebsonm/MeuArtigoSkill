"""Security regressions for optional metadata APIs; entirely mocked and offline.

No live API account, real token, private Zotero library, or external full text
is accessed. Redirect behavior must fail closed even with BYOC credentials.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

import sys
SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import bibliographic_connectors as bc
import bibliographic_enrichment as be
import provider_http_security as net


class NoRedirectSecurityTests(unittest.TestCase):
    def test_provider_host_allowlist_refuses_confusable_and_insecure_urls(self):
        attacks = (
            "http://api.zotero.org/users/123/items",
            "https://api.zotero.org.evil.example/users/123/items",
            "https://api.zotero.org@evil.example/users/123/items",
            "https://api.zotero.org:444/users/123/items",
            "https://api.zotero.org:notaport/users/123/items",
            "https://api.zotero.org/users/123/items#token",
            "https://api.openalex.org/works?search=x" + chr(10) + "evil",
            "https://api.crossref.org/works-extra?query=secret",
            "https://api.openalex.org/works/secret?query=test",
            "https://api.unpaywall.org.evil.example/v2/10.1234/a",
        )
        for url in attacks:
            with self.subTest(url=url), self.assertRaisesRegex(
                bc.ProviderFailure, "UNSUPPORTED_ENDPOINT"
            ):
                net.validate_url(url)

    def test_fixed_provider_urls_are_allowed(self):
        for url in (
            "https://api.zotero.org/users/100/items?limit=1",
            "https://api.unpaywall.org/v2/10.1234/test?email=sample%40example.org",
            "https://api.opencitations.net/index/v2/citation-count/doi:10.1234/test",
            "https://api.openalex.org/works?search=sample",
            "https://api.crossref.org/works?query.bibliographic=sample",
            "https://api.semanticscholar.org/graph/v1/paper/search?query=sample",
        ):
            with self.subTest(url=url):
                net.validate_url(url)

    def test_redirect_handler_refuses_to_follow_location(self):
        handler = net.NoExternalRedirect()
        self.assertIsNone(handler.redirect_request(
            None, None, 302, "Found", {"Location": "https://evil.example"},
            "https://evil.example/exfiltrate"))

    def test_private_zotero_redirect_returns_redacted_error(self):
        fake_token = "TEST_PRIVATE_ZOTERO_SECRET_DO_NOT_LOG"
        class Redirected:
            def open(self, request, timeout=20):
                raise HTTPError(request.full_url, 302, "redirect to adversary",
                                {"Location": "https://evil.example/collect"}, None)
        seen = []
        def builder(handler):
            seen.append(handler)
            return Redirected()
        with patch.object(net, "build_opener", side_effect=builder):
            with self.assertRaises(bc.ProviderFailure) as caught:
                net.read_json("https://api.zotero.org/users/100/items",
                              {"Zotero-API-Key": fake_token}, max_bytes=1000)
        self.assertEqual(caught.exception.status, "REDIRECT_BLOCKED")
        self.assertNotIn(fake_token, str(caught.exception))
        self.assertEqual(len(seen), 1)
        self.assertIsInstance(seen[0], net.NoExternalRedirect)

    def test_doi_and_openalex_redirects_are_explicitly_blocked(self):
        for url, headers in (
            ("https://api.unpaywall.org/v2/10.1234/test",
             {"Accept": "application/json"}),
            ("https://api.openalex.org/works?search=test",
             {"Accept": "application/json", "x-api-key": "FAKE_KEY"}),
        ):
            class Redirected:
                def open(self, request, timeout=20):
                    raise HTTPError(request.full_url, 307, "synthetic redirect",
                                    {"Location": "https://evil.example"}, None)
            with self.subTest(url=url), patch.object(
                    net, "build_opener", return_value=Redirected()):
                with self.assertRaises(bc.ProviderFailure) as caught:
                    net.read_json(url, headers, max_bytes=100)
                self.assertEqual(caught.exception.status, "REDIRECT_BLOCKED")

    def test_bounded_response_is_rejected_without_full_json_read(self):
        class Response:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self, amount):
                self_amount = amount
                assert self_amount == 11
                return b"x" * 11
        class Opener:
            def open(self, request, timeout=20):
                return Response()
        with patch.object(net, "build_opener", return_value=Opener()):
            with self.assertRaisesRegex(bc.ProviderFailure, "RESPONSE_TOO_LARGE"):
                net.read_json("https://api.crossref.org/works?query=test",
                              {"Accept": "application/json"}, max_bytes=10)

    def test_bad_json_is_not_reported_as_zero_results(self):
        class Response:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self, amount):
                return b"not-json"
        class Opener:
            def open(self, request, timeout=20):
                return Response()
        with patch.object(net, "build_opener", return_value=Opener()):
            with self.assertRaisesRegex(bc.ProviderFailure, "INVALID_RESPONSE"):
                net.read_json("https://api.crossref.org/works?query=test",
                              {"Accept": "application/json"}, max_bytes=100)

    def test_provider_specific_http_404_semantics_remain_explicit(self):
        class Missing:
            def open(self, request, timeout=20):
                raise HTTPError(request.full_url, 404, "not found", {}, None)
        with patch.object(net, "build_opener", return_value=Missing()):
            with self.assertRaises(bc.ProviderFailure) as a:
                bc.default_fetch("https://api.crossref.org/works?query=x", {})
            with self.assertRaises(bc.ProviderFailure) as b:
                be._fetch("https://api.unpaywall.org/v2/10.1234/unknown", {})
        self.assertEqual(a.exception.status, "INVALID_REQUEST")
        self.assertEqual(b.exception.status, "NOT_FOUND")

    def test_mock_fetcher_does_not_bypass_fixed_origin_safety(self):
        called = []
        with self.assertRaisesRegex(bc.ProviderFailure, "UNSUPPORTED_ENDPOINT"):
            be._fetch("https://bad.example/private",
                      {"authorization": "FAKE_TOKEN"},
                      fetcher=lambda *_: called.append("unexpected"))
        self.assertEqual(called, [])


class ZoteroPrivateExportSecurityTests(unittest.TestCase):
    def setUp(self):
        t = TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        self.result = {
            "status": "COMPLETE",
            "records": [{"title": "=HYPERLINK('evil')",
                         "source_id": "SYNT-001",
                         "doi": "10.1234/synthetic",
                         "notes": "SECRET_IN_PRIVATE_NOTES",
                         "abstractNote": "SECRET_IN_PRIVATE_ABSTRACT",
                         "api_key": "SECRET_LOCAL_KEY"}],
        }

    def test_private_export_has_restricted_permissions_and_whitelisted_fields(self):
        dest = self.root / "private"
        summary = be.export_zotero_staging(dest, self.result)
        path = Path(summary["csv_path"])
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        payload = path.read_text(encoding="utf-8-sig")
        self.assertIn("'=HYPERLINK", payload)
        for secret in ("SECRET_IN_PRIVATE_NOTES", "SECRET_IN_PRIVATE_ABSTRACT",
                       "SECRET_LOCAL_KEY"):
            self.assertNotIn(secret, payload + json.dumps(summary))
        self.assertFalse(summary["drive_sync_verified"])
        self.assertFalse(summary["scientific_validated"])

    def test_repeated_export_cannot_overwrite_private_library(self):
        dest = self.root / "private"
        summary = be.export_zotero_staging(dest, self.result)
        path = Path(summary["csv_path"])
        saved = path.read_bytes()
        with self.assertRaisesRegex(ValueError, "PRIVATE_STAGING_ALREADY_EXISTS"):
            be.export_zotero_staging(dest, {
                "status": "COMPLETE", "records": [{"title": "Changed"}]})
        self.assertEqual(saved, path.read_bytes())
        self.assertFalse(list(dest.glob(".zotero-private-*")))

    def test_symlink_destination_is_rejected_without_mutating_external_file(self):
        out = self.root / "external"
        out.mkdir()
        target = out / "zotero_personal_metadata.csv"
        target.write_text("OLD_PRIVATE_DATA", encoding="utf-8")
        alias = self.root / "alias"
        alias.symlink_to(out, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "PRIVATE_STAGING_SYMLINK"):
            be.export_zotero_staging(alias, self.result)
        self.assertEqual(target.read_text(), "OLD_PRIVATE_DATA")

    def test_corrupt_private_items_do_not_disappear_silently(self):
        def fake(url, headers):
            return [
                {"key": "K1", "data": {"title": "First valid entry"}},
                {"key": "K2", "data": "corrupt private record"},
            ]
        r = be.list_own_zotero_metadata(
            user_id="100", api_key="DUMMY", execute=True, fetcher=fake)
        self.assertEqual(r["status"], "INVALID_RESPONSE")
        self.assertEqual(r["records"], [])
        self.assertEqual(r["returned"], 0)

    def test_credentials_with_crlf_are_rejected_prior_to_network_access(self):
        for key in ("secret\nX-Evil: 1", "secret\rX-Evil: 1"):
            called = []
            r = be.list_own_zotero_metadata(
                user_id="100", api_key=key, execute=True,
                fetcher=lambda *_: called.append("network") or [])
            self.assertEqual(r["status"], "NOT_CONFIGURED")
            self.assertEqual(called, [])
        self.assertEqual(
            be.list_own_zotero_metadata(user_id="١٠٠", api_key="DUMMY",
                                         execute=True)["status"], "NOT_CONFIGURED")

    def test_malformed_zotero_creator_list_fails_closed(self):
        r = be.list_own_zotero_metadata(
            user_id="100", api_key="DUMMY", execute=True,
            fetcher=lambda u, h: [{
                "key": "K", "data": {"title": "Synthetic", "creators": "not a list"}
            }])
        self.assertEqual(r["status"], "INVALID_RESPONSE")

    def test_failed_private_write_never_publishes_incomplete_csv(self):
        out = self.root / "private"
        with patch.object(be.csv, "DictWriter", side_effect=OSError("simulated drive failure")):
            with self.assertRaises(OSError):
                be.export_zotero_staging(out, self.result)
        self.assertFalse((out / "zotero_personal_metadata.csv").exists())
        self.assertFalse(list(out.glob(".zotero-private-*")))


if __name__ == "__main__":
    unittest.main()
