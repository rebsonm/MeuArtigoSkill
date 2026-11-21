#!/usr/bin/env python3
"""Opt-in, read-only search of 475 *bibliographic prospecting* cards.

These records are NOT full-text summaries or primary-source citations. Only
the original bibliographic catalogue, user-authored prospecting questions and
source metadata are read. They never authorize a private-PDF download.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys

import consult_github_methodology as gh

INDEX = "knowledge/methodology/source_registry_catalog.json"
SCHEMA = "MEU_ARTIGO_SOURCE_CARD_INDEX_V1"
DEFAULT_REF = "d6eafb692e2332372570e7d9a39ceb4fc27f9e48"
PATH = re.compile(r"knowledge/methodology/source_cards/src-[0-9]{4}\.md\Z")
REF = re.compile(r"[0-9a-f]{40}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
MAX_CATALOG_BYTES = 850_000
MAX_CARD_BYTES = 6_500
MAX_RECORDS = 600
MAX_CONTEXT = 6_500
MIN_CONTEXT = 350
MAX_QUESTION = 800
_ALLOWED_RIGHTS = {"NOT_CHECKED", "VERIFIED_PUBLISHER_LICENSE"}


def _catalog(blob: bytes) -> list[dict]:
    if not isinstance(blob, bytes) or len(blob) > MAX_CATALOG_BYTES:
        raise ValueError("REGISTRY_CATALOG_TOO_LARGE")
    try:
        root = json.loads(blob.decode("utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ValueError("REGISTRY_CATALOG_NOT_UTF8_JSON") from exc
    if not isinstance(root, dict) or root.get("schema") != SCHEMA:
        raise ValueError("REGISTRY_SCHEMA_INVALID")
    docs = root.get("documents")
    if root.get("source_text_read_in_ledger") != sum(
            1 for d in (docs if isinstance(docs, list) else [])
            if isinstance(d, dict) and d.get("source_read_scope") != "NOT_RECORDED_IN_LEDGER"):
        raise ValueError("REGISTRY_READING_COUNT_INCONSISTENT")
    if not isinstance(docs, list) or len(docs) != 475 or len(docs) > MAX_RECORDS:
        raise ValueError("REGISTRY_DOCUMENT_COUNT_INVALID")
    if root.get("third_party_full_text_included") is not False:
        raise ValueError("REGISTRY_MUST_NOT_CONTAIN_SOURCE_TEXT")
    paths = set()
    ids = set()
    for doc in docs:
        if not isinstance(doc, dict):
            raise ValueError("REGISTRY_ENTRY_INVALID")
        path = doc.get("path")
        sid = doc.get("source_id")
        if not isinstance(path, str) or not PATH.fullmatch(path) or path in paths:
            raise ValueError("REGISTRY_PATH_UNSAFE")
        if not isinstance(sid, str) or not re.fullmatch(r"SRC-[0-9]{4}", sid) or sid in ids:
            raise ValueError("REGISTRY_DUPLICATE_ID")
        if path.rsplit("/", 1)[-1] != sid.lower() + ".md":
            raise ValueError("REGISTRY_ID_PATH_MISMATCH")
        if doc.get("source_metadata_only") is not True:
            raise ValueError("REGISTRY_NOT_METADATA_ONLY")
        if not isinstance(doc.get("sha256"), str) or not DIGEST.fullmatch(doc["sha256"]):
            raise ValueError("REGISTRY_HASH_REQUIRED")
        if not isinstance(doc.get("title"), str) or not doc["title"] or len(doc["title"]) > 175:
            raise ValueError("REGISTRY_TITLE_INVALID")
        if not isinstance(doc.get("topic"), str) or len(doc["topic"]) > 150:
            raise ValueError("REGISTRY_TOPIC_INVALID")
        terms = doc.get("keywords")
        if not isinstance(terms, list) or len(terms) > 24 or any(
                not isinstance(t, str) or len(t) > 55 for t in terms):
            raise ValueError("REGISTRY_KEYWORDS_INVALID")
        if doc.get("rights_review") not in _ALLOWED_RIGHTS:
            raise ValueError("REGISTRY_RIGHTS_INVALID")
        if doc.get("has_original_public_pdf") and (
                doc["rights_review"] != "VERIFIED_PUBLISHER_LICENSE"
                or not isinstance(doc.get("public_pdf_path"), str)
                or not doc["public_pdf_path"].startswith("knowledge/methodology/pdfs/")):
            raise ValueError("REGISTRY_UNLICENSED_PDF_REFERENCE")
        if doc.get("bibliography_match_status") not in {
                "CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED", "IDENTITY_UNRESOLVED"}:
            raise ValueError("REGISTRY_MATCH_STATUS_INVALID")
        paths.add(path)
        ids.add(sid)
    return docs


def _score(question: str, item: dict) -> int:
    query_terms = gh._terms(question)
    if not query_terms:
        return 0
    title_terms = gh._terms(item["title"])
    topic_terms = gh._terms(item["topic"])
    keyword_terms = gh._terms(" ".join(item["keywords"]))
    id_terms = gh._terms(item["source_id"])
    coverage = {t for t in query_terms if t in title_terms or
                t in topic_terms or t in keyword_terms or t in id_terms}
    if len(query_terms) >= 3 and len(coverage) * 2 < len(query_terms):
        return 0
    if not coverage:
        return 0
    return (sum(5 for t in query_terms if t in title_terms) +
            sum(3 for t in query_terms if t in topic_terms) +
            sum(2 for t in query_terms if t in keyword_terms) +
            sum(12 for t in query_terms if t in id_terms))


def query(question: str, *, ref: str, top: int = 3,
          max_chars: int = 3400, fetch=None) -> dict:
    if not isinstance(ref, str) or not REF.fullmatch(ref):
        raise ValueError("IMMUTABLE_COMMIT_REQUIRED")
    if not isinstance(question, str) or not question.strip() or len(question) > MAX_QUESTION:
        raise ValueError("QUESTION_INVALID")
    if not (1 <= top <= 5 and MIN_CONTEXT <= max_chars <= MAX_CONTEXT):
        raise ValueError("CONTEXT_LIMIT_INVALID")
    fetcher = gh._fetch if fetch is None else fetch
    raw = fetcher(ref, INDEX, MAX_CATALOG_BYTES)
    docs = _catalog(raw)
    matches = sorted(((_score(question, x), x) for x in docs),
                     key=lambda y: (-y[0], y[1]["path"]))
    candidates = [item for score, item in matches if score > 0][:top]
    left = max_chars
    hits = []
    for item in candidates:
        if left <= 0:
            break
        raw = fetcher(ref, item["path"], MAX_CARD_BYTES)
        if not isinstance(raw, bytes) or not 0 < len(raw) <= MAX_CARD_BYTES:
            raise ValueError("REGISTRY_CARD_BYTES_INVALID")
        if hashlib.sha256(raw).hexdigest() != item["sha256"]:
            raise ValueError("REGISTRY_CARD_DIGEST_MISMATCH")
        try:
            card = raw.decode("utf-8")
        except UnicodeError as exc:
            raise ValueError("REGISTRY_CARD_UTF8_INVALID") from exc
        excerpt = card[:left]
        hits.append({
            "source_id": item["source_id"],
            "title": item["title"],
            "topic": item["topic"],
            "path": item["path"],
            "github_commit": ref,
            "excerpt": excerpt,
            "excerpt_truncated": len(excerpt) < len(card),
            "citation_grade": "P_BIBLIOGRAPHIC_PROSPECTING_NOT_SOURCE_EVIDENCE",
            "source_work_directly_verified": False,
            "rights_review": item["rights_review"],
            "bibliography_match_status": item["bibliography_match_status"],
            "must_not_claim_primary_source_read": True,
            "scientific_review_approved": False,
        })
        left -= len(excerpt)
    return {
        "status": "BIBLIOGRAPHIC_LEADS_ONLY" if hits else "NO_MATCH",
        "retrieval_mode": "SOURCE_REGISTRY_LEXICAL_METADATA_ONLY",
        "returned_context_chars": max_chars - left,
        "hits": hits,
        "source_library_full_text_read": False,
        "scientific_quality_validated": False,
        "scientific_gate_approved": False,
        "private_sources_accessed": False,
        "public_pdf_upload_authorized_by_metadata": False,
        "warning": "These are bibliography leads and generic [P] prompts, not source-derived [I] conclusions or [L] support.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default=DEFAULT_REF)
    parser.add_argument("--question", required=True)
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--max-chars", type=int, default=3400)
    args = parser.parse_args(argv)
    try:
        result = query(args.question, ref=args.ref, top=args.top,
                       max_chars=args.max_chars)
    except (OSError, ValueError) as exc:
        result = {"status": "UNAVAILABLE_OR_BLOCKED",
                  "reason": str(exc),
                  "scientific_gate_approved": False,
                  "private_sources_accessed": False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "BIBLIOGRAPHIC_LEADS_ONLY" else 2


if __name__ == "__main__":
    sys.exit(main())
