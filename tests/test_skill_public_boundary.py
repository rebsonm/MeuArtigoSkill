"""Protect the public Skill-only distribution and research governance."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
# Optional documentation of externally connected protocol tools is not
# equivalent to shipping a service inside the standalone Skill archive.
LEGACY_TERMS=("visual"+"-app","meu_artigo_"+"dashboard")
DISTRIBUTION_TERM="pl"+"ugin"
PROTOCOL_TERM="m"+"cp"
OPTIONAL_PROTOCOL_DOCS={
    "SKILL.md",
    "references/"+PROTOCOL_TERM+"-tool-use.md",
    "docs/CHATGPT.md",
    "docs/CHATGPT-"+PROTOCOL_TERM.upper()+"-HOST-ACCEPTANCE.md",
    "docs/COMPATIBILIDADE-PLATAFORMAS.md",
    # User-requested optional read-only MCP Apps code remains OUTSIDE
    # the self-contained public Skill archive and has its own CI.
    "CHANGELOG.md",
    "references/native-chat-dashboard.md",
    "scripts/build_research_site.py",
    ".github/workflows/mcp-apps-ci.yml",
    "tests/test_skill_public_boundary.py",
    "tests/test_optional_"+PROTOCOL_TERM+"_skill.py",
    # Reviewed source-only integrated homologation; neither file is a server.
    "scripts/homologate_integrated_skill.py",
    "tests/test_integrated_skill_homologation.py",
    "docs/INTEGRATED-SKILL-HOMOLOGATION.md",
}
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
                if any(t in relative.lower() for t in LEGACY_TERMS):
                    problems.append((relative,"legacy filename"))
                if (PROTOCOL_TERM in relative.lower() and
                        relative not in OPTIONAL_PROTOCOL_DOCS):
                    problems.append((relative,"unexpected protocol artifact"))
                if DISTRIBUTION_TERM in relative.lower():
                    problems.append((relative,"unexpected distribution artifact"))
                content=p.read_text(encoding="utf-8",errors="replace").lower()
                for term in LEGACY_TERMS:
                    if term in content:
                        problems.append((relative,term))
                # Tool-use guidance is allowed only in reviewed instructions,
                # not arbitrary executable files or new distribution projects.
                if relative not in OPTIONAL_PROTOCOL_DOCS:
                    for term in (DISTRIBUTION_TERM,PROTOCOL_TERM):
                        if term in content:
                            problems.append((relative,term))
        self.assertEqual(problems,[],f"Public Skill boundary violated: {problems}")

    def test_optional_chat_ui_is_not_packaged_in_public_skill(self):
        import sys
        sys.path.insert(0, str(ROOT/"scripts"))
        from build_skill_bundle import list_sources
        shipped=[p.relative_to(ROOT).as_posix() for p in list_sources(ROOT)]
        self.assertIn("assets/research_site.html",shipped)
        self.assertFalse(any(p.startswith("integrations/") for p in shipped))
        self.assertFalse(any("node_modules" in p or p.endswith("server.mjs") for p in shipped))

    def test_scientific_human_controls_remain(self):
        source=(ROOT/"SKILL.md").read_text(encoding="utf-8")
        for token in ("GATE_ID","DEC_ID","SNAP_ID","GOOGLE_DRIVE_FIRST",
                      "WORK_FALLBACK","Counter_Evidence_IDs"):
            self.assertIn(token,source)

if __name__=="__main__":unittest.main()
