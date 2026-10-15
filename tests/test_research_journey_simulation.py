"""End-to-end synthetic researcher journeys; never authenticate a fictional actor."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import simulate_research_journeys as journeys

class ResearchJourneySimulationTests(unittest.TestCase):
    def test_eight_different_methods_run_full_trajectory(self):
        report=journeys.run()
        self.assertEqual(report["case_count"],8)
        self.assertEqual(len(report["case_results"]),8)
        self.assertTrue(report["all_cases_preserve_human_gate"])
        self.assertEqual(report["real_human_judgments_collected"],0)
        self.assertFalse(report["independent_academic_validation"])
        self.assertFalse(report["seven_scientific_gates_modified"])
        self.assertFalse(report["actual_next_step_router_executed"])
        self.assertFalse(report["google_drive_synced"])
        self.assertEqual(len(set(report["route_coverage"])),8)
        for row in report["case_results"]:
            with self.subTest(route=row["research_route"]):
                self.assertEqual(len(row["events"]),8)
                self.assertTrue(row["exploration_verified"])
                self.assertEqual(len(row["compared_ids"]),2)
                self.assertTrue(row["unlisted_route_available"])
                self.assertFalse(row["gate_approved"])
                self.assertFalse(row["researcher_decision_saved"])
                self.assertFalse(row["researcher_decision_authenticated"])
                self.assertFalse(row["project_created_or_modified"])
                self.assertFalse(row["semantic_method_suitability_validated"])
                self.assertEqual(row["proposal"]["proposed_entry_status"],"NOT_WRITTEN")
                self.assertFalse(row["proposal"]["is_additional_canonical_field"])
                self.assertEqual(row["continuation"]["method_route_confirmation"],
                                 "PENDING_HUMAN_DECISION")
                self.assertTrue(row["continuation"]["requires_real_human_researcher_choice"])
                self.assertFalse(row["continuation"]["can_preapprove_gate_0002"])
                self.assertTrue(all(not e["scientific_gate_approved"] for e in row["events"]))
                self.assertTrue(all(not e["real_human_decision_obtained"] for e in row["events"]))

    def test_no_private_question_or_fixture_reasoning_is_exported(self):
        inputs=journeys.simulated_cases()
        outputs=json.dumps(journeys.run())
        for case in inputs:
            self.assertNotIn(case["question"],outputs)
            self.assertNotIn(case["rationale"],outputs)
            row=next(x for x in journeys.run()["case_results"] if x["case_id"]==case["id"])
            self.assertEqual(row["fictional_question_sha256"],
                hashlib.sha256(case["question"].encode()).hexdigest())

    def test_known_canonical_fields_and_noncanonical_dimensions_are_distinct(self):
        result=journeys.run()
        for case in result["case_results"]:
            if case["research_route"]=="MIXED_METHODS":
                self.assertEqual(case["proposal"]["target_existing_field"],"meta_inference_plan")
            if case["research_route"]=="DESIGN_SCIENCE":
                self.assertEqual(case["proposal"]["target_existing_field"],"evaluation_plan")
            self.assertIn(case["proposal"]["proposal_kind"],
                {"EXISTING_METHOD_PROFILE_FIELD_ONLY","EXPLORATION_WITHOUT_CANONICAL_FIELD"})

    def test_missing_fake_actor_cannot_be_accepted_as_real_decision(self):
        case=journeys.simulated_cases()[0]
        for actor in ("REAL_RESEARCHER","AGENT","",None):
            bad={**case,"actor_type":actor}
            with self.subTest(actor=actor):
                with self.assertRaisesRegex(ValueError,"fictional actors"):
                    journeys.fictional_case(bad)

    def test_unknown_methods_or_out_of_catalogue_choices_fail_closed(self):
        case=journeys.simulated_cases()[0]
        for diff in ({"route":"HISTORICAL_NOT_YET_MAPPED"},
                     {"choice_id":"INVENTED_OPTION"},
                     {"comparison_id":"INVENTED_OPTION"},
                     {"choice_id":case["comparison_id"]},
                     {"dimension":"future_fake_dimension"}):
            bad={**case,**diff}
            with self.subTest(diff=diff),self.assertRaises(ValueError):
                journeys.fictional_case(bad)

    def test_short_rationale_not_treated_as_scientific_approval(self):
        case=journeys.simulated_cases()[0]
        with self.assertRaisesRegex(ValueError,"rationale"):
            journeys.fictional_case({**case,"rationale":"Looks good"})
        with self.assertRaisesRegex(ValueError,"fabricated questions"):
            journeys.fictional_case({**case,"question":"Actual confidential research proposal with real people."})

    def test_causality_and_sampling_claims_cannot_be_auto_certified(self):
        report=journeys.run()
        for row in report["case_results"]:
            self.assertFalse(row["source_evidence_checked"])
            self.assertFalse(row["external_academic_data_accessed"])
            self.assertFalse(row["gate_approved"])
            self.assertFalse(row["researcher_decision_authenticated"])
            self.assertTrue(row["continuation"]["independent_method_validation_required_to_claim_accuracy"])
        self.assertEqual(report["real_human_judgments_collected"],0)

    def test_output_is_explicit_create_only_and_does_not_modify_existing_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            protected=root/"existing.json"
            protected.write_text("DO_NOT_OVERWRITE",encoding="utf-8")
            command=[sys.executable,str(ROOT/"scripts/simulate_research_journeys.py"),
                     "--output",str(protected)]
            failed=subprocess.run(command,capture_output=True,text=True)
            self.assertEqual(failed.returncode,2)
            self.assertEqual(protected.read_text(encoding="utf-8"),"DO_NOT_OVERWRITE")
            destination=root/"new-synthetic-report.json"
            successful=subprocess.run([*command[:-1],str(destination)],
                                      capture_output=True,text=True)
            self.assertEqual(successful.returncode,0,successful.stderr)
            out=json.loads(destination.read_text())
            self.assertEqual(out["case_count"],8)
            self.assertEqual(out["schema"],"MEU_ARTIGO_SYNTHETIC_JOURNEY_EVALUATION_V1")
            self.assertFalse(out["canonical_workspace_mutated"])
            self.assertFalse(out["independent_academic_validation"])

    def test_deterministic_and_no_external_provider_calls(self):
        self.assertEqual(journeys.run(),journeys.run())
        self.assertEqual(journeys.run()["case_results"][0]["fixture_label"],
                         "SYNTHETIC_AUTHOR_CONSTRUCTED_NOT_A_HUMAN_STUDY")
        self.assertTrue(journeys.run()["human_decision_is_only_a_simulated_fixture"])

if __name__=="__main__":
    unittest.main()
