"""Small multilingual metadata-discovery smoke tests, not a semantic relevance study.

Fixtures express known topic-to-document mappings only; passing them cannot
establish scientific quality, human source interpretation, host availability,
copyright clearance or independent effectiveness with real researchers.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import consult_github_methodology as cards
import public_method_pdf as pdfs


class MultilingualMethodologyDiscoverySmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards = cards._catalog((ROOT / cards.INDEX_PATH).read_bytes())
        cls.pdfs = pdfs.metadata((ROOT / pdfs.CATALOG).read_bytes())

    def ranked_cards(self, question):
        return [doc["path"].split("/")[-1]
                for s, doc in sorted(
                    ((cards._relevance(question, doc), doc) for doc in self.cards),
                    key=lambda row: (-row[0], row[1]["path"]))
                if s > 0]

    def ranked_pdfs(self, question):
        return [doc["path"].split("/")[-1]
                for s, doc in sorted(
                    ((pdfs._score(question, doc), doc) for doc in self.pdfs),
                    key=lambda row: (-row[0], row[1]["path"]))
                if s > 0]

    def test_targeted_multilingual_metadata_discovery(self):
        cases = [
            ("séries temporais interrompidas", "interrupted-time-series-inference.md",
             "lopez-bernal-cummins-gasparrini-2017.pdf"),
            ("métodos mistos triangulação integração", "mixed-methods-integration.md",
             "paranhos-et-al-2016.pdf"),
            ("estudo de caso organizacional", "case-study-bounded-design.md",
             "harrison-birks-franklin-mills-2017.pdf"),
            ("reprodutibilidade computacional", "reproducible-computational-workflow.md",
             "sandve-et-al-2013-reproducible-research.pdf"),
            ("metanálise quantitativa heterogeneidade", "meta-analysis-design-and-reporting.md",
             "forero-et-al-2019-meta-analysis.pdf"),
            ("escrita artigo científico estrutura", "manuscript-argument-structure.md",
             "mensh-kording-2017-paper-structure.pdf"),
            ("saturação entrevistas qualitativas", "thematic-saturation.md",
             "guest-namey-chen-2020-saturation.pdf"),
            ("bibliometria análise de citações", "bibliometrics-claim-boundary.md",
             "maia-bezerra-2020.pdf"),
            ("what is grounded theory", "grounded-theory-analytic-logic.md",
             "prigol-behrens-2019.pdf"),
        ]
        for question, card, pdf in cases:
            with self.subTest(question=question):
                self.assertIn(card, self.ranked_cards(question)[:2])
                self.assertEqual(self.ranked_pdfs(question)[0], pdf)

    def test_protected_scope_and_unrelated_questions_are_no_match(self):
        for question in (
                "causal inference regression discontinuity",
                "modelagem de equações estruturais",
                "how do volcanoes cause earthquakes",
        ):
            with self.subTest(question=question):
                self.assertFalse(self.ranked_cards(question))
                self.assertFalse(self.ranked_pdfs(question))

    def test_specific_review_card_beats_generic_content_analysis(self):
        cards_top = self.ranked_cards("revisão sistemática PRISMA transparência")
        self.assertEqual(cards_top[0], "prisma-2020-reporting.md")
        self.assertEqual(self.ranked_pdfs("análise temática reflexiva"), [])
        self.assertIn("reflexive-thematic-analysis.md",
                      self.ranked_cards("análise temática reflexiva")[:2])


if __name__ == "__main__":
    unittest.main()
