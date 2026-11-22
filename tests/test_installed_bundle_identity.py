"""Regression for T01/T02: test actual installed identity and mutated payloads."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_installed_bundle import verify


class InstalledBundleIdentityTests(unittest.TestCase):
    def test_valid_bundle_then_mismatched_icon_and_agent_metadata(self):
        with tempfile.TemporaryDirectory() as base:
            root = Path(base)
            data = {"agents/openai.yaml": b"agent: legitimate\n",
                    "assets/icon.svg": b"<svg></svg>",
                    "VERSION": b"1.0.0-rc.1\n"}
            for path, content in data.items():
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            manifest = {"schema_version": 2, "version": "1.0.0-rc.1",
                        "build_source_commit": "a"*40,
                        "source_verification": "CLEAN_GIT_CHECKOUT",
                        "files": {p: hashlib.sha256(v).hexdigest() for p,v in data.items()}}
            (root / "BUNDLE_MANIFEST.json").write_text(json.dumps(manifest))
            self.assertEqual(verify(root)["status"], "PASS")
            (root / "agents/openai.yaml").write_text("changed", encoding="utf-8")
            (root / "assets/icon.svg").write_text("<svg>changed</svg>", encoding="utf-8")
            failed = verify(root)
            self.assertEqual(failed["status"], "FAIL")
            self.assertEqual(failed["mismatched_files"], ["agents/openai.yaml", "assets/icon.svg"])
            self.assertTrue(failed["checks"]["expected_version_matches_executable"])

    def test_old_executable_version_rejected_even_with_consistent_old_manifest(self):
        with tempfile.TemporaryDirectory() as base:
            root = Path(base)
            (root / "VERSION").write_text("0.9.0-beta.6\n", encoding="utf-8")
            sha = hashlib.sha256((root/"VERSION").read_bytes()).hexdigest()
            (root / "BUNDLE_MANIFEST.json").write_text(json.dumps({
                "version": "0.9.0-beta.6", "files": {"VERSION": sha}}))
            result = verify(root)
            self.assertEqual(result["status"], "FAIL")
            self.assertFalse(result["checks"]["expected_version_matches_executable"])
            self.assertEqual(result["executable_version"], "0.9.0-beta.6")


if __name__ == "__main__":
    unittest.main()
