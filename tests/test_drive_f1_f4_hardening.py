"""F1-F4 fail-closed Drive tests: synthetic only; no Google Drive credentials or writes."""
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
import drive_api_proof as scanner

ROOT = "fictional-drive-root-001"
AUDIT = "fictional-audit-parent-001"
REMOTE = "fictional-journal-id-001"

def plan():
    return {"schema": 1, "kind": "MEU_ARTIGO_DRIVE_DELIVERY_PLAN",
            "drive_root_id": ROOT, "project_folder": "SYNTHETIC",
            "entries": [
                {"path": "01_Dados", "parent": "", "type": "folder"},
                {"path": "02_Analise", "parent": "", "type": "folder"},
                {"path": "01_Dados/file.csv", "parent": "01_Dados",
                 "type": "file", "sha256": "a"*64, "size": 1}]}

def pending(parent=ROOT):
    return {"attempt_id": "attempt-example-001",
            "parent_id": parent, "before_scan_token": "scan-before-0001",
            "state": "OUTCOME_UNKNOWN", "observed_remote_id": None}

def encoded(data):
    return (json.dumps(data,sort_keys=True,ensure_ascii=False,indent=2)+"\n").encode()

class FakeRemote:
    def __init__(self, content):
        self.content = content
        self.patches = 0
    def send(self, token, url, *, method="GET", body=None):
        if method == "PATCH":
            self.patches += 1
            self.content = body
            return b"{}"
        if "alt=media" in url:
            return self.content
        return json.dumps({"id":REMOTE,"parents":[AUDIT],"mimeType":"application/json",
                            "name":"journal.json","trashed":False}).encode()

