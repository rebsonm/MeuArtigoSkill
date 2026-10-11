"""Guard frozen scientific snapshot evidence against ID collisions."""
from __future__ import annotations

import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "create_snapshot.py"
MGMT = "00_Gestao_e_Continuidade"


class SnapshotCollisionProtectionTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "project"
        self.mgmt = self.root / MGMT
        self.mgmt.mkdir(parents=True)
        (self.mgmt / "CONTINUIDADE.md").write_text(
            "Original research continuity\n", encoding="utf-8")
        self.snapshots = self.mgmt / "Snapshots"
        self.snapshots.mkdir()

    def create(self, milestone: str):
        return subprocess.run(
            [sys.executable, str(RUNNER), str(self.root), "--milestone", milestone],
            capture_output=True, text=True)

    def test_existing_snapshot_with_same_id_and_different_milestone_is_immutable(self):
        historical = self.snapshots / "SNAP-0001_Original"
        historical.mkdir()
        sentinel = historical / "important-evidence.txt"
        original = b"preserved frozen human scientific decision"
        sentinel.write_bytes(original)
        run = self.create("Different title")
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn("SNAPSHOT_ID_COLLISION", run.stderr)
        self.assertEqual(sentinel.read_bytes(), original)
        self.assertFalse((self.snapshots / "SNAP-0001_Different-title").exists())
        with (self.mgmt / "19_Snapshots.csv").open(
                newline="", encoding="utf-8-sig") as handle:
            self.assertEqual(len(list(csv.DictReader(handle))), 0)

    def test_same_path_collision_does_not_erase_previous_incomplete_snapshot(self):
        stale = self.snapshots / "SNAP-0001_Repeated"
        stale.mkdir()
        marker = stale / "incomplete-original.bin"
        marker.write_bytes(b"do not destroy")
        run = self.create("Repeated")
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertEqual(marker.read_bytes(), b"do not destroy")

    def test_normal_new_snapshot_still_freezes_original_files(self):
        result = self.create("First milestone")
        self.assertEqual(result.returncode, 0, result.stderr)
        snap = self.snapshots / "SNAP-0001_First-milestone"
        self.assertTrue((snap / "manifest-sha256.txt").is_file())
        self.assertEqual(
            (snap / "payload" / MGMT / "CONTINUIDADE.md").read_text(encoding="utf-8"),
            "Original research continuity\n")
        with (self.mgmt / "19_Snapshots.csv").open(
                newline="", encoding="utf-8-sig") as handle:
            records = list(csv.DictReader(handle))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["SNAP_ID"], "SNAP-0001")


if __name__ == "__main__":
    unittest.main()
