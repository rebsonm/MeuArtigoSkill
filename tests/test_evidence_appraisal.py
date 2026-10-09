"""Offline adversarial checks for type-aware critical appraisal.

No sources, human reviewers or scientific conclusions are fabricated as
research evidence: temporary fixture records only exercise software checks.
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
import appraise_evidence as app
import init_project as init

def run(name,*argv):
    return subprocess.run([sys.executable,str(SCRIPTS/name),*map(str,argv)],
                          capture_output=True,text=True)


class EvidenceAppraisalTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.mgmt=self.root/"00_Gestao_e_Continuidade"
        self.mgmt.mkdir()
        self.file=self.root/app.EVIDENCE
        self.headers=init.TABLES[app.EVIDENCE]
        self.write([{"Evidence_ID":"EVID-0001","Citation":"Temporary test fixture"}])
        (self.mgmt/"PROJECT_CONFIG.json").write_text(json.dumps({"critical_appraisal_required":True}),encoding="utf-8")
        self.checklist=self.root/"rubric.json"

    def write(self, rows):
        with self.file.open("w",encoding="utf-8-sig",newline="") as s:
            w=csv.DictWriter(s,fieldnames=self.headers);w.writeheader();w.writerows(rows)

    def rows(self):
        return app.load(self.root)[-1]

    def checklist_for(self,family="QUALITATIVE",rating="YES"):
        contents={k:{"rating":rating,"basis":"The source sections were checked against this item in the methodological description."}
                  for k in app.FAMILIES[family]}
        self.checklist.write_text(json.dumps(contents),encoding="utf-8")
        return contents

    def record(self,family="QUALITATIVE",judgement="SUITABLE_FOR_CLAIM",**overrides):
        args=["record",self.root,"--evidence-id","EVID-0001","--family",family,
              "--checklist",self.checklist,"--judgement",judgement,
              "--rationale","The source method fits the exact theoretical claim and the stated research scope.",
              "--limitations","There may still be limitations due to the accessible material and external validity.",
              "--reviewer","Researcher",
              "--review-evidence","Direct response recorded in the research session"]
        for key,value in overrides.items():
            flag="--"+key.replace("_","-")
            loc=args.index(flag);args[loc+1]=value
        return run("appraise_evidence.py",*args)

    def test_seven_distinct_type_specific_checklists(self):
        self.assertEqual(len(app.FAMILIES),7)
        self.assertNotEqual(set(app.FAMILIES["QUALITATIVE"]),set(app.FAMILIES["QUANTITATIVE"]))
        self.assertIn("authority_version",app.FAMILIES["NORMATIVE"])
        self.assertIn("synthesis_appraisal",app.FAMILIES["REVIEW"])

    def test_template_has_no_auto_scores(self):
        proc=run("appraise_evidence.py","template","--family","REVIEW")
        self.assertEqual(proc.returncode,0,proc.stderr)
        template=json.loads(proc.stdout)
        self.assertEqual(template["search_coverage"]["rating"],"")
        self.assertIn("question",template["search_coverage"])

    def test_correctly_recorded_human_judgement_is_structurally_valid(self):
        self.checklist_for()
        result=self.record()
        self.assertEqual(result.returncode,0,result.stderr)
        row=self.rows()[0]
        self.assertEqual(row["Appraisal_family"],"QUALITATIVE")
        self.assertEqual(row["Appraisal_judgement"],"SUITABLE_FOR_CLAIM")
        self.assertEqual(app.assessment_issues(row,required=True),[])
        self.assertIn("research session",row["Appraisal_evidence"])

    def test_an_unassessed_reference_is_not_approved(self):
        report=app.audit(self.rows(),required_ids={"EVID-0001"},enforce=True,headers=self.headers)
        self.assertTrue(any("not documented" in v for v in report["errors"]))

    def test_wrong_family_checklist_is_rejected(self):
        self.checklist_for("QUANTITATIVE")
        result=self.record(family="QUALITATIVE")
        self.assertNotEqual(result.returncode,0)
        self.assertIn("checklist keys",result.stderr)

    def test_false_suitability_with_flagged_criterion_is_blocked(self):
        table=self.checklist_for()
        table["design_fit"]["rating"]="NO"
        self.checklist.write_text(json.dumps(table),encoding="utf-8")
        result=self.record()
        self.assertNotEqual(result.returncode,0)
        self.assertIn("conflicts with flagged",result.stderr)

    def test_flagged_source_can_be_qualified_not_automatically_excluded(self):
        self.checklist_for(rating="UNCLEAR")
        result=self.record(judgement="USE_WITH_CAVEATS")
        self.assertEqual(result.returncode,0,result.stderr)
        audit=app.audit(self.rows(),required_ids={"EVID-0001"},enforce=True,headers=self.headers)
        self.assertEqual(audit["errors"],[])
        self.assertEqual(audit["counts"]["with_caveats"],1)

    def test_missing_rationale_is_not_allowed(self):
        self.checklist_for()
        result=self.record(rationale="OK")
        self.assertNotEqual(result.returncode,0)

    def test_missing_criterion_basis_is_rejected(self):
        vals=self.checklist_for()
        vals["analysis_trace"]["basis"]="OK"
        self.checklist.write_text(json.dumps(vals),encoding="utf-8")
        self.assertNotEqual(self.record().returncode,0)

    def test_not_applicable_requires_explanation_and_is_not_unqualified(self):
        vals=self.checklist_for()
        vals["analysis_trace"]["rating"]="NOT_APPLICABLE"
        vals["analysis_trace"]["basis"]=""
        self.checklist.write_text(json.dumps(vals),encoding="utf-8")
        self.assertNotEqual(self.record().returncode,0)

    def test_ai_cannot_be_attributed_as_human_reviewer(self):
        self.checklist_for()
        self.assertNotEqual(self.record(reviewer="ChatGPT").returncode,0)

    def test_record_is_not_silently_overwritten(self):
        self.checklist_for()
        self.assertEqual(self.record().returncode,0)
        self.assertNotEqual(self.record().returncode,0)

    def test_missing_human_review_evidence_is_rejected(self):
        self.checklist_for()
        self.assertNotEqual(self.record(review_evidence="sim").returncode,0)

    def test_unsuitable_evidence_cannot_support_frozen_claim(self):
        self.checklist_for(rating="NO")
        self.assertEqual(self.record(judgement="DO_NOT_USE_FOR_CLAIM").returncode,0)
        checked=app.audit(self.rows(),required_ids={"EVID-0001"},enforce=True,headers=self.headers)
        self.assertTrue(any("cannot rely" in x for x in checked["errors"]))

    def test_insufficient_evidence_must_not_be_promoted_to_suitable(self):
        self.checklist_for(rating="UNCLEAR")
        self.assertEqual(self.record(judgement="INSUFFICIENT_INFORMATION").returncode,0)
        check=app.audit(self.rows(),required_ids={"EVID-0001"},enforce=True,headers=self.headers)
        self.assertTrue(check["errors"])

    def test_incorrect_criterion_json_detected_even_if_manually_written(self):
        row=self.rows()[0]
        row.update({"Appraisal_family":"QUALITATIVE","Appraisal_criteria":"{\"wrong\":true}",
                    "Appraisal_judgement":"SUITABLE_FOR_CLAIM"})
        self.assertTrue(app.assessment_issues(row))

    def test_legacy_project_does_not_require_unrecorded_appraisals(self):
        report=app.audit(self.rows(),required_ids=set(),enforce=False,headers=self.headers)
        self.assertEqual(report["errors"],[])

    def test_unknown_material_evidence_id_is_detected(self):
        report=app.audit(self.rows(),required_ids={"EVID-9999"},enforce=True,headers=self.headers)
        self.assertTrue(any("unknown evidence" in x for x in report["errors"]))

    def test_gate6_approval_validates_quality_for_used_evidence(self):
        with (self.mgmt/"09_Claims_Ledger.csv").open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=init.TABLES["00_Gestao_e_Continuidade/09_Claims_Ledger.csv"])
            w.writeheader();w.writerow({"Claim_ID":"CLAIM-0001","Evidence_IDs":"EVID-0001",
                                         "Robustness_status":"ROBUST"})
        with (self.mgmt/"18_Human_Validation_Gates.csv").open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=init.TABLES["00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv"])
            w.writeheader();w.writerow({"GATE_ID":"GATE-0006","Status":"COMPLETED",
                                         "Decision":"APPROVED","Validated_by":"Researcher",
                                         "Validation_method":"Researcher review"})
        result=run("validate_project.py",self.root)
        self.assertIn("critical appraisal: EVID-0001: critical appraisal not documented",result.stdout)
        self.checklist_for()
        self.assertEqual(self.record().returncode,0)
        result=run("validate_project.py",self.root)
        self.assertNotIn("critical appraisal:",result.stdout)

    def test_public_repo_docs_dont_claim_private_access(self):
        readme=(ROOT/"README.md").read_text(encoding="utf-8").lower()
        guide=(ROOT/"docs/COMECE-AQUI.md").read_text(encoding="utf-8").lower()
        self.assertIn("repositório público",readme)
        self.assertNotIn("repositório privado",readme)
        self.assertNotIn("repositório está privado",guide)

    def test_existing_workbook_tab_is_extended_not_replaced(self):
        workbook=(SCRIPTS/"build_matrix_template.py").read_text(encoding="utf-8")
        self.assertIn('"A1:AF1"',workbook)
        self.assertIn('"09_MATRIZ_EVID"',workbook)
        self.assertIn('"Julgamento crítico"',workbook)


if __name__=="__main__":
    unittest.main()
