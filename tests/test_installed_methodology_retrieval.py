"""Regression suite for the optional installed two-channel methodology reader.

No internet requests, no protected library, no manuscript mutations and no
automatic scientific validation. The published Skill package remains lightweight.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import consult_public_methodology as hybrid
import consult_github_methodology as cards
import public_method_pdf as pdfs
from build_skill_bundle import list_sources

REF = "b" * 40


class InstalledMethodologyBoundaryTests(unittest.TestCase):
    def sources(self, tamper_pdf=False):
        card_index = json.loads((ROOT / cards.INDEX_PATH).read_text(encoding="utf-8"))
        pdf_index = json.loads((ROOT / pdfs.CATALOG).read_text(encoding="utf-8"))
        sources = {
            cards.INDEX_PATH: json.dumps(card_index).encode("utf-8"),
            pdfs.CATALOG: json.dumps(pdf_index).encode("utf-8"),
        }
        for item in card_index["documents"] + pdf_index["documents"]:
            sources[item["path"]] = (ROOT / item["path"]).read_bytes()
        if tamper_pdf:
            for item in pdf_index["documents"]:
                sources[item["path"]] += b"adversarial-tamper"
        calls = []
        def get(ref, path, limit):
            self.assertEqual(ref, REF)
            calls.append(path)
            if path not in sources:
                raise RuntimeError("Unexpected unreviewed retrieval")
            return sources[path]
        return get, calls

    def test_catalogue_expansion_snapshot_and_metadata(self):
        cards_catalog = json.loads((ROOT / cards.INDEX_PATH).read_text(encoding="utf-8"))
        pdf_catalog = json.loads((ROOT / pdfs.CATALOG).read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cards_catalog["documents"]), 61)
        self.assertGreaterEqual(len(pdf_catalog["documents"]), 33)
        self.assertEqual(len([x for x in cards_catalog["documents"] if
                              x.get("editorial_status") == "DRAFT_NEEDS_INDEPENDENT_REVIEW"]),
                         len(cards_catalog["documents"]) - 4)  # four earlier unreviewed cards
        self.assertRegex(hybrid.DEFAULT_PUBLIC_SNAPSHOT, r"^[a-f0-9]{40}$")
        self.assertEqual(hybrid.DEFAULT_PUBLIC_SNAPSHOT,
                         "b8df3d0a1699f73da63a132c07154efdafb6d5be")
        for item in cards_catalog["documents"]:
            raw = (ROOT / item["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), item["sha256"])
            self.assertEqual(item["source_kind"], "ORIGINAL_CURATED_SUMMARY")
        for item in pdf_catalog["documents"]:
            self.assertEqual(item["rights"], "PUBLIC_REDISTRIBUTION_REVIEWED")
            self.assertTrue(item["license_url"].startswith("https://"))
            self.assertIn(item["license"], ("CC BY 4.0", "CC BY"))

    def test_no_match_fetches_only_two_catalogues(self):
        get, calls = self.sources()
        result = hybrid.query("extraterrestrial igneous volcano astronomy", ref=REF,
                              card_fetch=get, pdf_fetch=get)
        self.assertEqual(result["status"], "NO_MATCH")
        self.assertEqual(calls, [cards.INDEX_PATH, pdfs.CATALOG])
        self.assertEqual(result["returned_context_chars"], 0)

    def test_editorial_guidance_is_never_direct_primary_evidence(self):
        get, calls = self.sources()
        result = hybrid.query("prisma revisão sistemática reporting", ref=REF,
                              card_fetch=get, pdf_fetch=get, max_chars=1500)
        self.assertIn(result["status"], ("RETRIEVED_WITH_REVIEW_REQUIRED",))
        self.assertTrue(result["card_hits"])
        self.assertFalse(result["scientific_gate_approved"])
        self.assertFalse(result["scientific_quality_validated"])
        self.assertFalse(result["private_sources_accessed"])
        self.assertLessEqual(result["returned_context_chars"], 1500)
        for card in result["card_hits"]:
            self.assertEqual(card["citation_grade"], "I_EDITORIAL_SYNTHESIS_ONLY")
            self.assertTrue(card["must_not_claim_primary_source_read"])
            self.assertFalse(card["primary_source_directly_verified"])
            self.assertIn(card["editorial_status"],
                          {"NOT_INDEPENDENTLY_REVIEWED", "DRAFT_NEEDS_INDEPENDENT_REVIEW"})
            self.assertEqual(card["github_commit"], REF)
        self.assertLessEqual(len([x for x in calls if x.endswith(".pdf")]), 1)

    def test_pdf_tampering_cannot_be_upgraded_to_source_verification(self):
        get, calls = self.sources(tamper_pdf=True)
        result = hybrid.query("confiabilidade revisão sistemática", ref=REF,
                              card_fetch=get, pdf_fetch=get)
        self.assertEqual(result["pdf_status"], "UNAVAILABLE_OR_BLOCKED")
        self.assertFalse(result["pdf_hits"])
        self.assertTrue(result["card_hits"])
        self.assertTrue(result["requires_primary_source_verification"])

    def test_moving_ref_bad_budget_and_unavailable_host(self):
        get, calls = self.sources()
        for kw in ({"ref": "main"}, {"ref": REF, "max_chars": 800},
                   {"ref": REF, "max_cards": 20}):
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                hybrid.query("revisão", card_fetch=get, pdf_fetch=get, **kw)
        self.assertEqual(calls, [])
        def denied(ref, path, limit):
            raise OSError("No authorized HTTPS runtime")
        result = hybrid.query("revisão", ref=REF, card_fetch=denied, pdf_fetch=denied)
        self.assertEqual(result["status"], "PARTIAL_OR_UNAVAILABLE")
        self.assertFalse(result["card_hits"])
        self.assertFalse(result["pdf_hits"])

    def test_distribution_bundles_readers_only_not_corpora(self):
        files = {x.relative_to(ROOT).as_posix() for x in list_sources(ROOT)}
        self.assertIn("scripts/consult_public_methodology.py", files)
        self.assertIn("scripts/public_method_pdf.py", files)
        self.assertIn("scripts/consult_github_methodology.py", files)
        self.assertIn("references/GITHUB-METHODOLOGY.md", files)
        self.assertFalse(any(f.startswith("knowledge/") for f in files))
        self.assertFalse(any(f.endswith(".pdf") for f in files))
        self.assertFalse(any(f.startswith("experimental/") for f in files))
        self.assertNotIn("scripts/build_skill_bundle.py", files)

    def test_no_automatic_external_access_or_private_credentials(self):
        source = (ROOT / "scripts/consult_public_methodology.py").read_text("utf-8")
        self.assertIn("if __name__ == \"__main__\"", source)
        self.assertIn("requires_primary_source_verification", source)
        self.assertIn("scientific_gate_approved", source)
        self.assertNotIn("automatically download all", source.lower())


if __name__ == "__main__":
    unittest.main()
