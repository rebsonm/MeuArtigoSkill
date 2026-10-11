"""Phase 4 UX source contract: all fixtures synthetic; no real Drive or research."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import visual_dashboard as visual


def table(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)


class ApprovedUXDataContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.mgmt = self.root / visual.MGMT
        self.mgmt.mkdir()
        (self.mgmt / "PROJECT_CONFIG.json").write_text(json.dumps({
            "project_name": "SYNTHETIC UX FIXTURE; NOT A RESEARCH RESULT",
            "storage_mode": "GOOGLE_DRIVE_STAGING",
            "storage_state": "DRIVE_STAGING_PENDING_UPLOAD",
            "presentation_mode": "FULL",
        }), encoding="utf-8")

    def create(self, key, rows):
        table(self.mgmt / visual.FILES[key], rows)

    def test_empty_visual_remains_unknown_not_ready(self):
        d = visual.view(self.root)
        self.assertIsNone(d["scientific"]["epistemic_counts"])
        self.assertIsNone(d["scientific"]["editorial"]["checklist_count"])
        self.assertIsNone(d["synchronization"]["snapshots_registered"])
        self.assertIsNone(d["synchronization"]["drive_synchronized_now"])
        self.assertFalse(d["scientific"]["editorial"]["ready_to_submit"])
        self.assertFalse(d["onboarding"]["drive_live_permission_verified"])
        self.assertFalse(d["project"]["storage_verified_in_this_session"])
        self.assertFalse(d["scientific"]["gates"])
        self.assertIsNone(d["operational"]["status_counts"])

    def test_three_epistemic_labels_do_not_fabricate_other_rows(self):
        self.create("evidence", [
            {"Evidence_ID": "E-1", "Epistemic_label": "[L]"},
            {"Evidence_ID": "E-2", "Epistemic_label": "I"},
            {"Evidence_ID": "E-3", "Epistemic_label": "P"},
            {"Evidence_ID": "E-4", "Epistemic_label": ""},
        ])
        d = visual.view(self.root)
        self.assertEqual(d["scientific"]["epistemic_counts"], {"L": 1, "I": 1, "P": 1})
        self.assertEqual(d["scientific"]["epistemic_unclassified"], 1)
        self.assertEqual(d["scientific"]["evidence_rows_registered"], 4)

    def test_planned_search_is_not_executed_or_falsely_verified(self):
        self.create("searches", [
            {"Search_ID": "S-1", "Database_or_source": "Scopus", "Status": "PLANNED"},
            {"Search_ID": "S-2", "Database_or_source": "WoS", "Status": "NOT_EXECUTED"},
        ])
        d = visual.view(self.root, mode="FULL")
        self.assertEqual(d["scientific"]["searches_logged"], 2)
        self.assertEqual(d["scientific"]["searches_marked_complete_in_register"], 0)
        self.assertEqual([r["status"] for r in d["scientific"]["searches"]], ["PLANNED", "NOT_EXECUTED"])
        self.assertNotIn("Literal_query", json.dumps(d["scientific"]["searches"]))
        self.assertEqual(visual.view(self.root, mode="MINIMAL")["scientific"]["searches"], [])

    def test_kanban_cards_group_from_actual_status_without_mutation(self):
        self.create("tasks", [
            {"CADA_ID": "CADA-0001", "Status": "READY", "Title": "Read article",
             "Next_action": "Read article"},
            {"CADA_ID": "CADA-0002", "Status": "BLOCKED", "Title": "Access data",
             "Blocker": "Requires account access"},
            {"CADA_ID": "CADA-0003", "Status": "DONE", "Completion_evidence": "Local evidence"},
        ])
        before = (self.mgmt / visual.FILES["tasks"]).read_bytes()
        d = visual.view(self.root, mode="FULL")
        self.assertEqual(d["operational"]["status_counts"]["READY"], 1)
        self.assertEqual(d["operational"]["status_counts"]["BLOCKED"], 1)
        self.assertEqual(d["operational"]["status_counts"]["DONE"], 1)
        self.assertEqual(d["operational"]["tasks_done_reported"], 1)
        self.assertEqual(d["operational"]["next_action"]["id"], "CADA-0001")
        self.assertEqual((self.mgmt / visual.FILES["tasks"]).read_bytes(), before)

    def test_editorial_never_claims_approval_just_from_checklist(self):
        self.create("submissions", [
            {"Item": "Journal", "Status": "DONE"},
            {"Item": "Disclosure", "Status": "PENDING"},
        ])
        self.create("gates", [
            {"GATE_ID": "GATE-0007", "Name": "Release", "Status": "COMPLETED",
             "Decision": "APPROVED", "Validated_by": "Synthetic author",
             "Validation_evidence": "Simulated approval"},
        ])
        journal = self.root / "06_Submissao/Regras_da_Revista/JOURNAL_PROFILE.json"
        journal.parent.mkdir(parents=True)
        journal.write_text(json.dumps({
            "status": "VERIFIED", "official_rules_verified": True,
            "journal_name": "Synthetic Journal"}), encoding="utf-8")
        anon = self.mgmt / "ANONYMIZATION_PROFILE.json"
        anon.write_text('{"status":"VERIFIED"}', encoding="utf-8")
        e = visual.view(self.root)["scientific"]["editorial"]
        self.assertEqual(e["pending_checklist_items"], 1)
        self.assertTrue(e["gate7_approval_recorded"])
        self.assertFalse(e["ready_to_submit"])
        self.assertTrue(e["journal_official_rules_verified"])
        self.assertEqual(e["journal_name"], "Synthetic Journal")

    def test_gate_without_named_validator_not_approved(self):
        self.create("gates", [
            {"GATE_ID": "GATE-0007", "Name": "Submission", "Status": "COMPLETED",
             "Decision": "APPROVED", "Validated_by": "",
             "Validation_evidence": "Unattributed memo"},
        ])
        self.assertFalse(visual.view(self.root)["scientific"]["editorial"]["gate7_approval_recorded"])

    def test_snapshot_receipt_is_record_only_not_live_drive_sync(self):
        self.create("snapshots", [
            {"SNAP_ID": "SNAP-1", "Timestamp": "2026-10-11T10:00:00",
             "Manifest_SHA256": "a" * 64, "Validation_status": "VALID"},
        ])
        sync = visual.view(self.root)["synchronization"]
        self.assertEqual(sync["snapshots_registered"], 1)
        self.assertEqual(sync["last_recorded_snapshot"]["id"], "SNAP-1")
        self.assertTrue(sync["last_recorded_snapshot"]["has_manifest_sha256"])
        self.assertIsNone(sync["drive_synchronized_now"])

    def test_unverified_trace_stays_unverified_on_timeline(self):
        self.create("trace", [
            {"Trace_ID": "TRACE-0009", "Status": "UNVERIFIED", "Action_summary": "Attempted query"},
        ])
        d = visual.view(self.root, mode="FULL")
        self.assertEqual(d["traceability"]["latest_events"][0]["status"], "UNVERIFIED")

    def test_external_symlink_register_is_not_read(self):
        with tempfile.TemporaryDirectory() as secret:
            outside = Path(secret) / "outside.csv"
            outside.write_text("CADA_ID,Status\nSECRET,READY\n", encoding="utf-8")
            (self.mgmt / visual.FILES["tasks"]).symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "outside the authorized project"):
                visual.view(self.root)

    def test_unnamed_project_does_not_leak_filesystem_folder(self):
        config = self.mgmt / "PROJECT_CONFIG.json"
        config.write_text('{"storage_mode":"GOOGLE_DRIVE_STAGING"}', encoding="utf-8")
        d = visual.view(self.root)
        self.assertEqual(d["project"]["title"], "Projeto sem título")
        self.assertNotIn(self.root.name, json.dumps(d))

    def test_bad_journal_profile_fails_closed(self):
        p = self.root / "06_Submissao/Regras_da_Revista/JOURNAL_PROFILE.json"
        p.parent.mkdir(parents=True)
        p.write_text("{malformed", encoding="utf-8")
        d = visual.view(self.root)
        self.assertFalse(d["scientific"]["editorial"]["journal_official_rules_verified"])
        self.assertFalse(d["scientific"]["editorial"]["ready_to_submit"])

    def test_all_navigation_modules_and_mobile_states_exist_in_ui_source(self):
        ui = (SCRIPTS.parent / "visual-app/src/mcp-app.ts").read_text(encoding="utf-8")
        html = (SCRIPTS.parent / "visual-app/mcp-app.html").read_text(encoding="utf-8")
        for marker in ("Visão geral", "Etapas", "Tarefas C.A.D.A.", "Fontes e buscas",
                       "Evidências [L/I/P]", "Validações", "Rastreabilidade",
                       "Submissão", "Sincronização", "Primeiro uso"):
            self.assertIn(marker, ui)
        for marker in ("Próxima ação recomendada", "Mapa dos gates", "canban-does-not-exist"):
            # Unknown marks must not accidentally be introduced into final UI.
            if marker == "canban-does-not-exist":
                self.assertNotIn(marker, ui)
            else:
                self.assertIn(marker, ui)
        self.assertIn("prefers-color-scheme:dark", html)
        self.assertIn("@media(max-width:640px)", html)
        self.assertNotIn("12/20", ui + html)
        self.assertNotIn("2/7", ui + html)
        self.assertNotIn("innerHTML", ui)

if __name__ == "__main__":
    unittest.main()
