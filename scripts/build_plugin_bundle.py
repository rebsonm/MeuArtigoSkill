#!/usr/bin/env python3
"""Build a deterministic, sanitized Meu Artigo plugin candidate without deployment.

The archive contains the existing research Skill plus manifest/icon metadata.
The MCP Apps server in visual-app/ is separate source: an installed plugin will
not gain hosted tools or UI merely by carrying Python/TypeScript code.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from build_skill_bundle import list_sources, source_provenance, sha256
from version_info import read_version

ROOT = Path(__file__).resolve().parents[1]
FIXED_DATE = (2026, 10, 11, 0, 0, 0)
ICON_PATH = "./assets/icon.svg"
ALLOWED_MANIFEST = ("plugin.json", ".codex-plugin/plugin.json")


def json_bytes(obj: dict) -> bytes:
    return (json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def plugin_adapter(original: bytes) -> bytes:
    """Keep the original scientific router while adding a minimal plugin runtime boundary."""
    source = original.decode("utf-8")
    marker = "\n---\n"
    loc = source.find(marker, 4)
    if not source.startswith("---\n") or loc < 0:
        raise ValueError("SKILL.md needs valid YAML frontmatter")
    addition = (
        "\n## Packaged ChatGPT plugin runtime\n\n"
        "This Skill is loaded under skills/meu-artigo/. All relative docs/scripts "
        "live under this directory. Plugin installation alone grants no Google "
        "Drive access, local Python execution, hosting, paid API subscriptions "
        "or MCP Apps connection. Verify actual tools and canonical storage "
        "before claiming an operation. The visual-app/ server is developed "
        "separately and requires a real authorized deployment. Never turn a "
        "visual action or an AI screening proposal into human gate approval.\n"
    )
    return (source[:loc + len(marker)] + addition + source[loc + len(marker):]).encode("utf-8")


def build(root: Path, destination: Path) -> dict:
    root = root.resolve()
    version = read_version(root)
    if not version:
        raise ValueError("VERSION is absent")
    desired = f"MeuArtigoPlugin-v{version}-candidate.zip"
    if destination.name != desired:
        raise ValueError("Package filename must be " + desired)
    originals = list_sources(root)  # Strong allowlist: excludes corpus, secrets, PDFs.
    files = {}
    for item in originals:
        rel = item.relative_to(root).as_posix()
        name = "skills/meu-artigo/" + rel
        files[name] = plugin_adapter(item.read_bytes()) if rel == "SKILL.md" else item.read_bytes()

    for rel in ALLOWED_MANIFEST:
        manifest = json.loads((root / "plugin" / rel).read_text(encoding="utf-8"))
        manifest["version"] = version
        if manifest.get("name") != "meu-artigo":
            raise ValueError("Inconsistent plugin identity")
        ui = (manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})
              if rel == "plugin.json" else manifest.get("interface", {}))
        if ui.get("logo") != ICON_PATH or ui.get("composerIcon") != ICON_PATH:
            raise ValueError("Plugin icon paths not configured")
        files[rel] = json_bytes(manifest)
    files["assets/icon.svg"] = (root / "assets" / "icon.svg").read_bytes()
    if not files["assets/icon.svg"].lstrip().startswith(b"<svg "):
        raise ValueError("Missing SVG logo")
    files["README.md"] = (
        "# Meu Artigo plugin candidate\n\n"
        "Private plugin source package; research Skill and original logo are "
        "bundled. The MCP Apps visual server is NOT automatically deployed, "
        "and this archive does not include an MCP server endpoint. "
        "No installation, external synchronization or scientific validation is "
        "implied. See skills/meu-artigo/docs/MEU-ARTIGO-VISUAL.md.\n"
    ).encode("utf-8")

    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(files.items()):
            zi = ZipInfo(name, FIXED_DATE)
            zi.compress_type = ZIP_DEFLATED
            zi.external_attr = 0o100644 << 16
            z.writestr(zi, data, compress_type=ZIP_DEFLATED, compresslevel=9)

    with ZipFile(destination, "r") as z:
        if z.testzip() is not None or len(z.namelist()) != len(files):
            raise ValueError("ZIP integrity failure")
        if any(".." in Path(n).parts or n.startswith("/") for n in z.namelist()):
            raise ValueError("Unsafe archive member")
        for name, value in files.items():
            if z.read(name) != value:
                raise ValueError("Unexpected archive mismatch: " + name)

    provenance = source_provenance(root)
    receipt = {
        "schema_version": 1, "package": destination.name,
        "version": version, "package_sha256": sha256(destination.read_bytes()),
        "repository_origin": "https://github.com/rebsonm/MeuArtigoSkill",
        "source_commit": provenance["build_source_commit"],
        "source_verification": provenance["source_verification"],
        "plugin_kind": "SKILLS_ONLY_CANDIDATE",
        "mcp_app_deployed": False, "drive_sync_verified": False,
        "scientific_quality_validated": False,
        "included_files": len(files),
    }
    (destination.parent / "PLUGIN_BUILD_RECEIPT.json").write_bytes(json_bytes(receipt))
    return receipt


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", default=str(ROOT))
    p.add_argument("--out")
    a = p.parse_args(argv)
    root = Path(a.repo)
    version = read_version(root)
    dest = Path(a.out) if a.out else root / "dist" / f"MeuArtigoPlugin-v{version}-candidate.zip"
    receipt = build(root, dest)
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
