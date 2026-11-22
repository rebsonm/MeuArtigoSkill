#!/usr/bin/env python3
"""One-off rights reconnaissance against Crossref from public article titles.

This is metadata discovery, NOT a rights authorization, source read,
publisher PDF acquisition, or scientific validation. No private document
bytes, Drive IDs, tokens or source-archive file names leave this process.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import difflib
import json
from pathlib import Path
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "knowledge" / "methodology" / "intake"
PARTS = [BASE / f"rights-ledger-part-0{i}.json" for i in range(1, 6)]
MANIFEST = BASE / "rights-ledger-manifest.json"
URL = "https://api.crossref.org/works"
MAX_RESPONSE = 400_000
MAX_LOOKUPS = 420
CCBY4 = "https://creativecommons.org/licenses/by/4.0"


def simple(text: str) -> str:
    value = unicodedata.normalize("NFKD", text.casefold())
    value = "".join(c for c in value if not unicodedata.combining(c))
    return " ".join(re.findall(r"[a-z0-9]+", value))


def close_enough(a: str, b: str) -> bool:
    x, y = simple(a), simple(b)
    if not x or not y:
        return False
    if x == y:
        return True
    if len(x) < 20 or len(y) < 20:
        return False
    q1 = set(x.split())
    q2 = set(y.split())
    overlap = len(q1 & q2) / max(1, len(q1 | q2))
    return overlap >= .90 and difflib.SequenceMatcher(None, x, y).ratio() >= .94


def lookup(title: str) -> dict:
    query = urllib.parse.urlencode({
        "query.title": title,
        "rows": 3,
    })
    url = URL + "?" + query
    request = urllib.request.Request(url, headers={
        "User-Agent": "MeuArtigoSkill-Crossref-Metadata/1.0 (research method catalogue; https://github.com/rebsonm/MeuArtigoSkill)",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(request, timeout=20) as response:
        if urllib.parse.urlsplit(response.geturl()).hostname != "api.crossref.org":
            raise ValueError("UNREVIEWED_METADATA_HOST")
        blob = response.read(MAX_RESPONSE+1)
        if len(blob) > MAX_RESPONSE:
            raise ValueError("CROSSREF_RESPONSE_TOO_LARGE")
    result = json.loads(blob)
    items = result.get("message", {}).get("items", [])
    for item in items:
        titles = item.get("title") or []
        if not titles or not isinstance(titles[0],str) or not close_enough(title,titles[0]):
            continue
        doi = item.get("DOI")
        if not isinstance(doi, str) or not re.fullmatch(r"10\.[0-9]{4,9}/\S{3,180}", doi, flags=re.I):
            continue
        publisher = item.get("publisher")
        when = item.get("published",item.get("issued",{})).get("date-parts", [[]])
        year = when[0][0] if when and when[0] else None
        if not isinstance(year,int) or year < 1900 or year > 2027:
            year = None
        licenses = []
        for lic in item.get("license") or []:
            raw = lic.get("URL")
            if isinstance(raw,str) and raw.startswith(("https://", "http://")) and len(raw) <= 350:
                licenses.append({
                    "url": raw,
                    "content_version": lic.get("content-version", "NOT_REPORTED"),
                })
        license_candidate = any(
            x["url"].lower().replace("http://","https://").rstrip("/") == CCBY4
            and x["content_version"] in ("vor", "NOT_REPORTED")
            for x in licenses
        )
        return {
            "status": "MATCHED_PUBLISHER_METADATA_NOT_SOURCE_VERIFIED",
            "doi_candidate": doi.lower(),
            "official_title_candidate": titles[0],
            "publisher_candidate": publisher if isinstance(publisher,str) else None,
            "published_year_candidate": year,
            "publication_type_candidate": item.get("type"),
            "license_statements": licenses[:6],
            "cc_by_4_candidate": license_candidate,
            "crossref_record_url": f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}",
            "is_exact_source_file_identity_checked": False,
            "rights_to_copy_original_pdf_established": False,
        }
    return {"status": "NO_STRICT_TITLE_MATCH", "cc_by_4_candidate": False}


def guarded(title: str) -> dict:
    try:
        return lookup(title)
    except (ValueError, OSError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"status":"METADATA_LOOKUP_UNAVAILABLE",
                "error_kind":type(exc).__name__, "cc_by_4_candidate":False}


def main() -> int:
    batches = [json.loads(p.read_text(encoding="utf-8")) for p in PARTS]
    selected = []
    for i, batch in enumerate(batches):
        for j, row in enumerate(batch["records"]):
            title = row.get("bibliographic_title_original")
            if isinstance(title,str) and len(title) >= 12:
                selected.append((i,j,title))
    if len(selected) > MAX_LOOKUPS:
        raise ValueError("METADATA_LOOKUP_BUDGET_EXCEEDED")
    cache = {}
    unique = sorted({title for _,_,title in selected})
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(guarded,title):title for title in unique}
        for future in as_completed(futures):
            title = futures[future]
            try:
                cache[title] = future.result()
            except Exception:
                cache[title] = {"status":"UNAVAILABLE","cc_by_4_candidate":False}
    tally = {}
    for i,j,title in selected:
        row = batches[i]["records"][j]
        status = cache[title]
        # Metadata is only a candidate; do not change public rights decisions.
        row["crossref_metadata_screen"] = status
        row["rights_review"] = "NOT_CHECKED"
        row["publisher_license"] = "NOT_CHECKED"
        row["public_distribution"] = "NOT_AUTHORIZED_BY_THIS_LEDGER"
        name = status["status"]
        tally[name] = tally.get(name,0) + 1
    for p, batch in zip(PARTS,batches):
        p.write_text(json.dumps(batch,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["crossref_title_metadata_queries"] = len(unique)
    manifest["crossref_source_rows_screened"] = len(selected)
    manifest["crossref_results_by_status"] = tally
    manifest["crossref_ccby4_publisher_metadata_candidates"] = sum(
        1 for i,j,_ in selected
        if batches[i]["records"][j]["crossref_metadata_screen"].get("cc_by_4_candidate")
    )
    manifest["crossref_screened_licenses_are_publication_authorizations"] = False
    manifest["actual_individually_verified_rights_in_this_ledger"] = 0
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "selected_source_records":len(selected), "unique_titles":len(unique),
        "status_counts":tally,
        "ccby4_metadata_candidates":manifest["crossref_ccby4_publisher_metadata_candidates"],
        "publication_rights_approved":0,
    },indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
