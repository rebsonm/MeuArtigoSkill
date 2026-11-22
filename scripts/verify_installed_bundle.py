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
from xml.etree import ElementTree

MAX_FILE_BYTES = 8_000_000
MAX_PAYLOADS = 1000
HOST_PRESENTATION = {
    "agents/openai.yaml": "PLATFORM_YAML_RESERIALIZATION",
    "assets/icon.svg": "HOST_ICON_REPLACEMENT",
}
RECEIPT_SCHEMA = "MEU_ARTIGO_HOST_PRESENTATION_REVIEW_V1"
SHA = re.compile(r"[0-9a-f]{64}\Z")



def _safe_host_svg(path: Path) -> bool:
    """Reject executable SVG features while preserving platform appearance freedom."""
    try:
        data = path.read_bytes()
        if len(data) > 1_000_000:
            return False
        root = ElementTree.fromstring(data)
        if root.tag.split("}")[-1].lower() != "svg":
            return False
        forbidden = {"script", "foreignobject", "iframe", "object", "embed",
                     "animate", "animatetransform", "set", "image"}
        for node in root.iter():
            if node.tag.split("}")[-1].lower() in forbidden:
                return False
            for key, value in node.attrib.items():
                key = key.split("}")[-1].lower()
                v = value.strip().lower()
                if (key.startswith("on") or key in {"href", "src"} or
                    "javascript:" in v or "data:" in v or
                    "url(http" in v or "url(//" in v):
                    return False
        return True
    except (ElementTree.ParseError, OSError, UnicodeError):
        return False


def _validate_host_receipt(root: Path, receipt_path: Path, *, manifest_sha: str,
                           expected_manifest_sha: str | None, version: str,
                           build_commit: str | None, source_digests: dict,
                           mismatched: list[str]) -> tuple[list[str], str]:
    """Allow only exact, externally reviewed host rewrites of two presentation assets.

    Never create or sign this receipt automatically. A receipt is an operator
    attestation, not cryptographic proof of the host's identity.
    """
    if not expected_manifest_sha or not SHA.fullmatch(expected_manifest_sha):
        return [], "PINNED_MANIFEST_SHA256_REQUIRED"
    if manifest_sha != expected_manifest_sha:
        return [], "BUNDLE_MANIFEST_NOT_PINNED"
    receipt_path = receipt_path.expanduser()
    if receipt_path.is_symlink():
        return [], "RECEIPT_SYMLINK_REJECTED"
    receipt_path = receipt_path.resolve()
    if receipt_path == root or root in receipt_path.parents:
        return [], "RECEIPT_MUST_BE_OUTSIDE_SKILL"
    if not receipt_path.is_file() or receipt_path.is_symlink() or receipt_path.stat().st_size > 500_000:
        return [], "RECEIPT_MISSING_OR_UNSAFE"
    try:
        record = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (ValueError, OSError, UnicodeError):
        return [], "RECEIPT_INVALID_JSON"
    if (not isinstance(record, dict) or record.get("schema") != RECEIPT_SCHEMA or
        record.get("host") != "CHATGPT" or record.get("expected_version") != version or
        record.get("bundle_manifest_sha256") != manifest_sha or
        record.get("build_source_commit") != build_commit or
        record.get("reviewed") is not True or
        len(str(record.get("reviewer", "")).strip()) < 3 or
        len(str(record.get("review_evidence", "")).strip()) < 30 or
        len(str(record.get("host_save_readback_evidence", "")).strip()) < 20):
        return [], "RECEIPT_AUTHORIZATION_OR_PROVENANCE_INCOMPLETE"
    entries = record.get("transformed_assets")
    if not isinstance(entries, list) or len(entries) != len(mismatched):
        return [], "RECEIPT_ASSET_SET_MISMATCH"
    mapped = {}
    for item in entries:
        if not isinstance(item, dict) or item.get("path") in mapped:
            return [], "RECEIPT_DUPLICATE_OR_INVALID"
        name = item.get("path")
        if name not in HOST_PRESENTATION or name not in mismatched:
            return [], "UNAPPROVED_PAYLOAD_TRANSFORMATION"
        if (item.get("host_action") != HOST_PRESENTATION[name] or
            item.get("source_sha256") != source_digests[name] or
            item.get("reviewed") is not True or
            not isinstance(item.get("installed_sha256"), str) or
            not SHA.fullmatch(item["installed_sha256"])):
            return [], "RECEIPT_ASSET_PROVENANCE_INVALID"
        target = root / name
        if not target.is_file() or target.is_symlink():
            return [], "RECEIPT_ASSET_MISSING"
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest != item["installed_sha256"]:
            return [], "HOST_PRESENTATION_CHANGED_AFTER_REVIEW"
        if name.endswith(".svg") and not _safe_host_svg(target):
            return [], "HOST_ICON_UNSAFE_XML"
        if name.endswith(".yaml"):
            try:
                body = target.read_text(encoding="utf-8")
            except (UnicodeError, OSError):
                return [], "HOST_YAML_INVALID_UTF8"
            if len(body) > 100_000 or not re.search(r"(?m)^\s*interface\s*:", body):
                return [], "HOST_YAML_PRESENTATION_STRUCTURE_MISSING"
        mapped[name] = digest
    if set(mapped) != set(mismatched):
        return [], "RECEIPT_NOT_EXACT_MISMATCH_SET"
    return sorted(mapped), "HOST_REVIEWED_EXACT_PAYLOAD_BYTES"


