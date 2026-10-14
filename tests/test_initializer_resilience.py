"""Emergency initializer regressions based on the October 2026 external beta.4 report.

Synthetic disposable local fixtures only. These tests do not claim Drive sync,
scientific validation, or any external research activity.
"""
from __future__ import annotations

import contextlib
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import init_project

MGMT = "00_Gestao_e_Continuidade"


def fake_workbook(path: Path):
    """Small valid ZIP fixture for validating the initializer's XLSX boundary."""
    with zipfile.ZipFile(path, "w") as workbook:
        workbook.writestr("[Content_Types].xml", "<Types/>")
        workbook.writestr("xl/workbook.xml", "<workbook/>")


class InitializerResilienceTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        # The project path derives from the actual runtime year.
        self.project = self.base / f"ARTIGO_Resilience-Test_{init_project.date.today().year}"
        self.mgmt = self.project / MGMT

    def run_initializer(self, on_generate):
        args = [
            "init_project.py", "--path", str(self.base),
            "--name", "Resilience Test",
            "--problem", "Synthetic question for offline software regression",
            "--storage-mode", "WORK_FALLBACK",
            "--fallback-authorized-by", "SYNTHETIC_FIXTURE_USER",
        ]
        stdout,stderr = io.StringIO(),io.StringIO()
        with patch.object(sys, "argv", args), patch.object(init_project.subprocess, "run", side_effect=on_generate) as called, contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = init_project.main()
        return result, stdout.getvalue(), stderr.getvalue(), called

    def read_config(self):
        return json.loads((self.mgmt / "PROJECT_CONFIG.json").read_text(encoding="utf-8"))

    def assert_core_ready(self):
        self.assertTrue((self.mgmt / "PROTOCOLO.md").is_file())
        self.assertIn("# PROTOCOLO", (self.mgmt / "PROTOCOLO.md").read_text(encoding="utf-8"))
        self.assertTrue((self.mgmt / "CONTINUIDADE.md").is_file())
        self.assertEqual(self.read_config()["status"], "INITIALIZED")
        self.assertEqual(self.read_config()["local_core_status"], "VERIFIED")
        self.assertEqual(init_project.core_issues(self.project), [])
        with (self.mgmt / "11_CADA_Control.csv").open(encoding="utf-8-sig", newline="") as f:
            first = next(csv.DictReader(f))
        self.assertEqual(first["Status"], "DONE")
        self.assertNotIn("matrix generated", first["Completion_evidence"])
        self.assertNotIn("Drive sync verified", first["Completion_evidence"])
        with (self.mgmt / "18_Human_Validation_Gates.csv").open(encoding="utf-8-sig", newline="") as f:
            gates = list(csv.DictReader(f))
        self.assertEqual(len(gates), 7)
        self.assertTrue(all(x["Decision"] == "PENDING" for x in gates))

    def test_generator_timeout_keeps_protocol_and_core_ready(self):
        def hangs(command, **kwargs):
            self.assertEqual(kwargs["timeout"], 90)
            self.assert_core_ready()
            self.assertEqual(self.read_config()["visual_matrix_status"], "PENDING_GENERATION")
            raise subprocess.TimeoutExpired(command, timeout=kwargs["timeout"])

        status,out,err,called = self.run_initializer(hangs)
        self.assertEqual(status, 0, err)
        self.assertEqual(called.call_count, 1)
        self.assertIn("matrix_status=PENDING_TIMEOUT", out)
        self.assert_core_ready()
        self.assertEqual(self.read_config()["visual_matrix_status"], "PENDING_TIMEOUT")
        self.assertFalse(list(self.mgmt.glob(".matrix-*.xlsx")))
        self.assertFalse(list(self.mgmt.glob("MATRIZ_MESTRA_*.xlsx")))

    def test_failed_generator_never_leaves_partial_xlsx(self):
        def fails(command, **kwargs):
            Path(command[command.index("--output") + 1]).write_bytes(b"partial ZIP")
            raise subprocess.CalledProcessError(2, command, stderr="synthetic failure")

        status,out,err,_ = self.run_initializer(fails)
        self.assertEqual(status, 0, err)
        self.assertIn("PENDING_GENERATOR_FAILED", out)
        self.assert_core_ready()
        self.assertFalse(list(self.mgmt.glob(".matrix-*.xlsx")))
        self.assertFalse(list(self.mgmt.glob("MATRIZ_MESTRA_*.xlsx")))

    def test_dependency_unavailable_is_distinct_from_generator_failure(self):
        def unavailable(command, **kwargs):
            raise subprocess.CalledProcessError(
                2, command, stderr="XLSX_UNAVAILABLE: optional artifact_tool is unavailable")
        status,out,err,_=self.run_initializer(unavailable)
        self.assertEqual(status,0,err)
        self.assertIn("PENDING_XLSX_DEPENDENCY_UNAVAILABLE",out)
        self.assert_core_ready()

    def test_optional_filesystem_error_preserves_local_core(self):
        with patch.object(init_project, "build_optional_visual_matrix", side_effect=OSError("synthetic disk error")):
            status,out,err,called=self.run_initializer(
                lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("no subprocess")))
        self.assertEqual(status,0,err)
        self.assertIn("PENDING_FILESYSTEM_ERROR",out)
        called.assert_not_called()
        self.assert_core_ready()

    def test_successful_generation_promotes_only_verified_workbook(self):
        def generated(command, **kwargs):
            self.assert_core_ready()
            fake_workbook(Path(command[command.index("--output") + 1]))
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

        status,out,err,_=self.run_initializer(generated)
        self.assertEqual(status,0,err)
        self.assertIn("matrix_status=CREATED_VERIFIED",out)
        workbook=next(self.mgmt.glob("MATRIZ_MESTRA_*.xlsx"))
        self.assertTrue(init_project.valid_visual_workbook(workbook))
        self.assert_core_ready()

        def must_not_regenerate(*args, **kwargs):
            raise AssertionError("verified workbook must never be regenerated")
        status,out,err,called=self.run_initializer(must_not_regenerate)
        self.assertEqual(status,0,err)
        self.assertIn("matrix_status=EXISTS_VERIFIED",out)
        called.assert_not_called()

    def test_resume_partial_workspace_without_overwriting_researcher_document(self):
        status,_,err,_=self.run_initializer(
            lambda command, **kw: (_ for _ in ()).throw(subprocess.TimeoutExpired(command, 90)))
        self.assertEqual(status,0,err)
        continuity=self.mgmt/"CONTINUIDADE.md"
        continuity.write_text(continuity.read_text(encoding="utf-8")+"\nUser-edited continuity note\n",encoding="utf-8")
        (self.mgmt/"PROTOCOLO.md").unlink()

        def regenerated(command, **kwargs):
            self.assert_core_ready()
            fake_workbook(Path(command[command.index("--output") + 1]))
            return subprocess.CompletedProcess(command, 0)

        status,out,err,_=self.run_initializer(regenerated)
        self.assertEqual(status,0,err)
        self.assertIn("CREATED_VERIFIED",out)
        self.assertIn("User-edited continuity note",continuity.read_text(encoding="utf-8"))
        self.assert_core_ready()

    def test_invalid_existing_xlsx_is_not_replaced(self):
        self.run_initializer(lambda command, **kw: (_ for _ in ()).throw(subprocess.TimeoutExpired(command,90)))
        workbook=self.mgmt/"MATRIZ_MESTRA_Resilience-Test.xlsx"
        workbook.write_bytes(b"user-controlled-corrupted-workbook")
        status,out,err,called=self.run_initializer(
            lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("must not overwrite")))
        self.assertEqual(status,0,err)
        self.assertIn("INVALID_EXISTING_XLSX_REQUIRES_REVIEW",out)
        called.assert_not_called()
        self.assertEqual(workbook.read_bytes(),b"user-controlled-corrupted-workbook")
        self.assert_core_ready()

    def test_corrupted_canonical_table_blocks_init_instead_of_claiming_success(self):
        self.run_initializer(lambda command, **kw: (_ for _ in ()).throw(subprocess.TimeoutExpired(command,90)))
        target=self.mgmt/"02_Search_Log.csv"
        target.write_text("unexpected,headers\n",encoding="utf-8")
        status,out,err,called=self.run_initializer(
            lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("must block")))
        self.assertEqual(status,2)
        self.assertIn("CORE_INVALID: Invalid table header",err)
        self.assertEqual(self.read_config()["status"],"INITIALIZATION_BLOCKED")
        self.assertEqual(self.read_config()["local_core_status"],"INVALID")
        self.assertEqual(target.read_text(encoding="utf-8"),"unexpected,headers\n")
        called.assert_not_called()


if __name__ == "__main__":
    unittest.main()
