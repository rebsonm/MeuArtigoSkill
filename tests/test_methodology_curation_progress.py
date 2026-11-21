"""Read-only inventory accounting: no private source ingestion or invented coverage."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experimental" / "conceptual_rag"))
import curation_progress


class SourceArchiveCurationAccountingTests(unittest.TestCase):
    def test_metadata_inventory_and_public_corpus_are_not_conflated(self):
        report = curation_progress.audit(ROOT)
        self.assertEqual(report["archive_folders_including_nested"], 75)
        self.assertEqual(report["archive_pdf_records"], 475)
        self.assertEqual(report["archive_distinct_filenames"], 466)
        self.assertEqual(report["public_editorial_cards"], 23)
        self.assertEqual(report["published_source_pdf_records_on_draft_branch"], 12)
        self.assertEqual(report["card_editorial_states"].get(
            "DRAFT_NEEDS_INDEPENDENT_REVIEW"), 19)
        self.assertEqual(report["card_editorial_states"].get(
            "NOT_INDEPENDENTLY_REVIEWED"), 4)
        self.assertFalse(report["private_pdf_full_text_inspected"])
        self.assertFalse(report["source_to_card_exact_coverage_verified"])
        self.assertFalse(report["legal_and_scientific_review_completed"])

    def test_unreviewed_source_group_cannot_be_laundered_to_licensed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = ROOT / "knowledge" / "methodology"
            target = root / "knowledge" / "methodology"
            (target / "inventory").mkdir(parents=True)
            for file in (source / "inventory").glob("drive-source-candidates-part-*.json"):
                shutil.copyfile(file, target / "inventory" / file.name)
            for file in ("catalog.json", "pdf_catalog.json"):
                shutil.copyfile(source / file, target / file)
            part = target / "inventory" / "drive-source-candidates-part-01.json"
            value = json.loads(part.read_text(encoding="utf-8"))
            value["rights_status"] = "PUBLIC_REDISTRIBUTION_REVIEWED"
            part.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "SOURCE_RIGHTS_CLASSIFICATION_CHANGED"):
                curation_progress.audit(root)


if __name__ == "__main__":
    unittest.main()
