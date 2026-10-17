"""Stage 13: synthetic REG-013/001/019 and read-only UI contract tests.

No real source corpus, respondent, external connection or gate approval.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import scientific_panel_projection as projection
import scientific_diagnostic as diag
import evaluation_package as package
import evaluation_registry as registry
import build_research_site as site
import build_research_workspace as workspace
import test_scientific_diagnostic as fixture


class Stage13DiagnosticAndReplayTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)

    def synthetic_case(self):
        case=fixture.DiagnosticTests(
            "test_even_clear_checks_do_not_make_scientific_approval")
        case.setUp()
        self.addCleanup(case.doCleanups)
        return case

    def test_missing_inputs_never_appear_as_zero_findings(self):
        p=projection.project(self.root)
        self.assertEqual(p["status"],"INPUTS_UNAVAILABLE")
        for k in ("objective_blockers","review_occurrences",
                  "advisory_occurrences","strict_required_occurrences"):
            self.assertIsNone(p[k])
        self.assertTrue(p["human_review_required"])
        self.assertFalse(p["scientific_quality_validated"])

    def test_clean_register_is_still_pending_human_review(self):
        case=self.synthetic_case()
        p=projection.project(case.root)
        self.assertEqual(p["status"],"RECORDED_UNASSESSED")
        self.assertEqual(p["verdict"],"REVISAO_CIENTIFICA_PENDENTE")
        self.assertEqual(p["objective_blockers"],0)
        self.assertIn("CLAIM_PENDING_HUMAN_REVIEW",p["priority_codes"])
        self.assertTrue(p["human_review_required"])
        self.assertFalse(p["scientific_quality_validated"])
        self.assertFalse(p["scientific_gate_approved"])
        self.assertFalse(p["semantic_support_proven"])

    def test_documentary_conflict_stays_objective_not_semantic(self):
        case=self.synthetic_case()
        case.claims[0]["Evidence_IDs"]="EVID-9999"
        case.write_inputs()
        p=projection.project(case.root)
        self.assertGreater(p["objective_blockers"],0)
        self.assertEqual(p["verdict"],"CORRECAO_REQUERIDA")
        self.assertTrue(p["human_review_required"])

    def test_private_source_and_reviewer_not_emitted(self):
        case=self.synthetic_case()
        marker="SECRET_NEVER_IN_UI_7437"
        case.evidence[0]["Citation"]="Fictional "+marker
        case.write_inputs()
        report=projection.project(case.root)
        self.assertNotIn(marker,json.dumps(report))
        self.assertNotIn(case.article.read_text(),json.dumps(report))
        self.assertNotIn(str(case.root),json.dumps(report))
        self.assertLess(len(json.dumps(report)),4000)

    def test_invalid_diagnostic_never_becomes_positive_ui_verdict(self):
        case=self.synthetic_case()
        model=workspace.model(route="QUALITATIVE")
        model["is_project_bound"]=True
        model["tasks"]={"items":[]}
        model["human_gates"]={"items":[]}
        model["scientific_diagnostic"]=projection.project(case.root)
        good=site.project_site_model(model)
        self.assertEqual(good["scientific_diagnostic"]["status"],
                         "RECORDED_UNASSESSED")
        self.assertFalse(good["automatic_scientific_approval"])
        self.assertFalse(good["canonical_writes_allowed"])
        model["scientific_diagnostic"]["scientific_quality_validated"]=True
        with self.assertRaisesRegex(ValueError,"SITE_DIAGNOSTIC_APPROVAL_FORBIDDEN"):
            site.project_site_model(model)

    def test_unknown_counter_is_rejected_not_disguised_as_zero(self):
        model=workspace.model(route="QUALITATIVE")
        model["is_project_bound"]=True
        d=projection.unavailable()
        d["objective_blockers"]=0
        model["scientific_diagnostic"]=d
        with self.assertRaisesRegex(ValueError,"SITE_DIAGNOSTIC_UNKNOWN_NOT_ZERO"):
            site.project_site_model(model)

    def test_script_payload_in_diagnostic_code_is_rejected(self):
        model=workspace.model(route="QUALITATIVE")
        model["is_project_bound"]=True
        d=projection.unavailable()
        d["priority_codes"]=["<img onerror=alert(1)>"]
        model["scientific_diagnostic"]=d
        with self.assertRaisesRegex(ValueError,"SITE_DIAGNOSTIC_CODES_INVALID"):
            site.project_site_model(model)

    def test_replay_archive_is_deterministic_and_not_science(self):
        cat=ROOT/"benchmarks/critical_cases_v1.json"
        first=self.root/"run1.zip"
        second=self.root/"run2.zip"
        a=package.build(first,cat)
        b=package.build(second,cat)
        self.assertEqual(first.read_bytes(),second.read_bytes())
        self.assertEqual(a["archive_sha256"],b["archive_sha256"])
        check=package.validate(first)
        self.assertTrue(check["replay_verified"])
        self.assertFalse(check["scientific_validity_proven"])
        self.assertFalse(check["external_evidence_verified"])
        self.assertEqual(check["run_count"],0)

    def test_replay_publish_rejects_atomic_name_collision(self):
        cat=ROOT/"benchmarks/critical_cases_v1.json"
        target=self.root/"collision.zip"
        original=package.os.link
        def competitor(src,dst,*,follow_symlinks=False):
            Path(dst).write_text("FOREIGN_WRITER",encoding="utf-8")
            raise FileExistsError("simulated concurrent publish")
        with patch.object(package.os,"link",side_effect=competitor):
            with self.assertRaisesRegex(ValueError,"Output already exists"):
                package.build(target,cat)
        self.assertEqual(target.read_text(),"FOREIGN_WRITER")
        self.assertEqual(list(self.root.glob(".reg019-*.zip")),[])

    def test_self_reported_score_cannot_be_certified(self):
        catalog=json.loads((ROOT/"benchmarks/critical_cases_v1.json")
                           .read_text(encoding="utf-8"))
        cases=registry.validate_catalog(catalog)
        result=registry.summarize(cases,{})
        self.assertEqual(result["observed"],0)
        self.assertIsNone(result["match_rate_on_observed"])
        self.assertFalse(result["scientific_validity_established"])
        self.assertFalse(result["independent_reviewer_authenticated"])


if __name__=="__main__":
    unittest.main()
