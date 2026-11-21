"""F7 immutable checkpoint anchor chain tests; fake Drive, no credentials."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import drive_create_guard as guard
import drive_f7_anchor as anchor
import drive_journal_checkpoint as checkpoint

ROOT = "synthetic-root-00001"
AUDIT = "synthetic-audit-0001"
FILE = "synthetic-file-00001"
TOKEN = "synthetic-bearer-token"
KEY = bytes(range(32))


def wire(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


class Remote:
    def __init__(self, raw):
        self.raw = raw
        self.reads = 0

    def sender(self, token, url, *, method="GET", body=None):
        if token != TOKEN:
            raise AssertionError("Unexpected token")
        if method != "GET":
            raise AssertionError("Anchor must never mutate Drive")
        if "alt=media" in url:
            self.reads += 1
            return self.raw
        return json.dumps({"id": FILE, "name": "audit.json",
                           "mimeType": "application/json",
                           "parents": [AUDIT], "trashed": False}).encode()


class ReceiptChainTests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.temp = Path(t.name)
        self.project = self.temp / "research-project"
        self.project.mkdir()
        self.archive = self.temp / "trusted-executor-archive"
        self.archive.mkdir(mode=0o700)
        self.plan = {
            "schema": 1, "kind": "MEU_ARTIGO_DRIVE_DELIVERY_PLAN",
            "drive_root_id": ROOT, "project_folder": "research-project",
            "entries": [{"type": "folder", "path": "01_Dados", "parent": ""}]
        }
        self.initial = guard.initial_journal(self.plan)
        self.pending = copy.deepcopy(self.initial)
        self.pending["operations"]["01_Dados"] = {
            "state": "OUTCOME_UNKNOWN", "attempt_id": "synthetic-attempt-1",
            "parent_id": ROOT, "before_scan_token": "scan-before-0001",
            "observed_remote_id": None
        }
        self.remote = Remote(wire(self.initial))

    def digest(self):
        return hashlib.sha256(self.remote.raw).hexdigest()

    def seal(self, head=None, *, key=KEY):
        return anchor.seal_remote_checkpoint(
            self.archive, self.project, self.plan, AUDIT, FILE,
            TOKEN, self.digest(), key, head,
            authorized_initial_bootstrap=(head is None),
            sender=self.remote.sender)

    def verified(self, head, *, key=KEY):
        return anchor.verify_remote_against_anchor(
            self.archive, self.project, self.plan, AUDIT, FILE,
            TOKEN, head, key, sender=self.remote.sender)

    def test_missing_initial_attestation_blocks_before_network_or_files(self):
        with self.assertRaisesRegex(anchor.AnchorError,
                                    "ANCHOR_NEW_HISTORY_ATTESTATION_REQUIRED"):
            anchor.seal_remote_checkpoint(
                self.archive, self.project, self.plan, AUDIT, FILE,
                TOKEN, self.digest(), KEY, None,
                sender=self.remote.sender)
        self.assertEqual(self.remote.reads, 0)
        self.assertEqual(list(self.archive.iterdir()), [])

    def test_initial_attestation_rejected_if_previous_head_supplied(self):
        original = self.seal()
        self.remote.raw = wire(self.pending)
        with self.assertRaisesRegex(anchor.AnchorError,
                                    "ANCHOR_BOOTSTRAP_ONLY_FOR_NEW_HISTORY"):
            anchor.seal_remote_checkpoint(
                self.archive, self.project, self.plan, AUDIT, FILE,
                TOKEN, self.digest(), KEY, original["head_sha256"],
                authorized_initial_bootstrap=True,
                sender=self.remote.sender)

    def test_initial_receipt_requires_remote_readback(self):
        result = self.seal()
        self.assertEqual(result["action"], "ANCHOR_RECEIPT_SEALED")
        self.assertEqual(result["sequence"], 1)
        self.assertTrue(result["external_head_persistence_required"])
        self.assertEqual(self.remote.reads, 1)
        self.assertTrue((self.archive / "00000001.json").exists())
        self.assertEqual(result["head_sha256"],
                         anchor.sha((self.archive / "00000001.json").read_bytes()))

    def test_second_receipt_links_previous_and_rechecks_remote(self):
        first = self.seal()
        self.remote.raw = wire(self.pending)
        second = self.seal(first["head_sha256"])
        self.assertEqual(second["sequence"], 2)
        self.assertNotEqual(first["head_sha256"], second["head_sha256"])
        self.assertEqual(self.remote.reads, 2)
        result = self.verified(second["head_sha256"])
        self.assertEqual(result["action"], "ANCHOR_AND_REMOTE_MATCH")
        self.assertFalse(result["create_permitted"])
        self.assertEqual(result["count"], 2)

    def test_valid_old_receipt_replay_is_blocked_by_trusted_latest_head(self):
        first = self.seal()
        self.remote.raw = wire(self.pending)
        last = self.seal(first["head_sha256"])
        # Roll back BOTH the remote file and the visible archive to the old
        # internally consistent first record: an independently held head wins.
        self.remote.raw = wire(self.initial)
        (self.archive / "00000002.json").unlink()
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_TRUSTED_HEAD_MISMATCH"):
            self.verified(last["head_sha256"])

    def test_archive_loss_requires_manual_recovery(self):
        first = self.seal()
        (self.archive / "00000001.json").unlink()
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_HISTORY_MISSING"):
            self.verified(first["head_sha256"])

    def test_hmac_tampering_is_rejected(self):
        result = self.seal()
        path = self.archive / "00000001.json"
        doc = json.loads(path.read_bytes())
        doc["payload"]["journal_sha256"] = "b" * 64
        path.write_bytes(anchor.canonical(doc))
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_HMAC_INVALID"):
            self.verified(result["head_sha256"])

    def test_wrong_key_cannot_approve_existing_archive(self):
        result = self.seal()
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_HMAC_INVALID"):
            self.verified(result["head_sha256"], key=bytes(range(1, 33)))

    def test_wrong_pinned_head_is_rejected(self):
        self.seal()
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_TRUSTED_HEAD_MISMATCH"):
            self.verified("0" * 64)

    def test_existing_history_must_not_be_silently_reinitialized(self):
        self.seal()
        self.remote.raw = wire(self.pending)
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_PINNED_HEAD_REQUIRED"):
            self.seal()

    def test_duplicate_remote_checkpoint_receipt_is_refused(self):
        first = self.seal()
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_REPEATED_JOURNAL_STATE"):
            self.seal(first["head_sha256"])

    def test_remote_state_mismatch_refuses_seal_without_new_file(self):
        first = self.seal()
        # Local desired digest is the new pending state, but the remote
        # still exposes the old initial checkpoint (no successful PATCH).
        with self.assertRaisesRegex(checkpoint.JournalSyncError, "JOURNAL_REMOTE_SHA_MISMATCH"):
            anchor.seal_remote_checkpoint(
                self.archive, self.project, self.plan, AUDIT, FILE,
                TOKEN, hashlib.sha256(wire(self.pending)).hexdigest(),
                KEY, first["head_sha256"], sender=self.remote.sender)
        self.assertFalse((self.archive / "00000002.json").exists())

    def test_remote_modified_after_seal_is_detected_on_verify(self):
        first = self.seal()
        self.remote.raw = wire(self.pending)
        with self.assertRaisesRegex(checkpoint.JournalSyncError, "JOURNAL_REMOTE_SHA_MISMATCH"):
            self.verified(first["head_sha256"])

    def test_directory_inside_research_project_is_rejected(self):
        inside = self.project / "audit"
        inside.mkdir(mode=0o700)
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_PRIVATE_DIRECTORY_REQUIRED"):
            anchor.seal_remote_checkpoint(
                inside, self.project, self.plan, AUDIT, FILE,
                TOKEN, self.digest(), KEY, None,
                authorized_initial_bootstrap=True,
                sender=self.remote.sender)

    def test_directory_group_access_is_rejected(self):
        os.chmod(self.archive, 0o750)
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_DIRECTORY_PERMISSIONS_TOO_BROAD"):
            self.seal()

    def test_unrecognized_file_in_archive_is_rejected(self):
        (self.archive / "unsigned.txt").write_text("unsafe")
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_UNEXPECTED_OR_UNSAFE_ENTRY"):
            self.seal()

    def test_gap_in_receipt_numbering_is_rejected(self):
        first = self.seal()
        self.remote.raw = wire(self.pending)
        second = self.seal(first["head_sha256"])
        (self.archive / "00000002.json").rename(self.archive / "00000003.json")
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_HISTORY_GAP"):
            self.verified(second["head_sha256"])

    def test_archive_not_an_authority_without_independent_head(self):
        self.seal()
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_PINNED_HEAD_REQUIRED"):
            anchor.read_verified_chain(self.archive, self.plan, AUDIT, FILE,
                                       KEY, self.project, None)

    def test_receipt_file_must_not_be_world_readable(self):
        record = self.seal()
        os.chmod(self.archive / "00000001.json", 0o644)
        with self.assertRaisesRegex(anchor.AnchorError,
                                    "ANCHOR_RECEIPT_PERMISSIONS_TOO_BROAD"):
            self.verified(record["head_sha256"])

    def test_symlinked_archive_is_rejected(self):
        link = self.temp / "other-archive-link"
        link.symlink_to(self.archive, target_is_directory=True)
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_PRIVATE_DIRECTORY_REQUIRED"):
            anchor.seal_remote_checkpoint(
                link, self.project, self.plan, AUDIT, FILE,
                TOKEN, self.digest(), KEY, None,
                authorized_initial_bootstrap=True,
                sender=self.remote.sender)

    def test_plan_change_makes_previous_receipt_unusable(self):
        first = self.seal()
        changed_plan = copy.deepcopy(self.plan)
        changed_plan["entries"].append(
            {"type": "folder", "path": "02_Extra", "parent": ""})
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_CHAIN_OR_SCOPE_INVALID"):
            anchor.read_verified_chain(
                self.archive, changed_plan, AUDIT, FILE,
                KEY, self.project, first["head_sha256"])

    def test_audit_file_swap_cannot_validate_chain(self):
        first = self.seal()
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_CHAIN_OR_SCOPE_INVALID"):
            anchor.read_verified_chain(
                self.archive, self.plan, AUDIT, "synthetic-other-file-001",
                KEY, self.project, first["head_sha256"])

    def test_moved_audit_parent_cannot_validate_chain(self):
        first = self.seal()
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_CHAIN_OR_SCOPE_INVALID"):
            anchor.read_verified_chain(
                self.archive, self.plan, "synthetic-other-parent-01", FILE,
                KEY, self.project, first["head_sha256"])

    def test_secret_key_too_short_refused_before_sealing(self):
        with self.assertRaisesRegex(anchor.AnchorError, "ANCHOR_KEY_UNAVAILABLE"):
            self.seal(key=b"short")
        self.assertEqual(self.remote.reads, 0)
        self.assertEqual(list(self.archive.iterdir()), [])

    def test_untrusted_remote_readback_is_not_a_ledger_signature(self):
        self.seal()
        self.remote.raw = wire(self.pending)
        # Retain the old signed receipt but change remote journal. A correct
        # signed chain cannot by itself ratify changed remote content.
        old = (self.archive / "00000001.json").read_bytes()
        pinned = hashlib.sha256(old).hexdigest()
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_REMOTE_SHA_MISMATCH"):
            self.verified(pinned)

    def test_anchor_receipts_never_write_scientific_gates(self):
        gates = self.project / "18_Human_Validation_Gates.csv"
        gates.write_text("GATE-0001,PENDING")
        self.seal()
        self.assertEqual(gates.read_text(), "GATE-0001,PENDING")


if __name__ == "__main__":
    unittest.main()
