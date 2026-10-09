"""Public presentation regression checks.

Technical internals belong in developer docs and source, not in the GitHub
landing-page pitch or public release notes.
"""
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT/"scripts"))
from version_info import read_version, release_notes_path
README=ROOT/"README.md"
RELEASE=release_notes_path(ROOT)
HISTORICAL_RELEASES=sorted((ROOT/"docs").glob("NOTAS-DA-VERSAO-*.md"))
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
        self.assertIn(read_version(ROOT),readme)
        for word in ("pesquisador","fontes","C.A.D.A.","Como começar","versão beta"):
            self.assertIn(word.lower(),readme.lower())

    def test_public_release_notes_do_not_expose_internal_remediation_codes(self):
        for path in HISTORICAL_RELEASES:
            doc=path.read_text(encoding="utf-8")
            for pattern in CODES:
                self.assertNotRegex(doc,re.compile(pattern,re.I),
                    f"Developer-only term in public release note {path.name}")

    def test_public_docs_exclude_private_collections_and_internal_roadmap_codes(self):
        """Private source provenance and internal development tickets stay outside public docs."""
        forbidden = re.compile(
            r"\bPPGA\b|ppga-methodological|\bRT-\d{2}\b|\bP-\d{2}\b|\bT-\d{2}\b",
            re.I,
        )
        docs = [ROOT/"README.md", ROOT/"SKILL.md", ROOT/"CHANGELOG.md", ROOT/"SECURITY.md", ROOT/"CONTRIBUTING.md"]
        docs += list((ROOT/"docs").rglob("*.md"))
        docs += list((ROOT/"references").rglob("*.md"))
        for path in docs:
            self.assertNotRegex(
                path.read_text(encoding="utf-8"), forbidden,
                f"Private institutional provenance or internal development code in {path}"
            )
        self.assertFalse((ROOT/"references"/"ppga-methodological-foundations.md").exists())
        self.assertIn("Apache License 2.0", (ROOT/"README.md").read_text(encoding="utf-8"))
        self.assertIn("Rebson de Morais Mendes", (ROOT/"NOTICE").read_text(encoding="utf-8"))

    def test_links_in_readme_resolve_to_real_repository_documents(self):
        text=README.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)",text):
            if target.startswith(("https://","http://","#")):
                continue
            self.assertTrue((ROOT/target).resolve().is_file(),
                f"Missing public link target: {target}")

    def test_beta_version_and_release_notes_agree(self):
        version=(ROOT/"VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version,read_version(ROOT))
        self.assertIn(version,README.read_text(encoding="utf-8"))
        self.assertIn(version,RELEASE.read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()
