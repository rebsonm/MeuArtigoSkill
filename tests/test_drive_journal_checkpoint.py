"""Offline synthetic tests for Drive journal checkpoint, no network or credentials."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import drive_create_guard as guard
import drive_journal_checkpoint as checkpoint

ROOT = "synthetic-root-00001"
AUDIT = "synthetic-audit-0001"
REMOTE_ID = "synthetic-file-00001"


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


class FakeDrive:
    def __init__(self, raw):
        self.raw = raw
        self.posts = 0
        self.metadata_parent = AUDIT
        self.timeout_after_side_effect = False
        self.timeout_without_effect = False
        self.read_fails_after_write = False

    def sender(self, token, url, *, method="GET", body=None):
        if method == "PATCH":
            self.posts += 1
            if self.timeout_without_effect:
                raise checkpoint.JournalSyncError("DRIVE_JOURNAL_REMOTE_REQUEST_FAILED")
            self.raw = body
            if self.timeout_after_side_effect:
                raise checkpoint.JournalSyncError("DRIVE_JOURNAL_REMOTE_REQUEST_FAILED")
            return b'{"id":"' + REMOTE_ID.encode() + b'"}'
        if "alt=media" in url:
            if self.read_fails_after_write and self.posts:
                raise checkpoint.JournalSyncError("DRIVE_JOURNAL_REMOTE_REQUEST_FAILED")
            return self.raw
        return json.dumps({
            "id": REMOTE_ID, "name": "guard-journal.json",
            "parents": [self.metadata_parent],
            "mimeType": "application/json", "trashed": False
        }).encode()


class DurableJournalCheckpointTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.project_root = self.root / "research"
        self.project_root.mkdir()
        self.journal_path = self.root / "audit" / "journal.json"
        self.journal_path.parent.mkdir()
        self.plan = {"kind": "MEU_ARTIGO_DRIVE_DELIVERY_PLAN", "schema": 1,
                     "drive_root_id": ROOT, "project_folder": "research",
                     "entries": [{"type": "folder", "path": "01_Dados", "parent": ""}]}
        self.before = guard.initial_journal(self.plan)
        self.after = copy.deepcopy(self.before)
        self.after["operations"]["01_Dados"] = {
            "state": "OUTCOME_UNKNOWN", "attempt_id": "test-abc",
            "parent_id": ROOT, "before_scan_token": "scan-test-0001",
            "observed_remote_id": None
        }
        self.journal_path.write_bytes(encode(self.after))
        self.drive = FakeDrive(encode(self.before))

    def push(self, drive=None):
        d = drive or self.drive
        return checkpoint.push_once(REMOTE_ID, AUDIT, "dummy-token-long",
                                    self.plan, self.journal_path,
                                    hashlib.sha256(encode(self.before)).hexdigest(),
                                    sender=d.sender)

    def test_push_then_downloaded_digest_matches(self):
        result = self.push()
        self.assertEqual(result["action"], "JOURNAL_REMOTE_VERIFIED_AFTER_WRITE")
        self.assertEqual(result["sha256"], hashlib.sha256(encode(self.after)).hexdigest())
        self.assertEqual(self.drive.posts, 1)
        self.assertEqual(self.drive.raw, self.journal_path.read_bytes())

    def test_ambiguous_patch_with_actual_effect_is_verified(self):
        self.drive.timeout_after_side_effect = True
        result = self.push()
        self.assertTrue(result["ambiguous_response_reconciled"])
        self.assertEqual(self.drive.posts, 1)

    def test_timeout_without_effect_is_blocked_no_retry(self):
        self.drive.timeout_without_effect = True
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_WRITE_OUTCOME_UNVERIFIED"):
            self.push()
        self.assertEqual(self.drive.posts, 1)
        self.assertEqual(self.drive.raw, encode(self.before))

    def test_post_update_readback_failure_blocks(self):
        self.drive.read_fails_after_write = True
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_WRITE_OUTCOME_UNVERIFIED"):
            self.push()
        self.assertEqual(self.drive.posts, 1)

    def test_rollback_to_empty_intent_log_is_refused(self):
        self.drive.raw = encode(self.after)
        self.journal_path.write_bytes(encode(self.before))
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_TRANSITION_DROPPED_INTENT"):
            checkpoint.push_once(
                REMOTE_ID, AUDIT, "dummy-token-long", self.plan,
                self.journal_path, hashlib.sha256(encode(self.after)).hexdigest(),
                sender=self.drive.sender)
        self.assertEqual(self.drive.posts, 0)

    def test_changes_to_pending_attempt_identity_are_refused(self):
        self.drive.raw = encode(self.after)
        changed = copy.deepcopy(self.after)
        changed["operations"]["01_Dados"]["attempt_id"] = "forged-attempt"
        self.journal_path.write_bytes(encode(changed))
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_TRANSITION_CHANGED_INTENT"):
            checkpoint.push_once(
                REMOTE_ID, AUDIT, "dummy-token-long", self.plan,
                self.journal_path, hashlib.sha256(encode(self.after)).hexdigest(),
                sender=self.drive.sender)
        self.assertEqual(self.drive.posts, 0)

    def test_resolved_operation_cannot_return_to_unknown(self):
        resolved = copy.deepcopy(self.after)
        resolved["operations"]["01_Dados"].update(
            state="RESOLVED", observed_remote_id="synthetic-folder-0001",
            after_scan_token="scan-after-0002")
        self.drive.raw = encode(resolved)
        self.journal_path.write_bytes(encode(self.after))
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_TRANSITION_ROLLBACK"):
            checkpoint.push_once(
                REMOTE_ID, AUDIT, "dummy-token-long", self.plan,
                self.journal_path, hashlib.sha256(encode(resolved)).hexdigest(),
                sender=self.drive.sender)
        self.assertEqual(self.drive.posts, 0)

    def test_cannot_add_parallel_create_while_previous_is_uncertain(self):
        self.drive.raw = encode(self.after)
        next_state = copy.deepcopy(self.after)
        next_state["operations"]["other/child"] = {
            "state": "OUTCOME_UNKNOWN", "attempt_id": "another",
            "parent_id": ROOT, "before_scan_token": "scan-x"}
        self.journal_path.write_bytes(encode(next_state))
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_TRANSITION_UNRESOLVED_PREVIOUS_INTENT"):
            checkpoint.push_once(
                REMOTE_ID, AUDIT, "dummy-token-long", self.plan,
                self.journal_path, hashlib.sha256(encode(self.after)).hexdigest(),
                sender=self.drive.sender)
        self.assertEqual(self.drive.posts, 0)

    def test_remote_changed_precondition_blocks_no_patch(self):
        self.drive.raw = encode(self.after)
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_REMOTE_CHANGED_NO_WRITE"):
            self.push()
        self.assertEqual(self.drive.posts, 0)

    def test_identical_remote_journal_does_not_patch(self):
        self.journal_path.write_bytes(encode(self.before))
        result = self.push()
        self.assertEqual(result["action"], "JOURNAL_ALREADY_VERIFIED")
        self.assertEqual(self.drive.posts, 0)

    def test_parent_id_mismatch_blocks(self):
        self.drive.metadata_parent = "wrong-parent-0001"
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_REMOTE_IDENTITY_MISMATCH"):
            self.push()
        self.assertEqual(self.drive.posts, 0)

    def test_wrong_remote_plan_blocks(self):
        other = copy.deepcopy(self.before)
        other["drive_root_id"] = "wrong-root-000001"
        self.drive.raw = encode(other)
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_REMOTE_PLAN_MISMATCH"):
            self.push()
        self.assertEqual(self.drive.posts, 0)

    def test_corrupted_remote_json_blocks(self):
        self.drive.raw = b"not-json"
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_REMOTE_JSON_INVALID"):
            self.push()

    def test_restore_remote_checkpoint_to_new_local_audit_path(self):
        dst = self.root / "restored" / "journal.json"
        result = checkpoint.restore(REMOTE_ID, AUDIT, "dummy-token-long",
                                    self.plan, dst, hashlib.sha256(encode(self.before)).hexdigest(),
                                    project_root=self.project_root,
                                    sender=self.drive.sender)
        self.assertEqual(result["action"], "JOURNAL_RESTORED")
        self.assertEqual(dst.read_bytes(), encode(self.before))

    def test_restore_cannot_overwrite_existing_checkpoint(self):
        dst = self.root / "restored.json"
        dst.write_text("keep")
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "LOCAL_JOURNAL_EXISTS_NO_OVERWRITE"):
            checkpoint.restore(REMOTE_ID, AUDIT, "dummy-token-long",
                               self.plan, dst, hashlib.sha256(encode(self.before)).hexdigest(),
                                    project_root=self.project_root,
                               sender=self.drive.sender)
        self.assertEqual(dst.read_text(), "keep")

    def test_restore_cannot_write_within_scientific_project(self):
        dst = self.project_root / "journal.json"
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_MUST_BE_OUTSIDE_PROJECT"):
            checkpoint.restore(REMOTE_ID, AUDIT, "dummy-token-long",
                               self.plan, dst, hashlib.sha256(encode(self.before)).hexdigest(),
                                    project_root=self.project_root,
                               sender=self.drive.sender)

    def test_restore_requires_pinned_digest_against_old_valid_journal(self):
        # An old empty journal matches the plan but would lose the pending
        # operation: the independently retained digest must reject it.
        self.drive.raw = encode(self.before)
        expected_current = hashlib.sha256(encode(self.after)).hexdigest()
        dst = self.root / "stale-journal.json"
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_RESTORE_SHA_MISMATCH"):
            checkpoint.restore(REMOTE_ID, AUDIT, "dummy-token-long",
                               self.plan, dst, expected_current,
                               project_root=self.project_root,
                               sender=self.drive.sender)
        self.assertFalse(dst.exists())

    def test_restore_rejects_invalid_unpinned_digest(self):
        dst = self.root / "without-anchor.json"
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "EXPECTED_JOURNAL_SHA_INVALID"):
            checkpoint.restore(REMOTE_ID, AUDIT, "dummy-token-long",
                               self.plan, dst, "not-an-authenticated-sha",
                               project_root=self.project_root,
                               sender=self.drive.sender)
        self.assertFalse(dst.exists())

    def test_downloaded_remote_sha_verified_without_write(self):
        result = checkpoint.remote_matches(REMOTE_ID, AUDIT, "dummy-token-long",
                    self.plan, hashlib.sha256(encode(self.before)).hexdigest(),
                    sender=self.drive.sender)
        self.assertEqual(result["action"], "JOURNAL_REMOTE_VERIFIED")
        self.assertEqual(self.drive.posts, 0)

    def test_sha_mismatch_does_not_claim_verified(self):
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_REMOTE_SHA_MISMATCH"):
            checkpoint.remote_matches(REMOTE_ID, AUDIT, "dummy-token-long",
                                      self.plan, "a" * 64, sender=self.drive.sender)

    def test_recovered_intent_remains_unresolved_and_blocks_create_retry(self):
        self.drive.raw = encode(self.after)
        restored = self.root / "after-session-crash.json"
        checkpoint.restore(REMOTE_ID, AUDIT, "dummy-token-long",
                           self.plan, restored, hashlib.sha256(encode(self.after)).hexdigest(),
                           project_root=self.project_root,
                           sender=self.drive.sender)
        loaded = guard.read_journal(self.plan, restored)
        self.assertEqual(loaded["operations"]["01_Dados"]["state"], "OUTCOME_UNKNOWN")


if __name__ == "__main__":
    unittest.main()
