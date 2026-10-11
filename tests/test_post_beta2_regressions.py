"""INC-001/002 and Gate4 regression fixtures; no real research data or external calls."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
from validate_project import split_reference_ids
from build_skill_bundle import source_provenance, package
from version_info import read_version
import hashlib



def write_csv(path, headers, records):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(records)


def records_in(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


class PostBeta2ImportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.export = self.root / "export.csv"
        self.out = self.root / "output"

    def run_dedupe(self):
        return subprocess.run([sys.executable, str(SCRIPTS / "dedupe_records.py"),
                               str(self.export), "--out-dir", str(self.out)],
                              capture_output=True, text=True)

    def test_second_run_does_not_overwrite_or_relabel_prior_outputs(self):
        write_csv(self.export, ["Title", "DOI"],
                  [{"Title": "First import", "DOI": "10.1234/first"}])
        self.assertEqual(self.run_dedupe().returncode, 0)
        outputs = {p.name: p.read_bytes() for p in self.out.iterdir() if p.is_file()}
        write_csv(self.export, ["Unexpected"], [{"Unexpected": "invalid"}])
        second = self.run_dedupe()
        self.assertEqual(second.returncode, 2)
        self.assertIn("OUTPUT_DIRECTORY_ALREADY_HAS_RESULTS", second.stderr)
        self.assertEqual(
            outputs,
            {p.name: p.read_bytes() for p in self.out.iterdir() if p.is_file()},
        )

    def test_partial_prior_output_blocks_new_import(self):
        self.out.mkdir()
        (self.out / "exact_duplicate_audit.csv").write_text("prior run\n")
        write_csv(self.export, ["Title", "DOI"],
                  [{"Title": "New item", "DOI": "10.1234/new"}])
        result = self.run_dedupe()
        self.assertEqual(result.returncode, 2)
        self.assertIn("OUTPUT_DIRECTORY_ALREADY_HAS_RESULTS", result.stderr)
        self.assertEqual((self.out / "exact_duplicate_audit.csv").read_text(),
                         "prior run\n")

    def test_unknown_schema_rejected_with_structured_diagnostic(self):
        write_csv(self.export, ["unexpected_column"], [{"unexpected_column": "invalid"}])
        result = self.run_dedupe()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.out / "consolidated_exact_dedup.csv").exists())
        diagnostic = json.loads((self.out / "import_diagnostics.json").read_text())
        self.assertEqual(diagnostic["valid_records"], 0)
        self.assertEqual(diagnostic["rejected_records"], 1)
        self.assertTrue(any(d["reason"] == "MISSING_BIBLIOGRAPHIC_SCHEMA"
                            for d in diagnostic["diagnostics"]))

    def test_title_only_is_quarantined_but_good_neighbor_survives(self):
        write_csv(self.export, ["Title", "Authors", "Year"],
                  [{"Title": "Known research", "Authors": "Sample Author", "Year": "2025"},
                   {"Title": "Unknown research", "Authors": "", "Year": ""}])
        result = self.run_dedupe()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(records_in(self.out / "consolidated_exact_dedup.csv")), 1)
        bad = records_in(self.out / "rejected_records.csv")
        self.assertEqual(bad[0]["_reject_reason"], "MISSING_BIBLIOGRAPHIC_IDENTITY")

    def test_no_doi_is_not_reason_for_exclusion(self):
        write_csv(self.export, ["Article Title", "Creator", "Publication Year"],
                  [{"Article Title": "Research without DOI", "Creator": "Researcher",
                    "Publication Year": "2024"}])
        self.assertEqual(self.run_dedupe().returncode, 0)
        self.assertEqual(len(records_in(self.out / "consolidated_exact_dedup.csv")), 1)

    def test_stable_non_doi_identifier_can_support_title(self):
        write_csv(self.export, ["Title", "openalex_id"],
                  [{"Title": "Verified identity", "openalex_id": "W12345678"}])
        self.assertEqual(self.run_dedupe().returncode, 0)
        self.assertEqual(len(records_in(self.out / "consolidated_exact_dedup.csv")), 1)

    def test_malformed_extra_columns_quarantined_not_silently_accepted(self):
        self.export.write_text("Title,Authors,Year\nGood,Scientist,2025\nBad,Scientist,2025,extra\n",
                               encoding="utf-8")
        self.assertEqual(self.run_dedupe().returncode, 0)
        self.assertEqual(len(records_in(self.out / "consolidated_exact_dedup.csv")), 1)
        self.assertEqual(records_in(self.out / "rejected_records.csv")[0]["_reject_reason"],
                         "MALFORMED_ROW")

    def test_conflicting_explicit_versions_same_doi_are_preserved(self):
        write_csv(self.export, ["Title", "Authors", "Year", "DOI", "Version"],
                  [{"Title": "Article", "Authors": "Scholar", "Year": "2025",
                    "DOI": "10.1234/example", "Version": "v1"},
                   {"Title": "Article", "Authors": "Scholar", "Year": "2025",
                    "DOI": "10.1234/example", "Version": "v2"}])
        self.assertEqual(self.run_dedupe().returncode, 0)
        self.assertEqual(len(records_in(self.out / "consolidated_exact_dedup.csv")), 2)

    def test_same_doi_merges_and_keeps_both_records_and_searches(self):
        write_csv(self.export, ["Title", "DOI", "Record_ID", "Search_ID"],
                  [{"Title": "Article", "DOI": "10.1234/example", "Record_ID": "R-1",
                    "Search_ID": "S-1"},
                   {"Title": "Article", "DOI": "https://doi.org/10.1234/example",
                    "Record_ID": "R-2", "Search_ID": "S-2"}])
        self.assertEqual(self.run_dedupe().returncode, 0)
        saved = records_in(self.out / "consolidated_exact_dedup.csv")
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["Record_ID"], "R-1")
        self.assertEqual(saved[0]["Search_ID"], "S-1")
        self.assertEqual(saved[0]["_merged_Record_IDs"], "R-1;R-2")
        self.assertEqual(saved[0]["_merged_Search_IDs"], "S-1;S-2")
        audit = records_in(self.out / "exact_duplicate_audit.csv")
        self.assertEqual(audit[0]["duplicate_Record_ID"], "R-2")

    def test_fuzzy_titles_are_candidates_only(self):
        write_csv(self.export, ["Title", "Authors", "Year"],
                  [{"Title": "Tool for classroom use", "Authors": "Scholar", "Year": "2025"},
                   {"Title": "Tools for classroom use", "Authors": "Scholar", "Year": "2025"}])
        self.assertEqual(self.run_dedupe().returncode, 0)
        self.assertEqual(len(records_in(self.out / "consolidated_exact_dedup.csv")), 2)
        near = records_in(self.out / "near_duplicate_review.csv")
        self.assertEqual(len(near), 1)
        self.assertEqual(near[0]["decision"], "REVIEW_REQUIRED")


class PostBeta2XlsxAndTraceTests(unittest.TestCase):
    def test_help_without_optional_site_packages(self):
        proc = subprocess.run([sys.executable, "-S", str(SCRIPTS / "build_matrix_template.py"),
                               "--help"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("--check-deps", proc.stdout)

    def test_preflight_without_dependency_has_clear_diagnostic(self):
        proc = subprocess.run([sys.executable, "-S", str(SCRIPTS / "build_matrix_template.py"),
                               "--check-deps"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("XLSX_UNAVAILABLE", proc.stdout)

    def test_failed_generation_creates_no_fake_xlsx(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d) / "master.xlsx"
            proc = subprocess.run([sys.executable, "-S",
                                   str(SCRIPTS / "build_matrix_template.py"),
                                   "--output", str(dest), "--project-name", "Test"],
                                  capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("XLSX_UNAVAILABLE", proc.stderr)
            self.assertFalse(dest.exists())

    def test_multiple_traces_are_parsed_without_new_ids(self):
        self.assertEqual(split_reference_ids("TRACE-0009;TRACE-0010"),
                         ["TRACE-0009", "TRACE-0010"])
        self.assertEqual(split_reference_ids("TRACE-0011, TRACE-0012"),
                         ["TRACE-0011", "TRACE-0012"])


class PostBeta2BuildProvenanceTests(unittest.TestCase):
    def test_missing_git_does_not_invent_commit(self):
        with tempfile.TemporaryDirectory() as d:
            result = source_provenance(Path(d))
            self.assertIsNone(result["build_source_commit"])
            self.assertEqual(result["source_verification"], "UNVERIFIED")

    def test_package_hash_receipt_is_external_to_zip(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d) / f"MeuArtigoSkill-v{read_version(ROOT)}.zip"
            manifest = package(ROOT, dest)
            receipt = json.loads((dest.parent / "BUNDLE_BUILD_RECEIPT.json").read_text())
            self.assertEqual(receipt["package_sha256"], hashlib.sha256(dest.read_bytes()).hexdigest())
            self.assertEqual(manifest["build_source_commit"], receipt["build_source_commit"])
            self.assertEqual(receipt["distribution_type"], "SKILL_ZIP")
            self.assertFalse(receipt["scientific_quality_validated"])


if __name__ == "__main__":
    unittest.main()
