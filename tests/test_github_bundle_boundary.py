"""The installed Skill must stay small; public method cards live in Git only."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_skill_bundle

class GitMethodologyBundleBoundary(unittest.TestCase):
    def test_remote_catalog_is_not_shipped(self):
        files={x.relative_to(ROOT).as_posix() for x in build_skill_bundle.list_sources(ROOT)}
        self.assertIn('scripts/consult_github_methodology.py',files)
        self.assertIn('scripts/consult_public_methodology.py',files)
        self.assertIn('scripts/public_method_pdf.py',files)
        self.assertIn('references/GITHUB-METHODOLOGY.md',files)
        self.assertFalse(any(x.startswith('knowledge/') for x in files))
        self.assertTrue((ROOT/'knowledge/methodology/catalog.json').exists())
        self.assertTrue((ROOT/'knowledge/methodology/pdf_catalog.json').exists())
        self.assertFalse(any(x.lower().endswith('.pdf') for x in files))
        self.assertNotIn('knowledge/methodology/pdf_catalog.json',files)
        self.assertNotIn('experimental/conceptual_rag/github_pdf_reader.py',files)

if __name__=='__main__':unittest.main()
