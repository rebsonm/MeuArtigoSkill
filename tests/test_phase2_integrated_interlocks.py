"""Integrated Phase-2 synthetic audit: stop incompatible pending journals.

Exercise the real command entry points (not only the shared guard). All
attestations and bibliographic content are synthetic, never human approvals.
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

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import choose_method_route
import gate_snapshot_transaction as gate_tx
import governance_events
import method_route_transaction as method_tx
import method_routes
import register_transaction as import_tx
from transaction_coordinator import (ConflictingResearchTransaction,
                                     active_journals, require_no_conflict)

MGMT = "00_Gestao_e_Continuidade"


def csv_register(path, headers, data=()):
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


class Phase2InterlockTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "workspace"
        self.mgmt = self.root / MGMT
        self.mgmt.mkdir(parents=True)
        (self.mgmt / "PROJECT_CONFIG.json").write_text(json.dumps({
            "method_route_governance_required": True,
            "method_route": "UNDECIDED",
            "article_type": "integrative review",
        }), encoding="utf-8")
        (self.mgmt / "METHOD_PROFILE.json").write_text(
            json.dumps(method_routes.new_profile("UNDECIDED")), encoding="utf-8")
        csv_register(self.mgmt / "18_Human_Validation_Gates.csv",
                     governance_events.GATE_HEADERS,
                     [{"GATE_ID": "GATE-0001", "Status": "READY",
                       "Name": "Define question", "Scientific_stage": "01"}])
        csv_register(self.mgmt / "17_Decision_Log.csv",
                     governance_events.DEC_HEADERS)
        csv_register(self.mgmt / "13_Traceability_Log.csv",
                     governance_events.TRACE_HEADERS)
        csv_register(self.mgmt / "02_Search_Log.csv", ["id", "name"],
                     [{"id": "BASE", "name": "Search"}])
        csv_register(self.mgmt / "03_Screening.csv", ["id", "name"],
                     [{"id": "BASE", "name": "Screening"}])

    def marker(self, name):
        from transaction_coordinator import JOURNALS
        folder = self.mgmt / JOURNALS[name]
        folder.mkdir()
        return folder

    def approve_gate(self):
        return governance_events.record_gate(Namespace(
            project=self.root, gate_id="GATE-0001", decision="APPROVED",
            validated_by="Synthetic reviewer", method="Synthetic review",
            evidence="synthetic-review-reference", notes="Testing only",
            researcher_rationale="", researcher_limitation="",
            no_snapshot=True))

    def choose(self):
        return choose_method_route.choose(
            self.root, "INTEGRATIVE_REVIEW", "Synthetic reviewer",
            "synthetic human message ID", "I chose this approach to integrate heterogeneous research while acknowledging the limits of database coverage.")

    def import_registers(self):
        updates = {rel: (["id", "name"], [{"id": "NEXT", "name": "Synthetic"}])
                   for rel in import_tx.FILES}
        # Trace's header is an actual governance schema; keep it correct.
        updates[import_tx.FILES[2]] = (governance_events.TRACE_HEADERS, [])
        return import_tx.apply_register_transaction(self.root, updates, str)

    def snapshot(self):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "create_snapshot.py"),
             str(self.root), "--milestone", "Synthetic transition"],
            capture_output=True, text=True)

    def test_pending_bibliographic_import_blocks_scientific_changes(self):
        self.marker("bibliographic")
        originals = [(self.mgmt / filename).read_bytes() for filename in
                     ("PROJECT_CONFIG.json", "18_Human_Validation_Gates.csv",
                      "13_Traceability_Log.csv")]
        with self.assertRaisesRegex(ConflictingResearchTransaction, "bibliographic"):
            self.choose()
        with self.assertRaisesRegex(ConflictingResearchTransaction, "bibliographic"):
            self.approve_gate()
        with self.assertRaisesRegex(ConflictingResearchTransaction, "bibliographic"):
            governance_events.record_decision(Namespace(project=self.root))
        snap = self.snapshot()
        self.assertNotEqual(snap.returncode, 0)
        self.assertIn("OTHER_PENDING_RESEARCH_TRANSACTION", snap.stderr)
        self.assertFalse((self.mgmt / "19_Snapshots.csv").exists())
        after = [(self.mgmt / filename).read_bytes() for filename in
                 ("PROJECT_CONFIG.json", "18_Human_Validation_Gates.csv",
                  "13_Traceability_Log.csv")]
        self.assertEqual(originals, after)

    def test_pending_method_route_blocks_import_gate_and_freeze(self):
        self.marker("method_route")
        original = (self.mgmt / "13_Traceability_Log.csv").read_bytes()
        for action in (self.import_registers, self.approve_gate):
            with self.subTest(action=action.__name__):
                with self.assertRaisesRegex(ConflictingResearchTransaction,
                                            "method_route"):
                    action()
        snap = self.snapshot()
        self.assertNotEqual(snap.returncode, 0)
        self.assertIn("OTHER_PENDING_RESEARCH_TRANSACTION", snap.stderr)
        self.assertEqual((self.mgmt / "13_Traceability_Log.csv").read_bytes(), original)
        self.assertFalse((self.mgmt / "19_Snapshots.csv").exists())

    def test_pending_gate_snapshot_blocks_import_method_decision_and_manual_snapshot(self):
        self.marker("gate_snapshot")
        original = (self.mgmt / "18_Human_Validation_Gates.csv").read_bytes()
        for action in (self.import_registers, self.choose,
                       lambda: governance_events.record_decision(Namespace(project=self.root))):
            with self.subTest(action=str(action)):
                with self.assertRaisesRegex(ConflictingResearchTransaction,
                                            "gate_snapshot"):
                    action()
        snap = self.snapshot()
        self.assertNotEqual(snap.returncode, 0)
        self.assertIn("OTHER_PENDING_RESEARCH_TRANSACTION", snap.stderr)
        self.assertEqual((self.mgmt / "18_Human_Validation_Gates.csv").read_bytes(), original)

    def test_two_overlapping_journals_block_each_recovery_without_erasing_evidence(self):
        method = self.marker("method_route")
        gate = self.marker("gate_snapshot")
        with self.assertRaisesRegex(ConflictingResearchTransaction, "gate_snapshot"):
            method_tx.recover_method_route(self.root)
        with self.assertRaisesRegex(ConflictingResearchTransaction, "method_route"):
            gate_tx.recover_gate_snapshot(self.root)
        self.assertTrue(method.is_dir())
        self.assertTrue(gate.is_dir())
        gate.rmdir()
        bibliographic = self.marker("bibliographic")
        with self.assertRaisesRegex(ConflictingResearchTransaction, "bibliographic"):
            method_tx.recover_method_route(self.root)
        with self.assertRaisesRegex(ConflictingResearchTransaction, "method_route"):
            import_tx.recover_pending_transaction(self.root)
        self.assertTrue(bibliographic.is_dir())
        self.assertTrue(method.is_dir())

    def test_symlink_journal_is_also_interlocked(self):
        outside = self.root / "outside"
        outside.mkdir()
        alias = self.mgmt / ".pending_bibliographic_import"
        alias.symlink_to(outside, target_is_directory=True)
        self.assertEqual(active_journals(self.root), {"bibliographic"})
        with self.assertRaises(ConflictingResearchTransaction):
            self.choose()
        self.assertTrue(alias.is_symlink())
        self.assertTrue(outside.is_dir())

    def test_clean_workspace_is_not_blocked_by_interlock(self):
        self.assertEqual(active_journals(self.root), set())
        require_no_conflict(self.root)
        self.assertFalse(import_tx.has_pending_transaction(self.root))
        self.assertEqual(self.choose(), "DEC-0001")
        self.assertFalse(method_tx.has_pending_method_route(self.root))
        self.assertEqual(self.snapshot().returncode, 0)

    def test_gate_journal_still_allows_its_own_internal_snapshot(self):
        # The gate handler owns the journal; this test ensures the previous
        # six-stage gate-to-snapshot flow is not blocked by the new interlock.
        self.assertEqual(self.approve_gate(), 0)
        self.assertFalse(gate_tx.has_pending_gate_snapshot(self.root))


if __name__ == "__main__":
    unittest.main()
