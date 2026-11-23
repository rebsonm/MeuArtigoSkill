"""Protect the RC.4 plugin-only boundary and internal scientific governance.

A plugin is now the *intended* distribution; do not reintroduce servers,
secret-carrying tools, multiple installers or a separate visual app.
"""
from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]

class PublicPluginBoundaryTests(unittest.TestCase):
    def test_single_plugin_source_and_internal_skill(self):
        manifest=json.loads((ROOT/"plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"],"meu-artigo")
        self.assertEqual(manifest["version"],"1.0.0-rc.4")
        self.assertTrue((ROOT/"SKILL.md").is_file())
        self.assertTrue((ROOT/"scripts/build_plugin_bundle.py").is_file())
        self.assertFalse((ROOT/"visual-app").exists())
        self.assertFalse((ROOT/"plugin").exists())
        self.assertFalse((ROOT/"mcp.json").exists())
        self.assertFalse((ROOT/"mcp").exists())

    def test_no_second_rc4_skill_distribution_or_external_server(self):
        readme=(ROOT/"README.md").read_text(encoding="utf-8")
        ci=(ROOT/".github/workflows/release-audit.yml").read_text(encoding="utf-8")
        builder=(ROOT/"scripts/build_plugin_bundle.py").read_text(encoding="utf-8")
        self.assertIn("plugin-only",readme.lower())
        self.assertIn("steps.rc.outputs.plugin_only != 'true'",ci)
        self.assertIn("MeuArtigoPlugin-v",builder)
        self.assertIn("RC4_LOGO_PENDING",builder)
        self.assertIn("THIRD_PARTY_PDF_OR_SECRET_NOT_ALLOWED",builder)
        self.assertNotIn("/releases/download/v1.0.0-rc.4/MeuArtigoSkill-",readme)
        self.assertNotIn("mcpServers",json.dumps(json.loads((ROOT/"plugin.json").read_text())))

    def test_scientific_human_controls_remain(self):
        source=(ROOT/"SKILL.md").read_text(encoding="utf-8")
        for token in ("GATE_ID","DEC_ID","SNAP_ID","GOOGLE_DRIVE_FIRST",
                      "WORK_FALLBACK","Counter_Evidence_IDs","[L]","[I]","[P]"):
            self.assertIn(token,source)

if __name__=="__main__":
    unittest.main()
