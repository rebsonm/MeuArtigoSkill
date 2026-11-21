"""No-network integration and safety tests for the experimental two-channel retriever."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experimental" / "conceptual_rag"))
import hybrid_public_retriever as hybrid
import consult_github_methodology as cards
import github_pdf_reader as pdfs

REF = "b" * 40


class HybridPublicRetrievalTests(unittest.TestCase):
    def sources(self, *, bad_pdf=False, forbidden_rights=False):
        catalogue = json.loads((ROOT / cards.INDEX_PATH).read_text("utf-8"))
        pdf_catalogue = json.loads((ROOT / pdfs.CATALOG).read_text("utf-8"))
        if forbidden_rights:
            pdf_catalogue["documents"][0]["rights"] = "PRIVATE_AUTHORIZED"
        files = {
            cards.INDEX_PATH: json.dumps(catalogue).encode(),
            pdfs.CATALOG: json.dumps(pdf_catalogue).encode(),
        }
        for c in catalogue["documents"]:
            files[c["path"]] = (ROOT / c["path"]).read_bytes()
        for p in pdf_catalogue["documents"]:
            files[p["path"]] = (ROOT / p["path"]).read_bytes()
        if bad_pdf:
            pdf_path = pdf_catalogue["documents"][0]["path"]
            files[pdf_path] += b"tampering"
        calls = []
        def fetch(ref, path, limit):
            self.assertEqual(ref, REF)
            calls.append(path)
            return files[path]
        return fetch, calls

    def test_no_match_reads_only_metadata_catalogues(self):
        fetch, calls = self.sources()
        result = hybrid.query("quasar volcano asteroids", ref=REF,
                              card_fetch=fetch, pdf_fetch=fetch)
        self.assertEqual(result["status"], "NO_MATCH")
        self.assertEqual(calls, [cards.INDEX_PATH, pdfs.CATALOG])
        self.assertEqual(result["returned_context_chars"], 0)

    def test_card_and_pdf_selection_with_separate_evidence_grades(self):
        fetch, calls = self.sources()
        result = hybrid.query("revisão literatura confiabilidade", ref=REF,
                              max_chars=1400, card_fetch=fetch, pdf_fetch=fetch)
        self.assertEqual(result["card_status"], "RETRIEVED")
        self.assertTrue(result["card_hits"])
        self.assertEqual(result["card_hits"][0]["citation_grade"],
                         "I_EDITORIAL_SYNTHESIS_ONLY")
        self.assertTrue(result["card_hits"][0]["must_not_claim_primary_source_read"])
        self.assertLessEqual(result["returned_context_chars"], 1400)
        self.assertFalse(result["scientific_gate_approved"])
        self.assertFalse(result["private_sources_accessed"])
        self.assertIn(pdfs.CATALOG, calls)
        self.assertLessEqual(len([p for p in calls if p.endswith(".pdf")]), 1)
        if result["pdf_hits"]:
            self.assertEqual(result["pdf_hits"][0]["citation_grade"],
                             "PDF_TEXT_EXTRACTED_REVIEW_PENDING")
            self.assertFalse(result["pdf_hits"][0]["page_label_verified"])
            self.assertTrue(result["pdf_hits"][0]["doi"])

    def test_tampered_pdf_does_not_turn_card_into_primary_evidence(self):
        fetch, calls = self.sources(bad_pdf=True)
        result = hybrid.query("revisão sistemática confiabilidade", ref=REF,
                              card_fetch=fetch, pdf_fetch=fetch)
        self.assertEqual(result["pdf_status"], "UNAVAILABLE_OR_BLOCKED")
        self.assertEqual(result["card_status"], "RETRIEVED")
        self.assertTrue(result["card_hits"])
        self.assertFalse(result["pdf_hits"])
        self.assertEqual(result["status"], "RETRIEVED_WITH_REVIEW_REQUIRED")

    def test_unreviewed_rights_block_public_pdf_even_with_matching_card(self):
        fetch, calls = self.sources(forbidden_rights=True)
        result = hybrid.query("revisão confiabilidade", ref=REF,
                              card_fetch=fetch, pdf_fetch=fetch)
        self.assertEqual(result["pdf_status"], "UNAVAILABLE_OR_BLOCKED")
        self.assertTrue(result["card_hits"])
        self.assertFalse([p for p in calls if p.endswith(".pdf")])

    def test_invalid_budget_and_moving_ref_fail_before_network(self):
        fetch, calls = self.sources()
        for kw in ({"ref": "main"}, {"ref": REF, "max_chars": 700},
                   {"ref": REF, "max_cards": 20}):
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                hybrid.query("revisão", card_fetch=fetch, pdf_fetch=fetch, **kw)
        self.assertEqual(calls, [])

    def test_catalogue_has_only_original_cards_and_documented_pdf_rights(self):
        catalogue = json.loads((ROOT / cards.INDEX_PATH).read_text("utf-8"))
        licensed = json.loads((ROOT / pdfs.CATALOG).read_text("utf-8"))
        self.assertTrue(catalogue["documents"])
        self.assertGreaterEqual(len(licensed["documents"]), 6)
        for card in catalogue["documents"]:
            self.assertEqual(card["source_kind"], "ORIGINAL_CURATED_SUMMARY")
            self.assertEqual(card["rights"], "PUBLIC_REDISTRIBUTION_REVIEWED")
        for item in licensed["documents"]:
            for field in ("authors", "year", "doi", "source_url", "license",
                          "license_url", "rights_evidence", "sha256"):
                self.assertTrue(item.get(field), msg=(item["path"], field))
            self.assertEqual(item["rights"], "PUBLIC_REDISTRIBUTION_REVIEWED")

    def test_documented_rights_and_installer_isolation(self):
        policy = (ROOT / "knowledge/methodology/CARD-POLICY.md").read_text("utf-8")
        self.assertIn("scientific/editorial fidelity review", policy)
        self.assertIn("serial reconstruction", policy)
        from build_skill_bundle import list_sources
        paths = {p.relative_to(ROOT).as_posix() for p in list_sources(ROOT)}
        self.assertFalse(any(p.startswith("knowledge/") for p in paths))
        self.assertNotIn("experimental/conceptual_rag/hybrid_public_retriever.py", paths)


if __name__ == "__main__":
    unittest.main()
