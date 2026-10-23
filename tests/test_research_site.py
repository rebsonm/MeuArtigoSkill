"""Approved blue site: brand, accessibility, canonical source and safety tests."""
from __future__ import annotations
import base64
import copy
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import stat
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import build_research_site as site
import build_research_workspace as workspace

class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.metas=[]
    def handle_starttag(self,tag,attrs):
        if tag=="meta":
            self.metas.append(dict(attrs))

class ResearchSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.preview=workspace.model(route="QUALITATIVE",mode="MINIMAL")
        cls.html=site.render_site(cls.preview)

    def test_ten_approved_sections_preserved(self):
        for label in ("Visão geral","Etapas","Tarefas C.A.D.A.",
                      "Fontes e buscas","Evidências","Validações","Métodos",
                      "Rastreabilidade","Submissão","Sincronização"):
            with self.subTest(label=label):
                self.assertIn(label,self.html)
        self.assertIn("function go(page)",self.html)

    def test_selected_method_blue_text_is_readable(self):
        self.assertIn(".option.selected h3{color:#073b91",self.html)
        self.assertIn(".option.selected p{color:#334f78",self.html)
        self.assertIn(".option.selected .pill.green{color:#fff;background:#0B57D0",self.html)
        self.assertIn('aria-pressed=',self.html)

    def test_logo_matches_real_repository_svg(self):
        item=re.search(r'src="data:image/svg\+xml;base64,([A-Za-z0-9+/=]+)"',self.html)
        self.assertIsNotNone(item)
        self.assertEqual(hashlib.sha256(base64.b64decode(item.group(1))).digest(),
                         hashlib.sha256((ROOT/"assets"/"icon.svg").read_bytes()).digest())
        self.assertNotIn('class="mark">MA</span>',self.html)

    def test_csp_blocks_network_and_external_scripts(self):
        parser=MetaParser()
        parser.feed(self.html)
        policies=[x["content"] for x in parser.metas if x.get("http-equiv")=="Content-Security-Policy"]
        self.assertEqual(len(policies),1)
        for keyword in ("default-src 'none'","connect-src 'none'",
                        "object-src 'none'","img-src data:","form-action 'none'"):
            self.assertIn(keyword,policies[0])
        self.assertNotIn('<script src=',self.html)

    def test_preview_fictional_only(self):
        self.assertIn('"kind":"ILLUSTRATIVE_PREVIEW"',self.html)
        self.assertIn("Nenhum dado real",self.html)
        self.assertEqual(site.project_site_model(self.preview)["kind"],"ILLUSTRATIVE_PREVIEW")

    def canonical(self):
        m=copy.deepcopy(self.preview)
        m["is_project_bound"]=True
        m["active_route"]="QUALITATIVE"
        m["overview"]["human_gate_approvals_recorded"]=1
        m["tasks"]["items"]=[{"id":"CADA-001","task":"Revisar fontes",
                               "execution_owner":"Pesquisador","deadline":None}]
        m["human_gates"]={"items":[{"id":"GATE-0001","approval_documented":True},
                                   {"id":"GATE-0002","approval_documented":False}],"total":7}
        m["decision_continuity"]["next_action"]={
            "code":"RESEARCHER_REVIEW_REQUIRED",
            "explanation":"Conferir protocolo antes de avançar.",
            "responsible":"HUMAN_RESEARCHER"}
        return m

    def test_canonical_projection_only_whitelisted_fields(self):
        v=site.project_site_model(self.canonical())
        self.assertEqual(v["kind"],"CANONICAL_LOCAL_SNAPSHOT")
        self.assertEqual(v["documented_gate_count"],1)
        self.assertEqual(v["tasks"][0]["id"],"CADA-001")
        self.assertFalse(v["canonical_drive_sync_verified"])
        self.assertFalse(v["automatic_scientific_approval"])
        self.assertFalse(v["canonical_writes_allowed"])

    def test_no_uncontrolled_javascript_from_project_text(self):
        m=self.canonical()
        bad="</script><script>alert(1)</script> &"
        m["tasks"]["items"][0]["task"]=bad
        m["PRIVATE_TOKEN"]="DO-NOT-PUBLISH-TOKEN"
        html=site.render_site(m)
        self.assertNotIn(bad,html)
        self.assertNotIn("DO-NOT-PUBLISH-TOKEN",html)
        self.assertIn(r"\u003c/script\u003e",html)
        self.assertIn(r"\u0026",html)
        self.assertIn("const e=(value)=>",html)

    def test_missing_canonical_rows_are_blocked(self):
        m=self.canonical()
        m["tasks"]["items"]=None
        with self.assertRaisesRegex(ValueError,"SITE_CANONICAL_PROJECTION_INCOMPLETE"):
            site.render_site(m)

    def test_no_local_bridge_tokens_allowed(self):
        m=self.canonical()
        m["local_bridge"]={"enabled":True,"session_token":"SECRET"}
        with self.assertRaisesRegex(ValueError,"SITE_LOCAL_BRIDGE_NOT_SUPPORTED"):
            site.render_site(m)

    def test_bad_schema_rejected(self):
        m=self.canonical()
        m["schema"]="INVALID"
        with self.assertRaisesRegex(ValueError,"SITE_SNAPSHOT_SCHEMA_INVALID"):
            site.render_site(m)

    def test_preview_cli_writes_0600_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"demo.html"
            self.assertEqual(site.main(["--preview-route","QUALITATIVE",
                                        "--output",str(path)]),0)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode),0o600)
            previous=path.read_bytes()
            self.assertEqual(site.main(["--preview-route","QUALITATIVE",
                                        "--output",str(path)]),2)
            self.assertEqual(path.read_bytes(),previous)

    def test_website_builder_does_not_call_cloud_apis(self):
        code=(ROOT/"scripts"/"build_research_site.py").read_text()
        for prohibited in ("boto3","requests.","files.create","push_once("):
            self.assertNotIn(prohibited,code)

if __name__=="__main__":
    unittest.main()
