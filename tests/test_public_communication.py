"""Public presentation regression checks.

Technical internals belong in developer docs and source, not in the GitHub
landing-page pitch or public release notes.
"""
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
README=ROOT/"README.md"
RELEASE=ROOT/"docs"/"NOTAS-DA-VERSAO-0.8.0-beta.3.md"
OLD_RELEASE=ROOT/"docs"/"NOTAS-DA-VERSAO-0.8.0-beta.2.md"
FIRST_RELEASE=ROOT/"docs"/"NOTAS-DA-VERSAO-0.8.0-beta.1.md"
CODES=[
    r"\bRT-\d{2}\b",
    r"\bGATE-\d{4}\b",
    r"\bCADA-\d{4}\b",
    r"\b(?:DEC_ID|SNAP_ID|GATE_ID|TRACE_ID|AI_Use_ID)\b",
    r"\bscripts/[A-Za-z0-9_-]+\.py\b",
    r"\b(?:test_[a-z_]+\.py|PROJECT_CONFIG\.json)\b",
    r"\b(?:MATRIX_ONLY|WORK_FALLBACK|EXTERNAL_ANONYMIZED)\b",
]

class PublicCommunicationTests(unittest.TestCase):
    def test_landing_page_is_for_researchers_not_developers(self):
        readme=README.read_text(encoding="utf-8")
        for pattern in CODES:
            self.assertNotRegex(readme,re.compile(pattern,re.I),
                f"Developer-only term in public README: {pattern}")
        self.assertIn("repositório público",readme)
        self.assertIn("0.8.0-beta.3",readme)
        for word in ("pesquisador","fontes","C.A.D.A.","Como começar","versão beta"):
            self.assertIn(word.lower(),readme.lower())

    def test_public_release_notes_do_not_expose_internal_remediation_codes(self):
        for path in [RELEASE,OLD_RELEASE,FIRST_RELEASE]:
            doc=path.read_text(encoding="utf-8")
            for pattern in CODES:
                self.assertNotRegex(doc,re.compile(pattern,re.I),
                    f"Developer-only term in public release note {path.name}")

    def test_links_in_readme_resolve_to_real_repository_documents(self):
        text=README.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)",text):
            if target.startswith(("https://","http://","#")):
                continue
            self.assertTrue((ROOT/target).resolve().is_file(),
                f"Missing public link target: {target}")

    def test_beta_version_and_release_notes_agree(self):
        version=(ROOT/"VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version,"0.8.0-beta.3")
        self.assertIn(version,README.read_text(encoding="utf-8"))
        self.assertIn(version,RELEASE.read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()
