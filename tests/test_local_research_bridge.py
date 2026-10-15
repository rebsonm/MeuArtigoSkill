"""Loopback research bridge regression tests: synthetic, no real projects.

The bridge is not a ChatGPT connection and is not a user-authentication
mechanism. It must not save/approve/change a canonical project.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from build_research_workspace import model,render
from local_research_bridge import LocalResearchBridge,BRIDGE_SCHEMA
from method_routes import MGMT,new_profile
from init_project import TABLES

def csv_file(path,headers,rows):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,headers)
        writer.writeheader()
        writer.writerows([{h:r.get(h,"") for h in headers} for r in rows])

class LoopbackBridgeTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        root=Path(self.t.name)
        self.project=root/"fictional_project"
        self.m=self.project/MGMT
        self.m.mkdir(parents=True)
        (self.m/"PROJECT_CONFIG.json").write_text(json.dumps({
            "method_route":"QUALITATIVE","method_route_governance_required":True,
            "presentation_mode":"MINIMAL","storage_mode":"GOOGLE_DRIVE"}))
        (self.m/"METHOD_PROFILE.json").write_text(json.dumps(new_profile("QUALITATIVE")))
        (self.m/"CONTINUIDADE.md").write_text(
            "# Synthetic continuity\nNext valid action: CADA-0001\nPRIVATE_NOT_EXPORTED")
        csv_file(self.m/"11_CADA_Control.csv",TABLES[f"{MGMT}/11_CADA_Control.csv"],[
            {"CADA_ID":"CADA-0001","Status":"READY","Title":"Fictional task",
             "Assigned_to":"AGENT","Execution_mode":"AUTONOMOUS",
             "Next_action":"SENSITIVE_NEXT_ACTION_NO_EXPORT","Scientific_stage":"01"}])
        csv_file(self.m/"18_Human_Validation_Gates.csv",
                 TABLES[f"{MGMT}/18_Human_Validation_Gates.csv"],[
                    {"GATE_ID":f"GATE-{i:04d}","Status":"READY",
                     "Decision":"PENDING","Scientific_stage":str(i).zfill(2)}
                    for i in range(1,8)])
        csv_file(self.m/"17_Decision_Log.csv",
                 ["DEC_ID","Decision_type","Decision_question","Decision",
                  "Status","Decided_by","Trace_ID","Rationale"],[])
        csv_file(self.m/"13_Traceability_Log.csv",["Trace_ID","Notes"],[])
        self.before={p.name:p.read_bytes() for p in self.m.iterdir() if p.is_file()}
        self.server=LocalResearchBridge(project=self.project)
        self.addCleanup(self.server.server_close)
        self.thread=threading.Thread(target=self.server.serve_forever,
                                     kwargs={"poll_interval":.01},daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)

    def stop_server(self):
        self.server.shutdown()
        self.thread.join(timeout=2)

    def req(self,path="/",*,method="GET",payload=None,headers=None):
        hdr=dict(headers or {})
        if payload is not None:
            hdr["Content-Type"]="application/json"
            data=json.dumps(payload).encode("utf-8")
        else:
            data=None
        r=Request(self.server.trusted_origin+path,data=data,method=method,headers=hdr)
        try:
            with urlopen(r,timeout=3) as f:
                return f.status,dict(f.headers),f.read().decode("utf-8")
        except HTTPError as e:
            return e.code,dict(e.headers),e.read().decode("utf-8")

    def token(self):
        return {"X-Meu-Artigo-Session":self.server.session_token,
                "Origin":self.server.trusted_origin}

    def assert_unchanged(self):
        self.assertEqual({p.name:p.read_bytes() for p in self.m.iterdir() if p.is_file()},
                         self.before)

    def test_only_loopback_binding_is_allowed(self):
        with self.assertRaisesRegex(ValueError,"loopback"):
            LocalResearchBridge(address=("0.0.0.0",0))
        with self.assertRaisesRegex(ValueError,"loopback"):
            LocalResearchBridge(address=("::",0))
        self.assertEqual(self.server.server_address[0],"127.0.0.1")

    def test_served_page_contains_only_current_session_and_local_csp(self):
        status,headers,html=self.req()
        self.assertEqual(status,200)
        self.assertIn("connect-src 'self'",html)
        self.assertNotIn("connect-src 'none'",html)
        self.assertIn(self.server.session_token,html)
        self.assertIn('"enabled":true',html)
        self.assertIn("Atualizar dados locais",html)
        self.assertEqual(headers["Cache-Control"],"no-store, no-cache, max-age=0")
        self.assertEqual(headers["X-Frame-Options"],"DENY")
        self.assertEqual(headers["Referrer-Policy"],"no-referrer")
        self.assertNotIn("PRIVATE_NOT_EXPORTED",html)
        self.assertNotIn("SENSITIVE_NEXT_ACTION_NO_EXPORT",html)
        self.assert_unchanged()

    def test_offline_page_cannot_embed_live_credential(self):
        data=model(route="QUALITATIVE")
        offline=render(data)
        self.assertIn("connect-src 'none'",offline)
        self.assertNotIn(self.server.session_token,offline)
        with self.assertRaisesRegex(ValueError,"credentials"):
            render(self.server.snapshot())
        with self.assertRaisesRegex(ValueError,"credentials"):
            render(data,live=True)

    def test_anonymous_api_read_and_draft_are_denied(self):
        s,_,body=self.req("/api/snapshot")
        self.assertEqual(s,403)
        self.assertEqual(json.loads(body)["error"],"ACCESS_DENIED")
        s,_,body=self.req("/api/preflight",method="POST",payload={
            "field":"tradition","proposal":"Fictional case study with constraints."})
        self.assertEqual(s,403)
        self.assert_unchanged()

    def test_cross_site_origin_denied_even_with_valid_secret(self):
        s,_,body=self.req("/api/snapshot",headers={
            "X-Meu-Artigo-Session":self.server.session_token,
            "Origin":"https://untrusted.example"})
        self.assertEqual(s,403)
        s,_,body=self.req("/api/snapshot",headers={
            "X-Meu-Artigo-Session":self.server.session_token,
            "Sec-Fetch-Site":"cross-site"})
        self.assertEqual(s,403)
        self.assert_unchanged()

    def test_authenticated_refresh_reads_updated_canonical_state(self):
        s,headers,raw=self.req("/api/snapshot",headers=self.token())
        self.assertEqual(s,200)
        data=json.loads(raw)
        self.assertEqual(data["local_bridge"]["schema"],BRIDGE_SCHEMA)
        self.assertTrue(data["local_bridge"]["read_only"])
        self.assertFalse(data["local_bridge"]["canonical_write"])
        self.assertFalse(data["local_bridge"]["gate_approval"])
        self.assertFalse(data["local_bridge"]["chat_host_connected"])
        self.assertEqual(data["tasks"]["items"][0]["task"],"Fictional task")
        # External change is visible on the next requested snapshot.
        records=self.m/"11_CADA_Control.csv"
        rows=list(csv.DictReader(records.open(encoding="utf-8-sig",newline="")))
        rows[0]["Title"]="Updated fictional task title"
        csv_file(records,TABLES[f"{MGMT}/11_CADA_Control.csv"],rows)
        s,_,raw=self.req("/api/snapshot",headers=self.token())
        self.assertEqual(s,200)
        self.assertEqual(json.loads(raw)["tasks"]["items"][0]["task"],
                         "Updated fictional task title")

    def test_local_preflight_checks_real_python_guard_and_never_writes(self):
        payload={"field":"tradition","proposal":"PENDING"}
        s,_,raw=self.req("/api/preflight",method="POST",payload=payload,
                           headers=self.token())
        self.assertEqual(s,200)
        result=json.loads(raw)
        self.assertEqual(result["status"],"BLOCKED_BEFORE_WRITING")
        self.assertIn("PLACEHOLDER_NOT_EVIDENCE",
                      {f["code"] for f in result["findings"]})
        self.assertFalse(result["scientific_gate_approved"])
        self.assertFalse(result["canonical_write_possible_via_endpoint"])
        self.assertFalse(result["draft_text_persisted"])
        self.assert_unchanged()

    def test_substantive_draft_is_not_echoed_or_scientifically_approved(self):
        private="CONFIDENTIAL_FICTIONAL_METHOD_DRAFT_553218 explaining an original bounded research design."
        s,_,raw=self.req("/api/preflight",method="POST",
                          payload={"field":"analysis_logic","proposal":private},
                          headers=self.token())
        self.assertEqual(s,200)
        info=json.loads(raw)
        self.assertNotIn(private,raw)
        self.assertEqual(info["status"],"DRAFT_REQUIRES_HUMAN_REVIEW")
        self.assertFalse(info["semantic_suitability_verified"])
        self.assertFalse(info["human_identity_authenticated"])
        self.assertFalse(info["safe_to_write_automatically"])
        self.assert_unchanged()

    def test_wrong_method_or_unknown_field_is_rejected(self):
        cases=[
            {"field":"inference_aim","proposal":"CAUSAL"},
            {"dimension":"fake","proposal":"A defensible fictional method."},
            {"field":"analysis_logic","dimension":"analysis",
             "proposal":"A defensible fictional method."},
            {"field":"tradition","option_id":"INVENTED",
             "proposal":"A bounded and fictional analytic choice."},
        ]
        for params in cases:
            with self.subTest(params=params):
                s,_,raw=self.req("/api/preflight",method="POST",
                                 payload=params,headers=self.token())
                self.assertEqual(s,422)
                self.assertNotIn("defensible fictional",raw)
        self.assert_unchanged()

    def test_no_put_patch_delete_options_or_remote_cors(self):
        for method in ("PUT","PATCH","DELETE","OPTIONS"):
            with self.subTest(method=method):
                status,headers,body=self.req("/api/snapshot",
                    method=method,headers=self.token())
                self.assertEqual(status,405)
                self.assertNotIn("Access-Control-Allow-Origin",headers)
        self.assert_unchanged()

    def test_requests_cannot_select_arbitrary_paths_or_inject_query(self):
        for path in ("/api/snapshot?download=1","/api/../METHOD_PROFILE.json",
                     "/api/write","/favicon.ico"):
            with self.subTest(path=path):
                s,_,raw=self.req(path,headers=self.token())
                self.assertIn(s,(403,404))
                self.assertNotIn("SECRET_",raw)
        self.assert_unchanged()

    def test_visual_screen_has_only_manual_local_refresh_and_no_auto_commit(self):
        s,_,html=self.req("/")
        self.assertEqual(s,200)
        self.assertIn('addEventListener("click",refreshSnapshot)',html)
        self.assertIn('bridgeRequest("/api/preflight"',html)
        self.assertIn('bridgeRequest("/api/snapshot"',html)
        self.assertNotIn('bridgeRequest("/api/approve"',html)
        self.assertNotIn('bridgeRequest("/api/write"',html)
        self.assertNotIn("setInterval(",html)
        self.assertNotIn("localStorage",html)

if __name__=="__main__":
    unittest.main()
