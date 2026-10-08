"""Behavioral controls using explicitly artificial, temporary records only."""
import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import init_project
import governance_events

def run(name, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / name), *map(str, args)],
                          capture_output=True, text=True)

def write_csv(path, headers, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

class Controls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.mgmt = self.root / "00_Gestao_e_Continuidade"
        self.mgmt.mkdir()
        self.final = self.root / "06_Submissao/Arquivos_Finais"
        self.final.mkdir(parents=True)

    def profile(self, status="VERIFIED", **extra):
        data = {"status": status, "sensitive_terms": {},
                "default_external_artifact_mode": "EXTERNAL_ANONYMIZED", **extra}
        (self.mgmt / "ANONYMIZATION_PROFILE.json").write_text(json.dumps(data), encoding="utf-8")

    def audit(self, *args):
        result = run("audit_anonymization.py", self.root, *args)
        reports = sorted((self.root / "06_Submissao/Anonimizacao").glob("*.json"))
        return result, json.loads(reports[-1].read_text(encoding="utf-8"))

    def dedupe(self, records):
        path = self.root / "input.csv"
        write_csv(path, ["title", "doi", "authors", "year"], records)
        result = run("dedupe_records.py", path, "--out-dir", self.root / "out")
        self.assertEqual(result.returncode, 0, result.stderr)
        return read_csv(self.root / "out/consolidated_exact_dedup.csv")

    def test_conflicting_dois_same_title_are_retained(self):
        records = [{"title": "Introduction", "doi": doi, "authors": "Example A", "year": "2020"}
                   for doi in ["10.1234/a", "10.1234/b"]]
        self.assertEqual(len(self.dedupe(records)), 2)
        self.assertEqual(len(read_csv(self.root / "out/near_duplicate_review.csv")), 1)

    def test_title_requires_author_and_year(self):
        self.assertEqual(len(self.dedupe([
            {"title": "Editorial", "authors": "Example A", "year": "2020"},
            {"title": "Editorial", "authors": "Example B", "year": "2020"},
            {"title": "Editorial"}])), 3)

    def test_corroborated_title_merges(self):
        row = {"title": "Specific title", "authors": "Example A", "year": "2020"}
        self.assertEqual(len(self.dedupe([row, {**row, "doi": "10.1234/a"}])), 1)

    def test_exact_doi_merges(self):
        self.assertEqual(len(self.dedupe([
            {"title": "Version A", "doi": "https://doi.org/10.1234/a"},
            {"title": "Version B", "doi": "10.1234/a"}])), 1)

    def test_unicode_titles_remain_distinct(self):
        self.assertEqual(len(self.dedupe([
            {"title": "研究甲", "authors": "作者", "year": "2020"},
            {"title": "研究乙", "authors": "作者", "year": "2020"}])), 2)

    def test_learned_doi_cannot_merge_conflicting_record(self):
        row = {"title": "Specific title", "authors": "Example A", "year": "2020"}
        self.assertEqual(len(self.dedupe([row, {**row, "doi": "10.1234/a"},
                                          {**row, "doi": "10.1234/b"}])), 2)

    def test_empty_audit_cannot_be_acknowledged(self):
        self.profile()
        result, report = self.audit("--acknowledge-human-review")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report["result"], "FAIL")

    def test_unverified_profile_cannot_pass(self):
        self.profile("TO_CONFIGURE")
        (self.final / "manuscript.txt").write_text("Neutral content", encoding="utf-8")
        result, report = self.audit()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report["result"], "FAIL")

    def test_not_required_needs_rationale(self):
        self.profile("NOT_REQUIRED")
        (self.final / "manuscript.txt").write_text("Neutral content", encoding="utf-8")
        self.assertNotEqual(self.audit()[0].returncode, 0)

    def test_sensitive_content_fails(self):
        self.profile()
        (self.final / "manuscript.txt").write_text("author@example.org", encoding="utf-8")
        self.assertEqual(self.audit()[1]["result"], "FAIL")

    def initialize_release(self):
        for rel, headers in init_project.TABLES.items():
            write_csv(self.root / rel, headers, [])
        for name in ["CONTINUIDADE.md", "PROTOCOLO.md", "RASTREABILIDADE.md"]:
            (self.mgmt / name).write_text("Temporary test state", encoding="utf-8")
        self.profile()
        write_csv(self.mgmt / "18_Human_Validation_Gates.csv",
                  governance_events.GATE_HEADERS,
                  [{"GATE_ID": "GATE-0007", "Status": "COMPLETED",
                    "Decision": "APPROVED", "Validated_by": "Test reviewer",
                    "Validation_method": "Inspected temporary fixtures",
                    "Validation_evidence": "Synthetic test attestation"}])
        (self.final / "manuscript.txt").write_text("Neutral content", encoding="utf-8")
        self.assertEqual(self.audit()[0].returncode, 0)

    def test_release_requires_current_file_set_and_profile(self):
        self.initialize_release()
        self.assertEqual(run("validate_project.py", self.root).returncode, 0)
        manuscript = self.final / "manuscript.txt"
        manuscript.write_text("Modified content", encoding="utf-8")
        self.assertNotEqual(run("validate_project.py", self.root).returncode, 0)
        self.assertEqual(self.audit()[0].returncode, 0)
        self.assertEqual(run("validate_project.py", self.root).returncode, 0)
        added = self.final / "supplement.txt"
        added.write_text("Extra content", encoding="utf-8")
        self.assertNotEqual(run("validate_project.py", self.root).returncode, 0)
        self.audit()
        manuscript.unlink()
        self.assertNotEqual(run("validate_project.py", self.root).returncode, 0)
        self.audit()
        self.profile(notes="Changed scope")
        self.assertNotEqual(run("validate_project.py", self.root).returncode, 0)

    def test_legacy_audit_does_not_authorize_release(self):
        self.initialize_release()
        for path in (self.root / "06_Submissao/Anonimizacao").glob("*.json"):
            path.write_text('{"result": "PASS"}', encoding="utf-8")
        self.assertNotEqual(run("validate_project.py", self.root).returncode, 0)

    def test_default_decision_is_proposed_without_human(self):
        result = run("governance_events.py", "decision", self.root,
                     "--type", "METHOD", "--question", "Which design?",
                     "--decision", "Provisional design")
        self.assertEqual(result.returncode, 0, result.stderr)
        row = read_csv(self.mgmt / "17_Decision_Log.csv")[0]
        self.assertEqual(row["Status"], "PROPOSED")
        self.assertEqual(row["Decided_by"], "")

    def test_approval_requires_attribution_and_evidence(self):
        args = ("decision", self.root, "--type", "METHOD", "--question", "Which design?",
                "--decision", "Design", "--status", "APPROVED", "--rationale", "Reason")
        self.assertNotEqual(run("governance_events.py", *args).returncode, 0)
        self.assertNotEqual(run("governance_events.py", *args, "--decided-by", "Test reviewer").returncode, 0)
        result = run("governance_events.py", *args, "--decided-by", "Test reviewer",
                     "--evidence", "Synthetic attestation")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Synthetic attestation", read_csv(self.mgmt / "17_Decision_Log.csv")[0]["Notes"])

    def test_gate_requires_evidence(self):
        write_csv(self.mgmt / "18_Human_Validation_Gates.csv",
                  governance_events.GATE_HEADERS, [{"GATE_ID": "GATE-0001"}])
        args = ("gate", self.root, "--gate-id", "GATE-0001", "--decision", "APPROVED",
                "--validated-by", "Test reviewer", "--method", "Reviewed", "--no-snapshot")
        self.assertNotEqual(run("governance_events.py", *args).returncode, 0)
        self.assertEqual(run("governance_events.py", *args, "--evidence", "Synthetic attestation").returncode, 0)

if __name__ == "__main__":
    unittest.main()

