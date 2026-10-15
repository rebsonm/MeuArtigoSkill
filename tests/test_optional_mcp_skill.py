"""Synthetic contract checks for optional external MCP tool use by a Skill.

No real MCP connection, authentication or installed ChatGPT host is exercised.
"""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class OptionalMcpSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entry=(ROOT/"SKILL.md").read_text(encoding="utf-8")
        cls.rules=(ROOT/"references/mcp-tool-use.md").read_text(encoding="utf-8")
        cls.chat=(ROOT/"docs/CHATGPT.md").read_text(encoding="utf-8")
        cls.agent=(ROOT/"agents/openai.yaml").read_text(encoding="utf-8")

    def test_entrypoint_has_a_bundled_optional_tool_integration_contract(self):
        self.assertIn("[optional usage contract](references/mcp-tool-use.md)",
                      self.entry)
        self.assertLess(len(self.entry),15500)

    def test_mcp_is_not_required_to_install_or_use_scientific_core(self):
        for phrase in ("optional", "does not install", "does not",
                       "already-connected", "Graceful fallback",
                       "NOT_VERIFIED"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(),self.rules.lower())
        self.assertNotIn("dependencies:",self.agent)
        self.assertNotIn("MCP_NOT_CONNECTED",self.entry)
        self.assertFalse((ROOT/"mcp-preview").exists())
        self.assertFalse((ROOT/"mcp").exists())

    def test_tool_results_cannot_bypass_canonical_scientific_governance(self):
        for required in ("CONTINUIDADE.md","DEC/TRACE",
                         "C.A.D.A.","seven human gates",
                         "actual tools", "authorized project",
                         "researcher decision", "out of scope",
                         "NOT_VERIFIED", "WORK_FALLBACK"):
            with self.subTest(required=required):
                self.assertIn(required.lower(),self.rules.lower())

    def test_mcp_apps_ui_is_not_claimed_to_be_a_skill_only_feature(self):
        self.assertIn("separate host",self.rules)
        self.assertIn("does **not** activate MCP Apps UI",self.rules)
        self.assertIn("when its Skill ZIP is installed",self.chat)

    def test_real_host_acceptance_keeps_evidence_levels_separate(self):
        record=(ROOT/"docs/CHATGPT-MCP-HOST-ACCEPTANCE.md").read_text(encoding="utf-8")
        for phrase in ("0.9.0-beta.4","HOST-2: Same-session workflow",
                       "HOST-3: New Skill candidate",
                       "HOST-4: Own MCP tool call",
                       "HOST-5: MCP Apps visualization",
                       "NOT_VERIFIED",
                       "operator-observed smoke check",
                       "tool origin cannot be independently attributed"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(),record.lower())
        self.assertIn("real-host acceptance record",self.rules)
        self.assertIn("does **not** certify",self.rules)
        self.assertNotIn("MCP Apps visualization | OBSERVED",record)

    def test_fallback_is_explicit_and_does_not_simulate_connected_tool(self):
        self.assertIn("No exposed MCP tool means",self.rules)
        self.assertIn("authorized native tool",self.rules)
        self.assertIn("If no MCP connection is available",self.chat)
        self.assertIn("continue as a normal Skill",self.chat)

if __name__ == "__main__":
    unittest.main()
