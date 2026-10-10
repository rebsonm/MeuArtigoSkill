"""Regression tests for the read-only Meu Artigo Visual projection."""
import csv
import importlib.util
import json
import tempfile
import unittest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from datetime import date
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "visual_dashboard.py"
spec = importlib.util.spec_from_file_location("visual_dashboard", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class VisualDashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = self.root / "00_Gestao_e_Continuidade"
        self.base.mkdir()
        (self.base / "PROJECT_CONFIG.json").write_text(json.dumps({
            "project_name": "Artigo <teste>", "presentation_mode": "MINIMAL",
            "storage_mode": "GOOGLE_DRIVE_STAGING",
            "storage_state": "DRIVE_STAGING_PENDING_UPLOAD"
        }), encoding="utf8")

    def rows(self, filename, rows):
        path = self.base / filename
        with path.open("w", encoding="utf-8-sig", newline="") as out:
            w = csv.DictWriter(out, fieldnames=list(dict.fromkeys(k for row in rows for k in row)))
            w.writeheader()
            w.writerows(rows)

    def test_empty_registers_are_unknown_not_success(self):
        d = mod.view(self.root)
        self.assertIsNone(d["operational"]["completion_percent"])
        self.assertIsNone(d["scientific"]["gates_total"])
        self.assertIsNone(d["synchronization"]["drive_synchronized_now"])
        self.assertTrue(d["missing_registers"])

    def test_no_false_scientific_approvals(self):
        self.rows("11_CADA_Control.csv", [
            {"CADA_ID": "CADA-0001", "Status": "DONE", "Completion_evidence": "receipt"},
            {"CADA_ID": "CADA-0002", "Status": "READY", "Next_action": "Revisar"},
        ])
        self.rows("18_Human_Validation_Gates.csv", [
            {"GATE_ID": "GATE-0001", "Name": "Questão", "Status": "COMPLETED",
             "Decision": "APPROVED", "Validated_by": "", "Validation_evidence": ""},
            {"GATE_ID": "GATE-0002", "Name": "Método", "Status": "READY",
             "Decision": "PENDING", "Validated_by": "", "Validation_evidence": ""},
        ])
        d = mod.view(self.root)
        self.assertEqual(d["operational"]["completion_percent"], 50)
        self.assertEqual(d["scientific"]["gates_approved_documented"], 0)
        self.assertEqual(d["scientific"]["next_ready_gate"]["id"], "GATE-0002")
        self.assertEqual(d["operational"]["next_action"]["id"], "CADA-0002")
        self.assertNotIn("tasks", d["scientific"])

    def test_recorded_gate_proof_only_not_identity_authentication(self):
        self.rows("18_Human_Validation_Gates.csv", [
            {"GATE_ID": "GATE-0001", "Name": "Questão", "Status": "COMPLETED",
             "Decision": "APPROVED", "Validated_by": "researcher",
             "Validation_evidence": "document-ref"},
        ])
        d = mod.view(self.root, mode="FULL")
        self.assertEqual(d["scientific"]["gates_approved_documented"], 1)
        self.assertFalse(d["project"]["storage_verified_in_this_session"])

    def test_overdue_and_blocked_not_next_action(self):
        self.rows("11_CADA_Control.csv", [
            {"CADA_ID": "CADA-0001", "Status": "BLOCKED", "Next_action": "Bloqueada",
             "Deadline": "2026-01-01", "Priority": "HIGH"},
            {"CADA_ID": "CADA-0002", "Status": "READY", "Next_action": "Próxima",
             "Deadline": "", "Priority": "LOW"},
        ])
        d = mod.view(self.root, today=date(2026, 10, 10))
        self.assertEqual(d["operational"]["tasks_overdue"], 1)
        self.assertEqual(d["operational"]["tasks_blocked"], 1)
        self.assertEqual(d["operational"]["next_action"]["action"], "Próxima")

    def test_unrecorded_source_is_not_read(self):
        self.rows("02_Search_Log.csv", [{"Status": "PLANNED", "Records_found": "250"}])
        d = mod.view(self.root)
        self.assertEqual(d["scientific"]["searches_logged"], 1)
        self.assertEqual(d["scientific"]["searches_marked_complete_in_register"], 0)
        self.assertNotIn("250", json.dumps(d))

    def test_missing_config_is_error(self):
        (self.base / "PROJECT_CONFIG.json").unlink()
        with self.assertRaises(ValueError):
            mod.view(self.root)

    def test_read_only_does_not_touch_source_files(self):
        before = {p.name: p.read_bytes() for p in self.base.iterdir()}
        mod.view(self.root)
        after = {p.name: p.read_bytes() for p in self.base.iterdir()}
        self.assertEqual(before, after)

    def test_text_fallback(self):
        s = mod.plain_text(mod.view(self.root))
        self.assertIn("Próxima ação:", s)
        self.assertIn("não equivale", s)

if __name__ == "__main__":
    unittest.main()
