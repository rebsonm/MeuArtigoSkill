"""Recoverable update of C.A.D.A., continuity and the derived dashboard.

Single authorized local writer only. Neither the journal nor its hashes
authenticate a researcher, prove a scientific result, or verify Drive sync.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
from uuid import uuid4

from transaction_coordinator import require_no_conflict

MGMT = "00_Gestao_e_Continuidade"
MARKER = ".pending_cada_continuity"
FILES = (
    MGMT + "/11_CADA_Control.csv",
    "CONTINUIDADE.md",
    MGMT + "/15_CADA_Dashboard.csv",
)


class PendingCADAContinuity(RuntimeError):
    pass


def journal_dir(root: Path) -> Path:
    return Path(root) / MGMT / MARKER


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sync_bytes(path: Path, data: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def _manifest(journal: Path) -> dict:
    path = journal / "manifest.json"
    if not path.is_file() or path.is_symlink():
        raise PendingCADAContinuity("CADA_JOURNAL_MANIFEST_MISSING")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise PendingCADAContinuity("CADA_JOURNAL_MANIFEST_INVALID") from exc
    if (not isinstance(value, dict) or value.get("schema_version") != 1
            or value.get("state") not in {"PREPARED", "COMMITTED"}
            or not isinstance(value.get("entries"), list)
            or len(value["entries"]) != len(FILES)
            or [e.get("path") for e in value["entries"] if isinstance(e, dict)]
               != list(FILES)):
        raise PendingCADAContinuity("CADA_JOURNAL_MANIFEST_INVALID")
    for entry in value["entries"]:
        if (not isinstance(entry, dict)
                or not all(isinstance(entry.get(k), str)
                           and len(entry[k]) == 64
                           and all(c in "0123456789abcdef" for c in entry[k])
                           for k in ("before_sha256", "after_sha256"))):
            raise PendingCADAContinuity("CADA_JOURNAL_MANIFEST_INVALID")
    return value


def recover(root: Path) -> dict:
    """Explicit recovery of a verified partial local write.

    If any canonical file was independently altered after interruption,
    leave the journal untouched and request manual reconciliation.
    """
    root = Path(root).resolve()
    require_no_conflict(root, allow=("cada_continuity",))
    journal = journal_dir(root)
    if not journal.exists() and not journal.is_symlink():
        return {"status": "NO_PENDING_CADA_CONTINUITY"}
    if journal.is_symlink() or not journal.is_dir():
        raise PendingCADAContinuity("UNSAFE_CADA_JOURNAL")
    manifest = _manifest(journal)
    for index, entry in enumerate(manifest["entries"]):
        path = root / entry["path"]
        old = journal / f"before_{index}.bin"
        if (not old.is_file() or old.is_symlink()
                or digest(old.read_bytes()) != entry["before_sha256"]):
            raise PendingCADAContinuity("CADA_BACKUP_CHANGED_MANUAL_REVIEW")
        if not path.is_file() or path.is_symlink():
            raise PendingCADAContinuity("CADA_CANONICAL_MISSING_MANUAL_REVIEW")
        actual = digest(path.read_bytes())
        if manifest["state"] == "COMMITTED":
            if actual != entry["after_sha256"]:
                raise PendingCADAContinuity("CADA_COMMITTED_OUTPUT_CHANGED_MANUAL_REVIEW")
        elif actual not in {entry["before_sha256"], entry["after_sha256"]}:
            raise PendingCADAContinuity("CADA_INDEPENDENT_EDIT_MANUAL_REVIEW")
    if manifest["state"] == "COMMITTED":
        shutil.rmtree(journal)
        return {"status": "COMMITTED_CADA_CONTINUITY_VERIFIED"}
    for index, entry in enumerate(manifest["entries"]):
        path = root / entry["path"]
        temp = journal / ("restore_" + str(index) + "_" + uuid4().hex + ".bin")
        try:
            sync_bytes(temp, (journal / f"before_{index}.bin").read_bytes())
            os.replace(temp, path)
        finally:
            temp.unlink(missing_ok=True)
    shutil.rmtree(journal)
    return {"status": "PREPARED_CADA_CONTINUITY_ROLLED_BACK"}


def apply(root: Path, new_contents: dict[str, bytes]) -> None:
    root = Path(root).resolve()
    require_no_conflict(root)
    if set(new_contents) != set(FILES):
        raise ValueError("CADA_CONTINUITY_REQUIRES_EXACT_THREE_FILES")
    old_contents: dict[str, bytes] = {}
    for rel in FILES:
        file = root / rel
        if file.is_symlink() or not file.is_file():
            raise ValueError("UNSAFE_OR_MISSING_CADA_CONTINUITY_FILE")
        old_contents[rel] = file.read_bytes()
        if not isinstance(new_contents[rel], bytes):
            raise ValueError("CADA_CONTINUITY_BYTES_REQUIRED")
    journal = journal_dir(root)
    try:
        journal.mkdir(mode=0o700)
    except FileExistsError as exc:
        raise PendingCADAContinuity("RECOVER_PENDING_CADA_CONTINUITY_FIRST") from exc

    prepared = False
    try:
        entries = []
        for index, rel in enumerate(FILES):
            old, new = old_contents[rel], new_contents[rel]
            sync_bytes(journal / f"before_{index}.bin", old)
            sync_bytes(journal / f"after_{index}.bin", new)
            entries.append({"path": rel, "before_sha256": digest(old),
                            "after_sha256": digest(new)})
        manifest = {"schema_version": 1, "state": "PREPARED", "entries": entries}
        sync_bytes(journal / "manifest.json",
                   (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        prepared = True
        # Detect a direct edit between preflight and the first replacement.
        for index, rel in enumerate(FILES):
            file = root / rel
            if file.is_symlink() or digest(file.read_bytes()) != entries[index]["before_sha256"]:
                raise PendingCADAContinuity("CADA_INPUT_CHANGED_BEFORE_COMMIT")
        for index, rel in enumerate(FILES):
            os.replace(journal / f"after_{index}.bin", root / rel)
        manifest["state"] = "COMMITTED"
        sync_bytes(journal / "manifest.next",
                   (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        os.replace(journal / "manifest.next", journal / "manifest.json")
        shutil.rmtree(journal)
    except Exception:
        if prepared:
            # Roll back ordinary interrupted writes, but preserve a journal
            # on mismatch instead of overwriting possible independent work.
            recover(root)
        else:
            shutil.rmtree(journal)
        raise
