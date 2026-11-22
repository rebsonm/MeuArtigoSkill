"""Maintain exact PPGA open-PDF source identity without weakening historic tests."""

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METHODS = ROOT / "knowledge" / "methodology"
EXPECTED = {
    "mirzaei-mabin-zwikael-2025-hybrid-project-management.pdf": ("6012d1ecae3aa60258aa6d4fea86b5ff1a94db2914de6f1a5079014f8d7d6886", 1807583, "10.1080/09537287.2024.2349231"),
    "martinsuo-tilebein-birollo-2024-project-lifecycles.pdf": ("1b1d66b221e3c7c1eed14a29d1cdfc1f341de231c6417e870a1df60d5eee514a", 415970, "10.1016/j.ijproman.2024.102653"),
    "mariani-2026-projects-ready-for-ai.pdf": ("4d2ff1fdec51501ed79b912ab9341fa51ed034f57cbdc2b3fd3625bbe1bed5be", 622527, "10.1016/j.ijproman.2026.102846"),
    "chen-martins-zhang-dong-2025-digital-transformation-projects.pdf": ("25d5a29d0d3d28d4eacf9e0a6fedfb567a37b20814b42aa403b8e2ea396d4b6b", 2404059, "10.3390/systems13080625"),
}


class PPGAOriginalPDFBatchTests(unittest.TestCase):
    def test_four_original_pdf_licenses_provenance_and_unchanged_bytes(self):
        catalog = json.loads((METHODS / "pdf_catalog.json").read_text("utf-8"))
        entries = {Path(x["path"]).name: x for x in catalog["documents"]}
        self.assertEqual(len(catalog["documents"]), 55)
        self.assertEqual(len(entries), 55)
        self.assertEqual(len(list((METHODS / "pdfs").glob("*.pdf"))), 55)
        for filename, (sha256, size, doi) in EXPECTED.items():
            with self.subTest(filename=filename):
                doc = entries[filename]
                original = METHODS / doc["path"].split("knowledge/methodology/", 1)[-1]
                self.assertTrue(original.is_file())
                self.assertEqual(original.stat().st_size, size)
                self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), sha256)
                self.assertEqual(doc["sha256"], sha256)
                self.assertEqual(doc["size"], size)
                self.assertEqual(doc["doi"], doi)
                self.assertEqual(doc["rights"], "PUBLIC_REDISTRIBUTION_REVIEWED")
                self.assertEqual(doc["license"], "CC BY 4.0")
                self.assertEqual(doc["license_url"], "https://creativecommons.org/licenses/by/4.0/")
                self.assertTrue(doc["original_file_unchanged"])
                self.assertEqual(doc["source_url"], "https://doi.org/" + doi)

    def test_pdf_catalogue_is_not_scientific_approval(self):
        catalog = json.loads((METHODS / "pdf_catalog.json").read_text("utf-8"))
        self.assertFalse(catalog["scientific_quality_validated"])
        self.assertFalse(catalog["installer_includes_pdfs"])


if __name__ == "__main__":
    unittest.main()
