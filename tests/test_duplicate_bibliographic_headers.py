"""Regression: ambiguous bibliographic headers never enter canonical data."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
IMPORTER = ROOT / "scripts" / "dedupe_records.py"


class HeaderValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.out = self.root / "result"

    def execute(self, *paths):
        return subprocess.run(
            [sys.executable, str(IMPORTER), *(str(p) for p in paths),
             "--out-dir", str(self.out)],
            text=True, capture_output=True,
        )

    def read_csv(self, name):
        with (self.out / name).open(encoding="utf-8-sig", newline="") as fh:
            return list(csv.DictReader(fh))

    def assert_quarantine(self, path, reason, count):
        result = self.execute(path)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse((self.out / "consolidated_exact_dedup.csv").exists())
        diagnostic = json.loads((self.out / "import_diagnostics.json").read_text())
        self.assertTrue(any(d["reason"] == reason
                            and d["affected_records"] == count
                            for d in diagnostic["diagnostics"]))
        self.assertEqual(diagnostic["rejected_records"], count)
        manifest = json.loads((self.out / "import_sources_manifest.json").read_text())
        self.assertEqual(manifest["inputs"][0]["read_status"], reason)
        self.assertEqual(manifest["inputs"][0]["rows_observed"], count)
        self.assertEqual(
            manifest["inputs"][0]["content_sha256"],
            hashlib.sha256(path.read_bytes()).hexdigest(),
        )
        self.assertFalse((self.out / ".dedupe_import_in_progress").exists())
        return self.read_csv("rejected_records.csv")

    def test_duplicate_exact_csv_headers_quarantines_both_cells(self):
        path = self.root / "duplicate.csv"
        path.write_text(
            "Title,Title,DOI\nFirst title,Second title,10.1234/item\n",
            encoding="utf-8",
        )
        rejected = self.assert_quarantine(path, "DUPLICATE_HEADER", 1)
        self.assertIn("First title", rejected[0]["_raw_record"])
        self.assertIn("Second title", rejected[0]["_raw_record"])

    def test_same_header_different_case_and_spacing_is_duplicate(self):
        path = self.root / "case.csv"
        path.write_text("DOI, doi ,Title\n10.1234/a,10.1234/b,Test\n",
                        encoding="utf-8")
        rejected = self.assert_quarantine(path, "DUPLICATE_HEADER", 1)
        self.assertIn("10.1234/a", rejected[0]["_raw_record"])
        self.assertIn("10.1234/b", rejected[0]["_raw_record"])

    def test_aliases_of_same_scientific_field_are_ambiguous(self):
        path = self.root / "aliases.csv"
        path.write_text(
            "Title,Article Title,DOI\nWork A,Work B,10.1234/a\n",
            encoding="utf-8",
        )
        self.assert_quarantine(path, "AMBIGUOUS_BIBLIOGRAPHIC_HEADERS", 1)

    def test_identifier_alias_conflicts_are_not_accepted(self):
        path = self.root / "identifiers.csv"
        path.write_text(
            "Title,DOI,Record_ID,Record ID\nExample,10.1234/a,R-1,R-2\n",
            encoding="utf-8",
        )
        self.assert_quarantine(path, "AMBIGUOUS_BIBLIOGRAPHIC_HEADERS", 1)

    def test_blank_header_is_quarantined(self):
        path = self.root / "empty_column.csv"
        path.write_text(
            "Title,,DOI\nItem,unlabelled,10.1234/a\n",
            encoding="utf-8",
        )
        self.assert_quarantine(path, "EMPTY_HEADER", 1)

    def test_tsv_duplicate_headers_are_detected(self):
        path = self.root / "duplicate.tsv"
        path.write_text(
            "Title\tDOI\tYear\tYear\nItem\t10.1234/a\t2020\t2021\n",
            encoding="utf-8",
        )
        self.assert_quarantine(path, "DUPLICATE_HEADER", 1)

    def test_unrelated_extra_column_does_not_block_valid_data(self):
        path = self.root / "valid.csv"
        path.write_text(
            "Title,DOI,Journal\nArticle,10.1234/a,Sample journal\n",
            encoding="utf-8",
        )
        result = self.execute(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        saved = self.read_csv("consolidated_exact_dedup.csv")
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["Journal"], "Sample journal")
        self.assertEqual(saved[0]["_norm_doi"], "10.1234/a")

    def test_invalid_file_quarantined_but_clean_other_file_processed(self):
        bad = self.root / "bad.csv"
        good = self.root / "good.csv"
        bad.write_text(
            "Title,Title,DOI\nOne,Two,10.1234/a\n",
            encoding="utf-8",
        )
        good.write_text("Title,DOI\nValid,10.1234/valid\n",
                        encoding="utf-8")
        result = self.execute(bad, good)
        self.assertEqual(result.returncode, 0, result.stderr)
        accepted = self.read_csv("consolidated_exact_dedup.csv")
        self.assertEqual(len(accepted), 1)
        self.assertEqual(accepted[0]["Title"], "Valid")
        rejected = self.read_csv("rejected_records.csv")
        self.assertEqual(len(rejected), 1)
        self.assertEqual(rejected[0]["_reject_reason"], "DUPLICATE_HEADER")
        manifest = json.loads((self.out / "import_sources_manifest.json").read_text())
        self.assertEqual([r["read_status"] for r in manifest["inputs"]],
                         ["DUPLICATE_HEADER", "READABLE"])

    def test_scopus_authors_and_author_full_names_are_complementary(self):
        # Synthetically reconstructed from documented Scopus CSV field layout.
        path = self.root / "scopus_representative.csv"
        with path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["Authors", "Author full names", "Author(s) ID",
                             "Title", "Year", "Source title", "DOI", "EID"])
            writer.writerow(["Silva, M.", "Silva, Maria", "12345678900",
                             "A bibliometric study", "2025", "Journal X",
                             "10.1234/scopus", "2-s2.0-12345"])
        result = self.execute(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        records = self.read_csv("consolidated_exact_dedup.csv")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["Authors"], "Silva, M.")
        self.assertEqual(records[0]["Author full names"], "Silva, Maria")
        self.assertEqual(records[0]["_first_author"], "silvam")
        self.assertEqual(records[0]["_norm_doi"], "10.1234/scopus")
        self.assertEqual(self.read_csv("rejected_records.csv"), [])

    def test_wos_tagged_columns_au_af_ti_py_di_are_complementary(self):
        # Representative WoS tab-delimited tags (not an actual licensed export).
        path = self.root / "wos_representative.tsv"
        with path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh, delimiter="\t")
            writer.writerow(["AU", "AF", "TI", "PY", "DI", "UT"])
            writer.writerow(["Souza, A", "Souza, Ana", "A public administration study",
                             "2024", "10.1234/wos", "WOS:000000"])
        result = self.execute(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        record = self.read_csv("consolidated_exact_dedup.csv")[0]
        self.assertEqual(record["AU"], "Souza, A")
        self.assertEqual(record["AF"], "Souza, Ana")
        self.assertEqual(record["_first_author"], "souzaa")
        self.assertEqual(record["_norm_doi"], "10.1234/wos")
        self.assertEqual(self.read_csv("rejected_records.csv"), [])

    def test_wos_long_headers_authors_and_full_names_are_complementary(self):
        path = self.root / "wos_long.tsv"
        with path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh, delimiter="\t")
            writer.writerow(["Authors", "Author Full Names", "Article Title",
                             "Publication Year", "DOI"])
            writer.writerow(["Costa, J", "Costa, João", "Public governance",
                             "2023", "10.1234/governance"])
        result = self.execute(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        row = self.read_csv("consolidated_exact_dedup.csv")[0]
        self.assertEqual(row["Authors"], "Costa, J")
        self.assertEqual(row["Author Full Names"], "Costa, João")
        self.assertEqual(row["_norm_title"], "public governance")

    def test_wos_full_names_af_can_stand_alone_without_au(self):
        path = self.root / "wos_fullonly.tsv"
        with path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh, delimiter="\t")
            writer.writerow(["AF", "TI", "PY"])
            writer.writerow(["Barros, Carla", "Digitalization and governance", "2022"])
        result = self.execute(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.read_csv("consolidated_exact_dedup.csv")[0]["_first_author"],
                         "barroscarla")

    def test_two_short_author_aliases_remain_ambiguous(self):
        path = self.root / "short_aliases.csv"
        path.write_text(
            "Authors,Author names,Author full names,Title,Year\n"
            "Smith J,Smith John,Smith John,Research,2025\n",
            encoding="utf-8",
        )
        self.assert_quarantine(path, "AMBIGUOUS_BIBLIOGRAPHIC_HEADERS", 1)

    def test_title_synonyms_still_quarantined_even_if_equal(self):
        path = self.root / "title_aliases.csv"
        path.write_text(
            "Title,Article Title,DOI\nSame title,Same title,10.1234/same\n",
            encoding="utf-8",
        )
        self.assert_quarantine(path, "AMBIGUOUS_BIBLIOGRAPHIC_HEADERS", 1)

    def test_wos_doi_tag_and_doi_header_remain_ambiguous(self):
        path = self.root / "doi_aliases.tsv"
        path.write_text(
            "DI\tDOI\tTI\n10.1234/a\t10.1234/b\tExample\n",
            encoding="utf-8",
        )
        self.assert_quarantine(path, "AMBIGUOUS_BIBLIOGRAPHIC_HEADERS", 1)

    @unittest.skipUnless(importlib.util.find_spec("openpyxl"),
                         "Optional openpyxl is unavailable in this environment")
    def test_xlsx_complementary_authors_still_valid(self):
        from openpyxl import Workbook
        path = self.root / "scopus_repr.xlsx"
        book = Workbook()
        book.active.append(["Authors", "Author full names", "Title", "DOI"])
        book.active.append(["Lima, R.", "Lima, Regina", "Governance", "10.1234/xlsx"])
        book.save(path)
        book.close()
        result = self.execute(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = self.read_csv("consolidated_exact_dedup.csv")[0]
        self.assertEqual(data["Authors"], "Lima, R.")
        self.assertEqual(data["Author full names"], "Lima, Regina")

    @unittest.skipUnless(importlib.util.find_spec("openpyxl"),
                         "Optional openpyxl is unavailable in this environment")
    def test_xlsx_duplicate_header_does_not_overwrite_cells(self):
        from openpyxl import Workbook
        path = self.root / "duplicate.xlsx"
        book = Workbook()
        sheet = book.active
        sheet.append(["Title", "Title", "DOI"])
        sheet.append(["First title", "Second title", "10.1234/a"])
        book.save(path)
        book.close()
        rows = self.assert_quarantine(path, "DUPLICATE_HEADER", 1)
        self.assertIn("First title", rows[0]["_raw_record"])
        self.assertIn("Second title", rows[0]["_raw_record"])


if __name__ == "__main__":
    unittest.main()
