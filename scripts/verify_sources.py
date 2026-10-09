#!/usr/bin/env python3
"""Independent bibliographic and local locator checks for canonical evidence.

Uses Python's standard library for network/metadata checks. PDF text extraction
is local and optional (pypdf or pdftotext). Never uploads source documents.
Metadata verification is NOT a semantic assessment of a scientific claim.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

MGMT = "00_Gestao_e_Continuidade"
DOI_RX = re.compile(r"^10\.\d{4,9}/\S+$", re.I)
PAGE_RX = re.compile(r"\b(?:p(?:age|ágina|ág)?\.?|pp\.)\s*(\d{1,5})\b", re.I)
MAX_SOURCE_BYTES = 30 * 1024 * 1024


def cell(row, *names):
    for name in names:
        value = (row.get(name) or "").strip()
        if value:
            return value
    return ""


def rows(path):
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(x for x in value if not unicodedata.combining(x))
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def doi_of(value):
    value = str(value or "").strip()
    value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value, flags=re.I)
    value = urllib.parse.unquote(value).strip().rstrip(".,;)")
    return value.lower() if DOI_RX.fullmatch(value) else ""


def provider_query(provider, doi, mailto="", timeout=8):
    """Fetch JSON from fixed academic hosts; no arbitrary user-supplied URLs."""
    if provider == "crossref":
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/")
        if mailto:
            url += "?mailto=" + urllib.parse.quote(mailto, safe="@")
    elif provider == "openalex":
        url = "https://api.openalex.org/works/" + urllib.parse.quote("https://doi.org/" + doi, safe=":/")
        key = os.environ.get("OPENALEX_API_KEY", "").strip()
        if key:
            url += "?api_key=" + urllib.parse.quote(key, safe="")
    else:
        raise ValueError("Unsupported provider")
    if provider == "crossref":
        time.sleep(0.22)  # stay below the anonymous single-record request limit
    req = urllib.request.Request(url, headers={"User-Agent": "MeuArtigoSourceCheck/1.0 (academic source verification)", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status != 200:
                return {"status": "ERROR", "http_status": response.status}
            data = json.load(response)
        if provider == "crossref":
            data = data.get("message") or {}
        return {"status": "FOUND", "data": data}
    except urllib.error.HTTPError as exc:
        return {"status": "NOT_FOUND" if exc.code == 404 else "ERROR", "http_status": exc.code}
    except (urllib.error.URLError, TimeoutError, ValueError, OSError, json.JSONDecodeError) as exc:
        return {"status": "ERROR", "reason": type(exc).__name__}


def metadata_fields(provider, data):
    if provider == "crossref":
        titles = data.get("title") or []
        title = titles[0] if isinstance(titles, list) and titles else ""
        years = (data.get("published") or {}).get("date-parts") or (data.get("issued") or {}).get("date-parts") or []
        year = str(years[0][0]) if years and years[0] else ""
        authors = [a.get("family") or "" for a in (data.get("author") or [])]
        update = data.get("update-to") or []
        relation = data.get("relation") or {}
        retracted = any("retract" in str(v).lower() for v in update)
        retracted = retracted or any("retract" in str(k).lower() for k in relation)
        updates = bool(update or relation.get("is-corrected-by"))
        return {"doi": str(data.get("DOI") or ""), "title": title, "year": year, "authors": authors,
                "retracted": bool(retracted), "updated": updates}
    primary = (data.get("authorships") or [])
    authors = [((a.get("author") or {}).get("display_name") or "") for a in primary]
    return {"doi": str(data.get("doi") or ""), "title": data.get("display_name") or data.get("title") or "",
            "year": str(data.get("publication_year") or ""), "authors": authors,
            "retracted": data.get("is_retracted") is True, "updated": False}


def match_metadata(doi, title, year, authors, responses):
    checks = []
    retract = False
    updated = False
    for provider in ("crossref", "openalex"):
        response = responses.get(provider) or {"status": "UNAVAILABLE"}
        status = response.get("status") or "ERROR"
        item = {"provider": provider, "status": status, "http_status": response.get("http_status")}
        if status == "FOUND":
            info = metadata_fields(provider, response.get("data") or {})
            if doi_of(info["doi"]) != doi:
                item["status"] = "DOI_MISMATCH"
            else:
                score = SequenceMatcher(None, norm(title), norm(info["title"])).ratio() if title else None
                item["title_similarity"] = round(score, 3) if score is not None else None
                # Minor online/print year differences are flagged for review.
                year_ok = not year or not info["year"] or (
                    year.isdigit() and info["year"].isdigit() and abs(int(year) - int(info["year"])) <= 1)
                item["year_compatible"] = year_ok
                item["status"] = "VERIFIED" if score is not None and score >= 0.86 and year_ok else (
                    "TITLE_MISMATCH" if score is not None and score < 0.86 else "YEAR_MISMATCH" if not year_ok else "INSUFFICIENT")
                if authors and info["authors"]:
                    family = norm(re.split(r"[,;]|\band\b", authors)[0]).split(" ")[-1]
                    normalized = [norm(x).split(" ")[-1] for x in info["authors"] if norm(x)]
                    item["author_corresponds"] = family in normalized if family else None
                    if item["author_corresponds"] is False:
                        item["status"] = "AUTHOR_MISMATCH"
                retract = retract or info["retracted"]
                updated = updated or info["updated"]
        checks.append(item)
    states = [x["status"] for x in checks]
    if any(s in {"DOI_MISMATCH", "TITLE_MISMATCH", "AUTHOR_MISMATCH", "YEAR_MISMATCH"} for s in states):
        result = "MISMATCH"
    elif "VERIFIED" in states:
        result = "VERIFIED"
    elif all(s == "NOT_FOUND" for s in states):
        result = "NOT_FOUND"
    else:
        result = "UNVERIFIED"
    return result, checks, retract, updated


def safe_local_path(root, raw):
    if not raw:
        return None, "NOT_PROVIDED"
    if raw.startswith(("http://", "https://", "drive:", "s3:")):
        return None, "REMOTE_NOT_DOWNLOADED"
    path = (root / raw).resolve()
    if not path.is_relative_to(root.resolve()):
        return None, "OUTSIDE_WORKSPACE"
    if not path.is_file():
        return None, "FILE_NOT_FOUND"
    if path.stat().st_size > MAX_SOURCE_BYTES:
        return None, "FILE_TOO_LARGE"
    if path.suffix.lower() not in {".pdf", ".txt", ".md"}:
        return None, "UNSUPPORTED_FORMAT"
    return path, "LOCAL_FILE"


def source_pages(path):
    if path.suffix.lower() in {".txt", ".md"}:
        return [path.read_text(encoding="utf-8-sig", errors="replace")]
    try:
        from pypdf import PdfReader
        return [(p.extract_text() or "") for p in PdfReader(str(path)).pages]
    except Exception:
        if shutil.which("pdftotext"):
            try:
                result = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True,
                                        timeout=20, check=True)
                return result.stdout.decode("utf-8", errors="replace").split("\f")
            except (OSError, subprocess.SubprocessError):
                pass
    return None


def check_locator(root, filepath, locator):
    path, source_status = safe_local_path(root, filepath)
    out = {"status": source_status, "source_sha256": digest(path) if path else None, "matched_page": None}
    if path is None:
        return out
    if not locator:
        out["status"] = "LOCATOR_NOT_PROVIDED"
        return out
    # Page numbers alone or semantic summaries cannot be verified as quotations.
    quoted = re.search(r'[“"]([^”"]{20,})[”"]', locator)
    phrase = quoted.group(1) if quoted else re.sub(
        r"^(?:p(?:age|ágina|ág)?\.?|pp\.)\s*\d+(?:\s*[-–]\s*\d+)?\s*[:;,–-]?\s*", "", locator, flags=re.I).strip()
    if len(norm(phrase)) < 25 or len(norm(phrase).split()) < 5:
        out["status"] = "LOCATOR_NOT_CHECKABLE"
        return out
    pages = source_pages(path)
    if not pages or not any(norm(x) for x in pages):
        out["status"] = "TEXT_UNAVAILABLE"
        return out
    # Use normalized exact textual anchors: fuzzy similarity cannot prove existence.
    needle = norm(phrase)
    found = [i + 1 for i, page in enumerate(pages) if needle in norm(page)]
    if not found:
        out["status"] = "PASSAGE_NOT_FOUND"
        return out
    page = PAGE_RX.search(locator)
    if page and path.suffix.lower() == ".pdf" and int(page.group(1)) not in found:
        out["status"] = "PAGE_MISMATCH"
        out["matched_page"] = found[0]
        return out
    out["status"] = "MATCHED"
    out["matched_page"] = found[0] if path.suffix.lower() == ".pdf" else None
    return out


def verify_row(row, root, lookup, fetcher=provider_query, offline=False, mailto=""):
    evidence_id = cell(row, "Evidence_ID")
    record_id = cell(row, "Record_ID")
    info = lookup.get(record_id) or {}
    token = cell(row, "DOI_or_persistent_ID", "DOI") or info.get("DOI", "")
    doi = doi_of(token)
    title = cell(row, "Title", "Article_title", "Source_title") or info.get("Title", "")
    year = cell(row, "Year") or info.get("Year", "")
    authors = cell(row, "Authors") or info.get("Authors", "")
    locator = cell(row, "Supporting_locator", "Locator")
    filepath = cell(row, "FullText_path", "Full_text_path", "PDF_path", "Source_path", "File_path") or info.get("File_or_URL", "")
    if not doi:
        metadata_status = "INVALID_DOI" if str(token).lower().startswith(("10.", "doi:", "https://doi.org")) else "NO_DOI"
        checks = []
        retracted, updated = False, False
    elif offline:
        metadata_status, checks, retracted, updated = "UNVERIFIED", [], False, False
    else:
        replies = {provider: fetcher(provider, doi, mailto) for provider in ("crossref", "openalex")}
        metadata_status, checks, retracted, updated = match_metadata(doi, title, year, authors, replies)
    locator_check = check_locator(root, filepath, locator)
    local_source, _ = safe_local_path(root, filepath)
    blockers = (metadata_status in {"INVALID_DOI", "MISMATCH", "NOT_FOUND"} or
                locator_check["status"] in {"PASSAGE_NOT_FOUND", "OUTSIDE_WORKSPACE"})
    review = (metadata_status != "VERIFIED" or locator_check["status"] != "MATCHED" or
              retracted or updated)
    outcome = "FAIL" if blockers else "REVIEW_REQUIRED" if review else "METADATA_AND_LOCATOR_CHECKED"
    return {"Evidence_ID": evidence_id, "Record_ID": record_id, "doi": doi or None,
            "metadata_status": metadata_status, "metadata_checks": checks,
            "retraction_alert": retracted, "update_alert": updated,
            "locator_status": locator_check["status"], "source_sha256": locator_check["source_sha256"],
            "source_path": local_source.relative_to(root).as_posix() if local_source else None,
            "matched_page": locator_check["matched_page"],
            "claim_support_status": "NOT_SEMANTICALLY_VERIFIED", "result": outcome}


def index_project(root):
    screening = {r.get("Record_ID"): r for r in rows(root / MGMT / "03_Screening.csv") if r.get("Record_ID")}
    trackers = rows(root / MGMT / "04_FullText_Tracker.csv")
    evidence_to_record = {}
    for item in trackers:
        record = (item.get("Record_ID") or "").strip()
        for eid in re.split(r"[,;\s]+", item.get("Evidence_matrix_id") or ""):
            if eid:
                evidence_to_record[eid] = record
        if record:
            screening.setdefault(record, {}).update({
                "File_or_URL": item.get("File_or_URL") or "",
            })
    return screening, evidence_to_record


def verify_project(root, offline=False, mailto="", fetcher=provider_query):
    root = root.resolve()
    path = root / MGMT / "05_Evidence_Matrix.csv"
    if not path.is_file():
        raise FileNotFoundError(f"Evidence matrix not found: {path}")
    screening, links = index_project(root)
    verified = []
    cache = {}
    def cached_fetch(provider, doi, contact=""):
        key = (provider, doi)
        if key not in cache:
            cache[key] = fetcher(provider, doi, contact)
        return cache[key]
    for original in rows(path):
        record = links.get(original.get("Evidence_ID") or "") or original.get("Record_ID") or ""
        item = dict(original)
        item["Record_ID"] = record
        verified.append(verify_row(item, root, screening, cached_fetch, offline, mailto))
    return {"schema_version": 1, "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "input_file": f"{MGMT}/05_Evidence_Matrix.csv",
            "input_sha256": digest(path), "offline": bool(offline),
            "checks": verified,
            "summary": {"records": len(verified), "checked": sum(x["result"] == "METADATA_AND_LOCATOR_CHECKED" for x in verified),
                        "review_required": sum(x["result"] == "REVIEW_REQUIRED" for x in verified),
                        "failed": sum(x["result"] == "FAIL" for x in verified)},
            "disclaimer": "Metadata and textual locator checks do not establish semantic claim support."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_path", help="Existing initialized project workspace")
    parser.add_argument("--offline", action="store_true", help="Skip network metadata queries; unverifiable is never success")
    parser.add_argument("--mailto", default="", help="Optional contact for Crossref polite access")
    parser.add_argument("--output", help="Custom report path within the project workspace")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero when any evidence needs review or fails")
    args = parser.parse_args(argv)
    root = Path(args.project_path).resolve()
    out = (Path(args.output).resolve() if args.output else root / MGMT / "SOURCE_VERIFICATION.json")
    if not out.is_relative_to(root):
        parser.error("Report must be saved inside the project workspace")
    try:
        report = verify_project(root, offline=args.offline, mailto=args.mailto)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"report": str(out), **report["summary"]}, ensure_ascii=False))
    return 2 if args.strict and (report["summary"]["failed"] or report["summary"]["review_required"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
