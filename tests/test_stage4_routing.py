"""Static engineering regression for progressive skill routing, not a user study."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


class Stage4RouterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill=(ROOT/"SKILL.md").read_text(encoding="utf-8")
        cls.foundation=(ROOT/"references/methodological-foundations.md").read_text(encoding="utf-8")
        cls.index=(ROOT/"references/INDICE-METODOLOGICO.md").read_text(encoding="utf-8")
        cls.context=(ROOT/"references/CONTEXTO-POR-ETAPA.md").read_text(encoding="utf-8")
        cls.platform=(ROOT/"references/platform-capability-preflight.md").read_text(encoding="utf-8")

    def test_entrypoint_is_compact_and_route_first(self):
        self.assertLess(len(self.skill), 13000)
        self.assertIn("references/CONTEXTO-POR-ETAPA.md", self.skill)
        self.assertIn("references/INDICE-METODOLOGICO.md", self.skill)
        self.assertIn("references/fluxo-essencial.md", self.skill)
        self.assertIn("docs/ROTAS-METODOLOGICAS.md", self.skill)

    def test_safeguards_remain_in_entrypoint(self):
        for expected in (
            "GOOGLE_DRIVE_FIRST", "WORK_FALLBACK", "CONTINUIDADE.md",
            "JOURNAL_PROFILE.json", "ANONYMIZATION_PROFILE.json",
            "ZERO_NONESSENTIAL_METADATA", "UNVERIFIED",
            "Counter_Evidence_IDs", "Robustness_status",
            "W3C PROV", "RO-Crate", "GATE_ID", "DEC_ID",
            "SNAP_ID", "audit_anonymization.py",
            "sanitize_metadata.py", "Grounded Corpus", "Corpus Map",
            "[L]", "[I]", "[P]", "EMPIRICAL_RESULT",
        ):
            with self.subTest(safeguard=expected):
                self.assertIn(expected, self.skill)

    def test_original_methodology_and_bibliography_preserved(self):
        for old_section in (
            "## 1. Famílias de revisão",
            "## 3. Coerência do desenho",
            "## 4. Pesquisa qualitativa",
            "## 5. Pesquisa com artefatos",
            "## 10. Referências bibliográficas selecionadas",
            "https://doi.org/10.1111/joms.12582",
            "https://doi.org/10.1111/joms.12581",
        ):
            with self.subTest(section=old_section):
                self.assertIn(old_section, self.foundation)
        self.assertIn("identificação bibliográfica", self.index)
        self.assertIn("metadados", self.index)
        self.assertIn("não", self.index)

    def test_progressive_mode_does_not_disable_scientific_controls(self):
        self.assertIn("não",self.context.lower())
        self.assertIn("MINIMAL",self.context)
        self.assertIn("FULL",self.context)
        self.assertIn("CONTINUIDADE.md",self.context)
        mode=(ROOT/"docs/MODO-NUCLEO-MINIMO.md").read_text(encoding="utf-8")
        self.assertIn("não elimina registros",mode.lower())
        self.assertIn("CONTEXTO-POR-ETAPA.md",mode)

    def test_platform_capability_not_claimed_as_real_execution(self):
        for key in ("ChatGPT", "Claude", "Gemini", "UNVERIFIED",
                    "AVAILABLE_VERIFIED", "AVAILABLE_NOT_TESTED",
                    "WORK_FALLBACK"):
            with self.subTest(key=key):
                self.assertIn(key,self.platform)
        compat=(ROOT/"docs/COMPATIBILIDADE-PLATAFORMAS.md").read_text(encoding="utf-8")
        self.assertIn("PENDENTE",compat)
        self.assertIn("platform-capability-preflight.md",compat)

    def test_beginner_routing_is_not_universal_review_flow(self):
        beginner=(ROOT/"references/beginner-mode.md").read_text(encoding="utf-8")
        self.assertIn("fluxo-essencial.md",beginner)
        self.assertIn("quantitativo",beginner)
        self.assertIn("MINIMAL",beginner)
        self.assertIn("UNDECIDED",beginner)


if __name__=="__main__":
    unittest.main()
