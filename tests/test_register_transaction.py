"""Recovery / fault injection tests, entirely temporary and synthetic."""
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import register_transaction as tx


class RegisterTransactionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.original = {}
        for idx, rel in enumerate(tx.FILES):
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("id,name\nBASE,Original\n", encoding="utf-8")
            self.original[rel] = path.read_bytes()
        self.updates = {rel: (["id", "name"], [
            {"id": "NEXT", "name": '=HYPERLINK("https://unsafe.example")'}
        ]) for rel in tx.FILES}
        self.escape = lambda v: "'" + str(v) if str(v).startswith("=") else str(v)

    def test_success_updates_all_three_and_cleans_journal(self):
        tx.apply_register_transaction(self.root, self.updates, self.escape)
        for rel in tx.FILES:
            data = (self.root / rel).read_text(encoding="utf-8-sig")
            self.assertIn("NEXT", data)
            self.assertIn("'=HYPERLINK", data)
        self.assertFalse(tx.has_pending_transaction(self.root))
        self.assertEqual(tx.recover_pending_transaction(self.root)["status"],
                         "NO_PENDING_TRANSACTION")

    def test_exception_after_first_replace_rolls_back_every_file(self):
        real_replace = tx.os.replace
        def fail_second(src, dst):
            if Path(src).name == "after_1.csv":
                raise OSError("simulated disk failure")
            return real_replace(src, dst)
        with patch.object(tx.os, "replace", side_effect=fail_second):
            with self.assertRaises(OSError):
                tx.apply_register_transaction(self.root, self.updates, self.escape)
        for rel in tx.FILES:
            self.assertEqual((self.root / rel).read_bytes(), self.original[rel])
        self.assertFalse(tx.has_pending_transaction(self.root))

    def test_process_termination_leaves_visible_journal_then_can_recover(self):
        real_replace = tx.os.replace
        def power_loss(src, dst):
            if Path(src).name == "after_1.csv":
                raise SystemExit("power off during CSV update")
            return real_replace(src, dst)
        with patch.object(tx.os, "replace", side_effect=power_loss):
            with self.assertRaises(SystemExit):
                tx.apply_register_transaction(self.root, self.updates, self.escape)
        self.assertTrue(tx.has_pending_transaction(self.root))
        self.assertNotEqual((self.root / tx.FILES[0]).read_bytes(),
                            self.original[tx.FILES[0]])
        with self.assertRaises(tx.PendingTransaction):
            tx.apply_register_transaction(self.root, self.updates, self.escape)
        result = tx.recover_pending_transaction(self.root)
        self.assertEqual(result["status"], "PREPARED_IMPORT_ROLLED_BACK")
        for rel in tx.FILES:
            self.assertEqual((self.root / rel).read_bytes(), self.original[rel])
        self.assertFalse(tx.has_pending_transaction(self.root))

    def test_missing_backup_causes_hard_failure_not_false_recovery(self):
        real_replace = tx.os.replace
        def power_loss(src, dst):
            if Path(src).name == "after_1.csv":
                raise SystemExit("simulated crash")
            return real_replace(src, dst)
        with patch.object(tx.os, "replace", side_effect=power_loss):
            with self.assertRaises(SystemExit):
                tx.apply_register_transaction(self.root, self.updates, self.escape)
        backup = tx.journal_dir(self.root) / "before_0.csv"
        backup.unlink()
        with self.assertRaises(tx.PendingTransaction):
            tx.recover_pending_transaction(self.root)
        self.assertTrue(tx.has_pending_transaction(self.root))

    def test_rejects_partial_updates_and_unknown_extra_files(self):
        with self.assertRaises(ValueError):
            tx.apply_register_transaction(self.root,
                                          {tx.FILES[0]: self.updates[tx.FILES[0]]},
                                          self.escape)
        self.assertFalse(tx.has_pending_transaction(self.root))

    def test_committed_journal_requires_hash_match_before_cleanup(self):
        tx.apply_register_transaction(self.root, self.updates, self.escape)
        journal = tx.journal_dir(self.root)
        journal.mkdir()
        manifest = {
            "schema_version": 1,
            "state": "COMMITTED",
            "entries": [{"path": rel,
                         "before_sha256": "0" * 64,
                         "after_sha256": tx._digest(self.root / rel)}
                        for rel in tx.FILES]
        }
        (journal / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.assertEqual(
            tx.recover_pending_transaction(self.root)["status"],
            "COMMITTED_CONFIRMED_AND_JOURNAL_CLEANED"
        )
        self.assertFalse(journal.exists())


if __name__ == "__main__":
    unittest.main()
