"""Adversarial privacy regression for external provenance exports.

All names, text, credentials and topics below are synthetic software fixtures,
never research data or external review records.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_provenance.py"


class ExternalExportPrivacyTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.mgmt = self.root / "00_Gestao_e_Continuidade"
        self.mgmt.mkdir()
        (self.mgmt / "PROJECT_CONFIG.json").write_text(
            json.dumps({"project_name": "SECRET_PROJECT_UNIQUE_47"}), encoding="utf-8"
        )
        # Synthetic software fixture illustrates why default private exports
        # MUST NOT be shared.
        with (self.mgmt / "02_Search_Log.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Search_ID", "Literal_query", "Status"])
            writer.writeheader()
            writer.writerow({"Search_ID": "SRCH-321", "Literal_query": "SECRET_SEARCH_UNIQUE_52",
                             "Status": "PLANNED"})
        self.manuscript = self.root / "05_Manuscrito/Versao_Canonica/approved.md"
        self.manuscript.parent.mkdir(parents=True)
        self.manuscript.write_text("# Safe document\nA structural non-scientific test fixture.\n",
                                   encoding="utf-8")

    def call(self, audience="PUBLIC", *extra):
        return subprocess.run([sys.executable, str(EXPORTER), str(self.root),
                               "--audience", audience, "--no-record-export-event",
                               *extra], capture_output=True, text=True, timeout=30)

    def packages(self):
        root = self.root / "06_Submissao/Arquivos_Finais"
        return sorted(root.glob("RO_CRATE_*.zip")) if root.is_dir() else []

    def manifest(self, **changes):
        obj = {
            "schema_version": 1, "audience": "COLLABORATIVE",
            "reviewed_by": "Human researcher",
            "reviewed_at": "2026-10-09T17:00:00-03:00",
            "review_scope": "Confidentiality and sharing permission checked on exact text",
            "files": [{"path": "05_Manuscrito/Versao_Canonica/approved.md",
                       "sha256": hashlib.sha256(self.manuscript.read_bytes()).hexdigest()}]
        }
        obj.update(changes)
        p = self.root / "approved.json"
        p.write_text(json.dumps(obj), encoding="utf-8")
        return "approved.json"

    def test_public_never_contains_project_content_even_if_internal_logs_exist(self):
        r = self.call()
        self.assertEqual(r.returncode, 0, r.stderr)
        with zipfile.ZipFile(self.packages()[0]) as z:
            names = z.namelist()
            all_text = "\n".join(z.read(n).decode("utf-8") for n in names)
            self.assertNotIn("SECRET_PROJECT_UNIQUE_47", all_text)
            self.assertNotIn("SECRET_SEARCH_UNIQUE_52", all_text)
            self.assertNotIn("PROJECT_CONFIG.json", all_text)
            self.assertNotIn("approved.md", all_text)
            self.assertNotIn("SEARCH", all_text)
            self.assertFalse(any("payload/" in n for n in names))
            self.assertIn('"audience": "PUBLIC"', all_text)

    def test_collaborative_without_explicit_manifest_is_metadata_only(self):
        r = self.call("COLLABORATIVE")
        self.assertEqual(r.returncode, 0, r.stderr)
        with zipfile.ZipFile(self.packages()[0]) as z:
            self.assertFalse(any("payload/" in x for x in z.namelist()))

    def test_collaborative_includes_only_exact_hash_approved_manuscript(self):
        manifest = self.manifest()
        r = self.call("COLLABORATIVE", "--approved-files-manifest", manifest)
        self.assertEqual(r.returncode, 0, r.stderr)
        with zipfile.ZipFile(self.packages()[0]) as z:
            names = z.namelist()
            content = "\n".join(z.read(n).decode("utf-8") for n in names)
            self.assertTrue(any(n.endswith("approved.md") for n in names))
            self.assertNotIn("SECRET_SEARCH_UNIQUE_52", content)
            self.assertNotIn("PROJECT_CONFIG.json", content)

    def test_changed_file_invalidates_human_review(self):
        manifest = self.manifest()
        self.manuscript.write_text("# Changed since approval\n", encoding="utf-8")
        r = self.call("COLLABORATIVE", "--approved-files-manifest", manifest)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("changed since human approval", r.stderr)
        self.assertFalse(self.packages())

    def test_public_does_not_accept_manual_file_exceptions(self):
        manifest = self.manifest()
        r = self.call("PUBLIC", "--approved-files-manifest", manifest)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(self.packages())

    def test_external_export_cannot_include_protected_fulltext(self):
        for audience in ("PUBLIC", "COLLABORATIVE"):
            r = self.call(audience, "--include-fulltext", "--confirm-rights-review")
            self.assertNotEqual(r.returncode, 0)
        self.assertFalse(self.packages())

    def test_fake_human_attestation_is_rejected(self):
        manifest = self.manifest(reviewed_by="ChatGPT")
        r = self.call("COLLABORATIVE", "--approved-files-manifest", manifest)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(self.packages())

    def test_sensitive_content_fails_closed(self):
        self.manuscript.write_text("TOKEN: a-real-looking-secret\nmail@example.org\n",
                                   encoding="utf-8")
        manifest = self.manifest()
        r = self.call("COLLABORATIVE", "--approved-files-manifest", manifest)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Possible personal data or credential", r.stderr)
        self.assertFalse(self.packages())

    def test_unsafe_file_path_cannot_be_authorized(self):
        manifest = self.manifest(files=[{"path": "00_Gestao_e_Continuidade/PROJECT_CONFIG.json",
                                         "sha256": "0"*64}])
        r = self.call("COLLABORATIVE", "--approved-files-manifest", manifest)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(self.packages())

    def test_symlinked_canonical_file_does_not_bypass_filter(self):
        private_file = self.root / "private.md"
        private_file.write_text("PRIVATE", encoding="utf-8")
        self.manuscript.unlink()
        self.manuscript.symlink_to(private_file)
        manifest = self.manifest(files=[{"path": "05_Manuscrito/Versao_Canonica/approved.md",
                                         "sha256": hashlib.sha256(private_file.read_bytes()).hexdigest()}])
        r = self.call("COLLABORATIVE", "--approved-files-manifest", manifest)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(self.packages())


if __name__ == "__main__":
    unittest.main()
