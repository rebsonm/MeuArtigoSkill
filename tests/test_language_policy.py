"""Locale configuration and untranslated-source inventory: engineering tests only."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from language_config import normalized_tag, project_language_settings, settings_issues
from audit_source_language import audit


class AutomaticLanguageTests(unittest.TestCase):
    def test_default_is_auto_conversation_and_undecided_manuscript(self):
        self.assertEqual(project_language_settings(),{
            "interaction_language_mode":"AUTO",
            "interaction_language":"auto",
            "manuscript_language":"undecided",
        })

    def test_portuguese_is_not_a_required_installation_setting(self):
        # In automatic mode, direct messages drive model-side language choice.
        settings=project_language_settings()
        self.assertEqual(settings["interaction_language"],"auto")
        policy=(ROOT/"references/language-policy.md").read_text(encoding="utf-8")
        self.assertIn("latest **substantive direct message**",policy)
        self.assertIn("manuscript language",policy.lower())
        self.assertIn("Portuguese",policy)

    def test_explicit_conversation_and_independent_manuscript_choice(self):
        selected=project_language_settings("pt-br","en",explicitly_selected=True)
        self.assertEqual(selected["interaction_language"],"pt-BR")
        self.assertEqual(selected["interaction_language_mode"],"EXPLICIT")
        self.assertEqual(selected["manuscript_language"],"en")
        self.assertEqual(settings_issues(selected),[])

    def test_unconfirmed_fixed_language_is_rejected(self):
        with self.assertRaises(ValueError):
            project_language_settings("es")
        with self.assertRaises(ValueError):
            project_language_settings("../pt-BR",explicitly_selected=True)

    def test_legacy_workspace_does_not_require_new_language_fields(self):
        self.assertEqual(settings_issues({"project_name":"old"}),[])

    def test_auto_and_explicit_states_are_not_confusable(self):
        self.assertTrue(settings_issues({
            "interaction_language_mode":"AUTO",
            "interaction_language":"pt-BR",
            "manuscript_language":"undecided",
        }))

    def test_portuguese_document_is_detected_without_echoing_private_content(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/"docs").mkdir()
            (root/"docs/guide.md").write_text(
                "A pesquisa científica deve verificar a revisão e a análise. "
                "O pesquisador precisa documentar todas as fontes e resultados "
                "para a construção do projeto, conforme o processo e a metodologia.",
                encoding="utf-8",
            )
            result=audit(root)
            self.assertEqual(result["source_files_requiring_editorial_language_review"],1)
            self.assertFalse(result["all_source_translated_verified"])
            self.assertTrue(all("text" not in x for x in result["unresolved"]))

    def test_english_file_passes_conservative_signal_not_human_review(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/"guide.md").write_text(
                "A scientific research project must record original evidence, "
                "real human decisions and the journal's author instructions.",
                encoding="utf-8")
            report=audit(root)
            self.assertEqual(report["source_files_requiring_editorial_language_review"],0)
            self.assertFalse(report["all_source_translated_verified"])

    def test_entrypoint_and_adapter_treat_english_source_as_not_english_user(self):
        text=(ROOT/"SKILL.md").read_text(encoding="utf-8")
        adapter=(ROOT/"agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("references/language-policy.md",text)
        self.assertIn("conversation",text.lower())
        self.assertIn("respond to me in the language",adapter)


if __name__=="__main__":
    unittest.main()
