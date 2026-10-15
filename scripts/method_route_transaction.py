"""Recoverable local transaction for a scientific method-route selection.

Five canonical files are journaled together: two decision/trace registers,
the project config, method profile and human validation gates. This is local
filesystem consistency only, never evidence of synced Google Drive state.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
from uuid import uuid4
from transaction_coordinator import require_no_conflict

MGMT = "00_Gestao_e_Continuidade"
JOURNAL = ".pending_method_route_change"
FILES = (
    "PROJECT_CONFIG.json",
    "METHOD_PROFILE.json",
    "18_Human_Validation_Gates.csv",
    "17_Decision_Log.csv",
    "13_Traceability_Log.csv",
)


class PendingMethodRouteTransaction(RuntimeError):
    pass


def require_authorized_local_canonical_storage(cfg: dict) -> None:
    """Fail closed before writing a local method route/field transaction.

    Drive-canonical projects cannot treat a potentially stale local mirror
    as the writable source of truth. The authorization is a declared local
    project flag, not independent proof of researcher identity or permission.
    """
    if (not isinstance(cfg, dict)
            or cfg.get("storage_mode") != "WORK_FALLBACK"
            or cfg.get("fallback_authorized") is not True):
        raise ValueError("AUTHORIZED_LOCAL_CANONICAL_STORAGE_REQUIRED")



def journal_dir(root: Path) -> Path:
    return Path(root) / MGMT / JOURNAL


def has_pending_method_route(root: Path) -> bool:
    return journal_dir(root).exists() or journal_dir(root).is_symlink()


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sync_bytes(path: Path, payload: bytes) -> None:
    with path.open("xb") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())


def _manifest_write(folder: Path, content: dict) -> None:
    tmp = folder / ("manifest_" + uuid4().hex + ".tmp")
    try:
        _sync_bytes(tmp, (json.dumps(content, sort_keys=True, indent=2) + "\n").encode("utf-8"))
        os.replace(tmp, folder / "manifest.json")
    finally:
        tmp.unlink(missing_ok=True)


def recover_method_route(root: Path) -> dict:
    """Explicitly reconcile a pending local journal; never infer a gate approval."""
    root = Path(root).resolve()
    require_no_conflict(root, allow=("method_route",))
    folder = journal_dir(root)
    if not folder.exists() and not folder.is_symlink():
        return {"status": "NO_PENDING_METHOD_ROUTE"}
    if folder.is_symlink() or not folder.is_dir():
        raise PendingMethodRouteTransaction("UNSAFE_METHOD_ROUTE_JOURNAL_MANUAL_RECOVERY_REQUIRED")
    mpath = folder / "manifest.json"
    if not mpath.is_file() or mpath.is_symlink():
        raise PendingMethodRouteTransaction("MISSING_METHOD_ROUTE_MANIFEST_MANUAL_RECOVERY_REQUIRED")
    try:
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise PendingMethodRouteTransaction("INVALID_METHOD_ROUTE_MANIFEST") from exc
    entries = manifest.get("entries")
    if (manifest.get("schema_version") != 1
            or manifest.get("state") not in {"PREPARED", "COMMITTED"}
            or not isinstance(entries, list)
            or len(entries) != len(FILES)
            or [entry.get("name") for entry in entries if isinstance(entry, dict)] != list(FILES)):
        raise PendingMethodRouteTransaction("INVALID_METHOD_ROUTE_MANIFEST")
    mgmt = root / MGMT
    # Check ALL backups before the first restoration; reject edited or unsafe
    # journal entries rather than using unverified bytes to rewrite research.
    for i, entry in enumerate(entries):
        original = folder / f"before_{i}"
        target = mgmt / entry["name"]
        if (not original.is_file() or original.is_symlink()
                or _sha(original) != entry.get("before_sha256")
                or not target.is_file() or target.is_symlink()):
            raise PendingMethodRouteTransaction("METHOD_ROUTE_BACKUP_OR_TARGET_CHANGED_MANUAL_REVIEW_REQUIRED")
    if manifest["state"] == "COMMITTED":
        if any(_sha(mgmt / entry["name"]) != entry.get("after_sha256") for entry in entries):
            raise PendingMethodRouteTransaction("COMMITTED_METHOD_ROUTE_CHANGED_MANUAL_REVIEW_REQUIRED")
        shutil.rmtree(folder)
        return {"status": "COMMITTED_METHOD_ROUTE_CONFIRMED_AND_JOURNAL_CLEANED"}
    for i, entry in enumerate(entries):
        target = mgmt / entry["name"]
        restore_tmp = folder / ("restore_" + str(i) + "_" + uuid4().hex)
        try:
            _sync_bytes(restore_tmp, (folder / f"before_{i}").read_bytes())
            os.replace(restore_tmp, target)
        finally:
            restore_tmp.unlink(missing_ok=True)
    shutil.rmtree(folder)
    return {"status": "PREPARED_METHOD_ROUTE_ROLLED_BACK"}


@contextmanager
def protect_method_route(root: Path):
    """Rollback normal failures; crashes leave a visible, recoverable journal."""
    root = Path(root).resolve()
    mgmt = root / MGMT
    require_no_conflict(root, allow=("method_route",))
    folder = journal_dir(root)
    try:
        folder.mkdir(mode=0o700)
    except FileExistsError as exc:
        raise PendingMethodRouteTransaction("METHOD_ROUTE_TRANSACTION_PENDING_RECOVERY_REQUIRED") from exc
    try:
        entries = []
        for i, name in enumerate(FILES):
            src = mgmt / name
            if not src.is_file() or src.is_symlink():
                raise PendingMethodRouteTransaction("MISSING_OR_UNSAFE_METHOD_ROUTE_CANONICAL_FILE")
            backup = folder / f"before_{i}"
            _sync_bytes(backup, src.read_bytes())
            entries.append({"name": name, "before_sha256": _sha(backup)})
        manifest = {"schema_version": 1, "state": "PREPARED", "entries": entries}
        _manifest_write(folder, manifest)
    except Exception:
        shutil.rmtree(folder)
        raise
    try:
        yield
        for entry in entries:
            dest = mgmt / entry["name"]
            if not dest.is_file() or dest.is_symlink():
                raise PendingMethodRouteTransaction("MISSING_METHOD_ROUTE_OUTPUT")
            entry["after_sha256"] = _sha(dest)
        manifest["state"] = "COMMITTED"
        _manifest_write(folder, manifest)
    except Exception:
        recover_method_route(root)
        raise
    else:
        shutil.rmtree(folder)
