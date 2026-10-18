# E05 VPS — source-level runtime fix (2026-10-18)

**Scope:** draft PR #89, E05 synthetic staging only. This change has **NOT** been installed on the real VPS; production pilot, main, Auth0, Google Drive, and installed Plugin are unchanged.

## Observed operator evidence and known integration defect

- E05 was moved to source `3ed581f941767e2b15b0b4a2f782b24151985540` with `E05_SOURCE_AND_PREFLIGHT=PASS`.
- Its systemd service was created and enabled but exited with status 1. This is not host acceptance.
- The old bootstrap started the client with `--profile meu-artigo-e05` even though the previously working E05 setup selected the explicit file `/opt/meu-artigo-e05/tunnel-profiles/meu-artigo-e05.yaml` using `--profile-file`. The source-level mismatch is proven; its causal contribution to the VPS process exit has **not** been established.
- An earlier transient diagnostic referenced the wrong credential source; its `control_plane_api_key=FAIL` does not prove the protected runtime credential was invalid. An additional wrapper repair rejected the systemd credential declaration even though the original bootstrap contained `LoadCredential=control_plane_api_key:/etc/meu-artigo-e05/runtime-key`.

## Integrated source change

1. `scripts/e05-vps-runtime-launch.sh` becomes the **single reviewed launcher** copied by the staging bootstrap, replacing the generated inline shell.
2. It runs only under `meuartigo-e05`, requires the original **explicit** `--profile-file` path, and reads the per-service credential copy from `$CREDENTIALS_DIRECTORY/control_plane_api_key` supplied by systemd `LoadCredential`.
3. It invokes `doctor --json` and `run` with **identical** profile and key-file arguments, never a guessed transient unit credential path. The doctor report is parsed in memory and only generic status codes are emitted, without raw key, YAML or diagnostic text.
4. A persistent local configuration failure exits with status **78**; `RestartPreventExitStatus=78` prevents an endless restart loop due to a missing local credential, profile or invalid doctor configuration. Transient runtime failures retain `Restart=always`.
5. Offline executable regressions with synthetic credentials cover success, missing or malformed key, doctor failure, missing profile and credential directory, installer-template consistency, and prohibited destructive operations.

## C.A.D.A. execution register

| Task | Owner | Dependency | Status and closing evidence |
| --- | --- | --- | --- |
| OPS-01 stage Git permission | VPS operator | Previously required | **DONE on VPS**; Git update resumed |
| OPS-02 E05 source/preflight | VPS operator | OPS-01 | **DONE on VPS** at prior source pin |
| OPS-03 executable/secret storage | VPS operator | OPS-02 | Files present; actual remote authorization not verified |
| OPS-04 canonical launcher and unit contract | Engineering/CI | Source SHA | **SOURCE FIXED**, exact-SHA CI and independent review required |
| OPS-05 stable E05 on VPS | Authorized remote operator | Reviewed source deployment | **OPEN**: active/enabled process, no config restart loops and actual tunnel connectivity still need remote evidence |
| R02 ChatGPT host acceptance | Host tester | OPS-05 | **OPEN**: ALPHA/BRAVO, 10 screens, stale-state clearing and effective CSP |
| R01 independent cumulative review | Independent reviewer | Final SHA | **OPEN** |
| R03–R10 | Maintainer and consenting testers | Prior gates | **OPEN**: merge, OAuth, Drive, workflow, private/public distribution |

Original plan: D01–D15 source-engineered in candidate, D16–D18 unaccepted, **0/10 final go-live gates closed**. Do not request repetitive user-run repair scripts; completing an existing VPS systemd deployment requires a securely authorized remote execution channel, which this conversation does not have.

Upstream contracts: [OpenAI tunnel-client configuration](https://github.com/openai/tunnel-client/blob/master/docs/configuration.md), [doctor JSON semantics](https://github.com/openai/tunnel-client/blob/master/cmd/client/doctor_command.go), and [systemd credentials](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html).
