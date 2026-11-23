#!/usr/bin/env python3
"""Fail closed on mismatched GitHub/Zenodo software release identities.

This is an offline publication gate. It does not fetch records, publish a
GitHub release, modify Zenodo records, authenticate evidence or approve science.
Preflight checks a tag against the exact checked-out source; post-archive
requires separately observed, source-pinned evidence from BOTH providers.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+-rc\.[1-9][0-9]*$")
SHA_RE = re.compile(r"^[a-f0-9]{40}$")
HASH_RE = re.compile(r"^[a-f0-9]{64}$")
DOI_RE = re.compile(r"^10\.5281/zenodo\.[1-9][0-9]*$")


def _versions(citation: str) -> tuple[str | None, str | None]:
    """Parse only the two existing CFF scalar version fields; no YAML eval."""
    root = re.findall(r'^version:\s*["\']?([^"\'\s]+)', citation, flags=re.M)
    pref = re.search(r"(?m)^preferred-citation:\s*$", citation)
    tail = citation[pref.end():] if pref else ""
    preferred = re.findall(r'^  version:\s*["\']?([^"\'\s]+)', tail, flags=re.M)
    return (root[0] if len(root) == 1 else None,
            preferred[0] if len(preferred) == 1 else None if preferred else "")


def preflight(root: Path, tag: str) -> list[str]:
    """Inspect source metadata at the exact tag candidate checkout."""
    errors = []
    try:
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
        root_cff, preferred_cff = _versions((root / "CITATION.cff").read_text(encoding="utf-8"))
    except OSError:
        return ["SOURCE_IDENTITY_UNAVAILABLE"]
    if not VERSION_RE.fullmatch(version):
        errors.append("SOURCE_IS_NOT_VALID_RC")
    if tag != "v" + version:
        errors.append("GITHUB_TAG_DIFFERS_FROM_SOURCE_VERSION")
    if root_cff != version:
        errors.append("CITATION_TOP_LEVEL_VERSION_MISMATCH")
    if preferred_cff not in ("", version):
        errors.append("CITATION_PREFERRED_VERSION_MISMATCH")
    return errors


def reconcile(github: dict, zenodo: dict) -> list[str]:
    """Fail closed unless independently observed archive identities agree.

    Inputs must come from observed GitHub release/tag evidence and a Zenodo
    record plus a verified archived-source manifest. Merely writing a JSON
    claim here does not independently establish that evidence.
    """
    errors = []
    tag = github.get("tag")
    version = tag[1:] if isinstance(tag, str) and tag.startswith("v") else ""
    if not VERSION_RE.fullmatch(version):
        errors.append("GITHUB_RELEASE_TAG_INVALID")
    if github.get("version") != version:
        errors.append("GITHUB_RELEASE_VERSION_MISMATCH")
    if zenodo.get("version") != version:
        errors.append("ZENODO_VERSION_DIFFERS_FROM_GITHUB_TAG")
    gsha, zsha = github.get("source_commit"), zenodo.get("source_commit")
    if not isinstance(gsha, str) or not SHA_RE.fullmatch(gsha):
        errors.append("GITHUB_TAG_SOURCE_SHA_NOT_VERIFIED")
    if not isinstance(zsha, str) or not SHA_RE.fullmatch(zsha):
        errors.append("ZENODO_ARCHIVED_SOURCE_SHA_NOT_VERIFIED")
    if (isinstance(gsha, str) and SHA_RE.fullmatch(gsha) and
            isinstance(zsha, str) and SHA_RE.fullmatch(zsha) and gsha != zsha):
        errors.append("ARCHIVED_SOURCE_COMMIT_DIFFERS")
    doi = zenodo.get("version_doi")
    if not isinstance(doi, str) or not DOI_RE.fullmatch(doi):
        errors.append("ZENODO_VERSION_SPECIFIC_DOI_NOT_VERIFIED")
    # An installable Skill ZIP and Zenodo's GitHub source archive are NOT
    # necessarily byte-for-byte equivalent. Check hashes only for the
    # same declared artifact kind; source SHA must match in every case.
    gkind, zkind = github.get("archive_kind"), zenodo.get("archive_kind")
    if gkind and zkind and gkind == zkind:
        gh, zh = github.get("archive_sha256"), zenodo.get("archive_sha256")
        if not all(isinstance(x, str) and HASH_RE.fullmatch(x) for x in (gh, zh)):
            errors.append("SAME_KIND_ARCHIVE_HASH_NOT_VERIFIED")
        elif gh != zh:
            errors.append("SAME_KIND_ARCHIVE_HASH_MISMATCH")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest="stage", required=True)
    pre = sub.add_parser("preflight")
    pre.add_argument("--tag", required=True)
    post = sub.add_parser("reconcile")
    post.add_argument("--github-evidence", type=Path, required=True)
    post.add_argument("--zenodo-evidence", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.stage == "preflight":
            errors = preflight(args.root, args.tag)
        else:
            github = json.loads(args.github_evidence.read_text(encoding="utf-8"))
            zenodo = json.loads(args.zenodo_evidence.read_text(encoding="utf-8"))
            if not isinstance(github, dict) or not isinstance(zenodo, dict):
                raise ValueError("Evidence must consist of objects")
            errors = reconcile(github, zenodo)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        errors = ["EXTERNAL_EVIDENCE_UNAVAILABLE_OR_INVALID"]
    print("github_zenodo_parity=" + ("BLOCKED" if errors else
          "DOCUMENTARY_CHECK_PASSED_NOT_INDEPENDENTLY_AUTHENTICATED"))
    for issue in errors:
        print("  " + issue)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
