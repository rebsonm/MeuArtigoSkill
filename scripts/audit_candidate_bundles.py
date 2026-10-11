#!/usr/bin/env python3
"""Fail-closed offline audit of unpublished Skill and plugin review bundles.

No deployment, credential handling, research corpus access or release publication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

from version_info import ROOT, read_version

DISALLOWED = {".pdf", ".doc", ".docx", ".xlsx", ".xls", ".env", ".pem",
              ".key", ".p12", ".sqlite", ".db", ".secrets"}
DISALLOWED_SUBSTRINGS = ("/fulltext_corpus/", "/corpus_real/", "/private/",
                         "project_config.json", "/node_modules/", "/__pycache__/",
                         "credentials.json", "service-account", "token.json")
REQUIRED_PLUGIN_FILES = {"plugin.json", ".codex-plugin/plugin.json",
                         "assets/icon.svg", "skills/meu-artigo/SKILL.md",
                         "skills/meu-artigo/LICENSE", "skills/meu-artigo/NOTICE"}
EXPECTED_ICON = "./assets/icon.svg"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_zip(archive: Path) -> dict[str, bytes]:
    with ZipFile(archive, "r") as z:
        names = z.namelist()
        if z.testzip() is not None or len(set(names)) != len(names):
            raise ValueError(f"{archive.name}: corrupt or duplicate ZIP members")
        for n in names:
            p = PurePosixPath(n)
            if (not n or n.startswith("/") or "\\" in n or
                    ".." in p.parts or p.is_absolute() or
                    any(x.startswith(".env") for x in p.parts) or
                    p.suffix.lower() in DISALLOWED or
                    any(frag in "/" + n.lower() for frag in DISALLOWED_SUBSTRINGS)):
                raise ValueError(f"{archive.name}: prohibited path: {n}")
            obj = z.getinfo(n)
            if (obj.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError(f"{archive.name}: symlinks prohibited: {n}")
            if obj.file_size > 8 * 1024 * 1024:
                raise ValueError(f"{archive.name}: unexpectedly large member: {n}")
        return {n: z.read(n) for n in names}


def validate_candidates(root: Path, dist: Path) -> dict:
    version = read_version(root)
    skill = dist / f"MeuArtigoSkill-v{version}.zip"
    plugin = dist / f"MeuArtigoPlugin-v{version}-candidate.zip"
    for p in (skill, plugin):
        if not p.is_file():
            raise ValueError(f"candidate archive missing: {p.name}")
    a = validate_zip(skill)
    b = validate_zip(plugin)
    if "BUNDLE_MANIFEST.json" not in a or not REQUIRED_PLUGIN_FILES.issubset(b):
        raise ValueError("missing Skill manifest or essential plugin members")
    manifest = json.loads(a["BUNDLE_MANIFEST.json"])
    if manifest["version"] != version or manifest["scientific_quality_validated"] is not False:
        raise ValueError("invalid Skill version or scientific-status claim")
    if set(manifest["files"]) != set(a) - {"BUNDLE_MANIFEST.json"}:
        raise ValueError("Skill archive differs from manifest file list")
    for n, digest in manifest["files"].items():
        if sha(a[n]) != digest:
            raise ValueError(f"Skill per-file checksum mismatch: {n}")
    for n, data in a.items():
        if n != "BUNDLE_MANIFEST.json" and n != "SKILL.md":
            if b.get("skills/meu-artigo/" + n) != data:
                raise ValueError(f"Skill/plugin embedded source mismatch: {n}")
    packed_skill = b["skills/meu-artigo/SKILL.md"].decode("utf-8")
    if "Plugin installation alone grants no" not in packed_skill:
        raise ValueError("Plugin boundary adapter missing")
    if not all(x in packed_skill for x in ("GATE", "Google Drive", "C.A.D.A.")):
        raise ValueError("Core scientific workflow has been lost")
    portable = json.loads(b["plugin.json"])
    codex = json.loads(b[".codex-plugin/plugin.json"])
    ui = portable["extensions"]["com.openai"]["interface"]
    alt = codex["interface"]
    if not all(x.get("name") == "meu-artigo" and x.get("version") == version
               for x in (portable, codex)):
        raise ValueError("Plugin identity and version mismatch")
    if (ui.get("logo") != EXPECTED_ICON or ui.get("composerIcon") != EXPECTED_ICON
            or alt.get("logo") != EXPECTED_ICON or alt.get("composerIcon") != EXPECTED_ICON):
        raise ValueError("Plugin listing icon fields are missing or inconsistent")
    for key in ("displayName", "shortDescription", "longDescription",
                "developerName", "defaultPrompt"):
        if ui.get(key) != alt.get(key):
            raise ValueError(f"Plugin manifest presentation differs: {key}")
    if len(ui["shortDescription"]) > 30:
        raise ValueError("Plugin shortDescription exceeds the documented limit")
    if (b["assets/icon.svg"] != a.get("assets/icon.svg") or
            b["assets/icon.svg"] != b["skills/meu-artigo/assets/icon.svg"] or
            b["assets/icon.svg"] != (root / "assets/icon.svg").read_bytes()):
        raise ValueError("Icon is not the unchanged historical SVG")
    if "mcp.json" in b or ".app.json" in b or any(n.startswith("visual-app/") for n in b):
        raise ValueError("Candidate cannot imply active MCP server or App binding")
    if not a["LICENSE"].lstrip().startswith(b"Apache License"):
        raise ValueError("Apache-2.0 license is missing")
    if not a["NOTICE"].startswith(b"Meu Artigo"):
        raise ValueError("Original NOTICE attribution is missing")
    receipt_files = ["BUNDLE_BUILD_RECEIPT.json", "PLUGIN_BUILD_RECEIPT.json"]
    for fname in receipt_files:
        if not (dist / fname).is_file():
            raise ValueError(f"Missing external build receipt: {fname}")
    skill_receipt = json.loads((dist / receipt_files[0]).read_text(encoding="utf-8"))
    plugin_receipt = json.loads((dist / receipt_files[1]).read_text(encoding="utf-8"))
    if skill_receipt["package_sha256"] != sha(skill.read_bytes()) or \
       plugin_receipt["package_sha256"] != sha(plugin.read_bytes()):
        raise ValueError("External package receipt checksum does not match real bytes")
    if (plugin_receipt["plugin_kind"] != "SKILLS_ONLY_CANDIDATE" or
            plugin_receipt["mcp_app_deployed"] is not False or
            plugin_receipt["drive_sync_verified"] is not False or
            plugin_receipt["scientific_quality_validated"] is not False):
        raise ValueError("Plugin receipt overstates deployment or scientific validity")
    notes = (root / "docs" / f"NOTAS-DA-VERSAO-{version}.md").read_text(encoding="utf-8")
    citation = (root / "CITATION.cff").read_text(encoding="utf-8")
    if "NOT PUBLISHED" not in notes or re.search(r"(?m)^date-released:", citation):
        raise ValueError("Candidate must stay clearly unpublished")
    report = {
        "schema_version": 1,
        "version": version,
        "candidate_only": True,
        "public_release_created": False,
        "plugin_installed_or_updated": False,
        "mcp_app_deployed": False,
        "drive_sync_verified": False,
        "scientific_validation_claimed": False,
        "skill": {"filename": skill.name, "sha256": sha(skill.read_bytes()),
                  "members": len(a)},
        "plugin": {"filename": plugin.name, "sha256": sha(plugin.read_bytes()),
                   "members": len(b), "kind": "SKILLS_ONLY_CANDIDATE"},
        "source_verification": skill_receipt.get("source_verification", "UNVERIFIED"),
        "source_commit": skill_receipt.get("build_source_commit"),
        "checks": ["CRC", "paths", "per-file hashes", "privacy allowlist",
                   "manifest identity", "historical icon", "skill core",
                   "external receipts", "no fabricated MCP endpoint",
                   "unpublished status"],
    }
    return report


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", default=str(ROOT))
    p.add_argument("--dist", default="")
    args = p.parse_args()
    root = Path(args.repo).resolve()
    dist = Path(args.dist).resolve() if args.dist else root / "dist"
    try:
        report = validate_candidates(root, dist)
    except (OSError, KeyError, ValueError, TypeError, RuntimeError) as exc:
        print("CANDIDATE_VERIFICATION=FAILED; " + str(exc))
        return 2
    (dist / "CANDIDATE_VERIFICATION.json").write_text(
        json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    (dist / "CANDIDATE_SHA256SUMS.txt").write_text(
        report["skill"]["sha256"] + "  " + report["skill"]["filename"] + "\n" +
        report["plugin"]["sha256"] + "  " + report["plugin"]["filename"] + "\n",
        encoding="utf-8")
    print("CANDIDATE_VERIFICATION=PASSED")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
