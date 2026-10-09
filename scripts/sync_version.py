#!/usr/bin/env python3
"""Synchronize *derived* public version metadata from the canonical VERSION file.

The contributor authors real release notes first; no source data, empirical
results or release commentary is synthesized. The script never publishes a
release, uploads materials or changes a Git tag.
"""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re

from version_info import ROOT, read_version, release_notes_path


def replace_once(pattern: str, new: str, text: str, label: str) -> str:
    updated, count = re.subn(pattern, lambda _: new, text, count=1, flags=re.M)
    if count != 1:
        raise ValueError(f"Cannot find the expected {label} declaration")
    return updated


def sync(root: Path, release_date: str) -> list[str]:
    root = Path(root)
    version = read_version(root)
    try:
        release_day = date.fromisoformat(release_date)
    except ValueError as exc:
        raise ValueError("Use ISO release date YYYY-MM-DD") from exc
    if release_day.isoformat() != release_date:
        raise ValueError("Use exact ISO release date YYYY-MM-DD")
    notes = release_notes_path(root)
    if not notes.is_file() or not notes.read_text(encoding="utf-8").strip():
        raise ValueError(f"Author real release notes before syncing: {notes.name}")
    if version not in notes.read_text(encoding="utf-8"):
        raise ValueError("Release notes must identify the matching VERSION")

    paths = {
        "README.md": root/"README.md",
        "CITATION.cff": root/"CITATION.cff",
        "CHANGELOG.md": root/"CHANGELOG.md",
    }
    contents = {name: p.read_text(encoding="utf-8") for name,p in paths.items()}
    readme = replace_once(r"^\*\*Versão atual:\*\* \`[^\`]+\`",
                          f"**Versão atual:** \`{version}\`",
                          contents["README.md"], "README version")
    citation = replace_once(r'^version:\s*"[^"]+"',
                             f'version: "{version}"',
                             contents["CITATION.cff"], "CITATION version")
    citation = replace_once(r'^date-released:\s*"[^"]+"',
                             f'date-released: "{release_date}"',
                             citation, "CITATION release date")

    changelog = contents["CHANGELOG.md"]
    header = f"## {version} — {release_date}"
    if header not in changelog:
        m = re.search(r"(?m)^## Unreleased\s*\n", changelog)
        if not m:
            raise ValueError("CHANGELOG is missing Unreleased section")
        n = re.search(r"(?m)^## ", changelog[m.end():])
        if n is None:
            raise ValueError("CHANGELOG must retain at least one past version")
        boundary = m.end() + n.start()
        release_content = changelog[m.end():boundary].strip()
        if release_content.startswith("Nenhuma alteração adicional registrada"):
            release_content = ""
        if not release_content:
            release_content = f"- Consulte [as notas da versão](docs/{notes.name})."
        changelog = (
            changelog[:m.start()] +
            f"## Unreleased\n\nNenhuma alteração adicional registrada desde \`{version}\`.\n\n" +
            f"{header}\n\n{release_content}\n\n" + changelog[boundary:]
        )
    # First validate all edits, *then* write. Rerunning is safe.
    changes = []
    for name, updated in (
        ("README.md",readme), ("CITATION.cff",citation), ("CHANGELOG.md",changelog)
    ):
        if updated != contents[name]:
            changes.append(name)
            paths[name].write_text(updated,encoding="utf-8")
    return changes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=str(ROOT))
    ap.add_argument("--date", required=True, help="Real release date in YYYY-MM-DD format")
    args = ap.parse_args(argv)
    try:
        changed = sync(Path(args.repo), args.date)
    except (OSError, ValueError) as exc:
        ap.error(str(exc))
    print("derived_version=" + read_version(Path(args.repo)))
    print("updated=" + (", ".join(changed) if changed else "(already in sync)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
