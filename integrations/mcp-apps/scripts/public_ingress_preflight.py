#!/usr/bin/env python3
"""Read-only structural gate for a reviewed Nginx HTTPS MCP proxy candidate.

NO nginx changes, network calls, systemd operations, certificates read, or OAuth
access occur. A PASS is necessary but INSUFFICIENT for live deployment.
"""
from __future__ import annotations

import argparse
import json
import re
import stat
from pathlib import Path

REQUIRED_PATHS = frozenset({
    "/mcp",
    "/.well-known/oauth-protected-resource",
    "/.well-known/oauth-protected-resource/mcp",
    "/.well-known/openai-apps-challenge",
    "/",
})
UPSTREAM = "http://127.0.0.1:8085"
TEMPLATE_HOST = "YOUR_MCP_HOST.example"
TEMPLATE_CERT = "/REPLACE_WITH_CERTIFICATE_CHAIN.pem"
TEMPLATE_KEY = "/REPLACE_WITH_PRIVATE_KEY.pem"


def _require(flag: bool, code: str) -> None:
    if not flag:
        raise ValueError(code)


def inspect(text: str, *, host: str | None = None,
            require_cert_files: bool = False) -> dict:
    """Inspect expected-only directives, not a complete Nginx parser."""
    _require(isinstance(text, str) and len(text) <= 40_000,
             "PROXY_CONFIGURATION_INVALID")
    # Ignore comments; unknown active locations, includes and proxies are denied.
    clean = "\n".join(line.split("#", 1)[0] for line in text.splitlines())
    _require("include " not in clean and "location ~" not in clean
             and "return 200" not in clean, "PROXY_UNREVIEWED_DIRECTIVE")
    locations = re.findall(
        r"(?m)^\s*location\s+(=)?\s*([^\s{]+)\s*\{", clean)
    _require(len(locations) == len(REQUIRED_PATHS) and
             {path for _, path in locations} == REQUIRED_PATHS,
             "PROXY_LOCATION_ALLOWLIST_INVALID")
    for equal, route in locations:
        _require((route == "/" and equal == "") or
                 (route != "/" and equal == "="),
                 "PROXY_LOCATION_MATCH_NOT_EXACT")
    parts = {}
    for match in re.finditer(
        r"(?m)^\s*location\s+(=)?\s*([^\s{]+)\s*\{([^{}]*)\}", clean
    ):
        parts[match.group(2)] = match.group(3)
    _require(set(parts) == REQUIRED_PATHS, "PROXY_LOCATION_BODY_INVALID")
    for route in REQUIRED_PATHS:
        target = re.findall(r"(?m)^\s*proxy_pass\s+([^;]+);", parts[route])
        if route in {"/mcp", "/.well-known/oauth-protected-resource",
                     "/.well-known/oauth-protected-resource/mcp"}:
            _require(target == [UPSTREAM], "PROXY_TARGET_INVALID")
        else:
            _require(not target, "PROXY_UNEXPECTED_UPSTREAM")
    _require("return 404;" in parts["/"],
             "PROXY_DENY_DEFAULT_MISSING")
    _require("alias /var/lib/meu-artigo-verification/openai-apps-challenge;"
             in parts["/.well-known/openai-apps-challenge"],
             "PROXY_CHALLENGE_PATH_INVALID")
    for directive in (
        "listen 443 ssl;", "ssl_protocols TLSv1.2 TLSv1.3;",
        "ssl_session_tickets off;", "server_tokens off;",
        "client_max_body_size 256k;", "access_log off;",
        "add_header X-Content-Type-Options nosniff always;",
    ):
        _require(directive in clean, "PROXY_SECURITY_BOUNDARY_MISSING")
    for directive in (
        "proxy_set_header Authorization $http_authorization;",
        "proxy_set_header Origin $http_origin;",
        "proxy_set_header X-Forwarded-Proto https;",
        "proxy_buffering off;",
    ):
        _require(directive in parts["/mcp"],
                 "PROXY_MCP_HEADERS_MISSING")
    names = re.findall(r"(?m)^\s*server_name\s+([^;]+);", clean)
    certs = re.findall(r"(?m)^\s*ssl_certificate\s+([^;]+);", clean)
    keys = re.findall(r"(?m)^\s*ssl_certificate_key\s+([^;]+);", clean)
    _require(len(names) == len(certs) == len(keys) == 1,
             "PROXY_TLS_CONFIG_INVALID")
    if host is None:
        _require(names[0] == TEMPLATE_HOST and certs[0] == TEMPLATE_CERT
                 and keys[0] == TEMPLATE_KEY,
                 "PROXY_TEMPLATE_PLACEHOLDER_DRIFT")
        return {"status": "SOURCE_TEMPLATE_PASS", "live_tls": "NOT_TESTED",
                "oauth_pkce": "NOT_TESTED", "host_csp": "NOT_OBSERVED"}
    _require(bool(re.fullmatch(r"[a-z0-9]+(?:[.-][a-z0-9]+)+", host)) and
             not host.endswith((".example", ".test", ".invalid", ".local")),
             "PROXY_EXPECTED_HOST_INVALID")
    _require(names[0] == host and certs[0] != TEMPLATE_CERT
             and keys[0] != TEMPLATE_KEY and
             certs[0].startswith("/") and keys[0].startswith("/"),
             "PROXY_RENDERED_TLS_INCOMPLETE")
    if require_cert_files:
        for name in (certs[0], keys[0]):
            p = Path(name)
            _require(p.is_file(), "PROXY_TLS_FILE_MISSING")
        key_mode = stat.S_IMODE(Path(keys[0]).stat().st_mode)
        _require(key_mode & 0o077 == 0, "PROXY_TLS_KEY_TOO_PERMISSIVE")
    return {"status": "RENDERED_SOURCE_CHECK_PASS",
            "live_tls": "NOT_TESTED", "oauth_pkce": "NOT_TESTED",
            "host_csp": "NOT_OBSERVED"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--expected-host", default=None)
    parser.add_argument("--require-cert-files", action="store_true")
    args = parser.parse_args()
    try:
        if args.require_cert_files and not args.expected_host:
            raise ValueError("PROXY_EXPECTED_HOST_REQUIRED")
        verdict = inspect(args.config.read_text(encoding="utf-8"),
                          host=args.expected_host,
                          require_cert_files=args.require_cert_files)
    except (OSError, ValueError, UnicodeError) as exc:
        # Never echo paths or private system configuration into public CI.
        print(json.dumps({"status": "FAIL",
                          "code": str(exc) if isinstance(exc, ValueError)
                          else "PROXY_IO_ERROR"}))
        return 2
    print(json.dumps(verdict, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
