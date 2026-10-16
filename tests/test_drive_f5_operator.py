"""F5 isolated authenticated-host contract tests; all API calls are simulated."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import drive_create_guard as guard
import drive_f5_operator as operator
import drive_f7_anchor as anchor
import drive_journal_checkpoint as checkpoint

ROOT = "synthetic-root-00001"
AUDIT_PARENT = "synthetic-audit-0001"
AUDIT_FILE = "synthetic-file-00001"
NEW_ID = "synthetic-created-0001"
TOKEN = "fake-credential-is-not-real"
KEY = bytes(range(32))


def wire(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


class FakeDrive:
    def __init__(self, plan):
        self.journal = wire(guard.initial_journal(plan))
        self.folders = []
        self.posts = 0
        self.patch_count = 0
        self.ambiguous = False
        self.create_effect = True
        self.fail_checkpoint = False
        self.root_name = "MEU_ARTIGO_PR74_TESTE_SINTETICO_FAKE"

    def sender(self, token, url, *, method="GET", body=None):
        if token != TOKEN:
            raise checkpoint.JournalSyncError("DRIVE_TOKEN_MISSING")
        if method == "PATCH":
            if self.fail_checkpoint:
                raise checkpoint.JournalSyncError("DRIVE_JOURNAL_REMOTE_REQUEST_FAILED")
            self.patch_count += 1
            self.journal = body
            return b"{}"
        if "alt=media" in url:
            return self.journal
        if AUDIT_FILE in url:
            return json.dumps({
                "id": AUDIT_FILE, "name": "audit.json", "parents": [AUDIT_PARENT],
                "mimeType": "application/json", "trashed": False,
            }).encode()
        if ROOT in url:
            return json.dumps({
                "id": ROOT, "name": self.root_name,
                "mimeType": operator.FOLDER_MIME, "trashed": False,
            }).encode()
        raise AssertionError("Unexpected remote request")

    def fetch_page(self, token, params):
        if token != TOKEN or "pageToken" in params:
            raise AssertionError("Unexpected scan")
        return {"kind": "drive#fileList", "files": [{
            "id": fid, "name": "01_Dados", "parents": [ROOT],
            "mimeType": operator.FOLDER_MIME, "trashed": False,
        } for fid in self.folders]}

    def creator(self, token, parent, name, *, sender):
        if token != TOKEN or parent != ROOT or name != "01_Dados":
            raise AssertionError("Wrong scope")
        self.posts += 1
        if self.create_effect:
            self.folders.append(NEW_ID)
        if self.ambiguous:
            raise checkpoint.JournalSyncError("DRIVE_JOURNAL_REMOTE_REQUEST_FAILED")
        return {"id": NEW_ID, "name": name, "parents": [parent]}


class FakeTrustedHead:
    """A test double ONLY; not an independent durable CAS authority."""
    def __init__(self, head):
        self.current = head
        self.reject_cas = False
        self.stale_readback = False
        self.cas_calls = 0
        self.candidate = None
        self.reject_on_call = None

    def read_head(self):
        if self.stale_readback and self.candidate:
            return self.candidate
        return self.current

    def compare_and_set(self, previous_head, new_head):
        self.cas_calls += 1
        if (self.reject_cas or self.reject_on_call == self.cas_calls
                or self.current != previous_head):
            return False
        if self.stale_readback:
            self.candidate = previous_head
        self.current = new_head
        return True


class F5HostTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.project = self.root / "project"
        self.project.mkdir()
        self.journal_path = self.root / "private" / "journal.json"
        self.journal_path.parent.mkdir()
        self.plan = {
            "kind": "MEU_ARTIGO_DRIVE_DELIVERY_PLAN", "schema": 1,
            "drive_root_id": ROOT, "project_folder": "project",
            "entries": [{"path": "01_Dados", "type": "folder", "parent": ""}]
        }
        self.drive = FakeDrive(self.plan)
        self.journal_path.write_bytes(self.drive.journal)
        self.anchor_archive = self.root / "trusted-executor-receipts"
        self.anchor_archive.mkdir(mode=0o700)
        first = anchor.seal_remote_checkpoint(
            self.anchor_archive, self.project, self.plan,
            AUDIT_PARENT, AUDIT_FILE, TOKEN,
            hashlib.sha256(self.drive.journal).hexdigest(),
            KEY, None, authorized_initial_bootstrap=True,
            sender=self.drive.sender)
        self.trusted_head = FakeTrustedHead(first["head_sha256"])

    def run_flow(self, *, execute=False, previous=None):
        previous = previous or hashlib.sha256(self.drive.journal).hexdigest()
        return operator.guarded_synthetic_create(
            self.plan, self.journal_path, self.project, "01_Dados",
            AUDIT_PARENT, AUDIT_FILE, TOKEN, previous, execute=execute,
            fetch_page=self.drive.fetch_page, sender=self.drive.sender,
            creator=self.drive.creator,
            trusted_head=self.trusted_head,
            anchor_archive=self.anchor_archive, anchor_key=KEY)

    def test_default_read_only_no_intent_or_external_create(self):
        result = self.run_flow()
        self.assertEqual(result["action"], "PRECHECK_ONLY_NO_CREATE")
        self.assertEqual(self.drive.posts, 0)
        self.assertEqual(self.drive.patch_count, 0)
        self.assertEqual(self.journal_path.read_bytes(), self.drive.journal)

    def test_single_success_checkpoints_intent_and_resolution(self):
        result = self.run_flow(execute=True)
        self.assertEqual(result["action"], "VERIFIED_SINGLE_SYNTHETIC_CREATE")
        self.assertEqual(result["remote_id"], NEW_ID)
        self.assertEqual(self.drive.posts, 1)
        self.assertEqual(self.drive.patch_count, 2)
        self.assertEqual(self.trusted_head.cas_calls, 2)
        self.assertEqual(len(list(self.anchor_archive.iterdir())), 3)
        self.assertEqual(hashlib.sha256(self.drive.journal).hexdigest(),
                         result["journal_sha256"])
        self.assertEqual(guard.read_journal(self.plan, self.journal_path)
                         ["operations"]["01_Dados"]["state"], "RESOLVED")

    def test_error_after_remote_side_effect_is_reconciled_once(self):
        self.drive.ambiguous = True
        result = self.run_flow(execute=True)
        self.assertEqual(result["action"], "VERIFIED_SINGLE_SYNTHETIC_CREATE")
        self.assertTrue(result["create_return_was_ambiguous"])
        self.assertEqual(self.drive.posts, 1)

    def test_no_remote_effect_blocks_without_retry(self):
        self.drive.ambiguous = True
        self.drive.create_effect = False
        result = self.run_flow(execute=True)
        self.assertEqual(result["action"], "BLOCKED_AMBIGUOUS_OUTCOME")
        self.assertEqual(self.drive.posts, 1)
        self.assertEqual(self.drive.patch_count, 1)
        self.assertEqual(guard.read_journal(self.plan, self.journal_path)
                         ["operations"]["01_Dados"]["state"], "OUTCOME_UNKNOWN")

    def test_checkpoint_failure_prevents_external_create(self):
        self.drive.fail_checkpoint = True
        with self.assertRaises(checkpoint.JournalSyncError):
            self.run_flow(execute=True)
        self.assertEqual(self.drive.posts, 0)

    def test_remote_journal_digest_mismatch_blocks_before_intent(self):
        with self.assertRaisesRegex(checkpoint.JournalSyncError,
                                    "JOURNAL_REMOTE_SHA_MISMATCH"):
            self.run_flow(execute=True, previous="a" * 64)
        self.assertEqual(self.drive.posts, 0)
        self.assertEqual(self.drive.patch_count, 0)

    def test_non_synthetic_root_is_rejected_before_all_writes(self):
        self.drive.root_name = "Actual Research Project"
        with self.assertRaisesRegex(operator.HostBlock,
                                    "SYNTHETIC_ROOT_IDENTITY_MISMATCH"):
            self.run_flow(execute=True)
        self.assertEqual(self.drive.posts, 0)
        self.assertEqual(self.drive.patch_count, 0)

    def test_prior_uncertain_create_is_blocked_even_in_read_only_mode(self):
        pending = guard.initial_journal(self.plan)
        pending["operations"]["01_Dados"] = {
            "state": "OUTCOME_UNKNOWN", "attempt_id": "pending-001",
            "parent_id": ROOT, "before_scan_token": "scan-before-0001",
            "observed_remote_id": None,
        }
        self.drive.journal = wire(pending)
        self.journal_path.write_bytes(self.drive.journal)
        next_receipt = anchor.seal_remote_checkpoint(
            self.anchor_archive, self.project, self.plan,
            AUDIT_PARENT, AUDIT_FILE, TOKEN,
            hashlib.sha256(self.drive.journal).hexdigest(),
            KEY, self.trusted_head.current, sender=self.drive.sender)
        self.assertTrue(self.trusted_head.compare_and_set(
            self.trusted_head.current, next_receipt["head_sha256"]))
        summary = self.run_flow(execute=False)
        self.assertEqual(
            summary["action"],
            "BLOCKED_PREVIOUS_CREATE_INTENT_REQUIRES_RECONCILIATION")
        self.assertFalse(summary["create_permitted"])
        attempt = self.run_flow(execute=True)
        self.assertEqual(
            attempt["action"],
            "BLOCKED_PREVIOUS_CREATE_INTENT_REQUIRES_RECONCILIATION")
        self.assertEqual(self.drive.posts, 0)
        self.assertEqual(self.drive.patch_count, 0)

    def test_missing_trusted_head_backend_blocks_live_create(self):
        with self.assertRaisesRegex(ValueError, "F8_TRUSTED_HEAD_BACKEND_REQUIRED"):
            operator.guarded_synthetic_create(
                self.plan, self.journal_path, self.project, "01_Dados",
                AUDIT_PARENT, AUDIT_FILE, TOKEN,
                hashlib.sha256(self.drive.journal).hexdigest(),
                execute=True, fetch_page=self.drive.fetch_page,
                sender=self.drive.sender, creator=self.drive.creator)
        self.assertEqual(self.drive.posts, 0)
        self.assertEqual(self.drive.patch_count, 0)

    def test_stale_trusted_head_blocks_before_intent(self):
        self.trusted_head.current = "0" * 64
        with self.assertRaisesRegex(ValueError, "ANCHOR_TRUSTED_HEAD_MISMATCH"):
            self.run_flow(execute=True)
        self.assertEqual(self.drive.posts, 0)
        self.assertEqual(self.drive.patch_count, 0)

    def test_failed_independent_cas_blocks_create_after_remote_intent(self):
        self.trusted_head.reject_cas = True
        with self.assertRaisesRegex(ValueError, "F8_TRUSTED_HEAD_CAS_REJECTED"):
            self.run_flow(execute=True)
        self.assertEqual(self.drive.posts, 0)
        self.assertEqual(self.drive.patch_count, 1)
        self.assertEqual(len(list(self.anchor_archive.iterdir())), 2)
        self.assertEqual(guard.read_journal(self.plan, self.journal_path)
                         ["operations"]["01_Dados"]["state"], "OUTCOME_UNKNOWN")
        with self.assertRaisesRegex(ValueError, "ANCHOR_TRUSTED_HEAD_MISMATCH"):
            self.run_flow(execute=True)
        self.assertEqual(self.drive.posts, 0)

    def test_independent_head_readback_failure_blocks_before_create(self):
        self.trusted_head.stale_readback = True
        with self.assertRaisesRegex(ValueError, "F8_TRUSTED_HEAD_READBACK_MISMATCH"):
            self.run_flow(execute=True)
        self.assertEqual(self.drive.posts, 0)
        self.assertEqual(self.drive.patch_count, 1)

    def test_resolved_state_head_cas_failure_never_claims_success(self):
        self.trusted_head.reject_on_call = 2
        with self.assertRaisesRegex(ValueError, "F8_TRUSTED_HEAD_CAS_REJECTED"):
            self.run_flow(execute=True)
        # Exactly one external create, but completion cannot be attested
        # because the high-watermark rejected the final signed receipt.
        self.assertEqual(self.drive.posts, 1)
        self.assertEqual(self.drive.patch_count, 2)
        self.assertEqual(self.trusted_head.cas_calls, 2)
        self.assertEqual(len(list(self.anchor_archive.iterdir())), 3)
        with self.assertRaisesRegex(ValueError, "ANCHOR_TRUSTED_HEAD_MISMATCH"):
            self.run_flow(execute=True)
        self.assertEqual(self.drive.posts, 1)

    def test_missing_archive_blocks_live_create(self):
        from shutil import rmtree
        rmtree(self.anchor_archive)
        with self.assertRaisesRegex(ValueError, "ANCHOR_PRIVATE_DIRECTORY_REQUIRED"):
            self.run_flow(execute=True)
        self.assertEqual(self.drive.posts, 0)
        self.assertEqual(self.drive.patch_count, 0)

    def test_invalid_hmac_key_blocks_before_create(self):
        with self.assertRaisesRegex(ValueError, "F8_HMAC_KEY_REQUIRED"):
            operator.guarded_synthetic_create(
                self.plan, self.journal_path, self.project, "01_Dados",
                AUDIT_PARENT, AUDIT_FILE, TOKEN,
                hashlib.sha256(self.drive.journal).hexdigest(),
                execute=True, fetch_page=self.drive.fetch_page,
                sender=self.drive.sender, creator=self.drive.creator,
                trusted_head=self.trusted_head,
                anchor_archive=self.anchor_archive, anchor_key=b"short")
        self.assertEqual(self.drive.posts, 0)

    def test_existing_remote_folder_is_never_created_again(self):
        self.drive.folders.append(NEW_ID)
        result = self.run_flow(execute=True)
        self.assertEqual(result["action"], "BLOCKED_OR_NOT_NEEDED")
        self.assertEqual(self.drive.posts, 0)

    def test_old_journal_cannot_be_reused_after_side_effect(self):
        self.run_flow(execute=True)
        with self.assertRaisesRegex(operator.HostBlock,
                                    "LOCAL_AND_REMOTE_JOURNAL_DIFFER"):
            # Simulate a stale copy of the original journal after restart.
            self.journal_path.write_bytes(wire(guard.initial_journal(self.plan)))
            self.run_flow(execute=True)
        self.assertEqual(self.drive.posts, 1)

    def test_existing_host_lock_is_never_removed(self):
        lock = self.journal_path.with_name("journal.json.f5-host.lock")
        lock.write_text("other-worker")
        with self.assertRaises(FileExistsError):
            self.run_flow(execute=True)
        self.assertEqual(lock.read_text(), "other-worker")
        self.assertEqual(self.drive.posts, 0)


if __name__ == "__main__":
    unittest.main()
