# E05 autonomous VPS staging — operational transition

Updated 2026-10-18. This is a **private synthetic-only** E05 tunnel, not the live
multi-researcher production Plugin. It does not change Auth0, Google Drive,
production Nginx, the original stage17 process, main, or installed Plugins.

## Verified operator evidence before the migration

- E05 stage source: `f7bdf1b92d62163b1530549361416fc0789cf98b`,
  owned by `meuartigo-e05`, canonical stage, with a clean working tree.
- Protected original pilot source:
  `fab60a8a2a254461d1fcd1fc66e67d7e109ed760`.
- No matching foreground `tunnel-client` process on that account during the
  operator's read-only inspection; this is consistent with the previous
  `Session terminated`, without proving the precise root cause.
- The first stage update printed `E05_STAGE_FROM` and `E05_STAGE_TARGET`,
  then failed with `fatal: .git/index: index file open failed: Permission denied`.
  A likely narrow cause is index ownership after a previous root `git status`.
  Do not assume this until the bootstrap explicitly checks the file owner.
- GitHub ancestry: E05 commit is exactly 35 commits behind the last pinned
  CI-green candidate `3ed581f941767e2b15b0b4a2f782b24151985540`
  with zero divergent commits. That commit passed seven source CI checks.

## Source-controlled deliverables in this PR

- `scripts/e05-vps-autonomous-bootstrap.sh`: one-time, interactive, root-authorized
  **E05-only** update. It checks paths, owners, the protected pilot SHA, no
  existing service/process and clean Git state. It may repair **only the
  exact stage `.git/index` file** when that regular, unlinked file is owned
  by root. It uses the dedicated non-root account for Git fetch/switch and
  the full existing E05 staged source preflight.
- The bootstrap installs a dedicated `systemd` service with
  `Restart=always`, `LoadCredential` using a root-owned mode 0400 key
  file stored on the VPS, a strict service filesystem boundary and no public
  network listener. The restricted runtime key is entered once locally via
  an interactive terminal; it is never passed as a command-line value,
  echoed or committed. The client is started with
  `--control-plane.api-key=file:<systemd-credential-path>`.
- `scripts/e05-vps-autonomous-status.sh`: read-only operational summary;
  service active/enabled does not claim ChatGPT/OAuth/CSP is verified.
- `scripts/e05-vps-autonomous-rollback.sh`: explicit emergency E05
  service disable and staged-source return to last observed old SHA,
  preserving production and leaving the root-protected credential for
  separate revocation.
- `scripts/test_e05_vps_autonomous_contract.py`: **offline** negative
  inspection of unsafe shell patterns and structural assertions, plus
  `bash -n` checks in MCP Apps CI.

The bootstrap refuses to install into an existing service unit or run alongside
another E05 tunnel instance. If validation fails, inspect the sanitized STOP
code, do not escalate to recursive permission changes, `git reset --hard`
or an unauthenticated public endpoint. A successful local preflight cannot
guarantee systemd, tunnel health or private ChatGPT tool discovery.

## C.A.D.A. (Capturar · Atribuir · Definir prazo · Acompanhar)

| Task | Capturar: deliverable | Atribuir: owner | Definir prazo: dependency | Acompanhar: acceptance |
| --- | --- | --- | --- | --- |
| OPS-01 | Diagnose and repair stage index permission | VPS operator, dedicated stage user | Before stage update | Root-owned linked checks; only exact index file repaired if permitted |
| OPS-02 | Fast-forward only E05 to pinned approved SHA and preflight | VPS operator | After OPS-01 | `E05_SOURCE_AND_PREFLIGHT=PASS` |
| OPS-03 | Provision narrow persistent tunnel runtime credential | Authorized VPS operator | One-time bootstrap, after preflight | Root-only file, `LoadCredential`, no secret in logs or Git |
| OPS-04 | Install/start automatic-restart service | VPS operator / systemd | After OPS-03 | `E05_BOOTSTRAP_COMPLETE=YES` and `is-enabled/is-active` |
| OPS-05 | Verify process recovery and remote E05 tool | Human operator + ChatGPT tester | After OPS-04 | Actual private tunnel health, fixture ALPHA/BRAVO and effective CSP |
| GOV-01 | Review whole candidate independently | Independent reviewer | Before PR integration | Reviewer sign-off on exact head |
| DIST-01 | Production OAuth/Drive and public Plugin separately | Maintainer and consenting users | After integration/real acceptance | No public launch without separate authorization |

### Run principle

Operator receives the reviewed source snapshot as a downloadable package and
invokes bootstrap **once on the VPS itself** with a terminal and
`--apply`. After successful service enable/start, the Windows computer is
not a tunnel dependency. The ongoing Google Drive access belongs only to
each researcher's ChatGPT connector: it must NOT migrate to this VPS.

This document alone does **not** prove bootstrap execution. Until actual VPS
output is reported, OPS-01 through OPS-04 are `PREPARED_NOT_DEPLOYED`
and the original R02 acceptance is `OPEN`.

Official background: https://developers.openai.com/api/docs/guides/secure-mcp-tunnels
