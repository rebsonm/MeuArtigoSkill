"""F6 connected-Drive folder-only search receipt validation, entirely synthetic."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import drive_f6_connected_search as bridge

PARENT = "synthetic-folder-parent-0001"
FIRST = "synthetic-folder-id-00001"
SECOND = "synthetic-folder-id-00002"
QUERY = "'" + PARENT + "' in parents and trashed = false"


def child(name="01_Dados", rid=FIRST):
    return {"id": rid, "title": name,
            "mime_type": "application/vnd.google-apps.folder",
            "parent_ids": [PARENT]}


def entry(items, *, requested=None, next_page=None):
    return {
        "request": {
            "parent_id": PARENT, "item_type": "folder",
            "special_filter_query_str": QUERY, "page_token": requested,
        },
        "response": {"results": items, "next_page_token": next_page},
    }


def document(pages):
    return {"schema": bridge.SCHEMA, "parent_id": PARENT, "pages": pages}


class ConnectedFolderSearchTests(unittest.TestCase):
    def test_one_real_shaped_folder_is_only_a_candidate(self):
        result = bridge.verify_folder_pages(document([entry([child()])]), "01_Dados")
        self.assertEqual(result["action"],
                         "EXISTING_FOLDER_CANDIDATE_METADATA_READ_REQUIRED")
        self.assertFalse(result["create_permitted"])
        self.assertEqual(result["remote_id"], FIRST)

    def test_empty_complete_folder_scan_does_not_authorize_creation(self):
        result = bridge.verify_folder_pages(document([entry([])]), "01_Dados")
        self.assertEqual(result["action"], "BLOCKED_ABSENT_IN_FOLDER_ONLY_SCAN")
        self.assertFalse(result["create_permitted"])

    def test_exact_two_page_cursor_chain_is_accepted_for_existing_folder(self):
        pages = [entry([], next_page="opaque-page-two"),
                 entry([child()], requested="opaque-page-two")]
        result = bridge.verify_folder_pages(document(pages), "01_Dados")
        self.assertEqual(result["remote_id"], FIRST)
        self.assertFalse(result["create_permitted"])

    def test_nonterminal_page_cannot_claim_complete(self):
        with self.assertRaisesRegex(ValueError,
                                    "CONNECTED_FOLDER_PAGINATION_NOT_EXHAUSTED"):
            bridge.verify_folder_pages(document([entry([], next_page="more")]),
                                       "01_Dados")

    def test_missing_terminal_receipt_field_fails_closed(self):
        doc = document([entry([child()])])
        del doc["pages"][0]["response"]["next_page_token"]
        with self.assertRaisesRegex(ValueError,
                                    "CONNECTED_FOLDER_RESPONSE_INCOMPLETE"):
            bridge.verify_folder_pages(doc, "01_Dados")

    def test_type_conflict_not_hidden_as_folder(self):
        doc = document([entry([child()])])
        doc["pages"][0]["response"]["results"][0]["mime_type"] = "text/plain"
        with self.assertRaisesRegex(ValueError,
                                    "CONNECTED_FOLDER_ID_OR_PARENT_CONFLICT"):
            bridge.verify_folder_pages(doc, "01_Dados")

    def test_wrong_parent_id_is_never_reused(self):
        doc = document([entry([child()])])
        doc["pages"][0]["response"]["results"][0]["parent_ids"] = ["some-other-parent-00001"]
        with self.assertRaisesRegex(ValueError,
                                    "CONNECTED_FOLDER_ID_OR_PARENT_CONFLICT"):
            bridge.verify_folder_pages(doc, "01_Dados")

    def test_duplicate_folder_names_block_reuse(self):
        doc = document([entry([child(), child(rid=SECOND)])])
        result = bridge.verify_folder_pages(doc, "01_Dados")
        self.assertEqual(result["action"], "BLOCKED_DUPLICATE_EXISTING_FOLDERS")
        self.assertFalse(result["create_permitted"])

    def test_duplicate_id_on_separate_pages_blocks(self):
        doc = document([entry([child()], next_page="second"),
                        entry([child()], requested="second")])
        with self.assertRaisesRegex(ValueError,
                                    "CONNECTED_FOLDER_ID_OR_PARENT_CONFLICT"):
            bridge.verify_folder_pages(doc, "01_Dados")

    def test_injected_filter_query_is_rejected(self):
        doc = document([entry([child()])])
        doc["pages"][0]["request"]["special_filter_query_str"] = "trashed = false"
        with self.assertRaisesRegex(ValueError,
                                    "CONNECTED_FOLDER_PARENT_QUERY_MISMATCH"):
            bridge.verify_folder_pages(doc, "01_Dados")

    def test_keyword_filter_cannot_hide_other_direct_children(self):
        doc = document([entry([child()])])
        doc["pages"][0]["request"]["query"] = "01_Dados"
        with self.assertRaisesRegex(ValueError,
                                    "CONNECTED_FOLDER_HIDDEN_FILTERS_FORBIDDEN"):
            bridge.verify_folder_pages(doc, "01_Dados")

    def test_viewed_only_filter_cannot_hide_unseen_folders(self):
        doc = document([entry([child()])])
        doc["pages"][0]["request"]["require_viewed_by_user"] = True
        with self.assertRaisesRegex(ValueError,
                                    "CONNECTED_FOLDER_HIDDEN_FILTERS_FORBIDDEN"):
            bridge.verify_folder_pages(doc, "01_Dados")

    def test_content_fetch_option_rejected_in_metadata_only_scan(self):
        doc = document([entry([child()])])
        doc["pages"][0]["request"]["best_effort_fetch"] = True
        with self.assertRaisesRegex(ValueError,
                                    "CONNECTED_FOLDER_CONTENT_FETCH_UNNECESSARY"):
            bridge.verify_folder_pages(doc, "01_Dados")

    def test_unscoped_folder_search_is_rejected(self):
        doc = document([entry([child()])])
        doc["pages"][0]["request"]["parent_id"] = "untrusted-parent-0001"
        with self.assertRaisesRegex(ValueError,
                                    "CONNECTED_FOLDER_PAGE_SCOPE_OR_CURSOR_MISMATCH"):
            bridge.verify_folder_pages(doc, "01_Dados")

    def test_wrong_cursor_is_rejected(self):
        doc = document([entry([], next_page="next"),
                        entry([child()], requested="other")])
        with self.assertRaisesRegex(ValueError,
                                    "CONNECTED_FOLDER_PAGE_SCOPE_OR_CURSOR_MISMATCH"):
            bridge.verify_folder_pages(doc, "01_Dados")

    def test_cursor_replay_is_rejected(self):
        doc = document([entry([], next_page="same"),
                        entry([], requested="same", next_page="same"),
                        entry([child()], requested="same")])
        with self.assertRaisesRegex(ValueError,
                                    "CONNECTED_FOLDER_CURSOR_REPLAY"):
            bridge.verify_folder_pages(doc, "01_Dados")

    def test_missing_page_results_are_rejected(self):
        doc = document([entry([])])
        del doc["pages"][0]["response"]["results"]
        with self.assertRaisesRegex(ValueError,
                                    "CONNECTED_FOLDER_RESPONSE_INCOMPLETE"):
            bridge.verify_folder_pages(doc, "01_Dados")

    def test_all_verdicts_refuse_create_even_when_folder_missing(self):
        for pages in ([entry([])],
                      [entry([child()])],
                      [entry([child(), child(rid=SECOND)])]):
            result = bridge.verify_folder_pages(document(pages), "01_Dados")
            self.assertIs(result["create_permitted"], False)


if __name__ == "__main__":
    unittest.main()
