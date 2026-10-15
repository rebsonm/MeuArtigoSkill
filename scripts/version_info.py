#!/usr/bin/env python3
"""VERSION is the only editable source of the current release identifier.

Historical release notes are intentionally retained. This module does not
claim that the current main commit has been released; publishing is explicit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_PATTERN = re.compile(r"\d+\.\d+\.\d+(?:-beta\.\d+)?\Z")


def read_version(root: Path = ROOT) -> str:
    version_file = Path(root) / "VERSION"
    if not version_file.is_file():
        raise ValueError("VERSION is missing")
    version = version_file.read_text(encoding="utf-8").strip()
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError(f"Invalid release version in VERSION: {version!r}")
    return version


def release_notes_path(root: Path = ROOT) -> Path:
    return Path(root) / "docs" / f"NOTAS-DA-VERSAO-{read_version(root)}.md"


def release_zip_name(root: Path = ROOT) -> str:
    return f"MeuArtigoSkill-v{read_version(root)}.zip"


def diagnostic(root: Path = ROOT) -> dict:
    """Describe only locally inspected Skill files, not the active host installation."""
    root = Path(root)
    report = {
        "schema": "MEU_ARTIGO_SKILL_DIAGNOSTIC_V1",
        "source_version": None,
        "bundle_manifest_available": False,
        "bundle_content_status": "NOT_CHECKED",
        "host_installed_skill_verified": False,
        "public_release_verified": False,
        "observed_build_source_commit": None,
        "limitations": [
            "This local inspection cannot prove which Skill a host currently loaded.",
            "A GitHub release and a repository VERSION are not proof of active installation.",
        ],
    }
    try:
        report["source_version"] = read_version(root)
    except (OSError, ValueError):
        report["bundle_content_status"] = "VERSION_MISSING_OR_INVALID"
        return report
    manifest = root / "BUNDLE_MANIFEST.json"
    if not manifest.is_file() or manifest.is_symlink():
        report["bundle_content_status"] = "SOURCE_VERSION_ONLY"
        return report
    report["bundle_manifest_available"] = True
    try:
        obj = json.loads(manifest.read_text(encoding="utf-8"))
        files = obj["files"]
        if (not isinstance(obj, dict) or not isinstance(files, dict)
                or not files or obj.get("version") != report["source_version"]):
            raise ValueError("Manifest/version mismatch")
        for raw_path, expected in files.items():
            if not isinstance(raw_path, str) or not raw_path or raw_path.startswith("/"):
                raise ValueError("Unsafe path")
            p = Path(raw_path)
            if any(part in (".", "..", "") for part in p.parts) or p.is_absolute():
                raise ValueError("Unsafe manifest member")
            if not isinstance(expected, str) or not re.fullmatch(r"[a-f0-9]{64}", expected):
                raise ValueError("Invalid digest")
            target = root / p
            if not target.is_file() or target.is_symlink():
                raise ValueError("Missing or linked bundle file")
            if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                raise ValueError("Bundle file digest mismatch")
        report["bundle_content_status"] = "LOCAL_BUNDLE_FILES_MATCH_MANIFEST"
        report["observed_build_source_commit"] = obj.get("build_source_commit")
    except (ValueError, KeyError, TypeError, OSError, UnicodeError, json.JSONDecodeError):
        report["bundle_content_status"] = "BUNDLE_MANIFEST_INVALID_OR_FILES_CHANGED"
    return report


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--diagnose", action="store_true")
    p.add_argument("--root", type=Path, default=ROOT)
    args = p.parse_args()
    if args.diagnose:
        print(json.dumps(diagnostic(args.root), ensure_ascii=False, indent=2))
    else:
        print(read_version(args.root))
