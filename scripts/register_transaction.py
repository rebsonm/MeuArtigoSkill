"""Recoverable, single-writer update of Meu Artigo's three bibliographic CSVs.

A journal protects against interrupted multi-file updates. CSV files are not
a database transaction: concurrent direct readers must stop when a journal is
present. This module is restricted to explicitly authorized local fallback
projects, never a replacement for verified Google Drive synchronization.

No network calls, secrets, human approval or scientific claims are created.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
from uuid import uuid4
from transaction_coordinator import require_no_conflict

MGMT = "00_Gestao_e_Continuidade"
JOURNAL_NAME = ".pending_bibliographic_import"
FILES = (
    MGMT + "/02_Search_Log.csv",
    MGMT + "/03_Screening.csv",
    MGMT + "/13_Traceability_Log.csv",
)


class PendingTransaction(RuntimeError):
    pass


def journal_dir(root: Path) -> Path:
    return root / MGMT / JOURNAL_NAME


def has_pending_transaction(root: Path) -> bool:
    return journal_dir(Path(root)).exists()


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json_sync(file: Path, obj: dict) -> None:
    with file.open("w", encoding="utf-8") as fp:
        json.dump(obj, fp, ensure_ascii=False, indent=2)
        fp.write("\n")
        fp.flush()
        os.fsync(fp.fileno())


def _csv_sync(path: Path, headers: list[str], rows: list[dict], cell_filter) -> None:
    with path.open("x", encoding="utf-8-sig", newline="") as fp:
        w = csv.DictWriter(fp, fieldnames=headers)
        w.writeheader()
        w.writerows([{h: cell_filter(row.get(h, "")) for h in headers} for row in rows])
        fp.flush()
        os.fsync(fp.fileno())


def _restore_prepared(root: Path, journal: Path, manifest: dict) -> None:
    """Restore every before-image or fail visibly with the journal preserved."""
    entries = manifest["entries"]
    # Validate all backup hashes before touching any canonical file.
    for i, entry in enumerate(entries):
        backup = journal / ("before_" + str(i) + ".csv")
        if not backup.is_file() or _digest(backup) != entry["before_sha256"]:
            raise PendingTransaction("INCOMPLETE_BACKUPS_MANUAL_RECOVERY_REQUIRED")
    for i, entry in enumerate(entries):
        destination = root / entry["path"]
        temp = journal / ("restore_" + str(i) + "_" + uuid4().hex + ".csv")
        shutil.copyfile(journal / ("before_" + str(i) + ".csv"), temp)
        os.replace(temp, destination)


def recover_pending_transaction(root: Path) -> dict:
    """Explicit recovery; never claim a partial transaction was committed."""
    root = Path(root).resolve()
    require_no_conflict(root, allow=("bibliographic",))
    journal = journal_dir(root)
    if not journal.exists():
        return {"status": "NO_PENDING_TRANSACTION"}
    if not journal.is_dir() or journal.is_symlink():
        raise PendingTransaction("UNSAFE_JOURNAL_MANUAL_RECOVERY_REQUIRED")
    record = journal / "manifest.json"
    if not record.is_file():
        raise PendingTransaction("MISSING_TRANSACTION_MANIFEST_MANUAL_RECOVERY_REQUIRED")
    try:
        manifest = json.loads(record.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise PendingTransaction("INVALID_TRANSACTION_MANIFEST") from exc
    entries = manifest.get("entries")
    if (manifest.get("schema_version") != 1 or not isinstance(entries, list)
            or [e.get("path") for e in entries if isinstance(e, dict)] != list(FILES)
            or len(entries) != len(FILES)
            or manifest.get("state") not in {"PREPARED", "COMMITTED"}):
        raise PendingTransaction("INVALID_TRANSACTION_MANIFEST")
    if manifest["state"] == "COMMITTED":
        for i, entry in enumerate(entries):
            target = root / entry["path"]
            if not target.is_file() or _digest(target) != entry["after_sha256"]:
                raise PendingTransaction("COMMITTED_OUTPUT_CHANGED_MANUAL_REVIEW_REQUIRED")
        shutil.rmtree(journal)
        return {"status": "COMMITTED_CONFIRMED_AND_JOURNAL_CLEANED"}
    _restore_prepared(root, journal, manifest)
    shutil.rmtree(journal)
    return {"status": "PREPARED_IMPORT_ROLLED_BACK"}


def apply_register_transaction(root: Path, updates: dict, cell_filter) -> None:
    """All-or-rollback on ordinary exceptions; recoverable after process crash.

    Writers outside this protocol are not transaction-aware. No concurrent
    imports are allowed. A stale journal blocks further writes until recovered.
    """
    root = Path(root).resolve()
    require_no_conflict(root, allow=("bibliographic",))
    if set(updates) != set(FILES):
        raise ValueError("EXPECTED_EXACT_THREE_CANONICAL_REGISTERS")
    journal = journal_dir(root)
    try:
        journal.mkdir(mode=0o700)
    except FileExistsError as exc:
        raise PendingTransaction("PENDING_IMPORT_MUST_BE_RECOVERED_FIRST") from exc
    manifest = {"schema_version": 1, "state": "PREPARED", "entries": []}
    prepared = False
    try:
        for i, rel in enumerate(FILES):
            original = root / rel
            if not original.is_file() or original.is_symlink():
                raise ValueError("UNSAFE_OR_MISSING_CANONICAL_REGISTER")
            headers, rows = updates[rel]
            backup = journal / f"before_{i}.csv"
            after = journal / f"after_{i}.csv"
            shutil.copyfile(original, backup)
            _csv_sync(after, headers, rows, cell_filter)
            manifest["entries"].append({
                "path": rel,
                "before_sha256": _digest(backup),
                "after_sha256": _digest(after),
            })
        _json_sync(journal / "manifest.json", manifest)
        prepared = True
        for i, rel in enumerate(FILES):
            os.replace(journal / f"after_{i}.csv", root / rel)
        manifest["state"] = "COMMITTED"
        _json_sync(journal / "manifest.next", manifest)
        os.replace(journal / "manifest.next", journal / "manifest.json")
        # Keep a journal if cleanup fails; next explicit recovery verifies hashes.
        shutil.rmtree(journal)
    except Exception:
        if prepared:
            # Leave journal intact if restoration fails (visible hard blocker).
            recover_pending_transaction(root)
        else:
            shutil.rmtree(journal)
        raise
