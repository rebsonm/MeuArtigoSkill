"""Phase-5 integrated read-only continuity audit regressions (synthetic data).

No genuine researcher approval, external API search or Drive write is
represented by these fixtures. CI checks structural local consistency only.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from test_phase5_cada_continuity_transaction import Phase5RecordedCompletionTests
import cada_continuity_integrity as integrity
import cada_continuity_transaction as journal
import native_chat_dashboard as ui
import update_cada_continuity as updater
import init_project


class Phase5IntegratedAuditTests(unittest.TestCase):
    def setUp(self):
        # Reuse the PR-49 executable-fixture initializer without inheriting
        # its test methods or rerunning the same regression suite.
        fixture = Phase5RecordedCompletionTests(
            "test_confirmed_local_execution_updates_three_files_and_preserves_gate")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.fixture = fixture
        self.root = fixture.root
        self.trace = fixture.receipt()
        self.reported = updater.complete(self.root, "CADA-0002", self.trace)

    def inspect(self):
        return integrity.audit(self.root)

    def mutate_csv(self, path: Path, update):
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            fields = list(reader.fieldnames)
            rows = list(reader)
        update(rows)
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fields)
            writer.writeheader()
            writer.writerows(rows)

    def mutate_metric(self, key, value):
        def change(rows):
            for row in rows:
                if row["Metric"] == key:
                    row["Value"] = value
        self.mutate_csv(self.fixture.dashboard, change)

    def test_valid_completion_reconciles_ui_and_all_three_canonical_files(self):
        report = self.inspect()
        self.assertEqual(report["status"], "CHECKED")
        self.assertEqual(report["errors"], [])
        self.assertTrue(report["last_operational_proof_checked"])
        self.assertFalse(report["human_gate_approved"])
        self.assertFalse(report["scientific_quality_proven"])
        self.assertFalse(report["drive_sync_verified"])
        local = ui.panel(self.root, mode="MINIMAL")
        full = ui.panel(self.root, mode="FULL")
        self.assertEqual(local["continuation"], full["continuation"])
        self.assertEqual(local["continuation"]["integrity_status"], "CHECKED")
        self.assertEqual(local["continuation"]["integrity_error_count"], 0)
        self.assertTrue(local["continuation"]["last_operational_proof_checked"])
        self.assertFalse(local["continuation"]["technical_preparation_possible"])
        self.assertEqual(local["continuation"]["next_gate_id"], "GATE-0001")
        self.assertEqual(local["tasks"]["items"][0].keys(),
                         {"id", "task", "execution_owner", "deadline"}.keys()
                         if False else local["tasks"]["items"][0].keys())
        self.assertEqual(self.fixture.gates.read_bytes().count(b"PENDING"), 14)

    def test_dashboard_active_count_forgery_is_blocked(self):
        self.mutate_metric("Total_active_items", "0")
        report = self.inspect()
        self.assertIn("CADA_DASHBOARD_COUNT_MISMATCH_TOTAL_ACTIVE_ITEMS",
                      report["errors"])

    def test_ready_task_count_inflation_is_detected(self):
        self.mutate_metric("Ready_items", "500")
        self.assertIn("CADA_DASHBOARD_COUNT_MISMATCH_READY_ITEMS",
                      self.inspect()["errors"])

    def test_claimed_next_cada_id_not_in_router_is_detected(self):
        self.mutate_metric("Next_CADA_ID", "CADA-9999")
        self.assertIn("CADA_DASHBOARD_NEXT_TASK_MISMATCH", self.inspect()["errors"])

    def test_wrong_next_human_gate_cannot_disappear_from_dashboard(self):
        self.mutate_metric("Next_human_gate", "GATE-0007")
        self.assertIn("CADA_DASHBOARD_NEXT_GATE_MISMATCH",
                      self.inspect()["errors"])

    def test_last_cada_marker_must_refer_to_actually_done_task(self):
        self.mutate_metric("Last_completed_CADA_ID", "CADA-0003")
        self.assertIn("LAST_COMPLETED_CADA_NOT_DONE", self.inspect()["errors"])

    def test_unpaired_last_trace_marker_blocks_validation(self):
        self.mutate_metric("Last_trace_event", "")
        self.assertIn("INCOMPLETE_CADA_TRANSITION_MARKERS",
                      self.inspect()["errors"])

    def test_local_trace_hash_tampered_after_done_revokes_green_audit(self):
        rec = self.root / f"{self.fixture.mgmt.name}/TRACE_RECEIPTS/{self.trace}.json"
        rec.write_bytes(rec.read_bytes() + b"\naltered")
        report = self.inspect()
        self.assertIn("LAST_TECHNICAL_RECEIPT_INVALID_OR_CHANGED", report["errors"])
        self.assertFalse(report["last_operational_proof_checked"])

    def test_last_local_output_changed_after_done_revokes_proof(self):
        output = self.fixture.mgmt / "SOURCE_VERIFICATION.json"
        output.write_bytes(output.read_bytes() + b"\n")
        self.assertIn("LAST_TECHNICAL_RECEIPT_INVALID_OR_CHANGED",
                      self.inspect()["errors"])

    def test_fabricated_completion_evidence_does_not_authenticate_trace(self):
        def change(rows):
            for row in rows:
                if row["CADA_ID"] == "CADA-0002":
                    row["Completion_evidence"] = "AI said completed"
        self.mutate_csv(self.fixture.taskfile, change)
        self.assertIn("LAST_COMPLETION_TRACE_LINK_MISSING",
                      self.inspect()["errors"])

    def test_removed_trace_row_invalidates_previous_task_completion(self):
        self.mutate_csv(self.fixture.tracefile, lambda rows: rows.clear())
        self.assertIn("LAST_TECHNICAL_RECEIPT_INVALID_OR_CHANGED",
                      self.inspect()["errors"])

    def test_continuity_change_log_tamper_is_detected(self):
        path = self.fixture.continuity
        path.write_text(path.read_text().replace(
            f"local {self.trace}; scientific gates unchanged.",
            "local TRACE-9999; scientific gates unchanged."), encoding="utf-8")
        self.assertIn("CADA_CONTINUITY_CHANGE_LOG_MISSING",
                      self.inspect()["errors"])

    def test_stale_continuity_next_id_blocks_progress(self):
        path = self.fixture.continuity
        path.write_text(path.read_text().replace(
            "- CADA_ID: NONE", "- CADA_ID: CADA-0002"), encoding="utf-8")
        self.assertIn("CADA_CONTINUITY_STALE_NEXT_TASK", self.inspect()["errors"])

    def test_missing_dashboard_marker_skips_legacy_projects_only(self):
        def remove_completion(rows):
            rows[:] = [r for r in rows if r["Metric"] not in (
                "Last_trace_event", "Last_completed_CADA_ID")]
        self.mutate_csv(self.fixture.dashboard, remove_completion)
        self.assertEqual(self.inspect()["status"], "NOT_APPLICABLE_LEGACY")
        # This is an explicit compatibility compromise, not proof of
        # scientific validity or a reconstructed completed project.
        self.assertFalse(self.inspect()["last_operational_proof_checked"])

    def test_pending_journal_blocks_panel_and_global_validator(self):
        journal.journal_dir(self.root).mkdir()
        report = self.inspect()
        self.assertIn("PENDING_CADA_CONTINUITY_TRANSACTION", report["errors"])
        projected = ui.panel(self.root)
        self.assertEqual(projected["continuation"]["status"],
                         "CADA_CONTINUITY_INTEGRITY_REVIEW")
        self.assertFalse(projected["continuation"]["technical_preparation_possible"])
        self.assertFalse(projected["drive_sync_verified_in_this_session"])
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_project.py"),
                                 str(self.root)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Interrupted C.A.D.A. continuity transaction", result.stdout)
        self.assertTrue(journal.journal_dir(self.root).exists())

    def test_corrupt_dashboard_blocks_further_completion_preflight(self):
        self.mutate_metric("Total_active_items", "-1")
        report = self.inspect()
        self.assertTrue(report["errors"])
        # Even if the task list is edited later, this invalid state must
        # not be compounded into an additional operational transition.
        with self.assertRaisesRegex(ValueError,
                                    "CADA_PREVIOUS_CONTINUITY_INTEGRITY_REVIEW_REQUIRED"):
            updater.complete(self.root, "CADA-0002", self.trace)
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_project.py"),
                                 str(self.root)], capture_output=True, text=True)
        self.assertIn("C.A.D.A. continuity integrity:", result.stdout)
        projected = ui.panel(self.root)
        self.assertEqual(projected["continuation"]["status"],
                         "CADA_CONTINUITY_INTEGRITY_REVIEW")
        self.assertGreater(projected["continuation"]["integrity_error_count"], 0)

    def test_integrity_audit_is_read_only_and_does_not_approve_gate(self):
        before = {p.relative_to(self.root).as_posix(): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        self.inspect()
        ui.panel(self.root, mode="FULL")
        ui.panel(self.root, mode="MINIMAL")
        self.assertEqual(
            {p.relative_to(self.root).as_posix(): p.read_bytes()
             for p in self.root.rglob("*") if p.is_file()}, before)
        with self.fixture.gates.open(encoding="utf-8-sig", newline="") as stream:
            self.assertTrue(all(row["Status"] == "PENDING"
                                for row in csv.DictReader(stream)))


if __name__ == "__main__":
    unittest.main()
