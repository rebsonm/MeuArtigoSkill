"""Offline adversarial tests of public-doc checks; software fixtures only."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import audit_public_docs as audit


class PublicDocumentationAuditTests(unittest.TestCase):
    def test_repository_has_no_flagged_public_sources(self):
        result = audit.inspect(ROOT)
        self.assertGreater(result["documents"], 20)
        self.assertEqual(result["issues"], [], "\n".join(result["issues"]))

    def test_detects_old_private_roadmap_reference(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "SECURITY.md").write_text("See RT-09 control.", encoding="utf-8")
            issues = audit.inspect(root)["issues"]
            self.assertTrue(any("private remediation ticket" in x for x in issues))

    def test_detects_private_collection_in_researcher_docs(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "docs").mkdir()
            (root / "docs/guide.md").write_text("PPGA methodological inventory", encoding="utf-8")
            self.assertTrue(audit.inspect(root)["issues"])

    def test_detects_secret_signature_without_disclosing_secret(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            token = "ghp_" + "A" * 36
            (root / "NOTICE").write_text("Token: " + token, encoding="utf-8")
            items = audit.inspect(root)["issues"]
            self.assertTrue(items)
            self.assertNotIn(token, "\n".join(items))

    def test_excludes_scripts_where_controls_are_legitimate(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "scripts").mkdir()
            (root / "scripts/anything.py").write_text("RT-09 GATE-001\n", encoding="utf-8")
            self.assertEqual(audit.inspect(root)["issues"], [])

    def test_includes_new_root_markdown_and_github_templates(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "NEW_DOCUMENT.md").write_text("RT-02\n", encoding="utf-8")
            (root / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True)
            (root / ".github" / "ISSUE_TEMPLATE" / "prompt.md").write_text("RT-03\n", encoding="utf-8")
            self.assertEqual(len(audit.inspect(root)["issues"]), 2)


if __name__ == "__main__":
    unittest.main()
