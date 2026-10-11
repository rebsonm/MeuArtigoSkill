"""Integrated Phase-4 hybrid bibliographic software audit (all synthetic).

Manual Scopus/WoS exports and mocked optional API results are merged by the
same production CLI. This is not a real search, screened corpus, API licence,
human decision, or independent Google Drive validation.
"""
from __future__ import annotations

from argparse import Namespace
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import bibliographic_connectors as bc
import bibliographic_workflow as bw
import dedupe_records as dedupe
import init_project


def csv_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


class Phase4HybridEndToEnd(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name) / "workspace"
        self.root.mkdir()
        self.mgmt = self.root / bw.MGMT
        self.mgmt.mkdir()
        (self.mgmt / "PROJECT_CONFIG.json").write_text(json.dumps({
            "storage_mode": "WORK_FALLBACK", "fallback_authorized": True,
        }), encoding="utf-8")
        for name in (bw.SEARCH, bw.SCREENING, bw.TRACE):
            bw._atomic_csv(self.root / name, init_project.TABLES[name], [])
        self.scopus = self.root / "manual-scopus.csv"
        with self.scopus.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=["Title", "DOI", "Authors", "Year"])
            writer.writeheader()
            writer.writerow({"Title": "Framework for public accountability",
                             "DOI": "10.1234/exact", "Authors": "Alice Evidence",
                             "Year": "2024"})
        self.wos = self.root / "manual-wos.tsv"
        self.wos.write_text(
            "Article Title\tDOI\tAuthors\tPublication Year\n"
            "Interagency digital accountability mechanisms\t10.1234/near\tAlice Evidence\t2024\n",
            encoding="utf-8")
        def fake(url, headers):
            return {"meta": {"count": 2}, "results": [
                self.oa("Framework for public accountability", "10.1234/exact", "W10001"),
                self.oa("Interagency digital accountability mechanism",
                        "10.1234/near-variant", "W10002"),
            ]}
        self.outcome = bc.search("openalex", "synthetic governance",
                                 execute=True, fetcher=fake, limit=2)
        self.stage = self.root / "api-staging"
        self.receipt = bw.export_staging(self.root, self.stage, self.outcome)
        self.api_csv = self.stage / "openalex_metadata.csv"

    @staticmethod
    def oa(title, doi, work_id):
        return {"id": "https://openalex.org/" + work_id,
                "display_name": title,
                "doi": "https://doi.org/" + doi,
                "publication_year": 2024,
                "authorships": [{"author": {"display_name": "Alice Evidence"}}],
                "primary_location": {
                    "landing_page_url": "https://example.org/mock",
                    "source": {"display_name": "Synthetic Journal"}}}

    def dedupe(self, inputs=None, output="hybrid-results"):
        inputs = inputs or [self.scopus, self.wos, self.api_csv]
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/dedupe_records.py"),
             *(str(p) for p in inputs), "--out-dir", str(self.root / output)],
            capture_output=True, text=True)

    def test_hybrid_scopus_wos_api_preserves_origin_and_near_duplicates(self):
        original = {p.name: p.read_bytes() for p in (self.scopus, self.wos, self.api_csv)}
        result = self.dedupe()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("import_status=COMPLETE", result.stdout)
        output = self.root / "hybrid-results"
        diagnostics = json.loads((output / "import_diagnostics.json").read_text())
        self.assertEqual(diagnostics["status"], "COMPLETE")
        self.assertFalse(diagnostics["requires_researcher_review"])
        self.assertEqual(diagnostics["input_records"], 4)
        self.assertEqual(diagnostics["exact_duplicates"], 1)
        self.assertEqual(diagnostics["canonical_after_exact_dedup"], 3)
        self.assertGreaterEqual(diagnostics["near_duplicate_pairs_to_review"], 1)
        duplicates = csv_rows(output / "exact_duplicate_audit.csv")
        self.assertEqual(duplicates[0]["reason"], "exact_doi")
        consolidated = csv_rows(output / "consolidated_exact_dedup.csv")
        self.assertTrue(any("INPUT-0001" in r["_source_locations"]
                            and "INPUT-0003" in r["_source_locations"]
                            for r in consolidated))
        near = csv_rows(output / "near_duplicate_review.csv")
        self.assertTrue(all(r["decision"] == "REVIEW_REQUIRED" for r in near))
        self.assertIn("10.1234/near", {r["_norm_doi"] for r in consolidated})
        self.assertIn("10.1234/near-variant", {r["_norm_doi"] for r in consolidated})
        entries = json.loads((output / "import_sources_manifest.json").read_text())["inputs"]
        self.assertEqual([r["source_input_id"] for r in entries],
                         ["INPUT-0001", "INPUT-0002", "INPUT-0003"])
        for entry, file in zip(entries, (self.scopus, self.wos, self.api_csv)):
            self.assertEqual(entry["content_sha256"],
                             hashlib.sha256(original[file.name]).hexdigest())
            self.assertEqual(file.read_bytes(), original[file.name])
        # Dedupe is a staging-only operation; it cannot fake a corpus freeze.
        self.assertEqual(csv_rows(self.mgmt / "03_Screening.csv"), [])
        self.assertFalse((self.mgmt / "18_Human_Validation_Gates.csv").exists())

    def test_api_commit_plus_hybrid_dedupe_does_not_pretend_manual_corpus_is_screened(self):
        imported = bw.commit_to_authorized_local_project(
            self.root, self.outcome, self.api_csv)
        self.assertEqual(imported["new_records"], 2)
        srows = csv_rows(self.mgmt / "03_Screening.csv")
        self.assertEqual(len(srows), 2)
        self.assertTrue(all(not r["Pass1_decision"] for r in srows))
        self.assertTrue(all(not r["Abstract"] for r in srows))
        trace = csv_rows(self.mgmt / "13_Traceability_Log.csv")
        self.assertEqual(trace[0]["Status"], "UNVERIFIED")
        self.assertIn(self.receipt["export_sha256"], csv_rows(
            self.mgmt / "02_Search_Log.csv")[0]["Notes"])
        self.assertFalse((self.mgmt / "18_Human_Validation_Gates.csv").exists())
        self.assertEqual(self.dedupe().returncode, 0)
        self.assertEqual(len(csv_rows(self.mgmt / "03_Screening.csv")), 2)

    def test_missing_manual_export_keeps_valid_rows_but_declares_partial_batch(self):
        missing = self.root / "missing-manual.csv"
        result = self.dedupe([self.scopus, missing, self.api_csv])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("import_status=PARTIAL_INPUTS", result.stdout)
        d = json.loads((self.root / "hybrid-results/import_diagnostics.json").read_text())
        self.assertTrue(d["requires_researcher_review"])
        self.assertEqual(d["status"], "PARTIAL_INPUTS")
        self.assertEqual(d["canonical_after_exact_dedup"], 2)
        manifest = json.loads((self.root / "hybrid-results/import_sources_manifest.json").read_text())
        self.assertEqual(manifest["inputs"][1]["read_status"], "UNREADABLE_EXPORT")

    def test_nonexistent_full_batch_does_not_create_fictitious_corpus(self):
        result = self.dedupe([self.root / "missing1.csv", self.root / "missing2.csv"])
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "hybrid-results/consolidated_exact_dedup.csv").exists())

    def test_second_attempt_cannot_overwrite_earlier_hybrid_outputs(self):
        self.assertEqual(self.dedupe().returncode, 0)
        original = (self.root / "hybrid-results/import_sources_manifest.json").read_bytes()
        second = self.dedupe()
        self.assertEqual(second.returncode, 2)
        self.assertEqual((self.root / "hybrid-results/import_sources_manifest.json").read_bytes(), original)

    def test_invalid_doi_suffix_cannot_claim_exact_doi_identity(self):
        self.assertEqual(dedupe.norm_doi("10.1234/valid junk suffix"), "")
        self.assertEqual(dedupe.norm_doi("10.1234/valid"), "10.1234/valid")

    def test_source_edited_during_own_parse_aborts_before_emitting_results(self):
        native_reader = dedupe.read_tabular
        def changing_reader(path):
            content = native_reader(path)
            if Path(path) == self.scopus:
                self.scopus.write_bytes(self.scopus.read_bytes() + b"\n")
            return content
        with patch.object(dedupe, "read_tabular", side_effect=changing_reader):
            out = self.root / "changed-own-input"
            result = dedupe.run_import(out, Namespace(
                inputs=[str(self.scopus), str(self.wos)], fuzzy_threshold=0.94))
        self.assertEqual(result, 2)
        self.assertFalse((out / "consolidated_exact_dedup.csv").exists())
        self.assertFalse((out / "import_sources_manifest.json").exists())

    def test_first_input_edited_while_second_is_parsed_aborts_whole_batch(self):
        native_reader = dedupe.read_tabular
        def changing_reader(path):
            if Path(path) == self.wos:
                self.scopus.write_bytes(self.scopus.read_bytes() + b"\n")
            return native_reader(path)
        with patch.object(dedupe, "read_tabular", side_effect=changing_reader):
            out = self.root / "changed-previous-input"
            result = dedupe.run_import(out, Namespace(
                inputs=[str(self.scopus), str(self.wos)], fuzzy_threshold=0.94))
        self.assertEqual(result, 2)
        self.assertFalse((out / "consolidated_exact_dedup.csv").exists())
        self.assertFalse((out / "import_sources_manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
