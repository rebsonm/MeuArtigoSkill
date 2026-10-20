"""Adversarial output confinement tests for REG-018, REG-011 and REG-013.

All inputs are synthetic; no canonical source file is modified.
"""
from __future__ import annotations
from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import report_output_guard as guard
import reference_audit as ref
import semantic_claim_review as sem
import scientific_diagnostic as diag


class ReportOutputGuardTests(unittest.TestCase):
    def setUp(self):
        td=tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self.root=Path(td.name)
        self.m=self.root/"00_Gestao_e_Continuidade"
        self.m.mkdir()
        self.records={}
        for name in ("18_Human_Validation_Gates.csv", "PROJECT_CONFIG.json",
                     "CONTINUIDADE.md", "09_Claims_Ledger.csv",
                     "05_Evidence_Matrix.csv", "01_Protocolo.csv",
                     "17_Decision_Log.csv"):
            p=self.m/name
            p.write_bytes(("PRIVATE_UNMODIFIED_"+name).encode())
            self.records[name]=p.read_bytes()
        self.writers=(
            lambda dest: ref._write_output(self.root,dest,{"audit":"synthetic"}),
            lambda dest: sem.save_local(self.root,dest,{"audit":"synthetic"},None),
            lambda dest: diag.output_file(self.root,dest,"synthetic",None),
        )

    def assert_preserved(self):
        for name,original in self.records.items():
            self.assertEqual((self.m/name).read_bytes(),original,name)

    def test_all_writers_reject_every_critical_canonical_target(self):
        for writer in self.writers:
            for name in self.records:
                with self.subTest(writer=writer,name=name):
                    with self.assertRaisesRegex(ValueError,"98_Technical_Reports"):
                        writer(self.m/name)
            self.assert_preserved()

    def test_all_writers_reject_arbitrary_existing_project_files(self):
        unrelated=self.root/"05_Manuscrito"/"canonical.md"
        unrelated.parent.mkdir()
        unrelated.write_text("PROTECTED_ORIGINAL",encoding="utf-8")
        for writer in self.writers:
            with self.assertRaisesRegex(ValueError,"98_Technical_Reports"):
                writer(unrelated)
        self.assertEqual(unrelated.read_text(encoding="utf-8"),"PROTECTED_ORIGINAL")

    def test_all_writers_reject_outside_and_traversal(self):
        for writer in self.writers:
            with self.assertRaises(ValueError):
                writer(self.root.parent/"outside-report.json")
            with self.assertRaises(ValueError):
                writer(Path("98_Technical_Reports")/".."/"PROJECT_CONFIG.json")
        self.assertFalse((self.root.parent/"outside-report.json").exists())

    def test_all_writers_reject_existing_report_files_including_symlink(self):
        out=self.root/guard.REPORTS
        out.mkdir()
        existing=out/"existing.json"
        existing.write_text("DO_NOT_OVERWRITE",encoding="utf-8")
        for writer in self.writers:
            with self.assertRaises(FileExistsError):
                writer(existing)
        self.assertEqual(existing.read_text(encoding="utf-8"),"DO_NOT_OVERWRITE")
        guard.write_report(self.root,Path(guard.REPORTS)/"new.txt","first",
                           allowed_extensions=frozenset({".txt"}))
        with self.assertRaises(FileExistsError):
            guard.write_report(self.root,Path(guard.REPORTS)/"new.txt","overwrite",
                               allowed_extensions=frozenset({".txt"}))
        self.assertEqual((out/"new.txt").read_text(),"first")

    def test_symlinked_report_directory_is_denied(self):
        if not hasattr(Path,"symlink_to"):
            self.skipTest("No symbolic links available")
        external=self.root/"not-for-reports"
        external.mkdir()
        link=self.root/guard.REPORTS
        try:
            link.symlink_to(external,target_is_directory=True)
        except (NotImplementedError, OSError):
            self.skipTest("Symbolic links unavailable")
        for writer in self.writers:
            with self.assertRaises(ValueError):
                writer(Path(guard.REPORTS)/"trial.json")
        self.assertEqual(list(external.iterdir()),[])

    def test_symlink_output_is_denied_even_when_target_outside(self):
        out=self.root/guard.REPORTS
        out.mkdir()
        target=self.root/"private.txt"
        target.write_text("PRIVATE",encoding="utf-8")
        link=out/"linked.json"
        try:
            link.symlink_to(target)
        except (NotImplementedError, OSError):
            self.skipTest("Symbolic links unavailable")
        for writer in self.writers:
            with self.assertRaises(FileExistsError):
                writer(link)
        self.assertEqual(target.read_text(),"PRIVATE")

    def test_each_writer_can_create_new_scoped_report(self):
        ref._write_output(self.root,Path(guard.REPORTS)/"references.json",{"test":1})
        sem.save_local(self.root,Path(guard.REPORTS)/"claims.json",{"test":2},None)
        diag.output_file(self.root,Path(guard.REPORTS)/"diagnosis.html",
                         "<html>synthetic</html>",None)
        self.assertTrue((self.root/guard.REPORTS/"references.json").is_file())
        self.assertTrue((self.root/guard.REPORTS/"claims.json").is_file())
        self.assertTrue((self.root/guard.REPORTS/"diagnosis.html").is_file())
        self.assert_preserved()

    def test_reject_wrong_extensions_and_nested_paths(self):
        with self.assertRaises(ValueError):
            ref._write_output(self.root,Path(guard.REPORTS)/"not-json.html",{})
        with self.assertRaises(ValueError):
            sem.save_local(self.root,Path(guard.REPORTS)/"script.py",{},None)
        with self.assertRaises(ValueError):
            diag.output_file(self.root,Path(guard.REPORTS)/"nested"/"report.html","x",None)
        with self.assertRaises(ValueError):
            diag.output_file(self.root,Path(guard.REPORTS)/"invalid:name.html","x",None)

if __name__=="__main__":
    unittest.main()
