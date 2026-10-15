"""Skill connection status must remain readable and honest."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

class PreflightPresentationTests(unittest.TestCase):
    def test_researcher_preflight_is_evidence_based(self):
        doc=(ROOT/"docs/CHATGPT.md").read_text(encoding="utf-8")
        self.assertIn("short, readable explanation rather than empty tables",doc)
        self.assertIn("NOT_VERIFIED",doc)
        self.assertIn("read-after-write",doc)
    def test_entrypoint_keeps_scientific_safeguards(self):
        s=(ROOT/"SKILL.md").read_text(encoding="utf-8")
        self.assertIn("DEC_ID",s)
        self.assertIn("GATE_ID",s)
        self.assertIn("GOOGLE_DRIVE_FIRST",s)
        self.assertIn("Use bullets",s)

if __name__=="__main__":unittest.main()
