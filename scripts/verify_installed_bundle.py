#!/usr/bin/env python3
"""Verify the ACTUAL installed Skill directory, not a separately downloaded PR snapshot.

A host may rewrite icon or agent metadata: list mismatches without attributing
tampering. Use the immutable ZIP manifest to determine whether the active
installation is byte-identical to the tested candidate. No network, secrets
or modifications.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

MAX_FILE_BYTES = 8_000_000
MAX_PAYLOADS = 1000
SHA = re.compile(r"[0-9a-f]{64}\Z")


def verify(root: Path, *, expected_version="1.0.0-rc.1") -> dict:
    root = root.resolve()
    manifest_path = root / "BUNDLE_MANIFEST.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        return {"status": "FAIL", "reason": "BUNDLE_MANIFEST_NOT_INSTALLED",
                "expected_version": expected_version}
    if manifest_path.stat().st_size > 2_000_000:
        raise ValueError("MANIFEST_TOO_LARGE")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    items = manifest.get("files")
    if not isinstance(items, dict) or not (1 <= len(items) <= MAX_PAYLOADS):
        raise ValueError("INVALID_BUNDLE_MANIFEST")
    version_path = root / "VERSION"
    version = (version_path.read_text(encoding="utf-8").strip()
               if version_path.is_file() and not version_path.is_symlink() else None)
    declared = manifest.get("version")
    mismatches = []
    missing = []
    for name, digest in sorted(items.items()):
        p = Path(name)
        if (not isinstance(name, str) or p.is_absolute() or
                ".." in p.parts or str(p).startswith(".") or
                not isinstance(digest, str) or not SHA.fullmatch(digest)):
            raise ValueError("UNSAFE_OR_INVALID_MANIFEST_ENTRY")
        target = root / p
        if not target.is_file() or target.is_symlink():
            missing.append(name)
            continue
        if target.stat().st_size > MAX_FILE_BYTES:
            mismatches.append(name)
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != digest:
            mismatches.append(name)
    checks = {"expected_version_matches_executable": version == expected_version,
              "manifest_matches_executable": declared == version,
              "payload_integrity": not (mismatches or missing)}
    status = "PASS" if all(checks.values()) else "FAIL"
    return {"status": status, "checks": checks,
            "expected_version": expected_version,
            "manifest_version": declared, "executable_version": version,
            "manifest_build_source_commit": manifest.get("build_source_commit"),
            "source_verification": manifest.get("source_verification"),
            "payload_count": len(items), "mismatched_files": mismatches,
            "missing_files": missing,
            "note": "A differing installed asset does not prove tampering; inspect host transforms and reinstall if necessary."}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--expected-version", default="1.0.0-rc.1")
    args = p.parse_args(argv)
    try:
        result = verify(args.root, expected_version=args.expected_version)
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = {"status": "FAIL", "reason": str(exc)}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
