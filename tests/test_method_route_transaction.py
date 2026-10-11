"""Synthetic fault injection for local method-route consistency and recovery."""
from __future__ import annotations

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
import choose_method_route as route
import governance_events as governance
import method_route_transaction as tx
import method_routes

MGMT = "00_Gestao_e_Continuidade"
ROUTE = "INTEGRATIVE_REVIEW"
REVIEWER = "Synthetic Test Researcher"
EVIDENCE = "synthetic-human-message-reference-only"
RATIONALE = ("I chose this approach to integrate heterogeneous scientific "
             "evidence while acknowledging incomplete coverage limitations.")


def write_csv(path: Path, headers: list[str], records: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)


class MethodRouteTransactionTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name) / "project"
        self.mgmt = self.root / MGMT
        self.mgmt.mkdir(parents=True)
        (self.mgmt / "PROJECT_CONFIG.json").write_text(json.dumps({
            "method_route_governance_required": True,
            "method_route": "UNDECIDED",
            "article_type": "review",
        }), encoding="utf-8")
        (self.mgmt / "METHOD_PROFILE.json").write_text(
            json.dumps(method_routes.new_profile("UNDECIDED")), encoding="utf-8")
        gates = [{"GATE_ID": f"GATE-{i:04d}", "Status": "PENDING"}
                 for i in range(1, 8)]
        write_csv(self.mgmt / "18_Human_Validation_Gates.csv",
                  governance.GATE_HEADERS, gates)
        write_csv(self.mgmt / "17_Decision_Log.csv", governance.DEC_HEADERS, [])
        write_csv(self.mgmt / "13_Traceability_Log.csv", governance.TRACE_HEADERS, [])
        self.before = {name: (self.mgmt / name).read_bytes() for name in tx.FILES}

    def choose(self):
        return route.choose(self.root, ROUTE, REVIEWER, EVIDENCE, RATIONALE)

    def assert_original(self):
        for name, before in self.before.items():
            self.assertEqual((self.mgmt / name).read_bytes(), before, name)

    def inject_failure(self, error):
        original = Path.write_text

        def fail_profile(path, *args, **kwargs):
            if path.name == "METHOD_PROFILE.json":
                raise error
            return original(path, *args, **kwargs)

        return mock.patch.object(Path, "write_text", fail_profile)

    def test_success_writes_five_correlated_artifacts_and_cleans_journal(self):
        did = self.choose()
        self.assertEqual(did, "DEC-0001")
        self.assertFalse(tx.has_pending_method_route(self.root))
        cfg = json.loads((self.mgmt / "PROJECT_CONFIG.json").read_text())
        profile = json.loads((self.mgmt / "METHOD_PROFILE.json").read_text())
        self.assertEqual(cfg["method_route"], ROUTE)
        self.assertEqual(profile["route"], ROUTE)
        self.assertEqual(profile["route_decision_id"], did)
        with (self.mgmt / "17_Decision_Log.csv").open(
                newline="", encoding="utf-8-sig") as f:
            decisions = list(csv.DictReader(f))
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["DEC_ID"], did)
        with (self.mgmt / "13_Traceability_Log.csv").open(
                newline="", encoding="utf-8-sig") as f:
            traces = list(csv.DictReader(f))
        self.assertEqual(len(traces), 1)
        self.assertEqual(decisions[0]["Trace_ID"], traces[0]["Trace_ID"])

    def test_handled_error_after_decision_logging_rolls_back_every_file(self):
        with self.inject_failure(OSError("injected file write error")):
            with self.assertRaisesRegex(OSError, "injected"):
                self.choose()
        self.assert_original()
        self.assertFalse(tx.has_pending_method_route(self.root))

    def test_abrupt_stop_blocks_new_decisions_until_explicit_recovery(self):
        with self.inject_failure(SystemExit("simulated abrupt termination")):
            with self.assertRaises(SystemExit):
                self.choose()
        self.assertTrue(tx.has_pending_method_route(self.root))
        with self.assertRaisesRegex(tx.PendingMethodRouteTransaction, "PENDING_RECOVERY"):
            self.choose()
        cli = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "choose_method_route.py"),
             str(self.root), "--recover-pending"],
            capture_output=True, text=True)
        self.assertEqual(cli.returncode, 0, cli.stderr)
        self.assertIn("PREPARED_METHOD_ROUTE_ROLLED_BACK", cli.stdout)
        self.assert_original()
        self.assertFalse(tx.has_pending_method_route(self.root))
        self.assertEqual(self.choose(), "DEC-0001")

    def test_tampered_backup_blocks_recovery_and_keeps_journal(self):
        with self.inject_failure(SystemExit("abrupt")):
            with self.assertRaises(SystemExit):
                self.choose()
        (tx.journal_dir(self.root) / "before_0").write_bytes(b"untrusted payload")
        with self.assertRaisesRegex(tx.PendingMethodRouteTransaction, "BACKUP_OR_TARGET_CHANGED"):
            tx.recover_method_route(self.root)
        self.assertTrue(tx.has_pending_method_route(self.root))

    def test_committed_journal_only_clears_after_hash_verification(self):
        old_rmtree = tx.shutil.rmtree
        folder = tx.journal_dir(self.root)

        def refuse_cleanup(path, *args, **kwargs):
            if Path(path) == folder:
                raise OSError("injected final cleanup error")
            return old_rmtree(path, *args, **kwargs)

        with mock.patch.object(tx.shutil, "rmtree", refuse_cleanup):
            with self.assertRaisesRegex(OSError, "cleanup"):
                self.choose()
        self.assertTrue(tx.has_pending_method_route(self.root))
        self.assertEqual(
            tx.recover_method_route(self.root)["status"],
            "COMMITTED_METHOD_ROUTE_CONFIRMED_AND_JOURNAL_CLEANED")
        self.assertFalse(tx.has_pending_method_route(self.root))
        self.assertEqual(json.loads((self.mgmt / "PROJECT_CONFIG.json").read_text())["method_route"], ROUTE)


if __name__ == "__main__":
    unittest.main()
