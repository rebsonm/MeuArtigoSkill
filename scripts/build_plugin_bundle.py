#!/usr/bin/env python3
"""Build one deterministic RC.4 ChatGPT plugin, never a standalone Skill installer.

--preflight reports a missing approved user logo as BLOCKED, without claiming
package readiness. Normal build fails closed when that logo is unavailable.
No external publishing, account access or scientific gate approvals occur.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import struct
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

from build_skill_bundle import list_sources, source_provenance
from bundle_dependency_audit import audit as audit_dependencies
from version_info import read_version

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "meu-artigo"
PLUGIN_VERSION = "1.0.0-rc.4"
LOGO_PATH = "assets/rc4-logo.png"
FIXED_TIME = (2026, 10, 9, 0, 0, 0)
INTEGRITY_PATH = "PLUGIN_BUNDLE_MANIFEST.json"
PACKAGE_PREFIX = PLUGIN_NAME + "/"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def checked_logo(root: Path) -> tuple[bool, str]:
    path = root / LOGO_PATH
    if not path.is_file() or path.is_symlink():
        return False, "RC4_LOGO_PENDING_VERIFIED_IMAGE_FILE"
    data = path.read_bytes()
    if not (len(data) >= 24 and len(data) <= 5 * 1024 * 1024
            and data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR"):
        return False, "RC4_LOGO_INVALID_PNG_OR_SIZE"
    width, height = struct.unpack(">II", data[16:24])
    if not (48 <= width <= 4096 and 48 <= height <= 4096 and width == height):
        return False, "RC4_LOGO_DIMENSIONS_REQUIRE_REVIEW"
    return True, "VERIFIED_PNG_SIGNATURE_AND_DIMENSIONS"


def source_payload(root: Path) -> dict[str, bytes]:
    files = list_sources(root)
    payload = {p.relative_to(root).as_posix(): p.read_bytes() for p in files}
    local_modules = {p.stem for p in (root / "scripts").glob("*.py") if p.is_file()}
    audit = audit_dependencies(payload, local_source_modules=local_modules)
    if audit["errors"]:
        raise ValueError("BUNDLE_DEPENDENCY_CLOSURE_FAILED: " + "; ".join(audit["errors"][:5]))
    if any(p.lower().endswith(".pdf") or "/.env" in p.lower() for p in payload):
        raise ValueError("THIRD_PARTY_PDF_OR_SECRET_NOT_ALLOWED")
    return payload


def checked_manifest(root: Path) -> dict:
    version = read_version(root)
    if version != PLUGIN_VERSION:
        raise ValueError("PLUGIN_ONLY_RC4_REQUIRES_VERSION_1_0_0_RC4")
    obj = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    if (obj.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
            or obj.get("name") != PLUGIN_NAME or obj.get("version") != version):
        raise ValueError("PLUGIN_SOURCE_MANIFEST_MISMATCH")
    return obj


def preflight(root: Path) -> dict:
    checked_manifest(root)
    payload = source_payload(root)
    if not payload["SKILL.md"].startswith(b"---\nname: meu-artigo\n"):
        raise ValueError("WRONG_SCIENTIFIC_ENTRYPOINT")
    ok, logo_status = checked_logo(root)
    return {
        "source_version": PLUGIN_VERSION,
        "distribution": "CHATGPT_PLUGIN_ONLY",
        "nested_skill_internal_only": True,
        "scientific_quality_validated": False,
        "logo_ready": ok,
        "logo_status": logo_status,
        "plugin_build_ready": ok,
        "included_science_files": len(payload),
        "host_normal_chat_verified": False,
        "host_work_verified": False,
        "source_evidence_only": True,
    }


def package(root: Path, dest: Path) -> dict:
    root = root.resolve()
    state = preflight(root)
    if not state["plugin_build_ready"]:
        raise ValueError(state["logo_status"] + ": do not publish with placeholder logo")
    if dest.name != f"MeuArtigoPlugin-v{PLUGIN_VERSION}.zip":
        raise ValueError("RC4_PACKAGE_NAME_MISMATCH")
    manifest = copy.deepcopy(checked_manifest(root))
    interface = manifest["extensions"]["com.openai"]["interface"]
    interface["logo"] = "./" + LOGO_PATH
    interface["composerIcon"] = "./" + LOGO_PATH

    source = source_payload(root)
    source_files = [root / p for p in source]
    provenance = source_provenance(root, source_files)
    built = {f"skills/{PLUGIN_NAME}/{p}": data for p, data in source.items()}
    built["plugin.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
    built[LOGO_PATH] = (root / LOGO_PATH).read_bytes()
    integrity = {
        "schema_version": 1,
        "version": PLUGIN_VERSION,
        "distribution_type": "CHATGPT_PLUGIN_ONLY",
        "publication_verified": False,
        "scientific_quality_validated": False,
        "source_entrypoint_sha256": digest(source["SKILL.md"]),
        "source_verification": provenance["source_verification"],
        "build_source_commit": provenance["build_source_commit"],
        "files": {path: digest(data) for path, data in sorted(built.items())},
    }
    built[INTEGRITY_PATH] = (json.dumps(integrity, indent=2, sort_keys=True) + "\n").encode()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(dest, "w", ZIP_DEFLATED, compresslevel=9) as z:
        for path, content in sorted(built.items()):
            info = ZipInfo(PACKAGE_PREFIX + path, FIXED_TIME)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, content, compress_type=ZIP_DEFLATED, compresslevel=9)
    verify_package(dest)
    (dest.parent / "SHA256SUMS.txt").write_text(
        f"{digest(dest.read_bytes())}  {dest.name}\n", encoding="utf-8")
    (dest.parent / "PLUGIN_BUILD_RECEIPT.json").write_text(
        json.dumps({
            "version": PLUGIN_VERSION, "distribution_type": "CHATGPT_PLUGIN_ONLY",
            "package": dest.name, "package_sha256": digest(dest.read_bytes()),
            "source_entrypoint_sha256": integrity["source_entrypoint_sha256"],
            "source_verification": provenance["source_verification"],
            "build_source_commit": provenance["build_source_commit"],
            "publication_verified": False, "host_acceptance_verified": False,
            "scientific_quality_validated": False,
        }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return integrity


def verify_package(path: Path) -> dict:
    with ZipFile(path, "r") as z:
        infos = z.infolist()
        paths = [i.filename for i in infos]
        if len(paths) != len(set(paths)) or len(paths) > 3000:
            raise ValueError("DUPLICATE_OR_OVERSIZED_PLUGIN_ARCHIVE")
        if any(not p.startswith(PACKAGE_PREFIX) or ".." in Path(p).parts
               or p.startswith("/") or "\\" in p for p in paths):
            raise ValueError("UNSAFE_PLUGIN_ARCHIVE_PATH")
        if any(i.is_dir() or (i.external_attr >> 16) & 0o170000 == 0o120000
               or i.flag_bits & 1 for i in infos):
            raise ValueError("UNSAFE_ENCRYPTED_OR_LINKED_PLUGIN_ARCHIVE")
        root = PACKAGE_PREFIX
        required = {root + "plugin.json",
                    root + f"skills/{PLUGIN_NAME}/SKILL.md",
                    root + LOGO_PATH, root + INTEGRITY_PATH}
        if not required.issubset(paths) or any(p.lower().endswith(".pdf") for p in paths):
            raise ValueError("MISSING_REQUIRED_PLUGIN_COMPONENT_OR_PDF_PRESENT")
        integrity = json.loads(z.read(root + INTEGRITY_PATH))
        files = {p.removeprefix(root): p for p in paths if p != root + INTEGRITY_PATH}
        if set(files) != set(integrity["files"]):
            raise ValueError("PLUGIN_INTEGRITY_MEMBERS_MISMATCH")
        for rel, member in files.items():
            if digest(z.read(member)) != integrity["files"][rel]:
                raise ValueError("PLUGIN_MEMBER_SHA256_MISMATCH: " + rel)
        manifest = json.loads(z.read(root + "plugin.json"))
        if manifest["version"] != PLUGIN_VERSION or manifest["name"] != PLUGIN_NAME:
            raise ValueError("PLUGIN_MANIFEST_IDENTITY_MISMATCH")
        if manifest["extensions"]["com.openai"]["interface"].get("logo") != "./" + LOGO_PATH:
            raise ValueError("APPROVED_LOGO_NOT_REFERENCED")
        skill = z.read(root + f"skills/{PLUGIN_NAME}/SKILL.md")
        if digest(skill) != integrity["source_entrypoint_sha256"]:
            raise ValueError("SOURCE_SKILL_CONTENT_CHANGED")
        if integrity["publication_verified"] or integrity["scientific_quality_validated"]:
            raise ValueError("UNSUPPORTED_PUBLICATION_OR_SCIENCE_CLAIM")
        return integrity


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        if args.verify:
            result = verify_package(args.verify)
        elif args.preflight:
            result = preflight(args.repo)
        else:
            destination = args.out or args.repo / "dist" / f"MeuArtigoPlugin-v{PLUGIN_VERSION}.zip"
            result = package(args.repo, destination)
            result = {**result, "package": str(destination)}
    except (ValueError, OSError, KeyError, TypeError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
