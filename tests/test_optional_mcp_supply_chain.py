"""Synthetic offline contract checks for optional MCP Apps npm supply chain."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_optional_mcp_supply_chain import validate


class OptionalMcpSupplyChainTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.dir = self.root / "integrations" / "mcp-apps"
        self.dir.mkdir(parents=True)
        self.pkg = {"name": "test-private-mcp", "version": "0.0.1", "private": True,
                    "dependencies": {"zod": "^3.25.0"}, "devDependencies": {}}
        self.lock = {"name": self.pkg["name"], "version": self.pkg["version"],
                     "lockfileVersion": 3, "packages": {"": {
                         "name": self.pkg["name"], "version": self.pkg["version"],
                         "dependencies": self.pkg["dependencies"], "devDependencies": {}}}}

    def write(self):
        (self.dir / "package.json").write_text(json.dumps(self.pkg))
        (self.dir / "package-lock.json").write_text(json.dumps(self.lock))

    def test_no_optional_node_module_in_baseline(self):
        self.assertEqual(validate(self.root)["status"], "NOT_IN_BASELINE")

    def test_unlocked_manifest_is_blocked(self):
        (self.dir / "package.json").write_text(json.dumps(self.pkg))
        with self.assertRaisesRegex(ValueError, "LOCK_REQUIRED"):
            validate(self.root)

    def test_consistent_npm_lock_is_admitted(self):
        self.write()
        self.assertEqual(validate(self.root)["status"], "LOCK_DECLARATIONS_MATCH")

    def test_manifest_drift_is_blocked(self):
        self.write()
        self.pkg["dependencies"]["zod"] = "^4.0.0"
        (self.dir / "package.json").write_text(json.dumps(self.pkg))
        with self.assertRaisesRegex(ValueError, "DRIFT"):
            validate(self.root)

    def test_not_private_is_blocked(self):
        self.write()
        self.pkg["private"] = False
        (self.dir / "package.json").write_text(json.dumps(self.pkg))
        with self.assertRaisesRegex(ValueError, "MUST_BE_PRIVATE"):
            validate(self.root)

    def test_old_lock_format_is_blocked(self):
        self.write()
        self.lock["lockfileVersion"] = 1
        (self.dir / "package-lock.json").write_text(json.dumps(self.lock))
        with self.assertRaisesRegex(ValueError, "VERSION_UNSUPPORTED"):
            validate(self.root)


if __name__ == "__main__":
    unittest.main()
