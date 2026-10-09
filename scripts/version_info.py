#!/usr/bin/env python3
"""VERSION is the only editable source of the current release identifier.

Historical release notes are intentionally retained. This module does not
claim that the current main commit has been released; publishing is explicit.
"""
from __future__ import annotations

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


if __name__ == "__main__":
    print(read_version())
