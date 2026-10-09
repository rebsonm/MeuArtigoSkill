"""Behavioral quality benchmarking checks using a real published reference set.

Candidate values are constructed only inside disposable unit-test fixtures.
They are NOT represented as empirical research or actual model outputs.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import quality_benchmark as q


class QualityBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference_path = q.DEFAULT_REFERENCE
        cls.reference = q.reference_cases(q.read_json(cls.reference_path))

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def candidate_file(self, data, name="candidate.json"):
        file = self.root / name
        q.write_json(file, data)
        return file

    def test_real_publication_reference_is_well_formed(self):
        self.assertEqual(len(self.reference), 4)
        self.assertEqual(self.reference["ai_diffusion_review"]["reported_counts"]["included"], 73)
        self.assertEqual(self.reference["governance_integration_review"]["reported_counts"]["included"], 67)
        self.assertEqual(self.reference["brazilian_governance_integrative_review"]["reported_counts"]["included"], 13)
        self.assertEqual(self.reference["brazilian_governance_integrative_review"]["reported_counts"]["identified"], 400)

    def test_derived_stage_totals_are_reconciled_without_adding_records(self):
        flow = self.reference["ai_diffusion_review"]["derived_counts"]
        self.assertEqual(flow["identified"], 248)
        self.assertEqual(flow["duplicates_removed"], 82)
        self.assertEqual(flow["screened_excluded"], 49)
        self.assertEqual(flow["full_text_excluded"], 44)
        self.assertNotIn("screened", self.reference["governance_integration_review"]["reported_counts"])

    def test_inconsistent_published_reference_is_rejected(self):
        sample = q.read_json(self.reference_path)
        sample["cases"][0]["derived_counts"]["duplicates_removed"] = 12
        with self.assertRaises(ValueError):
            q.reference_cases(sample)

    def test_empty_candidate_has_zero_coverage_not_fake_success(self):
        candidate = self.candidate_file({"schema_version": 1, "cases": []})
        result = q.evaluate(self.reference_path, candidate, workspace=self.root)
        self.assertEqual(result["submitted_cases"], 0)
        self.assertIsNone(result["metrics"]["identity"]["doi_exact_rate_on_observed"])
        self.assertEqual(result["metrics"]["stage_counts"]["coverage"], 0)
        self.assertEqual(result["semantic_adjudication"]["status"], "NOT_EVALUATED")

    def test_real_reference_comparison_detects_arithmetic_mismatch(self):
        candidate = self.candidate_file({"schema_version": 1, "cases": [
            {"case": "ai_diffusion_review", "title": "AI adoption and diffusion in public administration: A systematic literature review and future research agenda",
             "doi": "10.1016/j.giq.2022.101774",
             "stage_counts": {"database_records": 221, "other_records": 27, "identified": 248,
                              "duplicates_removed": 82, "screened": 166,
                              "screened_excluded": 48, "full_text_reviewed": 117, "full_text_excluded": 44, "included": 73}}
        ]})
        result = q.evaluate(self.reference_path, candidate, workspace=self.root)
        metrics = result["metrics"]
        self.assertEqual(metrics["identity"]["doi_exact"], 1)
        self.assertEqual(metrics["stage_counts"]["observed"], 9)
        self.assertEqual(metrics["stage_counts"]["correct"], 8)
        self.assertEqual(metrics["stage_counts"]["inconsistent_cases"][0]["equation"], "full_text_reviewed")

    def test_doi_mutation_is_not_counted_as_correct(self):
        candidate = self.candidate_file({"schema_version": 1, "cases": [
            {"case": "governance_integration_review", "doi": "10.9999/not-this-article", "title": "Other publication"}
        ]})
        result = q.evaluate(self.reference_path, candidate, workspace=self.root)
        self.assertEqual(result["metrics"]["identity"]["doi_exact"], 0)
        self.assertEqual(result["metrics"]["identity"]["observed"], 1)

    def test_unscored_claims_are_not_misrepresented_as_verified(self):
        candidate = self.candidate_file({"schema_version": 1, "cases": [],
                                         "claims": [{"claim_id": "claim-1", "label": "SUPPORTED"}]})
        result = q.evaluate(self.reference_path, candidate, workspace=self.root)
        self.assertIsNone(result["semantic_adjudication"]["accuracy"])
        self.assertEqual(result["semantic_adjudication"]["adjudicated"], 0)

    def test_external_labels_are_not_treated_as_authenticated(self):
        candidate = self.candidate_file({"schema_version": 1, "cases": [],
                                         "claims": [{"claim_id": "claim-1", "label": "SUPPORTED"}]})
        gold = self.candidate_file({"schema_version": 1, "reviewer_reference": "Temporary test reviewer label",
                                    "claims": [{"claim_id": "claim-1", "label": "NOT_SUPPORTED"}]}, "annotations.json")
        result = q.evaluate(self.reference_path, candidate, workspace=self.root, adjudications=gold)
        self.assertEqual(result["semantic_adjudication"]["status"], "ANNOTATIONS_PROVIDED_UNAUTHENTICATED")
        self.assertEqual(result["semantic_adjudication"]["accuracy"], 0)

    def test_locators_require_real_local_source(self):
        candidate = self.candidate_file({"schema_version": 1, "cases": [
            {"case": "ai_diffusion_review", "locators": [
                {"claim_id": "claim-1", "source_path": "missing.txt",
                 "supporting_locator": "Several independent sources reported materially divergent evidence"}
            ]}
        ]})
        result = q.evaluate(self.reference_path, candidate, workspace=self.root)
        self.assertEqual(result["metrics"]["locators"]["observed"], 1)
        self.assertEqual(result["metrics"]["locators"]["matched"], 0)
        self.assertEqual(result["metrics"]["locators"]["pending"], 1)

    def test_local_locator_match_does_not_verify_semantics(self):
        (self.root / "source.txt").write_text(
            "The conceptual model was evaluated using two separate administrative samples.\n", encoding="utf-8")
        candidate = self.candidate_file({"schema_version": 1, "cases": [
            {"case": "ai_diffusion_review", "locators": [
                {"claim_id": "claim-1", "source_path": "source.txt",
                 "supporting_locator": '"The conceptual model was evaluated using two separate administrative samples."'}
            ]}
        ]})
        result = q.evaluate(self.reference_path, candidate, workspace=self.root)
        self.assertEqual(result["metrics"]["locators"]["matched"], 1)
        self.assertEqual(result["cases"][0]["locators"][0]["semantic_support"], "NOT_ADJUDICATED")

    def test_offline_pilot_records_inability_to_verify(self):
        result = q.pilot(self.reference_path, offline=True)
        self.assertEqual(result["verified_metadata"], 0)
        self.assertEqual(result["unverified_metadata"], 4)
        self.assertFalse(any(x["claims_scientifically_adjudicated"] for x in result["results"]))

    def test_pilot_mocked_provider_verification_is_not_semantic_validation(self):
        def fetch(provider, doi, _):
            row = next(x for x in self.reference.values() if x["doi"] == doi)
            if provider == "crossref":
                return {"status": "FOUND", "data": {"DOI": doi, "title": [row["title"]],
                      "published": {"date-parts": [[row["published_year"]]]}}}
            return {"status": "FOUND", "data": {"doi": "https://doi.org/" + doi,
                "display_name": row["title"], "publication_year": row["published_year"],
                "is_retracted": False}}
        result = q.pilot(self.reference_path, fetcher=fetch)
        self.assertEqual(result["verified_metadata"], 4)
        self.assertEqual(result["results"][0]["interpretation"], "BIBLIOGRAPHIC_IDENTITY_ONLY")

    def test_wrong_reference_hash_blocks_comparison(self):
        candidate = self.candidate_file({"schema_version": 1, "reference_sha256": "0" * 64, "cases": []})
        with self.assertRaises(ValueError):
            q.evaluate(self.reference_path, candidate, workspace=self.root)

    def test_cross_version_comparison_does_not_invent_missing_scores(self):
        before = self.candidate_file({"schema_version": 1, "cases": []}, "before.json")
        after = self.candidate_file({"schema_version": 1, "cases": [
            {"case": "governance_integration_review", "doi": "10.3390/digital5040059"}
        ]}, "after.json")
        result = q.evaluate(self.reference_path, after, workspace=self.root, baseline=before)
        self.assertIsNone(result["baseline_comparison"]["identity"]["change"])

    def test_unrecognized_case_is_rejected(self):
        candidate = self.candidate_file({"schema_version": 1, "cases": [{"case": "unknown"}]})
        with self.assertRaises(ValueError):
            q.evaluate(self.reference_path, candidate, workspace=self.root)


if __name__ == "__main__":
    unittest.main()
