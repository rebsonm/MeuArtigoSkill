"""Guarded canonical My Drive folder parent proof — synthetic, no writes."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import drive_root_anchor as anchor

ROOT = "my-drive-root-0000001"
CONTAINER_ID = "meu-artigo-parent-001"
PROJECT_ID = "research-project-id-001"
WRONG_PARENT = "other-project-parent-001"
P_NAME = "ARTIGO_Exemplo_2026"
FOLDER = "application/vnd.google-apps.folder"


def metadata(fid, name, parent):
    return {"id": fid, "name": name, "mimeType": FOLDER,
            "parents": [parent], "trashed": False}


def scan(parent, children, *, pages=None):
    return {
        "parent_id": parent, "complete": True,
        "scan_token": "provider-scanned-only",
        "children": copy.deepcopy(children),
        "page_evidence": pages or [{
            "source": "GOOGLE_DRIVE_FILES_LIST", "request_page_token": None,
            "next_page_token": None,
            "item_ids": [c["id"] for c in children]
        }]
    }


def item(id, name, kind="folder"):
    return {"id": id, "name": name, "type": kind}


def root():
    return {"id": ROOT, "mimeType": FOLDER, "trashed": False}


class RootFolderGuardTests(unittest.TestCase):
    def setUp(self):
        self.root_scan = scan(ROOT, [item(CONTAINER_ID, "Meu Artigo")])
        self.meta = metadata(CONTAINER_ID, "Meu Artigo", ROOT)
        self.child_scan = scan(CONTAINER_ID, [item(PROJECT_ID, P_NAME)])
        self.project_meta = metadata(PROJECT_ID, P_NAME, CONTAINER_ID)
        self.plan = {
            "schema": 1, "kind": "MEU_ARTIGO_DRIVE_DELIVERY_PLAN",
            "drive_root_id": PROJECT_ID,
            "project_folder": P_NAME,
            "entries": [{"path": "00_Gestao_e_Continuidade",
                         "type": "folder", "parent": ""}],
        }

    def resolved(self):
        return anchor.resolve_hierarchy(root(), self.root_scan,
            container_metadata=self.meta, project_name=P_NAME,
            container_scan=self.child_scan, project_metadata=self.project_meta)

    def test_existing_exact_root_container_is_reused(self):
        result = anchor.resolve_hierarchy(root(), self.root_scan,
                                           container_metadata=self.meta)
        self.assertEqual(result["action"], "CANONICAL_CONTAINER_VERIFIED")
        self.assertEqual(result["container_id"], CONTAINER_ID)
        self.assertFalse(result["create_permitted"])

    def test_missing_container_requests_guarded_create_only_under_my_drive(self):
        result = anchor.resolve_hierarchy(root(), scan(ROOT, []))
        self.assertEqual(result["action"], "CHECK_PARENT_FOR_GUARDED_CREATE")
        self.assertEqual(result["folder_name"], "Meu Artigo")
        self.assertEqual(result["parent_id"], ROOT)
        self.assertFalse(result["create_permitted"])

    def test_existing_container_still_needs_explicit_metadata_read(self):
        result = anchor.resolve_hierarchy(root(), self.root_scan)
        self.assertEqual(result["action"], "CHECK_EXACT_CHILD_METADATA")
        self.assertEqual(result["remote_id"], CONTAINER_ID)

    def test_duplicate_same_name_at_drive_root_never_selects_first(self):
        duplicate = scan(ROOT, [item(CONTAINER_ID, "Meu Artigo"),
                                item("second-meu-artigo-001", "Meu Artigo")])
        result = anchor.resolve_hierarchy(root(), duplicate)
        self.assertEqual(result["action"], "BLOCKED_DUPLICATE_SAME_NAME")
        self.assertFalse(result["create_permitted"])

    def test_same_name_file_at_root_blocks_creation(self):
        result = anchor.resolve_hierarchy(root(), scan(ROOT,
                         [item("existing-nonfolder-001", "Meu Artigo", "file")]))
        self.assertEqual(result["action"], "BLOCKED_NAME_NOT_FOLDER")

    def test_same_named_folder_in_unrelated_parent_is_not_reused(self):
        with self.assertRaisesRegex(anchor.RootAnchorError,
                                    "CANONICAL_FOLDER_PARENT_IDENTITY_MISMATCH"):
            anchor.resolve_hierarchy(root(), self.root_scan,
                container_metadata=metadata(CONTAINER_ID, "Meu Artigo", WRONG_PARENT))

    def test_meta_container_must_match_provider_observed_id(self):
        with self.assertRaisesRegex(anchor.RootAnchorError,
                                    "CANONICAL_FOLDER_PARENT_IDENTITY_MISMATCH"):
            anchor.resolve_hierarchy(root(), self.root_scan,
                container_metadata=metadata("other-scope-folder-001", "Meu Artigo", ROOT))

    def test_project_must_be_direct_child_of_container(self):
        with self.assertRaisesRegex(anchor.RootAnchorError,
                                    "CANONICAL_FOLDER_PARENT_IDENTITY_MISMATCH"):
            anchor.resolve_hierarchy(root(), self.root_scan,
                container_metadata=self.meta, project_name=P_NAME,
                container_scan=self.child_scan,
                project_metadata=metadata(PROJECT_ID, P_NAME, WRONG_PARENT))

    def test_same_named_project_is_reused_under_container(self):
        result = self.resolved()
        self.assertEqual(result["action"], "CANONICAL_PROJECT_VERIFIED")
        self.assertEqual(result["my_drive_root_id"], ROOT)
        self.assertEqual(result["container_id"], CONTAINER_ID)
        self.assertEqual(result["project_id"], PROJECT_ID)
        self.assertFalse(result["create_permitted"])

    def test_missing_project_cannot_be_created_in_random_location(self):
        result = anchor.resolve_hierarchy(root(), self.root_scan,
            container_metadata=self.meta, project_name=P_NAME,
            container_scan=scan(CONTAINER_ID, []))
        self.assertEqual(result["action"], "CHECK_PARENT_FOR_GUARDED_CREATE")
        self.assertEqual(result["parent_id"], CONTAINER_ID)
        self.assertFalse(result["create_permitted"])

    def test_duplicate_project_names_block_resumption(self):
        result = anchor.resolve_hierarchy(root(), self.root_scan,
            container_metadata=self.meta, project_name=P_NAME,
            container_scan=scan(CONTAINER_ID, [
                item(PROJECT_ID, P_NAME), item("second-project-id-0001", P_NAME)]))
        self.assertEqual(result["action"], "BLOCKED_DUPLICATE_SAME_NAME")

    def test_incomplete_root_scan_does_not_authorize_creation(self):
        partial = scan(ROOT, [])
        partial["page_evidence"][0]["next_page_token"] = "missing-next-page"
        with self.assertRaisesRegex(anchor.RootAnchorError, "CANONICAL_PAGINATION_INCOMPLETE"):
            anchor.resolve_hierarchy(root(), partial)

    def test_synthetic_fake_completed_with_mismatched_ids_refused(self):
        partial = scan(ROOT, [item(CONTAINER_ID, "Meu Artigo")])
        partial["page_evidence"][0]["item_ids"] = []
        with self.assertRaisesRegex(anchor.RootAnchorError, "CANONICAL_PAGINATION_INCOMPLETE"):
            anchor.resolve_hierarchy(root(), partial)

    def test_missing_root_metadata_blocked(self):
        with self.assertRaisesRegex(anchor.RootAnchorError, "MY_DRIVE_ROOT_METADATA_REQUIRED"):
            anchor.resolve_hierarchy(None, self.root_scan)

    def test_non_root_parent_metadata_blocked(self):
        bad_root = dict(root(), parents=[WRONG_PARENT])
        with self.assertRaisesRegex(anchor.RootAnchorError, "MY_DRIVE_ROOT_IDENTITY_INVALID"):
            anchor.resolve_hierarchy(bad_root, self.root_scan)

    def test_project_parent_scan_scope_must_match_container(self):
        with self.assertRaisesRegex(anchor.RootAnchorError, "CANONICAL_PARENT_SCAN_REQUIRED"):
            anchor.resolve_hierarchy(root(), self.root_scan,
                container_metadata=self.meta, project_name=P_NAME,
                container_scan=scan(WRONG_PARENT, [item(PROJECT_ID, P_NAME)]))

    def test_anchored_plan_preserves_exact_three_identifiers(self):
        scoped = anchor.attach_scope(self.plan, self.resolved())
        self.assertEqual(scoped["drive_root_id"], PROJECT_ID)
        self.assertEqual(scoped["root_scope"]["scheme"], anchor.SCHEME)
        self.assertEqual(scoped["root_scope"]["container_id"], CONTAINER_ID)
        self.assertEqual(anchor.require_scope(scoped)["my_drive_root_id"], ROOT)

    def test_unscoped_legacy_plan_cannot_pass_new_root_gate(self):
        with self.assertRaisesRegex(anchor.RootAnchorError, "CANONICAL_ROOT_SCOPE_REQUIRED"):
            anchor.require_scope(self.plan)

    def test_root_scope_drift_or_project_mismatch_is_rejected(self):
        scoped = anchor.attach_scope(self.plan, self.resolved())
        scoped["root_scope"]["container_id"] = PROJECT_ID
        with self.assertRaisesRegex(ValueError, "CANONICAL_ROOT_SCOPE_MISMATCH"):
            anchor.require_scope(scoped)

    def test_renamed_project_refused_even_if_project_id_is_right(self):
        with self.assertRaisesRegex(anchor.RootAnchorError, "CANONICAL_DELIVERY_PLAN_SCOPE_MISMATCH"):
            anchor.attach_scope(dict(self.plan, project_folder="ARTIGO_Outro_2026"),
                                self.resolved())

    def test_relative_nested_project_name_refused(self):
        with self.assertRaisesRegex(anchor.RootAnchorError, "CANONICAL_PROJECT_NAME_INVALID"):
            anchor.resolve_hierarchy(root(), self.root_scan,
                container_metadata=self.meta,
                project_name="other_project/ARTIGO_Exemplo_2026")

    def test_live_guard_cli_scope_requirement_blocks_old_arbitrary_root(self):
        import tempfile
        import drive_create_guard as create_guard
        with tempfile.TemporaryDirectory() as temp:
            journal = Path(temp) / "private" / "journal.json"
            # Must fail BEFORE any durable journal initialization.
            with self.assertRaisesRegex(anchor.RootAnchorError,
                                        "CANONICAL_ROOT_SCOPE_REQUIRED"):
                create_guard.locked_update(
                    self.plan, {"schema": 1}, journal, "00_Gestao_e_Continuidade",
                    "initialize", initialize_authorized=True,
                    enforce_root_scope=True)
            self.assertFalse(journal.exists())

    def test_scoped_delivery_plan_rejects_tampered_parent_identity(self):
        import drive_delivery as delivery
        plan = anchor.attach_scope(self.plan, self.resolved())
        plan["root_scope"]["project_id"] = ROOT
        with self.assertRaisesRegex(ValueError, "CANONICAL_ROOT_SCOPE_MISMATCH"):
            delivery.check_plan(plan)

    def test_scoped_plan_cli_writes_only_to_new_external_file(self):
        import json
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            project = base / "project"
            project.mkdir()
            audit = base / "audit"
            audit.mkdir()
            def dump(name, value):
                p = audit / name
                p.write_text(json.dumps(value), encoding="utf-8")
                return p
            root_meta = dump("my-drive.json", root())
            root_scan = dump("root-scan.json", self.root_scan)
            container_meta = dump("container-meta.json", self.meta)
            container_scan = dump("container-scan.json", self.child_scan)
            project_meta = dump("project-meta.json", self.project_meta)
            original = dump("plan.json", self.plan)
            dest = audit / "scoped-plan.json"
            cmd = [
                sys.executable,
                str(Path(__file__).resolve().parents[1] /
                    "scripts" / "drive_root_anchor.py"),
                "--root-metadata", str(root_meta), "--root-scan", str(root_scan),
                "--container-metadata", str(container_meta),
                "--container-scan", str(container_scan),
                "--project-metadata", str(project_meta),
                "--project-name", P_NAME,
                "--plan", str(original),
                "--project-root", str(project),
                "--scoped-plan-output", str(dest),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(dest.is_file())
            self.assertEqual(json.loads(dest.read_text())["root_scope"]["container_id"],
                             CONTAINER_ID)
            self.assertEqual(json.loads(original.read_text()), self.plan)
            # Never silently overwrite an existing pinned scoped plan.
            again = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            self.assertEqual(again.returncode, 2)
            self.assertEqual(json.loads(again.stdout)["action"], "BLOCKED")

    def test_scoped_plan_cli_refuses_destination_inside_project(self):
        import json
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            project = base / "project"
            project.mkdir()
            private = base / "private"
            private.mkdir()
            data = {
                "root.json": root(), "root-scan.json": self.root_scan,
                "container.json": self.meta,
                "container-scan.json": self.child_scan,
                "project.json": self.project_meta, "plan.json": self.plan,
            }
            for n, obj in data.items():
                (private / n).write_text(json.dumps(obj), encoding="utf-8")
            target = project / "not-allowed-plan.json"
            cmd = [sys.executable,
                str(Path(__file__).resolve().parents[1] /
                    "scripts" / "drive_root_anchor.py"),
                "--root-metadata", str(private / "root.json"),
                "--root-scan", str(private / "root-scan.json"),
                "--container-metadata", str(private / "container.json"),
                "--container-scan", str(private / "container-scan.json"),
                "--project-metadata", str(private / "project.json"),
                "--project-name", P_NAME, "--plan", str(private / "plan.json"),
                "--project-root", str(project), "--scoped-plan-output", str(target)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(target.exists())

    def test_created_folder_never_moves_existing_projects(self):
        result = anchor.resolve_hierarchy(root(), self.root_scan,
            container_metadata=self.meta, project_name="ARTIGO_Novo_2026",
            container_scan=self.child_scan)
        self.assertEqual(result["action"], "CHECK_PARENT_FOR_GUARDED_CREATE")
        self.assertNotIn("MOVE", result["action"])
        self.assertFalse(result["create_permitted"])


if __name__ == "__main__":
    unittest.main()
