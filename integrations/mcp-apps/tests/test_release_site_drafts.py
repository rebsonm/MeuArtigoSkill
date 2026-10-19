"""Prevent accidentally treating unapproved landing/legal pages as published."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

PAGES = Path(__file__).resolve().parents[1] / "deploy" / "site-drafts"
FILES = ("index.html", "suporte.html", "privacidade.html", "termos.html")


class PageElements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.lang = None
        self.title = False
        self.robots = None

    def handle_starttag(self, tag, attrs):
        kv = dict(attrs)
        if tag == "a" and "href" in kv:
            self.hrefs.append(kv["href"])
        if tag == "html":
            self.lang = kv.get("lang")
        if tag == "title":
            self.title = True
        if tag == "meta" and kv.get("name") == "robots":
            self.robots = kv.get("content")


class SiteDrafts(unittest.TestCase):
    def test_exact_four_static_pages_with_shared_accessible_navigation(self):
        for name in FILES:
            with self.subTest(name=name):
                page = (PAGES / name).read_text(encoding="utf-8")
                parser = PageElements()
                parser.feed(page)
                self.assertEqual(parser.lang, "pt-BR")
                self.assertTrue(parser.title)
                self.assertTrue(page.startswith("<!doctype html>"))
                self.assertIn('aria-label="Páginas"', page)
                self.assertIn('a:focus-visible', page)
                self.assertIn("viewport", page)
                for filename in FILES:
                    self.assertIn(filename, parser.hrefs)
                self.assertNotIn("<script", page.lower())
                self.assertNotIn("<iframe", page.lower())
                self.assertNotIn("<form", page.lower())

    def test_official_plugin_logo_and_blue_identity_are_shared_by_all_pages(self):
        # Reuse the original repository logo, not a newly generated or linked image.
        from pathlib import Path
        logo = (PAGES.parents[2] / "assets" / "icon.svg").read_text(encoding="utf-8")
        exact_logo = logo.replace(
            'role="img" aria-label="Meu Artigo"',
            'class="brand-icon" aria-hidden="true" focusable="false"'
        )
        for name in FILES:
            with self.subTest(name=name):
                page = (PAGES / name).read_text(encoding="utf-8")
                self.assertIn(exact_logo, page)
                self.assertIn('<span class="brand-name">Meu <strong>Artigo</strong></span>', page)
                self.assertIn('#0B57D0', page)
                self.assertIn('#2563EB', page)
                self.assertIn('background:#eaf2ff', page)
                self.assertNotIn('src="https://', page)
                self.assertNotIn('class="mark">MA', page)

    def test_unapproved_policy_pages_are_deliberately_not_publishable(self):
        for name in FILES:
            with self.subTest(name=name):
                page = (PAGES / name).read_text(encoding="utf-8")
                parser = PageElements()
                parser.feed(page)
                self.assertEqual(parser.robots, "noindex,nofollow")
                self.assertIn("Rascunho para revisão", page)
                self.assertIn("não aprovado", page)
                self.assertNotIn('name="google-site-verification"', page)
                self.assertNotIn("sk-proj-", page)
                self.assertNotIn("Authorization: Bearer ", page)
                self.assertNotIn("google-oauth2|", page)

    def test_privacy_and_terms_require_owner_approval(self):
        privacy = (PAGES / "privacidade.html").read_text(encoding="utf-8")
        terms = (PAGES / "termos.html").read_text(encoding="utf-8")
        support = (PAGES / "suporte.html").read_text(encoding="utf-8")
        product = (PAGES / "index.html").read_text(encoding="utf-8")
        self.assertIn("LGPD", privacy)
        self.assertIn("retenção", privacy)
        self.assertIn("Auth0", privacy)
        self.assertIn('mailto:rebsonm@gmail.com', support)
        self.assertIn('mailto:rebsonm@gmail.com', privacy)
        self.assertIn('mailto:rebsonm@gmail.com', terms)
        self.assertNotIn("[PREENCHER E VALIDAR", support)
        self.assertIn("bases legais", privacy.lower())
        self.assertIn("períodos de retenção", privacy)
        self.assertIn("direitos previstos no art. 18 da LGPD", privacy)
        for page in (support, privacy, terms, product):
            self.assertIn("Rebson de Morais Mendes", page)
        self.assertIn("pessoa física", privacy)
        self.assertIn("pessoa física", terms)
        self.assertIn("versão para revisão", terms)
        self.assertIn("legislação brasileira", terms)
        self.assertIn("piloto técnico restrito", product)
        self.assertIn("licença Apache License 2.0", terms)
        self.assertTrue((PAGES / "REVIEW-AND-VIDEO.md").exists())

if __name__ == "__main__":
    unittest.main()
