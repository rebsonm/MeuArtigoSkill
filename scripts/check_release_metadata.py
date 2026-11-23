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



def audit_candidate_metadata(root: Path) -> list[str]:
    """Check source-only RC honesty without requiring a release date or tag."""
    root = Path(root)
    errors: list[str] = []
    try:
        version = read_version(root)
        if not re.fullmatch(r"\d+\.\d+\.\d+-rc\.[1-9]\d*", version):
            return ["SOURCE_VERSION_IS_NOT_RELEASE_CANDIDATE"]
        citation = (root / "CITATION.cff").read_text(encoding="utf-8")
        changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
        readme = (root / "README.md").read_text(encoding="utf-8")
        notes = release_notes_path(root).read_text(encoding="utf-8")
        official = (root / "OFFICIAL_SKILL_RELEASE").read_text(encoding="utf-8").strip()
    except (OSError, ValueError, UnicodeError):
        return ["SOURCE_CANDIDATE_DOCUMENTS_NOT_AVAILABLE"]
    if f'version: "{version}"' not in citation:
        errors.append("CITATION_VERSION_INCONSISTENT")
    if re.search(r"(?m)^date-released\s*:", citation):
        errors.append("UNPUBLISHED_CANDIDATE_MUST_NOT_CLAIM_RELEASE_DATE")
    if f"## {version} — UNRELEASED" not in changelog:
        errors.append("CHANGELOG_CANDIDATE_HEADING_MISSING")
    if f"**Current version:** `{version}`" not in readme:
        errors.append("README_SOURCE_VERSION_INCONSISTENT")
    if not ("unpublished release candidate" in readme.lower() and
            "not published" in notes.lower() and
            "not a stable release" in notes.lower()):
        errors.append("CANDIDATE_NOT_CLEARLY_UNPUBLISHED")
    # Unpublished source candidates must preserve an older actual release pointer.
    def order(v: str):
        m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:-(beta|rc)\.(\d+))?", v)
        if not m:
            return None
        return (int(m[1]), int(m[2]), int(m[3]),
                {"beta": 0, "rc": 1, None: 2}[m[4]],
                int(m[5]) if m[5] else 0)
    official_order = order(official)
    candidate_order = order(version)
    if official_order is None or candidate_order is None or not official_order < candidate_order:
        errors.append("PUBLISHED_RECOMMENDATION_MUST_REMAIN_PRIOR_VERSION")
    from check_github_zenodo_parity import preflight as parity_preflight
    errors.extend(parity_preflight(root, "v" + version))
    if f"/releases/tag/v{version}" in readme:
        errors.append("UNPUBLISHED_RC_MUST_NOT_HAVE_RELEASE_LINK")
    return errors



def audit_published_source_metadata(root: Path) -> list[str]:
    """Check source metadata AFTER an actual release was verified externally.

    This is an offline consistency check: it must never pretend to query GitHub
    or prove installation in an assistant host.
    """
    root = Path(root)
    errors = audit_release_metadata(root)
    version = read_version(root)
    official = (root / "OFFICIAL_SKILL_RELEASE").read_text(encoding="utf-8").strip()
    citation = (root / "CITATION.cff").read_text(encoding="utf-8")
    readme = (root / "README.md").read_text(encoding="utf-8")
    if official != version:
        errors.append("PUBLISHED_RECOMMENDATION_DIFFERS_FROM_SOURCE_VERSION")
    if f'version: "{version}"' not in citation:
        errors.append("CITATION_VERSION_INCONSISTENT")
    if f"**Current version:** `{version}`" not in readme:
        errors.append("README_SOURCE_VERSION_INCONSISTENT")
    if "published" not in readme.lower() or "experimental" not in readme.lower():
        errors.append("PUBLISHED_PRERELEASE_NOT_CLEARLY_DESCRIBED")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=str(ROOT))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--require-today", action="store_true",
                      help="Require CITATION date to match UTC day of publication")
    mode.add_argument("--candidate", action="store_true",
                      help="Audit unpublished RC metadata without a publication date")
    mode.add_argument("--published-source", action="store_true",
                      help="Audit metadata of an already published release without checking GitHub")
    args = parser.parse_args(argv)
    when = datetime.now(timezone.utc).date().isoformat() if args.require_today else None
    try:
        errors = (audit_candidate_metadata(Path(args.repo)) if args.candidate else
                  audit_published_source_metadata(Path(args.repo)) if args.published_source else
                  audit_release_metadata(Path(args.repo), expected_date=when))
    except (OSError, ValueError):
        print("release_metadata=BLOCKED; cannot read verified source")
        return 2
    ready = ("READY_FOR_CANDIDATE_TESTING" if args.candidate else
             "PUBLISHED_SOURCE_METADATA_CONSISTENT" if args.published_source else
             "READY_FOR_MANUAL_REVIEW")
    print("release_metadata=" + ("BLOCKED" if errors else ready))
    for code in errors:
        print("  " + code)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
