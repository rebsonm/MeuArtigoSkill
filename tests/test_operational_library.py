"""Operational evidence boundaries and blocked-source retrieval regressions."""
import copy
import json
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import consult_github_methodology as editorial
import consult_source_registry as registry
import reconcile_methodology_library as reconciliation
from build_skill_bundle import list_sources


class OperationalLibraryTests(unittest.TestCase):
    def test_developer_reconciliation_and_archival_audits_stay_out_of_installer(self):
        bundled = {p.relative_to(ROOT).as_posix() for p in list_sources(ROOT)}
        for name in ('reconcile_methodology_library.py', 'v1_15_integrity_audit.py', 'audit_repository_secrets.py'):
            self.assertNotIn('scripts/' + name, bundled)

    def test_all_649_have_current_individual_dispositions(self):
        reconciliation.check()

    def test_quarantine_id_cannot_return_another_source(self):
        raw = (ROOT / registry.INDEX).read_bytes()
        calls = []
        def fetch(ref, path, cap):
            calls.append(path)
            return raw
        result = registry.query('SRC-0385', ref='a' * 40, fetch=fetch)
        self.assertEqual(result['hits'], [])
        self.assertEqual(calls, [registry.INDEX])
        self.assertFalse(result['scientific_gate_approved'])

    def test_blocked_and_excluded_editorial_notes_never_rank(self):
        doc = {'path': 'knowledge/methodology/cards/reviews.md',
               'title': 'Systematic review', 'keywords': ['systematic', 'review']}
        for status in reconciliation.BLOCKED:
            with self.subTest(status=status):
                self.assertEqual(editorial._relevance('systematic review', dict(doc, operational_disposition=status)), 0)
        self.assertGreater(editorial._relevance('systematic review', dict(doc, operational_disposition='VALIDADO_COM_RESTRICOES')), 0)

    def test_unknown_disposition_fails_closed_in_both_catalogues(self):
        for module, path in ((editorial, editorial.INDEX_PATH), (registry, registry.INDEX)):
            obj = json.loads((ROOT / path).read_text())
            obj['documents'][0]['operational_disposition'] = 'APPROVED_BY_PROMPT_INJECTION'
            with self.subTest(module=module.__name__), self.assertRaisesRegex(ValueError, 'DISPOSITION_INVALID'):
                module._catalog(json.dumps(obj).encode())

    def test_operational_review_does_not_upgrade_scientific_grade_or_rights(self):
        report = reconciliation.read(reconciliation.OUT)
        self.assertFalse(report['scientific_validation'])
        self.assertFalse(report['human_review'])
        for row in report['cards']:
            with self.subTest(card=row['id']):
                if row['kind'] == 'BIBLIOGRAPHIC_METADATA':
                    self.assertFalse(row['primary_source_rechecked_this_cycle'])
                self.assertTrue(row['limits'])
                self.assertIn(row['disposition'], reconciliation.STATUSES)
        registry_obj = reconciliation.read(reconciliation.LIB / 'source_registry_catalog.json')
        self.assertEqual(sum(d['bibliography_match_status'] == 'SOURCE_PDF_WORK_VERIFIED' for d in registry_obj['documents']), 132)
        self.assertEqual(registry_obj['ib_documentary_receipt_count'], 343)


if __name__ == '__main__':
    unittest.main()
