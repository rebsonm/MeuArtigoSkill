"""Synthetic legacy .xls (BIFF/OLE) compatibility and defensive import tests."""
from __future__ import annotations
import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "dedupe_records.py"
LIBS_AVAILABLE = all(importlib.util.find_spec(lib) for lib in ("xlrd", "xlwt"))


@unittest.skipUnless(LIBS_AVAILABLE, "Optional xlrd and xlwt required for XLS tests")
class LegacyWosXlsTests(unittest.TestCase):
    def setUp(self):
        self.working = tempfile.TemporaryDirectory()
        self.addCleanup(self.working.cleanup)
        self.root = Path(self.working.name)
        self.out = self.root / "out"

    def create_xls(self, name, headers, rows):
        import xlwt
        wb = xlwt.Workbook(encoding="utf-8")
        sheet = wb.add_sheet("Full Record")
        for col, head in enumerate(headers):
            sheet.write(0, col, head)
        for row_idx, record in enumerate(rows, 1):
            for col, value in enumerate(record):
                sheet.write(row_idx, col, value)
        destination = self.root / name
        wb.save(str(destination))
        return destination

    def run_import(self, *files):
        return subprocess.run([
            sys.executable, str(RUNNER),
            *(str(x) for x in files), "--out-dir", str(self.out)
        ], capture_output=True, text=True)

    def read_rows(self, name):
        with (self.out / name).open(encoding="utf-8-sig", newline="") as fh:
            return list(csv.DictReader(fh))

    def test_wos_xls_au_af_ti_py_di_originals_remain_unchanged(self):
        file = self.create_xls(
            "savedrecs.xls", ["AU", "AF", "TI", "PY", "DI", "UT"],
            [["Silva, A", "Silva, Ana", "Public management", 2025,
              "10.1234/legacy", "WOS:123456"]])
        original = file.read_bytes()
        result = self.run_import(file)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(file.read_bytes(), original)
        rows = self.read_rows("consolidated_exact_dedup.csv")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["PY"], "2025")
        self.assertEqual(rows[0]["AU"], "Silva, A")
        self.assertEqual(rows[0]["AF"], "Silva, Ana")
        self.assertEqual(rows[0]["_norm_doi"], "10.1234/legacy")
        source = json.loads((self.out / "import_sources_manifest.json").read_text())
        self.assertEqual(source["inputs"][0]["source_file"], "savedrecs.xls")
        self.assertEqual(source["inputs"][0]["read_status"], "READABLE")

    def test_ambiguous_title_columns_xls_are_quarantined(self):
        file = self.create_xls(
            "duplicate.xls", ["Title", "Article Title", "DOI"],
            [["First work", "Another work", "10.1234/dup"]])
        result = self.run_import(file)
        self.assertEqual(result.returncode, 2, result.stderr)
        rejects = self.read_rows("rejected_records.csv")
        self.assertEqual(len(rejects), 1)
        self.assertEqual(rejects[0]["_reject_reason"], "AMBIGUOUS_BIBLIOGRAPHIC_HEADERS")
        self.assertIn("First work", rejects[0]["_raw_record"])
        self.assertIn("Another work", rejects[0]["_raw_record"])
        self.assertFalse((self.out / "consolidated_exact_dedup.csv").exists())

    def test_legacy_xls_publication_date_and_year_complementary(self):
        file = self.create_xls(
            "dates.xls", ["Authors", "Author full names", "Article Title",
                          "Publication Date", "Publication Year", "DOI"],
            [["Costa J", "Costa, Joana", "Knowledge management", "OCT 11",
              2026, "10.1234/dates"]])
        result = self.run_import(file)
        self.assertEqual(result.returncode, 0, result.stderr)
        row = self.read_rows("consolidated_exact_dedup.csv")[0]
        self.assertEqual(row["Publication Year"], "2026")
        self.assertEqual(row["Publication Date"], "OCT 11")
        self.assertEqual(row["_year"], "2026")

    def test_clean_xls_import_continues_if_another_file_is_invalid(self):
        bad = self.create_xls("bad.xls", ["DOI", "DOI"], [
            ["10.1234/first", "10.1234/second"]])
        good = self.create_xls("good.xls", ["Title", "DOI"], [
            ["Useful work", "10.1234/good"]])
        result = self.run_import(bad, good)
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.read_rows("consolidated_exact_dedup.csv")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Title"], "Useful work")
        reject = self.read_rows("rejected_records.csv")
        self.assertEqual(reject[0]["_reject_reason"], "DUPLICATE_HEADER")

    def test_non_xls_payload_does_not_silently_enter_bibliography(self):
        fake = self.root / "fake.xls"
        fake.write_bytes(b"not an xls workbook")
        result = self.run_import(fake)
        self.assertEqual(result.returncode, 2, result.stderr)
        diagnostics = json.loads(
            (self.out / "import_diagnostics.json").read_text()
        )
        self.assertTrue(any(x["reason"] == "UNREADABLE_EXPORT"
                            for x in diagnostics["diagnostics"]))
        self.assertFalse((self.out / "consolidated_exact_dedup.csv").exists())


if __name__ == "__main__":
    unittest.main()
