"""Check user-facing diagnostics stay readable and the private icon hotfix is correctly described."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PreflightPresentationTests(unittest.TestCase):
    def test_no_blank_status_table_contract(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Use bullets, no empty tables", skill)
        guide = (ROOT / "docs" / "CHATGPT.md").read_text(encoding="utf-8")
        self.assertIn("avoid Markdown tables", guide)
        self.assertIn("not verified", guide.lower())

    def test_distinct_read_write_receipts_required(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        guide = (ROOT / "docs" / "CHATGPT.md").read_text(encoding="utf-8")
        self.assertIn("read does not establish", guide)
        self.assertIn("provider credits", guide)
        self.assertIn("scientific decisions", guide)

    def test_private_plugin_visual_hotfix_not_claimed_as_public_release(self):
        guide = (ROOT / "docs" / "CHATGPT.md").read_text(encoding="utf-8")
        self.assertIn("0.9.0-beta.5", guide)
        self.assertIn("scientific Skill remains **beta.4**", guide)
        self.assertIn("host-side", guide)
        self.assertIn("does **not** host an MCP Apps server", guide)


if __name__ == "__main__":
    unittest.main()
