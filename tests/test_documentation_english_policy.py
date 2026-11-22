"""Check English-only editorial documentation without altering original citations.

This is a conservative structural test, not a machine translation validator.
"""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_source_language import PORTUGUESE_WORDS, audit

CREDITS = Path("knowledge/methodology/PDF-ATTRIBUTIONS.md")
DOCS = (
    "references/capability-onboarding.md",
    "references/bibliographic-connectors.md",
    "docs/COMPROVACAO-EVENTOS.md",
    "docs/EXPORTACAO-SEGURA.md",
    "docs/VALIDACAO-FORMATIVA.md",
    "docs/SCREENING-AUDITAVEL.md",
)


class EnglishDocumentationPolicyTests(unittest.TestCase):
    def test_pdf_attribution_editorial_text_is_english(self):
        content = (ROOT / CREDITS).read_text(encoding="utf-8")
        rows = [line for line in content.splitlines()
                if line.startswith("| ") and line.split("|")[1].strip().isdigit()]
        self.assertEqual(len(rows), 51)
        editorial = "\n".join(
            line for line in content.splitlines() if not line.lstrip().startswith("|")
        )
        self.assertEqual(PORTUGUESE_WORDS.findall(editorial), [])
        self.assertIn("Third-party academic PDF credits", editorial)
        self.assertIn("Attribution and reuse conditions", editorial)
        self.assertIn("CC BY (version unspecified)", editorial)

    def test_language_audit_does_not_hide_portuguese_editorial_prose(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / CREDITS
            path.parent.mkdir(parents=True)
            # Source title in Portuguese is legitimate original metadata.
            table = ("| # | Original title |\n|---:|---|\n"
                     "| 1 | Pesquisa científica: revisão de metodologia e fontes |\n")
            path.write_text(
                "# English attribution register\n\n"
                "Esta documentação apresenta pesquisa científica e revisão "
                "de metodologia. O pesquisador não deve aprovar a publicação "
                "sem verificação das fontes e autorização.\n\n"
                + table, encoding="utf-8")
            result = audit(Path(temp))
            self.assertIn(CREDITS.as_posix(),
                          [item["path"] for item in result["unresolved"]])
            path.write_text(
                "# English attribution register\n\n"
                "Original authors retain their licensing rights.\n\n"
                + table, encoding="utf-8")
            self.assertEqual(audit(Path(temp))["unresolved"], [])

    def test_instruction_examples_do_not_reintroduce_portuguese(self):
        for item in DOCS:
            with self.subTest(document=item):
                content = (ROOT / item).read_text(encoding="utf-8")
                for outdated in (
                    "Conferir fontes", "Busca na base pendente de comprovação",
                    "Para não presumir capacidades", "Pesquisador\"",
                    "Identificação real do revisor autorizado",
                ):
                    self.assertNotIn(outdated, content)


if __name__ == "__main__":
    unittest.main()
