"""PR #52: canonical-continuity regressions using the actual project initializer.

All workspaces, approvals, exports and records are synthetic, disposable local
fixtures. A validated TRACE event only proves local execution; it does not
certify search completeness, human approval, or Google Drive synchronization.
"""
from __future__ import annotations

from argparse import Namespace
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import init_project
import next_step_router as routing
import native_chat_dashboard as dashboard
import cada_continuity_integrity as integrity
import cada_continuity_transaction as transaction
import trace_execution as trace
import update_cada_continuity as update


def table(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class RealInitializedContinuityTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.workspace = Path(temp.name)
        self.root = self.initialize(self.workspace, mode="WORK_FALLBACK")
        self.canonical = self.root / routing.CONTINUITY
        self.mgmt = self.root / routing.MGMT

    @staticmethod
    def initialize(parent: Path, *, mode: str):
        parent.mkdir(exist_ok=True)
        command = [
            sys.executable, str(ROOT / "scripts/init_project.py"),
            "--path", str(parent),
            "--name", "Synthetic Canonical Integration",
            "--problem", "Synthetic records for software regression only",
            "--article-type", "undecided", "--storage-mode", mode,
        ]
        if mode == "WORK_FALLBACK":
            command.extend(["--fallback-authorized-by",
                            "SYNTHETIC_TEST_USER_AUTHORIZATION_FIXTURE"])
        ran = subprocess.run(command, capture_output=True, text=True)
        if ran.returncode:
            raise AssertionError("Real initializer failed:\n" + ran.stderr[-1600:])
        found = list(parent.glob("ARTIGO_*"))
        if len(found) != 1:
            raise AssertionError("Expected exactly one initialized project")
        return found[0]

    def test_initializer_and_router_share_the_real_canonical_path(self):
        self.assertEqual(
            routing.CONTINUITY,
            "00_Gestao_e_Continuidade/CONTINUIDADE.md")
        self.assertEqual(transaction.FILES[1], routing.CONTINUITY)
        self.assertEqual(integrity.CONTINUITY, routing.CONTINUITY)
        self.assertTrue(self.canonical.is_file())
        self.assertFalse((self.root / "CONTINUIDADE.md").exists())
        self.assertEqual(len(table(self.mgmt / "18_Human_Validation_Gates.csv")), 7)
        result = routing.resolve(self.root)
        self.assertEqual(result["status"], "TECHNICAL_PREPARATION_AVAILABLE")
        self.assertEqual(result["next_task_id"], "CADA-0002")
        self.assertEqual(result["next_gate_id"], "GATE-0001")
        self.assertTrue(result["continuity_document_read"])
        self.assertFalse(result["scientific_gate_approved_by_this_command"])

    def test_real_initialization_does_not_pretend_unperformed_work_is_done(self):
        rows = table(self.mgmt / "11_CADA_Control.csv")
        self.assertEqual([x["Status"] for x in rows],
                         ["DONE", "READY", "CAPTURED"])
        self.assertEqual(rows[1]["Completion_evidence"], "")
        self.assertEqual(rows[2]["Completion_evidence"], "")
        gates = table(self.mgmt / "18_Human_Validation_Gates.csv")
        self.assertTrue(all(row["Decision"] == "PENDING" for row in gates))
        self.assertEqual(integrity.audit(self.root)["status"],
                         "NOT_APPLICABLE_LEGACY")
        self.assertFalse(integrity.audit(self.root)["last_operational_proof_checked"])

    def test_actual_dashboard_minimal_and_full_use_same_root_state(self):
        lite = dashboard.panel(self.root, mode="MINIMAL")
        full = dashboard.panel(self.root, mode="FULL")
        self.assertEqual(lite["continuation"], full["continuation"])
        self.assertEqual(lite["continuation"]["next_task_id"], "CADA-0002")
        self.assertEqual(lite["continuation"]["next_gate_id"], "GATE-0001")
        self.assertEqual(set(lite["tasks"]["items"][0]),
                         {"id", "task", "execution_owner", "deadline"})
        self.assertFalse(lite["continuation"]["scientific_gate_approved_by_navigation"])
        self.assertFalse(lite["continuation"]["drive_sync_verified_in_this_session"])

    def test_root_shadow_document_never_silently_supersedes_real_continuity(self):
        before = self.canonical.read_bytes()
        shadow = self.root / "CONTINUIDADE.md"
        shadow.write_text("## Next valid action\n- CADA_ID: CADA-9999\n")
        result = routing.resolve(self.root)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("ROOT_CONTINUITY_COPY_REQUIRES_RECONCILIATION",
                      result["blockers"])
        check = integrity.audit(self.root)
        self.assertEqual(check["status"], "BLOCKED")
        self.assertIn("ROOT_CONTINUITY_COPY_REQUIRES_RECONCILIATION",
                      check["errors"])
        self.assertEqual(self.canonical.read_bytes(), before)
        self.assertTrue(shadow.exists())  # No auto-deletion/migration.

    def test_missing_management_continuity_is_not_rescued_by_root_shadow(self):
        self.canonical.unlink()
        (self.root / "CONTINUIDADE.md").write_text(
            "## Next valid action\n- CADA_ID: CADA-0002\n")
        result = routing.resolve(self.root)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertFalse(result["technical_preparation_possible"])
        self.assertFalse(self.canonical.exists())

    def test_drive_staging_copy_never_becomes_approved_local_storage(self):
        other = self.initialize(self.workspace / "drive", mode="GOOGLE_DRIVE_STAGING")
        route = routing.resolve(other)
        self.assertEqual(route["status"], "CANONICAL_STORAGE_RECHECK_REQUIRED")
        self.assertFalse(route["technical_preparation_possible"])
        self.assertFalse(route["storage_verified_in_this_session"])
        self.assertTrue((other / routing.CONTINUITY).is_file())
        self.assertFalse((other / "CONTINUIDADE.md").exists())

    def prepare_trace_for_narrow_technical_task(self):
        """Adapt the seeded task to *actual local dedup*, not a novelty verdict."""
        cada_file = self.mgmt / "11_CADA_Control.csv"
        with cada_file.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = list(reader.fieldnames or [])
            tasks = list(reader)
        tasks[1]["Title"] = "Deduplicate a synthetic metadata export"
        tasks[1]["Description"] = "Operational CSV dedup only, not a novelty audit"
        tasks[1]["Next_action"] = "Run the offline deduplication utility"
        tasks[1]["Related_artifact"] = (
            "01_Auditoria_de_Novidade/consolidated_exact_dedup.csv")
        with cada_file.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, headers)
            writer.writeheader()
            writer.writerows(tasks)

        source = self.root / "02_Buscas_e_Exports/Scopus/synthetic_input.csv"
        source.write_text(
            "Title,DOI,Authors,Year\n"
            "Synthetic governance article,10.1234/synthetic-test,A Researcher,2024\n",
            encoding="utf-8")
        result = trace.run_script(Namespace(
            project=str(self.root),
            stage="01", cada_id="CADA-0002",
            action="LOCAL_DEDUPLICATION",
            summary="Synthetic local CSV consolidation, no external source",
            materiality="ADMINISTRATIVE",
            script="dedupe_records.py",
            outputs=[
                "01_Auditoria_de_Novidade/consolidated_exact_dedup.csv"],
            inputs=[
                "02_Buscas_e_Exports/Scopus/synthetic_input.csv"],
            script_args=[
                str(source), "--out-dir",
                str(self.root / "01_Auditoria_de_Novidade")]))
        self.assertEqual(result, 0)
        traces = table(self.mgmt / "13_Traceability_Log.csv")
        self.assertEqual(traces[-1]["Status"], "CONFIRMED")
        return traces[-1]["Trace_ID"]

    def test_real_init_then_next_execution_receipt_commit_audit_and_resume(self):
        trace_id = self.prepare_trace_for_narrow_technical_task()
        self.assertEqual(routing.resolve(self.root)["next_task_id"], "CADA-0002")
        gate_file = self.mgmt / "18_Human_Validation_Gates.csv"
        old_gates = gate_file.read_bytes()
        old_trace = (self.mgmt / "13_Traceability_Log.csv").read_bytes()
        event = update.complete(self.root, "CADA-0002", trace_id)
        self.assertEqual(event["status"], "OPERATIONAL_COMPLETION_RECORDED")
        self.assertFalse(event["scientific_gate_approved"])
        self.assertFalse(event["drive_sync_verified"])
        self.assertEqual(event["next_gate_id"], "GATE-0001")
        self.assertEqual(event["next_cada_id"], None)
        self.assertIn("CADA_ID: NONE", self.canonical.read_text(encoding="utf-8"))
        self.assertFalse((self.root / "CONTINUIDADE.md").exists())
        self.assertEqual(table(self.mgmt / "11_CADA_Control.csv")[1]["Status"], "DONE")
        self.assertEqual(gate_file.read_bytes(), old_gates)
        self.assertEqual((self.mgmt / "13_Traceability_Log.csv").read_bytes(), old_trace)
        self.assertEqual(routing.resolve(self.root)["status"],
                         "HUMAN_GATE_DECISION_REQUIRED")
        self.assertEqual(integrity.audit(self.root)["status"], "CHECKED")
        self.assertTrue(integrity.audit(self.root)["last_operational_proof_checked"])
        projected = dashboard.panel(self.root, mode="MINIMAL")
        self.assertEqual(projected["continuation"]["integrity_status"], "CHECKED")
        self.assertFalse(projected["continuation"]["technical_preparation_possible"])
        self.assertFalse(transaction.journal_dir(self.root).exists())

    def test_real_initialized_unverified_trace_cannot_mark_task_done(self):
        original = {
            relative: (self.root / relative).read_bytes()
            for relative in transaction.FILES
        }
        with self.assertRaisesRegex(ValueError, "TRACE_NOT_CONFIRMED"):
            update.complete(self.root, "CADA-0002", "TRACE-0001")
        self.assertEqual(
            {relative: (self.root / relative).read_bytes()
             for relative in transaction.FILES},
            original)


if __name__ == "__main__":
    unittest.main()
