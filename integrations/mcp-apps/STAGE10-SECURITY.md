# MCP dashboard security boundary

The researcher's ChatGPT Google Drive connector reads the existing
Meu Artigo files, tables and canonical decisions. No source files,
Google access tokens, refresh grants or Drive folder mapping enter
the MCP. The assistant supplies **only a validated per-request
display projection** to `meu_artigo_painel`; the MCP returns it to
its view. This is a transient data-processing activity, not a
zero-knowledge service.

Controls: request-specific Auth0 verification; no cross-user storage;
no DB or source file access; no server-side snapshot cache; strict
projection field allowlist and UTF-8 size cap; no document bodies or
tokens; bounded gates/tasks; rejection on unexpected fields; no
automatic scientific approval; incomplete evidence never treated as
zero defects; UI HTML-escaped rendering; stale view cleared on
failed or missing tool result. Source provenance and human decisions
remain with the researcher's original Drive records.

Supported request: `meu_artigo_painel(locale?,mode?,snapshot?)`.
The `snapshot` is a summary of what the host has already read, not
a Google Drive path, a Google token or a request for the MCP to
access storage. See `README.md` for the strict schema.

`test:host-boundary` ensures direct Drive access remains disabled.
`test:host-projection` checks alternating user snapshots, rejection
of private/bulk content, and absence of cached prior projects.
These tests do not certify private transport logs, real-user Google
connection isolation or future server modifications.

Actual OAuth to ChatGPT, Nginx/TLS proxying, two-account Drive use,
data minimization consent, incident response and privacy review
must be accepted separately before public deployment.
