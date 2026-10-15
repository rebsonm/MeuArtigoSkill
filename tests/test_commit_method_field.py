"""Synthetic human declarations used ONLY to exercise real controlled method writers.

The test actor does not authenticate people or validate scientific methods.
All tests run inside fresh disposable local projects, never a user's Drive.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import choose_method_route as route_writer
import commit_method_field as field_writer
import governance_events as gov
import method_route_transaction as tx
import method_routes
from method_routes import profile_issues

REVIEWER="Fictional human fixture researcher"
EVIDENCE="synthetic-human-answer-reference-0001"
RATIONALE="A fictional researcher's methodological decision is recorded only to test safe software write behavior and rollback."
PROSE=("The fictional inquiry uses deliberately bounded documentary data and considers "
       "context, provenance, alternative approaches and limits of transferability.")

def csv_file(path,headers,rows=None):
    with path.open("w",encoding="utf-8-sig",newline="") as stream:
        w=csv.DictWriter(stream,fieldnames=headers)
        w.writeheader()
        w.writerows(rows or [])

class MethodControlledWriterTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name)/"project"
        self.m=self.root/method_routes.MGMT
        self.m.mkdir(parents=True)
        (self.m/"PROJECT_CONFIG.json").write_text(json.dumps({
            "method_route_governance_required":True,"method_route":"UNDECIDED",
            "article_type":"fictional research"}))
        (self.m/"METHOD_PROFILE.json").write_text(json.dumps(method_routes.new_profile("UNDECIDED")))
        csv_file(self.m/"18_Human_Validation_Gates.csv",gov.GATE_HEADERS,
                 [{"GATE_ID":f"GATE-{i:04d}","Status":"PENDING","Decision":"PENDING"}
                   for i in range(1,8)])
        csv_file(self.m/"17_Decision_Log.csv",gov.DEC_HEADERS)
        csv_file(self.m/"13_Traceability_Log.csv",gov.TRACE_HEADERS)

    def choose(self,method="QUALITATIVE"):
        return route_writer.choose(self.root,method,REVIEWER,EVIDENCE,RATIONALE)

    def state(self):
        return {p.name:p.read_bytes() for p in self.m.iterdir() if p.is_file()}

    def commit(self,field="material_sources",value=PROSE,**changes):
        opts={"field":field,"proposed_text":value,
              "decided_by":REVIEWER,"evidence":EVIDENCE,
              "rationale":RATIONALE,
              "confirmed_by_researcher":True,
              "option_id":None,
              "acknowledge_warnings":False}
        opts.update(changes)
        return field_writer.commit(self.root,**opts)

    def test_success_writes_only_one_field_plus_dec_trace_and_no_gate(self):
        self.choose()
        gate_before=(self.m/"18_Human_Validation_Gates.csv").read_bytes()
        cfg_before=(self.m/"PROJECT_CONFIG.json").read_bytes()
        res=self.commit(option_id="DOCUMENTS")
        self.assertEqual(res["status"],"DECLARED_RESEARCHER_METHOD_FIELD_RECORDED_NOT_AUTHENTICATED")
        self.assertEqual(res["decision_id"],"DEC-0002")
        self.assertFalse(res["scientific_gate_approved"])
        self.assertFalse(res["scientific_suitability_validated"])
        self.assertFalse(res["real_researcher_identity_independently_authenticated"])
        self.assertFalse(res["google_drive_sync_verified"])
        self.assertFalse(res["field_value_echoed"])
        self.assertFalse(tx.has_pending_method_route(self.root))
        self.assertEqual((self.m/"PROJECT_CONFIG.json").read_bytes(),cfg_before)
        self.assertEqual((self.m/"18_Human_Validation_Gates.csv").read_bytes(),gate_before)
        profile=json.loads((self.m/"METHOD_PROFILE.json").read_text())
        self.assertEqual(profile["route_details"]["material_sources"],PROSE)
        with (self.m/"17_Decision_Log.csv").open(encoding="utf-8-sig",newline="") as st:
            dec=list(csv.DictReader(st))
        self.assertEqual(len(dec),2)
        self.assertEqual(dec[1]["Decision_type"],"METHOD")
        self.assertEqual(dec[1]["Decision_question"],"Researcher methodological detail: material_sources")
        self.assertNotIn(PROSE,dec[1]["Decision"])
        with (self.m/"13_Traceability_Log.csv").open(encoding="utf-8-sig",newline="") as st:
            self.assertEqual(len(list(csv.DictReader(st))),2)

    def test_rejects_markers_before_changing_any_file(self):
        self.choose()
        for token in ("PENDING","NOT_EXECUTED","APPROVED","N/A","null",""):
            with self.subTest(token=token):
                before=self.state()
                with self.assertRaisesRegex(ValueError,"METHOD_PREFLIGHT_BLOCKED"):
                    self.commit(value=token)
                self.assertEqual(self.state(),before)
                self.assertFalse(tx.has_pending_method_route(self.root))

    def test_rejects_foreign_fields_and_choices_without_governance_event(self):
        self.choose()
        before=self.state()
        with self.assertRaises(ValueError):
            self.commit(field="inference_aim",value="CAUSAL")
        with self.assertRaises(ValueError):
            self.commit(value=PROSE,option_id="PROBABILITY")
        self.assertEqual(self.state(),before)

    def test_denies_unconfirmed_routes_and_unattributed_decision(self):
        before=self.state()
        with self.assertRaisesRegex(ValueError,"confirmed"):
            self.commit()
        self.assertEqual(self.state(),before)
        self.choose()
        before=self.state()
        for params in (
            {"confirmed_by_researcher":False},
            {"decided_by":"PENDING"},
            {"evidence":"APPROVED"},
            {"rationale":"short"},
            {"rationale":"PENDING"},
        ):
            with self.subTest(params=params),self.assertRaises(ValueError):
                self.commit(**params)
            self.assertEqual(self.state(),before)

    def test_existing_field_must_not_be_silently_replaced(self):
        self.choose()
        self.commit()
        before=self.state()
        with self.assertRaisesRegex(ValueError,"METHOD_PREFLIGHT_BLOCKED"):
            self.commit(value="An alternative fictional plan for different materials.")
        self.assertEqual(self.state(),before)

    def test_warning_requires_explicit_acknowledgment_but_not_science_approval(self):
        self.choose()
        before=self.state()
        with self.assertRaisesRegex(ValueError,"WARNINGS_REQUIRE"):
            self.commit(value="Interviews")
        self.assertEqual(self.state(),before)
        result=self.commit(value="Interviews",acknowledge_warnings=True)
        self.assertEqual(result["warning_count_acknowledged"],1)
        self.assertFalse(result["scientific_gate_approved"])

    def test_rejects_when_scientific_gate_previously_approved(self):
        self.choose()
        path=self.m/"18_Human_Validation_Gates.csv"
        rows=gov.rows(path)
        rows[1]["Status"]="COMPLETED"
        rows[1]["Decision"]="APPROVED"
        csv_file(path,gov.GATE_HEADERS,rows)
        before=self.state()
        with self.assertRaisesRegex(ValueError,"gate"):
            self.commit()
        self.assertEqual(self.state(),before)

    def test_protects_against_partial_write_after_governance_event(self):
        self.choose()
        before=self.state()
        original=Path.write_text
        def fail(path,*args,**kw):
            if path.name=="METHOD_PROFILE.json":
                raise OSError("fictional simulated disk write failure")
            return original(path,*args,**kw)
        with mock.patch.object(Path,"write_text",fail):
            with self.assertRaisesRegex(OSError,"fictional simulated disk write failure"):
                self.commit()
        self.assertEqual(self.state(),before)
        self.assertFalse(tx.has_pending_method_route(self.root))

    def test_abrupt_stop_is_recoverable_and_does_not_approve_gate(self):
        self.choose()
        before=self.state()
        original=Path.write_text
        def stop(path,*args,**kw):
            if path.name=="METHOD_PROFILE.json":
                raise SystemExit("abrupt synthetic interruption")
            return original(path,*args,**kw)
        with mock.patch.object(Path,"write_text",stop):
            with self.assertRaises(SystemExit):
                self.commit()
        self.assertTrue(tx.has_pending_method_route(self.root))
        with self.assertRaises(tx.PendingMethodRouteTransaction):
            self.commit()
        result=tx.recover_method_route(self.root)
        self.assertEqual(result["status"],"PREPARED_METHOD_ROUTE_ROLLED_BACK")
        self.assertEqual(self.state(),before)
        self.assertFalse(tx.has_pending_method_route(self.root))

    def test_official_enum_is_enforced_inside_actual_writer(self):
        self.choose("QUANTITATIVE")
        before=self.state()
        with self.assertRaisesRegex(ValueError,"METHOD_PREFLIGHT_BLOCKED"):
            self.commit(field="inference_aim",value="DEMONSTRATED_CAUSAL")
        self.assertEqual(self.state(),before)
        result=self.commit(field="inference_aim",value="ASSOCIATIONAL")
        self.assertFalse(result["scientific_gate_approved"])
        self.assertEqual(json.loads((self.m/"METHOD_PROFILE.json").read_text())
                         ["route_details"]["inference_aim"],"ASSOCIATIONAL")

    def test_gate2_catches_manual_placeholder_edits_outside_writer(self):
        self.choose("QUANTITATIVE")
        profile=json.loads((self.m/"METHOD_PROFILE.json").read_text())
        profile["research_question"]="Fictional question about administrative rates."
        profile["intended_inference"]="ASSOCIATIONAL"
        profile["study_limits"]="Only synthetic data in a bounded exercise."
        profile["route_details"]={name:"A fictional defined method decision" for name in
                                  method_routes.REQUIRED_DESIGN["QUANTITATIVE"]}
        profile["route_details"]["inference_aim"]="ASSOCIATIONAL"
        profile["route_details"]["sampling_logic"]="PENDING"
        profile["onion"]["research_strategy"]="Fictional approach"
        profile["onion"]["techniques_and_procedures"]="Fictional techniques"
        profile["onion"]["coherence_rationale"]="Fictional methodological justification"
        issues=profile_issues(profile,"QUANTITATIVE",gate="GATE-0002")
        self.assertTrue(any("placeholder value in sampling_logic" in x for x in issues))
        profile["route_details"]["sampling_logic"]="Fictional bounded selection"
        self.assertFalse(any("placeholder value in sampling_logic" in x
                             for x in profile_issues(profile,"QUANTITATIVE",gate="GATE-0002")))

    def test_bad_route_provenance_refuses_without_writes(self):
        self.choose()
        profile=json.loads((self.m/"METHOD_PROFILE.json").read_text())
        profile["route_decision_id"]="DEC-0999"
        (self.m/"METHOD_PROFILE.json").write_text(json.dumps(profile))
        before=self.state()
        with self.assertRaisesRegex(ValueError,"matching"):
            self.commit()
        self.assertEqual(self.state(),before)

    def test_cli_requires_researcher_review_and_saves_no_private_content_to_output(self):
        self.choose()
        secret="Confidential fictional narrative explaining the methodological boundary of archival data and legitimate limitations."
        draft=self.root/"draft.txt"
        draft.write_text(secret)
        cmd=[sys.executable,str(ROOT/"scripts/commit_method_field.py"),str(self.root),
             "--field","material_sources","--draft-file",str(draft),
             "--decided-by",REVIEWER,"--evidence",EVIDENCE,"--rationale",RATIONALE]
        before=self.state()
        first=subprocess.run(cmd,capture_output=True,text=True)
        self.assertEqual(first.returncode,2)
        self.assertEqual(before,self.state())
        committed=subprocess.run(cmd+["--researcher-reviewed"],capture_output=True,text=True)
        self.assertEqual(committed.returncode,0,committed.stderr)
        self.assertNotIn(secret,committed.stdout)
        obj=json.loads(committed.stdout)
        self.assertEqual(obj["status"],"DECLARED_RESEARCHER_METHOD_FIELD_RECORDED_NOT_AUTHENTICATED")
        self.assertTrue(obj["local_transaction_committed"])
        self.assertFalse(obj["scientific_gate_approved"])

if __name__=="__main__":
    unittest.main()
