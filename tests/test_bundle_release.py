"""Offline beta bundle checks. No scientific data or access tokens required."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_skill_bundle as pkg


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for filename in pkg.ROOT_FILES:
            dest = self.root / filename
            dest.write_text("MIT License\n" if filename == "LICENSE" else "test item\n",
                            encoding="utf-8")
        (self.root / "VERSION").write_text("0.8.0-beta.5\n", encoding="utf-8")
        for dirname in pkg.DIR_TYPES:
            (self.root / dirname).mkdir()
        (self.root / "scripts" / "minimal.py").write_text("print('ok')\n", encoding="utf-8")
        (self.root / "docs" / "guide.md").write_text("Safe installation guide\n", encoding="utf-8")
        self.output = self.root / "dist" / "MeuArtigoSkill-v0.8.0-beta.5.zip"

    def test_zip_preserves_root_entrypoint_and_license(self):
        m = pkg.package(self.root, self.output)
        self.assertEqual(m["version"], "0.8.0-beta.5")
        self.assertFalse(m["scientific_quality_validated"])
        with ZipFile(self.output) as z:
            self.assertIn("SKILL.md", z.namelist())
            self.assertIn("LICENSE", z.namelist())
            self.assertNotIn("dist/MeuArtigoSkill-v0.8.0-beta.5.zip", z.namelist())
        self.assertEqual(pkg.verify_package(self.output)["files"], m["files"])

    def test_checksum_file_is_real_digest(self):
        pkg.package(self.root, self.output)
        declared = (self.root / "dist" / "SHA256SUMS.txt").read_text().split()[0]
        actual = hashlib.sha256(self.output.read_bytes()).hexdigest()
        self.assertEqual(declared, actual)

    def test_second_build_is_bitwise_identical(self):
        pkg.package(self.root, self.output)
        first = pkg.sha256(self.output.read_bytes())
        pkg.package(self.root, self.output)
        self.assertEqual(first, pkg.sha256(self.output.read_bytes()))

    def test_cannot_include_source_pdf(self):
        (self.root / "docs" / "protected.pdf").write_bytes(b"restricted fixture")
        with self.assertRaisesRegex(ValueError, "Unrecognized file"):
            pkg.package(self.root, self.output)
        self.assertFalse(self.output.exists())

    def test_cannot_include_suspicious_file(self):
        (self.root / "scripts" / "secret.env").write_text("TOKEN=synthetic", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Unrecognized file"):
            pkg.list_sources(self.root)

    def test_symlink_is_rejected(self):
        target = self.root / "outside.pdf"
        target.write_bytes(b"synthetic")
        (self.root / "docs" / "linked.md").symlink_to(target)
        with self.assertRaisesRegex(ValueError, "Symlink"):
            pkg.list_sources(self.root)

    def test_missing_license_is_rejected(self):
        (self.root / "LICENSE").unlink()
        with self.assertRaisesRegex(ValueError, "LICENSE"):
            pkg.list_sources(self.root)

    def test_tampered_zip_member_fails_verification(self):
        pkg.package(self.root, self.output)
        with ZipFile(self.output, "a") as z:
            z.writestr("extra-secret.txt", "should not be distributed")
        with self.assertRaisesRegex(ValueError, "Manifest and packaged"):
            pkg.verify_package(self.output)

    def test_repo_has_beta_docs_and_no_embedded_private_corpus(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, "0.8.0-beta.5")
        self.assertIn("MIT License", (ROOT / "LICENSE").read_text(encoding="utf-8"))
        paths = [p.relative_to(ROOT).as_posix() for p in pkg.list_sources(ROOT)]
        self.assertIn("docs/PROTOCOLO-BETA-USUARIOS.md", paths)
        self.assertIn("SECURITY.md", paths)
        self.assertNotIn("tests/test_bundle_release.py", paths)
        self.assertFalse(any(p.endswith(".pdf") or ".env" in p for p in paths))


if __name__ == "__main__":
    unittest.main()
