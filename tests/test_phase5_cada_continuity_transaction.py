"""Synthetic Phase 5 integration of traced execution, C.A.D.A., continuity.

Uses the real allowlisted offline local source verifier and disposable
research files. Human gates and actual scientific review remain untouched.
"""
from __future__ import annotations

from argparse import Namespace
import csv
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import init_project
import trace_execution as te
import update_cada_continuity as uc
import cada_continuity_transaction as tx
import next_step_router as router
from transaction_coordinator import require_no_conflict, ConflictingResearchTransaction

MGMT = "00_Gestao_e_Continuidade"


def make_csv(path, headers, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        writer.writeheader()
        writer.writerows([{name: value.get(name, "") for name in headers}
                          for value in rows])


def read_csv(path):
    with path.open("r", newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


class Phase5RecordedCompletionTests(unittest.TestCase):
    def setUp(self):
        ctx = tempfile.TemporaryDirectory()
        self.addCleanup(ctx.cleanup)
        self.root = Path(ctx.name)
        self.mgmt = self.root / MGMT
        self.mgmt.mkdir()
        self.config = self.mgmt / "PROJECT_CONFIG.json"
        self.config.write_text(json.dumps({
            "storage_mode": "WORK_FALLBACK",
            "fallback_authorized": True,
            "work_management_mode": "MATRIX_ONLY",
        }), encoding="utf-8")
        self.taskfile = self.mgmt / "11_CADA_Control.csv"
        self.dashboard = self.mgmt / "15_CADA_Dashboard.csv"
        self.continuity = self.root / router.CONTINUITY
        self.gates = self.mgmt / "18_Human_Validation_Gates.csv"
        self.tracefile = self.mgmt / "13_Traceability_Log.csv"
        self.tasks = [
            {"CADA_ID": "CADA-0001", "Status": "DONE",
             "Execution_mode": "AUTONOMOUS", "Scientific_stage": "00",
             "Completion_evidence": "Workspace scaffold created"},
            {"CADA_ID": "CADA-0002", "Status": "READY", "Scientific_stage": "08",
             "Execution_mode": "AUTONOMOUS_WITH_USER_DECISIONS", "Assigned_to": "AGENT",
             "Next_action": "Check synthetic reference metadata",
             "Dependency_IDs": "CADA-0001",
             "Related_artifact": f"{MGMT}/SOURCE_VERIFICATION.json"},
            {"CADA_ID": "CADA-0003", "Status": "CAPTURED", "Scientific_stage": "09",
             "Execution_mode": "DECISION_REQUIRED", "Assigned_to": "AGENT+RESEARCHER",
             "Next_action": "Review research design", "Dependency_IDs": "CADA-0002",
             "Related_artifact": f"{MGMT}/PROTOCOLO.md"},
        ]
        make_csv(self.taskfile, init_project.TABLES[f"{MGMT}/11_CADA_Control.csv"],
                 self.tasks)
        gate_items = [
            {"GATE_ID": f"GATE-{i:04d}",
             "Status": "PENDING", "Decision": "PENDING",
             "Scientific_stage": str(8 if i == 1 else 8 + i)}
            for i in range(1, 8)
        ]
        make_csv(self.gates, init_project.TABLES[f"{MGMT}/18_Human_Validation_Gates.csv"], gate_items)
        make_csv(self.tracefile, init_project.TABLES[f"{MGMT}/13_Traceability_Log.csv"], [])
        make_csv(self.dashboard, init_project.TABLES[f"{MGMT}/15_CADA_Dashboard.csv"],
                 [{"Metric": "Total_active_items", "Value": "2"},
                  {"Metric": "Next_CADA_ID", "Value": "CADA-0002"},
                  {"Metric": "Next_action", "Value": "Check synthetic reference metadata"},
                  {"Metric": "Next_human_gate", "Value": "GATE-0001"},
                  {"Metric": "Current_scientific_stage", "Value": "08"}])
        self.continuity.write_text(
            "# Synthetic article project\n"
            "## 13. Open issues and blockers\n- SCIENTIFIC_STATUS_NOT_VALIDATED\n"
            "## 14. Next valid action\n"
            "- CADA_ID: CADA-0002\n"
            "- Action: Check synthetic reference metadata\n"
            "- Owner: AGENT\n"
            "- Due: TO_DEFINE\n"
            "## 15. Change log\n- Previously recorded event.\n"
            "## 16. C.A.D.A. dashboard\n"
            "### Next valid action\n"
            "- CADA_ID: CADA-0002\n"
            "- Action: Check synthetic reference metadata\n"
            "- Owner: AGENT\n"
            "- Due: TO_DEFINE\n"
            "## 17. Scientific governance\n"
            "- Next human validation gate: GATE-0001\n"
            "- SCIENTIFIC_GATE_STILL_PENDING\n",
            encoding="utf-8")
        make_csv(self.mgmt / "05_Evidence_Matrix.csv",
                 ["Evidence_ID", "DOI_or_persistent_ID", "Supporting_locator"],
                 [{"Evidence_ID": "EVID-0001", "DOI_or_persistent_ID": "",
                   "Supporting_locator": "Synthetic reference location unavailable"}])

    def receipt(self, *, cada_id="CADA-0002", stage="08", outputs=None):
        r = te.run_script(Namespace(
            project=str(self.root), stage=stage, cada_id=cada_id,
            action="LOCAL_SOURCE_VERIFICATION", summary="Synthetic local source check",
            materiality="ADMINISTRATIVE", script="verify_sources.py",
            outputs=outputs or [f"{MGMT}/SOURCE_VERIFICATION.json"],
            inputs=[f"{MGMT}/05_Evidence_Matrix.csv"],
            script_args=["--offline"]))
        self.assertEqual(r, 0)
        rows = read_csv(self.tracefile)
        return rows[-1]["Trace_ID"]

    def before(self):
        return {rel: (self.root / rel).read_bytes() for rel in tx.FILES}

    def assert_unchanged(self, before):
        self.assertEqual(self.before(), before)

    def test_confirmed_local_execution_updates_three_files_and_preserves_gate(self):
        trace = self.receipt()
        before_gate = self.gates.read_bytes()
        before_trace = self.tracefile.read_bytes()
        result = uc.complete(self.root, "CADA-0002", trace)
        self.assertEqual(result["status"], "OPERATIONAL_COMPLETION_RECORDED")
        self.assertFalse(result["scientific_gate_approved"])
        self.assertFalse(result["drive_sync_verified"])
        self.assertIsNone(result["next_cada_id"])
        self.assertEqual(result["next_gate_id"], "GATE-0001")
        updated = read_csv(self.taskfile)
        self.assertEqual(updated[1]["Status"], "DONE")
        self.assertIn(trace, updated[1]["Completion_evidence"])
        self.assertEqual(updated[2]["Status"], "CAPTURED")
        md = self.continuity.read_text()
        self.assertIn("## 14. Next valid action\n- CADA_ID: NONE", md)
        self.assertIn("### Next valid action\n- CADA_ID: NONE", md)
        self.assertIn("Researcher scientific review pending: GATE-0001", md)
        self.assertIn("SCIENTIFIC_GATE_STILL_PENDING", md)
        self.assertIn("Previously recorded event", md)
        self.assertIn(f"local {trace}; scientific gates unchanged", md)
        metrics = {x["Metric"]: x["Value"] for x in read_csv(self.dashboard)}
        self.assertEqual(metrics["Next_CADA_ID"], "")
        self.assertEqual(metrics["Next_human_gate"], "GATE-0001")
        self.assertEqual(metrics["Total_active_items"], "1")
        self.assertEqual(metrics["Last_completed_CADA_ID"], "CADA-0002")
        self.assertEqual(metrics["Last_trace_event"], trace)
        self.assertEqual(metrics["Current_scientific_stage"], "08")
        self.assertEqual(self.gates.read_bytes(), before_gate)
        self.assertEqual(self.tracefile.read_bytes(), before_trace)
        self.assertFalse(tx.journal_dir(self.root).exists())
        self.assertEqual(router.resolve(self.root)["status"], "HUMAN_GATE_DECISION_REQUIRED")

    def test_duplicate_completion_is_blocked_and_idempotent(self):
        trace = self.receipt()
        uc.complete(self.root, "CADA-0002", trace)
        after = self.before()
        with self.assertRaisesRegex(ValueError, "NOT_AUTHORIZED"):
            uc.complete(self.root, "CADA-0002", trace)
        self.assert_unchanged(after)

    def test_unverified_trace_cannot_complete_task(self):
        tid = te.declare(Namespace(project=str(self.root),stage="08",
            cada_id="CADA-0002", action="SOURCE_REVIEW", summary="Declaration only",
            materiality="ADMINISTRATIVE"))
        self.assertEqual(tid, 0)
        before = self.before()
        with self.assertRaisesRegex(ValueError, "TRACE_NOT_CONFIRMED"):
            uc.complete(self.root, "CADA-0002", "TRACE-0001")
        self.assert_unchanged(before)

    def test_trace_from_another_task_is_not_reused(self):
        trace = self.receipt(cada_id="CADA-9999")
        before = self.before()
        with self.assertRaisesRegex(ValueError, "TRACE_NOT_CONFIRMED"):
            uc.complete(self.root, "CADA-0002", trace)
        self.assert_unchanged(before)

    def test_trace_from_wrong_scientific_stage_is_not_reused(self):
        trace = self.receipt(stage="07")
        before = self.before()
        with self.assertRaisesRegex(ValueError, "TRACE_NOT_CONFIRMED"):
            uc.complete(self.root, "CADA-0002", trace)
        self.assert_unchanged(before)

    def test_receipt_tamper_blocks_completion_without_mutation(self):
        trace = self.receipt()
        receipt = self.root / f"{MGMT}/TRACE_RECEIPTS/{trace}.json"
        receipt.write_bytes(receipt.read_bytes() + b"tamper")
        before = self.before()
        with self.assertRaisesRegex(ValueError, "TRACE_RECEIPT_MISSING_OR_CHANGED"):
            uc.complete(self.root, "CADA-0002", trace)
        self.assert_unchanged(before)

    def test_changed_local_output_invalidates_operational_proof(self):
        trace = self.receipt()
        output = self.mgmt / "SOURCE_VERIFICATION.json"
        output.write_bytes(output.read_bytes() + b"\n")
        before = self.before()
        with self.assertRaisesRegex(ValueError, "TRACE_OUTPUT_CHANGED"):
            uc.complete(self.root, "CADA-0002", trace)
        self.assert_unchanged(before)

    def test_task_artifact_must_match_actual_receipt_output(self):
        trace = self.receipt()
        data = read_csv(self.taskfile)
        data[1]["Related_artifact"] = f"{MGMT}/unrelated_project.md"
        make_csv(self.taskfile, init_project.TABLES[f"{MGMT}/11_CADA_Control.csv"], data)
        before = self.before()
        with self.assertRaisesRegex(ValueError, "TRACE_OUTPUT_DOES_NOT_MATCH_CADA_ARTIFACT"):
            uc.complete(self.root, "CADA-0002", trace)
        self.assert_unchanged(before)

    def test_unauthorized_drive_copy_cannot_be_updated(self):
        trace = self.receipt()
        self.config.write_text(json.dumps({"storage_mode": "GOOGLE_DRIVE"}), encoding="utf-8")
        before = self.before()
        with self.assertRaisesRegex(ValueError, "LOCAL_WORK_FALLBACK_AUTHORIZATION_REQUIRED"):
            uc.complete(self.root, "CADA-0002", trace)
        self.assert_unchanged(before)

    def test_stale_markdown_blocks_updates_until_reconciled(self):
        trace = self.receipt()
        self.continuity.write_text(
            self.continuity.read_text().replace("CADA-0002", "CADA-0003"),
            encoding="utf-8")
        before = self.before()
        with self.assertRaisesRegex(ValueError, "NOT_AUTHORIZED"):
            uc.complete(self.root, "CADA-0002", trace)
        self.assert_unchanged(before)

    def test_pending_scientific_transaction_blocks_operational_completion(self):
        trace = self.receipt()
        marker = self.mgmt / ".pending_method_route_change"
        marker.mkdir()
        before = self.before()
        with self.assertRaisesRegex(ValueError, "NOT_AUTHORIZED"):
            uc.complete(self.root, "CADA-0002", trace)
        self.assert_unchanged(before)

    def test_transaction_mid_commit_failure_restores_all_three_files(self):
        trace = self.receipt()
        before = self.before()
        real_replace = os.replace
        calls = [0]
        def fail_second(src, dst):
            calls[0] += 1
            if calls[0] == 2:
                raise OSError("simulated second-file storage failure")
            return real_replace(src, dst)
        with patch.object(tx.os, "replace", side_effect=fail_second):
            with self.assertRaises(OSError):
                uc.complete(self.root, "CADA-0002", trace)
        self.assertGreaterEqual(calls[0], 5)
        self.assert_unchanged(before)
        self.assertFalse(tx.journal_dir(self.root).exists())

    def test_explicit_recovery_of_interrupted_prepared_journal(self):
        before = self.before()
        journal = tx.journal_dir(self.root)
        journal.mkdir()
        manifest = {"schema_version": 1, "state": "PREPARED", "entries": []}
        for i, rel in enumerate(tx.FILES):
            content = before[rel]
            modified = content + b"simulated uncommitted data"
            (journal / f"before_{i}.bin").write_bytes(content)
            (journal / f"after_{i}.bin").write_bytes(modified)
            manifest["entries"].append({
                "path": rel,
                "before_sha256": tx.digest(content),
                "after_sha256": tx.digest(modified),
            })
        (journal / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (self.root / tx.FILES[0]).write_bytes(before[tx.FILES[0]] + b"simulated uncommitted data")
        with self.assertRaises(ConflictingResearchTransaction):
            require_no_conflict(self.root)
        self.assertIn("PENDING_RESEARCH_TRANSACTION_RECOVERY",
                      router.resolve(self.root)["blockers"])
        self.assertEqual(tx.recover(self.root)["status"],
                         "PREPARED_CADA_CONTINUITY_ROLLED_BACK")
        self.assert_unchanged(before)
        self.assertFalse(journal.exists())

    def test_recovery_rejects_independent_edit_without_destroying_journal(self):
        before = self.before()
        journal = tx.journal_dir(self.root)
        journal.mkdir()
        manifest = {"schema_version": 1, "state": "PREPARED", "entries": []}
        for i, rel in enumerate(tx.FILES):
            (journal / f"before_{i}.bin").write_bytes(before[rel])
            (journal / f"after_{i}.bin").write_bytes(before[rel] + b"new")
            manifest["entries"].append({
                "path": rel, "before_sha256": tx.digest(before[rel]),
                "after_sha256": tx.digest(before[rel] + b"new"),
            })
        (journal / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.taskfile.write_bytes(before[tx.FILES[0]] + b"independent edit")
        with self.assertRaisesRegex(tx.PendingCADAContinuity, "INDEPENDENT_EDIT"):
            tx.recover(self.root)
        self.assertTrue(journal.exists())
        self.assertIn(b"independent edit", self.taskfile.read_bytes())

    def test_no_next_action_when_all_gates_pending_does_not_invent_approval(self):
        trace = self.receipt()
        uc.complete(self.root, "CADA-0002", trace)
        self.assertEqual([row["Status"] for row in read_csv(self.gates)],
                         ["PENDING"] * 7)
        self.assertFalse(router.resolve(self.root)["technical_preparation_possible"])


if __name__ == "__main__":
    unittest.main()
