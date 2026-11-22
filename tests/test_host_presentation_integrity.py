"""T02 acceptance: original payload hashes plus separately attested host presentation.

No arbitrary mismatch is permitted. Operator review is explicit, never inferred
from platform-looking bytes, and anchored to an independently pinned manifest.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_installed_bundle import draft_host_receipt, verify


class PlatformManagedPresentationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "installed"
        self.root.mkdir()
        self.items = {
            "VERSION": b"1.0.0-rc.1\n",
            "scripts/core.py": b"print('Original, immutable logic')\n",
            "agents/openai.yaml": b'interface:\n  display_name: "Meu Artigo"\n',
            "assets/icon.svg": b'<svg xmlns="http://www.w3.org/2000/svg"></svg>',
        }
        for name, data in self.items.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.manifest = {
            "version": "1.0.0-rc.1", "build_source_commit": "a" * 40,
            "files": {n: hashlib.sha256(v).hexdigest()
                      for n, v in self.items.items()},
        }
        self.mf = self.root / "BUNDLE_MANIFEST.json"
        self.mf.write_text(json.dumps(self.manifest))
        self.pin = hashlib.sha256(self.mf.read_bytes()).hexdigest()
        self.receipt = self.base / "operator-reviewed-receipt.json"

    def transform(self):
        (self.root / "agents/openai.yaml").write_text(
            "interface:\n  display_name: Meu Artigo\nhost_policy:\n  enforced: true\n")
        (self.root / "assets/icon.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg"><rect width="20" height="20"/></svg>')

    def approved_receipt(self):
        draft = draft_host_receipt(self.root)
        self.assertFalse(draft["reviewed"])
        self.assertEqual(len(draft["transformed_assets"]), 2)
        for x in draft["transformed_assets"]:
            x["reviewed"] = True
        draft["reviewed"] = True
        draft["reviewer"] = "TEST OPERATOR"
        draft["review_evidence"] = "Test operator compared both post-save host asset bodies with packaged originals."
        draft["host_save_readback_evidence"] = "Test fixture: save and independent readback on the same local installation."
        self.receipt.write_text(json.dumps(draft))
        return draft

    def test_exact_original_bundle_passes_without_attestation(self):
        r = verify(self.root)
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["integrity_mode"], "ALL_BUNDLE_BYTES_EXACT")

    def test_host_rewrites_require_explicit_receipt_and_pin(self):
        self.transform()
        strict = verify(self.root)
        self.assertEqual(strict["status"], "FAIL")
        self.assertEqual(strict["mismatched_files"],
                         ["agents/openai.yaml", "assets/icon.svg"])
        draft = draft_host_receipt(self.root)
        self.assertFalse(draft["reviewed"])
        self.receipt.write_text(json.dumps(draft))
        self.assertEqual(verify(self.root, host_receipt=self.receipt,
                                expected_manifest_sha256=self.pin)["status"], "FAIL")
        self.approved_receipt()
        self.assertEqual(verify(self.root, host_receipt=self.receipt)["status"], "FAIL")
        good = verify(self.root, host_receipt=self.receipt,
                      expected_manifest_sha256=self.pin)
        self.assertEqual(good["status"], "PASS", good)
        self.assertEqual(good["integrity_mode"], "CORE_EXACT_HOST_PRESENTATION_ATTESTED")
        self.assertEqual(good["host_reviewed_presentation_files"],
                         ["agents/openai.yaml", "assets/icon.svg"])
        self.assertEqual(good["payload_count"], 4)
        self.assertEqual(good["mismatched_files"],
                         ["agents/openai.yaml", "assets/icon.svg"])

    def test_unrelated_core_change_can_never_be_attested(self):
        self.transform()
        self.approved_receipt()
        (self.root / "scripts/core.py").write_bytes(b"print('malicious')\n")
        r = verify(self.root, host_receipt=self.receipt,
                   expected_manifest_sha256=self.pin)
        self.assertEqual(r["status"], "FAIL")
        self.assertIn("scripts/core.py", r["unresolved_mismatches"])

    def test_reviewed_host_asset_modified_after_receipt_fails(self):
        self.transform()
        self.approved_receipt()
        (self.root / "agents/openai.yaml").write_text("interface:\n  display_name: attacker\n")
        r = verify(self.root, host_receipt=self.receipt,
                   expected_manifest_sha256=self.pin)
        self.assertEqual(r["status"], "FAIL")
        self.assertEqual(r["host_presentation_receipt_status"],
                         "HOST_PRESENTATION_CHANGED_AFTER_REVIEW")

    def test_unsafe_svg_not_accepted_even_if_reviewed(self):
        self.transform()
        (self.root / "assets/icon.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>')
        self.approved_receipt()
        r = verify(self.root, host_receipt=self.receipt,
                   expected_manifest_sha256=self.pin)
        self.assertEqual(r["status"], "FAIL")
        self.assertEqual(r["host_presentation_receipt_status"], "HOST_ICON_UNSAFE_XML")

    def test_wrong_manifest_pin_does_not_allow_attestation(self):
        self.transform()
        self.approved_receipt()
        r = verify(self.root, host_receipt=self.receipt,
                   expected_manifest_sha256="0" * 64)
        self.assertEqual(r["status"], "FAIL")
        self.assertEqual(r["host_presentation_receipt_status"], "BUNDLE_MANIFEST_NOT_PINNED")

    def test_external_receipt_mandatory(self):
        self.transform()
        receipt = self.approved_receipt()
        internal = self.root / "host_receipt.json"
        internal.write_text(json.dumps(receipt))
        r = verify(self.root, host_receipt=internal,
                   expected_manifest_sha256=self.pin)
        self.assertEqual(r["status"], "FAIL")
        self.assertEqual(r["host_presentation_receipt_status"],
                         "RECEIPT_MUST_BE_OUTSIDE_SKILL")


if __name__ == "__main__":
    unittest.main()
