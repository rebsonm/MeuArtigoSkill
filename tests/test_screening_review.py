"""Adversarial offline checks for provenance-aware single-researcher screening.

Test inputs are disposable software fixtures, not fabricated scientific evidence.
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/"scripts"
sys.path.insert(0,str(SCRIPTS))
import screening_review as screening
import init_project as initializer


def run(name,*args):
    return subprocess.run([sys.executable,str(SCRIPTS/name),*map(str,args)],
                          capture_output=True,text=True)


class ScreeningReviewTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.mgmt=self.root/"00_Gestao_e_Continuidade"
        self.mgmt.mkdir()
        self.path=self.root/screening.SCREENING
        self.headers=initializer.TABLES[screening.SCREENING]
        self.create([{"Record_ID":"R-0001","Title":"Test source record"}])
        (self.mgmt/"PROJECT_CONFIG.json").write_text(json.dumps(
            {"screening_human_decisions_required":True}),encoding="utf-8")

    def create(self,rows,cols=None):
        with self.path.open("w",encoding="utf-8-sig",newline="") as stream:
            writer=csv.DictWriter(stream,fieldnames=cols or self.headers)
            writer.writeheader()
            writer.writerows(rows)

    def data(self):
        _,_,rows=screening.read_table(self.root)
        return rows

    def suggest(self,proposal="BORDERLINE",stage="pass1"):
        return run("screening_review.py","propose",self.root,
                   "--stage",stage,"--record-id","R-0001",
                   "--proposal",proposal,
                   "--reason","The abstract covers a relevant question but leaves the institutional setting uncertain.",
                   "--source","Agent output ref in authorized research chat")

    def decide(self,decision="INCLUDE",stage="pass1",*extra):
        return run("screening_review.py","decide",self.root,
                   "--stage",stage,"--record-id","R-0001",
                   "--decision",decision,
                   "--reason","The record meets the documented inclusion criterion for public governance research.",
                   "--reviewer","Human reviewer",
                   "--evidence","Researcher decision recorded in conversation",
                   *extra)

    def test_schema_extends_existing_csv_and_no_new_ids(self):
        self.assertEqual(len(screening.EXTRA_COLUMNS),12)
        self.assertEqual(self.headers[-12:],screening.EXTRA_COLUMNS)
        self.assertIn("Pass1_decision",self.headers)

    def test_ai_only_is_not_human_final(self):
        result=self.suggest("EXCLUDE")
        self.assertEqual(result.returncode,0,result.stderr)
        row=self.data()[0]
        self.assertEqual(row["Pass1_AI_proposal"],"EXCLUDE")
        self.assertEqual(row["Pass1_decision"],"")
        report=screening.audit_rows(self.data(),enforce=True)
        self.assertEqual(report["counts"]["unreviewed_suggestions"],1)
        self.assertEqual(report["counts"]["recorded_exclusions"],0)

    def test_cannot_exclude_without_human_review(self):
        self.suggest("EXCLUDE")
        res=run("screening_review.py","audit",self.root,"--strict","--freeze")
        self.assertNotEqual(res.returncode,0)
        self.assertEqual(self.data()[0]["Pass1_decision"],"")

    def test_disagreement_requires_explicit_resolution(self):
        self.assertEqual(self.suggest("EXCLUDE").returncode,0)
        bad=self.decide("INCLUDE")
        self.assertNotEqual(bad.returncode,0)
        self.assertFalse(self.data()[0]["Pass1_decision"])
        good=self.decide("INCLUDE","pass1","--disagreement-reason",
                         "The researcher found direct alignment that the model did not recognize.")
        self.assertEqual(good.returncode,0,good.stderr)
        self.assertIn("researcher found",self.data()[0]["Pass1_disagreement_reason"].lower())
        audit=screening.audit_rows(self.data(),enforce=True)
        self.assertEqual(audit["counts"]["disagreements"],1)
        self.assertFalse(audit["errors"])

    def test_exclusion_requires_substantive_reason(self):
        bad=run("screening_review.py","decide",self.root,
                "--stage","pass1","--record-id","R-0001","--decision","EXCLUDE",
                "--reason","No","--reviewer","Human reviewer",
                "--evidence","Researcher decision recorded in conversation")
        self.assertNotEqual(bad.returncode,0)
        self.assertFalse(self.data()[0]["Pass1_decision"])

    def test_cannot_claim_agent_is_human_reviewer(self):
        result=run("screening_review.py","decide",self.root,
                   "--stage","pass1","--record-id","R-0001","--decision","EXCLUDE",
                   "--reason","This material does not meet the substantive eligibility criteria.",
                   "--reviewer","ChatGPT",
                   "--evidence","Researcher decision recorded in conversation")
        self.assertNotEqual(result.returncode,0)

    def test_human_decision_without_ai_is_allowed_not_double_screening(self):
        res=self.decide("EXCLUDE")
        self.assertEqual(res.returncode,0,res.stderr)
        audit=screening.audit_rows(self.data(),enforce=True,freeze=True)
        self.assertEqual(audit["errors"],[])
        self.assertEqual(audit["counts"]["ai_suggestions"],0)
        self.assertEqual(audit["counts"]["recorded_exclusions"],1)

    def test_ambiguous_case_blocks_freeze_until_pass2(self):
        self.assertEqual(self.decide("BORDERLINE").returncode,0)
        audit=screening.audit_rows(self.data(),enforce=True,freeze=True)
        self.assertTrue(any("corpus freeze" in x for x in audit["errors"]))
        self.assertEqual(self.decide("FULL TEXT — CORE","pass2").returncode,0)
        audit=screening.audit_rows(self.data(),enforce=True,freeze=True)
        self.assertEqual(audit["errors"],[])

    def test_pass2_cannot_overrule_pass1_exclusion(self):
        self.assertEqual(self.decide("EXCLUDE").returncode,0)
        result=self.decide("FULL TEXT — CORE","pass2")
        self.assertNotEqual(result.returncode,0)

    def test_a_proposal_cannot_be_backdated_after_final_decision(self):
        self.assertEqual(self.decide("INCLUDE").returncode,0)
        self.assertNotEqual(self.suggest("BORDERLINE").returncode,0)

    def test_final_human_decision_is_immutable_by_default(self):
        self.assertEqual(self.decide("INCLUDE").returncode,0)
        result=self.decide("EXCLUDE")
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(self.data()[0]["Pass1_decision"],"INCLUDE")

    def test_validator_rejects_unreviewed_manual_csv_exclusion(self):
        row=self.data()[0]
        row["Pass1_decision"]="EXCLUDE"
        row["Pass1_reason"]="Manual text in the final decision field"
        self.create([row])
        result=run("validate_project.py",self.root)
        self.assertNotEqual(result.returncode,0)
        self.assertIn("final decision without human review evidence",result.stdout)

    def test_legacy_project_without_opt_in_does_not_break_on_old_columns(self):
        cfg=self.mgmt/"PROJECT_CONFIG.json"
        cfg.write_text("{}",encoding="utf-8")
        old_headers=self.headers[:-12]
        self.create([{"Record_ID":"R-0001","Pass1_decision":"EXCLUDE",
                     "Pass1_reason":"Reviewed under old project rules"}],old_headers)
        report=screening.audit_rows(self.data(),enforce=False,headers=old_headers)
        self.assertFalse(report["errors"])
        strict=screening.audit_rows(self.data(),enforce=True,headers=old_headers)
        self.assertTrue(strict["errors"])

    def test_g4_approval_blocked_before_recording_when_ai_only(self):
        with (self.mgmt/"18_Human_Validation_Gates.csv").open("w",encoding="utf-8-sig",newline="") as stream:
            writer=csv.DictWriter(stream,fieldnames=initializer.TABLES[
                "00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv"])
            writer.writeheader()
            writer.writerow({"GATE_ID":"GATE-0004","Status":"READY","Name":"Freeze corpus"})
        self.assertEqual(self.suggest("EXCLUDE").returncode,0)
        args=["gate",self.root,"--gate-id","GATE-0004","--decision","APPROVED",
              "--validated-by","Researcher","--method","Protocol review",
              "--evidence","Direct human decision in chat","--no-snapshot"]
        blocked=run("governance_events.py",*args)
        self.assertNotEqual(blocked.returncode,0)
        # Agreement with an AI exclusion is permitted after documented human review.
        self.assertEqual(self.decide("EXCLUDE").returncode,0)
        approved=run("governance_events.py",*args)
        self.assertEqual(approved.returncode,0,approved.stderr)

    def test_duplicate_requires_canonical_record_link(self):
        row=self.data()[0]
        row["Duplicate_status"]="DUPLICATE"
        self.create([row])
        check=screening.audit_rows(self.data(),enforce=True,freeze=True)
        self.assertTrue(any("canonical record" in x for x in check["errors"]))
        row["Canonical_record_id"]="R-0002"
        # A duplicate cannot be the sole record in a frozen research corpus.
        # This real test fixture includes a reviewed canonical record as well.
        canonical_record={
            "Record_ID":"R-0002",
            "Pass1_decision":"EXCLUDE",
            "Pass1_reason":"The canonical record does not meet the documented scientific eligibility criteria.",
            "Pass1_reviewed_by":"Human reviewer",
            "Pass1_review_evidence":"Researcher decision recorded in conversation",
        }
        self.create([row, canonical_record])
        check=screening.audit_rows(self.data(),enforce=True,freeze=True)
        self.assertFalse(check["errors"])

    def test_excel_template_has_separate_proposal_and_review_columns(self):
        script=(SCRIPTS/"build_matrix_template.py").read_text(encoding="utf-8")
        for label in ("Pass1 proposta IA","Pass1 revisado por","Pass2 proposta IA","Pass2 evidência revisão"):
            self.assertIn(label,script)
        self.assertIn('end=excel_column(len(heads))',script)
        self.assertIn('"A1:AD1"',script)


if __name__=="__main__":
    unittest.main()
