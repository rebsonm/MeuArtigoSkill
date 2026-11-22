#!/usr/bin/env python3
"""Test-only PDF-bearing Skill ZIP. No public release or legal certification."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from build_skill_bundle import verify_package, FIXED_DATE

CATALOG = "knowledge/methodology/pdf_catalog.json"
SCOPE = "knowledge/methodology/intake/PUBLIC-PDF-TEST-APPROVALS-2026-11-22.json"
PDF_PATH = re.compile(r"knowledge/methodology/pdfs/[a-z0-9][a-z0-9_-]{2,75}\.pdf\Z")
SHA = re.compile(r"[a-f0-9]{64}\Z")
MANIFEST = "BUNDLE_MANIFEST.json"
NOTICE = "THIRD_PARTY_PDF_NOTICES.md"
SCOPE_COPY = "PUBLIC_PDF_TEST_SCOPE.json"


def digest(value):
    return hashlib.sha256(value).hexdigest()


def _info(name):
    info = ZipInfo(name, FIXED_DATE)
    info.compress_type = ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    return info


def select(root):
    root = root.resolve()
    scope_path = root / SCOPE
    if scope_path.is_symlink() or not scope_path.is_file():
        raise ValueError("REVIEW_SCOPE_MISSING_OR_LINKED")
    scope = json.loads(scope_path.read_text(encoding="utf-8"))
    if (scope.get("schema") != "MEU_ARTIGO_REVIEWED_PDF_PACKAGE_SCOPE_V1"
            or scope.get("candidate_use") != "TEST_ONLY_NOT_PUBLIC_RELEASE"
            or scope.get("source_catalogue_path") != CATALOG
            or not isinstance(scope.get("documents"), list)):
        raise ValueError("INVALID_REVIEW_SCOPE")
    catalog = json.loads((root / CATALOG).read_text(encoding="utf-8"))
    if catalog.get("schema") != "MEU_ARTIGO_PUBLIC_PDF_CATALOG_V1":
        raise ValueError("INVALID_SOURCE_CATALOG")
    sources = {d["path"]: d for d in catalog["documents"]}
    if len(sources) != len(catalog["documents"]):
        raise ValueError("DUPLICATE_CATALOG_PATH")
    result, visited, total_bytes = [], set(), 0
    for item in scope["documents"]:
        if not isinstance(item, dict):
            raise ValueError("INVALID_REVIEW_ENTRY")
        name = item.get("path")
        if (not isinstance(name, str) or not PDF_PATH.fullmatch(name)
                or name in visited or name not in sources):
            raise ValueError("UNREVIEWED_OR_DUPLICATE_PDF_PATH")
        visited.add(name)
        source = sources[name]
        if (item.get("license") != "CC BY 4.0"
                or source.get("license") != "CC BY 4.0"
                or source.get("rights") != "PUBLIC_REDISTRIBUTION_REVIEWED"
                or item.get("scope") != "CC_BY_4_0_ATTRIBUTION_REQUIRED"
                or item.get("review_actor") != "AI_ASSISTANT_DOCUMENTARY_CHECK"
                or item.get("exact_pdf_licence_certified_by_human") is not False
                or item.get("review_basis") not in {
                    "PLOS_APPLIES_CC_BY4_UNLESS_EXCEPTION_AND_ARTICLE_METADATA_REVIEWED",
                    "PRIMARY_ARTICLE_LICENSE_STATEMENT_REVIEWED"}
                or item.get("sha256") != source.get("sha256")
                or item.get("size") != source.get("size")
                or item.get("doi") != source.get("doi")
                or not isinstance(item.get("sha256"), str)
                or not SHA.fullmatch(item["sha256"])
                or not isinstance(item.get("rights_evidence_url"), str)
                or not item["rights_evidence_url"].startswith("https://")):
            raise ValueError("PDF_SCOPE_SOURCE_RIGHTS_MISMATCH:" + name)
        if item["review_basis"].startswith("PLOS_"):
            policy = item.get("publisher_policy_url")
            if (not item["doi"].startswith("10.1371/journal.")
                    or not isinstance(policy, str)
                    or not policy.startswith("https://journals.plos.org/")
                    or not item["rights_evidence_url"].startswith("https://journals.plos.org/")):
                raise ValueError("PLOS_POLICY_MISMATCH")
        path = root / name
        if not path.is_file() or path.is_symlink():
            raise ValueError("SOURCE_FILE_MISSING_OR_LINKED:" + name)
        data = path.read_bytes()
        if (not data.startswith(b"%PDF-") or len(data) > 20_000_000
                or len(data) != item["size"] or digest(data) != item["sha256"]):
            raise ValueError("PDF_BYTES_NOT_ORIGINAL:" + name)
        total_bytes += len(data)
        if total_bytes > 90_000_000:
            raise ValueError("PDF_TEST_PACKAGE_SIZE_EXCEEDED")
        result.append((item, source, data))
    if not result:
        raise ValueError("NO_EXPLICITLY_SELECTED_PDFS")
    return result, scope


def notices(selected):
    lines = [
        "# Third-party PDF notices (test candidate only)",
        "",
        "These original third-party PDF files are NOT Apache-2.0 software.",
        "Their declared CC BY 4.0 license requires credit, source and",
        "license links. PDF modifications: NONE. No author endorsement.",
        "Licensing: https://creativecommons.org/licenses/by/4.0/",
        "This archive is NOT an approved public stable release.",
        "Documentary review was by an AI assistant, NOT a human legal auditor.",
        "",
    ]
    for item, source, _ in sorted(selected, key=lambda entry: entry[0]["path"]):
        lines.extend([
            "## " + source["title"].replace("\n", " "),
            "",
            "Authors: " + source["authors"].replace("\n", " "),
            "Year: " + str(source["year"]),
            "DOI: https://doi.org/" + source["doi"],
            "Publisher: " + source["source_url"],
            "Rights evidence: " + item["rights_evidence_url"],
            "License: CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/",
            "Unmodified PDF path: " + item["path"],
            "Original SHA-256: " + item["sha256"],
            "",
        ])
    return ("\n".join(lines) + "\n").encode("utf-8")


def build(root: Path, base_zip: Path, output_zip: Path):
    root, base_zip, output_zip = root.resolve(), base_zip.resolve(), output_zip.resolve()
    if (output_zip == base_zip or "TEST-ONLY" not in output_zip.name
            or not base_zip.is_file() or base_zip.is_symlink()
            or output_zip.is_symlink()):
        raise ValueError("ONLY_NEW_TEST_ARCHIVE_ALLOWED")
    verify_package(base_zip)
    selected, scope = select(root)
    with ZipFile(base_zip) as z:
        names = z.namelist()
        if (NOTICE in names or SCOPE_COPY in names
                or any(n.startswith("knowledge/methodology/pdfs/") for n in names)):
            raise ValueError("BASE_PACKAGE_NOT_SKILL_ONLY")
        original = json.loads(z.read(MANIFEST))
        if original.get("publication_verified") is not False:
            raise ValueError("PUBLICATION_FLAG_MUST_BE_FALSE")
        payload = {name: z.read(name) for name in names if name != MANIFEST}
    for item, _, data in selected:
        payload[item["path"]] = data
    payload[NOTICE] = notices(selected)
    payload[SCOPE_COPY] = (json.dumps(scope, indent=2, sort_keys=True,
                                    ensure_ascii=False) + "\n").encode("utf-8")
    original["files"] = {name: digest(data) for name, data in sorted(payload.items())}
    original["third_party_pdfs"] = len(selected)
    original["pdf_distribution_scope"] = "TEST_ONLY_RIGHTS_REVIEW_INCOMPLETE"
    original["publication_verified"] = False
    manifest_bytes = (json.dumps(original, indent=2, sort_keys=True,
                                 ensure_ascii=False) + "\n").encode("utf-8")
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output_zip, "w", compression=ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(payload.items()):
            z.writestr(_info(name), data, compress_type=ZIP_DEFLATED, compresslevel=9)
        z.writestr(_info(MANIFEST), manifest_bytes, compress_type=ZIP_DEFLATED,
                   compresslevel=9)
    verified = verify_package(output_zip)
    return {"status": "PASS", "scope": "TEST_ONLY",
            "pdfs_in_package": len(selected),
            "pdf_raw_bytes": sum(len(data) for _, _, data in selected),
            "total_files": len(verified["files"]),
            "zip_sha256": digest(output_zip.read_bytes()),
            "manifest_sha256": digest(manifest_bytes),
            "public_release_authorized": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--base-zip", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    print(json.dumps(build(args.repo, args.base_zip, args.out),
                     indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
