"""Crash-aware local journal for gate/TRACE/snapshot registry coordination.

No journal implies a real human verified anything. A snapshot created before
an interruption is immutable evidence: NEVER delete it automatically.
Drive synchronization is outside this local filesystem transaction.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
from uuid import uuid4

MGMT = "00_Gestao_e_Continuidade"
JOURNAL_NAME = ".pending_gate_snapshot"
REGISTERS = ("13_Traceability_Log.csv", "18_Human_Validation_Gates.csv",
             "19_Snapshots.csv")


class PendingGateSnapshot(RuntimeError):
    pass


def journal_dir(root: Path) -> Path:
    return Path(root) / MGMT / JOURNAL_NAME


def has_pending_gate_snapshot(root: Path) -> bool:
    path = journal_dir(root)
    return path.exists() or path.is_symlink()


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_sync(path: Path, content: bytes) -> None:
    with path.open("xb") as out:
        out.write(content)
        out.flush()
        os.fsync(out.fileno())


def _write_manifest(journal: Path, obj: dict) -> None:
    dest = journal / "manifest.json"
    temp = journal / ("manifest-" + uuid4().hex + ".tmp")
    try:
        _write_sync(temp, (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode())
        os.replace(temp, dest)
    finally:
        temp.unlink(missing_ok=True)


def _snapshot_names(root: Path) -> set[str]:
    folder = Path(root) / MGMT / "Snapshots"
    if folder.is_symlink():
        raise PendingGateSnapshot("UNSAFE_SNAPSHOT_ROOT_MANUAL_REVIEW_REQUIRED")
    if not folder.exists():
        return set()
    if not folder.is_dir():
        raise PendingGateSnapshot("INVALID_SNAPSHOT_ROOT_MANUAL_REVIEW_REQUIRED")
    return {p.name for p in folder.iterdir()}


def recover_gate_snapshot(root: Path) -> dict:
    """Restore PREPARED registers if no new immutable snapshot appeared.

    If a snapshot was created, preserve it and keep the journal as a hard
    blocker; resolving such a collision requires an explicit audit.
    """
    root = Path(root).resolve()
    journal = journal_dir(root)
    if not has_pending_gate_snapshot(root):
        return {"status": "NO_PENDING_GATE_SNAPSHOT"}
    if journal.is_symlink() or not journal.is_dir():
        raise PendingGateSnapshot("UNSAFE_GATE_JOURNAL_MANUAL_REVIEW_REQUIRED")
    mpath = journal / "manifest.json"
    if not mpath.is_file() or mpath.is_symlink():
        raise PendingGateSnapshot("MISSING_GATE_MANIFEST_MANUAL_REVIEW_REQUIRED")
    try:
        data = json.loads(mpath.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise PendingGateSnapshot("INVALID_GATE_MANIFEST") from exc
    entries = data.get("entries")
    if (data.get("schema_version") != 1
            or data.get("state") not in {"PREPARED", "COMMITTED"}
            or not isinstance(entries, list)
            or len(entries) != len(REGISTERS)
            or [x.get("name") for x in entries if isinstance(x, dict)] != list(REGISTERS)
            or not isinstance(data.get("snapshot_names"), list)):
        raise PendingGateSnapshot("INVALID_GATE_MANIFEST")
    root_snapshots = _snapshot_names(root)
    baseline = set(data["snapshot_names"])
    newly_created = sorted(root_snapshots - baseline)
    for idx, entry in enumerate(entries):
        dest = root / MGMT / entry["name"]
        if dest.is_symlink() or (dest.exists() and not dest.is_file()):
            raise PendingGateSnapshot("GATE_REGISTER_UNSAFE_MANUAL_REVIEW_REQUIRED")
        before = journal / f"before_{idx}"
        if entry.get("existed") is True:
            if (not before.is_file() or before.is_symlink()
                    or _hash(before) != entry.get("before_sha256")):
                raise PendingGateSnapshot("GATE_BACKUP_CORRUPTED_MANUAL_REVIEW_REQUIRED")
        elif entry.get("existed") is not False:
            raise PendingGateSnapshot("INVALID_GATE_MANIFEST")
    if data["state"] == "COMMITTED":
        if any((not (root / MGMT / e["name"]).is_file()
                or _hash(root / MGMT / e["name"]) != e.get("after_sha256"))
               for e in entries):
            raise PendingGateSnapshot("COMMITTED_GATE_OUTPUT_CHANGED_MANUAL_REVIEW_REQUIRED")
        if set(data.get("committed_snapshot_names", [])) != newly_created:
            raise PendingGateSnapshot("COMMITTED_GATE_SNAPSHOT_MISMATCH_MANUAL_REVIEW_REQUIRED")
        shutil.rmtree(journal)
        return {"status": "COMMITTED_GATE_SNAPSHOT_VERIFIED_AND_CLEANED"}
    if newly_created:
        raise PendingGateSnapshot(
            "ORPHANED_GATE_SNAPSHOT_REQUIRES_RECONCILIATION: "
            + ", ".join(newly_created))
    for idx, entry in enumerate(entries):
        target = root / MGMT / entry["name"]
        if entry["existed"]:
            tmp = journal / ("restore-" + str(idx) + "-" + uuid4().hex)
            try:
                _write_sync(tmp, (journal / f"before_{idx}").read_bytes())
                os.replace(tmp, target)
            finally:
                tmp.unlink(missing_ok=True)
        elif target.exists():
            target.unlink()
    shutil.rmtree(journal)
    return {"status": "PREPARED_GATE_SNAPSHOT_ROLLED_BACK"}


@contextmanager
def protect_gate_snapshot(root: Path):
    root = Path(root).resolve()
    mgmt = root / MGMT
    baseline = sorted(_snapshot_names(root))
    journal = journal_dir(root)
    try:
        journal.mkdir(mode=0o700)
    except FileExistsError as exc:
        raise PendingGateSnapshot("PENDING_GATE_SNAPSHOT_MUST_BE_RECOVERED") from exc
    try:
        entries = []
        for idx, name in enumerate(REGISTERS):
            src = mgmt / name
            if src.is_symlink() or (src.exists() and not src.is_file()):
                raise PendingGateSnapshot("UNSAFE_GATE_REGISTER")
            exists = src.exists()
            entry = {"name": name, "existed": exists}
            if exists:
                backup = journal / f"before_{idx}"
                _write_sync(backup, src.read_bytes())
                entry["before_sha256"] = _hash(backup)
            entries.append(entry)
        state = {"schema_version": 1, "state": "PREPARED",
                 "entries": entries, "snapshot_names": baseline}
        _write_manifest(journal, state)
    except Exception:
        shutil.rmtree(journal)
        raise
    try:
        yield
        for entry in entries:
            path = mgmt / entry["name"]
            if not path.is_file() or path.is_symlink():
                raise PendingGateSnapshot("MISSING_GATE_OUTPUT")
            entry["after_sha256"] = _hash(path)
        state["state"] = "COMMITTED"
        state["committed_snapshot_names"] = sorted(_snapshot_names(root) - set(baseline))
        _write_manifest(journal, state)
    except Exception:
        recover_gate_snapshot(root)
        raise
    else:
        shutil.rmtree(journal)
