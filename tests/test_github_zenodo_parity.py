"""Local fixtures for RC identity parity; does not consult providers."""
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_github_zenodo_parity import preflight, reconcile


class ParityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "VERSION").write_text("1.0.0-rc.3\n", encoding="utf-8")
        (self.root / "CITATION.cff").write_text(
            'cff-version: 1.2.0\nversion: "1.0.0-rc.3"\n'
            'preferred-citation:\n  type: software\n  version: "1.0.0-rc.3"\n',
            encoding="utf-8")
        self.github = {
            "tag": "v1.0.0-rc.3", "version": "1.0.0-rc.3",
            "source_commit": "a" * 40, "archive_kind": "source",
            "archive_sha256": "b" * 64,
        }
        self.zenodo = {
            "version": "1.0.0-rc.3", "version_doi": "10.5281/zenodo.12345678",
            "source_commit": "a" * 40, "archive_kind": "source",
            "archive_sha256": "b" * 64,
        }

    def test_matching_candidate_and_archive_identity(self):
        self.assertEqual(preflight(self.root, "v1.0.0-rc.3"), [])
        self.assertEqual(reconcile(self.github, self.zenodo), [])

    def test_prevents_different_tag_and_source_version(self):
        self.assertIn("GITHUB_TAG_DIFFERS_FROM_SOURCE_VERSION",
                      preflight(self.root, "v1.0.0-rc.4"))

    def test_prevents_different_preferred_citation_version(self):
        p = self.root / "CITATION.cff"
        p.write_text(p.read_text().replace('  version: "1.0.0-rc.3"',
                                            '  version: "1.0.0-rc.2"'))
        self.assertIn("CITATION_PREFERRED_VERSION_MISMATCH",
                      preflight(self.root, "v1.0.0-rc.3"))

    def test_prevents_different_zenodo_version(self):
        self.zenodo["version"] = "1.0.0-rc.2"
        self.assertIn("ZENODO_VERSION_DIFFERS_FROM_GITHUB_TAG",
                      reconcile(self.github, self.zenodo))

    def test_prevents_different_code_at_same_version(self):
        self.zenodo["source_commit"] = "c" * 40
        self.assertIn("ARCHIVED_SOURCE_COMMIT_DIFFERS",
                      reconcile(self.github, self.zenodo))

    def test_missing_zenodo_archived_code_evidence_fails_closed(self):
        self.zenodo.pop("source_commit")
        self.assertIn("ZENODO_ARCHIVED_SOURCE_SHA_NOT_VERIFIED",
                      reconcile(self.github, self.zenodo))

    def test_same_kind_archive_hash_differs(self):
        self.zenodo["archive_sha256"] = "c" * 64
        self.assertIn("SAME_KIND_ARCHIVE_HASH_MISMATCH",
                      reconcile(self.github, self.zenodo))

    def test_different_kinds_require_source_commit_not_zip_equality(self):
        self.zenodo["archive_kind"] = "github-source"
        self.zenodo.pop("archive_sha256")
        self.assertEqual(reconcile(self.github, self.zenodo), [])

    def test_missing_version_doi_blocks_claim_of_publication(self):
        self.zenodo.pop("version_doi")
        self.assertIn("ZENODO_VERSION_SPECIFIC_DOI_NOT_VERIFIED",
                      reconcile(self.github, self.zenodo))


if __name__ == "__main__":
    unittest.main()
