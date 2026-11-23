"""Static contract checks for four-choice research decision guidance.

These tests confirm repository instructions, not live host widgets, model
compliance, usability improvement, scientific quality or Drive operations.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FourChoiceDecisionGuidanceTests(unittest.TestCase):
    def test_skill_loads_central_decision_policy(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/decision-navigation.md", skill)
        self.assertIn("three alternatives", skill.lower())
        self.assertIn("free-text", skill.lower())
        self.assertIn("native radio button", skill.lower())
        self.assertIn("D radio", skill)
        self.assertIn("gate", skill.lower())

    def test_guidance_preserves_four_options_and_human_review(self):
        doc = (ROOT / "references/decision-navigation.md").read_text(encoding="utf-8")
        for required in (
            "exactly three", "A, B, C", "Pros", "Cons",
            "Recommended", "D — Other", "open text field",
            "native interaction controls", "plain Markdown",
            "researcher's own rationale", "PENDING",
            "one", "not adopting it", "MINIMAL/FULL",
            "single-select radio button immediately before each option",
            "D is the **fourth radio option**",
            "never **automatically** changes",
        ):
            with self.subTest(phrase=required):
                self.assertIn(required, doc)
        self.assertIn("do not invent unsafe alternatives", doc.lower())
        self.assertIn("Typing a non-empty answer in the D field automatically selects", doc)
        self.assertIn("never submit on radio selection", doc.lower())
        self.assertIn("not a default selection", doc)
        self.assertIn("plain-chat choice", doc)
        self.assertIn("real editable free-text field immediately beneath D", doc)
        self.assertIn("Never hide, disable or require clicking D", doc)
        self.assertIn("Submit answer", doc)
        self.assertIn("disabled until a valid choice exists", doc)
        self.assertIn("whitespace-only D text", doc)
        self.assertIn("exact written proposal", doc)
        self.assertIn("never **automatically** changes", doc)

    def test_host_help_explains_fallback_and_limits(self):
        chatgpt = (ROOT / "docs/CHATGPT.md").read_text(encoding="utf-8")
        self.assertIn("Option D", chatgpt)
        self.assertIn("type", chatgpt)
        self.assertIn("not approve", chatgpt)
        self.assertIn("native", chatgpt)
        self.assertIn("four clickable radio buttons", chatgpt)
        self.assertIn("always-visible, enabled text field", chatgpt)
        self.assertIn("typing automatically selects D", chatgpt)
        self.assertIn("Submit answer", chatgpt)
        self.assertIn("does not send anything until", chatgpt)
        self.assertIn("no option should", chatgpt.lower())


if __name__ == "__main__":
    unittest.main()
