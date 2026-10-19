#!/usr/bin/env python3
"""E05 read-only runtime key grammar audit.

Uses the official tunnel-client ValidateControlPlaneAPIKey grammar. Never
prints, stores, transmits or hashes the secret. Does not prove remote auth.
"""
import os
import re
import stat

KEY_FILE = "/etc/meu-artigo-e05/runtime-key"
OFFICIAL = re.compile(r"[0-9A-Za-z_-]+", re.ASCII)
MAX_READ_BYTES = 4096


def classify(raw: bytes) -> tuple[str, str, str]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return ("FAIL", "FAIL", "NON_UTF8_SECRET")
    official_value = text.strip()
    if not official_value:
        return ("FAIL", "FAIL", "EMPTY_SECRET")
    if OFFICIAL.fullmatch(official_value) is None:
        return ("FAIL", "FAIL", "UNSUPPORTED_CHARACTER")
    # Official CLI strips whitespace around file contents, whereas our
    # source-controlled launcher intentionally forbids any newline or CR.
    if text != official_value:
        return ("PASS", "FAIL", "WRAPPER_REJECTS_WHITESPACE")
    if len(raw) < 20 or len(raw) > 2048 or not raw.startswith(b"sk-"):
        return ("PASS", "FAIL", "WRAPPER_REJECTS_PREFIX_OR_LENGTH")
    return ("PASS", "PASS", "SYNTAX_ACCEPTED_REMOTE_UNVERIFIED")


def read_protected_key() -> tuple[str, bytes | None]:
    if os.geteuid() != 0:
        return ("ROOT_REQUIRED", None)
    fd = None
    try:
        fd = os.open(KEY_FILE, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
        metadata = os.fstat(fd)
        if not (stat.S_ISREG(metadata.st_mode) and metadata.st_uid == 0
                and stat.S_IMODE(metadata.st_mode) == 0o400
                and metadata.st_nlink == 1):
            return ("FILE_OWNER_MODE_OR_LINK_INVALID", None)
        value = os.read(fd, MAX_READ_BYTES + 1)
        if len(value) > MAX_READ_BYTES:
            return ("SECRET_SIZE_INVALID", None)
        return ("PROTECTED_READ_OK", value)
    except OSError:
        return ("UNREADABLE_OR_MISSING_KEY", None)
    finally:
        if fd is not None:
            os.close(fd)


def main() -> int:
    print("E05_KEY_AUDIT_SCHEMA=OFFICIAL_GRAMMAR_READONLY_V1")
    print("E05_KEY_AUDIT_MUTATIONS=NONE")
    source, raw = read_protected_key()
    print("E05_KEY_SOURCE=" + source)
    if raw is None:
        print("E05_KEY_OFFICIAL_GRAMMAR=NOT_TESTED")
        print("E05_KEY_WRAPPER_POLICY=NOT_TESTED")
        print("E05_KEY_CLASS=LOCAL_FILE_UNAVAILABLE")
        print("E05_KEY_REMOTE_AUTH=NOT_TESTED")
        return 2
    official, wrapper, category = classify(raw)
    print("E05_KEY_OFFICIAL_GRAMMAR=" + official)
    print("E05_KEY_WRAPPER_POLICY=" + wrapper)
    print("E05_KEY_CLASS=" + category)
    print("E05_KEY_REMOTE_AUTH=NOT_TESTED")
    print("E05_KEY_AUDIT_COMPLETE=YES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
