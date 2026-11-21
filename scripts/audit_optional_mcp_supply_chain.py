#!/usr/bin/env python3
"""Fail-closed npm dependency contract for the optional, isolated MCP Apps module.

A manifest without an exact npm lock must fail. The upstream PR #74/#75 does
not yet contain a lockfile; merging it unchanged must therefore be blocked.
This tool never downloads packages, executes install hooks, or accepts auth.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL = Path("integrations/mcp-apps")


def validate(root: Path = ROOT) -> dict:
    folder = root / REL
    manifest = folder / "package.json"
    lockfile = folder / "package-lock.json"
    if not manifest.is_file():
        if lockfile.exists():
            raise ValueError("MCP_LOCK_WITHOUT_MANIFEST")
        return {"status": "NOT_IN_BASELINE", "node_mcp_present": False}
    if manifest.is_symlink() or lockfile.is_symlink():
        raise ValueError("MCP_MANIFEST_OR_LOCK_SYMLINK")
    if not lockfile.is_file():
        raise ValueError("MCP_NPM_LOCK_REQUIRED")
    try:
        pkg = json.loads(manifest.read_text(encoding="utf-8"))
        lock = json.loads(lockfile.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("MCP_INVALID_PACKAGE_OR_LOCK") from exc
    if not isinstance(pkg, dict) or not isinstance(lock, dict):
        raise ValueError("MCP_PACKAGE_OR_LOCK_NOT_OBJECT")
    if pkg.get("private") is not True or pkg.get("publishConfig"):
        raise ValueError("MCP_MUST_BE_PRIVATE")
    if lock.get("lockfileVersion") not in (2, 3):
        raise ValueError("MCP_LOCKFILE_VERSION_UNSUPPORTED")
    deps = pkg.get("dependencies", {})
    dev = pkg.get("devDependencies", {})
    if not isinstance(deps, dict) or not isinstance(dev, dict):
        raise ValueError("MCP_DEPENDENCY_MAP_INVALID")
    packages = lock.get("packages")
    rootpkg = packages.get("") if isinstance(packages, dict) else None
    if not isinstance(rootpkg, dict) or (
        rootpkg.get("dependencies", {}) != deps or
        rootpkg.get("devDependencies", {}) != dev or
        rootpkg.get("name") != pkg.get("name") or
        rootpkg.get("version") != pkg.get("version")
    ):
        raise ValueError("MCP_MANIFEST_LOCK_DRIFT")
    return {"status": "LOCK_DECLARATIONS_MATCH", "node_mcp_present": True}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        result = validate(args.root)
    except ValueError as exc:
        print("ERROR: " + str(exc))
        return 1
    print("supply_chain_status=" + result["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
