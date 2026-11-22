"""Integrity and language guard for the corrected public editorial Markdown.

Rewriting prose is not proof of original-source reading or scientific review.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "methodology"
REWRITE = "ENGLISH_EDITORIAL_REWRITE_METADATA_GROUNDED_NOT_SOURCE_REVIEW"
RESTORED = "RESTORED_PREEXISTING_ENGLISH_EDITORIAL_NOT_SCIENTIFIC_APPROVAL"
OBSOLETE = "MACHINE_TRANSLATED_REVIEW_PENDING"
PORTUGUESE = re.compile(
    r"\b(?:não|pesquisa|revisão|análise|metodologia|evidência|"
    r"direitos|autorização|científica|contribuição|verificação|"
    r"perguntas|conclusão|fontes|pesquisador|necessário)\b", re.I
)


class CorrectedMethodologyEnglishTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((BASE / "source_registry_catalog.json").read_text("utf-8"))
        cls.editorial = json.loads((BASE / "catalog.json").read_text("utf-8"))
        cls.ledger = json.loads((BASE / "intake/operational-validation.json").read_text("utf-8"))
        cls.by_path = {x["path"]: x for x in cls.ledger["cards"]}

    def test_exact_coverage_and_scientific_nonapproval(self):
        source = self.source["documents"]
        editorial = self.editorial["documents"]
        self.assertEqual((len(source), len(editorial), len(self.by_path)), (475, 174, 649))
        self.assertEqual(sum(x.get("translation_fidelity_status") == REWRITE
                             for x in source), 472)
        self.assertEqual(sum(x.get("translation_fidelity_status") in (REWRITE, RESTORED)
                             for x in editorial), 110)
        self.assertEqual(sum(x.get("translation_fidelity_status") == RESTORED
                             for x in editorial), 24)
        self.assertFalse(any(x.get("translation_fidelity_status") == OBSOLETE
                             for x in source + editorial))
        self.assertTrue(all(x.get("scientific_use_validated") is False
                            for x in source + editorial))

    def test_digests_exact_and_machine_gibberish_absent(self):
        targets = [x for x in self.source["documents"] + self.editorial["documents"]
                   if x.get("translation_fidelity_status") in (REWRITE, RESTORED)]
        self.assertEqual(len(targets), 582)
        for row in targets:
            with self.subTest(path=row["path"]):
                raw = (ROOT / row["path"]).read_bytes()
                digest = hashlib.sha256(raw).hexdigest()
                self.assertEqual(digest, row["sha256"])
                self.assertEqual(digest, self.by_path[row["path"]]["sha256"])
                content = raw.decode("utf-8")
                self.assertNotIn("== sync, corrected by elderman", content)
                self.assertNotIn("before playing it", content)
                self.assertNotIn("permission to play it", content)
                if row.get("translation_fidelity_status") == REWRITE:
                    self.assertIn("NOT", content)
                    self.assertIn("[L]", content)
                    self.assertIn("blob/9cf5b9ee91c0c0ade6c6d66316b26bde67cbe413", content)

    def test_new_english_editorial_prose_not_portuguese(self):
        targets = [x for x in self.source["documents"] + self.editorial["documents"]
                   if x.get("translation_fidelity_status") == REWRITE]
        for row in targets:
            with self.subTest(path=row["path"]):
                data = (ROOT / row["path"]).read_text("utf-8")
                prose = "\n".join(
                    line for line in data.splitlines()
                    if not line.startswith((
                        "- Original published title:",
                        "- Original catalogued topic label",
                        "Historic pending-review identifier",
                        "- Original earlier editorial record",
                        "Original Portuguese editorial notes",
                        "Source locator for independent verification",
                    ))
                    and "https://github.com/" not in line
                    and "REVISÃO_CIENTÍFICA_INDEPENDENTE_PENDENTE" not in line
                )
                # This is a conservative indicator, not a semantic equivalence test.
                self.assertFalse(PORTUGUESE.search(prose),
                                 "Portuguese editorial prose still detected")

if __name__ == "__main__":
    unittest.main()
