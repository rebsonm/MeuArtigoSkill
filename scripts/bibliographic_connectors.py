#!/usr/bin/env python3
"""Optional BYOC bibliographic metadata connectors.

No provider is contacted by importing this module. Only an explicit search
request can invoke HTTP. Licensed publishers are deliberately NOT implemented
as automatic fallbacks, and provider failures never block the manual workflow.

Production responses depend on vendor access, licences and quota. No full text
is fetched or submitted to an LLM by these adapters.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
import time
from typing import Callable
from urllib.parse import urlencode

from dedupe_records import norm_doi

OPEN_ALEX = "https://api.openalex.org/works"
CROSSREF = "https://api.crossref.org/works"
SEMANTIC_SCHOLAR = "https://api.semanticscholar.org/graph/v1/paper/search"
SUPPORTED = ("openalex", "crossref", "semantic_scholar")
LOCKED = ("scopus", "wos_starter", "wos_expanded")
RETRYABLE = {429, 500, 502, 503, 504}
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
FIELDS = ("title", "doi", "authors", "year", "source", "source_id",
          "journal", "document_type", "language", "landing_url")
DEFAULT_USER_AGENT = "MeuArtigoSkill/0.9 (bibliographic-metadata; user-managed)"


class ProviderFailure(Exception):
    def __init__(self, status: str):
        self.status = status
        super().__init__(status)  # Never retain URL or credential-bearing HTTP exception.


@dataclass
class SearchOutcome:
    provider: str
    query: str
    rows: list[dict[str, str]] = field(default_factory=list)
    status: str = "NOT_EXECUTED"
    reported_total: int | None = None
    pages_received: int = 0
    executed_at: str | None = None
    error_code: str | None = None
    export_sha256: str | None = None
    # No raw HTTP headers, tokens, URLs with credentials or abstracts.


def safe_metadata_text(value: object, limit: int = 1000) -> str:
    if not isinstance(value, str):
        return ""
    return value.replace("\x00", "").replace("\r", " ").replace("\n", " ").strip()[:limit]


def _authors_people(people: object, kind: str) -> str:
    if not isinstance(people, list):
        return ""
    names = []
    for person in people[:50]:
        if not isinstance(person, dict):
            continue
        if kind == "openalex":
            author = person.get("author") or {}
            raw = author.get("display_name") if isinstance(author, dict) else ""
        else:
            raw = " ".join(str(person.get(part) or "") for part in ("given", "family")).strip()
        name = safe_metadata_text(raw, 160)
        if name:
            names.append(name)
    return "; ".join(names)[:1500]


def normalize_openalex(item: dict) -> dict[str, str]:
    loc = item.get("primary_location") or {}
    src = loc.get("source") or {} if isinstance(loc, dict) else {}
    return {
        "title": safe_metadata_text(item.get("display_name") or item.get("title")),
        "doi": norm_doi(item.get("doi") or ""),
        "authors": _authors_people(item.get("authorships"), "openalex"),
        "year": str(item.get("publication_year") or ""),
        "source": "OpenAlex",
        "source_id": safe_metadata_text(item.get("id"), 180),
        "journal": safe_metadata_text(src.get("display_name")) if isinstance(src, dict) else "",
        "document_type": safe_metadata_text(item.get("type"), 80),
        "language": safe_metadata_text(item.get("language"), 24),
        "landing_url": safe_metadata_text(loc.get("landing_page_url"), 350)
        if isinstance(loc, dict) else "",
    }


def _first(values: object) -> str:
    return values[0] if isinstance(values, list) and values and isinstance(values[0], str) else ""


def normalize_crossref(item: dict) -> dict[str, str]:
    published = item.get("published") or item.get("issued") or {}
    parts = published.get("date-parts") or [] if isinstance(published, dict) else []
    first = parts[0] if isinstance(parts, list) and parts and isinstance(parts[0], list) else []
    return {
        "title": safe_metadata_text(_first(item.get("title")), 1000),
        "doi": norm_doi(item.get("DOI") or ""),
        "authors": _authors_people(item.get("author"), "crossref"),
        "year": str(first[0]) if first and isinstance(first[0], int) else "",
        "source": "Crossref",
        "source_id": safe_metadata_text(item.get("DOI"), 180),
        "journal": safe_metadata_text(_first(item.get("container-title"))),
        "document_type": safe_metadata_text(item.get("type"), 80),
        "language": safe_metadata_text(item.get("language"), 24),
        "landing_url": safe_metadata_text(item.get("URL"), 350),
    }


def normalize_semantic_scholar(item: dict) -> dict[str, str]:
    external = item.get("externalIds") or {}
    authors = item.get("authors") or []
    pub_types = item.get("publicationTypes") or []
    names = [safe_metadata_text(person.get("name"), 160)
             for person in authors[:50] if isinstance(person, dict)] if isinstance(authors, list) else []
    return {
        "title": safe_metadata_text(item.get("title")),
        "doi": norm_doi(external.get("DOI") or "") if isinstance(external, dict) else "",
        "authors": "; ".join(filter(None, names))[:1500],
        "year": str(item.get("year") or ""),
        "source": "Semantic Scholar",
        "source_id": safe_metadata_text(item.get("paperId"), 180),
        "journal": safe_metadata_text(item.get("venue")),
        "document_type": safe_metadata_text(
            pub_types[0] if isinstance(pub_types, list) and pub_types else "", 80),
        "language": "",
        "landing_url": safe_metadata_text(item.get("url"), 350),
    }


def default_fetch(url: str, headers: dict[str, str], timeout: int = 20) -> dict:
    # The shared transport checks exact HTTPS provider paths and refuses
    # HTTP redirects, including those that would forward API credentials.
    from provider_http_security import read_json
    data = read_json(url, headers, max_bytes=MAX_RESPONSE_BYTES,
                     timeout=timeout, missing_status="INVALID_REQUEST")
    if not isinstance(data, dict):
        raise ProviderFailure("INVALID_RESPONSE")
    return data


def _request(fetcher: Callable, url: str, headers: dict[str, str],
             retries: int = 2) -> dict:
    for attempt in range(retries + 1):
        try:
            return fetcher(url, headers)
        except ProviderFailure as exc:
            if exc.status not in {"RATE_LIMITED", "PROVIDER_UNAVAILABLE"} or attempt == retries:
                raise
            # Do not sleep in deterministic unit tests.
            if fetcher is default_fetch:
                time.sleep(min(2 ** attempt, 4))
    raise ProviderFailure("PROVIDER_UNAVAILABLE")


def _provider_item_valid(provider: str, item: dict) -> bool:
    """Reject structurally corrupt provider rows instead of silently dropping them.

    Missing optional bibliographic fields are permitted; a field that claims
    to contain a structured object but instead contains a list/string is not.
    """
    expected = {
        "openalex": {"primary_location": dict, "authorships": list},
        "crossref": {"title": list, "author": list, "published": dict, "issued": dict},
        "semantic_scholar": {"externalIds": dict, "authors": list, "publicationTypes": list},
    }
    return all(
        item.get(field) is None or isinstance(item[field], typ)
        for field, typ in expected[provider].items()
    )


def capabilities(provider: str) -> dict:
    if provider in SUPPORTED:
        return {
            "provider": provider, "metadata_search": True,
            "fulltext_retrieval": False, "requires_provider_key": False,
            "live_validated_in_current_session": False,
            "availability": "OPT_IN_ONLY",
        }
    if provider in LOCKED:
        return {
            "provider": provider, "metadata_search": False,
            "fulltext_retrieval": False, "requires_provider_key": True,
            "live_validated_in_current_session": False,
            "availability": "LICENCE_AND_EXECUTOR_REVIEW_REQUIRED",
        }
    raise ValueError("Unsupported bibliographic provider")


def search(provider: str, query: str, *, limit: int = 50,
           fetcher: Callable | None = None, email: str = "",
           api_key: str = "", execute: bool = False) -> SearchOutcome:
    """Execute bounded, opted-in metadata-only search; never a complete review.

    A custom fetcher is for deterministic tests, not remote permission bypass.
    The api_key argument MUST come from a secure runtime, never from CLI/chat.
    """
    if provider not in SUPPORTED:
        if provider in LOCKED:
            return SearchOutcome(provider=provider, query=query,
                                 status="LICENSE_BLOCKED", error_code="NOT_IMPLEMENTED")
        raise ValueError("Unsupported bibliographic provider")
    if not isinstance(query, str) or not query.strip() or len(query) > 600:
        raise ValueError("A nonempty bounded query is required")
    if not isinstance(limit, int) or not 1 <= limit <= 1000:
        raise ValueError("limit must be between 1 and 1000")
    outcome = SearchOutcome(provider=provider, query=query)
    if not execute:
        return outcome
    fetcher = fetcher or default_fetch
    outcome.executed_at = datetime.now(timezone.utc).isoformat()
    remaining = limit
    page = 1
    cursor = "*"
    seen_cursors: set[str] = set()
    pagination_incomplete = False
    try:
        while remaining:
            page_size = min(remaining, 100)
            if provider == "openalex":
                params = {"search": query, "per_page": str(page_size), "page": str(page)}
                if api_key:
                    params["api_key"] = api_key
                url = OPEN_ALEX + "?" + urlencode(params)
            elif provider == "crossref":
                params = {"query.bibliographic": query, "rows": str(page_size),
                          "cursor": cursor}
                if email:
                    params["mailto"] = email
                url = CROSSREF + "?" + urlencode(params)
            else:
                params = {"query": query, "offset": str((page - 1) * 100),
                          "limit": str(page_size),
                          "fields": "title,year,authors,externalIds,venue,url,publicationTypes"}
                url = SEMANTIC_SCHOLAR + "?" + urlencode(params)
            headers = {"User-Agent": DEFAULT_USER_AGENT, "Accept": "application/json"}
            if provider == "semantic_scholar" and api_key:
                headers["x-api-key"] = api_key
            data = _request(fetcher, url, headers)
            if not isinstance(data, dict):
                raise ProviderFailure("INVALID_RESPONSE")
            if provider == "openalex":
                raw_items = data.get("results")
                meta = data.get("meta") or {}
                n = meta.get("count") if isinstance(meta, dict) else None
                normalizer = normalize_openalex
            elif provider == "crossref":
                message = data.get("message") or {}
                raw_items = message.get("items") if isinstance(message, dict) else None
                n = message.get("total-results") if isinstance(message, dict) else None
                normalizer = normalize_crossref
            else:
                raw_items = data.get("data")
                n = data.get("total")
                normalizer = normalize_semantic_scholar
            if not isinstance(raw_items, list):
                raise ProviderFailure("INVALID_RESPONSE")
            if n is not None and (type(n) is not int or n < 0):
                raise ProviderFailure("INVALID_RESPONSE")
            if n is not None:
                outcome.reported_total = n
            # Validate the entire page before adding ANY of its rows. A
            # corrupt provider payload cannot quietly drop individual works
            # and convert an incomplete response into COMPLETE.
            if any(not isinstance(item, dict) or not _provider_item_valid(provider, item)
                   for item in raw_items):
                raise ProviderFailure("INVALID_RESPONSE")
            try:
                normalized = [normalizer(item) for item in raw_items[:remaining]]
            except (AttributeError, TypeError, ValueError, KeyError):
                raise ProviderFailure("INVALID_RESPONSE") from None
            outcome.rows.extend(normalized)
            remaining = limit - len(outcome.rows)
            outcome.pages_received += 1
            if len(raw_items) < page_size or not raw_items:
                break
            if provider in {"openalex", "semantic_scholar"}:
                page += 1
            else:
                next_cursor = message.get("next-cursor") if isinstance(message, dict) else None
                if not isinstance(next_cursor, str) or not next_cursor or next_cursor in seen_cursors:
                    # A full page with an unverified continuation must never
                    # silently certify complete pagination.
                    if outcome.reported_total is None or outcome.reported_total > len(outcome.rows):
                        pagination_incomplete = True
                    break
                seen_cursors.add(next_cursor)
                cursor = next_cursor
        # A bounded query is not evidence of complete database coverage.
        more = (outcome.reported_total is not None
                and outcome.reported_total > len(outcome.rows))
        unknown_full_page = (
            outcome.reported_total is None and outcome.pages_received > 0
            and remaining == 0
        )
        if pagination_incomplete:
            outcome.error_code = "PAGINATION_INCOMPLETE"
        elif unknown_full_page:
            outcome.error_code = "UNKNOWN_PROVIDER_TOTAL"
        outcome.status = "PARTIAL" if more or pagination_incomplete or unknown_full_page else "COMPLETE"
    except ProviderFailure as exc:
        outcome.error_code = exc.status
        outcome.status = "PARTIAL" if outcome.rows else exc.status
    # No successful status for zero results after a transport failure.
    return outcome
