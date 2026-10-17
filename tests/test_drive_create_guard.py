"""Offline, deliberately fictional ambiguous Drive create outcomes."""
from __future__ import annotations

import copy
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import drive_delivery as delivery
import drive_create_guard as guard

ROOT = "synthetic-root-00001"
CHILD = "synthetic-child-0001"


class FolderGuardTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.temp = Path(temporary.name)
        self.journal_path = self.temp / "audit" / "attempts.json"
        self.plan = {
            "kind": "MEU_ARTIGO_DRIVE_DELIVERY_PLAN", "schema": 1,
            "drive_root_id": ROOT, "project_folder": "SYNTHETIC",
            "entries": [
                {"type": "folder", "path": "01_Dados", "parent": ""},
                {"type": "file", "path": "01_Dados/test.csv", "parent": "01_Dados",
                 "size": 3, "sha256": "a" * 64}
            ]
        }
        self.inventory = {
            "schema": 1, "drive_root_id": ROOT, "observed_via": "FIXTURE",
            "entries": [], "parent_scans": [
                {"parent_id": ROOT, "complete": True,
                 "scan_token": "scan-initial-0001", "children": []}
            ]
        }
        self.journal = guard.initial_journal(self.plan)

    def live(self, inventory=None):
        # Fictional provider-shaped evidence: tests validation, NOT actual Drive.
        inv = copy.deepcopy(self.inventory if inventory is None else inventory)
        inv["observed_via"] = "LIVE_DRIVE"
        for scan in inv["parent_scans"]:
            scan["page_evidence"] = [{
                "source": "GOOGLE_DRIVE_FILES_LIST",
                "request_page_token": None, "next_page_token": None,
                "item_ids": [c["id"] for c in scan["children"]]
            }]
        return inv

    def begin(self, inventory=None, journal=None):
        return guard.create_preflight(
            self.plan, self.inventory if inventory is None else inventory,
            self.journal if journal is None else journal, "01_Dados",
            allow_fixture=True)

    def resolve(self, inventory=None, journal=None):
        return guard.resolve_create(
            self.plan, self.inventory if inventory is None else inventory,
            self.journal if journal is None else journal, "01_Dados",
            allow_fixture=True)

    def fresh(self, *, count=1):
        remote = copy.deepcopy(self.inventory)
        remote["parent_scans"][0]["scan_token"] = "scan-after-call-0002"
        if count:
            remote["entries"] = [{
                "type": "folder", "path": "01_Dados",
                "id": CHILD, "parent_id": ROOT
            }]
            remote["parent_scans"][0]["children"] = [
                {"name": "01_Dados", "type": "folder", "id": CHILD}
            ]
        if count == 2:
            remote["entries"].append({
                "type": "folder", "path": "01_Dados",
                "id": "synthetic-other-0002", "parent_id": ROOT
            })
            remote["parent_scans"][0]["children"].append({
                "name": "01_Dados", "type": "folder", "id": "synthetic-other-0002"
            })
        return remote

    def test_next_action_rejects_blind_folder_create(self):
        next_step = delivery.next_action(self.plan, self.inventory, allow_fixture=True)
        self.assertEqual(next_step["action"], "CHECK_PARENT_FOR_CREATE")
        self.assertIn("drive_create_guard.py", next_step["required_guard"])

    def test_complete_inventory_required_before_first_attempt(self):
        inv = copy.deepcopy(self.inventory)
        inv.pop("parent_scans")
        with self.assertRaisesRegex(ValueError, "PARENT_COMPLETE_SCAN"):
            self.begin(inv)
        self.assertEqual(self.journal["operations"], {})

    def test_partial_paginated_listing_is_rejected(self):
        inv = copy.deepcopy(self.inventory)
        inv["parent_scans"][0]["complete"] = False
        with self.assertRaisesRegex(ValueError, "PARENT_COMPLETE_SCAN"):
            self.begin(inv)

    def test_scan_must_correspond_to_observed_inventory(self):
        inv = copy.deepcopy(self.inventory)
        inv["parent_scans"][0]["children"].append({
            "id": CHILD, "name": "something-else", "type": "folder"
        })
        with self.assertRaisesRegex(ValueError, "PARENT_SCAN_INVENTORY_MISMATCH"):
            self.begin(inv)

    def test_first_create_returns_once_after_journaling(self):
        step, journal = self.begin()
        self.assertEqual(step["action"], "CREATE_FOLDER_ONCE")
        self.assertEqual(step["parent_id"], ROOT)
        self.assertEqual(step["name"], "01_Dados")
        self.assertEqual(journal["operations"]["01_Dados"]["state"], "OUTCOME_UNKNOWN")
        self.assertEqual(len(step["attempt_id"]), 24)

    def test_repeated_create_same_path_refused_even_after_timeout(self):
        first, journal = self.begin()
        second, _ = self.begin(journal=journal)
        self.assertEqual(first["action"], "CREATE_FOLDER_ONCE")
        self.assertEqual(second["action"], "REINSPECT_NO_RETRY")
        self.assertEqual(first["attempt_id"], second["attempt_id"])

    def test_ambiguous_error_with_actual_side_effect_is_reused(self):
        _, journal = self.begin()
        status, new_journal = self.resolve(self.fresh(), journal)
        self.assertEqual(status["action"], "RESOLVED_EXISTING_REMOTE_FOLDER")
        self.assertEqual(status["remote_id"], CHILD)
        self.assertEqual(new_journal["operations"]["01_Dados"]["state"], "RESOLVED")
        later = self.fresh()
        later["parent_scans"][0]["scan_token"] = "scan-verified-again-0003"
        again, _ = self.resolve(later, new_journal)
        self.assertEqual(again["action"], "ALREADY_RESOLVED")

    def test_resolved_intent_requires_new_remote_observation(self):
        _, journal = self.begin()
        _, journal = self.resolve(self.fresh(), journal)
        status, _ = self.resolve(self.fresh(), journal)
        self.assertEqual(status["action"], "REINSPECT_PARENT")

    def test_resolved_folder_disappearance_is_not_already_resolved(self):
        _, journal = self.begin()
        _, journal = self.resolve(self.fresh(), journal)
        later = self.fresh(count=0)
        later["parent_scans"][0]["scan_token"] = "scan-recheck-after-removal"
        status, _ = self.resolve(later, journal)
        self.assertEqual(status["action"], "BLOCKED_PREVIOUS_RESOLUTION_DRIFT")

    def test_parent_replacement_blocks_reconciliation_under_old_parent(self):
        plan = copy.deepcopy(self.plan)
        plan["entries"] = [
            {"type": "folder", "path": "01_Dados", "parent": ""},
            {"type": "folder", "path": "01_Dados/subfolder", "parent": "01_Dados"},
        ]
        old_parent = "synthetic-parent-old-1"
        new_parent = "synthetic-parent-new-1"
        initial = copy.deepcopy(self.inventory)
        initial["entries"] = [
            {"type": "folder", "path": "01_Dados", "id": old_parent, "parent_id": ROOT}
        ]
        initial["parent_scans"] = [
            {"parent_id": old_parent, "complete": True,
             "scan_token": "scan-before-parent-change", "children": []}
        ]
        journal = guard.initial_journal(plan)
        step, journal = guard.create_preflight(
            plan, initial, journal, "01_Dados/subfolder", allow_fixture=True)
        self.assertEqual(step["action"], "CREATE_FOLDER_ONCE")
        after = copy.deepcopy(initial)
        after["entries"] = [
            {"type": "folder", "path": "01_Dados", "id": new_parent, "parent_id": ROOT},
            {"type": "folder", "path": "01_Dados/subfolder", "id": CHILD,
             "parent_id": old_parent}
        ]
        after["parent_scans"][0].update(
            scan_token="scan-after-parent-change",
            children=[{"id": CHILD, "name": "subfolder", "type": "folder"}]
        )
        outcome, _ = guard.resolve_create(
            plan, after, journal, "01_Dados/subfolder", allow_fixture=True)
        self.assertEqual(outcome["action"], "BLOCKED_PARENT_DRIFT")

    def test_inconsistent_target_path_cannot_be_accepted(self):
        _, journal = self.begin()
        after = self.fresh()
        after["entries"][0]["path"] = "outside/01_Dados"
        outcome, _ = self.resolve(after, journal)
        self.assertEqual(outcome["action"], "BLOCKED_INCONSISTENT_TARGET_PATH")

    def test_duplicate_inventory_ids_cannot_pass_parent_scan(self):
        scan = self.fresh(count=2)
        scan["entries"][1]["id"] = scan["entries"][0]["id"]
        with self.assertRaisesRegex(ValueError, "PARENT_SCAN_INVENTORY_MISMATCH"):
            guard.direct_scan(self.plan, scan, ROOT, allow_fixture=True)

    def test_timeout_after_unobserved_effect_never_retries_blindly(self):
        _, journal = self.begin()
        result, _ = self.resolve(self.fresh(count=0), journal)
        self.assertEqual(result["action"], "BLOCKED_AMBIGUOUS_OUTCOME")
        second, _ = self.begin(journal=journal)
        self.assertEqual(second["action"], "REINSPECT_NO_RETRY")

    def test_stale_pre_operation_scan_cannot_resolve(self):
        _, journal = self.begin()
        output, _ = self.resolve(self.inventory, journal)
        self.assertEqual(output["action"], "REINSPECT_PARENT")

    def test_duplicate_folders_after_ambiguous_call_are_blocked(self):
        _, journal = self.begin()
        output, _ = self.resolve(self.fresh(count=2), journal)
        self.assertEqual(output["action"], "BLOCKED_DUPLICATE_NAME")

    def test_wrong_type_folder_name_is_blocked(self):
        _, journal = self.begin()
        inv = self.fresh()
        inv["entries"][0]["type"] = "file"
        inv["parent_scans"][0]["children"][0]["type"] = "file"
        output, _ = self.resolve(inv, journal)
        self.assertEqual(output["action"], "BLOCKED_TYPE_CONFLICT")

    def test_fixtures_not_accepted_as_live_drives(self):
        with self.assertRaisesRegex(ValueError, "LIVE_DRIVE_INVENTORY_REQUIRED"):
            guard.create_preflight(self.plan, self.inventory, self.journal, "01_Dados")

    def test_changed_plan_cannot_reuse_journal(self):
        other = copy.deepcopy(self.plan)
        other["entries"][1]["sha256"] = "b" * 64
        with self.assertRaisesRegex(ValueError, "INVALID_CREATE_JOURNAL"):
            guard.create_preflight(other, self.inventory, self.journal, "01_Dados",
                                   allow_fixture=True)

    def test_changed_root_inventory_is_rejected(self):
        inv = copy.deepcopy(self.inventory)
        inv["drive_root_id"] = "synthetic-other-root"
        with self.assertRaisesRegex(ValueError, "INVENTORY_ROOT"):
            self.begin(inv)

    def test_locked_begin_persists_journal_before_host_call(self):
        # For the on-disk interface the fixture must be explicitly identified as
        # a fictional live-shaped host result; this tests storage, not Drive.
        inv = self.live()
        init = guard.locked_update(self.plan, inv, self.journal_path, "01_Dados",
                                   "initialize", initialize_authorized=True)
        self.assertEqual(init["action"], "JOURNAL_INITIALIZED_NEW_PROJECT")
        step = guard.locked_update(self.plan, inv, self.journal_path, "01_Dados", "prepare")
        self.assertEqual(step["action"], "CREATE_FOLDER_ONCE")
        self.assertTrue(step["durable_readback_required"])
        self.assertEqual(step["journal_sha256"],
                         hashlib.sha256(self.journal_path.read_bytes()).hexdigest())
        data = guard.read_journal(self.plan, self.journal_path)
        self.assertEqual(data["operations"]["01_Dados"]["state"], "OUTCOME_UNKNOWN")
        self.assertFalse(self.journal_path.with_name("attempts.json.lock").exists())
        retry = guard.locked_update(self.plan, inv, self.journal_path, "01_Dados", "prepare")
        self.assertEqual(retry["action"], "REINSPECT_NO_RETRY")


    def test_missing_journal_is_not_silently_recreated_after_interruption(self):
        inv = self.live()
        with self.assertRaisesRegex(ValueError, "JOURNAL_MISSING_RECOVERY_REQUIRED"):
            guard.locked_update(self.plan, inv, self.journal_path, "01_Dados", "prepare")
        self.assertFalse(self.journal_path.exists())

    def test_initialize_requires_explicit_attestation(self):
        inv = self.live()
        with self.assertRaisesRegex(ValueError, "NEW_PROJECT_ATTESTATION_REQUIRED"):
            guard.locked_update(self.plan, inv, self.journal_path, "01_Dados", "initialize")
        self.assertFalse(self.journal_path.exists())

    def test_initialize_twice_does_not_erase_prior_operations(self):
        inv = self.live()
        guard.locked_update(self.plan, inv, self.journal_path, "01_Dados",
                            "initialize", initialize_authorized=True)
        guard.locked_update(self.plan, inv, self.journal_path, "01_Dados", "prepare")
        before = self.journal_path.read_bytes()
        with self.assertRaisesRegex(ValueError, "JOURNAL_ALREADY_EXISTS"):
            guard.locked_update(self.plan, inv, self.journal_path, "01_Dados",
                                "initialize", initialize_authorized=True)
        self.assertEqual(before, self.journal_path.read_bytes())

    def test_live_scan_requires_real_page_evidence_contract(self):
        inv = copy.deepcopy(self.inventory)
        inv["observed_via"] = "LIVE_DRIVE"
        with self.assertRaisesRegex(ValueError, "PARENT_PAGE_EVIDENCE_REQUIRED"):
            guard.direct_scan(self.plan, inv, ROOT)

    def test_live_scan_rejects_nonterminating_page_chain(self):
        inv = self.live()
        inv["parent_scans"][0]["page_evidence"][0]["next_page_token"] = "more-pages"
        with self.assertRaisesRegex(ValueError, "PARENT_PAGINATION_INCOMPLETE"):
            guard.direct_scan(self.plan, inv, ROOT)


    def test_lost_journal_restored_from_durable_copy_blocks_retry(self):
        inv = self.live()
        guard.locked_update(self.plan, inv, self.journal_path, "01_Dados",
                            "initialize", initialize_authorized=True)
        first = guard.locked_update(self.plan, inv, self.journal_path, "01_Dados", "prepare")
        durable_copy = self.journal_path.read_bytes()
        self.journal_path.unlink()
        with self.assertRaisesRegex(ValueError, "JOURNAL_MISSING_RECOVERY_REQUIRED"):
            guard.locked_update(self.plan, inv, self.journal_path, "01_Dados", "prepare")
        self.journal_path.write_bytes(durable_copy)
        resumed = guard.locked_update(self.plan, inv, self.journal_path, "01_Dados", "prepare")
        self.assertEqual(first["action"], "CREATE_FOLDER_ONCE")
        self.assertEqual(resumed["action"], "REINSPECT_NO_RETRY")
        self.assertEqual(guard.read_journal(self.plan, self.journal_path)["operations"]
                         ["01_Dados"]["state"], "OUTCOME_UNKNOWN")

    def test_live_scan_rejects_replayed_pagination_cursor(self):
        inv = self.live(self.fresh())
        inv["parent_scans"][0]["page_evidence"] = [
            {"source": "GOOGLE_DRIVE_FILES_LIST", "request_page_token": None,
             "next_page_token": "repeat-token", "item_ids": []},
            {"source": "GOOGLE_DRIVE_FILES_LIST", "request_page_token": "repeat-token",
             "next_page_token": "repeat-token", "item_ids": [CHILD]},
            {"source": "GOOGLE_DRIVE_FILES_LIST", "request_page_token": "repeat-token",
             "next_page_token": None, "item_ids": []},
        ]
        with self.assertRaisesRegex(ValueError, "PARENT_PAGINATION_CURSOR_REPLAY"):
            guard.direct_scan(self.plan, inv, ROOT)

    def test_live_scan_rejects_inconsistent_cursor(self):
        inv = self.live()
        inv["parent_scans"][0]["page_evidence"][0]["request_page_token"] = "injected"
        with self.assertRaisesRegex(ValueError, "PARENT_PAGINATION_CHAIN_INVALID"):
            guard.direct_scan(self.plan, inv, ROOT)

    def test_live_scan_rejects_missing_child_from_page_receipts(self):
        inv = self.live(self.fresh())
        inv["parent_scans"][0]["page_evidence"][0]["item_ids"] = []
        with self.assertRaisesRegex(ValueError, "PARENT_PAGINATION_CONTENT_MISMATCH"):
            guard.direct_scan(self.plan, inv, ROOT)

    def test_live_scan_rejects_duplicate_ids_across_pages(self):
        inv = self.live(self.fresh())
        inv["parent_scans"][0]["page_evidence"] = [
            {"source": "GOOGLE_DRIVE_FILES_LIST", "request_page_token": None,
             "next_page_token": "continuation", "item_ids": [CHILD]},
            {"source": "GOOGLE_DRIVE_FILES_LIST", "request_page_token": "continuation",
             "next_page_token": None, "item_ids": [CHILD]}
        ]
        with self.assertRaisesRegex(ValueError, "PARENT_PAGINATION_DUPLICATE_ID"):
            guard.direct_scan(self.plan, inv, ROOT)

    def test_live_scan_accepts_consistent_paginated_fixture(self):
        inv = self.live(self.fresh(count=2))
        ids = [c["id"] for c in inv["parent_scans"][0]["children"]]
        inv["parent_scans"][0]["page_evidence"] = [
            {"source": "GOOGLE_DRIVE_FILES_LIST", "request_page_token": None,
             "next_page_token": "page-2", "item_ids": [ids[0]]},
            {"source": "GOOGLE_DRIVE_FILES_LIST", "request_page_token": "page-2",
             "next_page_token": None, "item_ids": [ids[1]]}
        ]
        scan = guard.direct_scan(self.plan, inv, ROOT)
        self.assertEqual(len(scan["children"]), 2)

    def test_lock_owned_by_another_agent_is_not_removed(self):
        self.journal_path.parent.mkdir(parents=True)
        lock = self.journal_path.with_name("attempts.json.lock")
        lock.write_text("Other synthetic worker")
        inv = self.live()
        with self.assertRaises(FileExistsError):
            guard.locked_update(self.plan, inv, self.journal_path, "01_Dados", "prepare")
        self.assertEqual(lock.read_text(), "Other synthetic worker")

    def test_corrupt_journal_rejected(self):
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        self.journal_path.write_text("{}")
        with self.assertRaisesRegex(ValueError, "JOURNAL_PLAN_OR_ROOT_MISMATCH"):
            guard.read_journal(self.plan, self.journal_path)

    def test_cannot_target_file_as_folder(self):
        with self.assertRaisesRegex(ValueError, "FOLDER_NOT_IN_PLAN"):
            guard.create_preflight(self.plan, self.inventory, self.journal,
                                   "01_Dados/test.csv", allow_fixture=True)

    def test_no_scientific_records_written(self):
        gates = self.temp / "18_Human_Validation_Gates.csv"
        gates.write_text("GATE-0001,PENDING")
        self.begin()
        self.assertEqual(gates.read_text(), "GATE-0001,PENDING")


if __name__ == "__main__":
    unittest.main()
