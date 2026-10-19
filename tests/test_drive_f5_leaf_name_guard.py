"""F5 API helper leaf-boundary regression: offline sender, no Drive access."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import drive_f5_operator as operator


class F5CreateLeafSecurityTests(unittest.TestCase):
    PARENT = "synthetic-root-00001"
    TOKEN = "fictional-testing-only-no-valid-secret"

    def test_invalid_names_are_denied_before_any_post(self):
        forbidden = (
            "", ".", "..", "foo/bar", "foo//bar", "foo/../bar",
            "./foo", "foo\\bar", "\\", "unsafe\x00name",
            "unsafe\nname", "unsafe\rname", "unsafe\tname",
            "unsafe\x1fname", "unsafe\x7fname",
        )
        calls = []
        def sender(*args, **kwargs):
            calls.append((args, kwargs))
            raise AssertionError("No network call is allowed for invalid names")
        for name in forbidden:
            with self.subTest(name=repr(name)):
                with self.assertRaisesRegex(operator.HostBlock, "INVALID_FOLDER_NAME"):
                    operator.api_create_folder_once(
                        self.TOKEN, self.PARENT, name, sender=sender)
        self.assertEqual(calls, [], "Invalid names must trigger zero POSTs")

    def test_nonstring_names_are_denied_before_any_post(self):
        called = []
        def sender(*args, **kwargs):
            called.append(True)
            raise AssertionError("Unexpected POST")
        for value in (None, 17, {}, ["folder"], b"bytes"):
            with self.subTest(value=type(value).__name__):
                with self.assertRaisesRegex(operator.HostBlock, "INVALID_FOLDER_NAME"):
                    operator.api_create_folder_once(
                        self.TOKEN, self.PARENT, value, sender=sender)
        self.assertEqual(called, [])

    def test_valid_single_leaf_allows_one_scoped_post(self):
        calls = []
        name = "01_Dados"
        def sender(token, url, *, method, body):
            calls.append((token, url, method, json.loads(body)))
            return json.dumps({
                "id": "synthetic-created-0001",
                "name": name,
                "mimeType": operator.FOLDER_MIME,
                "parents": [self.PARENT],
            }).encode("utf8")
        observed = operator.api_create_folder_once(
            self.TOKEN, self.PARENT, name, sender=sender)
        self.assertEqual(observed["name"], name)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][2], "POST")
        self.assertEqual(calls[0][3]["parents"], [self.PARENT])
        self.assertEqual(calls[0][3]["name"], name)

    def test_invalid_parent_rejects_before_any_post(self):
        calls = []
        def sender(*args, **kwargs):
            calls.append(True)
        with self.assertRaises(ValueError):
            operator.api_create_folder_once(
                self.TOKEN, "../../wrong", "01_Dados", sender=sender)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
