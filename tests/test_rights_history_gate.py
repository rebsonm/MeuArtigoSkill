"""Read-only history audit tests, using synthetic local Git history only."""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_methodology_rights_history as history


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args], check=True,
        text=True, capture_output=True, timeout=15,
    )
    return result.stdout.strip()


class RightsHistorySafetyTests(unittest.TestCase):
    def test_real_incident_remains_pending_without_history_rewrite(self):
        data = history.load_manifest(ROOT)
        self.assertEqual(data["release_clearance"], "BLOCKED_PENDING_DOCUMENTED_DECISION")
        self.assertEqual(data["legal_conclusion"], "NOT_DETERMINED")
        entry = data["incidents"][0]
        self.assertEqual(entry["source_id"], "SRC-0367")
        self.assertEqual(entry["observed_license"], "CC BY-NC 4.0")
        self.assertFalse(entry["unrestricted_catalog_allowed"])
        self.assertFalse(entry["rewrite_authorized"])
        self.assertEqual(entry["owner_decision"], "PENDING")
        self.assertFalse((ROOT / entry["path"]).exists())
        pdfs = json.loads((ROOT / "knowledge/methodology/pdf_catalog.json").read_text("utf-8"))
        self.assertNotIn(entry["path"], [row["path"] for row in pdfs["documents"]])
        from build_skill_bundle import list_sources
        self.assertNotIn("scripts/audit_methodology_rights_history.py",
                         [p.relative_to(ROOT).as_posix() for p in list_sources(ROOT)])

    def test_synthetic_removed_file_is_still_in_full_history(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            git(root, "init", "-q")
            git(root, "config", "user.name", "Synthetic Test")
            git(root, "config", "user.email", "synthetic@example.invalid")
            path = "knowledge/methodology/pdfs/synthetic-fixture.pdf"
            target = root / path
            target.parent.mkdir(parents=True)
            target.write_bytes(b"synthetic fixture - not a real PDF")
            git(root, "add", path)
            git(root, "commit", "-qm", "Add synthetic specimen")
            containing = git(root, "rev-parse", "HEAD")
            blob = git(root, "rev-parse", "HEAD:" + path)
            target.unlink()
            git(root, "add", "-u")
            git(root, "commit", "-qm", "Remove synthetic specimen")
            removal = git(root, "rev-parse", "HEAD")
            data = {
                "release_clearance": "BLOCKED_PENDING_DOCUMENTED_DECISION",
                "incidents": [{
                    "source_id": "TEST-0001", "path": path,
                    "last_known_containing_commit": containing,
                    "historical_git_blob_sha": blob,
                    "deletion_commit": removal,
                    "owner_decision": "PENDING",
                    "history_review_status": "PENDING_COMPLETE_READ_ONLY_GIT_AUDIT"
                }],
            }
            manifest = root / history.INCIDENTS
            manifest.parent.mkdir(parents=True)
            manifest.write_text(
                json.dumps({"schema": "MEU_ARTIGO_RIGHTS_HISTORY_INCIDENTS_V1",
                            **data}), encoding="utf-8")
            self.assertEqual(history.load_manifest(root)["incidents"][0]["path"], path)
            out = history.audit(root, data)
            row = out["records"][0]
            self.assertTrue(row["historic_blob_locally_present"])
            self.assertTrue(row["last_containing_commit_has_path"])
            self.assertFalse(row["current_head_has_path"])
            self.assertTrue(row["local_refs_containing_historic_commit"])
            self.assertFalse(out["remote_caches_pull_refs_and_forks_exhaustively_checked"])
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(history.main(
                    ["--repo", str(root), "--require-release-clearance"]), 1)

    def test_refuse_invalid_path_and_commit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            p = root / history.INCIDENTS
            p.parent.mkdir(parents=True)
            base = history.load_manifest(ROOT)
            for field, value in (("path", "../../escape.pdf"),
                                 ("historical_git_blob_sha", "wrong")):
                with self.subTest(field=field):
                    data = json.loads(json.dumps(base))
                    data["incidents"][0][field] = value
                    p.write_text(json.dumps(data), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        history.load_manifest(root)


if __name__ == "__main__":
    unittest.main()
