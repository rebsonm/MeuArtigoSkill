"""Phase 6 Skill-package integrity regressions (fully offline).

Synthetic ZIPs and source snippets only; this is an engineering gate, not
scientific validation, publisher licensing or evidence of public release.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import bundle_dependency_audit as audit
import build_skill_bundle as bundle


def fake_source(root: Path):
    for name in bundle.ROOT_FILES:
        value = ("Apache License\n" if name == "LICENSE" else
                 "Meu Artigo\n" if name == "NOTICE" else "Fixture\n")
        (root / name).write_text(value, encoding="utf-8")
    (root / "VERSION").write_text(bundle.read_version(ROOT) + "\n", encoding="utf-8")
    for dirname in bundle.DIR_TYPES:
        (root / dirname).mkdir()
    (root / "SKILL.md").write_text(
        "---\nname: meu-artigo\ndescription: Test\n---\n"
        "[method](references/method.md)\n", encoding="utf-8")
    (root / "references/method.md").write_text("Synthetic method\n", encoding="utf-8")
    (root / "scripts/runtime.py").write_text(
        "from helper import transform\n"
        "from openpyxl import Workbook  # external, optional dependency\n"
        "def execute(): return transform()\n", encoding="utf-8")
    (root / "scripts/helper.py").write_text(
        "def transform(): return 'synthetic'\n", encoding="utf-8")


class Phase6PackageAuditTests(unittest.TestCase):
    def setUp(self):
        work = tempfile.TemporaryDirectory()
        self.addCleanup(work.cleanup)
        self.root = Path(work.name)
        fake_source(self.root)
        self.out = self.root / "dist" / (
            "MeuArtigoSkill-v" + bundle.read_version(ROOT) + ".zip")

    def test_valid_synthetic_bundle_has_closed_links_and_local_imports(self):
        manifest = bundle.package(self.root, self.out)
        self.assertTrue(manifest["installed_dependency_closure_checked"])
        self.assertFalse(manifest["scientific_quality_validated"])
        checked = bundle.verify_package(self.out)
        self.assertTrue(checked["installed_dependency_closure_checked"])
        with ZipFile(self.out) as archive:
            files = set(archive.namelist())
            self.assertIn("scripts/runtime.py", files)
            self.assertIn("scripts/helper.py", files)
            self.assertNotIn("tests/test_phase6_bundle_integrity.py", files)
            self.assertNotIn("scripts/bundle_dependency_audit.py", files)

    def test_source_only_local_dependency_cannot_enter_distribution(self):
        (self.root / "scripts/helper.py").unlink()
        (self.root / "scripts/runtime.py").write_text(
            "from other_private_helper import transform\n", encoding="utf-8")
        (self.root / "scripts/other_private_helper.py").write_text(
            "def transform(): return 'fixture'\n", encoding="utf-8")
        # This extra script is considered source-only by the allowlist.
        original = bundle.EXCLUDED_SCRIPT_NAMES
        try:
            bundle.EXCLUDED_SCRIPT_NAMES = original | {"other_private_helper.py"}
            with self.assertRaisesRegex(ValueError, "MISSING_LOCAL_PYTHON_DEPENDENCY"):
                bundle.package(self.root, self.out)
        finally:
            bundle.EXCLUDED_SCRIPT_NAMES = original
        self.assertFalse(self.out.exists())

    def test_missing_root_markdown_target_refuses_build_before_zip_creation(self):
        (self.root / "SKILL.md").write_text(
            "---\nname: meu-artigo\n---\n"
            "[missing](references/not-packaged.md)\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "MISSING_OR_UNSAFE_ENTRYPOINT_LINK"):
            bundle.package(self.root, self.out)
        self.assertFalse(self.out.exists())

    def test_parent_relative_entrypoint_link_is_not_eligible(self):
        result = audit.audit({"SKILL.md": b"[escape](../secret.md)\n"})
        self.assertTrue(any("MISSING_OR_UNSAFE_ENTRYPOINT_LINK" in x
                            for x in result["errors"]))

    def test_missing_bundled_python_dependency_is_detected_by_static_closure(self):
        result = audit.audit({
            "SKILL.md": b"---\nname: local\n---\n",
            "scripts/worker.py": b"import helper\n",
        }, local_source_modules={"helper", "worker"})
        self.assertTrue(any("MISSING_LOCAL_PYTHON_DEPENDENCY" in x
                            for x in result["errors"]))

    def test_optional_external_dependency_does_not_become_mandatory(self):
        result = audit.audit({
            "SKILL.md": b"---\nname: local\n---\n",
            "scripts/worker.py": b"from openpyxl import Workbook\n",
        }, local_source_modules={"worker"})
        self.assertEqual(result["errors"], [])
        self.assertFalse(result["external_optional_packages_independently_tested"])

    def test_syntax_error_in_installed_script_refuses_package(self):
        (self.root / "scripts/helper.py").write_text("def execute(\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "INVALID_INSTALLED_PYTHON"):
            bundle.package(self.root, self.out)
        self.assertFalse(self.out.exists())

    def test_verifier_rejects_zip_symlink_even_when_manifest_member_exists(self):
        self.out.parent.mkdir()
        with ZipFile(self.out, "w") as archive:
            archive.writestr(bundle.MANIFEST, b"{}")
            symbolic = ZipInfo("scripts/symlink.py")
            symbolic.create_system = 3
            symbolic.external_attr = (0o120777 << 16)
            archive.writestr(symbolic, "sensitive-local-file")
        with self.assertRaisesRegex(ValueError, "Unsafe, encrypted or oversized ZIP"):
            bundle.verify_package(self.out)

    def test_verifier_rejects_archive_with_more_than_3000_members(self):
        self.out.parent.mkdir()
        with ZipFile(self.out, "w", compression=ZIP_DEFLATED) as archive:
            archive.writestr(bundle.MANIFEST, "{}")
            for i in range(3000):
                archive.writestr("docs/%04d.md" % i, "")
        with self.assertRaisesRegex(ValueError, "Unsafe, encrypted or oversized ZIP"):
            bundle.verify_package(self.out)

    def test_verify_package_rechecks_entrypoint_links_even_if_hashes_rewritten(self):
        bundle.package(self.root, self.out)
        with ZipFile(self.out) as origin:
            payload = {name: origin.read(name) for name in origin.namelist()
                       if name != bundle.MANIFEST}
            manifest = json.loads(origin.read(bundle.MANIFEST))
        payload["SKILL.md"] = (
            b"---\nname: meu-artigo\n---\n"
            b"[unavailable](references/missing-in-archive.md)\n")
        manifest["files"]["SKILL.md"] = bundle.sha256(payload["SKILL.md"])
        with ZipFile(self.out, "w", compression=ZIP_DEFLATED) as dest:
            for name, content in payload.items():
                dest.writestr(name, content)
            dest.writestr(bundle.MANIFEST, json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "Broken Skill bundle closure"):
            bundle.verify_package(self.out)

    def test_reproducible_zip_with_dependency_verification(self):
        bundle.package(self.root, self.out)
        first = bundle.sha256(self.out.read_bytes())
        bundle.package(self.root, self.out)
        self.assertEqual(first, bundle.sha256(self.out.read_bytes()))


if __name__ == "__main__":
    unittest.main()
