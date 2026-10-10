#!/usr/bin/env python3
"""Optional DOI enrichment and private Zotero metadata: no credentials in chat.

Explicit calls only. No downloaded PDFs, article text mining or automatic
scientific evaluation. The adapter never exports Zotero notes, tags, abstracts,
attachments, user identity or access tokens. Use a locally authorized executor
that keeps provider credentials in protected environment variables.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from bibliographic_connectors import ProviderFailure, norm_doi, safe_metadata_text

UNPAYWALL = "https://api.unpaywall.org/v2/"
CITATIONS = "https://api.opencitations.net/index/v2/citation-count/doi:"
ZOTERO = "https://api.zotero.org/users/"
MAX_BYTES = 3_000_000


def _fetch(url: str, headers: dict[str, str], *, fetcher=None):
    if not url.startswith((UNPAYWALL, CITATIONS, ZOTERO)):
        raise ProviderFailure("UNSUPPORTED_ENDPOINT")
    if fetcher is not None:
        return fetcher(url, headers)
    try:
        with urlopen(Request(url, headers=headers, method="GET"), timeout=20) as response:
            body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ProviderFailure("RESPONSE_TOO_LARGE")
        return json.loads(body)
    except HTTPError as exc:
        if exc.code == 401:
            raise ProviderFailure("AUTH_FAILED") from None
        if exc.code == 403:
            raise ProviderFailure("LICENSE_BLOCKED") from None
        if exc.code == 429:
            raise ProviderFailure("RATE_LIMITED") from None
        if exc.code == 404:
            raise ProviderFailure("NOT_FOUND") from None
        raise ProviderFailure("PROVIDER_UNAVAILABLE" if exc.code >= 500 else "INVALID_REQUEST") from None
    except (URLError, TimeoutError):
        raise ProviderFailure("NETWORK_ERROR") from None
    except (ValueError, UnicodeError):
        raise ProviderFailure("INVALID_RESPONSE") from None


def lookup_doi(provider: str, doi: str, *, email: str = "",
               api_key: str = "", execute: bool = False, fetcher=None) -> dict:
    """Public metadata lookups; rights to AI-process PDFs are not inferred."""
    if provider not in ("unpaywall", "opencitations"):
        raise ValueError("Unknown DOI enrichment provider")
    normalized = norm_doi(doi)
    if not normalized:
        raise ValueError("Valid DOI required")
    result = {"provider": provider, "doi": normalized, "status": "NOT_EXECUTED",
              "fulltext_processed": False, "rights_confirmed": False,
              "scientific_validated": False}
    if not execute:
        return result
    if provider == "unpaywall":
        if not email or "@" not in email or len(email) > 254:
            result["status"] = "NOT_CONFIGURED"
            return result
        url = UNPAYWALL + quote(normalized, safe="/") + "?" + urlencode({"email": email})
        headers = {"Accept": "application/json", "User-Agent": "MeuArtigoSkill-metadata/0.9"}
    else:
        url = CITATIONS + quote(normalized, safe="/")
        headers = {"Accept": "application/json", "User-Agent": "MeuArtigoSkill-metadata/0.9"}
        if api_key:
            headers["authorization"] = api_key
    try:
        payload = _fetch(url, headers, fetcher=fetcher)
        if provider == "unpaywall":
            if not isinstance(payload, dict):
                raise ProviderFailure("INVALID_RESPONSE")
            location = payload.get("best_oa_location") or {}
            result.update({
                "status": "COMPLETE",
                "is_open_access_reported": payload.get("is_oa") if isinstance(payload.get("is_oa"), bool) else None,
                "oa_url_reported": safe_metadata_text(location.get("url_for_landing_page")
                    or location.get("url_for_pdf"), 450) if isinstance(location, dict) else "",
                "licence_reported": safe_metadata_text(location.get("license"), 100)
                    if isinstance(location, dict) else "",
            })
        else:
            if not isinstance(payload, list) or not payload or not isinstance(payload[0], dict):
                raise ProviderFailure("INVALID_RESPONSE")
            value = payload[0].get("count")
            if not str(value).isdigit():
                raise ProviderFailure("INVALID_RESPONSE")
            result.update({"status": "COMPLETE", "incoming_citation_count_reported": int(value)})
    except ProviderFailure as exc:
        result["status"] = exc.status
    return result


def list_own_zotero_metadata(*, user_id: str, api_key: str,
                             limit: int = 25, execute: bool = False,
                             fetcher=None) -> dict:
    """Retrieve user-scoped bibliography only, never attachments or private notes.

    The API key is sent in a request HEADER, and never persisted by this tool.
    """
    base = {"provider": "zotero", "status": "NOT_EXECUTED",
            "records": [], "returned": 0, "fulltext_processed": False,
            "scientific_validated": False}
    if not execute:
        return base
    if not (user_id and user_id.isdigit() and api_key):
        base["status"] = "NOT_CONFIGURED"
        return base
    if not 1 <= limit <= 100:
        raise ValueError("Zotero limit must be between 1 and 100")
    url = ZOTERO + quote(user_id, safe="") + "/items?" + urlencode({
        "limit": str(limit), "start": "0", "format": "json",
        "itemType": "journalArticle || book || conferencePaper"})
    headers = {"Zotero-API-Key": api_key, "Accept": "application/json",
               "User-Agent": "MeuArtigoSkill-metadata/0.9"}
    try:
        payload = _fetch(url, headers, fetcher=fetcher)
        if not isinstance(payload, list):
            raise ProviderFailure("INVALID_RESPONSE")
        records = []
        for item in payload[:limit]:
            data = item.get("data") if isinstance(item, dict) else None
            if not isinstance(data, dict):
                continue
            raw_creators = data.get("creators") or []
            authors = []
            for person in raw_creators[:40] if isinstance(raw_creators, list) else []:
                if not isinstance(person, dict):
                    continue
                author = safe_metadata_text(person.get("name")
                    or " ".join(str(person.get(p) or "") for p in ("firstName", "lastName")), 200)
                if author:
                    authors.append(author)
            year_string = safe_metadata_text(data.get("date"), 50)
            year_match = re.search(r"(?:19|20)\d{2}", year_string)
            records.append({
                "title": safe_metadata_text(data.get("title")),
                "doi": norm_doi(data.get("DOI") or ""),
                "authors": "; ".join(authors)[:1500],
                "year": year_match.group(0) if year_match else "",
                "source": "Zotero-user-library",
                "source_id": safe_metadata_text(item.get("key"), 100),
                "journal": safe_metadata_text(data.get("publicationTitle")),
                "document_type": safe_metadata_text(data.get("itemType"), 80),
                "language": safe_metadata_text(data.get("language"), 24),
                "landing_url": safe_metadata_text(data.get("url"), 350),
            })
        base.update({"status": "COMPLETE", "records": records, "returned": len(records)})
    except ProviderFailure as exc:
        base["status"] = exc.status
    return base


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    lookup = subs.add_parser("doi", help="Opt-in public DOI enrichment")
    lookup.add_argument("--provider", required=True, choices=["unpaywall", "opencitations"])
    lookup.add_argument("--doi", required=True)
    lookup.add_argument("--allow-network", action="store_true")
    zotero = subs.add_parser("zotero", help="Opt-in own Zotero private metadata")
    zotero.add_argument("--limit", type=int, default=25)
    zotero.add_argument("--allow-network", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "doi":
            result = lookup_doi(args.provider, args.doi,
                                email=os.environ.get("MEU_ARTIGO_CONTACT_EMAIL", ""),
                                api_key=os.environ.get("OPENCITATIONS_ACCESS_TOKEN", ""),
                                execute=args.allow_network)
        else:
            result = list_own_zotero_metadata(
                user_id=os.environ.get("ZOTERO_USER_ID", ""),
                api_key=os.environ.get("ZOTERO_API_KEY", ""),
                limit=args.limit, execute=args.allow_network)
        # DOI enrichment contains only source-reported OA/citation status.
        # Zotero personal metadata output needs local researcher-approved handling.
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result["status"] in {"COMPLETE", "NOT_EXECUTED"} else 2
    except ValueError:
        print("ERROR: INVALID_OPTIONAL_ENRICHMENT_REQUEST", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
