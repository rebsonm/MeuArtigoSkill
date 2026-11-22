#!/usr/bin/env python3
"""Inventory possible Portuguese editorial prose in every repository Markdown file.

Unlike the legacy release-source check, this includes methodology cards,
bibliographic prospecting cards, intake records, Wiki, docs, and references.
It is a signal for editorial review, not automatic translation certification.
Bibliographic titles and direct-source labels are preserved as source data.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from audit_source_language import PORTUGUESE_WORDS

ROOT = Path(__file__).resolve().parents[1]
IGNORE_DIRS = {".git", ".venv", "__pycache__", ".cache", "dist"}
SOURCE_LABELS = (
    "- Bibliographic source:", "- Fonte bibliográfica:",
    "- Original published title:", "- Título original:",
)
ANCHOR = re.compile(r'(?m)^\s*<a\s+id="[^"]+"></a>\s*$')


def inspect_markdown(root: Path, threshold: int = 7) -> dict:
    """Return source paths and counts, never document text or source excerpts."""
    if threshold < 1:
        raise ValueError("threshold must be positive")
    root = Path(root).resolve()
    files = sorted(
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() == ".md"
        and not any(part in IGNORE_DIRS for part in p.relative_to(root).parts)
    )
    unresolved = []
    unreadable = []
    by_area = {}
    for path in files:
        rel = path.relative_to(root).as_posix()
        top = rel.split("/")[0] if "/" in rel else "ROOT"
        by_area[top] = by_area.get(top, 0) + 1
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            unreadable.append(rel)
            continue
        content = ANCHOR.sub("", content)
        # Original bibliographic titles are source data, not translation targets.
        lines = []
        in_fence = False
        for line in content.splitlines():
            if line.lstrip().startswith(chr(96) * 3):
                in_fence = not in_fence
                continue
            if in_fence or line.lstrip().startswith(SOURCE_LABELS):
                continue
            if rel == "knowledge/methodology/PDF-ATTRIBUTIONS.md" and line.lstrip().startswith("|"):
                continue
            if rel == "knowledge/methodology/pdfs/README.md" and line.lstrip().startswith("|"):
                continue
            lines.append(line)
        hits = len(PORTUGUESE_WORDS.findall("\n".join(lines)))
        if hits >= threshold:
            unresolved.append({"path": rel, "portuguese_indicators": hits})
    unresolved.sort(key=lambda item: (-item["portuguese_indicators"], item["path"]))
    return {
        "scan_scope": "ALL_REPOSITORY_MARKDOWN_INCLUDING_CARDS_SOURCE_CARDS_INTAKE",
        "markdown_files_scanned": len(files),
        "markdown_by_top_level_area": by_area,
        "files_requiring_editorial_language_review": len(unresolved),
        "unresolved": unresolved,
        "unreadable": unreadable,
        "english_only_verified": False,
        "method": "heuristic indicator inventory; source quotations, scholarly titles and fidelity need human review",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=str(ROOT))
    parser.add_argument("--strict", action="store_true",
                        help="fail if any Markdown needs language review")
    parser.add_argument("--threshold", type=int, default=7)
    args = parser.parse_args(argv)
    result = inspect_markdown(Path(args.repo), args.threshold)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["unreadable"]:
        return 1
    return 2 if args.strict and result["unresolved"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
