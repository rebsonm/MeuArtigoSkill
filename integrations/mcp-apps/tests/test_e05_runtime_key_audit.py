"""Offline E05 runtime-key audit cases. Synthetic keys only; no real file."""
import importlib.util
from pathlib import Path
import unittest

AUDIT_PATH = Path(__file__).resolve().parents[1] / "scripts/e05-runtime-key-audit.py"
spec = importlib.util.spec_from_file_location("e05_key_audit", AUDIT_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RuntimeKeyAuditContract(unittest.TestCase):
    def test_official_and_launcher_accepted(self):
        self.assertEqual(module.classify(b"sk-" + b"abcDEF09_-" * 5),
                         ("PASS", "PASS", "SYNTAX_ACCEPTED_REMOTE_UNVERIFIED"))

    def test_official_disallowed_character(self):
        self.assertEqual(module.classify(b"sk-" + b"A" * 24 + b"."),
                         ("FAIL", "FAIL", "UNSUPPORTED_CHARACTER"))

    def test_invalid_utf8(self):
        self.assertEqual(module.classify(b"sk-" + b"A" * 24 + b"\xff"),
                         ("FAIL", "FAIL", "NON_UTF8_SECRET"))

    def test_empty(self):
        self.assertEqual(module.classify(b""),
                         ("FAIL", "FAIL", "EMPTY_SECRET"))

    def test_whitespace_official_accepts_but_launcher_rejects(self):
        self.assertEqual(module.classify(b"sk-" + b"A" * 24 + b"\n"),
                         ("PASS", "FAIL", "WRAPPER_REJECTS_WHITESPACE"))

    def test_no_prefix_official_accepts_but_launcher_rejects(self):
        self.assertEqual(module.classify(b"api_" + b"A" * 24),
                         ("PASS", "FAIL", "WRAPPER_REJECTS_PREFIX_OR_LENGTH"))

    def test_fails_closed_around_value_not_printed(self):
        source = AUDIT_PATH.read_text()
        self.assertIn("os.O_NOFOLLOW", source)
        self.assertIn("E05_KEY_AUDIT_MUTATIONS=NONE", source)
        self.assertNotIn("print(raw", source)
        self.assertNotIn("print(text", source)
        self.assertNotIn("hashlib", source)
        self.assertNotIn("requests", source)


if __name__ == "__main__":
    unittest.main()
