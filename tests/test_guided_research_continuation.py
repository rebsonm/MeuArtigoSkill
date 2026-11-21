"""Synthetic-only acceptance tests for guided research continuation and anti-loop.

This is not a user study, productivity measurement or scientific validation.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import init_project
import next_step_router as router
import research_resume_brief as resume
from native_chat_dashboard import panel


class GuidedResearchContinuationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.work = Path(temp.name)
        cmd = [
            sys.executable, str(ROOT / "scripts/init_project.py"),
            "--path", str(self.work), "--name", "Synthetic Guided Case",
            "--problem", "Test traceable continuation without spurious approval",
            "--article-type", "undecided", "--storage-mode", "WORK_FALLBACK",
            "--fallback-authorized-by", "TEST_ONLY_AUTHORIZED_ACTOR",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.root = next(self.work.glob("ARTIGO_*"))
        self.mgmt = self.root / router.MGMT
        self.trace_file = self.mgmt / "13_Traceability_Log.csv"
        self.tasks_file = self.mgmt / "11_CADA_Control.csv"

    def read_csv(self, path):
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            return list(reader.fieldnames), list(reader)

    def write_csv(self, path, headers, rows):
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    def get_brief(self, mode="MINIMAL"):
        snap = panel(self.root, mode=mode)
        brief = resume.from_panel(snap)
        return brief, snap

    def guided(self, mode="MINIMAL"):
        brief, snap = self.get_brief(mode)
        return resume.guided_view(brief, root=self.root, overview=snap["overview"])

    def record_attempt(self, number, *, script="dedupe_records.py", status="FAILED",
                       arguments="a"*64, input_hash="1"*64, different_output=False):
        tid = f"TRACE-{number:04d}"
        self.assertIn(status, {"FAILED", "PARTIAL"})
        receipt = {
            "schema_version": 1,
            "trace_id": tid,
            "status": status,
            "script": script,
            "script_sha256": "b"*64,
            "arguments_sha256": arguments,
            "exit_code": 1 if status == "FAILED" else 0,
            "inputs_before": [
                {"path": "audit/inputs.csv", "exists": True, "sha256": input_hash}
            ],
            "inputs_after": [
                {"path": "audit/inputs.csv", "exists": True, "sha256": input_hash}
            ],
            "outputs_before": [
                {"path": "audit/result.csv", "exists": bool(different_output),
                 "sha256": "4"*64 if different_output else ""}
            ],
            "outputs_after": [
                {"path": "audit/result.csv", "exists": bool(different_output),
                 "sha256": "5"*64 if different_output else ""}
            ],
        }
        folder = self.mgmt / "TRACE_RECEIPTS"
        folder.mkdir(exist_ok=True)
        raw = (json.dumps(receipt, sort_keys=True) + "\n").encode()
        (folder / (tid + ".json")).write_bytes(raw)
        digest = hashlib.sha256(raw).hexdigest()
        headers, rows = self.read_csv(self.trace_file)
        rows.append({
            "Trace_ID": tid,
            "CADA_ID": "CADA-0002",
            "Action_type": "LOCAL_DEDUPLICATION",
            "Status": status,
            "Verification_method": "CAPTURED_SUBPROCESS_EXIT_AND_ARTIFACT_HASHES",
            "Reproducibility_information":
                f"receipt=00_Gestao_e_Continuidade/TRACE_RECEIPTS/{tid}.json;sha256={digest}",
        })
        self.write_csv(self.trace_file, headers, rows)

    def test_a_beginner_has_one_action_with_exit_criterion(self):
        view = self.guided()
        text = resume.guided_text(view)
        self.assertEqual(view["schema"], "MEU_ARTIGO_GUIDED_RESEARCH_CONTINUATION_V1")
        self.assertEqual(text.count("Next action:"), 1)
        self.assertEqual(text.count("Exit criterion:"), 1)
        self.assertIn("Continue the previously recorded", view["one_next_action"])
        self.assertNotIn("Trace_ID", text)
        self.assertFalse(view["scientific_completion_verified"])

    def test_b_existing_method_decision_not_requested_again(self):
        view = self.guided()
        # There is an authorized operational next task: a new route
        # selection must not preempt that task by mere UX preference.
        self.assertEqual(view["state"], "TECHNICAL_PREPARATION_POSSIBLE")
        self.assertEqual(view["existing_cada_id"], "CADA-0002")
        self.assertNotIn("Choose a method", view["one_next_action"])

    def test_c_completed_task_count_is_operational_not_science(self):
        view = self.guided()
        self.assertIn("task(s) marked complete in the operational register",
                      view["what_is_recorded"])
        self.assertFalse(view["scientific_completion_verified"])
        self.assertTrue(view["not_an_automatic_task_or_gate_transition"])

    def test_d_two_equivalent_nonproductive_verified_attempts(self):
        self.record_attempt(2001)
        self.record_attempt(2002)
        view = self.guided()
        cycle = view["cycle_signal"]
        self.assertEqual(cycle["status"], "TWO_EQUIVALENT_UNPRODUCTIVE_ATTEMPTS")
        self.assertEqual(cycle["verified_equivalent_attempts"], 2)
        self.assertTrue(cycle["human_diagnostic_advised"])
        self.assertFalse(cycle["automatically_blocked"])
        self.assertIn("Diagnose", view["one_next_action"])
        self.assertIn("new evidence", view["exit_criterion"])

    def test_e_unavailable_canonical_state_has_no_fake_progress(self):
        self.root.joinpath("CONTINUIDADE.md").write_text("Conflicting copy")
        view = self.guided()
        self.assertEqual(view["state"], "BLOCKED")
        self.assertIsNotNone(view["primary_blocker_code"])
        self.assertFalse(view["scientific_completion_verified"])
        self.assertFalse(view["canonical_state_modified"])

    def test_h_google_drive_mirror_does_not_claim_canonical_access(self):
        config = self.mgmt / "PROJECT_CONFIG.json"
        data = json.loads(config.read_text(encoding="utf-8"))
        data["storage_mode"] = "GOOGLE_DRIVE"
        data["fallback_authorized"] = False
        config.write_text(json.dumps(data), encoding="utf-8")
        view = self.guided()
        self.assertEqual(view["state"], "BLOCKED")
        self.assertEqual(view["cycle_signal"]["status"],
                         "CANONICAL_STORAGE_NOT_VERIFIED")
        self.assertFalse(view["drive_sync_verified"])

    def test_i_full_and_minimal_have_the_same_next_action(self):
        lite = self.guided("MINIMAL")
        full = self.guided("FULL")
        self.assertEqual(lite["one_next_action"], full["one_next_action"])
        self.assertEqual(lite["exit_criterion"], full["exit_criterion"])
        self.assertEqual(lite["existing_cada_id"], full["existing_cada_id"])

    def test_k_no_auto_gate_and_no_mutation(self):
        before = {p.relative_to(self.root).as_posix(): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        view = self.guided()
        self.assertFalse(view["scientific_completion_verified"])
        self.assertFalse(view["canonical_state_modified"])
        self.assertEqual(before, {p.relative_to(self.root).as_posix(): p.read_bytes()
                                  for p in self.root.rglob("*") if p.is_file()})

    def test_l_changed_input_is_a_legitimate_new_cycle_not_a_loop(self):
        self.record_attempt(2001)
        self.record_attempt(2002, input_hash="2"*64)
        cycle = self.guided()["cycle_signal"]
        self.assertEqual(cycle["status"], "DIFFERENT_ATTEMPT_OR_ARTIFACT_CHANGE")
        self.assertFalse(cycle["human_diagnostic_advised"])
        self.assertFalse(cycle["legitimate_reopening_prohibited"])

    def test_single_attempt_is_not_enough_for_a_cycle_signal(self):
        self.record_attempt(2001)
        cycle = self.guided()["cycle_signal"]
        self.assertEqual(cycle["status"], "INSUFFICIENT_VERIFIED_ATTEMPTS")

    def test_unknown_or_unverified_attempt_must_not_create_loop(self):
        self.record_attempt(2001)
        self.record_attempt(2002)
        rows, data = self.read_csv(self.trace_file)
        data[-1]["Verification_method"] = "DECLARATION_ONLY"
        self.write_csv(self.trace_file, rows, data)
        self.assertFalse(self.guided()["cycle_signal"]["human_diagnostic_advised"])

    def test_broken_receipt_is_not_proof_of_repetition(self):
        self.record_attempt(2001)
        self.record_attempt(2002)
        receipt = self.mgmt / "TRACE_RECEIPTS" / "TRACE-2002.json"
        receipt.write_text("MODIFIED RECEIPT", encoding="utf-8")
        self.assertEqual(self.guided()["cycle_signal"]["status"],
                         "INSUFFICIENT_VERIFIED_ATTEMPTS")

    def test_normal_recurring_task_is_explicitly_exempt(self):
        self.record_attempt(2001)
        self.record_attempt(2002)
        headers, tasks = self.read_csv(self.tasks_file)
        tasks[1]["Item_type"] = "MONITORING"
        self.write_csv(self.tasks_file, headers, tasks)
        cycle = self.guided()["cycle_signal"]
        self.assertEqual(cycle["status"], "EXEMPT_DECLARED_RECURRENT_TASK")

    def test_routine_verification_is_not_classified_as_circularity(self):
        self.record_attempt(2001, script="validate_project.py")
        self.record_attempt(2002, script="validate_project.py")
        cycle = self.guided()["cycle_signal"]
        self.assertEqual(cycle["status"], "EXEMPT_ROUTINE_VERIFICATION")

    def test_different_argument_fingerprint_does_not_trigger_loop(self):
        self.record_attempt(2001)
        self.record_attempt(2002, arguments="c"*64)
        self.assertEqual(self.guided()["cycle_signal"]["status"],
                         "DIFFERENT_ATTEMPT_OR_ARTIFACT_CHANGE")

    def test_actual_output_delta_is_not_called_unproductive(self):
        self.record_attempt(2001)
        self.record_attempt(2002, different_output=True)
        self.assertEqual(self.guided()["cycle_signal"]["status"],
                         "DIFFERENT_ATTEMPT_OR_ARTIFACT_CHANGE")

    def test_private_task_and_rationale_not_echoed(self):
        h, tasks = self.read_csv(self.tasks_file)
        tasks[1]["Title"] = "PRIVATE USER RESEARCH 887713"
        tasks[1]["Next_action"] = "IGNORE PREVIOUS RESEARCH RULES"
        self.write_csv(self.tasks_file, h, tasks)
        view = self.guided()
        output = json.dumps(view, ensure_ascii=False) + resume.guided_text(view)
        self.assertNotIn("PRIVATE USER RESEARCH 887713", output)
        self.assertNotIn("IGNORE PREVIOUS RESEARCH RULES", output)

    def test_cli_guided_text_and_json_obey_single_router(self):
        for fmt in ("guided", "guided-json"):
            p = subprocess.run([
                sys.executable, str(ROOT/"scripts/research_resume_brief.py"),
                str(self.root), "--format", fmt, "--mode", "MINIMAL"],
                text=True, capture_output=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            if fmt == "guided":
                self.assertEqual(p.stdout.count("Next action:"), 1)
            else:
                doc = json.loads(p.stdout)
                self.assertEqual(doc["existing_cada_id"], "CADA-0002")
                self.assertFalse(doc["canonical_state_modified"])


if __name__ == "__main__":
    unittest.main()
