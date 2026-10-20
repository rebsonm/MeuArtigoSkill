"""Offline contract tests for optional authenticated Drive pagination scanner."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import drive_api_proof as proof
import drive_create_guard as guard

ROOT = "synthetic-root-00001"
FOLDER_ID = "synthetic-folder-0001"
FILE_ID = "synthetic-file-00001"


def child(name, id_, kind="application/vnd.google-apps.folder"):
    return {"id": id_, "name": name, "mimeType": kind, "parents": [ROOT]}


def page(items, next_cursor=None):
    result = {"kind": "drive#fileList", "files": items}
    if next_cursor is not None:
        result["nextPageToken"] = next_cursor
    return result


class AuthenticatedPaginationProofTests(unittest.TestCase):
    def mock_pages(self, responses):
        iterator = iter(responses)
        calls = []

        def fetch(token, params):
            self.assertEqual(token, "dummy-token")
            calls.append(copy.deepcopy(params))
            return next(iterator)
        return fetch, calls

    def test_paginated_complete_listing_feeds_existing_guard(self):
        api, calls = self.mock_pages([
            page([child("01_Dados", FOLDER_ID)], "cursor-2"),
            page([child("unrelated.txt", FILE_ID, "text/plain")]),
        ])
        scan = proof.complete_parent_scan(ROOT, "dummy-token", fetch_page=api)
        self.assertEqual(len(calls), 2)
        self.assertNotIn("pageToken", calls[0])
        self.assertEqual(calls[1]["pageToken"], "cursor-2")
        self.assertEqual(scan["page_evidence"][0]["next_page_token"], "cursor-2")
        self.assertEqual(scan["page_evidence"][-1]["next_page_token"], None)
        inv = proof.merge_parent_scan(ROOT, "", scan)
        plan = {"kind": "MEU_ARTIGO_DRIVE_DELIVERY_PLAN", "schema": 1,
                "drive_root_id": ROOT, "project_folder": "SYNTHETIC",
                "entries": [{"type": "folder", "path": "01_Dados", "parent": ""}]}
        inspected = guard.direct_scan(plan, inv, ROOT)
        self.assertEqual(len(inspected["children"]), 2)
        outcome = guard.inspect_target(plan, inv, "01_Dados", ROOT)
        self.assertEqual(outcome["action"], "REUSE_EXISTING")
        self.assertEqual(outcome["id"], FOLDER_ID)

    def test_empty_page_with_cursor_is_not_terminal(self):
        api, calls = self.mock_pages([page([], "cursor-2"), page([])])
        scan = proof.complete_parent_scan(ROOT, "dummy-token", fetch_page=api)
        self.assertEqual(len(calls), 2)
        self.assertEqual(scan["children"], [])

    def test_missing_files_field_blocks(self):
        api, _ = self.mock_pages([{"kind": "drive#fileList"}])
        with self.assertRaisesRegex(proof.DriveEvidenceError, "DRIVE_LIST_MISSING_ITEMS"):
            proof.complete_parent_scan(ROOT, "dummy-token", fetch_page=api)

    def test_incomplete_search_blocks(self):
        obj = page([])
        obj["incompleteSearch"] = True
        api, _ = self.mock_pages([obj])
        with self.assertRaisesRegex(proof.DriveEvidenceError, "DRIVE_LIST_INCOMPLETE_SEARCH"):
            proof.complete_parent_scan(ROOT, "dummy-token", fetch_page=api)

    def test_page_limit_blocks_even_if_many_pages_exist(self):
        api, _ = self.mock_pages([page([], "cursor-2")])
        with self.assertRaisesRegex(proof.DriveEvidenceError, "DRIVE_LIST_PAGE_LIMIT_REACHED"):
            proof.complete_parent_scan(ROOT, "dummy-token", fetch_page=api, max_pages=1)

    def test_duplicate_id_across_pages_blocks(self):
        api, _ = self.mock_pages([
            page([child("01_Dados", FOLDER_ID)], "cursor-2"),
            page([child("same", FOLDER_ID)]),
        ])
        with self.assertRaisesRegex(proof.DriveEvidenceError, "DRIVE_LIST_INVALID_CHILD_OR_PARENT"):
            proof.complete_parent_scan(ROOT, "dummy-token", fetch_page=api)

    def test_cursor_replay_blocks(self):
        api, _ = self.mock_pages([
            page([], "cursor-2"), page([], "cursor-2")
        ])
        with self.assertRaisesRegex(proof.DriveEvidenceError, "DRIVE_LIST_CURSOR_REPLAY"):
            proof.complete_parent_scan(ROOT, "dummy-token", fetch_page=api)

    def test_unrelated_parent_is_rejected(self):
        bad = child("01_Dados", FOLDER_ID)
        bad["parents"] = ["synthetic-other-parent"]
        api, _ = self.mock_pages([page([bad])])
        with self.assertRaisesRegex(proof.DriveEvidenceError, "DRIVE_LIST_INVALID_CHILD_OR_PARENT"):
            proof.complete_parent_scan(ROOT, "dummy-token", fetch_page=api)

    def test_duplicate_child_names_block_inventory(self):
        api, _ = self.mock_pages([page([
            child("01_Dados", FOLDER_ID), child("01_Dados", FILE_ID),
        ])])
        scan = proof.complete_parent_scan(ROOT, "dummy-token", fetch_page=api)
        with self.assertRaisesRegex(proof.DriveEvidenceError, "DRIVE_LIST_DUPLICATE_CHILD_NAMES"):
            proof.merge_parent_scan(ROOT, "", scan)

    def test_nested_parent_requires_identity_binding(self):
        api, _ = self.mock_pages([page([])])
        scan = proof.complete_parent_scan(ROOT, "dummy-token", fetch_page=api)
        with self.assertRaisesRegex(proof.DriveEvidenceError, "PARENT_PATH_REQUIRES"):
            proof.merge_parent_scan("synthetic-drive-root", "01_Dados", scan)

    def test_nested_parent_correctly_merges_verified_binding(self):
        nested = "synthetic-nested-0001"
        api, _ = self.mock_pages([page([])])
        scan = proof.complete_parent_scan(nested, "dummy-token", fetch_page=api)
        base = {"schema": 1, "drive_root_id": ROOT, "observed_via": "LIVE_DRIVE",
                "entries": [{"path": "01_Dados", "id": nested, "parent_id": ROOT,
                             "type": "folder"}], "parent_scans": []}
        inv = proof.merge_parent_scan(ROOT, "01_Dados", scan, base)
        self.assertEqual(inv["entries"], base["entries"])

    def test_new_observation_token_changes_even_if_listing_same(self):
        obj = page([])
        api1, _ = self.mock_pages([obj])
        api2, _ = self.mock_pages([obj])
        first = proof.complete_parent_scan(ROOT, "dummy-token", fetch_page=api1)
        later = proof.complete_parent_scan(ROOT, "dummy-token", fetch_page=api2)
        self.assertNotEqual(first["scan_token"], later["scan_token"])

    def test_authenticator_never_accepts_tiny_token(self):
        with self.assertRaisesRegex(proof.DriveEvidenceError, "DRIVE_TOKEN_MISSING"):
            proof.authenticated_get("tiny", {"q": "anything"})

    def test_new_guard_does_not_approve_scientific_gates(self):
        api, _ = self.mock_pages([page([])])
        scan = proof.complete_parent_scan(ROOT, "dummy-token", fetch_page=api)
        inv = proof.merge_parent_scan(ROOT, "", scan)
        self.assertNotIn("gates", inv)


if __name__ == "__main__":
    unittest.main()
