"""Official blue branding regression for the optional read-only HTML workspace."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "assets" / "research_workspace.html"
LOGO = ROOT / "assets" / "icon.svg"


class ResearchWorkspaceBrandTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = HTML.read_text(encoding="utf-8")
        cls.logo = LOGO.read_text(encoding="utf-8")

    def test_embeds_original_repository_logo_artwork(self):
        # The title and colors must not be represented by a generic MA avatar.
        expected = self.logo.replace(
            'role="img" aria-label="Meu Artigo"',
            'aria-hidden="true" focusable="false" class="brand-icon"')
        self.assertIn(expected, self.html)
        self.assertIn('class="brand-title">Meu <strong>Artigo</strong>', self.html)
        self.assertNotIn('class="mark">MA</span>', self.html)

    def test_brand_palette_matches_canonical_logo(self):
        self.assertIn("#0B57D0", self.logo)
        self.assertIn("#2563EB", self.logo)
        self.assertIn("--brand:#0B57D0", self.html)
        self.assertIn("--pale:#eaf2ff", self.html)
        self.assertIn("background:#fff;color:var(--ink)", self.html)

    def test_no_remote_image_or_network_permission_added(self):
        self.assertIn("connect-src 'none'", self.html)
        self.assertIn("img-src 'none'", self.html)
        self.assertIn("object-src 'none'", self.html)
        self.assertNotIn('src="https://', self.html)

    def test_existing_read_only_research_controls_survive(self):
        for element in ('id="dimension"', 'id="draft"', 'id="review-draft"',
                        'id="cada-rows"', 'id="blockers"', 'id="refresh-view"',
                        'data-ux-button="overview"', 'data-ux-button="methods"',
                        'data-ux-button="tasks"'):
            with self.subTest(element=element):
                self.assertIn(element, self.html)
        self.assertIn("Nenhum botão nesta tela salva decisões", self.html)


if __name__ == "__main__":
    unittest.main()
