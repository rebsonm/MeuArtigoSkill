"""Synthetic offline tests for Drive tree delivery (no live Drive claims)."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import drive_delivery as delivery

ROOT_ID = "drive-root-000000001"
MANAGE_ID = "drive-manage-000001"
ARTICLE_ID = "drive-article-00001"


class DriveDeliveryTests(unittest.TestCase):
    def setUp(self):
        handle = tempfile.TemporaryDirectory()
        self.addCleanup(handle.cleanup)
        self.base = Path(handle.name)
        self.root = self.base / "ARTIGO_FICTICIO_2026"
        (self.root / "00_Gestao_e_Continuidade").mkdir(parents=True)
        (self.root / "05_Manuscrito").mkdir()
        self.config = self.root / "00_Gestao_e_Continuidade" / "PROJECT_CONFIG.json"
        self.config.write_text(json.dumps({
            "storage_mode": "GOOGLE_DRIVE_STAGING",
            "canonical_storage_backend": "GOOGLE_DRIVE",
            "drive_workspace_url": "https://drive.google.com/drive/folders/" + ROOT_ID,
            "fallback_authorized": False}), encoding="utf-8")
        self.article = self.root / "05_Manuscrito" / "Rascunho de ensaio.md"
        self.article.write_text("Pesquisa sintética.\n", encoding="utf-8")
        self.plan = delivery.build_plan(self.root, ROOT_ID)
        files = {e["path"]: e for e in self.plan["entries"]}
        self.inventory = {"schema": 1, "drive_root_id": ROOT_ID,
                          "observed_via": "FIXTURE", "entries": [
            {"type": "folder", "path": "00_Gestao_e_Continuidade",
             "id": MANAGE_ID, "parent_id": ROOT_ID},
            {"type": "folder", "path": "05_Manuscrito",
             "id": ARTICLE_ID, "parent_id": ROOT_ID},
            {"type": "file", "path": "00_Gestao_e_Continuidade/PROJECT_CONFIG.json",
             "id": "drive-config-0000001", "parent_id": MANAGE_ID,
             "sha256": files["00_Gestao_e_Continuidade/PROJECT_CONFIG.json"]["sha256"]},
            {"type": "file", "path": "05_Manuscrito/Rascunho de ensaio.md",
             "id": "drive-file-00000001", "parent_id": ARTICLE_ID,
             "sha256": files["05_Manuscrito/Rascunho de ensaio.md"]["sha256"],
             "size": self.article.stat().st_size}
        ]}

    def verify(self, inv=None):
        return delivery.reconcile(self.plan, self.inventory if inv is None else inv,
                                  allow_fixture=True)

    def action(self, inv=None):
        return delivery.next_action(self.plan, self.inventory if inv is None else inv,
                                    allow_fixture=True)

    def test_plan_nested_sha_and_stability(self):
        table = {e["path"]: e for e in self.plan["entries"]}
        article = table["05_Manuscrito/Rascunho de ensaio.md"]
        self.assertEqual(article["parent"], "05_Manuscrito")
        self.assertEqual(article["sha256"], hashlib.sha256(self.article.read_bytes()).hexdigest())
        self.assertEqual(self.plan, delivery.build_plan(self.root, ROOT_ID))

    def test_verified_tree_is_done(self):
        self.assertTrue(self.verify()["complete"])
        self.assertEqual(self.action()["action"], "DONE")

    def test_missing_folders_are_created_before_files(self):
        inv = copy.deepcopy(self.inventory)
        inv["entries"] = []
        self.assertEqual(self.action(inv)["action"], "CHECK_PARENT_FOR_CREATE")
        inv["entries"] = copy.deepcopy(self.inventory["entries"][:2])
        self.assertEqual(self.action(inv)["action"], "UPLOAD_FILE")
        self.assertEqual(self.action(inv)["parent_id"], MANAGE_ID)

    def test_partial_upload_resumes_only_missing_file(self):
        inv = copy.deepcopy(self.inventory)
        inv["entries"] = inv["entries"][:-1]
        action = self.action(inv)
        self.assertEqual(action["action"], "UPLOAD_FILE")
        self.assertEqual(action["path"], "05_Manuscrito/Rascunho de ensaio.md")
        self.assertTrue(action["no_overwrite"])
        self.assertFalse(self.verify(inv)["complete"])

    def test_existing_without_digest_requires_readback(self):
        inv = copy.deepcopy(self.inventory)
        inv["entries"][-1].pop("sha256")
        self.assertEqual(self.action(inv)["action"], "READ_BACK_FILE")
        self.assertFalse(self.verify(inv)["complete"])

    def test_remote_content_mismatch_blocks_no_overwrite(self):
        inv = copy.deepcopy(self.inventory)
        inv["entries"][-1]["sha256"] = "0" * 64
        action = self.action(inv)
        self.assertEqual(action["reason"], "CONTENT_CONFLICT")
        self.assertTrue(action["no_overwrite"])

    def test_duplicate_remote_filename_blocks(self):
        inv = copy.deepcopy(self.inventory)
        duplicate = copy.deepcopy(inv["entries"][-1])
        duplicate["id"] = "drive-other-0000001"
        inv["entries"].append(duplicate)
        self.assertEqual(self.action(inv)["reason"], "DUPLICATE_REMOTE_PATH")

    def test_wrong_parent_blocks(self):
        inv = copy.deepcopy(self.inventory)
        inv["entries"][-1]["parent_id"] = ROOT_ID
        self.assertEqual(self.action(inv)["reason"], "PARENT_CONFLICT")

    def test_type_mismatch_blocks(self):
        inv = copy.deepcopy(self.inventory)
        inv["entries"][1]["type"] = "file"
        self.assertEqual(self.action(inv)["reason"], "TYPE_CONFLICT")

    def test_reject_inventory_for_different_drive_root(self):
        inv = copy.deepcopy(self.inventory)
        inv["drive_root_id"] = "drive-other-root123"
        with self.assertRaisesRegex(ValueError, "INVENTORY_ROOT"):
            self.verify(inv)

    def test_fixture_never_counts_as_live_without_flag(self):
        with self.assertRaisesRegex(ValueError, "LIVE_DRIVE_INVENTORY_REQUIRED"):
            delivery.reconcile(self.plan, self.inventory)
        inv = copy.deepcopy(self.inventory)
        inv["observed_via"] = "LIVE_DRIVE"
        self.assertTrue(delivery.reconcile(self.plan, inv)["complete"])

    def test_work_fallback_is_not_drive_canonical(self):
        cfg = json.loads(self.config.read_text())
        cfg.update(storage_mode="WORK_FALLBACK", canonical_storage_backend="WORK_FALLBACK",
                   fallback_authorized=True)
        self.config.write_text(json.dumps(cfg))
        with self.assertRaisesRegex(ValueError, "DRIVE_CANONICAL_PROJECT_REQUIRED"):
            delivery.build_plan(self.root, ROOT_ID)

    def test_cannot_swap_root_id(self):
        with self.assertRaisesRegex(ValueError, "DRIVE_ROOT_MISMATCH"):
            delivery.build_plan(self.root, "drive-other-root123")

    def test_existing_project_files_unchanged(self):
        before = {p.relative_to(self.root): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        self.verify()
        delivery.build_plan(self.root, ROOT_ID)
        after = {p.relative_to(self.root): p.read_bytes()
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_symlink_escape_rejected(self):
        external = self.base / "outside.txt"
        external.write_text("sensitive")
        try:
            (self.root / "05_Manuscrito" / "external.txt").symlink_to(external)
        except OSError:
            self.skipTest("unsupported symlink")
        with self.assertRaisesRegex(ValueError, "UNSAFE_PROJECT_FILE"):
            delivery.build_plan(self.root, ROOT_ID)

    def test_restricted_pdf_requires_explicit_rights_review(self):
        (self.root / "05_Manuscrito" / "paper.pdf").write_bytes(b"%PDF")
        with self.assertRaisesRegex(ValueError, "RESTRICTED_MATERIAL"):
            delivery.build_plan(self.root, ROOT_ID)
        self.assertTrue(delivery.build_plan(self.root, ROOT_ID, allow_restricted=True)[
            "restricted_materials_review_declared"])

    def test_credentials_file_rejected(self):
        (self.root / ".env").write_text("TOKEN=do-not-read", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "UNSAFE_PROJECT_FILE"):
            delivery.build_plan(self.root, ROOT_ID)

    def test_manifest_output_must_not_be_inside_project(self):
        path = self.root / "manifest.json"
        with self.assertRaisesRegex(ValueError, "REPORT_MUST_REMAIN_OUTSIDE_PROJECT_ROOT"):
            delivery.write_json(path, self.plan, root=self.root)
        self.assertFalse(path.exists())

    def test_other_remote_files_not_deleted(self):
        inv = copy.deepcopy(self.inventory)
        inv["entries"].append({"type": "file", "path": "unrelated.txt",
                               "id": "drive-extra-0000001", "parent_id": ROOT_ID})
        self.assertTrue(self.verify(inv)["complete"])
        self.assertEqual(self.verify(inv)["unexpected_remote_paths"], ["unrelated.txt"])

    def test_gates_preserved(self):
        gates = self.root / "00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv"
        gates.write_text("GATE_ID,Status\nGATE-0001,PENDING\n", encoding="utf-8")
        delivery.build_plan(self.root, ROOT_ID)
        self.assertIn("PENDING", gates.read_text(encoding="utf-8"))

    def test_parent_with_period_preserved(self):
        folder = self.root / "05_Manuscrito" / "versao.1"
        folder.mkdir()
        (folder / "texto.md").write_text("Test", encoding="utf-8")
        result = delivery.build_plan(self.root, ROOT_ID)
        items = {e["path"]: e for e in result["entries"]}
        self.assertEqual(items["05_Manuscrito/versao.1/texto.md"]["parent"],
                         "05_Manuscrito/versao.1")
        delivery.check_plan(result)


if __name__ == "__main__":
    unittest.main()
