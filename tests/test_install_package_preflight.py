"""Installation QA contract: sample archives are synthetic and contain no user data."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_install_package import diagnose


def make_zip(path: Path, files: dict[str, str]) -> None:
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as z:
        for name, value in files.items():
            z.writestr(name, value)


class InstallationArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.file = Path(self.tmp.name) / "distribution.zip"
        self.plugin_manifest = json.dumps({
            "name": "meu-artigo", "version": "0.9.0-beta.4",
            "extensions": {"com.openai": {"interface": {
                "logo": "./assets/icon.svg", "composerIcon": "./assets/icon.svg"
            }}},
        })
        self.entry = "---\nname: meu-artigo\ndescription: Research Skill\n---\n"

    def plugin(self, extra=None):
        content = {"plugin.json": self.plugin_manifest,
                   "skills/meu-artigo/SKILL.md": self.entry,
                   "assets/icon.svg": "<svg xmlns='http://www.w3.org/2000/svg'/>"}
        if extra:
            content.update(extra)
        make_zip(self.file, content)

    def test_valid_plugin_is_recognized(self):
        self.plugin()
        d = diagnose(self.file, "plugin")
        self.assertTrue(d["valid"])
        self.assertEqual(d["reason"], "PLUGIN_PACKAGE_OK")

    def test_valid_skill_is_recognized(self):
        make_zip(self.file, {"SKILL.md": self.entry, "VERSION": "0.9.0-beta.2"})
        d = diagnose(self.file, "skill")
        self.assertTrue(d["valid"])
        self.assertEqual(d["kind"], "SKILL")

    def test_skill_uploaded_as_plugin_gets_explanation(self):
        make_zip(self.file, {"SKILL.md": self.entry})
        d = diagnose(self.file, "plugin")
        self.assertEqual(d["reason"], "SKILL_NOT_PLUGIN")
        self.assertIn("Skills", d["next_step"])

    def test_plugin_uploaded_as_skill_gets_explanation(self):
        self.plugin()
        d = diagnose(self.file, "skill")
        self.assertEqual(d["reason"], "PLUGIN_NOT_SKILL")

    def test_github_source_archive_is_not_installable(self):
        make_zip(self.file, {
            "MeuArtigoSkill-fix-post-beta2-plugin-migration-20261011/SKILL.md": self.entry,
            "MeuArtigoSkill-fix-post-beta2-plugin-migration-20261011/VERSION": "0.9.0-beta.4",
            "MeuArtigoSkill-fix-post-beta2-plugin-migration-20261011/plugin/plugin.json": self.plugin_manifest,
        })
        d = diagnose(self.file, "plugin")
        self.assertFalse(d["valid"])
        self.assertEqual(d["kind"], "GITHUB_SOURCE")
        self.assertEqual(d["reason"], "SOURCE_ARCHIVE_NOT_INSTALLER")
        self.assertIn("Code", d["next_step"])

    def test_unwrapped_source_manifest_is_not_plugin(self):
        make_zip(self.file, {"plugin/plugin.json": self.plugin_manifest,
                             "SKILL-v1.md": self.entry})
        d = diagnose(self.file, "plugin")
        self.assertEqual(d["reason"], "MANIFEST_NESTED_IN_REPOSITORY")

    def test_corrupt_zip_fails_closed(self):
        self.file.write_text("I am not a ZIP archive", encoding="utf-8")
        self.assertFalse(diagnose(self.file)["valid"])
        self.assertEqual(diagnose(self.file)["reason"], "INVALID_OR_UNSAFE_ZIP")

    def test_missing_file_has_clear_diagnostic(self):
        self.assertEqual(diagnose(self.file)["reason"], "FILE_NOT_FOUND")

    def test_plugin_requires_a_skill_entry(self):
        make_zip(self.file, {"plugin.json": self.plugin_manifest})
        self.assertEqual(diagnose(self.file)["reason"], "MISSING_PACKAGED_SKILL")

    def test_plugin_requires_referenced_icon(self):
        make_zip(self.file, {"plugin.json": self.plugin_manifest,
                             "skills/meu-artigo/SKILL.md": self.entry})
        self.assertEqual(diagnose(self.file)["reason"], "MISSING_ICON_ASSET")

    def test_wrong_plugin_name_rejected(self):
        wrong = json.loads(self.plugin_manifest)
        wrong["name"] = "other-plugin"
        make_zip(self.file, {"plugin.json": json.dumps(wrong),
                             "skills/meu-artigo/SKILL.md": self.entry})
        self.assertEqual(diagnose(self.file)["reason"], "WRONG_PLUGIN_IDENTITY")

    def test_zip_path_escape_rejected(self):
        self.plugin({"../secret.txt": "nope"})
        self.assertEqual(diagnose(self.file)["reason"], "INVALID_OR_UNSAFE_ZIP")

    def test_cli_human_output_and_json(self):
        self.plugin()
        cmd = [sys.executable, str(ROOT / "scripts" / "check_install_package.py"),
               str(self.file), "--expect", "plugin"]
        plain = subprocess.run(cmd, capture_output=True, text=True, check=False)
        self.assertEqual(plain.returncode, 0, plain.stderr)
        self.assertIn("PASS", plain.stdout)
        structured = subprocess.run(cmd + ["--json"], capture_output=True,
                                    text=True, check=False)
        self.assertEqual(structured.returncode, 0, structured.stderr)
        self.assertEqual(json.loads(structured.stdout)["kind"], "PLUGIN")

    def test_actual_built_plugin_candidate_passes_preflight(self):
        from build_plugin_bundle import build
        from version_info import read_version
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / f"MeuArtigoPlugin-v{read_version(ROOT)}-candidate.zip"
            receipt = build(ROOT, output)
            self.assertTrue(output.is_file())
            self.assertEqual(receipt["version"], read_version(ROOT))
            result = diagnose(output, "plugin")
            self.assertTrue(result["valid"], result)
            self.assertEqual(result["kind"], "PLUGIN")

    def test_actual_built_skill_passes_preflight(self):
        from build_skill_bundle import package
        from version_info import read_version
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / f"MeuArtigoSkill-v{read_version(ROOT)}.zip"
            package(ROOT, output)
            result = diagnose(output, "skill")
            self.assertTrue(result["valid"], result)
            self.assertEqual(result["kind"], "SKILL")

    def test_cli_rejects_wrong_type_with_exit_2(self):
        make_zip(self.file, {"SKILL.md": self.entry})
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_install_package.py"),
             str(self.file), "--expect", "plugin"],
            capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("NOT READY", proc.stdout)


if __name__ == "__main__":
    unittest.main()
