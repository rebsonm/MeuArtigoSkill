"""Synthetic regression of cross-file claim and evidence provenance.

These fixtures do not contain scholarly findings or authenticated human review.
Passing structural checks never validates the interpretation of a source.
"""
from __future__ import annotations

import csv
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import claim_integrity as claims
import scientific_evidence_tiers as tiers

MGMT = "00_Gestao_e_Continuidade"


def write_csv(path, lines):
    if not lines:
        raise ValueError("synthetic fixture requires at least one entry")
    with path.open("w", encoding="utf-8-sig", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(lines[0]))
        writer.writeheader()
        writer.writerows(lines)


class ClaimEvidenceProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.evidence = [
            {"Evidence_ID": "EVID-0001", "Citation": "Synthetic record A (2021)",
             "DOI_or_persistent_ID": "", "Supporting_locator": "p. 3: synthetic claim text."},
            {"Evidence_ID": "EVID-0002", "Citation": "Synthetic record B (2022)",
             "DOI_or_persistent_ID": "", "Supporting_locator": "p. 5: synthetic comparison."},
        ]
        self.search = [{"Search_ID": "SEARCH-0001",
                        "Literal_query": "synthetic AND science",
                        "Status": "COMPLETE"}]
        self.row = {
            "Claim_ID": "CLAIM-0001", "Claim_type": "[L]",
            "Claim_text": "A synthetic paper reports a conditional relationship in its conceptual discussion.",
            "Evidence_IDs": "EVID-0001", "Locator_status": "MATCHED",
            "Human_validation": "VALIDATED", "Draft_status": "READY",
            "Researcher_review_evidence": "Synthetic direct researcher response reference, not actual review.",
        }

    def audit(self, update=None, evidence=None, search=None, *, strict=True, freeze=True):
        return claims.audit(
            [{**self.row, **(update or {})}],
            evidence if evidence is not None else self.evidence,
            search if search is not None else self.search,
            strict=strict, freeze=freeze,
            headers=list(self.row) + [c for c in claims.EXTRA_COLUMNS if c not in self.row])

    def test_unique_supported_literature_claim_keeps_existing_behavior(self):
        self.assertEqual(self.audit()["errors"], [])
        self.assertIs(self.audit()["semantic_support_proven"], False)

    def test_duplicate_evidence_id_must_not_resolve_to_arbitrary_citation(self):
        doubled = self.evidence + [{**self.evidence[0], "Citation": "Conflicting reference"}]
        report = self.audit(evidence=doubled)
        self.assertTrue(any("ambiguous duplicated Evidence_ID" in e for e in report["errors"]))

    def test_duplicate_search_id_must_not_support_proposition_novelty(self):
        duplicated = self.search + [{**self.search[0], "Literal_query": "other search"}]
        report = self.audit({
            "Claim_type": "[P]", "Nearest_prior_Evidence_IDs": "EVID-0002",
            "Contribution_delta": "The synthetic model proposes a limited addition to an existing approach.",
            "Novelty_scope": "The contribution is bounded to the narrowly defined synthetic corpus under inspection.",
            "Novelty_search_ref": "SEARCH-0001",
        }, search=duplicated)
        self.assertTrue(any("ambiguous duplicated Search_ID" in e for e in report["errors"]))

    def test_supporting_and_counter_citation_need_explanation(self):
        r = self.audit({"Counter_Evidence_IDs": "EVID-0001"})
        self.assertTrue(any("both supporting and counter-evidence" in e for e in r["errors"]))
        r = self.audit({
            "Counter_Evidence_IDs": "EVID-0001",
            "Alternative_explanations": "The same study reports divergent conditions, which warrant qualified interpretation in this synthetic example.",
        })
        self.assertEqual(r["errors"], [])
        self.assertTrue(any("same evidence" in w for w in r["warnings"]))

    def test_repeated_counter_identifier_is_rejected(self):
        r = self.audit({"Counter_Evidence_IDs": "EVID-0002; EVID-0002"})
        self.assertTrue(any("duplicate evidence identifier" in e for e in r["errors"]))

    def test_failed_literal_locator_blocks_final_literature_claim(self):
        for status in ("PASSAGE_NOT_FOUND", "PAGE_MISMATCH", "OUTSIDE_WORKSPACE"):
            with self.subTest(status=status):
                r = self.audit({"Locator_status": status})
                self.assertTrue(any("objective contradiction" in e for e in r["errors"]))

    def test_modern_evidence_without_source_citation_or_id_is_not_frozen(self):
        sources = [{**self.evidence[0], "Citation": "", "DOI_or_persistent_ID": ""}]
        r = self.audit(evidence=sources)
        self.assertTrue(any("lacks bibliographic citation" in e for e in r["errors"]))
        sources[0]["DOI_or_persistent_ID"] = "10.1234/synthetic"
        self.assertEqual(self.audit(evidence=sources)["errors"], [])

    def test_nearest_prior_requires_identity_on_final_proposition(self):
        r = self.audit({
            "Claim_type": "[P]", "Nearest_prior_Evidence_IDs": "EVID-0002",
            "Contribution_delta": "The synthetic model proposes a limited addition to an existing approach.",
            "Novelty_scope": "The contribution is bounded to a narrowly defined synthetic research corpus.",
            "Novelty_search_ref": "SEARCH-0001",
        }, evidence=[self.evidence[0], {**self.evidence[1], "Citation": ""}])
        self.assertTrue(any("nearest prior evidence" in e for e in r["errors"]))

    def test_unfrozen_legacy_draft_keeps_warning_based_checks(self):
        rows = [{**self.evidence[0], "Citation": ""}]
        r = self.audit({"Draft_status": "DRAFT"}, evidence=rows, strict=False, freeze=False)
        self.assertFalse(any("lacks bibliographic citation" in e for e in r["errors"]))


class EmpiricalTraceProvenanceTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.mgmt = self.root / MGMT
        self.mgmt.mkdir()
        (self.mgmt / "PROJECT_CONFIG.json").write_text(
            '{"method_route_governance_required": true, "method_route": "QUANTITATIVE"}',
            encoding="utf-8")
        (self.mgmt / "METHOD_PROFILE.json").write_text(
            '{"schema_version":1,"route":"QUANTITATIVE","evidence_status":"ANALYSIS_DOCUMENTED",'
            '"material_evidence_ref":"synthetic-material","analysis_evidence_ref":"synthetic-analysis"}',
            encoding="utf-8")
        write_csv(self.mgmt / "18_Human_Validation_Gates.csv", [
            {"GATE_ID": "GATE-0004", "Status": "COMPLETED", "Decision": "APPROVED"},
            {"GATE_ID": "GATE-0005", "Status": "COMPLETED", "Decision": "APPROVED"}])
        write_csv(self.mgmt / "09_Claims_Ledger.csv", [{
            "Claim_ID": "CLAIM-0001", "Claim_type": "EMPIRICAL_RESULT",
            "Trace_IDs": "TRACE-0001",
            "Researcher_review_evidence": "Synthetic reference, unverified."}])
        self.trace = self.mgmt / "13_Traceability_Log.csv"

    def check(self, events):
        if events is not None:
            write_csv(self.trace, events)
        return tiers.audit(self.root, freeze=True)

    def test_fictitious_trace_identifier_cannot_count_as_execution(self):
        r = self.check([{"Trace_ID": "TRACE-9999", "Status": "UNVERIFIED"}])
        self.assertTrue(any("TRACE_ID TRACE-0001 missing" in x for x in r["errors"]))

    def test_duplicated_trace_identifier_is_ambiguous(self):
        r = self.check([{"Trace_ID": "TRACE-0001", "Status": "UNVERIFIED"},
                        {"Trace_ID": "TRACE-0001", "Status": "UNVERIFIED"}])
        self.assertTrue(any("TRACE_ID TRACE-0001 missing or ambiguous" in x for x in r["errors"]))

    def test_failed_and_planned_trace_cannot_ground_frozen_empirical_claim(self):
        for status in ("PLANNED", "FAILED", "INVALID", "SUPERSEDED"):
            with self.subTest(status=status):
                r = self.check([{"Trace_ID": "TRACE-0001", "Status": status}])
                self.assertTrue(any("failed or unfinished" in x for x in r["errors"]))

    def test_single_existing_trace_passes_structural_link_but_not_scientific_truth(self):
        r = self.check([{"Trace_ID": "TRACE-0001", "Status": "UNVERIFIED"}])
        self.assertFalse(any("TRACE_ID" in x for x in r["errors"]))
        self.assertIs(r["empirical_scientific_result_independently_validated"], False)


if __name__ == "__main__":
    unittest.main()