def draft_host_receipt(root: Path, *, expected_version="1.0.0-rc.1") -> dict:
    """Generate an UNAPPROVED draft only; independent operator review required."""
    root = root.resolve()
    raw = (root / "BUNDLE_MANIFEST.json").read_bytes()
    manifest = json.loads(raw)
    assets = []
    for name, kind in HOST_PRESENTATION.items():
        path = root / name
        original = manifest["files"][name]
        observed = hashlib.sha256(path.read_bytes()).hexdigest()
        if original != observed:
            assets.append({"path": name, "host_action": kind,
                           "source_sha256": original, "installed_sha256": observed,
                           "reviewed": False})
    return {"schema": RECEIPT_SCHEMA, "host": "CHATGPT",
            "expected_version": expected_version,
            "build_source_commit": manifest.get("build_source_commit"),
            "bundle_manifest_sha256": hashlib.sha256(raw).hexdigest(),
            "reviewer": "", "reviewed": False, "review_evidence": "",
            "host_save_readback_evidence": "",
            "transformed_assets": assets}

def verify(root: Path, *, expected_version="1.0.0-rc.1",
           host_receipt: Path | None = None,
           expected_manifest_sha256: str | None = None) -> dict:
    root = root.resolve()
    manifest_path = root / "BUNDLE_MANIFEST.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        return {"status": "FAIL", "reason": "BUNDLE_MANIFEST_NOT_INSTALLED",
                "expected_version": expected_version}
    if manifest_path.stat().st_size > 2_000_000:
        raise ValueError("MANIFEST_TOO_LARGE")
    manifest_bytes = manifest_path.read_bytes()
    manifest_sha = hashlib.sha256(manifest_bytes).hexdigest()
    manifest = json.loads(manifest_bytes)
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
    acknowledged, receipt_status = [], "NOT_APPLICABLE"
    if host_receipt is not None and mismatches and not missing:
        acknowledged, receipt_status = _validate_host_receipt(
            root, host_receipt, manifest_sha=manifest_sha,
            expected_manifest_sha=expected_manifest_sha256,
            version=version, build_commit=manifest.get("build_source_commit"),
            source_digests=items, mismatched=mismatches)
    elif expected_manifest_sha256 and manifest_sha != expected_manifest_sha256:
        receipt_status = "BUNDLE_MANIFEST_NOT_PINNED"
    unresolved = sorted(set(mismatches) - set(acknowledged))
    checks = {"expected_version_matches_executable": version == expected_version,
              "manifest_matches_executable": declared == version,
              "manifest_pinned": (expected_manifest_sha256 is None or
                                  manifest_sha == expected_manifest_sha256),
              "payload_integrity": not (unresolved or missing)}
    status = "PASS" if all(checks.values()) else "FAIL"
    return {"status": status, "checks": checks,
            "expected_version": expected_version,
            "manifest_version": declared, "executable_version": version,
            "manifest_build_source_commit": manifest.get("build_source_commit"),
            "source_verification": manifest.get("source_verification"),
            "payload_count": len(items), "mismatched_files": mismatches,
            "unresolved_mismatches": unresolved,
            "host_reviewed_presentation_files": acknowledged,
            "host_presentation_receipt_status": receipt_status,
            "integrity_mode": ("CORE_EXACT_HOST_PRESENTATION_ATTESTED" if acknowledged
                               else "ALL_BUNDLE_BYTES_EXACT" if not mismatches else "FAILED"),
            "bundle_manifest_sha256": manifest_sha,
            "missing_files": missing,
            "note": "A differing installed asset does not prove tampering; inspect host transforms and reinstall if necessary."}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--expected-version", default="1.0.0-rc.1")
    p.add_argument("--host-receipt", type=Path, help="Operator-reviewed receipt stored OUTSIDE the Skill installation")
    p.add_argument("--expected-manifest-sha256", help="Immutable manifest SHA from independently verified release")
    p.add_argument("--emit-host-receipt-draft", action="store_true", help="Print an UNAPPROVED host presentation receipt draft, never approves it")
    args = p.parse_args(argv)
    try:
        result = (draft_host_receipt(args.root, expected_version=args.expected_version)
                  if args.emit_host_receipt_draft else verify(
                      args.root, expected_version=args.expected_version,
                      host_receipt=args.host_receipt,
                      expected_manifest_sha256=args.expected_manifest_sha256))
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = {"status": "FAIL", "reason": str(exc)}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if result.get("status") == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
