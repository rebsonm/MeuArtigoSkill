#!/usr/bin/env python3
"""Offline safety contract: never execute privileged staging actions in CI."""
from pathlib import Path

root = Path(__file__).resolve().parent
boot = (root / "e05-vps-autonomous-bootstrap.sh").read_text()
status = (root / "e05-vps-autonomous-status.sh").read_text()
rollback = (root / "e05-vps-autonomous-rollback.sh").read_text()

required = (
    "OLD=f7bdf1b92d62163b1530549361416fc0789cf98b",
    "TARGET=3ed581f941767e2b15b0b4a2f782b24151985540",
    "PILOT_SHA=fab60a8a2a254461d1fcd1fc66e67d7e109ed760",
    '[[ "$(stat -c %h "$INDEX")" == 1 ]]',
    'chown -- "$OWNER:$OWNER" "$INDEX"',
    'runuser -u "$OWNER" -- /bin/bash -s',
    'e05-stage-preflight.sh "$TARGET"',
    "LoadCredential=control_plane_api_key:/etc/meu-artigo-e05/runtime-key",
    "Restart=always",
    "ProtectSystem=strict",
    "ProtectHome=yes",
    "--control-plane.api-key=",
    "systemctl enable --now",
    "E05_BOOTSTRAP_COMPLETE=YES",
)
for token in required:
    assert token in boot, "Missing fail-closed/autonomy contract: " + token

for name, content in (("bootstrap", boot), ("status", status), ("rollback", rollback)):
    executable_lines = [
        line.lstrip() for line in content.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    for line in executable_lines:
        assert "chown -R" not in line and "chmod -R" not in line
        assert "git reset --hard" not in line and "rm -rf" not in line
        assert "curl | bash" not in line and "wget | bash" not in line
    assert "meu-artigo-stage17/src" in content, name + ": pilot SHA guard missing"
assert "systemctl disable --now" in rollback
assert "git switch --detach" in rollback
assert "E05_RUNTIME_TUNNEL_READY=NOT_PROVEN_BY_SYSTEMD" in status
assert "MEU_ARTIGO_MCP_MULTIUSER" not in boot
print("E05_VPS_AUTONOMOUS_STATIC_CONTRACT_PASS: shell syntax, pinned E05 SHA, pilot integrity, least-privilege credential, restart, rollback.")
