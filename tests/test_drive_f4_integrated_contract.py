"""F4 simulated end-to-end contract: page receipts, durable intent, one create.

This suite uses an in-memory Drive double and invokes the production helpers.
It is NOT a live API, OAuth, independent concurrent-writer, or installed-Skill
acceptance test. No research records are modified.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import drive_api_proof as scanner
import drive_create_guard as guard
import drive_journal_checkpoint as checkpoint

ROOT = "synthetic-root-00001"
AUDIT = "synthetic-audit-0001"
JOURNAL_ID = "synthetic-journal-0001"
FOLDER = "synthetic-subfolder-1"
TOKEN = "test-only-placeholder"


class FakeConnectedDrive:
    def __init__(self, initial_journal: bytes):
        self.folder_id = None
        self.remote_journal = initial_journal
        self.create_calls = 0
        self.patch_calls = 0

    def list_page(self, token, params):
        assert token == TOKEN
        assert params.get("q") == "'" + ROOT + "' in parents and trashed = false"
        children = []
        if self.folder_id:
            children.append({
                "id": self.folder_id, "name": "01_Dados",
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [ROOT], "trashed": False,
            })
        return {"kind": "drive#fileList", "files": children}

    def create_folder(self, *, effect: bool):
        self.create_calls += 1
        if effect:
            self.folder_id = FOLDER
        raise RuntimeError("Simulated ambiguous transport failure, never real API")

    def journal_sender(self, token, url, *, method="GET", body=None):
        assert token == TOKEN
        if method == "PATCH":
            self.patch_calls += 1
            self.remote_journal = body
            return b"{}"
        if "alt=media" in url:
            return self.remote_journal
        return json.dumps({
            "id": JOURNAL_ID, "name": "create-journal.json",
            "parents": [AUDIT], "mimeType": "application/json",
            "trashed": False,
        }).encode("utf-8")


class IntegratedF4ContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.project = self.root / "synthetic-project"
        self.project.mkdir()
        self.audit = self.root / "audit"
        self.audit.mkdir()
        self.journal = self.audit / "journal.json"
        self.plan = {
            "schema": 1, "kind": "MEU_ARTIGO_DRIVE_DELIVERY_PLAN",
            "drive_root_id": ROOT, "project_folder": self.project.name,
            "entries": [{"type": "folder", "path": "01_Dados", "parent": ""}],
        }
        self.remote = FakeConnectedDrive(
            (json.dumps(guard.initial_journal(self.plan), sort_keys=True,
                        indent=2, ensure_ascii=False) + "\n").encode("utf-8"))

    def scan(self):
        current = scanner.complete_parent_scan(
            ROOT, TOKEN, fetch_page=self.remote.list_page)
        return scanner.merge_parent_scan(ROOT, "", current)

    def checkpoint(self, expected_previous_sha):
        return checkpoint.push_once(
            JOURNAL_ID, AUDIT, TOKEN, self.plan, self.journal,
            expected_previous_sha, sender=self.remote.journal_sender)

    def initialize_and_prepare(self):
        inv = self.scan()
        setup = guard.locked_update(
            self.plan, inv, self.journal, "01_Dados", "initialize",
            project_root=self.project, initialize_authorized=True)
        self.assertEqual(setup["action"], "JOURNAL_INITIALIZED_NEW_PROJECT")
        self.assertEqual(
            setup["journal_sha256"], hashlib.sha256(self.journal.read_bytes()).hexdigest())
        # Independently pre-provisioned simulated remote file starts at this
        # same initial serialized content. No silent creation performed here.
        self.assertEqual(self.journal.read_bytes(), self.remote.remote_journal)
        old = hashlib.sha256(self.remote.remote_journal).hexdigest()
        result = guard.locked_update(
            self.plan, inv, self.journal, "01_Dados", "prepare",
            project_root=self.project)
        self.assertEqual(result["action"], "CREATE_FOLDER_ONCE")
        self.assertEqual(result["journal_sha256"],
                         hashlib.sha256(self.journal.read_bytes()).hexdigest())
        persisted = self.checkpoint(old)
        self.assertEqual(persisted["action"], "JOURNAL_REMOTE_VERIFIED_AFTER_WRITE")
        self.assertEqual(persisted["sha256"], result["journal_sha256"])
        self.assertEqual(self.remote.patch_calls, 1)
        return result

    def test_ambiguous_create_with_side_effect_recovers_same_id_and_journal(self):
        self.initialize_and_prepare()
        with self.assertRaisesRegex(RuntimeError, "Simulated ambiguous"):
            self.remote.create_folder(effect=True)
        inv = self.scan()
        outcome = guard.locked_update(
            self.plan, inv, self.journal, "01_Dados", "resolve",
            project_root=self.project)
        self.assertEqual(outcome["action"], "RESOLVED_EXISTING_REMOTE_FOLDER")
        self.assertEqual(outcome["remote_id"], FOLDER)
        expected_before = hashlib.sha256(self.remote.remote_journal).hexdigest()
        persisted = self.checkpoint(expected_before)
        self.assertEqual(persisted["sha256"], outcome["journal_sha256"])
        self.assertEqual(self.remote.patch_calls, 2)
        # Simulate a new session, with the local journal no longer available.
        self.journal.unlink()
        recovered = self.audit / "recovered.json"
        restored = checkpoint.restore(
            JOURNAL_ID, AUDIT, TOKEN, self.plan, recovered, persisted["sha256"],
            project_root=self.project, sender=self.remote.journal_sender)
        self.assertEqual(restored["action"], "JOURNAL_RESTORED")
        saved = guard.read_journal(self.plan, recovered)
        self.assertEqual(saved["operations"]["01_Dados"]["state"], "RESOLVED")
        self.assertEqual(saved["operations"]["01_Dados"]["observed_remote_id"], FOLDER)
        # The existing folder is reused; no second create is proposed.
        before = self.remote.create_calls
        observed = guard.inspect_target(self.plan, self.scan(), "01_Dados", ROOT)
        self.assertEqual(observed["action"], "REUSE_EXISTING")
        self.assertEqual(self.remote.create_calls, before)
        self.assertEqual(before, 1)

    def test_ambiguous_create_without_side_effect_stays_blocked(self):
        self.initialize_and_prepare()
        with self.assertRaisesRegex(RuntimeError, "Simulated ambiguous"):
            self.remote.create_folder(effect=False)
        inv = self.scan()
        result = guard.locked_update(
            self.plan, inv, self.journal, "01_Dados", "resolve",
            project_root=self.project)
        self.assertEqual(result["action"], "BLOCKED_AMBIGUOUS_OUTCOME")
        blocked = guard.locked_update(
            self.plan, inv, self.journal, "01_Dados", "prepare",
            project_root=self.project)
        self.assertEqual(blocked["action"], "REINSPECT_NO_RETRY")
        self.assertEqual(self.remote.create_calls, 1)

    def test_crash_after_prepared_intent_but_before_create_cannot_recreate(self):
        self.initialize_and_prepare()
        self.journal.unlink()
        with self.assertRaisesRegex(ValueError, "JOURNAL_MISSING_RECOVERY_REQUIRED"):
            guard.locked_update(
                self.plan, self.scan(), self.journal, "01_Dados", "prepare",
                project_root=self.project)
        dst = self.audit / "recovered-before-create.json"
        anchor = hashlib.sha256(self.remote.remote_journal).hexdigest()
        checkpoint.restore(
            JOURNAL_ID, AUDIT, TOKEN, self.plan, dst, anchor,
            project_root=self.project, sender=self.remote.journal_sender)
        self.assertEqual(
            guard.locked_update(
                self.plan, self.scan(), dst, "01_Dados", "prepare",
                project_root=self.project)["action"],
            "REINSPECT_NO_RETRY")
        self.assertEqual(self.remote.create_calls, 0)


if __name__ == "__main__":
    unittest.main()
