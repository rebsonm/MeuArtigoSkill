"""Final engineering candidate gate; disposable Git and package fixtures only.

Passing these checks verifies software wiring and artifact provenance,
NOT a real researcher, a scientific method, manuscript or platform account.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_skill_bundle as bundle
import test_phase6_bundle_integrity as synthetic_bundle


class Phase6FinalCandidateAuditTests(unittest.TestCase):
    def setUp(self):
        ctx = tempfile.TemporaryDirectory()
        self.addCleanup(ctx.cleanup)
        self.root = Path(ctx.name)
        synthetic_bundle.fake_source(self.root)
        self.archive = self.root / "dist" / (
            "MeuArtigoSkill-v" + bundle.read_version(ROOT) + ".zip")

    def git(self, *args):
        result = subprocess.run(["git", "-C", str(self.root), *args],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def committed_fixture(self):
        self.git("init", "-q")
        self.git("remote", "add", "origin", bundle.REPOSITORY + ".git")
        self.git("add", "-A")
        self.git("-c", "user.name=Synthetic Fixture",
                 "-c", "user.email=example@example.invalid",
                 "commit", "-qm", "synthetic baseline")
        return self.git("rev-parse", "HEAD")

    def test_tracked_unchanged_bundle_sources_can_be_attributed_to_git(self):
        sha = self.committed_fixture()
        attestation = bundle.source_provenance(self.root)
        self.assertEqual(attestation["build_source_commit"], sha)
        self.assertEqual(attestation["source_verification"], "CLEAN_GIT_CHECKOUT")
        manifest = bundle.package(self.root, self.archive)
        self.assertEqual(manifest["build_source_commit"], sha)
        self.assertEqual(manifest["source_verification"], "CLEAN_GIT_CHECKOUT")

    def test_untracked_allowlisted_file_must_not_claim_existing_git_commit(self):
        self.committed_fixture()
        (self.root / "docs" / "new_untracked.md").write_text(
            "Synthetic extra allowed Markdown\n", encoding="utf-8")
        result = bundle.source_provenance(self.root)
        self.assertIsNone(result["build_source_commit"])
        self.assertEqual(result["source_verification"], "UNVERIFIED")
        manifest = bundle.package(self.root, self.archive)
        self.assertIn("docs/new_untracked.md", manifest["files"])
        self.assertIsNone(manifest["build_source_commit"])
        self.assertEqual(manifest["source_verification"], "UNVERIFIED")
        self.assertEqual(bundle.verify_package(self.archive)["files"],
                         manifest["files"])

    def test_modified_tracked_file_is_not_attested_as_clean_commit(self):
        self.committed_fixture()
        (self.root / "scripts" / "helper.py").write_text(
            "def transform(): return 'modified fixture'\n", encoding="utf-8")
        attestation = bundle.source_provenance(self.root)
        self.assertIsNone(attestation["build_source_commit"])
        self.assertEqual(attestation["source_verification"], "UNVERIFIED")

    def test_untracked_out_of_distribution_build_output_does_not_change_provenance(self):
        sha = self.committed_fixture()
        (self.root / "dist").mkdir()
        (self.root / "dist" / "temporary_note.txt").write_text(
            "Not distributed\n", encoding="utf-8")
        attestation = bundle.source_provenance(self.root)
        self.assertEqual(attestation["build_source_commit"], sha)
        self.assertEqual(attestation["source_verification"], "CLEAN_GIT_CHECKOUT")

    def test_current_development_zip_bootstraps_core_commands_after_extraction(self):
        """Exercises the actual built Skill archive, not the Git source tree."""
        self.archive = self.root / (
            "MeuArtigoSkill-v" + bundle.read_version(ROOT) + ".zip")
        manifest = bundle.package(ROOT, self.archive)
        self.assertEqual(manifest["entrypoint"], "SKILL.md")
        self.assertFalse(manifest["scientific_quality_validated"])
        self.assertTrue(manifest["installed_dependency_closure_checked"])
        with ZipFile(self.archive) as z:
            self.assertEqual(set(z.namelist()),
                             set(manifest["files"]) | {bundle.MANIFEST})
            self.assertNotIn("scripts/build_skill_bundle.py", z.namelist())
            self.assertNotIn("scripts/quality_benchmark.py", z.namelist())
            self.assertNotIn("tests/test_phase6_final_candidate_audit.py",
                             z.namelist())
            target = self.root / "unpacked"
            target.mkdir()
            z.extractall(target)

        for script in (
            "init_project.py",
            "next_step_router.py",
            "update_cada_continuity.py",
            "native_chat_dashboard.py",
            "validate_project.py",
        ):
            with self.subTest(script=script):
                p = subprocess.run(
                    [sys.executable, str(target / "scripts" / script), "--help"],
                    cwd=target, capture_output=True, text=True, timeout=20,
                )
                self.assertEqual(p.returncode, 0, p.stderr[-1500:])
                self.assertIn("usage:", p.stdout.lower())
        self.assertEqual(
            (target / "VERSION").read_text(encoding="utf-8").strip(),
            bundle.read_version(ROOT),
        )

    def test_official_version_and_development_version_are_separate_files(self):
        official = (ROOT / "OFFICIAL_SKILL_RELEASE").read_text().strip()
        source_version = (ROOT / "VERSION").read_text().strip()
        self.assertTrue(official)
        self.assertTrue(source_version)
        self.assertNotEqual(
            ROOT / "OFFICIAL_SKILL_RELEASE", ROOT / "VERSION",
        )
        # Packaging a development candidate is not authority to alter either.
        original = ((ROOT / "OFFICIAL_SKILL_RELEASE").read_bytes(),
                    (ROOT / "VERSION").read_bytes())
        bundle.package(ROOT, self.archive)
        self.assertEqual(
            ((ROOT / "OFFICIAL_SKILL_RELEASE").read_bytes(),
             (ROOT / "VERSION").read_bytes()), original,
        )


if __name__ == "__main__":
    unittest.main()
