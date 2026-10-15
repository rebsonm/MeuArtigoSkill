"""Interactive read-only offline research workspace: engineering fixtures.

No user research, browser-host plugin installation, source validation, or
researcher authentication is claimed by this suite.
"""
from __future__ import annotations
import csv
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import build_research_workspace as app
from method_routes import MGMT, new_profile
from init_project import TABLES

class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]
        self.script_texts=[]
        self._script=False
    def handle_starttag(self,tag,attrs):
        data=dict(attrs)
        if "id" in data:self.ids.append(data["id"])
        if tag=="script":self._script=True
    def handle_data(self,data):
        if self._script:self.script_texts.append(data)
    def handle_endtag(self,tag):
        if tag=="script":self._script=False

def csv_file(path,headers,rows):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,headers)
        writer.writeheader()
        writer.writerows([{h:r.get(h,"") for h in headers} for r in rows])

class WorkspaceUiTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.project=self.root/"study"
        self.m=self.project/MGMT
        self.m.mkdir(parents=True)
        (self.m/"PROJECT_CONFIG.json").write_text(json.dumps({
            "method_route":"QUALITATIVE","method_route_governance_required":True,
            "presentation_mode":"MINIMAL","storage_mode":"GOOGLE_DRIVE"}))
        (self.m/"METHOD_PROFILE.json").write_text(json.dumps(new_profile("QUALITATIVE")))
        (self.m/"CONTINUIDADE.md").write_text(
            "# Fictional continuity\nNext valid action: CADA-0001\nPRIVATE_CONTINUITY_COMMENT")
        csv_file(self.m/"11_CADA_Control.csv",TABLES[f"{MGMT}/11_CADA_Control.csv"],[
            {"CADA_ID":"CADA-0001","Status":"READY","Title":"Fictional project task",
             "Execution_mode":"AUTONOMOUS","Assigned_to":"AGENT",
             "Next_action":"SENSITIVE_UNDISCLOSED_TASK_INSTRUCTION",
             "Scientific_stage":"01"}])
        csv_file(self.m/"18_Human_Validation_Gates.csv",
                 TABLES[f"{MGMT}/18_Human_Validation_Gates.csv"],[
            {"GATE_ID":f"GATE-{i:04d}","Status":"READY",
             "Decision":"PENDING","Scientific_stage":str(i).zfill(2)}
             for i in range(1,8)])
        csv_file(self.m/"17_Decision_Log.csv",
                 ["DEC_ID","Decision_type","Decision_question","Decision",
                  "Status","Decided_by","Trace_ID","Rationale"],[
            {"DEC_ID":"DEC-0001","Decision_type":"METHOD",
             "Decision_question":"SENSITIVE_PRIVATE_RESEARCH_QUESTION",
             "Decision":"QUALITATIVE","Status":"PROPOSED",
             "Decided_by":"","Trace_ID":"TRACE-0001",
             "Rationale":"SECRET_LONG_HUMAN_RATIONALE"}])
        csv_file(self.m/"13_Traceability_Log.csv",
                 ["Trace_ID","Notes"],[{"Trace_ID":"TRACE-0001",
                                       "Notes":"CONFIDENTIAL_SOURCE_SENTENCE"}])

    def test_fictional_model_no_approvals_or_fake_science(self):
        m=app.model(route="QUALITATIVE")
        self.assertEqual(m["schema"],app.SCHEMA)
        self.assertFalse(m["is_project_bound"])
        self.assertIsNone(m["overview"]["scientific_progress_percent"])
        self.assertFalse(m["overview"]["independent_scientific_validation"])
        self.assertFalse(m["overview"]["canonical_drive_sync_verified"])
        self.assertFalse(m["permissions"]["automatic_write_possible"] if "automatic_write_possible" in m["permissions"] else False)
        self.assertEqual(m["permissions"]["canonical_write"],"NOT_AVAILABLE_IN_THIS_UI")
        self.assertEqual(m["permissions"]["human_scientific_approval"],"NOT_AVAILABLE_IN_THIS_UI")
        self.assertEqual(len(m["method_guides"]["dimensions"]),5)
        self.assertEqual(len(m["tasks"]["columns"]),4)

    def test_all_routes_and_unlisted_method_possible(self):
        for route in ("UNDECIDED","QUALITATIVE","QUANTITATIVE",
                      "MIXED_METHODS","DESIGN_SCIENCE","SYSTEMATIC_REVIEW",
                      "CONCEPTUAL_THEORY","INTEGRATIVE_REVIEW",
                      "PROBLEMATIZING_REVIEW"):
            with self.subTest(route=route):
                m=app.model(route=route)
                intro=m["method_guides"]["overview"]
                self.assertIn("OTHER_NOT_LISTED",{x["id"] for x in intro["options"]})
                if route!="UNDECIDED":
                    self.assertEqual(set(m["method_guides"]["dimensions"]),
                                     {"sampling","sources","analysis","inference","reporting"})
                    self.assertTrue(all(d["options"][-1]["id"]=="OTHER_NOT_LISTED"
                         for d in m["method_guides"]["dimensions"].values()))

    def test_local_project_snapshot_keeps_private_records_out(self):
        m=app.model(project=self.project)
        self.assertTrue(m["is_project_bound"])
        self.assertEqual(m["active_route"],"QUALITATIVE")
        self.assertFalse(m["overview"]["canonical_drive_sync_verified"])
        self.assertIn("CANONICAL_STORAGE_NOT_VERIFIED",m["continuation"]["blockers"])
        self.assertEqual(m["tasks"]["columns"],
            ["ID Tarefa","Tarefa","Responsável execução","Prazo"])
        report=json.dumps(m)
        for confidential in ("SECRET_LONG_HUMAN_RATIONALE",
                             "SENSITIVE_PRIVATE_RESEARCH_QUESTION",
                             "CONFIDENTIAL_SOURCE_SENTENCE",
                             "SENSITIVE_UNDISCLOSED_TASK_INSTRUCTION",
                             "PRIVATE_CONTINUITY_COMMENT"):
            self.assertNotIn(confidential,report)
        self.assertFalse(m["decision_continuity"]["human_identity_authenticated"])
        self.assertFalse(m["decision_continuity"]["scientific_gate_approved"])

    def test_html_contains_interactive_controls_and_offline_security(self):
        page=app.render(app.model(route="QUANTITATIVE"))
        tags=Tags()
        tags.feed(page)
        needed={"dimension","options","compare","show-all","draft",
                "review-draft","clear-draft","draft-feedback",
                "research-model","last-decision","next-action",
                "cada-rows","blockers"}
        self.assertTrue(needed.issubset(tags.ids))
        self.assertIn("connect-src 'none'",page)
        self.assertIn("default-src 'none'",page)
        self.assertNotIn("https://",page)
        self.assertNotIn("src=",page)
        self.assertIn("addEventListener",page)
        self.assertIn("textContent",page)
        self.assertNotIn("innerHTML",page)
        self.assertNotIn("localStorage",page)
        self.assertNotIn("fetch(",page)
        self.assertNotIn("methodological_option_recommendation_independently_validated",page) # only backend contracts, no false badge

    def test_markup_embedding_escapes_script_termination_and_surrogates(self):
        m=app.model()
        payload="</script><script>alert('x')</script>&"
        m["decision_continuity"]["next_action"]["explanation"]=payload
        page=app.render(m)
        self.assertNotIn(payload,page)
        self.assertNotIn("</script><script>alert",page)
        self.assertIn(r"\u003c/script",page)
        # Reversibly parse the protected JSON script content.
        match=re.search(r'<script type="application/json" id="research-model">(.*?)</script>',page,re.S)
        self.assertIsNotNone(match)
        self.assertEqual(json.loads(match.group(1))["decision_continuity"]["next_action"]["explanation"],payload)

    def test_generated_html_created_once_0600_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as folder:
            dest=Path(folder)/"workspace.html"
            raw=app.render(app.model(route="QUALITATIVE"))
            app.save(dest,raw)
            self.assertEqual(dest.read_text(),raw)
            self.assertEqual(dest.stat().st_mode & 0o777,0o600)
            with self.assertRaisesRegex(ValueError,"new name"):
                app.save(dest,"overwrite attempt")
            self.assertEqual(dest.read_text(),raw)
            other=Path(folder)/"reused-link"
            other.symlink_to(dest)
            with self.assertRaisesRegex(ValueError,"new name"):
                app.save(other,raw)

    def test_cli_fictional_preview_no_file_writes_except_requested_output(self):
        with tempfile.TemporaryDirectory() as folder:
            dest=Path(folder)/"demo.html"
            cmd=[sys.executable,str(ROOT/"scripts/build_research_workspace.py"),
                 "--preview-route","MIXED_METHODS","--output",str(dest)]
            run=subprocess.run(cmd,text=True,capture_output=True)
            self.assertEqual(run.returncode,0,run.stderr)
            r=json.loads(run.stdout)
            self.assertFalse(r["scientific_approvals"])
            self.assertFalse(r["canonical_writes"])
            self.assertFalse(r["installed_chatgpt_plugin"])
            self.assertEqual(r["snapshot_kind"],"FICTIONAL_PREVIEW_NOT_A_REAL_PROJECT")
            duplicate=subprocess.run(cmd,text=True,capture_output=True)
            self.assertEqual(duplicate.returncode,2)
            self.assertTrue(dest.is_file())

    def test_no_project_mutation_when_generating_local_html(self):
        before={p.name:p.read_bytes() for p in self.m.iterdir() if p.is_file()}
        with tempfile.TemporaryDirectory() as folder:
            dest=Path(folder)/"authorized-local-snapshot.html"
            out=subprocess.run([sys.executable,str(ROOT/"scripts/build_research_workspace.py"),
                str(self.project),"--output",str(dest)],capture_output=True,text=True)
            self.assertEqual(out.returncode,0,out.stderr)
            self.assertNotIn("SECRET_LONG_HUMAN_RATIONALE",dest.read_text())
            self.assertIn("Fictional project task",dest.read_text())
        after={p.name:p.read_bytes() for p in self.m.iterdir() if p.is_file()}
        self.assertEqual(before,after)

    @unittest.skipUnless(shutil.which("node"),"Node unavailable in this environment")
    def test_client_javascript_is_syntactically_valid(self):
        page=app.render(app.model())
        match=re.search(r'<script>\s*(\(function\(\)\{.*?\}\)\(\);)\s*</script>',page,re.S)
        self.assertIsNotNone(match)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"workspace.js"
            path.write_text(match.group(1))
            test=subprocess.run(["node","--check",str(path)],capture_output=True,text=True)
            self.assertEqual(test.returncode,0,test.stderr)

if __name__=="__main__":
    unittest.main()
