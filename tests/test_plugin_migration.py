"""Plugin migration regressions. No connection, deployment, or scientific corpus."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_plugin_bundle import build
from version_info import read_version


class PluginCandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        self.archive = self.dir / f"MeuArtigoPlugin-v{read_version(ROOT)}-candidate.zip"

    def test_packaged_icon_is_exact_original(self):
        result = build(ROOT, self.archive)
        with ZipFile(self.archive) as z:
            icon = z.read("assets/icon.svg")
            self.assertEqual(icon, (ROOT / "assets/icon.svg").read_bytes())
            self.assertEqual(z.read("skills/meu-artigo/assets/icon.svg"), icon)
            portable = json.loads(z.read("plugin.json"))
            overlay = json.loads(z.read(".codex-plugin/plugin.json"))
            for obj in (portable["extensions"]["com.openai"]["interface"],
                        overlay["interface"]):
                self.assertEqual(obj["logo"], "./assets/icon.svg")
                self.assertEqual(obj["composerIcon"], "./assets/icon.svg")
            self.assertEqual(portable["version"], overlay["version"])
            self.assertEqual(portable["version"], read_version(ROOT))
            self.assertFalse(result["mcp_app_deployed"])

    def test_package_preserves_gates_and_does_not_leak_protected_content(self):
        build(ROOT, self.archive)
        with ZipFile(self.archive) as z:
            names = z.namelist()
            self.assertFalse(any(n.lower().endswith((".pdf", ".env", ".pem", ".key"))
                                 for n in names))
            self.assertFalse(any("/fulltext_corpus/" in n.lower() for n in names))
            skill = z.read("skills/meu-artigo/SKILL.md").decode()
            self.assertIn("GATE", skill)
            self.assertIn("Google Drive", skill)
            self.assertIn("Plugin installation alone grants no", skill)
            self.assertNotIn("mcp.json", names)
            self.assertNotIn("visual-app/dist/main.js", names)

    def test_digest_receipt_refers_to_real_archive_and_no_scientific_release(self):
        result = build(ROOT, self.archive)
        receipt = json.loads((self.dir / "PLUGIN_BUILD_RECEIPT.json").read_text())
        self.assertEqual(result, receipt)
        self.assertEqual(receipt["package_sha256"],
                         hashlib.sha256(self.archive.read_bytes()).hexdigest())
        self.assertFalse(receipt["scientific_quality_validated"])
        self.assertFalse(receipt["drive_sync_verified"])

    def test_bundle_is_deterministic(self):
        build(ROOT, self.archive)
        digest = hashlib.sha256(self.archive.read_bytes()).hexdigest()
        build(ROOT, self.archive)
        self.assertEqual(hashlib.sha256(self.archive.read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
