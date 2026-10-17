"""Stage 17 pre-pilot privacy regression tests. Synthetic data only."""
from __future__ import annotations
from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import reference_audit as refs
import scientific_diagnostic as diag
import report_output_guard as guard
import fictional_method_projection as fictional


class PrePilotPrivacyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.marker = "FICTIONAL_RESTRICTED_SOURCE_2026_NOT_REAL"

    def test_reference_cli_whitelists_only_counts(self):
        full = {"finding_counts": {"BLOCK": 1, "REVIEW": 2},
                "source_report_status": "STALE",
                "findings": [{"claim_id": self.marker,
                              "evidence_id": self.marker}]}
        out = io.StringIO()
        with patch.object(refs, "audit", return_value=full):
            with redirect_stdout(out):
                self.assertEqual(refs.main([str(self.root)]), 0)
        data = json.loads(out.getvalue())
        self.assertEqual(data["status"], "HUMAN_REVIEW_REQUIRED")
        self.assertNotIn("finding_counts", data)
        # A private in-process summary remains available without stdout.
        aggregate = refs.public_console_summary(full)
        self.assertEqual(aggregate["finding_counts"]["BLOCK"], 1)
        self.assertEqual(aggregate["finding_counts"]["REVIEW"], 2)
        self.assertNotIn(self.marker, out.getvalue())
        self.assertFalse(data["semantic_support_proven"])

    def test_reference_exception_never_leaks_file_or_secret(self):
        err = io.StringIO()
        with patch.object(refs, "audit", side_effect=ValueError(self.marker)):
            with redirect_stderr(err):
                self.assertEqual(refs.main([str(self.root)]), 1)
        self.assertEqual(err.getvalue().strip(), "REFERENCE_AUDIT_ERROR: INPUT_OR_OUTPUT_BLOCKED")

    def test_diagnostic_stdout_is_safe_even_if_renderer_has_private_text(self):
        summary = {"counts": {
            "blocking_occurrences": 1, "review_occurrences": 2,
            "heuristic_advisory_occurrences": 3,
            "contextual_advisory_occurrences": 4,
            "strict_required_occurrences": 1}}
        out = io.StringIO()
        with patch.object(diag, "compose", return_value=summary), \
             patch.object(diag, "markdown", return_value=self.marker):
            with redirect_stdout(out):
                self.assertEqual(diag.main([str(self.root)]), 0)
        info = json.loads(out.getvalue())
        self.assertNotIn(self.marker, out.getvalue())
        self.assertEqual(info["technical_blockers"], 1)
        self.assertTrue(info["human_review_required"])
        self.assertFalse(info["scientific_quality_validated"])

    def test_diagnostic_exception_string_is_not_logged(self):
        err = io.StringIO()
        with patch.object(diag, "compose", side_effect=ValueError(self.marker)):
            with redirect_stderr(err):
                self.assertEqual(diag.main([str(self.root)]), 1)
        self.assertEqual(err.getvalue().strip(), "DIAGNOSTIC_ERROR: INPUT_OR_OUTPUT_BLOCKED")

    def test_fictional_cli_never_echoes_dynamic_projection(self):
        out = io.StringIO()
        with patch.object(fictional, "fictional_projection",
                          return_value={"untrusted": self.marker}):
            with redirect_stdout(out):
                self.assertEqual(fictional.main(["--action", "all"]), 0)
        view = json.loads(out.getvalue())
        self.assertNotIn(self.marker, out.getvalue())
        self.assertTrue(view["preview_contract"]["fictional_only"])
        self.assertFalse(view["fictional_method_dialogue"]["gate_approved"])

    def test_local_report_rejects_bearer_before_creating_folder(self):
        target = Path("98_Technical_Reports/review.md")
        with self.assertRaisesRegex(ValueError, "restricted"):
            guard.write_report(self.root, target,
                               "Bearer " + "SYNTHETIC_TOKEN_CHARACTERS_123456",
                               allowed_extensions=frozenset({".md"}))
        self.assertFalse((self.root / guard.REPORTS).exists())

    def test_local_report_rejects_known_sensitive_markers(self):
        target = Path("98_Technical_Reports/review.md")
        with self.assertRaisesRegex(ValueError, "restricted"):
            guard.write_report(self.root, target,
                               "SECRET_PRIVATE_SOURCE_123_SYNTHETIC_ONLY",
                               allowed_extensions=frozenset({".md"}))
        self.assertFalse((self.root / guard.REPORTS).exists())

    def test_local_report_owner_only_and_no_overwrite(self):
        target = Path("98_Technical_Reports/review.json")
        full = guard.write_report(self.root, target, '{"diagnostic":"advisory"}',
                                  allowed_extensions=frozenset({".json"}))
        self.assertEqual(stat.S_IMODE(full.stat().st_mode), 0o600)
        self.assertEqual(full.read_text(), '{"diagnostic":"advisory"}')
        with self.assertRaises(FileExistsError):
            guard.write_report(self.root, target, "CHANGED",
                               allowed_extensions=frozenset({".json"}))
        self.assertEqual(full.read_text(), '{"diagnostic":"advisory"}')

    def test_local_report_payload_and_null_limit(self):
        target = Path("98_Technical_Reports/review.json")
        for content in ["Z" * (guard.MAX_REPORT_BYTES+1), "A"+chr(0)+"B"]:
            with self.assertRaises(ValueError):
                guard.write_report(self.root, target, content,
                                   allowed_extensions=frozenset({".json"}))
        self.assertFalse((self.root / guard.REPORTS).exists())

    def test_unrelated_project_file_is_not_modified(self):
        other = self.root / "09_Claims_Ledger.csv"
        other.write_text("UNCHANGED\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            guard.write_report(self.root, Path("09_Claims_Ledger.csv"),
                               "ATTEMPTED",allowed_extensions=frozenset({".csv"}))
        self.assertEqual(other.read_text(), "UNCHANGED\n")

if __name__=="__main__":
    unittest.main()
