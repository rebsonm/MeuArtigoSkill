"""Regressions for all 475 original-library bibliographic prospecting cards.

No private PDFs are opened and no scientifically reviewed card is synthesized
by this test. It checks coverage, honest evidence grade and immutable retrieval.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import consult_source_registry as registry
from build_skill_bundle import list_sources

REF = "b" * 40
C = ROOT / registry.INDEX


class SourceRegistryCompletenessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = C.read_bytes()
        cls.docs = registry._catalog(cls.raw)

    def test_exactly_one_record_for_every_source_pdf(self):
        known = []
        reviewed = 0
        for i in range(1, 6):
            ledger = json.loads((ROOT / "knowledge/methodology/intake" /
                                 f"rights-ledger-part-0{i}.json").read_text("utf-8"))
            for item in ledger["records"]:
                known.append(item["id"])
                if item["rights_review"] == "VERIFIED_PUBLISHER_LICENSE":
                    reviewed += 1
        ids = [x["source_id"] for x in self.docs]
        self.assertEqual(ids, known)
        self.assertEqual(len(ids), 475)
        self.assertEqual(len([x for x in self.docs
                              if x["bibliography_match_status"] ==
                                 "CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED"]), 404)
        self.assertEqual(len([x for x in self.docs
                              if x["bibliography_match_status"] ==
                                 "IDENTITY_UNRESOLVED"]), 71)
        self.assertEqual(len([x for x in self.docs if
                              x["rights_review"] == "VERIFIED_PUBLISHER_LICENSE"]),
                         reviewed)
        self.assertEqual(reviewed, 3)

    def test_sha256_and_source_metadata_only_every_card(self):
        for item in self.docs:
            with self.subTest(source_id=item["source_id"]):
                data = (ROOT / item["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])
                self.assertLessEqual(len(data), registry.MAX_CARD_BYTES)
                text = data.decode("utf-8")
                self.assertIn("FICHA_DE_PROSPECÇÃO_NÃO_REVISADA", text)
                self.assertIn("NÃO é [I] síntese de leitura nem [L]", text)
                self.assertIn("Não atribuir as propostas acima ao autor", text)
                self.assertNotIn("drive.google.com/drive/", text.lower())
                self.assertNotIn("access_token", text.lower())
                self.assertNotIn("AIza", text)
                self.assertTrue(item["source_metadata_only"])
                if item["rights_review"] == "NOT_CHECKED":
                    self.assertFalse(item["has_original_public_pdf"])
                    self.assertIsNone(item["public_pdf_path"])

    def test_retriever_is_bounded_and_cannot_upgrade_metadata(self):
        files = {registry.INDEX: self.raw}
        for d in self.docs:
            files[d["path"]] = (ROOT / d["path"]).read_bytes()
        calls = []
        def fetch(ref, path, limit):
            self.assertEqual(ref, REF)
            self.assertLessEqual(len(files[path]), limit)
            calls.append(path)
            return files[path]
        result = registry.query("institutional grammar specification encoding", ref=REF,
                                fetch=fetch, max_chars=1450)
        self.assertEqual(result["status"], "BIBLIOGRAPHIC_LEADS_ONLY")
        self.assertTrue(result["hits"])
        self.assertIn("SRC-0002", [x["source_id"] for x in result["hits"]])
        self.assertLessEqual(result["returned_context_chars"], 1450)
        self.assertFalse(result["scientific_quality_validated"])
        self.assertFalse(result["scientific_gate_approved"])
        self.assertFalse(result["private_sources_accessed"])
        self.assertFalse(result["public_pdf_upload_authorized_by_metadata"])
        self.assertLessEqual(len(calls), 4)
        for hit in result["hits"]:
            self.assertEqual(hit["citation_grade"],
                             "P_BIBLIOGRAPHIC_PROSPECTING_NOT_SOURCE_EVIDENCE")
            self.assertFalse(hit["source_work_directly_verified"])
            self.assertTrue(hit["must_not_claim_primary_source_read"])

    def test_unknown_question_no_source_card_retrieved(self):
        seen = []
        def fetch(ref, path, cap):
            seen.append(path)
            return self.raw
        result = registry.query("quasars astrophysics gravitational waves",
                                ref=REF, fetch=fetch)
        self.assertEqual(result["status"], "NO_MATCH")
        self.assertEqual(seen, [registry.INDEX])

    def test_unpinned_ref_and_tampering_fail_closed(self):
        for bad in ("main", "latest", "abc"):
            with self.subTest(ref=bad), self.assertRaisesRegex(ValueError, "IMMUTABLE"):
                registry.query("métodos qualitativos", ref=bad,
                               fetch=lambda *args: self.fail("Network was accessed"))
        files = {registry.INDEX: self.raw}
        for d in self.docs:
            files[d["path"]] = (ROOT / d["path"]).read_bytes() + b"tamper"
        with self.assertRaisesRegex(ValueError, "DIGEST_MISMATCH"):
            registry.query("gramática institucional", ref=REF,
                           fetch=lambda ref, path, limit: files[path])

    def test_candidate_installer_exposes_only_reader_not_source_archive(self):
        filenames = {p.relative_to(ROOT).as_posix() for p in list_sources(ROOT)}
        self.assertIn("scripts/consult_source_registry.py", filenames)
        self.assertNotIn(registry.INDEX, filenames)
        self.assertFalse(any(x.startswith("knowledge/") for x in filenames))
        self.assertFalse(any(x.endswith(".pdf") for x in filenames))


if __name__ == "__main__":
    unittest.main()
