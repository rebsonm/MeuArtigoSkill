#!/usr/bin/env python3
"""Build and verify a deterministic, installable public-beta Skill ZIP.

The allowlist protects against shipping private corpora, project data, caches
and third-party articles. A passing package check is not scientific validation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
from version_info import read_version

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = ("SKILL.md", "README.md", "CHANGELOG.md", "VERSION",
              "CITATION.cff", "LICENSE", "NOTICE", "CONTRIBUTING.md", "SECURITY.md")
DIR_TYPES = {
    "agents": {".yaml", ".yml"},
    "assets": {".svg", ".png"},
    "references": {".md"},
    "scripts": {".py"},
    "docs": {".md"},
    "benchmarks": {".json"},
}
MANIFEST = "BUNDLE_MANIFEST.json"
FIXED_DATE = (2026, 10, 9, 0, 0, 0)
REPOSITORY = "https://github.com/rebsonm/MeuArtigoSkill"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def list_sources(root: Path) -> list[Path]:
    found = []
    for filename in ROOT_FILES:
        path = root / filename
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"Required public package file unavailable: {filename}")
        found.append(path)
    for dirname, suffixes in DIR_TYPES.items():
        folder = root / dirname
        if not folder.is_dir() or folder.is_symlink():
            raise ValueError(f"Package directory missing or linked: {dirname}")
        for path in sorted(folder.rglob("*")):
            # Ignore only generated interpreter caches, never unrecognized data.
            if "__pycache__" in path.relative_to(root).parts or path.suffix.lower() in {".pyc",".pyo"}:
                continue
            if path.is_symlink():
                raise ValueError(f"Symlink cannot enter public bundle: {path}")
            if path.is_file():
                if path.suffix.lower() not in suffixes:
                    raise ValueError(f"Unrecognized file could expose private material: {path}")
                found.append(path)
    return sorted(found, key=lambda p: p.relative_to(root).as_posix())



def source_provenance(root: Path) -> dict[str, str | None]:
    """Attest a clean, exact git checkout when demonstrable; otherwise UNKNOWN."""
    unknown = {"build_source_commit": None, "source_verification": "UNVERIFIED"}
    if not (root / ".git").exists():
        return unknown

    def read(*args):
        p = subprocess.run(["git", "-C", str(root), *args],
                           capture_output=True, text=True, timeout=5, check=False)
        return p.stdout.strip() if p.returncode == 0 else None

    try:
        head = read("rev-parse", "--verify", "HEAD")
        dirty = read("status", "--porcelain", "--untracked-files=no")
        remote = read("config", "--get", "remote.origin.url")
    except (OSError, subprocess.TimeoutExpired):
        return unknown
    if not head or not re.fullmatch(r"[0-9a-f]{40}", head):
        return unknown
    # Whitelist the exact expected remote; do not leak credential-bearing URLs.
    permitted = {REPOSITORY, REPOSITORY + ".git",
                 "git@github.com:rebsonm/MeuArtigoSkill.git"}
    if dirty is None or dirty != "" or remote not in permitted:
        return unknown
    return {"build_source_commit": head, "source_verification": "CLEAN_GIT_CHECKOUT"}

def package(root: Path, destination: Path) -> dict:
    root = root.resolve()
    files = list_sources(root)
    version = read_version(root)
    if not version:
        raise ValueError("Missing package version")
    expected = f"MeuArtigoSkill-v{version}.zip"
    if destination.name != expected:
        raise ValueError(f"Unexpected package filename; expected {expected}")
    provenance = source_provenance(root)
    manifest = {"schema_version": 2, "version": version,
                "entrypoint": "SKILL.md", "license": "Apache-2.0",
                "scientific_quality_validated": False,
                "repository_origin_claim": REPOSITORY,
                "build_source_commit": provenance["build_source_commit"],
                "source_verification": provenance["source_verification"],
                "files": {p.relative_to(root).as_posix(): sha256(p.read_bytes()) for p in files}}
    if manifest["files"].get("LICENSE") != sha256((root / "LICENSE").read_bytes()):
        raise ValueError("License checksum is inconsistent")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_DEFLATED, compresslevel=9) as zipf:
        for file in files:
            name = file.relative_to(root).as_posix()
            item = ZipInfo(name, FIXED_DATE)
            item.compress_type = ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            zipf.writestr(item, file.read_bytes(), compress_type=ZIP_DEFLATED,
                          compresslevel=9)
        item = ZipInfo(MANIFEST, FIXED_DATE)
        item.compress_type = ZIP_DEFLATED
        item.external_attr = 0o100644 << 16
        zipf.writestr(item, json.dumps(manifest, ensure_ascii=False,
                                      sort_keys=True, indent=2).encode("utf-8") + b"\n")
    verify_package(destination)
    checksums = destination.parent / "SHA256SUMS.txt"
    package_digest = sha256(destination.read_bytes())
    checksums.write_text(f"{package_digest}  {destination.name}\n", encoding="utf-8")
    # The package digest must be outside its ZIP to avoid a self-referential hash.
    (destination.parent / "BUNDLE_BUILD_RECEIPT.json").write_text(
        json.dumps({"schema_version": 1, "package_name": destination.name,
                    "package_sha256": package_digest, "version": version,
                    "repository_origin_claim": REPOSITORY,
                    "build_source_commit": provenance["build_source_commit"],
                    "source_verification": provenance["source_verification"],
                    "distribution_type": "SKILL_ZIP_NOT_INSTALLED_PLUGIN",
                    "scientific_quality_validated": False},
                   sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return manifest


def verify_package(path: Path) -> dict:
    with ZipFile(path, "r") as z:
        names = z.namelist()
        if len(names) != len(set(names)) or MANIFEST not in names:
            raise ValueError("Duplicate members or missing manifest")
        if any(Path(name).is_absolute() or ".." in Path(name).parts or
               name.startswith(".") or "\\" in name for name in names):
            raise ValueError("Unsafe ZIP member path")
        manifest = json.loads(z.read(MANIFEST))
        if manifest.get("entrypoint") != "SKILL.md" or manifest.get("license") != "Apache-2.0":
            raise ValueError("Wrong bundle entrypoint or license")
        items = manifest.get("files") or {}
        if set(items) != set(names) - {MANIFEST}:
            raise ValueError("Manifest and packaged contents diverge")
        for name, expected in items.items():
            if sha256(z.read(name)) != expected:
                raise ValueError(f"Package member checksum mismatch: {name}")
        if not z.read("LICENSE").lstrip().startswith(b"Apache License"):
            raise ValueError("Published package missing Apache-2.0 license")
        if not z.read("NOTICE").startswith(b"Meu Artigo"):
            raise ValueError("Published package missing author attribution NOTICE")
        return manifest


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", default=str(ROOT))
    p.add_argument("--verify", default="")
    p.add_argument("--out", default="")
    args = p.parse_args(argv)
    root = Path(args.repo)
    if args.verify:
        result = verify_package(Path(args.verify))
    else:
        version = read_version(root)
        path = Path(args.out) if args.out else root / "dist" / f"MeuArtigoSkill-v{version}.zip"
        result = package(root, path)
        print(f"bundle={path}")
        print(f"checksum_file={path.parent / 'SHA256SUMS.txt'}")
    print(f"version={result['version']}")
    print(f"members={len(result['files'])}")
    print("scientific_quality_validated=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
