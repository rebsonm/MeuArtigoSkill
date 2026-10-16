"""Provider-shaped preflight tests, real code and simulated GET-only Drive."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import drive_root_live_preflight as live
import drive_root_anchor as anchor

ROOT = "my-drive-root-0000001"
CONTAINER = "meu-artigo-parent-001"
PROJECT = "research-project-id-001"
NAME = "ARTIGO_Exemplo_2026"
MIME = "application/vnd.google-apps.folder"


class FakeProvider:
    def __init__(self):
        self.root_folders = [{"id": CONTAINER, "name": "Meu Artigo",
                              "mimeType": MIME, "parents": [ROOT]}]
        self.globally_matching_projects = []
        self.children = [{"id": PROJECT, "name": NAME,
                          "mimeType": MIME, "parents": [CONTAINER]}]
        self.folders = {
            "root": {"id": ROOT, "mimeType": MIME, "trashed": False},
            CONTAINER: {"id": CONTAINER, "name": "Meu Artigo",
                        "mimeType": MIME, "parents": [ROOT], "trashed": False},
            PROJECT: {"id": PROJECT, "name": NAME, "mimeType": MIME,
                      "parents": [CONTAINER], "trashed": False},
        }
        self.calls = []

    def sender(self, token, url, *, method="GET", body=None):
        self.calls.append((method, url))
        if token != "mock-provider-token-synthetic" or method != "GET" or body is not None:
            raise AssertionError("read-only preflight made a write or wrong token")
        fid = unquote(url.split("/files/", 1)[1].split("?", 1)[0])
        return json.dumps(self.folders[fid]).encode()

    def fetch_page(self, token, params):
        self.calls.append(("files.list", dict(params)))
        if token != "mock-provider-token-synthetic":
            raise AssertionError("wrong token")
        parent = params["q"].split("'", 2)[1]
        if params.get("pageToken"):
            raise AssertionError("unexpected pagination")
        if params["q"].startswith("name = "):
            children = list(self.globally_matching_projects)
        elif parent == ROOT:
            children = self.root_folders
        elif parent == CONTAINER:
            children = self.children
        else:
            raise AssertionError("out of allowed scope")
        return {"kind": "drive#fileList", "files": children,
                "incompleteSearch": False}

    def run(self, name=NAME):
        return live.current_structure(
            "mock-provider-token-synthetic", project_name=name,
            sender=self.sender, fetch_page=self.fetch_page)


class LiveReadOnlyPreflightTests(unittest.TestCase):
    def setUp(self):
        self.provider = FakeProvider()

    def test_existing_root_and_project_reused_without_writes(self):
        result = self.provider.run()
        self.assertEqual(result["action"], "CANONICAL_PROJECT_VERIFIED")
        self.assertEqual(result["container_id"], CONTAINER)
        self.assertEqual(result["project_id"], PROJECT)
        self.assertFalse(result["create_permitted"])
        self.assertTrue(all(method in ("GET", "files.list")
                            for method, _ in self.provider.calls))

    def test_absent_container_requests_only_guarded_create_under_my_drive(self):
        self.provider.root_folders = []
        result = self.provider.run()
        self.assertEqual(result["action"], "CHECK_PARENT_FOR_GUARDED_CREATE")
        self.assertEqual(result["parent_id"], ROOT)
        self.assertEqual(result["folder_name"], "Meu Artigo")
        self.assertFalse(result["create_permitted"])
        self.assertNotIn(CONTAINER, [x[1] for x in self.provider.calls])

    def test_absent_article_requested_only_under_verified_container(self):
        self.provider.children = []
        result = self.provider.run()
        self.assertEqual(result["action"], "CHECK_PARENT_FOR_GUARDED_CREATE")
        self.assertEqual(result["parent_id"], CONTAINER)
        self.assertEqual(result["folder_name"], NAME)

    def test_existing_mislocated_project_prevents_duplicate_creation(self):
        self.provider.children = []
        self.provider.globally_matching_projects = [{
            "id": "other-location-project-0001", "name": NAME,
            "mimeType": MIME, "parents": ["some-other-parent-0001"],
            "trashed": False}]
        result = self.provider.run()
        self.assertEqual(result["action"], "BLOCKED_EXISTING_PROJECT_OUTSIDE_CONTAINER")
        self.assertEqual(result["observed_matching_folders"], 1)
        self.assertFalse(result["create_permitted"])

    def test_inconsistent_global_and_direct_parent_scans_block(self):
        self.provider.children = []
        self.provider.globally_matching_projects = [{
            "id": PROJECT, "name": NAME, "mimeType": MIME,
            "parents": [CONTAINER], "trashed": False}]
        result = self.provider.run()
        self.assertEqual(result["action"], "BLOCKED_PARENT_SCAN_GLOBAL_CONFLICT")
        self.assertFalse(result["create_permitted"])

    def test_global_search_incomplete_blocks_instead_of_authorizing_create(self):
        self.provider.children = []
        initial_fetch = self.provider.fetch_page
        def fetch(token, params):
            result = initial_fetch(token, params)
            if params["q"].startswith("name = "):
                result["incompleteSearch"] = True
            return result
        with self.assertRaisesRegex(anchor.RootAnchorError,
                                    "PROJECT_GLOBAL_SEARCH_INCOMPLETE"):
            live.current_structure(
                "mock-provider-token-synthetic", project_name=NAME,
                sender=self.provider.sender, fetch_page=fetch)

    def test_duplicate_my_drive_container_is_blocking(self):
        self.provider.root_folders.append({
            "id": "other-meu-artigo-id-001", "name": "Meu Artigo",
            "mimeType": MIME, "parents": [ROOT]})
        result = self.provider.run()
        self.assertEqual(result["action"], "BLOCKED_DUPLICATE_SAME_NAME")

    def test_provider_parent_drift_blocks_existing_folder_reuse(self):
        self.provider.folders[CONTAINER]["parents"] = ["unrelated-parent-00001"]
        with self.assertRaisesRegex(anchor.RootAnchorError,
                                    "CANONICAL_FOLDER_PARENT_IDENTITY_MISMATCH"):
            self.provider.run()

    def test_root_provider_must_be_real_root_metadata(self):
        self.provider.folders["root"]["parents"] = ["random-parent-id-00001"]
        with self.assertRaisesRegex(anchor.RootAnchorError,
                                    "MY_DRIVE_ROOT_IDENTITY_INVALID"):
            self.provider.run()

    def test_read_only_lookup_does_not_authenticate_for_create(self):
        result = self.provider.run()
        self.assertNotIn("CREATE_FOLDER_ONCE", json.dumps(result))
        self.assertNotIn("POST", [x[0] for x in self.provider.calls])

    def test_traversal_project_name_blocked_before_provider(self):
        with self.assertRaisesRegex(ValueError, "INVALID_RELATIVE_PATH"):
            self.provider.run("../wrong/folder")
        self.assertEqual(self.provider.calls, [])


if __name__ == "__main__":
    unittest.main()
