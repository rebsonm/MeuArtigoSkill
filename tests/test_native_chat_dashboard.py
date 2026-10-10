"""Synthetic engineering checks for the Skill-native visual projection.

These fixtures are not a scientific corpus, user study or UX evaluation.
"""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import native_chat_dashboard as native


class NativeChatDashboardTests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        self.mgmt = self.root / native.MGMT
        self.mgmt.mkdir()
        (self.mgmt / "PROJECT_CONFIG.json").write_text(json.dumps({
            "presentation_mode": "MINIMAL", "storage_mode": "GOOGLE_DRIVE"
        }), encoding="utf-8")
        self.write("11_CADA_Control.csv", [
            {"CADA_ID": "CADA-0001", "Status": "DONE",
             "Completion_evidence": "SECRET_RESPONSE_TEXT", "Deadline": "2026-10-10",
             "Next_action": "Sensitive internal action"},
            {"CADA_ID": "CADA-0002", "Status": "READY",
             "Completion_evidence": "", "Next_action": "Private action details"},
            {"CADA_ID": "CADA-0003", "Status": "BLOCKED", "Completion_evidence": ""},
            {"CADA_ID": "CADA-0004", "Status": "IN_PROGRESS", "Completion_evidence": ""},
        ])
        self.write("18_Human_Validation_Gates.csv", [
            {"GATE_ID": "GATE-0001", "Status": "COMPLETED", "Decision": "APPROVED",
             "Validated_by": "RESEARCHER", "Validation_evidence": "PRIVATE_ORIGINAL_MESSAGE"},
            {"GATE_ID": "GATE-0002", "Status": "READY", "Decision": "PENDING",
             "Validated_by": "", "Validation_evidence": ""},
            {"GATE_ID": "GATE-0003", "Status": "COMPLETED", "Decision": "APPROVED",
             "Validated_by": "", "Validation_evidence": ""},
            {"GATE_ID": "GATE-0004", "Status": "BLOCKED", "Decision": "PENDING",
             "Validated_by": "", "Validation_evidence": ""},
        ])
        self.write("05_Evidence_Matrix.csv", [{"Evidence_ID": "EVID-001", "FullText_path": "SECRET_SOURCE_PATH"}])
        self.write("09_Claims_Ledger.csv", [{"Claim_ID": "CLAIM-001", "Claim_text": "COPYRIGHTED_AND_PRIVATE_PASSAGE"}])
        self.write("13_Traceability_Log.csv", [{"Trace_ID": "TRACE-001", "Notes": "CONFIDENTIAL"}])

    def write(self, file: str, rows: list[dict]):
        headers = list(dict.fromkeys(k for row in rows for k in row))
        with (self.mgmt / file).open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, headers)
            w.writeheader()
            w.writerows(rows)

    def test_minimal_has_five_views_and_no_scientific_percentage(self):
        p = native.panel(self.root)
        self.assertEqual(p["mode"], "MINIMAL")
        self.assertEqual(set(["overview", "tasks", "gates", "evidence", "history_sync"]) - set(p), set())
        self.assertIsNone(p["overview"]["scientific_progress_percentage"])
        self.assertFalse(p["scientific_quality_independently_validated"])
        self.assertFalse(p["drive_sync_verified_in_this_session"])

    def test_true_human_approval_fields_not_partial(self):
        p = native.panel(self.root)
        self.assertEqual(p["overview"]["documented_gate_approvals"], 1)
        self.assertFalse(p["gates"]["items"][2]["approval_documented"])

    def test_cada_done_does_not_certify_science(self):
        p = native.panel(self.root)
        self.assertEqual(p["overview"]["tasks_reported_done"], 1)
        self.assertEqual(p["overview"]["active_tasks"], 3)
        self.assertEqual(p["overview"]["next_gate_id"], "GATE-0002")

    def test_minimal_truncation_is_presentation_only(self):
        a = native.panel(self.root)
        b = native.panel(self.root, mode="FULL")
        self.assertEqual(len(a["tasks"]["items"]), 3)
        self.assertEqual(len(b["tasks"]["items"]), 4)
        self.assertEqual(a["tasks"]["registered_total"], b["tasks"]["registered_total"])
        self.assertEqual(a["overview"], b["overview"])
        self.assertTrue(a["tasks"]["items_partial"])

    def test_cada_only_requested_four_columns_and_correct_mappings(self):
        self.write("11_CADA_Control.csv", [
            {"CADA_ID": "CADA-0001", "Task": "Review manuscript",
             "Owner": "Researcher", "Deadline": "2026-10-19",
             "Status": "READY", "Next_action": "Do not display this next step",
             "Completion_evidence": "Private proof"},
            {"CADA_ID": "CADA-0002", "Task": "Check sources",
             "Owner": "Team", "Deadline": "", "Status": "BLOCKED"},
        ])
        data = native.panel(self.root)
        row = data["tasks"]["items"][0]
        self.assertEqual(set(row), {"id", "task", "execution_owner", "deadline"})
        self.assertEqual(row, {"id": "CADA-0001", "task": "Review manuscript",
                               "execution_owner": "Researcher", "deadline": "2026-10-19"})
        self.assertEqual(data["tasks"]["items"][1]["deadline"], None)
        self.assertNotIn("Do not display this next step", json.dumps(data))
        self.assertNotIn("Private proof", json.dumps(data))

    def test_text_fallback_has_four_columns_and_missing_fields(self):
        self.write("11_CADA_Control.csv", [
            {"CADA_ID": "CADA-0009", "Task": "Compile | evidence",
             "Owner": "", "Deadline": "", "Status": "READY"}
        ])
        data = native.panel(self.root, mode="FULL")
        lines = native.task_table(data).splitlines()
        self.assertEqual(lines[0], "ID Tarefa | Tarefa | Responsável execução | Prazo")
        self.assertEqual(lines[1], "--- | --- | --- | ---")
        self.assertIn(r"Compile \| evidence", lines[2])
        self.assertIn("Not recorded", lines[2])
        self.assertEqual(len(lines), 3)
        self.assertIn("ID Tarefa | Tarefa | Responsável execução | Prazo",
                      native.fallback(data))

    def test_missing_canonical_task_does_not_substitute_next_action(self):
        data = native.panel(self.root, mode="FULL")
        self.assertEqual(data["tasks"]["items"][0]["id"], "CADA-0001")
        self.assertIsNone(data["tasks"]["items"][0]["task"])
        self.assertIsNone(data["tasks"]["items"][0]["execution_owner"])

    def test_canonical_csv_fields_match_project_initializer(self):
        # This checks the production CSV schema instead of a fabricated
        # Excel-only Task/Owner fixture (regression found during review).
        import init_project
        required = ("CADA_ID", "Title", "Assigned_to", "Deadline")
        fields = init_project.TABLES["00_Gestao_e_Continuidade/11_CADA_Control.csv"]
        self.assertTrue(all(field in fields for field in required))
        self.write("11_CADA_Control.csv", [
            {"CADA_ID": "CADA-0200", "Title": "Review the manuscript",
             "Assigned_to": "Researcher", "Deadline": "2026-10-20",
             "Status": "READY", "Next_action": "Different next action",
             "Task": "Obsolete Excel title", "Owner": "Wrong Excel owner"}
        ])
        row = native.panel(self.root)["tasks"]["items"][0]
        self.assertEqual(set(row), {"id", "task", "execution_owner", "deadline"})
        self.assertEqual(row, {
            "id": "CADA-0200", "task": "Review the manuscript",
            "execution_owner": "Researcher", "deadline": "2026-10-20",
        })
        self.assertNotIn("Different next action", json.dumps(native.panel(self.root)))
        self.assertNotIn("Obsolete Excel title", json.dumps(native.panel(self.root)))

    def test_minimal_prioritizes_active_work_and_marks_hidden_rows(self):
        self.write("11_CADA_Control.csv", [
            {"CADA_ID": "CADA-0001", "Title": "Old work",
             "Assigned_to": "Researcher", "Status": "DONE"},
            {"CADA_ID": "CADA-0002", "Title": "Second completed task",
             "Assigned_to": "Researcher", "Status": "DONE"},
            {"CADA_ID": "CADA-0003", "Title": "Pending work",
             "Assigned_to": "Agent", "Status": "READY"},
        ])
        minimal = native.panel(self.root, mode="MINIMAL")["tasks"]
        full = native.panel(self.root, mode="FULL")["tasks"]
        self.assertEqual([item["id"] for item in minimal["items"]], ["CADA-0003"])
        self.assertTrue(minimal["items_partial"])
        self.assertEqual([item["id"] for item in full["items"]],
                         ["CADA-0001", "CADA-0002", "CADA-0003"])
        self.assertFalse(full["items_partial"])

    def test_no_mutation_even_when_mode_override(self):
        before = {file: file.read_bytes() for file in self.mgmt.iterdir() if file.is_file()}
        native.panel(self.root, mode="FULL")
        native.panel(self.root, mode="MINIMAL")
        self.assertEqual(before, {file: file.read_bytes() for file in self.mgmt.iterdir() if file.is_file()})

    def test_no_paths_review_texts_or_copyrighted_material_in_payload(self):
        serialized = json.dumps(native.panel(self.root), ensure_ascii=False)
        for protected in ["SECRET_SOURCE_PATH", "COPYRIGHTED_AND_PRIVATE_PASSAGE",
                          "PRIVATE_ORIGINAL_MESSAGE", "SECRET_RESPONSE_TEXT",
                          "Sensitive internal action", "CONFIDENTIAL"]:
            self.assertNotIn(protected, serialized)

    def test_missing_input_not_faked_zero(self):
        p = native.panel(self.root)
        self.assertIsNone(p["history_sync"]["registered_sync_records"])
        self.assertIn("12_PM_Sync.csv", p["missing_registers"])
        self.assertEqual(p["evidence"]["source_report_presence"], "MISSING")
        self.assertIsNone(p["evidence"]["verified_sources"])

    def test_report_presence_does_not_imply_integrity(self):
        path = self.mgmt / "SOURCE_VERIFICATION.json"
        path.write_text(json.dumps({"schema_version": 1, "checks": [
            {"result": "METADATA_AND_LOCATOR_CHECKED"}]}), encoding="utf-8")
        data = native.panel(self.root)["evidence"]
        self.assertEqual(data["source_report_presence"], "PRESENT_NOT_AUDITED")
        self.assertIsNone(data["blocking_conflicts"])
        self.assertIsNone(data["verified_sources"])

    def test_no_config_does_not_substitute_a_demo(self):
        (self.mgmt / "PROJECT_CONFIG.json").unlink()
        with self.assertRaises(ValueError):
            native.panel(self.root)

    def test_bad_presentation_mode_rejected_without_changes(self):
        with self.assertRaises(ValueError):
            native.panel(self.root, mode="PUBLISHED")

    def test_text_fallback_does_not_claim_external_confirmation(self):
        x = native.fallback(native.panel(self.root))
        self.assertIn("Google Drive sync verified: NO", x)
        self.assertIn("not scientific validation", x)
        self.assertNotIn("COPYRIGHTED_AND_PRIVATE_PASSAGE", x)


if __name__ == "__main__":
    unittest.main()
