"""Offline regression tests for researcher's explanations at scientific gates."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import formative_gates as formative
import governance_events as governance


def run_script(name, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / name), *map(str, args)],
                          capture_output=True, text=True)


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


class FormativeGateTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.mgmt = self.root / "00_Gestao_e_Continuidade"
        self.mgmt.mkdir()
        self.gates = self.mgmt / "18_Human_Validation_Gates.csv"
        self.config = self.mgmt / "PROJECT_CONFIG.json"
        self.config.write_text(json.dumps({"formative_gates_required": True}), encoding="utf-8")
        self._seed_gate("GATE-0002")

    def _seed_gate(self, gid):
        with self.gates.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=governance.GATE_HEADERS)
            writer.writeheader()
            writer.writerow({"GATE_ID": gid, "Gate_type": "METHOD_PROTOCOL", "Status": "READY"})

    def approval(self, *options, gid="GATE-0002", decision="APPROVED"):
        return run_script(
            "governance_events.py", "gate", self.root, "--gate-id", gid,
            "--decision", decision, "--validated-by", "Researcher",
            "--method", "Direct methodological review",
            "--evidence", "Direct user response in the research conversation",
            "--no-snapshot", *options,
        )

    def explanations(self):
        return (
            "--researcher-rationale",
            "The integrative design permits comparing theoretical traditions to develop a conceptual synthesis.",
            "--researcher-limitation",
            "The conclusion remains conditional on coverage of the databases and explicit inclusion criteria.",
        )

    def test_substantive_original_response_completes_scientific_gate(self):
        result = self.approval(*self.explanations())
        self.assertEqual(result.returncode, 0, result.stderr)
        row = read_csv(self.gates)[0]
        self.assertEqual(row["Status"], "COMPLETED")
        self.assertEqual(row["Decision"], "APPROVED")
        self.assertEqual(formative.gate_issues(row), [])
        parsed = formative.extract_formative(row["Notes"])
        self.assertIn("integrative design", parsed["researcher_rationale"])
        self.assertIn("databases", parsed["researcher_limitation"])
        self.assertEqual(parsed["source"], row["Validation_evidence"])
        self.assertEqual(parsed["validated_by"], row["Validated_by"])

    def test_yes_without_explanation_cannot_approve(self):
        result = self.approval()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(read_csv(self.gates)[0]["Status"], "READY")
        self.assertFalse((self.mgmt / "13_Traceability_Log.csv").exists())

    def test_placeholder_cannot_approve(self):
        result = self.approval("--researcher-rationale", "Aprovado",
                               "--researcher-limitation", "OK")
        self.assertNotEqual(result.returncode, 0)

    def test_identical_reason_and_limitation_cannot_approve(self):
        phrase = "This is the best approach because the protocol brings different theories together."
        result = self.approval("--researcher-rationale", phrase,
                               "--researcher-limitation", phrase)
        self.assertNotEqual(result.returncode, 0)

    def test_approval_with_changes_still_requires_explanations(self):
        self.assertNotEqual(self.approval(decision="APPROVED_WITH_CHANGES").returncode, 0)
        self.assertEqual(self.approval(*self.explanations(), decision="APPROVED_WITH_CHANGES").returncode, 0)

    def test_rejected_decision_can_record_reason_without_approval(self):
        # The formative rule targets approval, not a refusal to approve.
        self.assertEqual(self.approval(decision="REJECTED").returncode, 0)

    def test_submission_release_gate_remains_operational(self):
        self._seed_gate("GATE-0007")
        result = self.approval(gid="GATE-0007")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIsNone(formative.extract_formative(read_csv(self.gates)[0]["Notes"]))

    def test_legacy_project_without_opt_in_is_not_automatically_migrated(self):
        self.config.write_text("{}", encoding="utf-8")
        self.assertEqual(self.approval().returncode, 0)

    def test_validator_blocks_removed_formative_response(self):
        self.assertEqual(self.approval(*self.explanations()).returncode, 0)
        data = read_csv(self.gates)
        data[0]["Notes"] = ""
        with self.gates.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=governance.GATE_HEADERS)
            writer.writeheader()
            writer.writerows(data)
        result = run_script("validate_project.py", self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no structured researcher explanation", result.stdout)

    def test_validator_blocks_forged_source_mismatch(self):
        self.assertEqual(self.approval(*self.explanations()).returncode, 0)
        data = read_csv(self.gates)
        data[0]["Validation_evidence"] = "Different, unsupported source"
        with self.gates.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=governance.GATE_HEADERS)
            writer.writeheader()
            writer.writerows(data)
        result = run_script("validate_project.py", self.root)
        self.assertIn("formative source does not correspond", result.stdout)

    def test_validator_blocks_changed_decision_in_formative_record(self):
        self.assertEqual(self.approval(*self.explanations()).returncode, 0)
        data = read_csv(self.gates)
        data[0]["Decision"] = "APPROVED_WITH_CHANGES"
        with self.gates.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=governance.GATE_HEADERS)
            writer.writeheader()
            writer.writerows(data)
        result = run_script("validate_project.py", self.root)
        self.assertIn("formative decision does not correspond", result.stdout)

    def test_short_explanation_is_rejected(self):
        self.assertNotEqual(self.approval("--researcher-rationale", "Because I agree",
                                          "--researcher-limitation", "No problem").returncode, 0)


if __name__ == "__main__":
    unittest.main()
