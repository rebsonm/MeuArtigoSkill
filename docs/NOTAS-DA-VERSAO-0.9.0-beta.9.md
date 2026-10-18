# Meu Artigo v0.9.0-beta.9 — source candidate

**Status: source candidate only. NOT a GitHub release, installed Plugin
update, or approved publication.** The separately verified published
standalone Skill remains v0.9.0-beta.6.

## Scope of the candidate

The beta.9 candidate consolidates the draft integration work through PR
#89, subject to independent cumulative source review and approval.

- Display-only MCP Apps dashboard: ten-screen interface, fixed synthetic
  ALPHA/BRAVO E05 test with a user-confirmed hover jitter correction.
  This acceptance covers a **private synthetic tunnel**, not real Drive
  synchronization or a published Plugin.
- Research continuity and Drive F1–F9: guarded folder reuse, duplicate
  detection, single-attempt synthetic create, independent journal proof and
  F7/F8/F9 trusted-head checks. **No real multiuser authorized Drive
  readback has been accepted**; real file mutations are not authorized.
- Scientific boundaries: seven decisions remain human-controlled;
  restored strict-advisory, report-writer and 24-case synthetic holdout
  regressions are **software tests**, not external scholarly validation.
- Security: fail-closed origin configuration for optional Auth0 bearer
  transport; no direct Google credentials or original document bodies
  in the generic MCP server; restrictive declared CSP allowlists.
  Effective ChatGPT iframe CSP and real OAuth/PKCE sign-in remain unverified.
- Packaging: deterministic independent public/private plugin candidates
  with a manifest/Skill checksum consistency gate. A private Plugin
  requires a **separately verified** registered production app, while
  the public With MCP submission keeps the server association outside
  the ZIP.

## Versioning and release guarantees

- Candidate source `VERSION`: `0.9.0-beta.9`.
- Candidate `README`, `CITATION.cff` and changelog refer to
  `0.9.0-beta.9`, but `CITATION.cff` omits a publication date until
  publication is actually authorized and completed.
- `OFFICIAL_SKILL_RELEASE` remains `0.9.0-beta.6` to avoid
  misrepresenting an unpublished candidate as the GitHub release.
- The user's existing private ChatGPT Plugin currently reports metadata
  `0.9.0-beta.8` but its embedded `skills/meu-artigo/VERSION` is
  `0.9.0-beta.6`. Updating that Plugin is a **separate future action**
  after real-host checks and explicit approval; the mere creation of a
  beta.9 package does not replace it.
- An all-green CI build does not certify scientific results, access to
  another researcher's Drive, a successfully installed private Plugin,
  OpenAI directory review or real security controls.

## Outstanding approvals before shipping

1. Obtain a second-person independent review of the cumulative GitHub
   diff and a maintainer decision regarding the old #65/#66 branches.
2. Verify the production MCP endpoint, Auth0 OAuth scopes and exact
   browser-origin/CSP policy through a non-synthetic real ChatGPT test.
3. With two consenting researchers, verify separate Google Drive
   authorizations and access denials A→B and B→A.
4. Freeze a review SHA and rerun the complete release, MCP,
   security, Chromium and CodeQL workflows on the exact commit.
5. Receive separate authorizations for: main merge, production
   deployment, private Plugin update and public submission.
6. Set a real publication date and create the tagged release only after
   the authorized release has been performed.

No automatic release, Plugin install, service restart or researcher
account access is performed by this source-candidate change.
