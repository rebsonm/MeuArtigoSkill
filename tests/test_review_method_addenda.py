"""Research-method additions: PRISMA 2020, B-SLR, correct rights and public ZIP isolation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_skill_bundle import list_sources


class ReviewMethodAddendaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards = json.loads((ROOT/"knowledge/methodology/catalog.json").read_text("utf-8"))["documents"]
        cls.pdfs = json.loads((ROOT/"knowledge/methodology/pdf_catalog.json").read_text("utf-8"))["documents"]

    def test_methodology_catalog_has_new_sources_and_verifiable_digests(self):
        self.assertEqual(len(self.cards), 164)
        wanted = {
            "marzi-et-al-2025-bslr-ten-steps.md",
            "snyder-2019-literature-review-designs.md",
            "salvador-1986-bibliographic-research-foundation.md",
            "grant-booth-2009-salsa-review-typology.md",
            "jaakkola-2020-four-conceptual-approaches.md",
            "prisma-2020-operational-reporting.md",
            "prisma-s-2021-search-reporting.md",
            "prisma-scr-2018-scoping.md",
            "prisma-p-2015-protocol.md",
            "saunders-lewis-thornhill-2023-onion.md",
        }
        actual = {Path(x["path"]).name for x in self.cards}
        self.assertTrue(wanted.issubset(actual))
        for x in self.cards:
            self.assertEqual(hashlib.sha256((ROOT/x["path"]).read_bytes()).hexdigest(),
                             x["sha256"])
            self.assertNotEqual(x.get("editorial_status"), "ACCEPTED")

    def test_two_new_licensed_pdf_originals_publisher_evidence_and_integrity(self):
        self.assertEqual(len(self.pdfs), 52)
        for doi in ("10.1111/ijmr.12381", "10.1007/s13162-020-00161-0"):
            item = next((x for x in self.pdfs if x.get("doi")==doi), None)
            self.assertIsNotNone(item)
            self.assertEqual(item["license"], "CC BY 4.0")
            self.assertTrue(item["rights_evidence"].startswith("https://"))
            data = (ROOT/item["path"]).read_bytes()
            self.assertTrue(data.startswith(b"%PDF"))
            self.assertEqual(len(data), item["size"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])

    def test_prisma_template_has_27_distinct_items_and_routes(self):
        body = (ROOT/"references/PRISMA-2020-CONTROLE.md").read_text("utf-8")
        items = [int(x) for x in re.findall(r"(?m)^\| (\d{1,2}) \|", body)]
        self.assertEqual(items, list(range(1, 28)))
        self.assertIn("not a review method", body.lower())
        for name in ("PRISMA-S", "PRISMA-ScR", "PRISMA-P", "B-SLR"):
            self.assertIn(name, body)
        self.assertIn("https://www.prisma-statement.org/prisma-2020-checklist", body)
        self.assertIn("not measured", body)
        self.assertIn("studies included", body.lower())

    def test_offline_guides_in_zip_and_no_private_collection_public_prose(self):
        package = {p.relative_to(ROOT).as_posix() for p in list_sources(ROOT)}
        self.assertIn("references/PRISMA-2020-CONTROLE.md", package)
        self.assertIn("references/REVIEW-METHOD-ROUTES.md", package)
        self.assertFalse(any("PPGA" in p for p in package))
        for path in ("references/REVIEW-METHOD-ROUTES.md",
                     "references/PRISMA-2020-CONTROLE.md"):
            data = (ROOT/path).read_text("utf-8")
            self.assertNotIn("PPGA", data)
            self.assertNotIn("drive.google.com/drive/folders/", data)
        self.assertFalse(any(p.startswith("knowledge/") for p in package))

    def test_no_unlicensed_original_pdf_promoted_by_registry_matching(self):
        manifest = json.loads((ROOT/"knowledge/methodology/intake/rights-ledger-manifest.json").read_text("utf-8"))
        self.assertEqual(manifest["actual_individually_verified_rights_in_this_ledger"], 18)
        self.assertEqual(manifest["source_pdf_count_public_catalogue"], 52)
        self.assertEqual(manifest["original_editorial_cards_count"], 164)
        self.assertFalse(manifest["private_corpus_copied"])


if __name__ == "__main__":
    unittest.main()
