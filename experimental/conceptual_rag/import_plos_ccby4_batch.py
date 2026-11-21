#!/usr/bin/env python3
"""One-time version-of-record PLOS CC BY 4.0 methodology intake.

Exact DOI allowlist only. Verify Crossref publisher, article DOI and
version-of-record CC BY 4.0 license before contacting PLOS for the original
PDF. Never touch private libraries, credentials or unpublished PDFs.
Failure to verify -> no upload. This is a draft-only test intake.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "knowledge" / "methodology"
PDF_DIR = BASE / "pdfs"
CATALOG = BASE / "pdf_catalog.json"
MAX_CATALOG = 40_000
MAX_SINGLE = 12_000_000
MAX_TOTAL = 85_000_000
LICENSE = "https://creativecommons.org/licenses/by/4.0/"

# DOI is an immutable published identifier, not a search term or an archive ID.
DOIS = [
    "10.1371/journal.pone.0181689",
    "10.1371/journal.pmed.1001069",
    "10.1371/journal.pone.0210776",
    "10.1371/journal.pone.0270673",
    "10.1371/journal.pone.0331666",
    "10.1371/journal.pone.0289695",
    "10.1371/journal.pone.0283092",
    "10.1371/journal.pcbi.1004961",
    "10.1371/journal.pcbi.1012179",
    "10.1371/journal.pcbi.1003453",
    "10.1371/journal.pcbi.1014882",
    "10.1371/journal.pcbi.1008938",
    "10.1371/journal.pcbi.1006508",
    "10.1371/journal.pcbi.1004385",
    "10.1371/journal.pcbi.1006379",
    "10.1371/journal.pcbi.1010139",
    "10.1371/journal.pcbi.1005412",
    "10.1371/journal.pcbi.1007846",
    "10.1371/journal.pcbi.1006036",
    "10.1371/journal.pcbi.1010749",
    "10.1371/journal.pcbi.1014419",
]

JOURNALS = {"pone": "plosone", "pmed": "plosmedicine", "pcbi": "ploscompbiol"}


class SafeRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlsplit(newurl)
        if parsed.scheme != "https" or parsed.hostname not in (
            "api.crossref.org", "journals.plos.org", "plos.org"
        ):
            raise ValueError("REDIRECT_HOST_NOT_ON_VERIFIED_ALLOWLIST")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = urllib.request.build_opener(SafeRedirects)


def download(url: str, limit: int, accept: str) -> bytes:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname not in (
        "api.crossref.org", "journals.plos.org"
    ):
        raise ValueError("SOURCE_HOST_NOT_ALLOWED")
    request = urllib.request.Request(url, headers={
        "User-Agent": "MeuArtigoSkill-DOI-CCBY-Intake/1.0 (+https://github.com/rebsonm/MeuArtigoSkill)",
        "Accept": accept,
    })
    with OPENER.open(request, timeout=26) as response:
        length = response.headers.get("Content-Length")
        if length is not None and int(length) > limit:
            raise ValueError("SOURCE_TOO_LARGE")
        return response.read(limit + 1)


def crossref(doi: str) -> dict:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    data = json.loads(download(url, 350_000, "application/json").decode("utf-8"))
    entry = data.get("message", {})
    if entry.get("DOI", "").lower() != doi or "Public Library of Science" not in entry.get("publisher", ""):
        raise ValueError("PUBLISHER_DOI_MISMATCH")
    rights = entry.get("license", [])
    def accepted(right):
        link = right.get("URL", "").lower().replace("http://", "https://")
        return (link.rstrip("/") == LICENSE.rstrip("/") and
                right.get("content-version") in ("vor", None))
    if not any(accepted(r) for r in rights):
        raise ValueError("VERSION_OF_RECORD_CCBY4_NOT_ATTESTED")
    title = (entry.get("title") or [""])[0]
    if not isinstance(title, str) or len(title) > 180 or len(title) < 10:
        raise ValueError("TITLE_MISSING_OR_OVERSIZED")
    names = []
    for a in entry.get("author", []):
        value = " ".join(s for s in (a.get("given", ""), a.get("family", "")) if s)
        if value:
            names.append(value)
    if not names:
        raise ValueError("AUTHORS_MISSING")
    when = entry.get("published", entry.get("issued", {})).get("date-parts", [[]])
    year = when[0][0] if when and when[0] else None
    if not isinstance(year, int) or not 1900 <= year <= 2026:
        raise ValueError("YEAR_INVALID")
    return {"title": title, "authors": "; ".join(names), "year": year}


def source_for(doi: str) -> tuple[str, str, str]:
    match = re.fullmatch(r"10\.1371/journal\.(pone|pmed|pcbi)\.(\d{7})", doi)
    if not match:
        raise ValueError("DOI_OUTSIDE_FIXED_PLOS_SCOPE")
    journal = JOURNALS[match.group(1)]
    source = f"https://journals.plos.org/{journal}/article?id={doi}"
    pdf = f"https://journals.plos.org/{journal}/article/file?id={doi}&type=printable"
    name = f"plos-{match.group(1)}-{match.group(2)}.pdf"
    return source, pdf, name


def keywords(title: str) -> list[str]:
    norm = re.findall(r"[A-Za-z]{4,}", title.lower())
    aliases = []
    for en, pt in (
        ("review", "revisao"), ("survey", "questionario"),
        ("research", "pesquisa"), ("sampling", "amostragem"),
        ("analysis", "analise"), ("statistical", "estatistica"),
        ("writing", "escrita"), ("data", "dados"), ("software", "reprodutibilidade"),
        ("publication", "publicacao"), ("knowledge", "conhecimento"),
        ("responsible", "responsabilidade"), ("reference", "citacao"),
    ):
        if en in norm or any(w.startswith(en) for w in norm):
            aliases.append(pt)
    return sorted(set(norm[:15] + aliases))[:27]


def main() -> int:
    original = CATALOG.read_bytes()
    if len(original) > MAX_CATALOG:
        raise ValueError("EXISTING_CATALOG_TOO_LARGE")
    catalog = json.loads(original)
    if catalog.get("schema") != "MEU_ARTIGO_PUBLIC_PDF_CATALOG_V1":
        raise ValueError("CATALOG_SCHEMA_INVALID")
    seen_doi = {d["doi"].lower() for d in catalog.get("documents", [])}
    newly_staged = []
    failures = []
    total_bytes = 0
    for doi in DOIS:
        if doi in seen_doi:
            continue
        try:
            source_url, pdf_url, filename = source_for(doi)
            official = crossref(doi)
            pdf = download(pdf_url, MAX_SINGLE, "application/pdf")
            if not (8_000 <= len(pdf) <= MAX_SINGLE and pdf.startswith(b"%PDF-")
                    and b"%%EOF" in pdf[-4096:]):
                raise ValueError("NOT_FULL_ORIGINAL_PDF")
            total_bytes += len(pdf)
            if total_bytes > MAX_TOTAL:
                raise ValueError("TOTAL_CORPUS_BATCH_TOO_LARGE")
            path = "knowledge/methodology/pdfs/" + filename
            if (ROOT / path).exists():
                raise ValueError("REFUSE_FILE_OVERWRITE")
            sha = hashlib.sha256(pdf).hexdigest()
            item = {
                "path": path, "title": official["title"],
                "authors": official["authors"], "year": official["year"],
                "doi": doi, "size": len(pdf), "sha256": sha,
                "rights": "PUBLIC_REDISTRIBUTION_REVIEWED", "license": "CC BY 4.0",
                "license_url": LICENSE, "rights_evidence": source_url,
                "source_url": source_url, "source_pdf_url": pdf_url,
                "rights_evidence_type": "PLOS_PUBLISHER_AND_CROSSREF_VOR_CC_BY_4",
                "keywords": keywords(official["title"]),
                "original_file_unchanged": True,
            }
            newly_staged.append((item, pdf))
            print("SOURCE_CHECKED_CCBY4:",doi,"bytes",len(pdf))
        except (ValueError, OSError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            failures.append({"doi": doi, "error_kind": type(exc).__name__,
                             "reason": str(exc)[:100]})
            print("SOURCE_SKIPPED:", doi, type(exc).__name__, str(exc)[:100])
    for item, pdf in newly_staged:
        (ROOT / item["path"]).write_bytes(pdf)
        catalog["documents"].append(item)
    catalog["version"] = "plos-cc-by4-import-2026-11-21"
    catalog["catalog_status"] = f"{len(catalog['documents'])}_PUBLIC_LICENSE_REVIEWED_ARTICLES"
    CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    readme = PDF_DIR / "README.md"
    if newly_staged:
        old = readme.read_text(encoding="utf-8")
        old = re.sub(r"\b14 source PDFs\b", f"{len(catalog['documents'])} source PDFs", old)
        additions = ["", "## Further PLOS original PDFs — crossref license checked", "",
                     "These originals remain outside the installer; verified source DOI, authors and SHA256 are in the JSON catalogue."]
        for entry, _ in newly_staged:
            additions.append(
                f"- {entry['authors']} ({entry['year']}), *{entry['title']}*. "
                f"DOI https://doi.org/{entry['doi']}. Source {entry['source_url']}. "
                f"Original file {Path(entry['path']).name}, SHA256 {entry['sha256']}."
            )
        readme.write_text(old.rstrip()+"\n"+"\n".join(additions)+"\n",encoding="utf-8")
    print(json.dumps({"new_pdfs":len(newly_staged),"total":len(catalog["documents"]),
                      "failures":failures},ensure_ascii=False,indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
