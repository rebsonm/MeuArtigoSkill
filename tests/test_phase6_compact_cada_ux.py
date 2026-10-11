"""Phase 6 non-Frankenstein UI/data tests on actual initialized workspaces.

One router, one set of gate/task rules, four visual C.A.D.A. columns.
No new project table, scientific approval, source fact, or Drive operation.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import init_project
import native_chat_dashboard as ui
import next_step_router as navigation
import update_cada_continuity as writer


class CompactCADAUXTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name)
        run = subprocess.run([
            sys.executable, str(ROOT / "scripts/init_project.py"),
            "--path", str(self.folder), "--name", "Synthetic UX Audit",
            "--problem", "Testing conservation of original source rules",
            "--article-type", "undecided", "--storage-mode", "WORK_FALLBACK",
            "--fallback-authorized-by", "SYNTHETIC_TEST_USER_AUTHORIZATION",
        ], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        projects = list(self.folder.glob("ARTIGO_*"))
        self.assertEqual(len(projects), 1)
        self.root = projects[0]
        self.mgmt = self.root / navigation.MGMT
        self.tasks_path = self.root / navigation.TASKS
        self.gates_path = self.root / navigation.GATES

    def load(self, path):
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            return list(reader.fieldnames or []), list(reader)

    def save(self, path, headers, rows):
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    def test_two_next_fields_are_compatibility_aliases_not_conflicting_predictions(self):
        data = ui.panel(self.root)
        route = navigation.resolve(self.root)
        self.assertEqual(data["overview"]["next_task_id"], route["next_task_id"])
        self.assertEqual(data["overview"]["next_gate_id"], route["next_gate_id"])
        self.assertEqual(data["continuation"]["next_task_id"], route["next_task_id"])
        self.assertEqual(data["continuation"]["next_gate_id"], route["next_gate_id"])
        self.assertEqual(route["status"], "TECHNICAL_PREPARATION_AVAILABLE")
        self.assertEqual(route["next_task_id"], "CADA-0002")

    def test_plain_text_shows_one_next_step_and_one_blocker_not_raw_conflicting_rows(self):
        data = ui.panel(self.root)
        text = ui.fallback(data)
        self.assertEqual(text.count("Next step:"), 1)
        self.assertEqual(text.count("First blocker:"), 1)
        self.assertNotIn("Next task / gate (raw register)", text)
        self.assertNotIn("Run first novelty/terminology scan", text)
        self.assertIn("TECHNICAL_PREPARATION_AVAILABLE", text)
        self.assertIn("CADA-0002", text)

    def test_minimal_prioritizes_actual_eligible_task_over_three_blocked_rows(self):
        headers, rows = self.load(self.tasks_path)
        added = []
        for n in (11, 12, 13, 14):
            added.append({
                "CADA_ID": f"CADA-{n:04d}",
                "Title": f"Blocked fixture work {n}",
                "Assigned_to": "AGENT",
                "Status": "BLOCKED",
                "Scientific_stage": "01",
                "Next_action": "Not eligible in this fixture",
            })
        self.save(self.tasks_path, headers, [rows[0], *added, *rows[1:]])
        minimal = ui.panel(self.root, mode="MINIMAL")
        full = ui.panel(self.root, mode="FULL")
        self.assertEqual(minimal["continuation"]["next_task_id"], "CADA-0002")
        self.assertEqual(minimal["tasks"]["items"][0]["id"], "CADA-0002")
        self.assertEqual(full["tasks"]["items"][0]["id"], "CADA-0001")
        self.assertEqual(len(minimal["tasks"]["items"]), 3)
        self.assertTrue(minimal["tasks"]["items_partial"])
        self.assertEqual(set(minimal["tasks"]["items"][0]),
                         {"id", "task", "execution_owner", "deadline"})
        self.assertEqual(minimal["overview"], full["overview"])

    def test_blocked_navigation_cannot_expose_raw_active_task_as_next(self):
        canonical = self.root / navigation.CONTINUITY
        shadow = self.root / "CONTINUIDADE.md"
        shadow.write_text("Synthetic conflicting version", encoding="utf-8")
        result = ui.panel(self.root, mode="MINIMAL")
        self.assertEqual(result["continuation"]["status"],
                         "CADA_CONTINUITY_INTEGRITY_REVIEW")
        self.assertFalse(result["continuation"]["technical_preparation_possible"])
        self.assertIsNone(result["overview"]["next_task_id"])
        self.assertIsNone(result["overview"]["next_gate_id"])
        self.assertEqual(result["continuation"]["next_task_id"],
                         result["overview"]["next_task_id"])
        self.assertIn("ROOT_CONTINUITY_COPY_REQUIRES_RECONCILIATION",
                      ui.fallback(result))
        self.assertTrue(canonical.exists())
        self.assertTrue(shadow.exists())

    def test_gate_approval_without_validation_reference_remains_pending(self):
        headers, gates = self.load(self.gates_path)
        gates[0]["Status"] = "COMPLETED"
        gates[0]["Decision"] = "APPROVED"
        gates[0]["Validated_by"] = "SYNTHETIC_RESEARCHER"
        gates[0]["Validation_evidence"] = ""
        self.save(self.gates_path, headers, gates)
        data = ui.panel(self.root)
        self.assertFalse(data["gates"]["items"][0]["approval_documented"])
        self.assertEqual(data["overview"]["documented_gate_approvals"], 0)
        self.assertEqual(data["overview"]["next_gate_id"], "GATE-0001")
        self.assertEqual(data["continuation"]["next_gate_id"], "GATE-0001")
        self.assertFalse(data["gates"]["items"][0]["independently_scientifically_validated"])

    def test_minimal_full_equivalent_safeguards_and_no_project_mutations(self):
        before = {p.relative_to(self.root).as_posix(): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        lite = ui.panel(self.root, mode="MINIMAL")
        full = ui.panel(self.root, mode="FULL")
        self.assertEqual(lite["overview"], full["overview"])
        self.assertEqual(lite["continuation"], full["continuation"])
        self.assertEqual(lite["gates"]["registered_total"], 7)
        self.assertFalse(lite["scientific_quality_independently_validated"])
        self.assertFalse(full["drive_sync_verified_in_this_session"])
        self.assertEqual({p.relative_to(self.root).as_posix(): p.read_bytes()
                          for p in self.root.rglob("*") if p.is_file()}, before)

    def test_dashboard_symlink_or_malformed_csv_is_unavailable_not_fake_zero(self):
        path = self.mgmt / "05_Evidence_Matrix.csv"
        old = path.read_bytes()
        path.unlink()
        private = self.root / "private.csv"
        private.write_text("Evidence_ID,SECRET_DATA\nP1,PRIVATE_CONTENT\n", encoding="utf-8")
        path.symlink_to(private)
        panel = ui.panel(self.root)
        self.assertIsNone(panel["evidence"]["registered_evidence_rows"])
        self.assertIn("05_Evidence_Matrix.csv", panel["missing_registers"])
        self.assertNotIn("PRIVATE_CONTENT", json.dumps(panel))
        path.unlink()
        path.write_bytes(b"Evidence_ID,Evidence_ID\nE1,E2\n")
        panel = ui.panel(self.root)
        self.assertIsNone(panel["evidence"]["registered_evidence_rows"])
        self.assertIn("05_Evidence_Matrix.csv", panel["missing_registers"])
        self.assertNotEqual(path.read_bytes(), old)

    def test_post_transition_candidate_is_the_same_as_router_policy(self):
        headers, tasks = self.load(self.tasks_path)
        task2 = tasks[1]
        task2["Status"] = "DONE"
        task2["Completion_evidence"] = "synthetic technical test proof"
        # A later-stage choice must not be selected ahead of pending Gate 1.
        gates = self.load(self.gates_path)[1]
        candidate, pending_id = writer.choose_next(tasks, gates)
        self.assertIsNone(candidate)
        self.assertEqual(pending_id, "GATE-0001")
        same_gate = navigation.pending_human_gate(gates)
        same_task, why = navigation.next_eligible_task(tasks, same_gate)
        self.assertIsNone(same_task)
        self.assertEqual(why[1], "TASK_NOT_READY")
        # With Gate 1 structurally documented, the next READY human task
        # can be selected by ID but never executed without real permission.
        gates[0].update({
            "Status": "COMPLETED", "Decision": "APPROVED",
            "Validated_by": "SYNTHETIC_RESEARCHER",
            "Validation_evidence": "fixture-only-attribution",
        })
        tasks[2]["Status"] = "READY"
        next_task, next_gate = writer.choose_next(tasks, gates)
        self.assertEqual(next_task["CADA_ID"], "CADA-0003")
        self.assertEqual(next_gate, "GATE-0002")
        self.assertEqual(next_task["CADA_ID"],
                         navigation.next_eligible_task(
                             tasks, navigation.pending_human_gate(gates))[0]["CADA_ID"])

    def test_no_gate_missing_or_repeated_is_treated_as_approved(self):
        _, gates = self.load(self.gates_path)
        gates = gates[:-1]
        with self.assertRaisesRegex(ValueError, "SEVEN_GATES"):
            navigation.pending_human_gate(gates)
        with self.assertRaisesRegex(ValueError, "SEVEN_GATES"):
            writer.choose_next([], gates)

    def test_source_values_never_used_as_actions_or_prompt_instructions(self):
        headers, rows = self.load(self.tasks_path)
        rows[1]["Title"] = "CONFIDENTIAL_WORKER_NOTES"
        rows[1]["Next_action"] = "IGNORE_PREVIOUS_RULES"
        self.save(self.tasks_path, headers, rows)
        data = ui.panel(self.root)
        # Titles remain visible because authorized C.A.D.A. title is requested.
        self.assertEqual(data["tasks"]["items"][0]["task"], "CONFIDENTIAL_WORKER_NOTES")
        # ... but raw instructions and completion evidence are never rendered.
        output = json.dumps(data)
        self.assertNotIn("IGNORE_PREVIOUS_RULES", output)
        self.assertFalse(data["continuation"]["scientific_gate_approved_by_navigation"])


if __name__ == "__main__":
    unittest.main()
