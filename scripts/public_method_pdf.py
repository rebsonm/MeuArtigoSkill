#!/usr/bin/env python3
"""Optional public PDF reader for a standalone scientific Skill.

Download only a license-reviewed, SHA-pinned public PDF selected via small
metadata catalogue. Inspect only requested PDF pages and return bounded text.
The PDF remains the canonical source; page indices are not printed page numbers.
No private sources, access tokens, remote models, OCR, silent publishing or writes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
import unicodedata
from typing import Callable

REPO = "rebsonm/MeuArtigoSkill"
BASE = "https://raw.githubusercontent.com/" + REPO + "/"
CATALOG = "knowledge/methodology/pdf_catalog.json"
SCHEMA = "MEU_ARTIGO_PUBLIC_PDF_CATALOG_V1"
REF_RE = re.compile(r"[a-f0-9]{40}\Z")
SHA_RE = re.compile(r"[a-f0-9]{64}\Z")
PATH_RE = re.compile(r"knowledge/methodology/pdfs/[a-z0-9][a-z0-9_-]{2,75}\.pdf\Z")
WORDS = re.compile(r"[^\W_]+", re.UNICODE)
MAX_CATALOG = 40000
MAX_PDF = 20_000_000
MAX_SOURCES = 150
MAX_PAGES = 4
MAX_CONTEXT = 5000


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("GITHUB_REDIRECT_BLOCKED")


def fetch_github(ref: str, path: str, limit: int) -> bytes:
    if not REF_RE.fullmatch(ref) or (path != CATALOG and not PATH_RE.fullmatch(path)):
        raise ValueError("UNSAFE_REMOTE_REFERENCE")
    request = urllib.request.Request(
        BASE + ref + "/" + path,
        headers={"User-Agent": "MeuArtigoPDFReader/0.1", "Accept": "application/octet-stream"},
    )
    opener = urllib.request.build_opener(_NoRedirect)
    with opener.open(request, timeout=12) as response:
        length = response.headers.get("Content-Length")
        if length and int(length) > limit:
            raise ValueError("REMOTE_BYTES_EXCEED_LIMIT")
        value = response.read(limit + 1)
        if len(value) > limit:
            raise ValueError("REMOTE_BYTES_EXCEED_LIMIT")
        return value


def metadata(blob: bytes) -> list[dict]:
    if not isinstance(blob, bytes) or len(blob) > MAX_CATALOG:
        raise ValueError("CATALOG_TOO_LARGE")
    try:
        obj = json.loads(blob.decode("utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ValueError("CATALOG_INVALID_JSON") from exc
    if not isinstance(obj, dict) or obj.get("schema") != SCHEMA or not isinstance(obj.get("documents"), list):
        raise ValueError("CATALOG_INVALID_SCHEMA")
    docs = obj["documents"]
    if len(docs) > MAX_SOURCES:
        raise ValueError("CATALOG_TOO_MANY_PDFS")
    seen = set()
    for entry in docs:
        if not isinstance(entry, dict):
            raise ValueError("PDF_ENTRY_INVALID")
        path = entry.get("path")
        if not isinstance(path, str) or not PATH_RE.fullmatch(path) or path in seen:
            raise ValueError("PDF_PATH_UNSAFE_OR_DUPLICATE")
        seen.add(path)
        if entry.get("rights") != "PUBLIC_REDISTRIBUTION_REVIEWED":
            raise ValueError("PUBLIC_PDF_RIGHTS_NOT_REVIEWED")
        if (not isinstance(entry.get("rights_evidence"), str)
                or not entry["rights_evidence"].startswith("https://")
                or len(entry["rights_evidence"]) > 600):
            raise ValueError("PUBLIC_PDF_RIGHTS_EVIDENCE_REQUIRED")
        if not isinstance(entry.get("sha256"), str) or not SHA_RE.fullmatch(entry["sha256"]):
            raise ValueError("PUBLIC_PDF_SHA_REQUIRED")
        if not isinstance(entry.get("size"), int) or not 0 < entry["size"] <= MAX_PDF:
            raise ValueError("PUBLIC_PDF_SIZE_EXCEEDED")
        if not isinstance(entry.get("title"), str) or not entry["title"].strip() or len(entry["title"]) > 180:
            raise ValueError("PUBLIC_PDF_TITLE_INVALID")
        keys = entry.get("keywords")
        if (not isinstance(keys, list) or len(keys) > 30
                or any(not isinstance(x, str) or len(x) > 65 for x in keys)):
            raise ValueError("PUBLIC_PDF_KEYWORDS_INVALID")
    return docs


_STOPWORDS = {"the", "and", "for", "with", "from", "how", "what", "when",
              "para", "como", "uma", "com", "qual", "quais", "sobre",
              "por", "del", "los", "las", "con", "una"}

def _tokens(value: str) -> set[str]:
    if not isinstance(value, str):
        return set()
    folded = "".join(c for c in unicodedata.normalize("NFKD", value.casefold())
                     if not unicodedata.combining(c))
    return {w for w in WORDS.findall(folded)
            if len(w) > 2 and w not in _STOPWORDS}


def _score(question: str, item: dict) -> int:
    q = _tokens(question)
    return (sum(3 for w in q if w in _tokens(" ".join(item["keywords"])))
            + sum(2 for w in q if w in _tokens(item["title"])))


def query(question: str, *, ref: str, fetch: Callable = fetch_github,
          max_chars: int = 3000, max_pages: int = 2) -> dict:
    if not isinstance(question, str) or not question.strip() or len(question) > 800:
        raise ValueError("QUESTION_INVALID")
    if not isinstance(ref, str) or not REF_RE.fullmatch(ref):
        raise ValueError("IMMUTABLE_GITHUB_COMMIT_REQUIRED")
    if not 300 <= max_chars <= MAX_CONTEXT or not 1 <= max_pages <= MAX_PAGES:
        raise ValueError("RETRIEVAL_BUDGET_INVALID")
    documents = metadata(fetch(ref, CATALOG, MAX_CATALOG))
    ranked = sorted(((_score(question, doc), doc) for doc in documents),
                    key=lambda x: (-x[0], x[1]["path"]))
    candidates = [doc for score, doc in ranked if score > 0]
    if not candidates:
        return {"status": "NO_MATCH_IN_PUBLIC_PDF_CATALOG", "pdf_fetched": False,
                "hits": [], "no_source_read_claim": True,
                "scientific_quality_validated": False}
    item = candidates[0]
    blob = fetch(ref, item["path"], item["size"])
    if (not isinstance(blob, bytes) or len(blob) != item["size"]
            or hashlib.sha256(blob).hexdigest() != item["sha256"]):
        raise ValueError("PDF_SIZE_OR_HASH_MISMATCH")
    if not blob.startswith(b"%PDF-"):
        raise ValueError("NOT_A_PDF")
    try:
        import fitz
    except ImportError:
        return {"status": "PDF_VERIFIED_BUT_LOCAL_PDF_PARSER_UNAVAILABLE",
                "pdf_fetched": True, "hits": [], "source": item["path"],
                "scientific_quality_validated": False}
    with fitz.open(stream=blob, filetype="pdf") as pdf:
        if pdf.needs_pass:
            return {"status": "ENCRYPTED_PDF_REQUIRES_AUTHORIZED_ACCESS",
                    "pdf_fetched": True, "hits": [],
                    "scientific_quality_validated": False}
        q = _tokens(question)
        pages = []
        for idx in range(len(pdf)):
            page = pdf[idx]
            body = page.get_text("text")
            score = sum(body.casefold().count(term) for term in q)
            if score > 0:
                pages.append((score, idx + 1, body,
                              len(page.get_images(full=False)) > 0))
        if not pages:
            return {"status": "NO_MATCH_IN_EXTRACTABLE_PDF_TEXT",
                    "pdf_fetched": True, "source": item["path"],
                    "needs_visual_pdf_review": True, "hits": [],
                    "scientific_quality_validated": False}
        pages.sort(key=lambda p: (-p[0], p[1]))
        remaining = max_chars
        hits = []
        for score, number, body, has_images in pages[:max_pages]:
            excerpt = body[:remaining]
            if not excerpt:
                break
            hits.append({"title": item["title"], "source": item["path"],
                         "commit": ref, "pdf_page": number,
                         "page_label_verified": False, "excerpt": excerpt,
                         "truncated": len(excerpt) < len(body),
                         "visual_review_recommended": has_images,
                         "evidence_type": "EXTRACTED_PDF_PAGE_NOT_SCIENTIFICALLY_VALIDATED",
                         "authors": item.get("authors"), "year": item.get("year"),
                         "doi": item.get("doi"), "source_url": item.get("source_url"),
                         "license": item.get("license"), "sha256": item["sha256"]})
            remaining -= len(excerpt)
            if remaining <= 0:
                break
        return {"status": "RETRIEVED_PDF_PAGES" if hits else "NO_CONTEXT_BUDGET",
                "pdf_fetched": True, "pages_in_pdf": len(pdf),
                "returned_context_chars": max_chars - remaining,
                "hits": hits, "read_only": True,
                "scientific_quality_validated": False,
                "note": "PDF page index is not printed pagination. Verify source visually."}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--question", required=True)
    ap.add_argument("--ref", required=True, help="Immutable Git commit")
    ap.add_argument("--max-chars", type=int, default=3000)
    ap.add_argument("--max-pages", type=int, default=2)
    a = ap.parse_args(argv)
    try:
        result = query(a.question, ref=a.ref,
                       max_chars=a.max_chars, max_pages=a.max_pages)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, urllib.error.URLError, TimeoutError) as exc:
        print(json.dumps({"status": "UNAVAILABLE_OR_BLOCKED", "reason": str(exc),
                          "no_source_read_claim": True,
                          "scientific_quality_validated": False},
                         ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
