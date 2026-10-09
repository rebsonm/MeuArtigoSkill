"""Offline regression for minimal GitHub Actions release/security invariants."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CIWorkflowSafetyTests(unittest.TestCase):
    def setUp(self):
        self.ci = (ROOT / ".github/workflows/release-audit.yml").read_text(encoding="utf-8")
        self.release = (ROOT / ".github/workflows/publish-beta.yml").read_text(encoding="utf-8")
        self.quality = (ROOT / ".github/workflows/scientific-quality-calibration.yml").read_text(encoding="utf-8")

    def test_third_party_actions_are_immutable_sha_pinned(self):
        for name, body in [
            ("Release audit", self.ci),
            ("Beta publisher", self.release),
            ("Scientific metadata calibration", self.quality),
        ]:
            actions = re.findall(r"(?m)^\s*(?:-\s*)?uses:\s*(\S+)", body)
            self.assertTrue(actions, f"{name}: no pinned actions")
            for action in actions:
                self.assertRegex(action, r"^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+@[a-f0-9]{40}$",
                                 f"{name} has mutable action ref {action!r}")

    def test_audit_retains_required_job_name_and_read_only_permission(self):
        self.assertIn("  audit:", self.ci)
        self.assertIn("contents: read", self.ci)
        self.assertNotIn("contents: write", self.ci)
        self.assertNotIn("gh release create", self.ci)
        self.assertIn("pull_request:", self.ci)
        self.assertIn("branches: [main]", self.ci)
        self.assertIn("audit_public_docs.py", self.ci)

    def test_public_release_requires_manual_trigger_and_new_tag(self):
        self.assertIn("  workflow_dispatch:", self.release)
        self.assertNotRegex(self.release, r"(?m)^\s{2}(?:push|pull_request):")
        self.assertIn("github.ref == 'refs/heads/main'", self.release)
        self.assertIn('"$ACK" != "publish-beta"', self.release)
        self.assertIn("gh release create", self.release)
        self.assertIn("already exists and must not be replaced", self.release)
        self.assertIn("Tag $TAG exists; refusing to move or overwrite it", self.release)
        self.assertIn("contents: write", self.release)
        self.assertIn("NOTAS-DA-VERSAO-", self.release)
        self.assertNotRegex(self.release, r"0\.8\.0-beta\.\d+")

    def test_calibration_metadata_is_not_treated_as_validated_science(self):
        self.assertIn("scientific_quality_validated=false", self.quality)
        self.assertIn("contents: read", self.quality)


if __name__ == "__main__":
    unittest.main()
