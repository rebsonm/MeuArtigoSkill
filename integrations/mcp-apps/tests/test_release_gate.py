"""Fail-closed go-live matrix tests; synthetic references and SHAs only."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "integrations" / "mcp-apps" / "scripts"))
from release_gate import assess, PHASES, ROLES

SHA = "a" * 40
OTHER = "b" * 40


class DocumentaryGateTests(unittest.TestCase):
    def record(self, key, status="PASS", sha=SHA):
        return {"status": status, "source_sha": sha,
                "evidence_ref": "EVID-TEST-0001",
                "observer_role": ROLES[key]}

    def test_all_ten_remain_open_without_evidence(self):
        report = assess(SHA)
        self.assertEqual(report["total"], 10)
        self.assertEqual(report["remaining"], 10)
        self.assertFalse(report["merge_authorized"])
        self.assertFalse(report["publication_authorized"])
        self.assertFalse(report["documentary_inputs_independently_authenticated"])

    def test_even_ten_recorded_passes_cannot_authorize_releases(self):
        records = {key: self.record(key) for key in PHASES}
        report = assess(SHA, records)
        self.assertEqual(report["remaining"], 0)
        self.assertEqual(report["decision"],
                         "RECORDED_ONLY_REQUIRES_EXTERNAL_APPROVAL")
        for key in ("merge_authorized", "deployment_authorized",
                    "plugin_update_authorized", "publication_authorized"):
            self.assertIs(report[key], False)

    def test_stale_or_failed_records_block(self):
        report = assess(SHA, {
            "R01": self.record("R01", sha=OTHER),
            "R02": self.record("R02", status="FAIL")
        })
        self.assertEqual(report["remaining"], 10)
        self.assertEqual(report["gates"][0]["status"], "STALE")
        self.assertEqual(report["gates"][1]["status"], "RECORDED_FAIL")

    def test_bad_status_role_sha_and_extra_fields_fail_closed(self):
        for bad in (
            {"R01": {**self.record("R01"), "approved": True}},
            {"R01": {**self.record("R01"), "observer_role": "MAINTAINER"}},
            {"R01": {**self.record("R01"), "status": "APPROVED"}},
            {"R01": {**self.record("R01"), "source_sha": "unverified"}},
            {"R01": {**self.record("R01"), "evidence_ref": "https://private.example"}},
            {"R99": self.record("R01")},
            ["not-an-object"],
        ):
            with self.subTest(case=str(bad)[:30]):
                with self.assertRaises(ValueError):
                    assess(SHA, bad)

    def test_bad_source_sha_is_never_accepted(self):
        for bad in ("", "latest", "abc", None):
            with self.assertRaises(ValueError):
                assess(bad)


if __name__ == "__main__":
    unittest.main()
