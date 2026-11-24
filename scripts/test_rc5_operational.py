#!/usr/bin/env python3
"""Offline deterministic RC.5 checks, not live host or scientific validation."""
import unittest
from types import SimpleNamespace
from doi_recovery import rank_candidates, recover
class Recovery(unittest.TestCase):
    def setUp(self):
        self.r={'title':'A test of governance','author':'Mendes','year':'2024','journal':'Example Journal'}
        self.c={'title':self.r['title'],'authors':'Rebson Mendes','year':'2024','journal':'Example Journal','doi':'10.1234/example','source':'Crossref'}
    def test_unique_candidate_not_verification(self):
        x=rank_candidates(self.r,[self.c]);self.assertEqual(x['status'],'MATCH_CANDIDATE');self.assertFalse(x['verified_identity']);self.assertFalse(x['human_gate_approved'])
    def test_ambiguous(self): self.assertEqual(rank_candidates(self.r,[self.c,dict(self.c,doi='10.1234/other')])['status'],'AMBIGUOUS')
    def test_conflict(self): self.assertEqual(rank_candidates(self.r,[dict(self.c,year='2023')])['status'],'CONFLICT')
    def test_no_network_default(self): self.assertEqual(recover(self.r)['status'],'NOT_EXECUTED')
    def test_fallback(self):
        calls=[]
        def fake(provider,*a,**kw):
            calls.append(provider);return SimpleNamespace(status='ERROR' if provider=='crossref' else 'PARTIAL',rows=[] if provider=='crossref' else [self.c],executed_at='synthetic')
        self.assertEqual(recover(self.r,allow_network=True,lookup=fake)['status'],'MATCH_CANDIDATE');self.assertEqual(calls,['crossref','openalex'])
    def test_failure_not_absence(self):
        def fake(*a,**kw): return SimpleNamespace(status='RATE_LIMITED',rows=[],executed_at='synthetic')
        self.assertEqual(recover(self.r,allow_network=True,lookup=fake)['status'],'UNVERIFIED')
if __name__=='__main__': unittest.main(verbosity=2)
