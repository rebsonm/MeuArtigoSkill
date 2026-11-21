#!/usr/bin/env python3
"""One-time, explicit public CC BY 4.0 original-PDF intake on a draft branch.

Only the exact pre-reviewed publisher/repository sources below are eligible.
No private Google Drive, bulk library, user credentials, token, LLM or MCP.
Downloaded bytes retain PDF source format; SHA256 and size are recorded.
No tag, merge, release, install ZIP change or scientific gate approval.
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
MAX_PDF_BYTES = 19_000_000
MAX_TOTAL_BYTES = 45_000_000

ALLOWED_HOSTS = {
    "link.springer.com", "media.springernature.com",
    "static-content.springer.com", "www.springer.com",
    "researchonline.jcu.edu.au", "www.ssoar.info",
    "journals.plos.org", "besjournals.onlinelibrary.wiley.com",
    "onlinelibrary.wiley.com", "api.wiley.com",
}

# Each journal/repository page was separately inspected for a CC BY 4.0
# notice; rights evidence describes the version of record, not a blanket
# license for other files in the user's research archive.
CANDIDATES = [
    {
        "file": "page-et-al-2021-prisma.pdf",
        "title": "The PRISMA 2020 statement: an updated guideline for reporting systematic reviews",
        "authors": "Matthew J. Page et al.",
        "year": 2021,
        "doi": "10.1186/s13643-021-01626-4",
        "pdf_url": "https://link.springer.com/content/pdf/10.1186/s13643-021-01626-4.pdf",
        "source_url": "https://link.springer.com/article/10.1186/s13643-021-01626-4",
        "rights_evidence": "https://link.springer.com/article/10.1186/s13643-021-01626-4",
        "keywords": ["prisma", "systematic", "review", "reporting", "flow", "revisao", "sistematica"],
    },
    {
        "file": "haddaway-et-al-2018-roses.pdf",
        "title": "ROSES RepOrting standards for Systematic Evidence Syntheses",
        "authors": "Neal R. Haddaway; Biljana Macura; Paul Whaley; Andrew S. Pullin",
        "year": 2018,
        "doi": "10.1186/s13750-018-0121-7",
        "pdf_url": "https://link.springer.com/content/pdf/10.1186/s13750-018-0121-7.pdf",
        "source_url": "https://link.springer.com/article/10.1186/s13750-018-0121-7",
        "rights_evidence": "https://link.springer.com/article/10.1186/s13750-018-0121-7",
        "keywords": ["roses", "systematic", "evidence", "maps", "environmental", "protocol", "review"],
    },
    {
        "file": "byrne-2022-reflexive-thematic-analysis.pdf",
        "title": "A worked example of Braun and Clarke's approach to reflexive thematic analysis",
        "authors": "David Byrne",
        "year": 2022,
        "doi": "10.1007/s11135-021-01182-y",
        "pdf_url": "https://link.springer.com/content/pdf/10.1007/s11135-021-01182-y.pdf",
        "source_url": "https://link.springer.com/article/10.1007/s11135-021-01182-y",
        "rights_evidence": "https://link.springer.com/article/10.1007/s11135-021-01182-y",
        "keywords": ["reflexive", "thematic", "qualitative", "braun", "clarke", "coding"],
    },
    {
        "file": "busetto-wick-gumbinger-2020.pdf",
        "title": "How to use and assess qualitative research methods",
        "authors": "Loraine Busetto; Wolfgang Wick; Christoph Gumbinger",
        "year": 2020,
        "doi": "10.1186/s42466-020-00059-z",
        "pdf_url": "https://link.springer.com/content/pdf/10.1186/s42466-020-00059-z.pdf",
        "source_url": "https://link.springer.com/article/10.1186/s42466-020-00059-z",
        "rights_evidence": "https://link.springer.com/article/10.1186/s42466-020-00059-z",
        "keywords": ["qualitative", "quality", "sampling", "interview", "observation", "assessment"],
    },
    {
        "file": "harrison-birks-franklin-mills-2017.pdf",
        "title": "Case Study Research: Foundations and Methodological Orientations",
        "authors": "Helena Harrison; Melanie Birks; Richard Franklin; Jane Mills",
        "year": 2017,
        "doi": "10.17169/fqs-18.1.2655",
        "pdf_url": "https://researchonline.jcu.edu.au/47422/1/47422_Birks_2017.pdf",
        "source_url": "https://researchonline.jcu.edu.au/47422/",
        "rights_evidence": "https://researchonline.jcu.edu.au/47422/",
        "keywords": ["case", "study", "yin", "merriam", "stake", "qualitative", "context"],
    },
    {
        "file": "guest-namey-chen-2020-saturation.pdf",
        "title": "A simple method to assess and report thematic saturation in qualitative research",
        "authors": "Greg Guest; Emily Namey; Mario Chen",
        "year": 2020,
        "doi": "10.1371/journal.pone.0232076",
        "pdf_url": "https://journals.plos.org/plosone/article/file?id=10.1371%2Fjournal.pone.0232076&type=printable",
        "source_url": "https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0232076",
        "rights_evidence": "https://journals.plos.org/plosone/s/licenses-and-copyright",
        "keywords": ["saturation", "qualitative", "sampling", "interviews", "threshold", "thematic"],
    },
    {
        "file": "nyumba-wilson-derrick-mukherjee-2018.pdf",
        "title": "The use of focus group discussion methodology: Insights from two decades of application in conservation",
        "authors": "Tobias O. Nyumba; Kerrie Wilson; Christina J. Derrick; Nibedita Mukherjee",
        "year": 2018,
        "doi": "10.1111/2041-210X.12860",
        "pdf_url": "https://besjournals.onlinelibrary.wiley.com/doi/pdfdirect/10.1111/2041-210X.12860",
        "source_url": "https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.12860",
        "rights_evidence": "https://besjournals.onlinelibrary.wiley.com/doi/pdfdirect/10.1111/2041-210X.12860",
        "keywords": ["focus", "group", "discussion", "qualitative", "moderator", "conservation"],
    },
]


class OnlyReviewedHTTPSRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlsplit(newurl)
        if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
            raise ValueError("UNREVIEWED_REDIRECT_HOST")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def read_public_pdf(url: str) -> bytes:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("URL_NOT_ALLOWED")
    opener = urllib.request.build_opener(OnlyReviewedHTTPSRedirects())
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "MeuArtigoSkill-Public-CCBY-Intake/1.0 (+https://github.com/rebsonm/MeuArtigoSkill)",
            "Accept": "application/pdf",
        },
    )
    with opener.open(request, timeout=22) as response:
        if urllib.parse.urlsplit(response.geturl()).hostname not in ALLOWED_HOSTS:
            raise ValueError("FINAL_HOST_NOT_ALLOWED")
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_PDF_BYTES:
            raise ValueError("PDF_TOO_LARGE")
        payload = response.read(MAX_PDF_BYTES + 1)
    if not (isinstance(payload, bytes) and 8_000 <= len(payload) <= MAX_PDF_BYTES
            and payload.startswith(b"%PDF-") and b"%%EOF" in payload[-4096:]):
        raise ValueError("INVALID_OR_OVERSIZED_ORIGINAL_PDF")
    return payload


def main() -> int:
    if not CATALOG.is_file() or not PDF_DIR.is_dir():
        print("CATALOG_OR_PDF_FOLDER_MISSING", file=sys.stderr)
        return 2
    doc = json.loads(CATALOG.read_text(encoding="utf-8"))
    if doc.get("schema") != "MEU_ARTIGO_PUBLIC_PDF_CATALOG_V1":
        raise ValueError("INVALID_CATALOG_SCHEMA")
    existing = {x["path"] for x in doc["documents"]}
    existing_dois = {x["doi"].casefold() for x in doc["documents"]}
    staged = []
    total = 0
    failures = []
    for item in CANDIDATES:
        path = "knowledge/methodology/pdfs/" + item["file"]
        if not re.fullmatch(r"knowledge/methodology/pdfs/[a-z0-9][a-z0-9_-]{2,75}\\.pdf", path):
            raise ValueError("UNSAFE_PDF_PATH")
        if path in existing or item["doi"].casefold() in existing_dois:
            print("ALREADY_CATALOGUED:", item["doi"])
            continue
        try:
            blob = read_public_pdf(item["pdf_url"])
        except (OSError, ValueError, urllib.error.URLError, TimeoutError) as exc:
            failures.append({"doi": item["doi"], "kind": type(exc).__name__})
            print("SOURCE_UNAVAILABLE:", item["doi"], type(exc).__name__)
            continue
        total += len(blob)
        if total > MAX_TOTAL_BYTES:
            failures.append({"doi": item["doi"], "kind": "TOTAL_BUDGET_EXCEEDED"})
            break
        digest = hashlib.sha256(blob).hexdigest()
        entry = {
            "path": path, "title": item["title"], "authors": item["authors"],
            "year": item["year"], "doi": item["doi"],
            "size": len(blob), "sha256": digest,
            "rights": "PUBLIC_REDISTRIBUTION_REVIEWED",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "rights_evidence": item["rights_evidence"],
            "source_url": item["source_url"],
            "source_pdf_url": item["pdf_url"],
            "source_bytes_unmodified": True,
            "keywords": item["keywords"],
        }
        staged.append((entry, blob))
    if not staged:
        print(json.dumps({"new_pdf_count": 0, "failed_sources": failures}, indent=2))
        return 0
    for entry, blob in staged:
        target = ROOT / entry["path"]
        if target.exists():
            raise ValueError("REFUSE_OVERWRITE")
        target.write_bytes(blob)
        doc["documents"].append(entry)
        print("STAGED_PUBLIC_PDF:", entry["doi"], entry["size"], entry["sha256"])
    doc["version"] = "pilot-cc-by-2026-11-21-multi-source"
    doc["catalog_status"] = f"{len(doc['documents'])}_PUBLIC_LICENSE_REVIEWED_ARTICLES"
    doc["note"] = (
        "Only original licensed public PDFs are stored. Catalog hashes and source "
        "license evidence document technical provenance, not independent scientific "
        "or legal validation. Private archive remains metadata-only."
    )
    CATALOG.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    readme = PDF_DIR / "README.md"
    old = readme.read_text(encoding="utf-8")
    old = old.replace("These are **six source PDFs**",
                      f"These are **{len(doc['documents'])} source PDFs**")
    old = old.replace("**Six source PDFs are publicly hosted;",
                      f"**{len(doc['documents'])} source PDFs are publicly hosted;")
    new_lines = ["", "## Additional original PDFs with individual CC BY 4.0 evidence",
                 "", "These are unchanged source PDFs; they are NOT part of the installed ZIP.",
                 ""]
    for entry, blob in staged:
        new_lines.append(
            f"- {entry['authors']} ({entry['year']}), *{entry['title']}*. "
            f"DOI: https://doi.org/{entry['doi']}. "
            f"[Publisher/licensing evidence]({entry['rights_evidence']}). "
            f"Original \`{Path(entry['path']).name}\`, SHA-256 \`{entry['sha256']}\`."
        )
    readme.write_text(old.rstrip() + "\n" + "\n".join(new_lines) + "\n", encoding="utf-8")
    print(json.dumps({"new_pdf_count": len(staged),
                      "catalog_total": len(doc["documents"]),
                      "failed_sources": failures}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
