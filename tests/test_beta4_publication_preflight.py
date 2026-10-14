"""Historical beta.4 publication preservation regressions.

This test intentionally checks the archived release notes, not the current VERSION.
"""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class HistoricalBeta4Tests(unittest.TestCase):
    def test_historical_release_remains_documented(self):
        notes=(ROOT/"docs/NOTAS-DA-VERSAO-0.9.0-beta.4.md").read_text(encoding="utf-8")
        changelog=(ROOT/"CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("v0.9.0-beta.4",notes)
        self.assertIn("## 0.9.0-beta.4 — 2026-10-11",changelog)
        self.assertIn("beta.4", (ROOT/"README.md").read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()
