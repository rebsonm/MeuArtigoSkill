"""Protect the public Skill-only distribution and research governance."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
TERMS=("pl"+"ugin","m"+"cp","visual"+"-app","meu_artigo_"+"dashboard")
SOURCE_TYPES={".py",".md",".yaml",".yml",".json",".ts",".html",".cff",".txt"}

class PublicSkillBoundaryTests(unittest.TestCase):
    def test_no_non_skill_subprojects(self):
        self.assertFalse((ROOT/("pl"+"ugin")).exists())
        self.assertFalse((ROOT/("visual"+"-app")).exists())
        self.assertFalse((ROOT/"scripts"/("build_"+"pl"+"ugin_bundle.py")).exists())
        self.assertTrue((ROOT/"SKILL.md").is_file())
        self.assertTrue((ROOT/"scripts/build_skill_bundle.py").is_file())

    def test_no_references_to_removed_distribution_in_current_tree(self):
        problems=[]
        for base in (ROOT,ROOT/"docs",ROOT/"references",ROOT/"scripts",
                     ROOT/"tests",ROOT/"agents",ROOT/".github"):
            paths=base.iterdir() if base==ROOT else base.rglob("*")
            for p in paths:
                if not p.is_file() or p.suffix.lower() not in SOURCE_TYPES:
                    continue
                relative=p.relative_to(ROOT).as_posix()
                if any(t in relative.lower() for t in TERMS):
                    problems.append((relative,"filename"))
                content=p.read_text(encoding="utf-8",errors="replace").lower()
                # The test deliberately constructs the forbidden terms
                # instead of documenting their removed public names.
                for term in TERMS:
                    if term in content:
                        problems.append((relative,term))
        self.assertEqual(problems,[],f"Public Skill boundary violated: {problems}")

    def test_scientific_human_controls_remain(self):
        source=(ROOT/"SKILL.md").read_text(encoding="utf-8")
        for token in ("GATE_ID","DEC_ID","SNAP_ID","GOOGLE_DRIVE_FIRST",
                      "WORK_FALLBACK","Counter_Evidence_IDs"):
            self.assertIn(token,source)

if __name__=="__main__":unittest.main()
