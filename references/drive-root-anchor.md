# Canonical My Drive parent — Meu Artigo (root safety rule)

## New and resumed project hierarchy

The *one canonical entry point* for all new and resumed Google Drive
projects is the user's **My Drive root**, not the currently open folder:

    My Drive/
      Meu Artigo/
        ARTIGO_<short-title>_<YYYY>/
          00_Gestao_e_Continuidade/
          01_Auditoria_de_Novidade/
          02_Buscas_e_Exports/
          03_Screening_e_FullText/
          04_Evidencias_e_Sintese/
          05_Manuscrito/
          06_Submissao/
          99_Arquivo_Historico/

Each article has an independent project root with the existing scientific
folder tree. "Meu Artigo" is the common parent container only — it is NOT
a replacement for each article folder, and its own root is never a corpus.

Never use the last visited Drive folder, a previously returned child ID, a
folder matching by display name elsewhere, or a chat-generated URL as the
parent of a new project. Never create another "Meu Artigo" inside an article
or another existing subfolder.

## Required provider lookup before any folder-create proposal

1. With authorized Google Drive access, use the **official files.get**
   \`fileId=root\` alias to observe the true My Drive root folder. Read
   its actual ID; do not call a shared-drive or arbitrary folder "root".
2. List all **direct children of this observed root ID**, not a keyword search
   over all Drive. Retrieve **all MIME types** and every \`nextPageToken\`;
   reject \`incompleteSearch\`, partial scans, duplicate file IDs and
   conflicting results. Compare the exact case-sensitive name \`Meu Artigo\`.
3. If exactly one *folder* matches, fetch its metadata by the returned ID
   and require \`parents == [REAL_MY_DRIVE_ROOT_ID]\`, expected name,
   folder MIME type, and not trashed. **Reuse it**, do not create.
4. If more than one matching item exists, or a file/shortcut with that
   exact name is found, **block for reconciliation**. Never arbitrarily
   select a winner, rename, merge or delete.
5. If no matching root child exists, report
   \`CHECK_PARENT_FOR_GUARDED_CREATE\` with name \`Meu Artigo\` and
   **parent ID = actual My Drive root ID**. This is a request for the
   durable journal / F7-F8 signed CAS creation flow. The read-only
   verifier itself returns \`create_permitted=false\` and never calls POST.
6. After any externally authorized creation, obtain a **new** complete
   direct-root scan and read exact metadata. A network error after a
   possible side effect is NOT permission to try the POST again.
7. Inspect the contents of the verified \`Meu Artigo\` folder for a
   project folder with the requested project name, again using all MIME
   types and full pagination. A single exact folder may be reused only
   after independent \`files.get\` confirms its parent is the container.
8. If the requested article is missing there, perform an additional
   paginated, exact-name folder discovery over accessible Drive items.
   A same-name project found under another parent **blocks duplication**
   and requires explicit reconciliation. A match claimed globally but
   absent from the direct parent scan also blocks.
9. Only with a verified container parent and no contradictory observations
   may a new article project be **proposed** for the guarded create
   flow with \`parents=[CANONICAL_MEU_ARTIGO_CONTAINER_ID]\`.
   For internal project subfolders, use the actual verified project ID,
   then the correct verified immediate parent of each planned child.
10. Only after the parent-to-child hierarchy and every file's actual
    parent and content readback are checked can Drive delivery be
    reported complete. Approval of scientific gates remains separate.

**The host MUST set explicit \`parents\` on every folder-create request**;
Google Drive can otherwise default a new folder to My Drive's root.
Project-specific subfolders must never inherit whichever directory the
researcher or tool happened to open. Official Drive folder documentation:
https://developers.google.com/workspace/drive/api/guides/folder

## Included source-level controls

- \`scripts/drive_root_anchor.py\`: validates exact root/container/article
  hierarchy, rejects ambiguity, and builds a new root-bound delivery-plan
  \`root_scope\` with the three unique IDs.
- \`scripts/drive_root_live_preflight.py\`: optional **read-only**
  authenticated official Drive v3 lookups for actual My Drive metadata,
  paginated direct children, existing projects and misplaced same-name
  projects. Without a separately authorized token the CLI blocks.
- \`scripts/drive_delivery.py\`: validates any bound \`root_scope\`
  against the project's \`drive_root_id\` and \`project_folder\`.
- \`scripts/drive_create_guard.py\`: its **external CLI** requires a
  root-bound plan before it can initialize or prepare a creation intent.
  The old in-process synthetic-fixture tests remain test-only.
- These tools **do not** create or move folders themselves. They cannot
  authenticate a model-authored scan transcript or manufacture a Drive
  credential. Real creation is still blocked until the previously
  specified F7-F8 trusted-journal acceptance is live.

## Legacy/mislocated projects

Existing projects stored elsewhere must **not be moved automatically**.
Moving them can break existing paths, citations, sharing permissions,
integrations and continuity. Classify them as
\`LEGACY_LOCATION_REVIEW_REQUIRED\`, preserve canonical data and source IDs,
present the exact observed parent chain and request a deliberate researcher
migration decision. Before migration, no new folders should be created under
the old incorrectly nested root.

A legacy, unscoped plan may be read for audit only; the external folder
guard CLI now blocks new creation from such a plan until the canonical
root scope has been verified. Never rewrite a previous F7 journal plan
hash merely to force a migration. A migration is a governed transition with
new agreed state, independent checkpoint proof and preserved prior history.

## Acceptance levels

- **Source-level safety contracts:** offline synthetic tests.
- **Read-only authenticated provider observation:** can verify a real
  existing root/container/project when a separately authorized executor
  provides credentials and actually runs.
- **Live creation/repair acceptance:** NOT demonstrated by these helpers.
  Requires actual F7/F8 trusted journal, a real independent head authority,
  non-idempotent create fault injection, recovery and user-authorized scope.
- **Scientific research validity and usability:** require separate human
  research review; CI does not establish either.

## Responsibility and provenance

The researcher (user) established the permanent "Meu Artigo" My Drive
folder rule and owns the original research methodology, canonical choices
and authorization for any migration/release. The assistant wrote this
guard, code, tests and instructions. Independent Google/AWS provider
observations and GitHub CI are labeled separately and never confused
with scientific sign-off or legal ownership assignments.
