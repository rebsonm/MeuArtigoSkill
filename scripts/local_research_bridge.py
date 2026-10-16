#!/usr/bin/env python3
"""Opt-in local-only read bridge for the interactive Meu Artigo research map.

This is NOT a deployed ChatGPT connection or an authentication system. Only
explicit loopback browser sessions may query an authorized local project.
No remote networking, cross-origin access, external credentials, file writes,
scientific gate decisions or automatic canonical research-field commits.
"""
from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import hmac
import json
import os
from pathlib import Path
import secrets
import signal
import sys
import tempfile
from urllib.parse import urlsplit

from adaptive_method_guide import for_project, preview
from build_research_workspace import SCHEMA, model, render
from method_decision_dimensions import DIMENSIONS
from method_fill_preflight import LIMIT_BYTES, inspect
from method_routes import ROUTES

MAX_BODY_BYTES=32_768
BRIDGE_SCHEMA="MEU_ARTIGO_LOCAL_READ_BRIDGE_V1"
READ_PERMISSIONS=("snapshot","preflight")
FORBIDDEN_METHODS=("PUT","PATCH","DELETE")

class LocalResearchBridge(ThreadingHTTPServer):
    """A local transport, not a scientific authority or multiuser service."""
    daemon_threads=True
    allow_reuse_address=False
    def __init__(self, *, project: Path|None=None, route: str="QUALITATIVE",
                 mode: str="MINIMAL", address=("127.0.0.1",0)):
        if address[0]!="127.0.0.1":
            raise ValueError("Only explicit IPv4 loopback binding is permitted")
        if project is not None and not Path(project).is_dir():
            raise ValueError("The authorized project directory must exist")
        if project is not None and route!="QUALITATIVE":
            raise ValueError("Project mode and fictional route are mutually exclusive")
        if route not in ROUTES or mode not in ("MINIMAL","FULL"):
            raise ValueError("Unknown research method or presentation mode")
        self.project=Path(project).resolve() if project is not None else None
        self.route=route
        self.mode=mode
        self.session_token=secrets.token_urlsafe(32)
        super().__init__(address,ResearchHandler)
    @property
    def trusted_origin(self):
        return "http://127.0.0.1:"+str(self.server_port)
    @property
    def host(self):
        return "127.0.0.1:"+str(self.server_port)
    def snapshot(self) -> dict:
        result=model(project=self.project,route=self.route,mode=self.mode)
        result["local_bridge"]={
            "schema":BRIDGE_SCHEMA,
            "enabled":True,
            "session_token":None,
            "origin":self.trusted_origin,
            "read_only":True,
            "available_actions":list(READ_PERMISSIONS),
            "canonical_write":False,
            "gate_approval":False,
            "human_authenticated":False,
            "drive_sync_verified":False,
            "chat_host_connected":False,
        }
        return result

