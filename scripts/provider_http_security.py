"""Network transport for explicitly opted-in academic metadata APIs.

Only fixed HTTPS provider endpoints are permitted. HTTP redirects are blocked
instead of forwarding bearer or Zotero credentials to another host. This
client does not authenticate academic content or confer provider entitlement.
"""
from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler

from bibliographic_connectors import ProviderFailure

ALLOWED = {
    "https://api.openalex.org/works": "exact",
    "https://api.crossref.org/works": "exact",
    "https://api.semanticscholar.org/graph/v1/paper/search": "exact",
    "https://api.unpaywall.org/v2/": "prefix",
    "https://api.opencitations.net/index/v2/citation-count/doi:": "prefix",
    "https://api.zotero.org/users/": "prefix",
}
REDIRECT_CODES = {301, 302, 303, 307, 308}


class NoExternalRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Return None so urllib produces an HTTPError. Never retransmit a
        # token or an institutional request to any Location URL.
        return None


def validate_url(url: str) -> None:
    if (not isinstance(url, str) or url.strip() != url
            or any(ord(char) < 32 or ord(char) == 127 for char in url)):
        raise ProviderFailure("UNSUPPORTED_ENDPOINT")
    try:
        target = urlsplit(url)
        no_port = target.port is None
    except ValueError:
        raise ProviderFailure("UNSUPPORTED_ENDPOINT") from None
    if (target.scheme != "https" or target.username is not None
            or target.password is not None or not no_port
            or target.fragment or not target.hostname
            or not target.netloc.isascii()):
        raise ProviderFailure("UNSUPPORTED_ENDPOINT")
    allowed = False
    for base, match in ALLOWED.items():
        p = urlsplit(base)
        if target.netloc != p.netloc:
            continue
        if match == "exact" and target.path == p.path:
            allowed = True
        elif match == "prefix" and target.path.startswith(p.path) and len(target.path) > len(p.path):
            allowed = True
    if not allowed:
        raise ProviderFailure("UNSUPPORTED_ENDPOINT")


def read_json(url: str, headers: dict[str, str], *,
              max_bytes: int, timeout: int = 20, missing_status: str = "INVALID_REQUEST"):
    validate_url(url)
    try:
        request = Request(url, headers=headers, method="GET")
        # Per-request opener: never install a global handler.
        with build_opener(NoExternalRedirect()).open(request, timeout=timeout) as response:
            body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise ProviderFailure("RESPONSE_TOO_LARGE")
        return json.loads(body)
    except HTTPError as exc:
        code = exc.code
        if code in REDIRECT_CODES:
            raise ProviderFailure("REDIRECT_BLOCKED") from None
        if code == 401:
            raise ProviderFailure("AUTH_FAILED") from None
        if code == 403:
            raise ProviderFailure("LICENSE_BLOCKED") from None
        if code == 429:
            raise ProviderFailure("RATE_LIMITED") from None
        if code == 404:
            raise ProviderFailure(missing_status) from None
        raise ProviderFailure("PROVIDER_UNAVAILABLE" if code >= 500 else "INVALID_REQUEST") from None
    except (TimeoutError, URLError, OSError):
        raise ProviderFailure("NETWORK_ERROR") from None
    except (UnicodeError, ValueError, TypeError):
        raise ProviderFailure("INVALID_RESPONSE") from None
