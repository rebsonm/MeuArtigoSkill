"""Security and method invariants for the fictional ChatGPT MCP Apps projection.

These are software checks, NOT user testing, research validation or hosting.
"""
from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mcp_preview_projection import fictional_projection
from method_routes import ROUTES

class McpPreviewProjectionTests(unittest.TestCase):
    def test_every_route_preserves_fictional_boundary(self):
        for route in ROUTES:
            with self.subTest(route=route):
                model = fictional_projection(route, "FULL")
                self.assertEqual(model["active_route"], route)
                self.assertFalse(model["is_project_bound"])
                self.assertEqual(model["snapshot_kind"], "FICTIONAL_PREVIEW_NOT_A_REAL_PROJECT")
                self.assertTrue(model["mcp_app"]["fictional_only"])
                self.assertFalse(model["mcp_app"]["real_project_access"])
                self.assertFalse(model["mcp_app"]["researcher_authenticated"])
                self.assertFalse(model["mcp_app"]["write_tools_available"])
                self.assertFalse(model["mcp_app"]["scientific_gate_approval_available"])
                self.assertFalse(model["overview"]["independent_scientific_validation"])
                self.assertFalse(model["overview"]["canonical_drive_sync_verified"])
                self.assertEqual(model["tasks"]["items"], [])
                self.assertEqual(model["human_gates"]["items"], [])
                self.assertIn("OTHER_NOT_LISTED",
                              [x["id"] for x in model["method_guides"]["overview"]["options"]])

    def test_invalid_inputs_and_paths_are_not_accepted(self):
        for route, mode in [("../data", "FULL"), ("QUALITATIVE", "WRITE"), ("", "MINIMAL")]:
            with self.subTest(route=route, mode=mode), self.assertRaises(ValueError):
                fictional_projection(route, mode)

    def test_cli_output_is_strictly_fictional(self):
        cmd = [sys.executable, "-I", str(ROOT / "scripts" / "mcp_preview_projection.py"),
               "--route", "QUALITATIVE", "--mode", "FULL"]
        run = subprocess.run(cmd, capture_output=True, text=True, check=True)
        projection = json.loads(run.stdout)
        self.assertFalse(projection["is_project_bound"])
        self.assertFalse(projection["mcp_app"]["write_tools_available"])
        bad = subprocess.run(cmd + ["/unauthorized/project"], capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)

    def test_widget_and_server_contain_no_canonical_write_tools(self):
        server = (ROOT/"mcp-preview"/"server.mjs").read_text(encoding="utf-8")
        html = (ROOT/"mcp-preview"/"widget.html").read_text(encoding="utf-8")
        self.assertIn('registerAppResource(', server)
        self.assertIn('registerAppTool(', server)
        self.assertEqual(server.count('registerAppTool('), 1)
        self.assertIn('ui/initialize', html)
        self.assertIn('ui/notifications/tool-result', html)
        self.assertIn('tools/call', html)
        self.assertNotIn('local_research_bridge', server)
        self.assertNotIn('commit_method_field', server)
        self.assertNotIn('innerHTML', html)

if __name__ == "__main__":
    unittest.main()
