#!/usr/bin/env python3
"""Fail-closed local technical report writer: never overwrite project data.

Only new outputs directly under 98_Technical_Reports are allowed.
No remote write/sync is implied. POSIX operations use directory handles.
"""
from __future__ import annotations

import os
from pathlib import Path
import re

REPORTS = "98_Technical_Reports"
MAX_REPORT_BYTES = 512_000
# Reject likely credentials and explicit restricted-corpus markers BEFORE
# any filesystem operation. This is a preventive check, not encryption.
SENSITIVE = re.compile(
    r"(?i)(?:Bearer\\s+[A-Za-z0-9_.-]{12,}|"
    r"(?:sk-|ghp_|github_pat_|AIza)[A-Za-z0-9_-]{12,}|"
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    r"PRIVATE_RESEARCH_EXCERPT|SECRET_PRIVATE_SOURCE)"
)

def private_report_payload(contents: str) -> str:
    if not isinstance(contents, str) or len(contents.encode("utf-8")) > MAX_REPORT_BYTES:
        raise ValueError("Private report content invalid or oversized")
    if chr(0) in contents or SENSITIVE.search(contents):
        raise ValueError("Private report may contain restricted information")
    return contents

NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,119}\Z")


def write_report(root: Path, requested: Path, contents: str,
                 *, allowed_extensions: frozenset[str]) -> Path:
    contents = private_report_payload(contents)
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Authorized project root is not a directory")
    raw = Path(requested)
    dest = raw if raw.is_absolute() else root / raw
    report_dir = root / REPORTS
    if (".." in raw.parts or dest.parent != report_dir or
            not NAME.fullmatch(dest.name) or
            dest.suffix.lower() not in allowed_extensions):
        raise ValueError("Report output must be a new supported file directly "
                         "inside " + REPORTS + " within the authorized project")
    if report_dir.is_symlink():
        raise ValueError("Symlinked report directory is prohibited")

    # POSIX directory handles protect against replacement of the containing
    # directory between checking it and opening an output file.
    portable = (not hasattr(os, "O_DIRECTORY") or
                os.open not in os.supports_dir_fd or
                os.mkdir not in os.supports_dir_fd)
    if portable:
        if report_dir.exists() and not report_dir.is_dir():
            raise ValueError("Report directory is not a regular directory")
        report_dir.mkdir(mode=0o700, exist_ok=True)
        if report_dir.is_symlink():
            raise ValueError("Symlinked report directory is prohibited")
        # Explicit owner-only mode even where directory-handle APIs are absent.
        fd = os.open(dest, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     getattr(os, "O_NOFOLLOW", 0), 0o600)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(contents)
                stream.flush()
                os.fsync(stream.fileno())
        except BaseException:
            dest.unlink(missing_ok=True)
            raise
        return dest

    flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
    root_fd = os.open(root, flags)
    report_fd = None
    try:
        try:
            os.mkdir(REPORTS, mode=0o700, dir_fd=root_fd)
        except FileExistsError:
            pass
        report_fd = os.open(REPORTS, flags, dir_fd=root_fd)
        file_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        file_fd = os.open(dest.name, file_flags, 0o600, dir_fd=report_fd)
        try:
            with os.fdopen(file_fd, "w", encoding="utf-8") as stream:
                stream.write(contents)
                stream.flush()
                os.fsync(stream.fileno())
        except BaseException:
            os.unlink(dest.name, dir_fd=report_fd)
            raise
        os.fsync(report_fd)
    finally:
        if report_fd is not None:
            os.close(report_fd)
        os.close(root_fd)
    return dest
