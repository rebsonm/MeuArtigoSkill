#!/usr/bin/env python3
"""Scan all tracked text files for high-confidence credential signatures.

This prevents common accidental commits; it is NOT a Git history scan or a
substitute for GitHub secret scanning / push protection. Never print secrets.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGNATURES = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"),
    "GitHub credential": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b"),
    "OpenAI API key": re.compile(r"\bsk-[A-Za-z0-9_-]{32,}\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "Google API key": re.compile(r"\bAIza[A-Za-z0-9_-]{35}\b"),
    "Google OAuth client secret": re.compile(r"\bGOCSPX-[A-Za-z0-9_-]{20,}\b"),
    "GitLab token": re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"),
    "npm token": re.compile(r"\bnpm_[A-Za-z0-9]{30,}\b"),
    "JWT": re.compile(r"\beyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\b"),
}
FORBIDDEN_BASENAMES = {
    ".env", "id_rsa", "id_ed25519", "google-credentials.json",
}
FORBIDDEN_SUFFIXES = {".pem", ".p12", ".pfx", ".jks"}
EXAMPLE_NAMES = {".env.example", ".env.sample", ".env.template"}


def scan_entry(name: str, blob: bytes) -> list[str]:
    """Return labels only, never the matching substring."""
    path = Path(name)
    if (path.name in FORBIDDEN_BASENAMES or
        (path.name.startswith(".env.") and path.name not in EXAMPLE_NAMES) or
        path.suffix in FORBIDDEN_SUFFIXES):
        return ["credential-like filename"]
    if b"\0" in blob:
        return []
    try:
        content = blob.decode("utf-8")
    except UnicodeDecodeError:
        return []
    return [label for label, pattern in SIGNATURES.items() if pattern.search(content)]


def inspect(root: Path = ROOT) -> dict:
    result = subprocess.run(["git", "ls-files", "-z", "--cached"],
                            cwd=root, stdout=subprocess.PIPE, check=True)
    names = [p.decode("utf-8") for p in result.stdout.split(b"\0") if p]
    alerts = []
    for rel in names:
        path = root / rel
        if path.is_symlink():
            continue
        # Avoid multi-megabyte non-source blobs; images and ZIPs are binary.
        if not path.is_file() or path.stat().st_size > 4_000_000:
            continue
        for label in scan_entry(rel, path.read_bytes()):
            alerts.append(f"{rel}: possible {label} (value suppressed)")
    return {"checked": len(names), "alerts": alerts}


if __name__ == "__main__":
    report = inspect()
    print("tracked_files_checked=" + str(report["checked"]))
    print("possible_secret_findings=" + str(len(report["alerts"])))
    for alert in report["alerts"]:
        print("ERROR:", alert)
    raise SystemExit(1 if report["alerts"] else 0)