class ResearchHandler(BaseHTTPRequestHandler):
    server:LocalResearchBridge
    def log_message(self, format, *args):
        # Deliberately never log paths, tokens, request body or private inputs.
        return
    def _headers(self,status:int,ctype:str,length:int):
        self.send_response(status)
        self.send_header("Content-Type",ctype)
        self.send_header("Content-Length",str(length))
        self.send_header("Cache-Control","no-store, no-cache, max-age=0")
        self.send_header("Pragma","no-cache")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("X-Frame-Options","DENY")
        self.send_header("Referrer-Policy","no-referrer")
        self.send_header("Cross-Origin-Resource-Policy","same-origin")
        self.send_header("Cross-Origin-Opener-Policy","same-origin")
        self.send_header("X-Robots-Tag","noindex, nofollow")
        self.end_headers()
    def _output(self,status:int,data:bytes,ctype="application/json; charset=utf-8"):
        self._headers(status,ctype,len(data))
        self.wfile.write(data)
    def _json(self,status:int,obj:dict):
        self._output(status,json.dumps(obj,sort_keys=True,ensure_ascii=False,
                                      separators=(",",":")).encode("utf-8"))
    def _denied(self,status:int=403,code:str="ACCESS_DENIED"):
        self._json(status,{"error":code,"scientific_gate_approved":False,
                           "canonical_write":False})
    def _trusted_request(self):
        # Exact Host/Origin/Fetch Metadata checks avoid DNS rebinding,
        # ambient cross-site access and browser background requests.
        if self.headers.get("Host")!=self.server.host:
            return False
        origin=self.headers.get("Origin")
        if origin is not None and origin!=self.server.trusted_origin:
            return False
        site=self.headers.get("Sec-Fetch-Site")
        if site is not None and site not in ("same-origin","none"):
            return False
        if self.headers.get("Transfer-Encoding"):
            return False
        return True
    def _authorized_api(self):
        if not self._trusted_request():return False
        supplied=self.headers.get("X-Meu-Artigo-Session","")
        return hmac.compare_digest(supplied,self.server.session_token)
    def do_GET(self):
        if not self._trusted_request():
            return self._denied()
        # No path parameters, query leaks or reflection of user data.
        if self.path=="/":
            # Never serve private task titles, registered routes, or a session
            # secret to an unauthenticated GET. The browser receives only a
            # fictional shell and must bootstrap its session via the URL
            # fragment and explicit authenticated /api/snapshot fetch.
            shell=model(route="UNDECIDED")
            shell["local_bridge"]={
                "schema":BRIDGE_SCHEMA,"enabled":True,
                "origin":self.server.trusted_origin,
                "session_token":None,"read_only":True,
                "available_actions":list(READ_PERMISSIONS),
                "canonical_write":False,"gate_approval":False,
                "chat_host_connected":False,
            }
            try:
                html=render(shell,live=True)
            except (OSError,ValueError,TypeError,KeyError):
                return self._denied(409,"LOCAL_SHELL_UNAVAILABLE")
            return self._output(200,html.encode("utf-8"),"text/html; charset=utf-8")
        if self.path=="/api/snapshot":
            if not self._authorized_api():return self._denied()
            try:
                result=self.server.snapshot()
            except (OSError,ValueError,TypeError,KeyError):
                return self._denied(409,"PROJECT_SNAPSHOT_REQUIRES_RECONCILIATION")
            return self._json(200,result)
        return self._denied(404,"UNKNOWN_ENDPOINT")
    def do_POST(self):
        if self.path!="/api/preflight":
            return self._denied(404,"ENDPOINT_READ_ONLY_OR_UNKNOWN")
        if not self._authorized_api():return self._denied()
        if self.headers.get("Content-Type")!="application/json":
            return self._denied(415,"EXPECTED_APPLICATION_JSON")
        try:
            n=int(self.headers.get("Content-Length","-1"))
        except ValueError:
            return self._denied(400,"INVALID_REQUEST_SIZE")
        if n<1 or n>MAX_BODY_BYTES:
            return self._denied(413,"REQUEST_SIZE_NOT_ALLOWED")
        try:
            payload=json.loads(self.rfile.read(n).decode("utf-8"))
            if not isinstance(payload,dict) or set(payload)-{
                 "dimension","field","option_id","proposal"}:
                raise ValueError("Unsupported request")
            proposal=payload.get("proposal")
            if not isinstance(proposal,str) or len(proposal.encode("utf-8"))>LIMIT_BYTES:
                raise ValueError("Draft missing or too large")
            dimension=payload.get("dimension")
            field=payload.get("field")
            option=payload.get("option_id")
            if (dimension is not None and dimension not in DIMENSIONS) or \
               (field is not None and (not isinstance(field,str) or len(field)>96)) or \
               (dimension is not None and field is not None):
                raise ValueError("Invalid field selector")
            if option is not None and (not isinstance(option,str) or len(option)>96):
                raise ValueError("Invalid option id")
            if self.server.project is not None:
                guide=for_project(self.server.project,field=field,dimension=dimension)
            else:
                guide=preview(self.server.route,field=field,dimension=dimension)
            result=inspect(guide,proposal=proposal,option_id=option)
        except (OSError,ValueError,TypeError,KeyError,UnicodeError,json.JSONDecodeError):
            return self._denied(422,"INVALID_OR_UNAVAILABLE_METHOD_DRAFT")
        # No draft text or original decision rationale is returned.
        result["local_bridge_only"]=True
        result["canonical_write_possible_via_endpoint"]=False
        result["human_identity_authenticated"]=False
        return self._json(200,result)
    def do_PUT(self):return self._denied(405,"METHOD_NOT_ALLOWED")
    def do_PATCH(self):return self._denied(405,"METHOD_NOT_ALLOWED")
    def do_DELETE(self):return self._denied(405,"METHOD_NOT_ALLOWED")
    def do_OPTIONS(self):return self._denied(405,"CORS_NOT_SUPPORTED")

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("project",nargs="?",type=Path)
    p.add_argument("--preview-route",choices=ROUTES)
    p.add_argument("--mode",choices=("MINIMAL","FULL"),default="MINIMAL")
    p.add_argument("--port",type=int,default=0,
                   help="Loopback only; 0 selects an unused OS-assigned port")
    a=p.parse_args(argv)
    if a.project and a.preview_route:
        p.error("Specify either authorized project or fictional preview")
    if a.port<0 or a.port>65535:p.error("Invalid port")
    try:
        with LocalResearchBridge(project=a.project,
                  route=a.preview_route or "QUALITATIVE",
                  mode=a.mode,address=("127.0.0.1",a.port)) as server:
            # The URL fragment is a bearer credential. Never emit the
            # credential to stdout/stderr or an application log, because
            # orchestrators commonly retain the process output.
            # Create an owner-only directory and an exclusive 0600 file;
            # both are deleted after the local server stops normally.
            with tempfile.TemporaryDirectory(prefix=".meu-artigo-session-", dir=Path.home()) as temp:
                session_path=Path(temp)/"launch-url.txt"
                fd=os.open(session_path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
                with os.fdopen(fd,"w",encoding="utf-8") as handle:
                    handle.write(server.trusted_origin+"/#session="+server.session_token+"\n")
                # Intentionally constant stdout: not even a derived local
                # file path, project state or bound port is logged. The
                # operator locates the private file in their HOME directory.
                print("LOCAL_READ_ONLY_BRIDGE_READY",flush=True)
                # On POSIX, systemd/subprocess termination sends SIGTERM.
                # Arrange ordinary cleanup instead of leaving the private
                # session file behind. SIGKILL cannot be intercepted.
                old_handler=signal.getsignal(signal.SIGTERM)
                def _terminate(_signum,_frame):
                    raise SystemExit(0)
                try:
                    signal.signal(signal.SIGTERM,_terminate)
                    server.serve_forever(poll_interval=.2)
                finally:
                    signal.signal(signal.SIGTERM,old_handler)
        return 0
    except (OSError,ValueError) as exc:
        print("LOCAL_BRIDGE_ERROR: "+type(exc).__name__,file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
