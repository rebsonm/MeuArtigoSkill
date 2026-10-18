# Meu Artigo — cross-conversation master handoff and final acceptance plan

**Recorded:** 2026-10-18, America/Fortaleza. **Scope:** actionable, source-controlled continuity plan for any next conversation. This document does not authorize merge, production deployment, Auth0/Drive changes, Plugin installation or publication.

**Source links:** [Draft PR #89](https://github.com/rebsonm/MeuArtigoSkill/pull/89); [Issue #83](https://github.com/rebsonm/MeuArtigoSkill/issues/83); [living acceptance matrix](REMAINING-MILESTONES.md); [original 18 deliveries](PLANO-MESTRE-18-ENTREGAS.md); [E05 root-cause notes](E05-VPS-ROOT-CAUSE-FIX.md).

## A. Verified baseline and true project counts

- Repository rebsonm/MeuArtigoSkill; candidate branch security/stage17-auth0-origin-hardening-20261018; Draft PR #89 targets main, and remains unmerged.
- Before adding this plan, last exact candidate SHA was 3311ba30ddf9e856b5301204c30e05da97e7904c with 7/7 successful GitHub Actions. On resumption, **fetch the NEW current PR head and its own checks**, not only this historical SHA.
- Of the 18 original deliveries, D01–D15 are technically implemented in the candidate, primarily with offline/synthetic tests. **D16, D17, D18 remain OPEN**. This is not 83% production readiness.
- The ten independent final acceptance gates **R01–R10 are all OPEN: 0/10 fully accepted**. Do not reset numbering or create spurious gates for each fix.
- Isolated VPS E05: deployed older source SHA 3ed581f941767e2b15b0b4a2f782b24151985540, previously demonstrated E05_SOURCE_AND_PREFLIGHT=PASS. Service meu-artigo-e05-tunnel.service exists and is enabled, but **last observed not active**.
- Original production/pilot stage17 checkout (/opt/meu-artigo-stage17/src, SHA fab60a8a2a254461d1fcd1fc66e67d7e109ed760) was observed unchanged. Do not modify or replace it while repairing isolated E05.
- Last real VPS evidence: E05_ACTIVATE_PRECONDITIONS=PASS; E05_ACTIVATE_PINNED_SOURCE=VERIFIED; E05_ACTIVATE_PROBE_USER_ACCESS=PASS; E05_RUNTIME_DOCTOR_CONFIG_SOURCE=PASS; E05_RUNTIME_DOCTOR_PROFILE_LOAD=PASS; E05_RUNTIME_DOCTOR_CONTROL_PLANE_API_KEY=FAIL; E05_RUNTIME_STOP=DOCTOR_LOCAL_CONTRACT_FAILED; E05_ACTIVATE_STOP=SAME_IDENTITY_CREDENTIAL_DOCTOR_FAILED.
- The E05 transient launcher path/permissions bug is **resolved**; the present blocker is specifically **local runtime key reading or formatting/config resolution**. The offline doctor error does NOT establish a revoked/unauthorized remote key, nor does it prove that the runtime is connected.
- Some software version labels have drifted: historical notes mention Skill beta.6 published, beta.9 source candidate, private Plugin beta.8 metadata embedding older beta.6. Verify exact currently installed source/manifests before release.
- User preference: move forward in large objective milestones, not a repeating test-error-test-error loop. Never rerun unaffected npm/Git/bootstrap/binary install as a troubleshooting default.

## B. Architecture and non-negotiable boundaries

1. Each researcher accesses their own individual Google Drive through their own ChatGPT Google Drive connection and consent. The MCP/VPS must not hold Google OAuth tokens, persist research file contents, directly read individual Drive records, or cache researcher-specific state across calls.
2. ChatGPT/Skill reads permitted sources, checks canonical identity and projects only bounded allowlisted UI fields for a single MCP call. UI is not proof of scientific truth or evidence quality.
3. Seven scientific approval gates always require human decisions. Never invent a scientific gate approval, study participant, deadline, evidence, article or citation.
4. E05 accepts only fixed, fictional synthetic ALPHA/BRAVO fixtures. Never send project files, private data, token values, Drive IDs, Auth0 secrets or full profile YAML there.
5. Do not merge PR #89, modify main, Nginx/Auth0, deploy production or update/publicize the Plugin without the gate-specific maintainer authorization. Existing stage17 pilot is protected.
6. Fail closed, PIN source by SHA/Git blob, retain rollback, never relax CSP/auth or print credentials/raw sensitive logs. A green CI validates its specific synthetic/source suite, not real service/host/Drive behavior.

## C. Complete 18-delivery ledger

| Delivery | Deliverable | Candidate state | Remaining proof |
|---|---|---|---|
| D01 | Freeze baseline/SHAs | Historical source documented | Final integration SHA |
| D02 | Map functions/overlaps | Source documented | Cumulative review |
| D03 | Unified Skill/ChatGPT/Drive/MCP architecture | Source implemented | Approve minimized projection/security |
| D04 | Dependency/security/CodeQL/CI | CI implemented | Check exact final SHA and review |
| D05 | Integrate predecessor changes safely | Candidate source | Review accumulated diff |
| D06 | Drive root/parent canonical reuse | Synthetic PASS | Real authorized Drive readback |
| D07 | Drive F1–F4 | Synthetic PASS | Real provider permission checks |
| D08 | Drive F5–F9, CAS, journal | Synthetic PASS | Provider-backed concurrency and receipts |
| D09 | Ten-screen blue dashboard | Synthetic PASS | ChatGPT-hosted interactive acceptance |
| D10 | Single MCP UI server | Synthetic PASS | Real tunnel discovery/rendering |
| D11 | Auth0 OAuth resource server | Offline PASS | Real PKCE A/B |
| D12 | Source provenance/scientific integrity advisories | Source implemented | Independent science review |
| D13 | Reproducible scientific diagnostics | Synthetic PASS | External claims/evidence assessment |
| D14 | Multi-method options/fictional projection | Synthetic PASS | Human methods assessment |
| D15 | Skill/native/MCP/HTML integrated horizontal tests | Synthetic PASS | Real user/browser/provider acceptance |
| **D16** | **Review and merge one PR** | **OPEN** | R01, R02, R03, R04 |
| **D17** | **Real VPS/ChatGPT/Auth0/Drive and workflow** | **OPEN** | R02 and R05–R08 |
| **D18** | **Private pilot and optional public release** | **OPEN** | R09/R10 and explicit approval |

The original 18 deliveries, 12 planned UX concepts, current 10 HTML screens, 21 C.A.D.A. tabs and 10 final gates are distinct inventories. Do not add them together.

## D. Ten final R01–R10 acceptance gates: responsible person, dependency and evidence

| Gate | Responsible | Prerequisite/dependency | Exact closing evidence | State |
|---|---|---|---|---|
| R01 independent cumulative review | Independent technical/security and science reviewer | Candidate HEAD stabilized; may run parallel with R02 | Signed SHA-scoped assessment of complete cumulative diff, security/knowledge/permission boundaries | OPEN |
| R02 isolated E05 in real ChatGPT | Authorized VPS operator + actual ChatGPT tester | Fix local key; start and confirm remote tunnel | E05 systemd healthy, ChatGPT ALPHA to BRAVO in same session, 10 screens, language, focus, resize, cleanup and effective CSP | BLOCKED |
| R03 explicit merge decision | Maintainer | R01+R02 accepted | Specific SHA authorization, PR #89 merge into main | OPEN |
| R04 merged main reproducibility | CI + maintainer | R03 | Green CI on merge SHA and package/hash reproducibility | OPEN |
| R05 actual production HTTPS/Auth0 endpoint | Authorized infrastructure operator | R04, separate production consent | Real TLS/proxy/Auth0 health, sanitized logs, security and rollback proof | OPEN |
| R06 real OAuth PKCE A/B | Two consenting users | R05 | Login, denial, revoke/expiry, separate sessions and origin/scope checks | OPEN |
| R07 real Drive F1–F9 A/B | Two consenting Drive owners | R06 | Canonical folder, CAS, journal, recovery, strict cross-user isolation, provider receipts | OPEN |
| R08 full researcher article end-to-end | Researcher + reviewer | R07 | Real create/resume, sources, evidence, tasks, seven human gates, workflow and recovery | OPEN |
| R09 controlled private Plugin pilot | Maintainer and invited testers | R08 plus installation consent | Version aligned source/Plugin/embedded UI, private installation, pilot acceptance and rollback | OPEN |
| R10 public publication (optional) | Maintainer and platform reviewer | R09 + separate public authorization | Approved public listing and external researcher acceptance | OPEN |

Private usable beta can be considered achieved at R09. Public listing only at R10; neither has an honest guaranteed calendar end date while dependencies/third parties remain open.

## E. Seven execution batches; finish without inventing milestones

**Batch A = R01 and R02 in parallel:** local key grammar audit and permitted correction, official E05 doctor PASS, start existing E05 (no npm/git reinstall), real ChatGPT ALPHA/BRAVO/ten screens/CSP, independent reviewer signoff.

**Batch B = R03/R04:** resolve reviewer findings, explicit SHA-scoped merge permission, integrate one PR, verify main CI and artifacts.

**Batch C = R05:** authorized production HTTPS, Auth0, Nginx, health and rollback, separately from the synthetic E05/pilot.

**Batch D = R06/R07:** two consenting real user accounts, OAuth PKCE and complete isolated Drive F1–F9/CAS/journal receipts.

**Batch E = R08:** one complete real research/authoring cycle including method choices, grounded provenance, task traceability, human gates and recovery.

**Batch F = R09:** coherent Plugin/Skill/UI versions, controlled installation and private researcher pilot.

**Batch G = R10:** optional public submission and external platform evaluation, only on explicit separate authorization.

These batches are execution groupings, **not seven extra R-gates**.

## F. Immediate verified root-cause work for Batch A

Upstream client references: openai/tunnel-client cmd/client/doctor_command.go and pkg/runtimeconfig/config.go and docs/configuration.md (GitHub master). The official API key flag may use file:/absolute/path or env:CONTROL_PLANE_API_KEY. File references are read and surrounding whitespace trimmed. The validation grammar permits ONLY ASCII letters, digits, underscore and hyphen (no dot, spaces, punctuation). Local structured doctor check control_plane_api_key FAIL is either a key-source/config or key-grammar problem; it is **not remote authentication**.

The checked-in E05 canonical launcher currently adds its own policy: starts with sk-, 20–2048 bytes and no CR/LF/NUL. Its last real run entered the official doctor (so the preliminary launcher format test passed). The client nevertheless rejected the key config. **Do not assume** why until isolated key grammar is examined.

**Next exact non-destructive action:** review the current source at integrations/mcp-apps/scripts/e05-runtime-key-audit.py and its synthetic test; on the authorized VPS, run only the SHA-verified version against the already existing protected /etc/meu-artigo-e05/runtime-key. It validates file mode and ownership, reports only bounded categories (not key, key hash, key length, or any content), never starts/stops the service or contacts OpenAI.

**Decision logic:**

| Sanitized local classification | Permitted targeted follow-through |
|---|---|
| Missing/unreadable or wrong owner/mode | Check only the credential file and systemd LoadCredential mapping; keep key private |
| Empty, non-UTF8 or unsupported characters | Obtain a real **OpenAI Tunnels Runtime API key** through approved account controls, replace root-only credential atomically with explicit owner authorization; do not paste key in chat or use an admin/model API key |
| Official grammar PASS but wrapper whitespace/prefix policy FAIL | Resolve policy difference/format under authorization; never print/transform secret blindly |
| Official grammar and wrapper both PASS but doctor still FAIL | Investigate CLI/file reference/preference under the same systemd UID, not key rotation by speculation |
| Doctor PASS but service remote readiness FAIL | Now move to remote tunnel authorization, polling/network reachability and health; never weaken Auth0/CSP |

Only when local doctor PASS: run already reviewed, rollback-guarded source file integrations/mcp-apps/scripts/e05-vps-activate-only.sh under its current SHA. This explicitly checks the original pilot, environment and checksum and does not repeat npm/Git/bootstrap. Then independently verify remotely exposed MCP and real ChatGPT R02; a stable local process alone is not R02 acceptance.

## G. Prior incidents resolved: never repeat

1. Root-owned .git/index prevented stage checkout: fixed narrowly.
2. Client binary missing from PATH: official client deployed from checksum-pinned release.
3. Named --profile differed from formerly working explicit --profile-file: canonical launcher now uses explicit profile.
4. Parsing raw/explanatory logs yielded false possible causes: now use doctor --json check IDs only.
5. Previous transient LoadCredential was incorrectly sourced from another unit's runtime directory: original trusted source is root-only /etc/meu-artigo-e05/runtime-key.
6. A script mistakenly claimed the unit did not declare a key: original unit does declare LoadCredential.
7. Preflight accidentally launched a script under /root as unprivileged E05 user: fixed via root-owned group-readable /run launcher; real POSIX permission tests added.
8. Latest operator evidence: config source PASS, profile PASS, control_plane_api_key FAIL. This is the ONLY immediate VPS blocker, not grounds to redo all other work.

## H. Continuity protocol for every future session

1. Start by fetching **current** Draft PR #89 HEAD (not stored stale SHA), exact-head GitHub Actions, this handoff, original 18-delivery plan and living matrix, and Issue #83.
2. Compare source HEAD with last real operator output. Never pretend the current source was deployed to VPS merely because GitHub updated.
3. Preserve C.A.D.A. in each update: capture concrete deliverable, assign owner, define dependency rather than invented date, accompany with evidence and next action.
4. Make at most one root-cause-directed change per incident. Keep same R-gate IDs and avoid redundant GitHub issue/PR updates.
5. If authenticated SSH is unavailable to the assistant, state that clearly and give only **one** small, independently reviewed operator command, with source SHA/hash and finite-state output expected. Do not ask to paste passwords or secrets.
6. No main merge, production Auth0/Nginx/Drive, private/public Plugin or publication without corresponding authorization.
7. Never declare R01 independent reviewer signoff from author-side CI, R02 ChatGPT acceptance from an offline doctor, nor remote authorization from local key grammar.
8. Repo is English-first under strict release audit; user-facing continuity can be provided in Portuguese outside tracked source files.

## I. Paste-ready resumption prompt

Continue the Meu Artigo project using the durable handoff in rebsonm/MeuArtigoSkill, file integrations/mcp-apps/CONTINUITY-HANDOFF.md, current Draft PR #89, Issue #83, REMAINING-MILESTONES.md and PLANO-MESTRE-18-ENTREGAS.md. Fetch current HEAD, exact-head CI, and compare with the last VPS operator evidence. Do not ask me to repeat our history. D01–D15 are source-implemented; D16–D18 are open; R01–R10 remain 0/10 accepted unless new verified proof exists. E05 last passed launcher access, config source and profile but failed official control_plane_api_key; next action is only the protected local key grammar audit, then one credential/source fix supported by evidence, official doctor PASS and guarded one-pass service activation. Do not repeat Git/npm/reinstall, touch original pilot, merge main, access a different researcher's Drive, update Auth0 or publish the Plugin without authorization. Complete the seven batches R01/R02 -> R03/R04 -> R05 -> R06/R07 -> R08 -> R09 -> optional R10. Show a concise C.A.D.A. matrix with evidence, owner, dependency and next step. Never conflate source CI, VPS runtime, ChatGPT host or scientific human acceptance.

**Terminal definition:** R01–R09 genuinely accepted = usable private beta; R01–R10 genuinely accepted and separate public permission = public release.