class Stage07JournalContractTests(unittest.TestCase):
    def setUp(self):
        self.p = plan()
        self.empty = guard.initial_journal(self.p)
        self.j = copy.deepcopy(self.empty)
        self.j["operations"]["01_Dados"] = pending()

    def test_initial_journal_has_no_operations(self):
        guard.validate_journal(self.p, self.empty)

    def test_pending_journal_is_valid_and_creates_no_side_effect(self):
        guard.validate_journal(self.p, self.j)
        self.assertEqual(self.j["operations"]["01_Dados"]["state"],"OUTCOME_UNKNOWN")

    def test_unknown_path_is_rejected(self):
        self.j["operations"]["unknown_folder"] = self.j["operations"].pop("01_Dados")
        with self.assertRaisesRegex(ValueError,"UNKNOWN_OR_INVALID_INTENT"):
            guard.validate_journal(self.p,self.j)

    def test_file_path_cannot_be_create_intent(self):
        self.j["operations"]["01_Dados/file.csv"]=self.j["operations"].pop("01_Dados")
        with self.assertRaisesRegex(ValueError,"UNKNOWN_OR_INVALID_INTENT"):
            guard.validate_journal(self.p,self.j)

    def test_parent_switch_is_blocked_for_root_child(self):
        self.j["operations"]["01_Dados"]["parent_id"]="different-parent-00001"
        with self.assertRaisesRegex(ValueError,"ROOT_INTENT_PARENT_DRIFT"):
            guard.validate_journal(self.p,self.j)

    def test_resolved_without_actual_folder_id_is_blocked(self):
        op=self.j["operations"]["01_Dados"]
        op.update(state="RESOLVED",observed_remote_id="not a valid drive id",after_scan_token="scan-after-0002")
        with self.assertRaisesRegex(ValueError,"REMOTE_ID_INVALID"):
            guard.validate_journal(self.p,self.j)

    def test_pending_cannot_claim_remote_resolution(self):
        self.j["operations"]["01_Dados"]["observed_remote_id"]="fake-folder-00001"
        with self.assertRaisesRegex(ValueError,"PENDING_WITH_RESOLUTION"):
            guard.validate_journal(self.p,self.j)

    def test_resolved_scan_cannot_be_replayed(self):
        op=self.j["operations"]["01_Dados"]
        op.update(state="RESOLVED",observed_remote_id="folder-existing-0001",
                  after_scan_token="scan-before-0001")
        with self.assertRaisesRegex(ValueError,"STALE_RESOLUTION_SCAN"):
            guard.validate_journal(self.p,self.j)

    def test_extra_fields_are_not_ignored(self):
        self.j["operations"]["01_Dados"]["approved_by_ai"]=True
        with self.assertRaisesRegex(ValueError,"UNKNOWN_INTENT_FIELD"):
            guard.validate_journal(self.p,self.j)

    def test_two_unresolved_operations_are_blocked(self):
        self.j["operations"]["02_Analise"]=pending()
        with self.assertRaisesRegex(ValueError,"MULTIPLE_UNRESOLVED"):
            guard.validate_journal(self.p,self.j)

    def test_invalid_root_must_not_reuse_journal(self):
        self.j["drive_root_id"]="different-drive-0001"
        with self.assertRaisesRegex(ValueError,"PLAN_OR_ROOT"):
            guard.validate_journal(self.p,self.j)

    def test_recovered_journal_with_forged_operation_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/"journal.json"
            self.j["operations"]["fake-folder"] = self.j["operations"].pop("01_Dados")
            dest.write_bytes(encoded(self.j))
            with self.assertRaisesRegex(ValueError,"UNKNOWN_OR_INVALID_INTENT"):
                guard.read_journal(self.p,dest)

    def test_remote_forged_journal_is_not_accepted_even_with_expected_hash(self):
        fake=copy.deepcopy(self.j)
        fake["operations"]["01_Dados"]["parent_id"]="incorrect-parent-00001"
        remote=FakeRemote(encoded(fake))
        with self.assertRaisesRegex(checkpoint.JournalSyncError,"REMOTE_INTENT_INVALID"):
            checkpoint.remote_matches(REMOTE,AUDIT,"fictional-token-long",self.p,
                                      hashlib.sha256(remote.content).hexdigest(),sender=remote.send)
        self.assertEqual(remote.patches,0)

    def test_malformed_new_intent_never_reaches_patch(self):
        remote=FakeRemote(encoded(self.empty))
        altered=copy.deepcopy(self.j)
        altered["operations"]["01_Dados"]["parent_id"]="wrong-parent-00001"
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"journal.json"
            path.write_bytes(encoded(altered))
            with self.assertRaisesRegex(checkpoint.JournalSyncError,"LOCAL_INTENT_INVALID"):
                checkpoint.push_once(REMOTE,AUDIT,"fictional-token-long",self.p,path,
                    hashlib.sha256(remote.content).hexdigest(),sender=remote.send)
            self.assertEqual(remote.patches,0)

    def test_missing_journal_never_auto_initializes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"missing-journal.json"
            with self.assertRaisesRegex(ValueError,"MISSING_RECOVERY_REQUIRED"):
                guard.read_journal(self.p,path)
            self.assertFalse(path.exists())

    def test_invalid_digest_type_fails_before_patch(self):
        remote=FakeRemote(encoded(self.empty))
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"journal.json"
            path.write_bytes(encoded(self.j))
            with self.assertRaisesRegex(checkpoint.JournalSyncError,"EXPECTED_JOURNAL_SHA_INVALID"):
                checkpoint.push_once(REMOTE,AUDIT,"fictional-token-long",self.p,path,None,
                                     sender=remote.send)
            self.assertEqual(remote.patches,0)

    def test_duplicate_different_mime_names_block_inventory(self):
        items=[{"id":"folder-0000001","name":"01_Dados","mimeType":scanner.FOLDER_MIME,
                "parents":[ROOT]},{"id":"file-0000000001","name":"01_Dados",
                "mimeType":"text/plain","parents":[ROOT]}]
        scan=scanner.complete_parent_scan(ROOT,"fictional-token-long",
                 fetch_page=lambda token,params:{"kind":"drive#fileList","files":items})
        with self.assertRaisesRegex(scanner.DriveEvidenceError,"DUPLICATE_CHILD_NAMES"):
            scanner.merge_parent_scan(ROOT,"",scan)

    def test_incomplete_cursor_chain_blocks(self):
        with self.assertRaisesRegex(scanner.DriveEvidenceError,"PAGE_LIMIT_REACHED"):
            scanner.complete_parent_scan(ROOT,"fictional-token-long",
              fetch_page=lambda t,p:{"kind":"drive#fileList","files":[],"nextPageToken":"still-more"},
              max_pages=1)

if __name__=="__main__":
    unittest.main()
