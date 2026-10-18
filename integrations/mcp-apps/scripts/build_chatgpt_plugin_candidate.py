#!/usr/bin/env python3
"""Build a non-published Meu Artigo ChatGPT plugin candidate.

The Skill payload is produced by the existing audited Skill ZIP builder.
Public submission packages MUST NOT contain an .app.json reference: the remote
MCP server is supplied separately via the OpenAI "With MCP" submission flow.
Private test candidates may reference a separately verified registered app.

No deployment, plugin installation, publication, Google Drive access or
scientific approval occurs in this script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
import sys

# Distribution tooling stays outside the installable researcher Skill.
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from build_skill_bundle import FIXED_DATE, package as build_skill_zip
from version_info import ROOT, read_version

APP_ID_PATTERN = re.compile(r"asdk_app_[A-Za-z0-9][A-Za-z0-9_-]*\Z")
# Never accidentally promote the known synthetic E05 acceptance plugin.
FORBIDDEN_TEST_APP_IDS = frozenset({
    "asdk_app_6ad412c004808191a27b70a8aceb8ac7",  # synthetic E05
    "asdk_app_6ad3cf00e45c81918892e94fdcbf4a2e",  # private MCP pilot
})
ALLOWED_CHANNELS = {"private", "public"}


def _json(data: dict) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _manifest(version: str, channel: str) -> dict:
    manifest = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": "meu-artigo",
        "version": version,
        "description": "Assistente científico para elaborar e acompanhar artigos com rastreabilidade, método C.A.D.A. e sete decisões humanas.",
        "author": {"name": "Rebson Mendes"},
        "license": "Apache-2.0",
        "repository": "https://github.com/rebsonm/MeuArtigoSkill",
        "extensions": {
            "com.openai": {
                "interface": {
                    "displayName": "Meu Artigo",
                    "shortDescription": "Pesquisa científica rastreável",
                    "longDescription": "Organize artigos, tarefas C.A.D.A., evidências e decisões humanas. Cada pesquisador utiliza seu próprio Google Drive autorizado. O painel MCP não aprova decisões científicas nem comprova a sincronização do Drive.",
                    "developerName": "Rebson Mendes",
                    "category": "Productivity",
                    "capabilities": ["Interactive"],
                    "composerIcon": "./assets/icon.svg",
                    "logo": "./assets/icon.svg",
                    "defaultPrompt": [
                        "Quero iniciar um artigo no Meu Artigo usando minha própria conexão Google Drive, sem criar pastas duplicadas.",
                        "Mostre o painel do meu artigo com tarefas C.A.D.A., evidências, etapas e aprovações humanas verificadas.",
                        "Continue meu artigo a partir dos registros canônicos realmente disponíveis, sem inventar progresso."
                    ],
                }
            }
        },
    }
    if channel == "private":
        manifest["extensions"]["com.openai"]["apps"] = "./.app.json"
    return manifest


def inspect_candidate(path: Path, root: Path, channel: str) -> dict:
    """Fail closed on cross-channel references, version drift and bundle tampering."""
    if channel not in ALLOWED_CHANNELS:
        raise ValueError("CHANNEL_INVALID")
    with ZipFile(path) as archive:
        infos = archive.infolist()
        names = [member.filename for member in infos]
        if len(names) != len(set(names)) or len(names) > 3000:
            raise ValueError("ZIP_DUPLICATE_OR_OVERSIZED")
        for item in infos:
            member = Path(item.filename)
            if (item.is_dir() or member.is_absolute() or
                    any(part in ("..", ".") for part in member.parts) or
                    item.file_size > 20 * 1024 * 1024 or
                    (item.external_attr >> 16) & 0o170000 == 0o120000):
                raise ValueError("UNSAFE_ZIP_MEMBER")
        required = {
            "plugin.json",
            "assets/icon.svg",
            "skills/meu-artigo/SKILL.md",
            "skills/meu-artigo/VERSION",
            "skills/meu-artigo/BUNDLE_MANIFEST.json",
        }
        if not required.issubset(names):
            raise ValueError("PACKAGE_REQUIRED_FILES_MISSING")
        plugin = json.loads(archive.read("plugin.json"))
        expected = read_version(root)
        packed = archive.read("skills/meu-artigo/VERSION").decode("utf-8").strip()
        if plugin.get("name") != "meu-artigo" or plugin.get("version") != expected or packed != expected:
            raise ValueError("PLUGIN_SKILL_VERSION_DRIFT")
        skill_manifest = json.loads(archive.read("skills/meu-artigo/BUNDLE_MANIFEST.json"))
        if skill_manifest.get("version") != expected:
            raise ValueError("BUNDLE_MANIFEST_VERSION_DRIFT")
        hashes = skill_manifest.get("files")
        if not isinstance(hashes, dict) or not hashes:
            raise ValueError("BUNDLE_MANIFEST_INVALID")
        prefixed = {"skills/meu-artigo/" + key for key in hashes}
        present_skill = {name for name in names if name.startswith("skills/meu-artigo/")}
        if present_skill != prefixed | {"skills/meu-artigo/BUNDLE_MANIFEST.json"}:
            raise ValueError("SKILL_PAYLOAD_MISMATCH")
        for name, digest in hashes.items():
            if (not isinstance(digest, str) or
                    hashlib.sha256(archive.read("skills/meu-artigo/" + name)).hexdigest() != digest):
                raise ValueError("SKILL_MEMBER_CHECKSUM_MISMATCH")
        openai = plugin.get("extensions", {}).get("com.openai", {})
        if not isinstance(openai, dict):
            raise ValueError("OPENAI_EXTENSION_INVALID")
        if channel == "public":
            if ".app.json" in names or openai.get("apps") or "mcp.json" in names or ".mcp.json" in names:
                raise ValueError("PUBLIC_MCP_APP_REFERENCE_FORBIDDEN")
        else:
            if openai.get("apps") != "./.app.json" or ".app.json" not in names:
                raise ValueError("PRIVATE_APP_MAPPING_REQUIRED")
            mapping = json.loads(archive.read(".app.json"))
            apps = mapping.get("apps", {})
            if not isinstance(apps, dict) or len(apps) != 1:
                raise ValueError("PRIVATE_APP_MAPPING_INVALID")
            item = next(iter(apps.values()))
            app_id = item.get("id") if isinstance(item, dict) else None
            if (not isinstance(app_id, str) or not APP_ID_PATTERN.fullmatch(app_id)
                    or app_id in FORBIDDEN_TEST_APP_IDS):
                raise ValueError("PRIVATE_APP_NOT_PRODUCTION_VERIFIED")
        if any(path.startswith(("hooks/", ".github/", "tests/")) for path in names):
            raise ValueError("INTERNAL_FILES_IN_PLUGIN")
        return {
            "schema": "MEU_ARTIGO_PLUGIN_CANDIDATE_V1",
            "channel": channel,
            "source_version": expected,
            "files_checked": len(names),
            "scientific_validation": "NOT_ASSERTED",
            "mcp_live_acceptance": "NOT_ASSERTED",
            "public_directory_approval": "NOT_ASSERTED",
            "registered_app_live_verified": False,
            "installation_authorized": False,
            "status": "SOURCE_PACKAGE_CHECK_PASS",
        }


def build_candidate(root: Path, destination: Path, channel: str,
                    app_id: str | None = None) -> dict:
    if channel not in ALLOWED_CHANNELS:
        raise ValueError("CHANNEL_INVALID")
    if channel == "public" and app_id is not None:
        raise ValueError("PUBLIC_APP_REFERENCE_FORBIDDEN")
    if channel == "private" and (
        not isinstance(app_id, str) or not APP_ID_PATTERN.fullmatch(app_id)
        or app_id in FORBIDDEN_TEST_APP_IDS
    ):
        raise ValueError("PRIVATE_REQUIRES_VERIFIED_PRODUCTION_APP_ID")
    version = read_version(root)
    expected_name = "MeuArtigoChatGPT-" + channel + "-v" + version + ".zip"
    if destination.name != expected_name:
        raise ValueError("OUTPUT_FILENAME_MISMATCH")
    with tempfile.TemporaryDirectory(prefix="meuartigo-candidate-") as temp:
        skill_path = Path(temp) / ("MeuArtigoSkill-v" + version + ".zip")
        build_skill_zip(root, skill_path)
        with ZipFile(skill_path) as skill:
            files = {"skills/meu-artigo/" + name: skill.read(name)
                     for name in skill.namelist()}
    files["plugin.json"] = _json(_manifest(version, channel))
    files["assets/icon.svg"] = (root / "assets/icon.svg").read_bytes()
    if channel == "private":
        files[".app.json"] = _json({"apps": {"meu-artigo": {"id": app_id}}})
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_DEFLATED, compresslevel=9) as z:
        for name in sorted(files):
            entry = ZipInfo(name, FIXED_DATE)
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            z.writestr(entry, files[name], compress_type=ZIP_DEFLATED, compresslevel=9)
    report = inspect_candidate(destination, root, channel)
    report["sha256"] = hashlib.sha256(destination.read_bytes()).hexdigest()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--channel", choices=sorted(ALLOWED_CHANNELS), required=True)
    parser.add_argument("--app-id", default=None,
                        help="PRIVATE ONLY: a separately verified production app ID, never E05")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    root = args.repo.resolve()
    version = read_version(root)
    target = args.output or root / "dist" / (
        "MeuArtigoChatGPT-" + args.channel + "-v" + version + ".zip")
    try:
        outcome = build_candidate(root, target, args.channel, args.app_id)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(outcome, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
