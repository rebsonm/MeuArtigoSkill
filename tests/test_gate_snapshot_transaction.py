"""Fault injection for scientific gate and immutable snapshot consistency."""
from __future__ import annotations

from argparse import Namespace
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import governance_events as gov
import gate_snapshot_transaction as tx

MGMT = "00_Gestao_e_Continuidade"


def write_register(path, headers, items=()):
    with path.open("w", encoding="utf-8-sig", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=headers)
        writer.writeheader()
        writer.writerows(items)


class GateSnapshotTransactionTests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name) / "project"
        self.mgmt = self.root / MGMT
        self.mgmt.mkdir(parents=True)
        (self.mgmt / "PROJECT_CONFIG.json").write_text("{}\n", encoding="utf-8")
        (self.mgmt / "CONTINUIDADE.md").write_text("Synthetic continuity\n", encoding="utf-8")
        write_register(self.mgmt / "13_Traceability_Log.csv", gov.TRACE_HEADERS)
        write_register(self.mgmt / "18_Human_Validation_Gates.csv", gov.GATE_HEADERS,
                       [{"GATE_ID": "GATE-0001", "Status": "READY",
                         "Name": "Define question", "Scientific_stage": "01"}])
        self.before = {name: (self.mgmt / name).read_bytes()
                       for name in tx.REGISTERS if (self.mgmt / name).exists()}

    def approve(self, no_snapshot=False):
        args = Namespace(project=self.root, gate_id="GATE-0001",
                         decision="APPROVED", validated_by="Synthetic Researcher",
                         method="Synthetic direct review",
                         evidence="synthetic-researcher-reference",
                         notes="Synthetic attestation for testing only",
                         researcher_rationale="", researcher_limitation="",
                         no_snapshot=no_snapshot)
        return gov.record_gate(args)

    def assert_original(self):
        for name, raw in self.before.items():
            self.assertEqual((self.mgmt / name).read_bytes(), raw, name)
        self.assertFalse((self.mgmt / "19_Snapshots.csv").exists())

    def test_success_binds_snapshot_to_gate_and_does_not_archive_journal(self):
        self.assertEqual(self.approve(), 0)
        self.assertFalse(tx.has_pending_gate_snapshot(self.root))
        with (self.mgmt / "18_Human_Validation_Gates.csv").open(
                encoding="utf-8-sig", newline="") as f:
            gate = next(csv.DictReader(f))
        with (self.mgmt / "19_Snapshots.csv").open(
                encoding="utf-8-sig", newline="") as f:
            snap = next(csv.DictReader(f))
        self.assertEqual(gate["Status"], "COMPLETED")
        self.assertEqual(gate["Snapshot_after"], snap["SNAP_ID"])
        self.assertEqual(snap["Gate_ID"], gate["GATE_ID"])
        self.assertEqual(snap["Validation_status"], "VALID")
        payload = Path(snap["Snapshot_path_or_URL"]) / "payload" / MGMT
        self.assertFalse((payload / tx.JOURNAL_NAME).exists())
        self.assertTrue((payload / "13_Traceability_Log.csv").exists())

    def test_approval_without_snapshot_preserves_legacy_no_snapshot_flow(self):
        self.assertEqual(self.approve(no_snapshot=True), 0)
        self.assertFalse(tx.has_pending_gate_snapshot(self.root))
        self.assertFalse((self.mgmt / "19_Snapshots.csv").exists())

    def test_failure_before_snapshot_directory_restores_gate_and_trace(self):
        with mock.patch.object(gov.subprocess, "run",
                               side_effect=subprocess.CalledProcessError(2, "snapshot")):
            with self.assertRaises(subprocess.CalledProcessError):
                self.approve()
        self.assert_original()
        self.assertFalse(tx.has_pending_gate_snapshot(self.root))

    def test_abrupt_interruption_requires_recovery_before_next_approval(self):
        with mock.patch.object(gov.subprocess, "run", side_effect=SystemExit("crash")):
            with self.assertRaises(SystemExit):
                self.approve()
        self.assertTrue(tx.has_pending_gate_snapshot(self.root))
        with self.assertRaisesRegex(tx.PendingGateSnapshot, "PENDING_GATE_SNAPSHOT"):
            self.approve()
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/governance_events.py"),
             "recover-gate", str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PREPARED_GATE_SNAPSHOT_ROLLED_BACK", result.stdout)
        self.assert_original()

    def test_orphan_snapshot_is_not_deleted_or_silently_approved(self):
        historical = self.mgmt / "Snapshots" / "SNAP-0001_Interrupted"
        original = b"preserve frozen partial artifacts"
        def interrupted(*args, **kwargs):
            historical.mkdir(parents=True)
            (historical / "source.bin").write_bytes(original)
            raise subprocess.CalledProcessError(2, "snapshot")
        with mock.patch.object(gov.subprocess, "run", side_effect=interrupted):
            with self.assertRaisesRegex(tx.PendingGateSnapshot, "ORPHANED_GATE"):
                self.approve()
        self.assertEqual((historical / "source.bin").read_bytes(), original)
        self.assertTrue(tx.has_pending_gate_snapshot(self.root))
        with self.assertRaisesRegex(tx.PendingGateSnapshot, "ORPHANED_GATE"):
            tx.recover_gate_snapshot(self.root)
        self.assertEqual((historical / "source.bin").read_bytes(), original)

    def test_corrupt_before_image_prevents_unsafe_recovery(self):
        with mock.patch.object(gov.subprocess, "run", side_effect=SystemExit("crash")):
            with self.assertRaises(SystemExit):
                self.approve()
        (tx.journal_dir(self.root) / "before_0").write_bytes(b"tampered")
        with self.assertRaisesRegex(tx.PendingGateSnapshot, "BACKUP_CORRUPTED"):
            tx.recover_gate_snapshot(self.root)
        self.assertTrue(tx.has_pending_gate_snapshot(self.root))


if __name__ == "__main__":
    unittest.main()
