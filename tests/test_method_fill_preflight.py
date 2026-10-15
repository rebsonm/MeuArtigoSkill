"""Preventive, synthetic and non-mutating methodological entry preflight tests.

These only test structural software rules. No scientific appropriateness,
researcher authentication, consent or empirical validity is established.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from method_routes import new_profile, REQUIRED_DESIGN
import method_fill_preflight as fill
import native_chat_dashboard as dashboard

class MethodFillPreflightTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.m=self.root/"00_Gestao_e_Continuidade"
        self.m.mkdir()
        (self.m/"CONTINUIDADE.md").write_text("# Fictional project - not a human gate approval\n")
        self.configure("QUALITATIVE")

    def configure(self,route):
        (self.m/"PROJECT_CONFIG.json").write_text(
            json.dumps({"method_route":route,"presentation_mode":"MINIMAL",
                       "method_route_governance_required":True,"storage_mode":"GOOGLE_DRIVE"}))
        (self.m/"METHOD_PROFILE.json").write_text(json.dumps(new_profile(route)))

    def inspect(self,text=None,*,field=None,dimension=None,option=None):
        return fill.for_existing_project(self.root,field=field,dimension=dimension,
                                         proposal=text,option_id=option)

    def test_initial_guide_explains_fields_without_inventing_content(self):
        report=self.inspect()
        self.assertEqual(report["status"],"GUIDANCE_ONLY_NO_DRAFT")
        self.assertEqual(report["target_field"],"tradition")
        self.assertFalse(report["proposed_draft_supplied"])
        self.assertIsNone(report["proposed_draft_sha256"])
        self.assertEqual(report["blocking_finding_count"],0)
        self.assertFalse(report["safe_to_write_automatically"])
        self.assertFalse(report["researcher_choice_authenticated"])
        self.assertTrue(report["human_action"]["required_to_accept_or_reject_proposal"])
        self.assertGreater(len(report["suggested_entry_elements"]),2)

    def test_substantive_proposal_awaits_human_and_is_never_echoed(self):
        draft="The researcher is considering a qualitative case-study design, bounded to one fictional institution, with no inference of population prevalence."
        before={p.name:p.read_bytes() for p in self.m.iterdir()}
        res=self.inspect(draft,field="tradition",option="CASE_STUDY")
        self.assertEqual(res["status"],"DRAFT_REQUIRES_HUMAN_REVIEW")
        self.assertFalse(res["scientific_gate_approved"])
        self.assertFalse(res["semantic_suitability_verified"])
        self.assertFalse(res["draft_text_persisted"])
        self.assertFalse(res["safe_to_write_automatically"])
        self.assertEqual(res["proposed_draft_sha256"],hashlib.sha256(draft.encode()).hexdigest())
        self.assertNotIn(draft,json.dumps(res))
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.m.iterdir()})

    def test_placeholder_workflow_tokens_are_blocked_before_any_write(self):
        for token in ("PENDING","NOT_EXECUTED","PENDING_HUMAN_DECISION",
                      "APPROVED","N/A","a definir","null",""):
            with self.subTest(token=token):
                res=self.inspect(token,field="sampling_logic")
                self.assertEqual(res["status"],"BLOCKED_BEFORE_WRITING")
                self.assertIn("PLACEHOLDER_NOT_EVIDENCE",
                              {f["code"] for f in res["findings"]})
                self.assertFalse(res["safe_to_write_automatically"])

    def test_mixed_and_quant_enum_constraints_use_canonical_vocabulary(self):
        self.configure("QUANTITATIVE")
        wrong=self.inspect("CAUSALLY PROVEN",field="inference_aim")
        self.assertIn("INVALID_CANONICAL_ENUM",{x["code"] for x in wrong["findings"]})
        correct=self.inspect("ASSOCIATIONAL",field="inference_aim")
        self.assertEqual(correct["status"],"DRAFT_REQUIRES_HUMAN_REVIEW")
        self.assertFalse(correct["scientific_gate_approved"])
        self.configure("MIXED_METHODS")
        wrong=self.inspect("PENDING",field="integration_type")
        self.assertIn("PLACEHOLDER_NOT_EVIDENCE",{x["code"] for x in wrong["findings"]})
        correct=self.inspect("MERGING",field="integration_type")
        self.assertEqual(correct["status"],"DRAFT_REQUIRES_HUMAN_REVIEW")
        self.assertEqual(set(correct["field_specific_constraints"]),
                         {"CONNECTING","BUILDING","MERGING","EMBEDDING"})

    def test_wrong_field_or_option_never_adopted(self):
        with self.assertRaises(ValueError):
            self.inspect("A justified fictional choice.",field="analysis_plan")
        with self.assertRaisesRegex(ValueError,"Option"):
            self.inspect("A justified fictional choice.",field="sampling_logic",
                         option="PROBABILITY")
        with self.assertRaisesRegex(ValueError,"either"):
            self.inspect("A justified fictional choice.",field="sampling_logic",
                         dimension="sampling")

    def test_existing_decision_cannot_be_overwritten_from_assistant(self):
        doc=json.loads((self.m/"METHOD_PROFILE.json").read_text())
        doc["route_details"]["analysis_logic"]="A pre-existing human-authored method"
        (self.m/"METHOD_PROFILE.json").write_text(json.dumps(doc))
        res=self.inspect("A different new explanation of thematic coding.",
                         field="analysis_logic")
        self.assertEqual(res["status"],"BLOCKED_BEFORE_WRITING")
        self.assertIn("EXISTING_DECISION_REQUIRES_REVIEW",
                      {x["code"] for x in res["findings"]})
        self.assertEqual(json.loads((self.m/"METHOD_PROFILE.json").read_text()),doc)

    def test_exploratory_reporting_has_no_unofficial_project_field(self):
        self.configure("CONCEPTUAL_THEORY")
        res=self.inspect("A proposed conceptual argument map with claims and objections.",
                         dimension="reporting")
        self.assertEqual(res["status"],"BLOCKED_BEFORE_WRITING")
        self.assertFalse(res["entry_has_existing_canonical_field"])
        self.assertIn("NO_CANONICAL_FIELD",{x["code"] for x in res["findings"]})
        res=self.inspect("Sampling 20 participants.",dimension="sampling")
        self.assertIn("GUIDANCE_NOT_READY",{x["code"] for x in res["findings"]})

    def test_unlisted_method_blocks_automatic_mapping_but_keeps_open_option(self):
        res=self.inspect("Fictional archival methodology using historical source critique.",
                         option="OTHER_NOT_LISTED")
        self.assertEqual(res["status"],"BLOCKED_BEFORE_WRITING")
        self.assertIn("UNLISTED_METHOD_NEEDS_MAPPING",{x["code"] for x in res["findings"]})
        self.assertTrue(res["human_action"]["required_to_authorize_any_real_change"])

    def test_uncorroborated_success_words_only_flag_advisory(self):
        res=self.inspect(
            "The artifact has been validated scientifically and is 100% reliable.",
            field="analysis_logic")
        self.assertEqual(res["status"],"DRAFT_REQUIRES_HUMAN_REVIEW")
        self.assertIn("ASSERTED_VALIDATION_NEEDS_EVIDENCE",
                      {x["code"] for x in res["findings"]})
        self.assertFalse(res["source_evidence_checked"])
        self.assertFalse(res["semantic_suitability_verified"])

    def test_invalid_profile_is_refused_without_reconstruction(self):
        cfg=json.loads((self.m/"PROJECT_CONFIG.json").read_text())
        cfg["method_route"]="DESIGN_SCIENCE"
        (self.m/"PROJECT_CONFIG.json").write_text(json.dumps(cfg))
        res=self.inspect("A fictional proposed evaluation approach.")
        self.assertIn("GUIDANCE_NOT_READY",{x["code"] for x in res["findings"]})
        self.assertEqual(res["status"],"BLOCKED_BEFORE_WRITING")
        self.assertFalse(res["canonical_project_modified"])

    def test_native_dashboard_includes_safeguarded_field_guidance(self):
        panel=dashboard.panel(self.root)
        guidance=panel["method_fill_guidance"]
        self.assertEqual(guidance["status"],"GUIDANCE_ONLY_NO_DRAFT")
        self.assertFalse(guidance["safe_to_write_automatically"])
        self.assertFalse(guidance["scientific_gate_approved"])
        self.assertIn("Method entry:",dashboard.fallback(panel))

    def test_script_handles_private_draft_without_echo_or_writes(self):
        draft="RESEARCHER_PRIVATE_METHOD_TEXT_65192 explaining the fictional methodological design in considerable detail."
        filename=self.root/"private-draft.txt"
        filename.write_text(draft,encoding="utf-8")
        snapshot={p.name:p.read_bytes() for p in self.m.iterdir()}
        command=[sys.executable,str(ROOT/"scripts/method_fill_preflight.py"),str(self.root),
                 "--field","analysis_logic","--draft-file",str(filename)]
        result=subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        payload=json.loads(result.stdout)
        self.assertNotIn(draft,result.stdout)
        self.assertNotIn(draft,result.stderr)
        self.assertEqual(payload["proposed_draft_sha256"],hashlib.sha256(draft.encode()).hexdigest())
        self.assertEqual(snapshot,{p.name:p.read_bytes() for p in self.m.iterdir()})
        filename.write_text("PENDING")
        rejected=subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(rejected.returncode,2)
        self.assertEqual(json.loads(rejected.stdout)["status"],"BLOCKED_BEFORE_WRITING")
        self.assertNotIn("PENDING",rejected.stderr)

    def test_oversize_and_binary_draft_fail_without_private_echo(self):
        too_large=self.root/"overlong.txt"
        too_large.write_text("a"* (fill.LIMIT_BYTES+1))
        with self.assertRaisesRegex(ValueError,"size"):
            fill._read_draft(too_large)
        bad=self.root/"binary.txt"
        bad.write_bytes(b"\xff\xff")
        with self.assertRaises(UnicodeDecodeError):
            fill._read_draft(bad)

    def test_non_empty_short_statement_is_caution_not_false_certification(self):
        res=self.inspect("Interviews",field="material_sources")
        self.assertEqual(res["status"],"DRAFT_REQUIRES_HUMAN_REVIEW")
        self.assertIn("BRIEF_DRAFT_NEEDS_EXPLANATION",
                      {x["code"] for x in res["findings"]})
        self.assertFalse(res["safe_to_write_automatically"])

if __name__=="__main__":
    unittest.main()
