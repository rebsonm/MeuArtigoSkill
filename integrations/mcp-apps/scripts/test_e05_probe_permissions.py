#!/usr/bin/env python3
"""Verify non-root E05 probe traversal while root-only diagnostics stay private.

Runs only on an ephemeral GitHub Actions VM with sudo. No VPS credentials
or network connections are used.
"""
import os
import pathlib
import pwd
import subprocess
import tempfile

assert os.geteuid() == 0, "Requires root to emulate service-account access"
nobody = pwd.getpwnam("nobody")
run = lambda path, action: subprocess.run(
    ["runuser", "-u", "nobody", "--", "/usr/bin/test", action, str(path)],
    check=False, capture_output=True, timeout=10,
).returncode

with tempfile.TemporaryDirectory(prefix=".e05-private-", dir="/root") as private:
    private_path = pathlib.Path(private)
    secret = private_path / "launcher"
    secret.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    secret.chmod(0o755)
    assert run(secret, "-r") != 0, "A non-root user unexpectedly traversed /root"

with tempfile.TemporaryDirectory(prefix=".e05-doctor-", dir="/run") as root:
    probe = pathlib.Path(root)
    os.chown(probe, 0, nobody.pw_gid)
    probe.chmod(0o750)
    launcher = probe / "launcher"
    launcher.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    os.chown(launcher, 0, nobody.pw_gid)
    launcher.chmod(0o750)
    assert run(launcher, "-r") == 0, "Non-root service user cannot read /run probe"
    assert run(launcher, "-x") == 0, "Non-root service user cannot execute /run probe"
    assert run(launcher, "-w") != 0, "Non-root service user may modify root-owned probe"

print("E05_UNIX_PROBE_PERMISSIONS_PASS: /root denied, /run group readable/executable, write denied")
