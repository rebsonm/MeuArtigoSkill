#!/usr/bin/env python3
"""Fail-closed public prose scanner for accidental private provenance/secrets.

This is a static *regression guard*, not a claim of exhaustive information
security review. It does not inspect Git history or private user workspaces.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# These are development/private-collection identifiers never intended for
# researcher-facing README, operational explanations or release notes.
PRIVATE_REFERENCE_PATTERNS = {
    "private collection name": re.compile(r"\bPPGA\b|ppga-methodological", re.I),
    "private remediation ticket": re.compile(r"\bRT-\d{2}\b|\bP-\d{2}\b|\bT-\d{2}\b", re.I),
}
# Precise secret signatures deliberately avoid broad "token" prose, which is
# legitimate in docs explaining secure workflows. No matches are printed.
SECRET_PATTERNS = {
    "private key block": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{25,})\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{32,}\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "Google API key": re.compile(r"\bAIza[A-Za-z0-9_-]{35}\b"),
}


def public_documents(root: Path) -> list[Path]:
    root = Path(root).resolve()
    result = {p for p in root.glob("*.md") if p.is_file() or p.is_symlink()}
    for folder in ("docs", "references", ".github"):
        base = root / folder
        if base.is_dir():
            result.update(p for p in base.rglob("*.md") if p.is_file() or p.is_symlink())
    for rel in ("NOTICE", "CITATION.cff"):
        p = root / rel
        if p.exists() or p.is_symlink():
            result.add(p)
    return sorted(result)


def inspect(root: Path) -> dict:
    root = Path(root).resolve()
    issues: list[str] = []
    paths = public_documents(root)
    for path in paths:
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            issues.append(f"{rel}: linked public document")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            issues.append(f"{rel}: cannot decode public document")
            continue
        patterns = dict(SECRET_PATTERNS)
        if path.suffix == ".md":
            patterns.update(PRIVATE_REFERENCE_PATTERNS)
        for label, pattern in patterns.items():
            if pattern.search(text):
                issues.append(f"{rel}: possible {label} (content intentionally suppressed)")
    return {"documents": len(paths), "issues": issues}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=str(ROOT))
    args = ap.parse_args(argv)
    result = inspect(Path(args.repo))
    print(f"public_documents_checked={result['documents']}")
    print(f"public_document_findings={len(result['issues'])}")
    for msg in result["issues"]:
        print("ERROR:", msg)
    return 1 if result["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
