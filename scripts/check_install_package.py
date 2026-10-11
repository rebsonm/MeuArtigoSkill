#!/usr/bin/env python3
"""Identify a Meu Artigo ZIP before a user attempts ChatGPT installation.

Offline only: no account, external API, scientific-corpus or plugin writes.
Exit 0 for a valid expected package; 2 for wrong type/structure; 1 for invalid ZIP.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile

MAX_FILES = 3000
MAX_UNCOMPRESSED = 100 * 1024 * 1024
SKILL_ENTRY = "skills/meu-artigo/SKILL.md"


def diagnose(path: Path, expect: str = "auto") -> dict[str, str | bool]:
    base = {"valid": False, "kind": "INVALID", "reason": "",
            "next_step": "", "expected": expect}
    if not path.is_file():
        return {**base, "reason": "FILE_NOT_FOUND",
                "next_step": "Choose a ZIP that exists on your computer; no upload was performed."}
    try:
        with ZipFile(path) as z:
            members = z.infolist()
            names = [m.filename for m in members if not m.is_dir()]
            all_names = set(names)
            if (len(members) > MAX_FILES or len(names) != len(all_names)
                    or sum(m.file_size for m in members) > MAX_UNCOMPRESSED
                    or any(m.filename.startswith("/") or "\\" in m.filename
                           or ".." in PurePosixPath(m.filename).parts
                           or (m.external_attr >> 16) & 0o170000 == 0o120000
                           for m in members)):
                raise ValueError("Unsafe, oversized or duplicate archive")
            if z.testzip() is not None:
                raise BadZipFile("CRC mismatch")

            def result(kind: str, valid: bool, reason: str, next_step: str):
                return {**base, "kind": kind, "valid": valid,
                        "reason": reason, "next_step": next_step}

            if "plugin.json" in all_names:
                try:
                    manifest = json.loads(z.read("plugin.json").decode("utf-8"))
                except (ValueError, UnicodeError):
                    return result("PLUGIN", False, "INVALID_PLUGIN_MANIFEST",
                                  "Obtain an official plugin distribution ZIP; do not rename a GitHub source archive.")
                identity = manifest.get("name") if isinstance(manifest, dict) else None
                if identity != "meu-artigo" or not manifest.get("version"):
                    return result("PLUGIN", False, "WRONG_PLUGIN_IDENTITY",
                                  "The manifest must name the Meu Artigo plugin and state its version.")
                if SKILL_ENTRY not in all_names:
                    return result("PLUGIN", False, "MISSING_PACKAGED_SKILL",
                                  "This ZIP needs skills/meu-artigo/SKILL.md. Download a prepared plugin ZIP.")
                skill = z.read(SKILL_ENTRY)
                if not skill.startswith(b"---\n"):
                    return result("PLUGIN", False, "INVALID_SKILL_ENTRY",
                                  "The plugin Skill entrypoint is invalid. Obtain the prepared distribution.")
                ui = manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})
                for key in ("logo", "composerIcon"):
                    path_value = ui.get(key)
                    if path_value and path_value.removeprefix("./") not in all_names:
                        return result("PLUGIN", False, "MISSING_ICON_ASSET",
                                      "The plugin references an icon that was not included in this ZIP.")
                if expect == "skill":
                    return result("PLUGIN", False, "PLUGIN_NOT_SKILL",
                                  "Use this ZIP under Plugins, not the Skills installer. For Skills download the published Skill ZIP.")
                return result("PLUGIN", True, "PLUGIN_PACKAGE_OK",
                              "Use Plugins → Add plugin or the existing plugin's Upload new version dialog. The plugin's capabilities still depend on real connected services.")

            if "SKILL.md" in all_names:
                if not z.read("SKILL.md").startswith(b"---\n"):
                    return result("SKILL", False, "INVALID_SKILL_ENTRY",
                                  "Obtain the published Skill distribution ZIP.")
                if expect == "plugin":
                    return result("SKILL", False, "SKILL_NOT_PLUGIN",
                                  "This is a Skill ZIP, not a plugin ZIP. Use the Skills upload menu; do not use Add plugin.")
                return result("SKILL", True, "SKILL_PACKAGE_OK",
                              "Use the platform's Skills upload, not Add plugin. Check access to any required external services after installation.")

            # GitHub's automatically generated source ZIP wraps the repository
            # in a branch-named directory and normally contains a plain SKILL.md.
            roots = {n.split("/", 1)[0] for n in names if "/" in n}
            for root in roots:
                if f"{root}/SKILL.md" in all_names and (
                    f"{root}/VERSION" in all_names or
                    f"{root}/plugin/plugin.json" in all_names
                ):
                    return result("GITHUB_SOURCE", False, "SOURCE_ARCHIVE_NOT_INSTALLER",
                                  "You downloaded Code → Download ZIP / Source code (zip). Do not upload it. For a Skill use the published release asset; for a plugin obtain the separately prepared plugin ZIP.")

            if "plugin/plugin.json" in all_names:
                return result("GITHUB_SOURCE", False, "MANIFEST_NESTED_IN_REPOSITORY",
                              "plugin/plugin.json belongs to the source tree, not the packaged plugin root. Obtain the prepared plugin ZIP.")
            return result("UNKNOWN", False, "NO_SUPPORTED_ENTRYPOINT",
                          "This ZIP has neither plugin.json plus skills/meu-artigo/SKILL.md nor a root SKILL.md. Download the correct distribution.")
    except (OSError, BadZipFile, ValueError, RuntimeError) as exc:
        return {**base, "reason": "INVALID_OR_UNSAFE_ZIP",
                "next_step": f"Check that this is an intact .zip under 100 MB and download it again. ({type(exc).__name__})"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check an installation ZIP offline before uploading to ChatGPT.")
    parser.add_argument("archive", type=Path, help="ZIP downloaded to your computer")
    parser.add_argument("--expect", choices=("auto", "skill", "plugin"), default="auto")
    parser.add_argument("--json", action="store_true", help="Machine-readable diagnostic")
    opts = parser.parse_args(argv)
    info = diagnose(opts.archive, opts.expect)
    if opts.json:
        print(json.dumps(info, ensure_ascii=False, sort_keys=True))
    else:
        print(("PASS" if info["valid"] else "NOT READY") + " — " + info["kind"] +
              " (" + info["reason"] + ")")
        print(info["next_step"])
    if info["valid"]:
        return 0
    return 1 if info["kind"] == "INVALID" else 2


if __name__ == "__main__":
    raise SystemExit(main())
