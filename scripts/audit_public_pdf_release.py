#!/usr/bin/env python3
"""Read-only technical preflight for optional public-PDF distribution.

Hash checks do not create copyright rights. The release decision remains
blocked until exact-version licenses, attribution, and publisher permissions
are independently reviewed. This script never copies or publishes PDFs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

PDF_SUBDIR = Path("knowledge/methodology/pdfs")
CATALOG = Path("knowledge/methodology/pdf_catalog.json")
PDF_PATH = re.compile(r"knowledge/methodology/pdfs/[a-z0-9][a-z0-9_-]{2,75}\\.pdf\\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\\Z")
MAX_SINGLE_BYTES = 20_000_000
MAX_PDF_BYTES = 100_000_000


def _digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            h.update(block)
    return h.hexdigest()


def audit(root: Path) -> dict:
    root = root.resolve()
    source = root / CATALOG
    catalogue = json.loads(source.read_text(encoding="utf-8"))
    docs = catalogue.get("documents")
    if catalogue.get("schema") != "MEU_ARTIGO_PUBLIC_PDF_CATALOG_V1" or not isinstance(docs, list):
        raise ValueError("INVALID_PDF_CATALOGUE")
    if len(docs) > 600:
        raise ValueError("PDF_CATALOGUE_TOO_LARGE")
    entries, issues, encountered, total_bytes = [], [], set(), 0
    pdf_dir = root / PDF_SUBDIR
    if not pdf_dir.is_dir() or pdf_dir.is_symlink():
        raise ValueError("PUBLIC_PDF_FOLDER_MISSING_OR_LINKED")
    for n, item in enumerate(docs, 1):
        name = item.get("path")
        if not isinstance(name, str) or not PDF_PATH.fullmatch(name) or name in encountered:
            issues.append({"row": n, "issue": "UNSAFE_OR_DUPLICATE_FILE_PATH"})
            continue
        encountered.add(name)
        target = root / name
        source_rights = item.get("rights")
        license_tag = item.get("license")
        requested_size = item.get("size")
        expected_digest = item.get("sha256")
        evidence = item.get("rights_evidence")
        url = item.get("source_url")
        license_url = item.get("license_url")
        author = item.get("authors")
        title = item.get("title")
        doi = item.get("doi")
        year = item.get("year")
        mistakes = []
        if source_rights != "PUBLIC_REDISTRIBUTION_REVIEWED":
            mistakes.append("RIGHTS_CLAIM_NOT_REVIEWED")
        if license_tag not in {"CC BY 4.0", "CC BY"}:
            mistakes.append("LICENSE_NOT_APPROVED_FOR_GENERAL_REUSE")
        if not isinstance(evidence, str) or not evidence.startswith("https://"):
            mistakes.append("PUBLISHER_RIGHTS_EVIDENCE_MISSING")
        if not isinstance(url, str) or not url.startswith("https://"):
            mistakes.append("SOURCE_URL_MISSING")
        if not isinstance(license_url, str) or not license_url.startswith("https://"):
            mistakes.append("LICENSE_URL_MISSING")
        if not isinstance(author, str) or not author.strip() or not isinstance(title, str) or not title.strip():
            mistakes.append("AUTHORS_OR_TITLE_MISSING")
        if not isinstance(year, int) or not (1800 <= year <= 2100):
            mistakes.append("YEAR_INVALID")
        if not isinstance(doi, str) or not doi.strip():
            mistakes.append("DOI_MISSING")
        if not isinstance(expected_digest, str) or not SHA256.fullmatch(expected_digest):
            mistakes.append("CATALOG_SHA256_INVALID")
        if (not isinstance(requested_size, int) or requested_size <= 0
                or requested_size > MAX_SINGLE_BYTES):
            mistakes.append("CATALOG_FILE_SIZE_INVALID")
        observed_size, observed_hash = None, None
        if not target.is_file() or target.is_symlink():
            mistakes.append("PDF_BINARY_MISSING_OR_LINKED")
        else:
            observed_size = target.stat().st_size
            total_bytes += observed_size
            if observed_size > MAX_SINGLE_BYTES:
                mistakes.append("PDF_BINARY_TOO_LARGE")
            if observed_size != requested_size:
                mistakes.append("PDF_SIZE_MISMATCH")
            if observed_size <= MAX_SINGLE_BYTES:
                observed_hash = _digest(target)
                if observed_hash != expected_digest:
                    mistakes.append("PDF_SHA256_MISMATCH")
        # A version-unknown BY label is not silently promoted to CC BY 4.0.
        if license_tag == "CC BY":
            mistakes.append("PUBLISHER_LICENSE_VERSION_REQUIRES_REVIEW")
        status = ("TECHNICAL_CANDIDATE_NOT_LEGAL_CLEARANCE"
                  if not mistakes else "PENDING_RECONCILIATION")
        entries.append({"path": name, "doi": doi, "title": title,
                        "authors": author, "year": year,
                        "license": license_tag, "license_url": license_url,
                        "rights_evidence": evidence, "source_url": url,
                        "catalog_sha256": expected_digest, "verified_sha256": observed_hash,
                        "size_bytes": observed_size, "review_status": status,
                        "issues": mistakes})
        for err in mistakes:
            issues.append({"path": name, "issue": err})
    discovered = {p.relative_to(root).as_posix() for p in pdf_dir.rglob("*.pdf")}
    extra = sorted(discovered - encountered)
    for name in extra:
        issues.append({"path": name, "issue": "UNLISTED_PDF_BINARY"})
    if total_bytes > MAX_PDF_BYTES:
        issues.append({"issue": "PDF_CORPUS_EXCEEDS_ARCHIVE_SAFETY_BUDGET"})
    integrity_errors = [item for item in issues if item["issue"] in {
        "UNSAFE_OR_DUPLICATE_FILE_PATH", "PDF_BINARY_MISSING_OR_LINKED",
        "PDF_BINARY_TOO_LARGE", "PDF_SIZE_MISMATCH", "PDF_SHA256_MISMATCH",
        "CATALOG_SHA256_INVALID", "CATALOG_FILE_SIZE_INVALID",
        "UNLISTED_PDF_BINARY", "PDF_CORPUS_EXCEEDS_ARCHIVE_SAFETY_BUDGET"
    }]
    return {"schema": "MEU_ARTIGO_PUBLIC_PDF_RELEASE_PREFLIGHT_V1",
            "catalogued_pdfs": len(docs), "files_in_directory": len(discovered),
            "total_bytes": total_bytes,
            "technical_candidates": sum(x["review_status"] == "TECHNICAL_CANDIDATE_NOT_LEGAL_CLEARANCE"
                                        for x in entries),
            "pending_reconciliation": sum(x["review_status"] == "PENDING_RECONCILIATION"
                                          for x in entries),
            "integrity_status": "PASS" if not integrity_errors else "FAIL",
            "release_clearance": "BLOCKED_PENDING_INDEPENDENT_RIGHTS_REVIEW",
            "credits_generated_from_catalogue_not_independent_legal_attestation": True,
            "issues": issues, "documents": entries}


def _safe(value) -> str:
    return str(value or "").replace("|", "\\|").replace("\\n", " ").replace("\\r", " ")


def attribution_register(result: dict) -> str:
    lines = [
        "# Candidate PDF attribution register (NOT an authorization to redistribute)",
        "",
        "Automatically transcribed from the public catalogue. Author, title, DOI,",
        "source publisher page and declared license are presented for independent",
        "verification. A public release must also preserve any notices included",
        "in the original PDF; catalogue metadata is NOT proof of legal clearance.",
        "",
        "| Work / authors | DOI | Declared license | Publisher evidence | State |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in result["documents"]:
        line = f'| {_safe(item["authors"])} ({_safe(item["year"])}), *{_safe(item["title"])}* | '
        line += f'{_safe(item["doi"])} | {_safe(item["license"])} | '
        line += f'{_safe(item["rights_evidence"])} | {_safe(item["review_status"])} |'
        lines.append(line)
    lines.extend(["", "No independent full-text license verification or distribution",
                  "permission is asserted by this generated register.", ""])
    return "\\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--verify-only", action="store_true",
                   help="CI: check exact PDF size/hash and catalogue coverage, not rights")
    p.add_argument("--out-json", type=Path)
    p.add_argument("--out-credits", type=Path)
    args = p.parse_args(argv)
    result = audit(args.repo)
    if args.out_json:
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    if args.out_credits:
        args.out_credits.parent.mkdir(parents=True, exist_ok=True)
        args.out_credits.write_text(attribution_register(result), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in {"issues", "documents"}},
                     ensure_ascii=False, indent=2))
    print("issues_count=" + str(len(result["issues"])))
    return 0 if result["integrity_status"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
