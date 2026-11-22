#!/usr/bin/env python3
"""Create a reproducible, PDF-free public source copy for Zenodo review.

The source snapshot is NOT a new GitHub release, Zenodo deposit, or Skill
installer. Third-party PDF binaries are intentionally excluded.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_TIME = (2026, 11, 22, 0, 0, 0)

def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def as_zip(zf: zipfile.ZipFile, name: str, data: bytes) -> None:
    entry = zipfile.ZipInfo(name, date_time=ARCHIVE_TIME)
    entry.compress_type = zipfile.ZIP_DEFLATED
    entry.external_attr = 0o100644 << 16
    zf.writestr(entry, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Separate output directory (outside Git checkout)")
    args = parser.parse_args()
    out = Path(args.output).resolve()
    if out == ROOT or ROOT in out.parents:
        raise ValueError("Output must not be inside the tracked repository")
    out.mkdir(parents=True, exist_ok=True)
    sha = git("rev-parse", "HEAD")
    when = git("show", "-s", "--format=%cI", "HEAD")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    paths = sorted(p for p in git("ls-files", "-z").split("\0") if p)
    if not paths:
        raise RuntimeError("No tracked repository files")
    listed = []
    excluded = []
    for name in paths:
        full = ROOT / name
        if not full.is_file():
            raise RuntimeError("Tracked file missing: " + name)
        if name.lower().endswith(".pdf"):
            excluded.append(name)
            continue
        if name.endswith((".zip", ".tar", ".tgz")):
            excluded.append(name)
            continue
        listed.append((name, full.read_bytes()))
    # This is intended as a public source and metadata archive, not a
    # redistribution of the 51 separately licensed original PDFs.
    if len([p for p in excluded if p.lower().endswith(".pdf")]) != 51:
        raise RuntimeError("Unexpected PDF inventory; stop and review")
    required = ["README.md", "NOTICE", "LICENSE", "CITATION.cff", "VERSION",
                "RIGHTSHOLDER-NOTICE.md", "docs/ZENODO-DEPOSIT-PREPARATION.md",
                "knowledge/methodology/PDF-ATTRIBUTIONS.md"]
    manifest_index = {n: digest(data) for n, data in listed}
    if not all(p in manifest_index for p in required):
        raise RuntimeError("Mandatory legal or provenance file missing")
    original_notice = next(b for n, b in listed if n == "RIGHTSHOLDER-NOTICE.md")
    if b"rebsonm@gmail.com" not in original_notice or b"Apache-2.0" not in original_notice:
        raise RuntimeError("Rights-holder notice incomplete")
    meta = {
        "archive_kind": "REVIEWABLE_PUBLIC_SOURCE_NOT_INSTALLABLE_SKILL_NOT_PUBLISHED_ZENODO",
        "source_repository": "https://github.com/rebsonm/MeuArtigoSkill",
        "source_commit_sha": sha,
        "source_commit_date": when,
        "declared_version_file": version,
        "official_skill_release_unchanged": "v1.0.0-rc.1",
        "files_included": len(listed),
        "third_party_pdf_files_excluded": 51,
        "pdf_binaries_included": 0,
        "sha256_of_each_included_file": manifest_index,
        "author_rights_contact": "rebsonm@gmail.com",
        "existing_record_doi_as_cited": "10.5281/zenodo.24397699",
        "further_zenodo_publication_performed": False,
        "scientific_gates_approved_by_snapshot": 0,
        "exclusion_note": "All 51 third-party scholarly PDF binaries are excluded; see rights register for external original sources.",
    }
    basename = "MeuArtigo-zenodo-source-review-" + sha[:12] + ".zip"
    archive = out / basename
    with zipfile.ZipFile(archive, "w") as zf:
        for path, data in listed:
            as_zip(zf, path, data)
        as_zip(zf, "_ZENODO_SOURCE_SNAPSHOT.json",
               (json.dumps(meta, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))
    with zipfile.ZipFile(archive) as zf:
        names = zf.namelist()
        if zf.testzip() is not None:
            raise RuntimeError("ZIP self-test failed")
        if any(p.lower().endswith(".pdf") for p in names):
            raise RuntimeError("A scholarly PDF leaked into the source ZIP")
        if len(names) != len(listed) + 1:
            raise RuntimeError("ZIP file count mismatch")
        saved = json.loads(zf.read("_ZENODO_SOURCE_SNAPSHOT.json"))
        if saved["source_commit_sha"] != sha:
            raise RuntimeError("Archive metadata does not match HEAD")
    checksum = digest(archive.read_bytes())
    (out / "SHA256SUMS-zenodo-review.txt").write_text(
        f"{checksum}  {basename}\n", encoding="utf-8")
    (out / "ZENODO-REVIEW-COPY-MANIFEST.json").write_text(
        json.dumps({k: v for k, v in meta.items() if k != "sha256_of_each_included_file"} |
                   {"archive_file": basename, "archive_sha256": checksum},
                   ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8")
    (out / "READ-FIRST-ZENODO.txt").write_text(
        "This is a public source snapshot for review before a future Zenodo version.\n"
        "It is NOT a versioned installable Meu Artigo Skill ZIP, a GitHub release,\n"
        "a published Zenodo record, or independent validation of research methodology.\n"
        "The 51 third-party scholarly PDFs are NOT included. Confirm that the record\n"
        "belongs to you and inspect the DOI/version relationship before depositing.\n"
        f"Git commit: {sha}\nVersion-file value (not a new release): {version}\n"
        f"Rights-holder email: rebsonm@gmail.com\nZIP SHA-256: {checksum}\n",
        encoding="utf-8")
    print(json.dumps({
        "archive": str(archive), "archive_sha256": checksum,
        "git_commit": sha, "files": len(listed),
        "third_party_pdfs_excluded": 51,
        "zenodo_deposit_published": False
    }, indent=2))

if __name__ == "__main__":
    main()
