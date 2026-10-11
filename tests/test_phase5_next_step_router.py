"""Synthetic Phase-5 continuation tests. No human decisions or Drive writes.

The command 'próximo' is navigation intent, not scientific consent. All
gate fields and operational statuses here are disposable test fixtures.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import next_step_router as router
import native_chat_dashboard as panel
import init_project


def table(path, headers, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerows([{header: row.get(header, "") for header in headers} for row in rows])


class NextStepPhase5Tests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.mgmt = self.root / router.MGMT
        self.mgmt.mkdir()
        self.config = self.mgmt / "PROJECT_CONFIG.json"
        self.config.write_text(json.dumps({
            "storage_mode": "WORK_FALLBACK",
            "fallback_authorized": True,
            "presentation_mode": "MINIMAL",
            "work_management_mode": "MATRIX_ONLY",
        }), encoding="utf-8")
        self.continuity = self.root / router.CONTINUITY
        self.continuity.write_text(
            "# Synthetic research continuity\nNext valid action: CADA-0002\n"
            "PRIVATE_RESEARCH_CONTEXT_AND_REVIEW_NOTES", encoding="utf-8")
        self.tasks = [
            {"CADA_ID": "CADA-0001", "Title": "Initialize",
             "Status": "DONE", "Execution_mode": "AUTONOMOUS",
             "Completion_evidence": "Synthetic setup receipt", "Scientific_stage": "00"},
            {"CADA_ID": "CADA-0002", "Title": "Prepare fictional literature audit",
             "Next_action": "CONTAINS_PRIVATE_LITERATURE_INSTRUCTIONS",
             "Status": "READY", "Execution_mode": "AUTONOMOUS_WITH_USER_DECISIONS",
             "Assigned_to": "AGENT", "Dependency_IDs": "CADA-0001",
             "Scientific_stage": "01"},
            {"CADA_ID": "CADA-0003", "Title": "Choose method",
             "Next_action": "Researcher selects design based on evidence",
             "Status": "CAPTURED", "Execution_mode": "DECISION_REQUIRED",
             "Assigned_to": "AGENT+RESEARCHER", "Dependency_IDs": "CADA-0002",
             "Scientific_stage": "02-03"},
        ]
        self.gates = [
            {"GATE_ID": f"GATE-{idx:04d}", "Status": "READY" if idx == 1 else "PENDING",
             "Decision": "PENDING", "Scientific_stage": f"{idx:02d}"}
            for idx in range(1, 8)
        ]
        self.write()

    def write(self):
        table(self.mgmt / "11_CADA_Control.csv",
              init_project.TABLES[router.TASKS], self.tasks)
        table(self.mgmt / "18_Human_Validation_Gates.csv",
              init_project.TABLES[router.GATES], self.gates)

    def check(self):
        return router.resolve(self.root)

    def complete_task(self, index, evidence="Synthetic operational receipt"):
        self.tasks[index].update(Status="DONE", Completion_evidence=evidence)
        # Mimic the real workflow's requirement to keep continuity current.
        if index == 1:
            self.continuity.write_text(
                "# Synthetic research continuity\nNext valid action: CADA-0003\n"
                "PRIVATE_RESEARCH_CONTEXT_AND_REVIEW_NOTES", encoding="utf-8")
        self.write()

    def approve_gate_structurally(self, index):
        # A synthetic fixture of an existing recorded decision, NOT an actual
        # human validation step performed by this Skill.
        self.gates[index].update(
            Status="COMPLETED", Decision="APPROVED",
            Validated_by="SYNTHTETIC_RESEARCHER",
            Validation_evidence="synthetic-message-fixture")
        self.write()

    def test_proximo_selects_authorized_technical_prep_without_approving_any_gate(self):
        before = {(p.name, p.read_bytes()) for p in self.mgmt.iterdir() if p.is_file()}
        result = self.check()
        self.assertEqual(result["status"], "TECHNICAL_PREPARATION_AVAILABLE")
        self.assertEqual(result["next_task_id"], "CADA-0002")
        self.assertEqual(result["next_gate_id"], "GATE-0001")
        self.assertTrue(result["technical_preparation_possible"])
        self.assertFalse(result["requires_human_decision"])
        self.assertFalse(result["scientific_gate_approved_by_this_command"])
        self.assertTrue(result["continuity_document_read"])
        self.assertFalse(result["storage_verified_in_this_session"])
        self.assertEqual({(p.name, p.read_bytes()) for p in self.mgmt.iterdir() if p.is_file()}, before)
        self.assertNotIn("PRIVATE_RESEARCH_CONTEXT", json.dumps(result))
        self.assertNotIn("CONTAINS_PRIVATE_LITERATURE", json.dumps(result))

    def test_after_task_is_done_router_stops_at_next_human_science_gate(self):
        self.complete_task(1)
        result = self.check()
        self.assertEqual(result["status"], "HUMAN_GATE_DECISION_REQUIRED")
        self.assertTrue(result["requires_human_decision"])
        self.assertEqual(result["next_gate_id"], "GATE-0001")
        self.assertFalse(result["technical_preparation_possible"])

    def test_recorded_gate_approval_does_not_grant_permission_to_choose_method(self):
        self.complete_task(1)
        self.approve_gate_structurally(0)
        self.tasks[2]["Status"] = "READY"
        self.write()
        result = self.check()
        self.assertEqual(result["status"], "HUMAN_TASK_DECISION_REQUIRED")
        self.assertEqual(result["next_task_id"], "CADA-0003")
        self.assertEqual(result["next_gate_id"], "GATE-0002")
        self.assertFalse(result["technical_preparation_possible"])
        self.assertTrue(result["requires_human_decision"])

    def test_false_completed_gate_without_researcher_reference_is_not_skipped(self):
        self.complete_task(1)
        self.gates[0].update(Status="COMPLETED", Decision="APPROVED")
        self.write()
        self.assertEqual(self.check()["next_gate_id"], "GATE-0001")
        self.assertTrue(self.check()["requires_human_decision"])

    def test_gate_order_uses_ids_not_physical_csv_row_order(self):
        self.complete_task(1)
        self.gates = list(reversed(self.gates))
        self.write()
        self.assertEqual(self.check()["next_gate_id"], "GATE-0001")

    def test_an_unfinished_dependency_does_not_become_an_executable_task(self):
        self.tasks[1]["Dependency_IDs"] = "CADA-0003"
        self.write()
        result = self.check()
        self.assertEqual(result["status"], "HUMAN_GATE_DECISION_REQUIRED")
        self.assertEqual(result["next_task_id"], None)
        self.assertIn("UNFINISHED_TASK_DEPENDENCY", result["blockers"])

    def test_nonexistent_dependency_rejected_without_fabricating_completion(self):
        self.tasks[1]["Dependency_IDs"] = "CADA-9999"
        self.write()
        self.assertIn("UNKNOWN_TASK_DEPENDENCY", self.check()["blockers"])

    def test_completed_dependency_without_evidence_is_not_independently_done(self):
        self.tasks[0]["Completion_evidence"] = ""
        self.write()
        self.assertIn("UNVERIFIED_TASK_DEPENDENCY_COMPLETION", self.check()["blockers"])

    def test_ready_task_in_later_stage_waits_for_prior_gate(self):
        self.complete_task(1)
        self.tasks[2].update(
            Status="READY", Execution_mode="AUTONOMOUS", Assigned_to="AGENT")
        self.write()
        r = self.check()
        self.assertEqual(r["status"], "HUMAN_GATE_DECISION_REQUIRED")
        self.assertIn("PRIOR_HUMAN_GATE_NOT_DOCUMENTED", r["blockers"])

    def test_pending_transaction_blocks_next_without_mutating_any_register(self):
        journal = self.mgmt / ".pending_gate_snapshot"
        journal.mkdir()
        old = (self.mgmt / "11_CADA_Control.csv").read_bytes()
        r = self.check()
        self.assertEqual(r["status"], "BLOCKED")
        self.assertEqual(r["pending_journals"], ["gate_snapshot"])
        self.assertIn("PENDING_RESEARCH_TRANSACTION_RECOVERY", r["blockers"])
        self.assertEqual((self.mgmt / "11_CADA_Control.csv").read_bytes(), old)
        self.assertTrue(journal.exists())

    def test_missing_continuity_does_not_guess_from_cada(self):
        self.continuity.unlink()
        r = self.check()
        self.assertEqual(r["status"], "BLOCKED")
        self.assertIn("CONTINUITY_MISSING_OR_UNSAFE", r["blockers"])
        self.assertIsNone(r["next_task_id"])

    def test_duplicate_tasks_or_incomplete_seven_gates_block_all_autonomy(self):
        self.tasks.append({**self.tasks[1], "Title": "Conflict"})
        self.write()
        self.assertIn("MISSING_OR_DUPLICATE_CADA_ID", self.check()["blockers"])
        self.tasks.pop()
        self.gates.pop()
        self.write()
        self.assertIn("SEVEN_GATES_NOT_PRESENT_OR_UNEXPECTED", self.check()["blockers"])

    def test_drive_mode_does_not_equate_local_copy_with_confirmed_sync(self):
        self.config.write_text(json.dumps({
            "storage_mode": "GOOGLE_DRIVE", "presentation_mode": "MINIMAL"
        }), encoding="utf-8")
        r = self.check()
        self.assertEqual(r["status"], "CANONICAL_STORAGE_RECHECK_REQUIRED")
        self.assertFalse(r["technical_preparation_possible"])
        self.assertFalse(r["storage_verified_in_this_session"])
        self.assertIn("CANONICAL_STORAGE_NOT_VERIFIED", r["blockers"])

    def test_unauthorized_fallback_requires_storage_reconfirmation(self):
        self.config.write_text(json.dumps({
            "storage_mode": "WORK_FALLBACK", "fallback_authorized": False
        }), encoding="utf-8")
        self.assertEqual(self.check()["status"], "CANONICAL_STORAGE_RECHECK_REQUIRED")

    def test_minimal_full_dashboard_same_navigation_and_four_cada_columns(self):
        minpanel = panel.panel(self.root, mode="MINIMAL")
        fullpanel = panel.panel(self.root, mode="FULL")
        self.assertEqual(minpanel["continuation"], fullpanel["continuation"])
        self.assertEqual(minpanel["continuation"]["next_task_id"], "CADA-0002")
        self.assertFalse(minpanel["continuation"]["scientific_gate_approved_by_navigation"])
        self.assertEqual(set(minpanel["tasks"]["items"][0]),
                         {"id", "task", "execution_owner", "deadline"})
        for payload in (minpanel, fullpanel):
            text = json.dumps(payload)
            self.assertNotIn("CONTAINS_PRIVATE_LITERATURE", text)
            self.assertNotIn("PRIVATE_RESEARCH_CONTEXT", text)
            self.assertNotIn("SYNTHTETIC_RESEARCHER", text)

    def test_stale_continuity_blocks_technical_advancement(self):
        self.continuity.write_text(
            "## 14. Next valid action\n- CADA_ID: CADA-0003\n",
            encoding="utf-8")
        r = self.check()
        self.assertEqual(r["status"], "CONTINUITY_RECONCILIATION_REQUIRED")
        self.assertIn("CONTINUITY_NEXT_ACTION_MISMATCH", r["blockers"])
        self.assertFalse(r["technical_preparation_possible"])
        self.assertTrue(r["requires_human_decision"])

    def test_conflicting_continuity_next_sections_require_reconciliation(self):
        self.continuity.write_text(
            "## 14. Next valid action\n- CADA_ID: CADA-0002\n"
            "### Next valid action\n- CADA_ID: CADA-0003\n",
            encoding="utf-8")
        r = self.check()
        self.assertEqual(r["status"], "BLOCKED")
        self.assertIn("CONTINUITY_CONFLICTING_NEXT_ACTIONS", r["blockers"])

    def test_initializer_style_continuity_identifies_same_cada_id_twice(self):
        source = (
            "## 14. Next valid action\n- CADA_ID: CADA-0002\n"
            "## 15. Other section\n- CADA_ID: CADA-9999\n"
            "### Next valid action\n- CADA_ID: CADA-0002\n"
        )
        self.assertEqual(router.recorded_next_ids(source),
                         ["CADA-0002", "CADA-0002"])

    def test_researcher_only_assignment_never_becomes_autonomous(self):
        self.tasks[1]["Assigned_to"] = "RESEARCHER"
        self.tasks[1]["Execution_mode"] = "AUTONOMOUS"
        self.write()
        r = self.check()
        self.assertEqual(r["status"], "HUMAN_TASK_DECISION_REQUIRED")
        self.assertFalse(r["technical_preparation_possible"])

    def test_all_next_intents_are_read_only_and_idempotent(self):
        original = {p.name: p.read_bytes() for p in self.mgmt.iterdir() if p.is_file()}
        for word in ("next", "proximo", "próximo", "resume"):
            with self.subTest(word=word):
                proc = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/next_step_router.py"),
                     str(self.root), "--intent", word],
                    capture_output=True, text=True)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                result = json.loads(proc.stdout)
                self.assertEqual(result["next_task_id"], "CADA-0002")
                self.assertFalse(result["scientific_gate_approved_by_this_command"])
        self.assertEqual({p.name: p.read_bytes() for p in self.mgmt.iterdir() if p.is_file()},
                         original)

    def test_missing_execution_permission_never_grants_autonomy(self):
        self.tasks[1]["Execution_mode"] = ""
        self.write()
        r = self.check()
        self.assertEqual(r["status"], "TASK_EXECUTION_PERMISSION_REVIEW")
        self.assertFalse(r["technical_preparation_possible"])
        self.assertTrue(r["requires_human_decision"])

    def test_marking_cada_done_does_not_make_scientific_quality_validated(self):
        self.complete_task(1)
        self.approve_gate_structurally(0)
        r = self.check()
        self.assertFalse(r["method_or_science_independently_validated"])
        self.assertFalse(r["scientific_gate_approved_by_this_command"])
        self.assertTrue(r["requires_human_decision"])


if __name__ == "__main__":
    unittest.main()
