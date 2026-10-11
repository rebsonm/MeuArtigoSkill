"""Optional Excel parser absence is isolated and does not discard valid sources."""
from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
IMPORTER = ROOT / "scripts" / "dedupe_records.py"


class OptionalExcelDependencyIsolationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def run_import_with_missing_module(self, extension: str, module: str, add_valid_csv: bool):
        case = self.root / extension.lstrip(".") / ("mixed" if add_valid_csv else "only")
        case.mkdir(parents=True)
        stub = case / "missing_module"
        stub.mkdir()
        (stub / (module + ".py")).write_text(
            'raise ImportError("simulated optional module unavailable")\n', encoding="utf-8")
        missing = case / ("historical" + extension)
        original = b"synthetic input placeholder, not a real spreadsheet"
        missing.write_bytes(original)
        inputs = [str(missing)]
        if add_valid_csv:
            valid = case / "valid.csv"
            with valid.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["Title", "DOI"])
                writer.writeheader()
                writer.writerow({"Title": "Valid independent article", "DOI": "10.1234/independent"})
            inputs.append(str(valid))
        out = case / "out"
        env = os.environ.copy()
        env["PYTHONPATH"] = str(stub) + os.pathsep + env.get("PYTHONPATH", "")
        done = subprocess.run(
            [sys.executable, str(IMPORTER), *inputs, "--out-dir", str(out)],
            capture_output=True, text=True, env=env,
        )
        return done, out, missing, original

    def test_missing_optional_reader_does_not_abort_valid_csv(self):
        for extension, module in [(".xls", "xlrd"), (".xlsx", "openpyxl")]:
            with self.subTest(extension=extension):
                done, out, missing, original = self.run_import_with_missing_module(
                    extension, module, True)
                self.assertEqual(done.returncode, 0, done.stderr)
                manifest = json.loads((out / "import_sources_manifest.json").read_text())
                self.assertEqual(
                    [x["read_status"] for x in manifest["inputs"]],
                    ["MISSING_OPTIONAL_EXCEL_PARSER", "READABLE"])
                self.assertEqual(
                    manifest["inputs"][0]["content_sha256"],
                    hashlib.sha256(original).hexdigest())
                self.assertEqual(missing.read_bytes(), original)
                diagnostic = json.loads((out / "import_diagnostics.json").read_text())
                self.assertTrue(any(
                    item["reason"] == "MISSING_OPTIONAL_EXCEL_PARSER"
                    for item in diagnostic["diagnostics"]))
                with (out / "consolidated_exact_dedup.csv").open(
                        newline="", encoding="utf-8-sig") as handle:
                    records = list(csv.DictReader(handle))
                self.assertEqual(len(records), 1)
                self.assertEqual(records[0]["_norm_doi"], "10.1234/independent")

    def test_only_missing_optional_reader_fails_with_persisted_diagnostics(self):
        for extension, module in [(".xls", "xlrd"), (".xlsx", "openpyxl")]:
            with self.subTest(extension=extension):
                done, out, _, _ = self.run_import_with_missing_module(
                    extension, module, False)
                self.assertEqual(done.returncode, 2, done.stderr)
                diagnostic = json.loads((out / "import_diagnostics.json").read_text())
                self.assertEqual(diagnostic["canonical_after_exact_dedup"], 0)
                self.assertEqual(
                    diagnostic["diagnostics"][0]["reason"],
                    "MISSING_OPTIONAL_EXCEL_PARSER")
                self.assertFalse((out / "consolidated_exact_dedup.csv").exists())
                self.assertFalse((out / ".dedupe_import_in_progress").exists())


if __name__ == "__main__":
    unittest.main()
