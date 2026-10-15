"""Acceptance guard for combined PR #67/#68/#69 without live services.

All project data and human declarations are fictional and disposable.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from homologate_integrated_skill import run, NAMES, EXPECTED

class IntegratedAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=run()

    def test_all_expected_end_to_end_scenarios_are_exercised(self):
        r=self.report
        self.assertEqual(r["schema"],"MEU_ARTIGO_INTEGRATED_SKILL_ACCEPTANCE_V1")
        self.assertEqual(r["case_count"],11)
        self.assertEqual({x["case"] for x in r["results"]},set(NAMES))
        self.assertEqual(set(EXPECTED),set(NAMES))
        self.assertTrue(r["all_scenarios_passed"])
        for row in r["results"]:
            with self.subTest(case=row["case"]):
                self.assertEqual(row["result"],"PASS")
                self.assertTrue(row["read_only_project_unchanged"])
                self.assertFalse(row["private_prose_exported"])
                self.assertFalse(row["scientific_approval"])
                self.assertFalse(row["cloud_sync_verified"])

    def test_acceptance_report_never_claims_host_mcp_or_cloud_coverage(self):
        r=self.report
        self.assertEqual(r["acceptance_kind"],"SYNTHETIC_LOCAL_INTEGRATION_ONLY")
        self.assertTrue(r["optional_mcp_instruction_contract_checked"])
        for key in (
            "host_mcp_connection_exercised",
            "project_owned_mcp_server_connected",
            "mcp_apps_ui_verified",
            "updated_skill_installed_in_chatgpt",
            "real_drive_access_or_sync_verified",
            "independent_scientific_validation",
            "original_user_projects_accessed",
            "original_user_projects_modified",
        ):
            with self.subTest(key=key):
                self.assertFalse(r[key])
        for key in (
            "all_cases_without_scientific_approval",
            "all_cases_without_canonical_writes",
            "all_cases_without_private_prose_export",
        ):
            self.assertTrue(r[key])
        serialized=json.dumps(r,ensure_ascii=False)
        self.assertNotIn("SYNTHETIC_PRIVATE_RESEARCH_CONTENT_NEVER_EXPOSE_9861",serialized)
        self.assertNotIn("/tmp/",serialized)
        self.assertNotIn("127.0.0.1",serialized)

    def test_generated_report_is_not_a_new_research_project_or_publication(self):
        script=(ROOT/"scripts/homologate_integrated_skill.py").read_text(encoding="utf-8")
        self.assertIn("tempfile.TemporaryDirectory",script)
        self.assertIn("no live MCP",script.lower().replace("mcp","MCP").replace("NO","no"))
        self.assertNotIn("requests.post",script)
        self.assertNotIn("serve_forever",script)
        self.assertNotIn("http.client",script)

if __name__=="__main__":
    unittest.main()
