"""T05 regression: project metadata must be populated from real initializer inputs."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import init_project as init


class InitialMetadataSeedTests(unittest.TestCase):
    def test_metadata_seed_uses_exact_user_arguments_and_never_approves_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "00_Projeto.csv"
            init.write_csv(path, init.TABLES["00_Gestao_e_Continuidade/00_Projeto.csv"])
            created = init.seed_project_metadata(
                path, name="Homologacao RC1", problem="Como melhorar coordenação?",
                article_type="undecided", method_route="UNDECIDED",
                journal="", storage_mode="GOOGLE_DRIVE_STAGING",
                storage_state="DRIVE_STAGING_PENDING_UPLOAD", drive_url="")
            self.assertTrue(created)
            with path.open(encoding="utf-8-sig", newline="") as stream:
                records = {r["Field"]: r for r in csv.DictReader(stream)}
            self.assertEqual(records["Project_name"]["Value"], "Homologacao RC1")
            self.assertEqual(records["Original_research_problem"]["Value"], "Como melhorar coordenação?")
            self.assertEqual(records["Proposed_method_route"]["Status"], "PROVISIONAL_NOT_APPROVED")
            self.assertEqual(records["Storage_state"]["Status"], "NOT_DRIVE_SYNC_PROOF")
            self.assertEqual(records["Target_journal"]["Status"], "PENDING")
            self.assertTrue(all("GATE" in x["Notes"] for x in records.values()))

            original = path.read_bytes()
            self.assertFalse(init.seed_project_metadata(path, name="Overwrite attempt",
                problem="different", article_type="experimental", method_route="UNDECIDED",
                journal="", storage_mode="WORK_FALLBACK",
                storage_state="WORK_FALLBACK_AUTHORIZED", drive_url=""))
            self.assertEqual(path.read_bytes(), original)

    def test_initializer_integration_creates_populated_csv_and_retains_on_repeat(self):
        with tempfile.TemporaryDirectory() as temp:
            args = ["init_project.py", "--path", temp, "--name", "RC1 Test",
                    "--problem", "Research question exactly as given",
                    "--storage-mode", "WORK_FALLBACK",
                    "--fallback-authorized-by", "SYNTHETIC_TEST_OPERATOR"]
            with patch.object(sys, "argv", args), patch.object(init, "build_optional_visual_matrix", return_value="PENDING_XLSX_DEPENDENCY_UNAVAILABLE"):
                self.assertEqual(init.main(), 0)
            project = Path(temp) / f"ARTIGO_RC1-Test_{init.date.today().year}"
            path = project / "00_Gestao_e_Continuidade/00_Projeto.csv"
            with path.open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertGreater(len(rows), 1)
            self.assertEqual(next(r["Value"] for r in rows if r["Field"] == "Original_research_problem"),
                             "Research question exactly as given")
            gates = project / "00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv"
            with gates.open(encoding="utf-8-sig", newline="") as stream:
                self.assertTrue(all(r["Status"] == "PENDING" for r in csv.DictReader(stream)))
            data = path.read_bytes()
            with patch.object(sys, "argv", args), patch.object(init, "build_optional_visual_matrix", return_value="PENDING_XLSX_DEPENDENCY_UNAVAILABLE"):
                self.assertEqual(init.main(), 0)
            self.assertEqual(path.read_bytes(), data)


if __name__ == "__main__":
    unittest.main()
