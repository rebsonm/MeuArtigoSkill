#!/usr/bin/env python3
"""Unified, read-only access to all 649 Meu Artigo cards at an immutable Git SHA.

475 source cards are bibliographic [P] leads, 174 are original editorial [I]/[P].
Blocked records remain visible in AUDIT mode but never return card text as
scientific evidence or as an active recommendation. No private PDFs are read.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import re
import sys

import consult_github_methodology as editorial
import consult_source_registry as bibliographic

SCHEMA = "MEU_ARTIGO_UNIFIED_649_CARDS_V1"
MAX_QUESTION = 800
MAX_TEXT = 5500
SRC_PATTERN = re.compile(r"SRC-[0-9]{4}\Z", re.IGNORECASE)
EC_PATTERN = re.compile(r"EC-[0-9]{4}\Z", re.IGNORECASE)
BLOCKED = {"BLOQUEADO_POR_EVIDENCIA", "EXCLUIDO_COM_JUSTIFICATIVA"}


def load(ref: str, fetch=None):
    """Load and validate both *complete* catalogues, without any card/PDF fetch."""
    if not isinstance(ref, str) or not editorial.REF_SHA.fullmatch(ref):
        raise ValueError("IMMUTABLE_GITHUB_SHA_REQUIRED")
    fetch = editorial._fetch if fetch is None else fetch
    src = bibliographic._catalog(fetch(ref, bibliographic.INDEX,
                                       bibliographic.MAX_CATALOG_BYTES))
    ed = editorial._catalog(fetch(ref, editorial.INDEX_PATH,
                                  editorial.MAX_INDEX_BYTES))
    if len(src) != 475 or len(ed) != 174:
        raise ValueError("INCOMPLETE_649_CARD_CATALOGUE")
    rows = []
    for item in src:
        rows.append({"id": item["source_id"], "kind": "BIBLIOGRAPHIC_PROSPECTING_P",
                     "title": item["title"], "path": item["path"],
                     "sha256": item["sha256"],
                     "terms": [item["title"], item["topic"]] + item["keywords"],
                     "disposition": item.get("operational_disposition", "NOT_REVIEWED"),
                     "source_identity": item.get("bibliography_match_status"),
                     "rights_review": item.get("rights_review", "NOT_CHECKED")})
    for idx, item in enumerate(ed, 1):
        rows.append({"id": f"EC-{idx:04d}", "kind": "ORIGINAL_EDITORIAL_I_P",
                     "title": item["title"], "path": item["path"],
                     "sha256": item["sha256"],
                     "terms": [item["title"]] + item["keywords"],
                     "disposition": item.get("operational_disposition", "NOT_REVIEWED"),
                     "source_identity": "NOT_APPLICABLE",
                     "rights_review": item["rights"]})
    if len(rows) != 649 or len({x["id"] for x in rows}) != 649 or len({x["path"] for x in rows}) != 649:
        raise ValueError("DUPLICATED_OR_INCOMPLETE_649_CARDS")
    return rows


def _public_record(row):
    blocked = row["disposition"] in BLOCKED
    return {"id": row["id"], "title": row["title"], "kind": row["kind"],
            "path": row["path"], "sha256": row["sha256"],
            "operational_disposition": row["disposition"],
            "available_for_guidance": not blocked,
            "citation_grade": "P_BIBLIOGRAPHIC_LEAD_ONLY"
            if row["kind"] == "BIBLIOGRAPHIC_PROSPECTING_P"
            else "I_P_ORIGINAL_EDITORIAL_GUIDANCE_ONLY",
            "source_identity": row["source_identity"],
            "rights_review": row["rights_review"],
            "scientific_quality_validated": False,
            "scientific_gate_approved": False,
            "source_pdf_read_in_this_query": False}


def select(rows, *, question=None, card_id=None, mode="guidance", top=5):
    """Selection is metadata-only, including for blocked audit records."""
    if mode not in {"guidance", "audit"} or not isinstance(top, int) or not 1 <= top <= 649:
        raise ValueError("INVALID_SELECTION")
    if (card_id is None) == (question is None):
        raise ValueError("QUESTION_XOR_CARD_ID_REQUIRED")
    if card_id is not None:
        if not isinstance(card_id, str) or not (SRC_PATTERN.fullmatch(card_id) or EC_PATTERN.fullmatch(card_id)):
            raise ValueError("INVALID_CARD_ID")
        matched = [x for x in rows if x["id"] == card_id.upper()]
    else:
        if not isinstance(question, str) or not question.strip() or len(question) > MAX_QUESTION:
            raise ValueError("INVALID_QUESTION")
        exact = re.findall(r"\b(?:SRC|EC)-[0-9]{4}\b", question, re.IGNORECASE)
        if exact:
            wanted = {x.upper() for x in exact}
            matched = [x for x in rows if x["id"] in wanted]
        else:
            tokens = editorial._terms(question)
            scored = []
            for x in rows:
                title = editorial._terms(x["title"])
                terms = editorial._terms(" ".join(x["terms"]))
                matched_terms = tokens & terms
                if matched_terms and (len(tokens) <= 2 or len(matched_terms)*2 >= len(tokens)):
                    scored.append((len(matched_terms)*2 + len(matched_terms & title)*3, x))
            matched = [x for _, x in sorted(scored, key=lambda t: (-t[0], t[1]["id"]))]
    if mode == "guidance":
        matched = [x for x in matched if x["disposition"] not in BLOCKED]
    return matched[:top]


def query(*, ref, question=None, card_id=None, mode="guidance", top=5,
          include_text=False, fetch=None):
    fetch = editorial._fetch if fetch is None else fetch
    rows = load(ref, fetch)
    chosen = select(rows, question=question, card_id=card_id, mode=mode, top=top)
    hits = []
    for row in chosen:
        item = _public_record(row)
        if include_text and mode == "guidance" and row["disposition"] not in BLOCKED:
            limit = (bibliographic.MAX_CARD_BYTES if row["id"].startswith("SRC-")
                     else editorial.MAX_CARD_BYTES)
            blob = fetch(ref, row["path"], limit)
            if (not isinstance(blob, bytes) or len(blob) > limit
                    or hashlib.sha256(blob).hexdigest() != row["sha256"]):
                raise ValueError("CARD_DIGEST_OR_BYTES_INVALID")
            try:
                value = blob.decode("utf-8")
            except UnicodeError as exc:
                raise ValueError("CARD_INVALID_UTF8") from exc
            item["excerpt"] = value[:MAX_TEXT]
            item["excerpt_truncated"] = len(value) > MAX_TEXT
            item["untrusted_reference_text"] = True
        hits.append(item)
    return {"schema": SCHEMA, "status": "RETRIEVED_FOR_REVIEW" if hits else "NO_ELIGIBLE_HITS",
            "ref": ref, "total_cards": 649, "bibliographic_cards": 475,
            "editorial_cards": 174,
            "dispositions": dict(Counter(x["disposition"] for x in rows)),
            "mode": mode, "hits": hits,
            "scientific_quality_validated": False,
            "private_sources_accessed": False,
            "scientific_gate_approved": False,
            "warning": "Bibliographic [P] leads and editorial [I]/[P] notes are not original [L] evidence; blocked records are audit-only."}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ref", default=editorial.DEFAULT_REF)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--question")
    group.add_argument("--id", dest="card_id")
    p.add_argument("--mode", choices=["guidance", "audit"], default="guidance")
    p.add_argument("--top", type=int, default=5)
    p.add_argument("--include-text", action="store_true")
    a = p.parse_args(argv)
    try:
        result = query(ref=a.ref, question=a.question, card_id=a.card_id,
                       mode=a.mode, top=a.top, include_text=a.include_text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "RETRIEVED_FOR_REVIEW" else 2
    except (ValueError, OSError, TimeoutError) as exc:
        print(json.dumps({"status": "UNAVAILABLE_OR_BLOCKED", "reason": str(exc),
                          "scientific_quality_validated": False}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
