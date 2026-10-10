#!/usr/bin/env python3
"""Fail-closed release-documentation preflight for manual GitHub publication.

This does NOT publish software and does NOT certify any scientific result.
Run only during an explicitly authorized, manual release on main. Normal
development PRs and unpublished source candidates are allowed to omit
`date-released` until real publication preparation.
"""
from __future__ import annotations

import argparse
from datetime import date, timezone, datetime
from pathlib import Path
import re

from version_info import ROOT, read_version, release_notes_path


def audit_release_metadata(root: Path, *, expected_date: str | None = None) -> list[str]:
    root = Path(root)
    v = read_version(root)
    errors: list[str] = []
    text = (root / "CITATION.cff").read_text(encoding="utf-8")
    matches = re.findall(r'^date-released:\s*"(\d{4}-\d{2}-\d{2})"\s*$',
                         text, flags=re.M)
    if len(matches) != 1:
        errors.append("CITATION_DATE_MISSING_OR_AMBIGUOUS")
    else:
        release_date = matches[0]
        try:
            date.fromisoformat(release_date)
        except ValueError:
            errors.append("CITATION_DATE_INVALID")
        if expected_date is not None and release_date != expected_date:
            errors.append("CITATION_DATE_DOES_NOT_MATCH_PUBLICATION_DATE")
        changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
        if f"## {v} — {release_date}" not in changelog:
            errors.append("CHANGELOG_PUBLICATION_DATE_INCONSISTENT")
    notes = release_notes_path(root).read_text(encoding="utf-8")
    if re.search(r"\b(?:RELEASE CANDIDATE ONLY|NOT PUBLISHED|UNRELEASED RELEASE CANDIDATE)\b",
                 notes, flags=re.I):
        errors.append("RELEASE_NOTES_STILL_DESCRIBE_UNPUBLISHED_CANDIDATE")
    readme = (root / "README.md").read_text(encoding="utf-8")
    url = f"https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v{v}"
    if url not in readme:
        errors.append("README_HAS_NO_EXACT_NEW_RELEASE_LINK")
    if re.search(rf"\bunpublished\s+v?{re.escape(v)}\b",
                 readme, flags=re.I):
        errors.append("README_STILL_CALLS_THIS_VERSION_UNPUBLISHED")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=str(ROOT))
    parser.add_argument("--require-today", action="store_true",
                        help="Require CITATION date to match UTC day of publication")
    args = parser.parse_args(argv)
    when = datetime.now(timezone.utc).date().isoformat() if args.require_today else None
    try:
        errors = audit_release_metadata(Path(args.repo), expected_date=when)
    except (OSError, ValueError):
        print("release_metadata=BLOCKED; cannot read verified source")
        return 2
    print("release_metadata=" + ("BLOCKED" if errors else "READY_FOR_MANUAL_REVIEW"))
    for code in errors:
        print("  " + code)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
