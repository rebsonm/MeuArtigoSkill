"""T33 regression: never conflate original editorial text rights with source PDF rights."""
from __future__ import annotations
import json
import re
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import consult_full_library as lib


class RightsScopeTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / "knowledge/methodology/catalog.json").read_text(encoding="utf-8"))
        self.docs = self.catalog["documents"]

    def test_all_174_rights_scopes_are_explicit(self):
        self.assertEqual(len(self.docs), 174)
        for item in self.docs:
            with self.subTest(path=item["path"]):
                self.assertEqual(item["rights_scope"], "ORIGINAL_EDITORIAL_TEXT_ONLY")
                self.assertIn(item["underlying_source_rights_status"],
                    {"UNVERIFIED_FOR_PUBLICATION", "NOT_ESTABLISHED_BY_CARD_CATALOG"})
                self.assertFalse(item.get("scientific_use_validated"))

    def test_body_unverified_source_rights_not_promoted_by_catalogue(self):
        count = 0
        for item in self.docs:
            body = (ROOT / item["path"]).read_text(encoding="utf-8")
            if re.search(r"^Rights status:\s*UNVERIFIED_FOR_PUBLICATION", body, re.MULTILINE):
                count += 1
                self.assertEqual(item["underlying_source_rights_status"],
                                 "UNVERIFIED_FOR_PUBLICATION", item["path"])
        self.assertGreaterEqual(count, 4)

    def test_ec0004_returns_conservative_underlying_rights(self):
        doc = next(x for x in self.docs if x["path"].endswith("/design-science.md"))
        row = {"id": "EC-0004", "kind": "ORIGINAL_EDITORIAL_I_P", "title": doc["title"],
               "path": doc["path"], "sha256": doc["sha256"], "disposition": doc["operational_disposition"],
               "source_identity": "NOT_APPLICABLE", "rights_review": doc["rights"],
               "original_card_rights_scope": doc["rights_scope"],
               "underlying_source_rights_status": doc["underlying_source_rights_status"]}
        result = lib._public_record(row)
        self.assertEqual(result["rights_review"], "UNVERIFIED_FOR_PUBLICATION")
        self.assertEqual(result["rights_review_scope"], "UNDERLYING_SOURCE")
        self.assertEqual(result["editorial_card_rights_scope"], "ORIGINAL_EDITORIAL_TEXT_ONLY")
        self.assertEqual(result["editorial_card_rights"], "PUBLIC_REDISTRIBUTION_REVIEWED")
        self.assertFalse(result["scientific_quality_validated"])


if __name__ == "__main__":
    unittest.main()
