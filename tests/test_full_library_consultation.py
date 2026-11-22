"""Regression tests for unified access to the entire 649-card library."""
from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import consult_full_library as lib


class TestUnifiedLibrary(unittest.TestCase):
    def setUp(self):
        self.a = {"id": "SRC-0001", "kind": "BIBLIOGRAPHIC_PROSPECTING_P",
                  "title": "Grounded theory", "path": "knowledge/methodology/source_cards/src-0001.md",
                  "sha256": hashlib.sha256(b"lead").hexdigest(), "terms": ["Grounded theory"],
                  "disposition": "VALIDADO_COM_RESTRICOES",
                  "source_identity": "CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED",
                  "rights_review": "NOT_CHECKED"}
        self.block = dict(self.a, id="SRC-0385", disposition="BLOQUEADO_POR_EVIDENCIA",
                          title="Quarantined reference", terms=["Quarantined reference"])
        self.ed = dict(self.a, id="EC-0001", kind="ORIGINAL_EDITORIAL_I_P",
                       title="Design science", terms=["Design science"],
                       disposition="CORRIGIDO_E_REVALIDADO")

    def test_blocked_exact_id_cannot_recommend_another_card(self):
        self.assertEqual(lib.select([self.a, self.block], card_id="SRC-0385"), [])
        audit = lib.select([self.a, self.block], card_id="src-0385", mode="audit")
        self.assertEqual([r["id"] for r in audit], ["SRC-0385"])
        self.assertFalse(lib._public_record(audit[0])["available_for_guidance"])

    def test_independent_categories_and_no_scientific_claim(self):
        self.assertEqual([r["id"] for r in lib.select([self.a, self.ed],
                        question="design science")], ["EC-0001"])
        self.assertFalse(lib._public_record(self.ed)["scientific_quality_validated"])
        self.assertIn("BIBLIOGRAPHIC_LEAD", lib._public_record(self.a)["citation_grade"])

    def test_exact_id_not_bypassed_by_extra_words(self):
        rows = lib.select([self.a, self.block], question="Use SRC-0385 grounded theory")
        self.assertEqual(rows, [])

    def test_invalid_request_rejected(self):
        with self.assertRaises(ValueError):
            lib.select([self.a], question="a", card_id="SRC-0001")
        with self.assertRaises(ValueError):
            lib.select([self.a], card_id="../src-0001.md")
        with self.assertRaises(ValueError):
            lib.select([self.a], card_id="SRC-0001", mode="release")

    def test_hash_and_whole_catalogue_coverage_from_mock(self):
        import json
        src = []
        for i in range(1, 476):
            src.append({"source_id": f"SRC-{i:04d}",
                        "path": f"knowledge/methodology/source_cards/src-{i:04d}.md",
                        "source_metadata_only": True, "sha256": "0"*64,
                        "title": f"Book {i}", "topic": "methods",
                        "keywords": ["methods"], "rights_review": "NOT_CHECKED",
                        "bibliography_match_status": "CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED",
                        "operational_disposition": "VALIDADO_COM_RESTRICOES"})
        src[384]["operational_disposition"] = "BLOQUEADO_POR_EVIDENCIA"
        ed = [{"path": f"knowledge/methodology/cards/card-{i:04d}.md",
               "sha256": "0"*64, "title": f"Method {i}",
               "keywords": ["method"], "source_kind": "ORIGINAL_CURATED_SUMMARY",
               "rights": "PUBLIC_REDISTRIBUTION_REVIEWED",
               "operational_disposition": "VALIDADO_COM_RESTRICOES"}
              for i in range(1, 175)]
        source_obj = {"schema": "MEU_ARTIGO_SOURCE_CARD_INDEX_V1",
                      "source_text_read_in_ledger": 0, "third_party_full_text_included": False,
                      "documents": [{**x, "source_read_scope": "NOT_RECORDED_IN_LEDGER",
                                     "has_original_public_pdf": False} for x in src]}
        ed_obj = {"schema": "MEU_ARTIGO_GITHUB_METHODOLOGY_V1", "documents": ed}
        mapping = {lib.bibliographic.INDEX: json.dumps(source_obj).encode(),
                   lib.editorial.INDEX_PATH: json.dumps(ed_obj).encode()}
        def fetch(ref, path, limit):
            self.assertLessEqual(len(mapping[path]), limit)
            return mapping[path]
        result = lib.query(ref="a"*40, card_id="SRC-0385", mode="audit", fetch=fetch)
        self.assertEqual(result["total_cards"], 649)
        self.assertEqual(len(result["hits"]), 1)
        self.assertNotIn("excerpt", result["hits"][0])
        self.assertFalse(result["hits"][0]["available_for_guidance"])
        guided = lib.query(ref="a"*40, card_id="SRC-0385", fetch=fetch)
        self.assertEqual(guided["hits"], [])
        self.assertEqual(result["dispositions"]["BLOQUEADO_POR_EVIDENCIA"], 1)
        full_inventory = lib.query(ref="a"*40, list_all=True, mode="audit", fetch=fetch)
        self.assertEqual(len(full_inventory["hits"]), 649)
        active_inventory = lib.query(ref="a"*40, list_all=True, mode="guidance", fetch=fetch)
        self.assertEqual(len(active_inventory["hits"]), 648)
        with self.assertRaises(ValueError):
            lib.query(ref="a"*40, list_all=True, mode="audit", include_text=True, fetch=fetch)


if __name__ == "__main__":
    unittest.main()
