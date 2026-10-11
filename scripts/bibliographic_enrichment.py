#!/usr/bin/env python3
"""Optional DOI enrichment and private Zotero metadata: no credentials in chat.

Explicit calls only. No downloaded PDFs, article text mining or automatic
scientific evaluation. The adapter never exports Zotero notes, tags, abstracts,
attachments, user identity or access tokens. Use a locally authorized executor
that keeps provider credentials in protected environment variables.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote, urlencode

from bibliographic_connectors import FIELDS, ProviderFailure, norm_doi, safe_metadata_text

UNPAYWALL = "https://api.unpaywall.org/v2/"
CITATIONS = "https://api.opencitations.net/index/v2/citation-count/doi:"
ZOTERO = "https://api.zotero.org/users/"
MAX_BYTES = 3_000_000


def _fetch(url: str, headers: dict[str, str], *, fetcher=None):
    from provider_http_security import read_json, validate_url
    # Also verify mock-target URLs, without granting an alternate endpoint.
    validate_url(url)
    if fetcher is not None:
        return fetcher(url, headers)
    return read_json(url, headers, max_bytes=MAX_BYTES,
                     missing_status="NOT_FOUND")


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
    if (not isinstance(user_id, str)
            or not re.fullmatch(r"[0-9]{1,30}", user_id)
            or not isinstance(api_key, str) or not api_key.strip()
            or "\\r" in api_key or "\\n" in api_key):
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
        if not isinstance(payload, list) or len(payload) > limit:
            raise ProviderFailure("INVALID_RESPONSE")
        records = []
        for item in payload:
            data = item.get("data") if isinstance(item, dict) else None
            if not isinstance(data, dict):
                raise ProviderFailure("INVALID_RESPONSE")
            raw_creators = data.get("creators") or []
            if not isinstance(raw_creators, list):
                raise ProviderFailure("INVALID_RESPONSE")
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


def export_zotero_staging(out_dir: Path, result: dict) -> dict:
    """Save only whitelisted metadata, never notes, tokens or personal auth."""
    if result.get("status") != "COMPLETE":
        raise ValueError("Zotero has not been retrieved")
    target = Path(out_dir)
    if target.is_symlink():
        raise ValueError("PRIVATE_STAGING_SYMLINK_NOT_ALLOWED")
    path = target.resolve()
    path.mkdir(parents=True, exist_ok=True)
    filename = path / "zotero_personal_metadata.csv"
    if filename.exists() or filename.is_symlink():
        raise ValueError("PRIVATE_STAGING_ALREADY_EXISTS")
    if not isinstance(result.get("records"), list) or any(
            not isinstance(item, dict) for item in result["records"]):
        raise ValueError("INVALID_PRIVATE_METADATA_RECORDS")
    # Create the complete private CSV in a same-directory temporary file.
    # Hard-linking then publishing guarantees create-only semantics (even if
    # another export races) rather than overwriting a researcher's library.
    from uuid import uuid4
    temp = path / (".zotero-private-" + uuid4().hex + ".tmp")
    try:
        with temp.open("x", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            for item in result["records"]:
                # Whitelist bibliographic metadata: never notes/tags/attachments.
                writer.writerow({field: (
                    "'" + str(item.get(field, "")) if str(item.get(field, "")).lstrip()[:1]
                    in ("=", "+", "-", "@") else str(item.get(field, ""))
                ) for field in FIELDS})
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temp, filename)
    finally:
        temp.unlink(missing_ok=True)
    return {
        "provider": "zotero", "status": "COMPLETE",
        "records_exported": len(result["records"]),
        "csv_path": str(filename), "sha256": hashlib.sha256(filename.read_bytes()).hexdigest(),
        "drive_sync_verified": False, "scientific_validated": False,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    lookup = subs.add_parser("doi", help="Opt-in public DOI enrichment")
    lookup.add_argument("--provider", required=True, choices=["unpaywall", "opencitations"])
    lookup.add_argument("--doi", required=True)
    lookup.add_argument("--allow-network", action="store_true")
    zotero = subs.add_parser("zotero", help="Opt-in own Zotero private metadata")
    zotero.add_argument("--limit", type=int, default=25)
    zotero.add_argument("--out-dir", help="User-approved private export location")
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
        if args.command == "zotero":
            if result["status"] == "COMPLETE" and args.out_dir:
                result = export_zotero_staging(Path(args.out_dir), result)
            else:
                # Do not stream a private user's complete bibliography into
                # console logs or model context without an explicit export.
                result = {"provider": "zotero", "status": result["status"],
                          "records_exported": 0,
                          "export_requires_out_dir": result["status"] == "COMPLETE"}
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result["status"] in {"COMPLETE", "NOT_EXECUTED"} else 2
    except ValueError:
        print("ERROR: INVALID_OPTIONAL_ENRICHMENT_REQUEST", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
