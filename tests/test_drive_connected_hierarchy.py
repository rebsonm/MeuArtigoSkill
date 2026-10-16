"""Synthetic-only tests for the read-only connected Drive hierarchy."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from drive_connected_hierarchy import inspect, SCHEMA
from drive_f6_connected_search import FOLDER_MIME

ROOT="my-root-id-00000001"
CONTAINER="my-article-dir-00001"
PROJECT="my-paper-id-00000001"
NAME="ARTIGO_Example_2026"

def folder(fid,name,parent):
    return {"id":fid,"title":name,"mime_type":FOLDER_MIME,"parent_ids":[parent]}
def page(parent,rows,cursor=None,nxt=None):
    return {"request":{"parent_id":parent,"item_type":"folder",
                       "special_filter_query_str":f"'{parent}' in parents and trashed = false",
                       "page_token":cursor, "query":""},
            "response":{"results":rows,"next_page_token":nxt}}
def fixture():
    c=folder(CONTAINER,"Meu Artigo",ROOT)
    p=folder(PROJECT,NAME,CONTAINER)
    return {"schema":SCHEMA,"root_requested_alias":"root",
       "root_metadata":{"id":ROOT,"title":"Meu Drive","mime_type":FOLDER_MIME,"parent_ids":None},
       "container_pages":{"schema":"MEU_ARTIGO_DRIVE_CONNECTED_FOLDER_SEARCH_V1",
                          "parent_id":ROOT,"pages":[page(ROOT,[c])]},
       "container_metadata":copy.deepcopy(c),"project_name":NAME,
       "project_pages":{"schema":"MEU_ARTIGO_DRIVE_CONNECTED_FOLDER_SEARCH_V1",
                        "parent_id":CONTAINER,"pages":[page(CONTAINER,[p])]},
       "project_metadata":copy.deepcopy(p)}

class DriveHierarchyReceiptTests(unittest.TestCase):
    def setUp(self):self.data=fixture()
    def test_confirmed_existing_project_is_read_only(self):
        o=inspect(self.data)
        self.assertEqual(o["action"],"CONNECTED_CANONICAL_PROJECT_RECONCILED")
        for k in ("create_permitted","canonical_write_authorized",
                  "scientific_gate_approved","provider_proof_independently_authenticated",
                  "all_mime_parent_scan_verified"):
            self.assertIs(o[k],False)
    def test_wrong_root_alias_denied(self):
        self.data["root_requested_alias"]="some-folder"
        with self.assertRaisesRegex(ValueError,"ROOT_ALIAS"):inspect(self.data)
    def test_root_has_no_parent(self):
        self.data["root_metadata"]["parent_ids"]=[CONTAINER]
        with self.assertRaisesRegex(ValueError,"PARENT_MISMATCH"):inspect(self.data)
    def test_shared_drive_is_not_my_drive(self):
        self.data["root_metadata"]["drive_id"]="shared-drive-000001"
        with self.assertRaisesRegex(ValueError,"SHARED_DRIVE"):inspect(self.data)
    def test_duplicate_container_blocks(self):
        self.data["container_pages"]["pages"][0]["response"]["results"].append(
            folder("another-container-id1","Meu Artigo",ROOT))
        self.assertEqual(inspect(self.data)["action"],"BLOCKED_DUPLICATE_EXISTING_FOLDERS")
    def test_container_parent_drift_denied(self):
        self.data["container_metadata"]["parent_ids"]=[PROJECT]
        with self.assertRaisesRegex(ValueError,"PARENT_MISMATCH"):inspect(self.data)
    def test_project_missing_metadata_needs_read(self):
        self.data["project_metadata"]=None
        self.assertEqual(inspect(self.data)["action"],"CHECK_EXACT_PROJECT_METADATA")
    def test_project_missing_in_folder_scan_never_create(self):
        self.data["project_pages"]["pages"][0]["response"]["results"]=[]
        v=inspect(self.data)
        self.assertEqual(v["action"],"BLOCKED_ABSENT_IN_FOLDER_ONLY_SCAN")
        self.assertIs(v["create_permitted"],False)
    def test_duplicate_project_blocks(self):
        self.data["project_pages"]["pages"][0]["response"]["results"].append(
            folder("another-paper-id-00001",NAME,CONTAINER))
        self.assertEqual(inspect(self.data)["action"],"BLOCKED_DUPLICATE_EXISTING_FOLDERS")
    def test_two_pages_prove_existing_folder(self):
        pages=self.data["project_pages"]
        pages["pages"]=[page(CONTAINER,[],nxt="p2"),
                        page(CONTAINER,[folder(PROJECT,NAME,CONTAINER)],cursor="p2")]
        self.assertEqual(inspect(self.data)["action"],"CONNECTED_CANONICAL_PROJECT_RECONCILED")
    def test_cursor_replay_denied(self):
        pages=self.data["project_pages"]
        pages["pages"]=[page(CONTAINER,[],nxt="p2"),
                        page(CONTAINER,[],cursor="p2",nxt="p2")]
        with self.assertRaisesRegex(ValueError,"CURSOR_REPLAY"):inspect(self.data)
    def test_missing_terminal_pagination_field_denied(self):
        del self.data["project_pages"]["pages"][0]["response"]["next_page_token"]
        with self.assertRaisesRegex(ValueError,"INCOMPLETE"):inspect(self.data)
    def test_filter_cannot_hide_children(self):
        self.data["project_pages"]["pages"][0]["request"]["query"]="some keyword"
        with self.assertRaisesRegex(ValueError,"HIDDEN_FILTERS"):inspect(self.data)
    def test_project_wrong_id_denied(self):
        self.data["project_metadata"]["id"]="wrong-project-id-00001"
        with self.assertRaisesRegex(ValueError,"CANDIDATE_ID"):inspect(self.data)
    def test_project_wrong_type_denied(self):
        self.data["project_metadata"]["mime_type"]="text/plain"
        with self.assertRaisesRegex(ValueError,"NAME_OR_TYPE"):inspect(self.data)
    def test_project_name_contract_denied(self):
        self.data["project_name"]="unscoped_folder"
        with self.assertRaisesRegex(ValueError,"PROJECT_NAME_INVALID"):inspect(self.data)
    def test_metadata_only_cannot_claim_all_mime_scan(self):
        self.assertIs(inspect(self.data)["all_mime_parent_scan_verified"],False)
    def test_project_parent_page_wrong_denied(self):
        self.data["project_pages"]["parent_id"]=ROOT
        with self.assertRaisesRegex(ValueError,"SCOPE_OR_CURSOR_MISMATCH"):inspect(self.data)

if __name__ == "__main__":
    unittest.main()
