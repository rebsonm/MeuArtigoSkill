# Connected Drive read-only hierarchy contract

The intended path is My Drive / Meu Artigo / ARTIGO_<topic>_<year>. The
optional read-only `scripts/drive_connected_hierarchy.py` checks folder-only
paginated search receipts and independent metadata observations. It never
authorizes creation, journal updates, publication or scientific gate decisions.

The receipt must record a root metadata lookup using alias `root`, exact
parent IDs, connector page requests, and explicit terminal `next_page_token`.
If an existing candidate is found, check its metadata again: matching folder
name, MIME type, ID, and immediate parent. Any duplicate, missing metadata,
cursor replay, parent mismatch or inconsistent type blocks.

Connected folder-only search does not include other MIME types. It therefore
cannot establish absence of a name conflict with a file, nor grant Drive write
permission. Remote create additionally requires an exhaustive all-MIME
provider listing plus durable journal/F7-F8 signed head/F9 CAS. Unknown
outcomes after a timeout are never retried automatically.

Do not commit real Drive IDs, project titles, credentials or read receipts
to a public repository. The script validates the shape of supplied observations,
not their authenticated provenance.
