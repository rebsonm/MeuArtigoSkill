import unittest
from ai_execution_identity import identity_issues, identity_record, identity_label, model_known
from editorial_ai_disclosure import render_compact
class Identity(unittest.TestCase):
    def setUp(self):
        self.row=dict(Platform_or_tool="ChatGPT", Model_or_version="GPT-6.2", Date="2026-11-24", Model_provider="OpenAI", Execution_environment="WORK", Client_surface="DESKTOP_APP", Model_configuration="NOT_EXPOSED", Execution_timestamp="2026-11-24T17:43:00-03:00", Model_identification_source="HOST_METADATA", Environment_identification_source="USER_REPORTED", Meu_Artigo_version="1.0.0-rc.5.1")
    def test_valid(self): self.assertEqual(identity_issues(self.row),[])
    def test_generic(self): self.assertFalse(model_known("ChatGPT")); self.assertTrue(identity_issues(dict(self.row,Model_or_version="ChatGPT")))
    def test_unknown(self): self.assertEqual(identity_issues(dict(self.row,Model_or_version="NOT_EXPOSED", Model_identification_source="NOT_EXPOSED",Execution_timestamp="NOT_EXPOSED")),[])
    def test_bad_timestamp(self): self.assertTrue(identity_issues(dict(self.row,Execution_timestamp="2026-11-24T17:43:00")))
    def test_date_mismatch(self): self.assertTrue(identity_issues(dict(self.row,Date="2026-11-23")))
    def test_legacy(self): self.assertIn("NOT_RECORDED",identity_label(identity_record({"Platform_or_tool":"ChatGPT"})))
    def test_sources(self): self.assertTrue(identity_issues(dict(self.row,Model_identification_source="NOT_EXPOSED")))
    def test_reporting_keeps_modes_dates(self):
        a=dict(identity_record(self.row),category="SCREENING",tool="ChatGPT",purpose="Screen records")
        b=dict(identity_record(dict(self.row,Execution_environment="CHAT",Client_surface="WEB",Date="2026-11-25",Execution_timestamp="2026-11-25T10:00:00-03:00")),category="SCREENING",tool="ChatGPT",purpose="Screen records")
        out=render_compact(dict(uses=[a,b],errors=[],journal="Example",location="METHODS")); self.assertIn("environment=WORK",out); self.assertIn("environment=CHAT",out); self.assertIn("2026-11-24",out); self.assertIn("2026-11-25",out)
if __name__=='__main__': unittest.main(verbosity=2)
