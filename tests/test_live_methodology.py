"""Offline contract checks for the installed public GitHub consultation router."""
import sys
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import consult_live_methodology as live

SHA = "a" * 40


def _method(*args, **kwargs):
    return {"status": "RETRIEVED_WITH_REVIEW_REQUIRED", "card_hits": [
        {"title": "Case study", "excerpt": "Guidance"}], "pdf_hits": []}


def _leads(*args, **kwargs):
    return {"status": "BIBLIOGRAPHIC_LEADS_ONLY", "hits": [
        {"source_id": "SRC-0001", "citation_grade": "P_BIBLIOGRAPHIC_PROSPECTING_NOT_SOURCE_EVIDENCE"}]}


class LiveConsultationTests(unittest.TestCase):
    def test_live_main_resolved_and_pinned_for_both_readers(self):
        with patch.object(live.methodology, "query", side_effect=_method) as method, \
             patch.object(live.registry, "query", side_effect=_leads) as lead:
            result = live.query("qualitative case study", head_resolver=lambda: SHA)
        self.assertTrue(result["current_main_verified"])
        self.assertEqual(result["commit"], SHA)
        self.assertEqual(method.call_args.kwargs["ref"], SHA)
        self.assertEqual(lead.call_args.kwargs["ref"], SHA)
        self.assertFalse(result["scientific_gate_approved"])
        self.assertFalse(result["private_sources_accessed"])

    def test_head_failure_uses_declared_immutable_fallback(self):
        with patch.object(live.methodology, "query", side_effect=_method), \
             patch.object(live.registry, "query", side_effect=_leads):
            result = live.query("research design", head_resolver=lambda: (_ for _ in ()).throw(OSError("offline")))
        self.assertFalse(result["current_main_verified"])
        self.assertEqual(result["commit"], live.FALLBACK_SNAPSHOT)
        self.assertIn("FALLBACK", result["commit_resolution"])

    def test_invalid_commit_rejected_before_fetch(self):
        with patch.object(live.methodology, "query") as method:
            with self.assertRaisesRegex(ValueError, "IMMUTABLE_GITHUB_COMMIT_REQUIRED"):
                live.query("methodology", ref="main")
            method.assert_not_called()

    def test_registry_results_are_not_claimed_as_evidence(self):
        with patch.object(live.methodology, "query", return_value={
            "status": "NO_MATCH", "card_hits": [], "pdf_hits": []}), \
             patch.object(live.registry, "query", side_effect=_leads):
            result = live.query("grounded theory", ref=SHA)
        self.assertEqual(result["status"], "BIBLIOGRAPHIC_LEADS_ONLY")
        self.assertFalse(result["scientific_quality_validated"])

    def test_question_invalid_no_requests(self):
        with patch.object(live.methodology, "query") as method:
            with self.assertRaisesRegex(ValueError, "QUESTION_INVALID"):
                live.query(" ", ref=SHA)
            method.assert_not_called()

    def test_technical_outage_does_not_approve_gates(self):
        with patch.object(live.methodology, "query", return_value={
            "status": "PARTIAL_OR_UNAVAILABLE", "card_hits": [], "pdf_hits": []}), \
             patch.object(live.registry, "query", side_effect=OSError("offline")):
            result = live.query("survey research", ref=SHA)
        self.assertEqual(result["status"], "PARTIAL_OR_UNAVAILABLE")
        self.assertFalse(result["scientific_gate_approved"])


if __name__ == "__main__":
    unittest.main()
