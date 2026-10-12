"""Ensure Wiki publishing stays separate from Skill releases."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class NativeWikiPublishingTests(unittest.TestCase):
    def test_pages(self):
        pages = list((ROOT / "wiki").glob("*.md"))
        self.assertGreaterEqual(len(pages), 15)
        for name in ("Home.md", "_Sidebar.md", "_Footer.md"):
            self.assertTrue((ROOT / "wiki" / name).is_file())

    def test_write_is_scoped_and_publication_non_destructive(self):
        body = (ROOT / ".github/workflows/publish-wiki.yml").read_text(encoding="utf-8")
        for part in ("workflow_dispatch:", "branches: [main]", "contents: write",
                     "GITHUB_REPOSITORY", ".wiki.git", "Wiki page $filename differs",
                     "diff --cached --check", "persist-credentials: false"):
            self.assertIn(part, body)
        self.assertNotIn("gh release create", body)
        self.assertNotIn("git push --force", body)
        self.assertNotIn("persist-credentials: true", body)
        self.assertNotIn("- 'wiki/**'", body)


if __name__ == "__main__":
    unittest.main()
