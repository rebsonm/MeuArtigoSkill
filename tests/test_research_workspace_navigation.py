"""Portable UI contract tests: no network, no real article, no approvals."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_research_workspace as workspace


class ScanUI(HTMLParser):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.sections = []
        self.areas = []
        self.nav_labels = []
        self.in_nav = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "nav" and a.get("class") == "ux-nav":
            self.in_nav = True
        if tag == "button" and "data-ux-button" in a:
            self.buttons.append(a)
        if tag == "section" and "data-ux-view" in a:
            self.sections.append(a)
        if tag == "textarea":
            self.areas.append(a)

    def handle_endtag(self, tag):
        if tag == "nav":
            self.in_nav = False


class ResearchUXNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = workspace.model(route="QUALITATIVE")
        cls.html = workspace.render(cls.model)
        cls.ui = ScanUI()
        cls.ui.feed(cls.html)

    def test_user_can_choose_four_focused_views_or_show_all(self):
        names = [b["data-ux-button"] for b in self.ui.buttons]
        self.assertEqual(names, ["overview", "methods", "draft", "tasks", "all"])
        self.assertEqual(self.ui.buttons[0]["aria-pressed"], "true")
        self.assertTrue(all(b["type"] == "button" for b in self.ui.buttons))

    def test_all_existing_research_sections_still_present(self):
        ids = {s["aria-labelledby"] for s in self.ui.sections}
        self.assertEqual(ids, {"study-title", "choices-title", "draft-title",
                               "continuity-title", "task-title", "guard-title"})

    def test_section_filter_is_presentation_only(self):
        self.assertIn('data-focus="overview"', self.html)
        self.assertIn('aria-pressed', self.html)
        self.assertIn("function chooseView", self.html)
        self.assertIn('data-ux-view="methods"', self.html)
        self.assertIn(".grid[data-focus]:not", self.html)

    def test_continuation_is_read_only_not_sent_to_server(self):
        area = [a for a in self.ui.areas if a.get("id") == "continuation-prompt"]
        self.assertEqual(len(area), 1)
        self.assertIn("readonly", area[0])
        start = self.html.index('$("prepare-continuation").addEventListener')
        end = self.html.index(" renderStatic();renderOptions();", start)
        handler = self.html[start:end]
        self.assertIn("action.code", handler)
        self.assertIn("area.select()", handler)
        for risky in ('bridgeRequest(', 'fetch(', 'post(', 'send(', 'model.tasks.items',
                      'localStorage', 'sessionStorage', 'navigator.clipboard'):
            self.assertNotIn(risky, handler)

    def test_no_automatic_scientific_approval_or_cloud_sync_claims(self):
        self.assertIn("Nenhum botão nesta tela salva decisões", self.html)
        self.assertIn("Sincronização Drive não verificada", self.html)
        self.assertNotIn('data-ux-button="approve"', self.html)
        self.assertFalse(self.model["permissions"]["canonical_write"])
        self.assertEqual(self.model["permissions"]["human_scientific_approval"],
                         "NOT_AVAILABLE_IN_THIS_UI")

    def test_cada_four_columns_unchanged(self):
        self.assertIn('<th>ID Tarefa</th><th>Tarefa</th><th>Responsável execução</th><th>Prazo</th>', self.html)

    def test_static_preview_contains_no_bridge_secrets(self):
        self.assertNotIn("session_token", json.dumps(self.model))
        self.assertNotIn("__RESEARCH_WORKSPACE_MODEL_JSON__", self.html)
        self.assertIn("connect-src 'none'", self.html)

    def test_missing_project_remains_clearly_fictional(self):
        self.assertFalse(self.model["is_project_bound"])
        self.assertIn("Demonstração fictícia", self.html)


if __name__ == "__main__":
    unittest.main()
