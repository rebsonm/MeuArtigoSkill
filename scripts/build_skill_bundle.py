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
from bundle_dependency_audit import audit as audit_bundle

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = ("SKILL.md", "VERSION", "CITATION.cff", "LICENSE", "NOTICE", "SECURITY.md")
DIR_TYPES = {
    "agents": {".yaml", ".yml"},
    "assets": {".svg", ".png", ".html"},
    "references": {".md"},
    "scripts": {".py"},
    "docs": {".md"},
}
# Researcher installation contains operational science files only.
# Development, distribution and release checks remain in the source repository.
EXCLUDED_SCRIPT_NAMES = frozenset({
    "audit_public_docs.py", "audit_source_language.py",
    "check_documentation_links.py", "check_install_package.py",
    "check_release_metadata.py", "release_audit.py",
    "smoke_test_provenance.py", "sync_version.py",
    "build_skill_bundle.py", "quality_benchmark.py",
    "mcp_preview_projection.py",
    "bundle_dependency_audit.py",
})
EXCLUDED_DOC_NAMES = frozenset({
    "GUIA-DE-RELEASES.md", "IMPLANTACAO-BETA.md",
    "PROTOCOLO-BETA-USUARIOS.md", "ENGLISH-SOURCE-MIGRATION.md",
    "RELATORIO-AUDITORIA-FINAL-BETA4.md", "ROTEIRO-HOMOLOGACAO-CONSOLIDADA.md",
})
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
                if dirname == "scripts" and path.name in EXCLUDED_SCRIPT_NAMES:
                    continue
                if dirname == "docs" and (path.name in EXCLUDED_DOC_NAMES or
                                          path.name.startswith("NOTAS-DA-VERSAO-")):
                    continue
                if dirname=="assets" and path.suffix.lower()==".html" and path.name!="research_workspace.html":
                    raise ValueError(f"Only the exact reviewed UI template is permitted: {path}")
                if path.suffix.lower() not in suffixes:
                    raise ValueError(f"Unrecognized file could expose private material: {path}")
                found.append(path)
    return sorted(found, key=lambda p: p.relative_to(root).as_posix())



def source_provenance(root: Path, packaged_files: list[Path] | None = None) -> dict[str, str | None]:
    """Attest a tracked, unchanged Git origin for *every bundled source*.

    A clean tracked tree alone cannot attest untracked files added to the
    allowlisted ZIP. Ignore out-of-package build artifacts (such as dist/)
    while refusing to associate a commit with an untracked included file.
    """
    unknown = {"build_source_commit": None, "source_verification": "UNVERIFIED"}
    if not (root / ".git").exists():
        return unknown

    def read(*args):
        p = subprocess.run(["git", "-C", str(root), *args],
                           capture_output=True, text=True, timeout=5, check=False)
        return p.stdout.strip() if p.returncode == 0 else None

    try:
        selected = packaged_files if packaged_files is not None else list_sources(root)
        relative = [file.relative_to(root).as_posix() for file in selected]
        if not relative:
            return unknown
        head = read("rev-parse", "--verify", "HEAD")
        # --error-unmatch fails if ANY included file has never been tracked.
        # Test every exact filename rather than trusting git status on the
        # entire source tree, which may ignore untracked allowed inputs.
        tracked = read("ls-files", "--error-unmatch", "--", *relative)
        dirty = read("status", "--porcelain", "--untracked-files=all", "--", *relative)
        remote = read("config", "--get", "remote.origin.url")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return unknown
    if not head or not re.fullmatch(r"[0-9a-f]{40}", head):
        return unknown
    # Whitelist the exact expected remote; do not leak credential-bearing URLs.
    permitted = {REPOSITORY, REPOSITORY + ".git",
                 "git@github.com:rebsonm/MeuArtigoSkill.git"}
    if tracked is None or dirty is None or dirty != "" or remote not in permitted:
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
    # The public archive must be runnable as a standalone Skill. Unlike a
    # source checkout it must not reference a missing local helper or entry
    # navigation document.
    all_modules = {p.stem for p in (root / "scripts").glob("*.py") if p.is_file()}
    payload = {p.relative_to(root).as_posix(): p.read_bytes() for p in files}
    closure = audit_bundle(payload, local_source_modules=all_modules)
    if closure["errors"]:
        raise ValueError("BUNDLE_DEPENDENCY_CLOSURE_FAILED: " + "; ".join(closure["errors"][:8]))
    provenance = source_provenance(root, files)
    manifest = {"schema_version": 2, "version": version,
                "entrypoint": "SKILL.md", "license": "Apache-2.0",
                "scientific_quality_validated": False,
                "installed_dependency_closure_checked": True,
                "repository_origin_claim": REPOSITORY,
                "build_source_commit": provenance["build_source_commit"],
                "source_verification": provenance["source_verification"],
                "files": {name: sha256(data) for name, data in payload.items()}}
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
                    "distribution_type": "SKILL_ZIP",
                    "scientific_quality_validated": False},
                   sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return manifest


def verify_package(path: Path) -> dict:
    with ZipFile(path, "r") as z:
        info = z.infolist()
        names = [item.filename for item in info]
        if len(names) != len(set(names)) or MANIFEST not in names:
            raise ValueError("Duplicate members or missing manifest")
        if (len(info) > 3000 or sum(item.file_size for item in info) > 100 * 1024 * 1024
                or any(item.is_dir() or item.file_size < 0
                       or (item.external_attr >> 16) & 0o170000 == 0o120000
                       or item.flag_bits & 1 for item in info)):
            raise ValueError("Unsafe, encrypted or oversized ZIP contents")
        if any(Path(name).is_absolute() or ".." in Path(name).parts or
               name.startswith(".") or "\\" in name for name in names):
            raise ValueError("Unsafe ZIP member path")
        manifest = json.loads(z.read(MANIFEST))
        if manifest.get("entrypoint") != "SKILL.md" or manifest.get("license") != "Apache-2.0":
            raise ValueError("Wrong bundle entrypoint or license")
        items = manifest.get("files") or {}
        if set(items) != set(names) - {MANIFEST}:
            raise ValueError("Manifest and packaged contents diverge")
        payload = {}
        for name, expected in items.items():
            if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
                raise ValueError("Malformed package member checksum")
            data = z.read(name)
            if sha256(data) != expected:
                raise ValueError(f"Package member checksum mismatch: {name}")
            payload[name] = data
        # A ZIP manifest must not certify files that are absent, even if the
        # hashes of all *present* objects match. Check installable references.
        closure = audit_bundle(payload)
        if closure["errors"]:
            raise ValueError("Broken Skill bundle closure: " + "; ".join(closure["errors"][:8]))
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
